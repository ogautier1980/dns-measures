#!/usr/bin/env python3
"""
Étape 2 du pipeline — Sélection des sondes RIPE Atlas et création des campagnes.

Fonctionnement :
  1. Récupère toutes les sondes actives satisfaisant les critères de qualité
  2. Stratifie par continent selon la table du chapitre 3 (30/25/20/10/10/5)
  3. Dans chaque strate, sélectionne les sondes en maximisant la diversité AS
  4. Lit le corpus de domaines (tranco_corpus.csv) et les groupe par NS faisant autorité
  5. Crée une mesure DNS RIPE Atlas par groupe de domaines (batch de 100 max)
  6. En mode --dry-run, affiche le plan sans créer de mesures

Usage :
  python create_ripe_measurements.py [--corpus data/processed/tranco_corpus.csv]
                                     [--output data/processed/measurements.json]
                                     [--dry-run]

Variables d'environnement :
  RIPE_ATLAS_API_KEY   Clé API RIPE Atlas (obligatoire hors dry-run)
"""

import argparse
import csv
import json
import logging
import os
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

API_BASE = "https://atlas.ripe.net/api/v2"
API_KEY  = os.getenv("RIPE_ATLAS_API_KEY", "")

# ── Allocation sondes par continent (chapitre 3, tableau 3.1) ─────────────────
# Proportions par continent (sum = 1.0) — les quotas absolus sont calculés
# dynamiquement selon --total-probes pour faciliter l'ajustement du budget.
CONTINENT_PROPORTIONS = {
    "EU": 0.30,   # Europe
    "NA": 0.25,   # Amérique du Nord
    "AP": 0.20,   # Asie-Pacifique
    "SA": 0.10,   # Amérique du Sud
    "AF": 0.10,   # Afrique
    "OC": 0.05,   # Océanie
}
# Valeur par défaut : 50 sondes → ~125 000 crédits/jour pour 500 domaines
DEFAULT_TOTAL_PROBES = 50
DEFAULT_MAX_DOMAINS  = 100   # top-100 Tranco (ajustable selon budget)

# Mapping pays → continent (ISO 3166-1 alpha-2 → code interne)
# Basé sur la classification standard ONU des régions
_EU_COUNTRIES = {
    "AL","AD","AT","BY","BE","BA","BG","HR","CY","CZ","DK","EE","FI","FR",
    "DE","GR","HU","IS","IE","IT","XK","LV","LI","LT","LU","MT","MD","MC",
    "ME","NL","MK","NO","PL","PT","RO","RU","SM","RS","SK","SI","ES","SE",
    "CH","UA","GB","VA",
}
_NA_COUNTRIES = {
    "AG","BS","BB","BZ","CA","CR","CU","DM","DO","SV","GD","GT","HT","HN",
    "JM","MX","NI","PA","KN","LC","VC","TT","US",
}
_SA_COUNTRIES = {
    "AR","BO","BR","CL","CO","EC","GY","PY","PE","SR","UY","VE",
}
_AF_COUNTRIES = {
    "DZ","AO","BJ","BW","BF","BI","CV","CM","CF","TD","KM","CG","CD","CI",
    "DJ","EG","GQ","ER","SZ","ET","GA","GM","GH","GN","GW","KE","LS","LR",
    "LY","MG","MW","ML","MR","MU","MA","MZ","NA","NE","NG","RW","ST","SN",
    "SL","SO","ZA","SS","SD","TZ","TG","TN","UG","ZM","ZW",
}
_OC_COUNTRIES = {
    "AU","FJ","KI","MH","FM","NR","NZ","PW","PG","WS","SB","TO","TV","VU",
}


def country_to_continent(cc: str) -> str:
    cc = (cc or "").upper()
    if cc in _EU_COUNTRIES:  return "EU"
    if cc in _NA_COUNTRIES:  return "NA"
    if cc in _SA_COUNTRIES:  return "SA"
    if cc in _AF_COUNTRIES:  return "AF"
    if cc in _OC_COUNTRIES:  return "OC"
    return "AP"   # défaut : Asie-Pacifique


# ──────────────────────────────────────────────────────────────────────────────
# Récupération des sondes RIPE Atlas
# ──────────────────────────────────────────────────────────────────────────────

def fetch_probes() -> list[dict]:
    """
    Récupère toutes les sondes actives avec :
      - status=1 (connected)
      - tags : system-ipv4-works, system-resolves-a-correctly
      - hardware version >= 3
    """
    log.info("Récupération des sondes RIPE Atlas actives…")
    params = {
        "status":        1,
        "tags":          "system-ipv4-works,system-resolves-a-correctly",
        "hardware_version__gte": 3,
        "fields":        "id,country_code,asn_v4,geometry,hardware_version,status",
        "format":        "json",
        "page_size":     500,
    }
    headers = {"Authorization": f"Key {API_KEY}"} if API_KEY else {}
    url     = f"{API_BASE}/probes/"
    probes  = []

    while url:
        r = requests.get(url, params=params, headers=headers, timeout=60)
        r.raise_for_status()
        data   = r.json()
        batch  = data.get("results", [])
        probes.extend(batch)
        url    = data.get("next")
        params = {}   # l'URL suivante contient déjà tous les paramètres
        log.debug("  … %d sondes récupérées", len(probes))
        time.sleep(0.2)

    log.info("Total sondes candidates : %d", len(probes))
    return probes


# ──────────────────────────────────────────────────────────────────────────────
# Sélection stratifiée
# ──────────────────────────────────────────────────────────────────────────────

def build_continent_quota(total_probes: int) -> dict[str, int]:
    """Calcule les quotas par continent selon les proportions et le total demandé."""
    quota = {}
    allocated = 0
    continents = list(CONTINENT_PROPORTIONS.keys())
    for i, cont in enumerate(continents):
        if i == len(continents) - 1:
            quota[cont] = total_probes - allocated
        else:
            quota[cont] = max(1, round(total_probes * CONTINENT_PROPORTIONS[cont]))
            allocated += quota[cont]
    return quota


def select_probes_stratified(probes: list[dict], total_probes: int = DEFAULT_TOTAL_PROBES) -> list[dict]:
    """
    Sélectionne exactement total_probes sondes selon les quotas continentaux,
    en maximisant la diversité des systèmes autonomes dans chaque strate.
    """
    continent_quota = build_continent_quota(total_probes)
    log.info("Quotas par continent : %s  (total=%d)", continent_quota, total_probes)

    # Grouper par continent
    by_continent: dict[str, list[dict]] = defaultdict(list)
    for p in probes:
        cc   = p.get("country_code", "")
        cont = country_to_continent(cc)
        by_continent[cont].append(p)

    selected = []

    for continent, quota in continent_quota.items():
        candidates = by_continent[continent]
        log.info("  %s : %d candidats → quota %d", continent, len(candidates), quota)

        if not candidates:
            log.warning("  Aucune sonde disponible pour %s !", continent)
            continue

        # Trier par ASN pour grouper, puis round-robin entre AS distincts
        by_as: dict[int, list[dict]] = defaultdict(list)
        for p in candidates:
            asn = p.get("asn_v4") or 0
            by_as[asn].append(p)

        # Round-robin AS : prend 1 sonde par AS jusqu'à atteindre le quota
        chosen: list[dict] = []
        as_lists  = list(by_as.values())
        as_index  = 0
        per_as_count: dict[int, int] = defaultdict(int)

        while len(chosen) < quota and as_lists:
            # Premier passage : 1 sonde par AS
            added_this_round = 0
            for as_probes in as_lists:
                if len(chosen) >= quota:
                    break
                as_probes.sort(key=lambda p: p.get("hardware_version", 0), reverse=True)
                # Prend la première sonde pas encore choisie de cet AS
                for probe in as_probes:
                    if probe not in chosen:
                        chosen.append(probe)
                        per_as_count[probe.get("asn_v4")] += 1
                        added_this_round += 1
                        break
            if added_this_round == 0:
                break   # Plus de sondes disponibles

        selected.extend(chosen)
        log.info("    → %d sondes sélectionnées (%d AS distincts)",
                 len(chosen), len({p.get("asn_v4") for p in chosen}))

    log.info("Total sondes sélectionnées : %d / %d", len(selected), total_probes)
    return selected


# ──────────────────────────────────────────────────────────────────────────────
# Lecture du corpus
# ──────────────────────────────────────────────────────────────────────────────

def load_corpus(csv_path: Path) -> list[dict]:
    """Charge le corpus CSV : [{rank, domain, ns}, ...]"""
    corpus = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["ns"] = [ns for ns in row.get("ns", "").split("|") if ns]
            corpus.append(row)
    log.info("Corpus chargé : %d domaines depuis %s", len(corpus), csv_path)
    return corpus


def resolve_ns_ip(ns_hostname: str) -> str | None:
    """Résout l'IP d'un NS hostname (simple, sans cache)."""
    import dns.resolver
    try:
        ans = dns.resolver.resolve(ns_hostname, "A")
        return str(ans[0])
    except Exception:
        return None


# ──────────────────────────────────────────────────────────────────────────────
# Création des mesures RIPE Atlas
# ──────────────────────────────────────────────────────────────────────────────

BATCH_SIZE    = 100   # domaines par mesure (limite API RIPE Atlas)
RATE_LIMIT_S  = 1.0   # délai entre les appels POST

def build_measurement_def(
    domain: str,
    ns_ip: str,
    probe_ids: list[int],
    date_label: str,
    is_oneoff: bool = False,
) -> dict:
    """Construit le payload JSON d'une mesure DNS RIPE Atlas (type dns)."""
    return {
        "definitions": [{
            "type":             "dns",
            "af":               4,
            "target":           ns_ip,
            "query_type":       "A",
            "query_class":      "IN",
            "query_argument":   domain,
            "use_probe_resolver": False,
            "set_rd_bit":       False,
            "set_nsid_bit":     True,
            "set_do_bit":       False,
            "set_cd_bit":       False,
            "protocol":         "UDP",
            "udp_payload_size": 1024,
            "include_abuf":     True,
            "retry":            2,
            "timeout":          5000,
            "is_oneoff":        is_oneoff,
            "interval":         86400,
            "description":      f"DNS geo-diversity - auth - {domain} - {date_label}",
        }],
        "probes": [{
            "type":      "probes",
            "value":     ",".join(str(pid) for pid in probe_ids),
            "requested": len(probe_ids),
        }],
        "is_oneoff": is_oneoff,
    }


def create_measurement(payload: dict, dry_run: bool = False) -> int | None:
    """
    Envoie la requête de création à l'API RIPE Atlas.
    Retourne le measurement ID, ou None en dry-run / erreur.
    """
    if dry_run:
        log.info("  [DRY-RUN] Mesure : %s",
                 payload["definitions"][0]["description"])
        return None

    if not API_KEY:
        log.error("RIPE_ATLAS_API_KEY non définie — impossible de créer des mesures.")
        return None

    url     = f"{API_BASE}/measurements/"
    headers = {
        "Authorization": f"Key {API_KEY}",
        "Content-Type":  "application/json",
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)

    if r.status_code == 201:
        msm_id = r.json()["measurements"][0]
        log.info("  Mesure créée : id=%d  domain=%s",
                 msm_id, payload["definitions"][0]["query_argument"])
        return msm_id
    else:
        log.error("  Erreur API (%d) : %s", r.status_code, r.text[:200])
        return None


# ──────────────────────────────────────────────────────────────────────────────
# Campagne principale (Q1 / Q2 / Q3) — NS faisant autorité
# ──────────────────────────────────────────────────────────────────────────────

def run_authoritative_campaign(
    corpus: list[dict],
    probe_ids: list[int],
    date_label: str,
    dry_run: bool,
    max_domains: int = DEFAULT_MAX_DOMAINS,
) -> list[dict]:
    """
    Crée une mesure par domaine (top max_domains), ciblant le NS faisant autorité primaire.
    Retourne la liste des mesures créées : [{domain, ns_ip, msm_id}, ...].
    """
    corpus = corpus[:max_domains]
    n_probes = len(probe_ids)
    credits_est = len(corpus) * n_probes * 10
    log.info("Campagne principale (NS faisant autorité) — %d domaines × %d sondes"
             " ≈ %s crédits/jour",
             len(corpus), n_probes, f"{credits_est:,}")
    created = []
    skipped = 0

    for i, entry in enumerate(corpus, 1):
        domain  = entry["domain"]
        ns_list = entry.get("ns", [])

        if not ns_list:
            log.debug("  Pas de NS connu pour %s — ignoré", domain)
            skipped += 1
            continue

        # Prend le NS primaire (premier de la liste pré-résolue)
        ns_primary = ns_list[0]
        ns_ip = resolve_ns_ip(ns_primary)
        if not ns_ip:
            log.debug("  NS IP non résolu pour %s (%s) — ignoré", domain, ns_primary)
            skipped += 1
            continue

        payload = build_measurement_def(domain, ns_ip, probe_ids, date_label)
        msm_id  = create_measurement(payload, dry_run=dry_run)

        created.append({
            "domain":  domain,
            "ns_host": ns_primary,
            "ns_ip":   ns_ip,
            "msm_id":  msm_id,
        })

        if i % 100 == 0:
            log.info("  Progression : %d/%d  skipped=%d", i, len(corpus), skipped)

        if not dry_run:
            time.sleep(RATE_LIMIT_S)

    log.info("Campagne principale : %d mesures créées, %d ignorées",
             len([c for c in created if c["msm_id"]]), skipped)
    return created


# ──────────────────────────────────────────────────────────────────────────────
# Campagne Q4 — Comparaison résolveurs (ISP local vs DNS public)
# ──────────────────────────────────────────────────────────────────────────────

Q4_RESOLVERS = {
    "isp_local":   None,          # use_probe_resolver=True
    "google":      "8.8.8.8",
    "cloudflare":  "1.1.1.1",
    "quad9":       "9.9.9.9",
}
Q4_SAMPLE_SIZE = 50    # sous-ensemble de domaines pour Q4 (défaut)


def build_q4_measurement(
    domain: str,
    resolver_name: str,
    resolver_ip: str | None,
    probe_ids: list[int],
    date_label: str,
) -> dict:
    """Construit une mesure via résolveur récursif (pour Q4)."""
    defn = {
        "type":           "dns",
        "af":             4,
        "query_type":     "A",
        "query_class":    "IN",
        "query_argument": domain,
        "set_rd_bit":     True,   # recursion désirée
        "set_nsid_bit":   False,
        "protocol":       "UDP",
        "udp_payload_size": 4096,
        "include_abuf":   True,
        "retry":          2,
        "timeout":        5000,
        "is_oneoff":      True,   # campagne ponctuelle pour Q4
        "description":    f"DNS Q4 resolver={resolver_name} {domain} {date_label}",
    }

    if resolver_ip:
        defn["target"]              = resolver_ip
        defn["use_probe_resolver"]  = False
    else:
        defn["use_probe_resolver"]  = True   # résolveur ISP local

    return {
        "definitions": [defn],
        "probes": [{
            "type":      "probes",
            "value":     ",".join(str(pid) for pid in probe_ids),
            "requested": len(probe_ids),
        }],
        "is_oneoff": True,
    }


def run_q4_campaign(
    corpus: list[dict],
    probe_ids: list[int],
    date_label: str,
    dry_run: bool,
    q4_sample: int = Q4_SAMPLE_SIZE,
) -> list[dict]:
    """
    Crée les mesures de comparaison de résolveurs pour Q4 (one-off).
    Utilise un sous-échantillon des q4_sample premiers domaines du corpus.
    """
    sample   = corpus[:q4_sample]
    created  = []
    n_probes = len(probe_ids)
    credits_est = len(sample) * len(Q4_RESOLVERS) * n_probes * 10
    log.info("Campagne Q4 (comparaison résolveurs) — %d domaines × %d résolveurs"
             " ≈ %s crédits (one-off)",
             len(sample), len(Q4_RESOLVERS), f"{credits_est:,}")

    for domain_entry in sample:
        domain = domain_entry["domain"]
        for resolver_name, resolver_ip in Q4_RESOLVERS.items():
            payload = build_q4_measurement(
                domain, resolver_name, resolver_ip, probe_ids, date_label
            )
            msm_id = create_measurement(payload, dry_run=dry_run)
            created.append({
                "domain":        domain,
                "resolver_name": resolver_name,
                "resolver_ip":   resolver_ip or "probe_local",
                "msm_id":        msm_id,
            })
            if not dry_run:
                time.sleep(RATE_LIMIT_S)

    log.info("Campagne Q4 : %d mesures créées",
             len([c for c in created if c["msm_id"]]))
    return created


# ──────────────────────────────────────────────────────────────────────────────
# Sauvegarde du plan de mesures
# ──────────────────────────────────────────────────────────────────────────────

def save_measurement_plan(
    probe_ids: list[int],
    auth_measurements: list[dict],
    q4_measurements: list[dict],
    date_label: str,
    output_path: Path,
) -> None:
    plan = {
        "created_at":        datetime.now(timezone.utc).isoformat(),
        "date_label":        date_label,
        "probe_ids":         probe_ids,
        "authoritative": {
            "count":         len(auth_measurements),
            "measurements":  auth_measurements,
        },
        "q4_resolver_comparison": {
            "count":         len(q4_measurements),
            "measurements":  q4_measurements,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(plan, indent=2))
    log.info("Plan de mesures sauvegardé : %s", output_path)


# ──────────────────────────────────────────────────────────────────────────────
# Point d'entrée
# ──────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sélectionne les sondes RIPE Atlas et crée les campagnes DNS."
    )
    parser.add_argument(
        "--corpus", type=str, default="data/processed/tranco_corpus.csv",
        help="Corpus de domaines (sortie de fetch_tranco.py)"
    )
    parser.add_argument(
        "--output", type=str, default="data/processed/measurements.json",
        help="Fichier JSON de sortie avec les IDs de mesures créées"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Affiche le plan sans créer de mesures RIPE Atlas"
    )
    parser.add_argument(
        "--q4-only", action="store_true",
        help="Crée uniquement la campagne Q4 (comparaison résolveurs)"
    )
    parser.add_argument(
        "--max-domains", type=int, default=DEFAULT_MAX_DOMAINS,
        help=f"Nombre max de domaines pour la campagne principale (défaut: {DEFAULT_MAX_DOMAINS})"
    )
    parser.add_argument(
        "--total-probes", type=int, default=DEFAULT_TOTAL_PROBES,
        help=f"Nombre total de sondes à sélectionner (défaut: {DEFAULT_TOTAL_PROBES})"
    )
    parser.add_argument(
        "--q4-sample", type=int, default=Q4_SAMPLE_SIZE,
        help=f"Nombre de domaines dans la campagne Q4 (défaut: {Q4_SAMPLE_SIZE})"
    )
    args = parser.parse_args()

    corpus_path  = Path(args.corpus)
    output_path  = Path(args.output)
    date_label   = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # ── Estimation du budget ──────────────────────────────────────────────────
    daily_main = args.max_domains * args.total_probes * 10
    oneoff_q4  = args.q4_sample * len(Q4_RESOLVERS) * args.total_probes * 10
    log.info("Budget estimé : %s crédits/jour (main) + %s crédits (Q4 one-off)",
             f"{daily_main:,}", f"{oneoff_q4:,}")

    if not corpus_path.exists():
        log.error("Corpus introuvable : %s  — lancez d'abord fetch_tranco.py", corpus_path)
        return 1

    # 1. Récupérer et sélectionner les sondes
    probes    = fetch_probes()
    selected  = select_probes_stratified(probes, total_probes=args.total_probes)
    probe_ids = [p["id"] for p in selected]

    if not probe_ids:
        log.error("Aucune sonde sélectionnée — arrêt.")
        return 1

    # Sauvegarder la sélection de sondes pour reproductibilité
    probes_path = output_path.parent / f"selected_probes_{date_label}.json"
    probes_path.parent.mkdir(parents=True, exist_ok=True)
    probes_path.write_text(json.dumps(
        [{"id": p["id"], "country": p.get("country_code"),
          "asn": p.get("asn_v4"), "hw": p.get("hardware_version")}
         for p in selected],
        indent=2
    ))
    log.info("Sondes sélectionnées sauvegardées : %s", probes_path)

    # 2. Charger le corpus
    corpus = load_corpus(corpus_path)

    # 3. Campagne principale (NS faisant autorité)
    auth_measurements = []
    if not args.q4_only:
        auth_measurements = run_authoritative_campaign(
            corpus, probe_ids, date_label,
            dry_run=args.dry_run, max_domains=args.max_domains,
        )

    # 4. Campagne Q4 (comparaison résolveurs)
    q4_measurements = run_q4_campaign(
        corpus, probe_ids, date_label,
        dry_run=args.dry_run, q4_sample=args.q4_sample,
    )

    # 5. Sauvegarder le plan
    save_measurement_plan(
        probe_ids, auth_measurements, q4_measurements, date_label, output_path
    )

    log.info("Étape 2 terminée — plan sauvegardé dans %s", output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
