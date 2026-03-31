#!/usr/bin/env python3
"""
Étape 1 du pipeline — Récupération et filtrage de la liste Tranco Top 10 000.

Fonctionnement :
  1. Télécharge la liste Tranco Top 10K via l'API officielle (https://tranco-list.eu/api)
  2. Valide chaque domaine : requête DNS A locale (exclut NXDOMAIN / SERVFAIL)
  3. Pré-résout les NS faisant autorité pour chaque domaine
  4. Sauvegarde le corpus final en CSV + JSON (avec identifiant Tranco pour reproductibilité)
  5. Enregistre le delta par rapport à la liste précédente (si elle existe)

Usage :
  python fetch_tranco.py [--list-id ID] [--output data/processed/] [--no-validate]

Sans --list-id, télécharge la liste la plus récente.
Avec --list-id, récupère une liste Tranco archivée spécifique (reproductibilité).
"""

import argparse
import csv
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import dns.resolver
import dns.exception
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

TRANCO_API   = "https://tranco-list.eu/api/lists/date/"
TRANCO_DL    = "https://tranco-list.eu/download/{list_id}/10000"
TOP_N        = 10_000
DNS_TIMEOUT  = 3.0   # secondes
DNS_RETRIES  = 1


# ──────────────────────────────────────────────────────────────────────────────
# Téléchargement Tranco
# ──────────────────────────────────────────────────────────────────────────────

def get_latest_list_id() -> tuple[str, str]:
    """
    Retourne (list_id, date_str) de la liste Tranco la plus récente disponible.
    Remonte jusqu'à 7 jours en arrière si la liste du jour n'est pas encore publiée.
    """
    from datetime import timedelta
    base = datetime.now(timezone.utc)
    for delta in range(7):
        candidate = (base - timedelta(days=delta)).strftime("%Y-%m-%d")
        url = f"{TRANCO_API}{candidate}"
        log.info("Interrogation API Tranco : %s", url)
        r = requests.get(url, timeout=30)
        if r.status_code == 404:
            log.debug("  Pas de liste pour %s — on remonte…", candidate)
            continue
        r.raise_for_status()
        data     = r.json()
        list_id  = data["list_id"]
        date_str = data.get("date", candidate)
        log.info("Liste Tranco : id=%s  date=%s", list_id, date_str)
        return list_id, date_str
    raise RuntimeError("Impossible de trouver une liste Tranco récente (7 jours)")


def download_tranco(list_id: str) -> list[tuple[int, str]]:
    """Télécharge les TOP_N domaines et retourne [(rank, domain), ...]."""
    url = TRANCO_DL.format(list_id=list_id)
    log.info("Téléchargement : %s", url)
    r = requests.get(url, timeout=120, stream=True)
    r.raise_for_status()

    entries: list[tuple[int, str]] = []
    for line in r.iter_lines():
        line = line.decode("utf-8").strip()
        if not line:
            continue
        parts = line.split(",", 1)
        if len(parts) == 2:
            rank, domain = int(parts[0]), parts[1].strip().lower()
            entries.append((rank, domain))
        if len(entries) >= TOP_N:
            break

    log.info("Téléchargé : %d domaines", len(entries))
    return entries


# ──────────────────────────────────────────────────────────────────────────────
# Validation DNS
# ──────────────────────────────────────────────────────────────────────────────

def make_resolver() -> dns.resolver.Resolver:
    res = dns.resolver.Resolver()
    res.timeout      = DNS_TIMEOUT
    res.lifetime     = DNS_TIMEOUT * (DNS_RETRIES + 1)
    res.nameservers  = ["8.8.8.8", "1.1.1.1"]   # résolveurs de référence stables
    return res


def check_domain_a(domain: str, resolver: dns.resolver.Resolver) -> bool:
    """Retourne True si le domaine a au moins un enregistrement A valide."""
    try:
        resolver.resolve(domain, "A")
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer,
            dns.resolver.NoNameservers, dns.exception.Timeout,
            dns.resolver.LifetimeTimeout):
        return False
    except Exception as exc:
        log.debug("check_a(%s) : %s", domain, exc)
        return False


def resolve_ns(domain: str, resolver: dns.resolver.Resolver) -> list[str]:
    """Retourne la liste des NS faisant autorité pour le domaine."""
    try:
        ans = resolver.resolve(domain, "NS")
        return sorted(str(r.target).rstrip(".").lower() for r in ans)
    except Exception:
        return []


def validate_corpus(
    entries: list[tuple[int, str]],
    skip_validate: bool = False,
) -> list[dict]:
    """
    Valide chaque domaine et retourne la liste des domaines actifs avec leurs NS.
    Chaque entrée : {rank, domain, ns_list, valid}.
    """
    resolver  = make_resolver()
    corpus    = []
    excluded  = 0
    total     = len(entries)

    log.info("Validation DNS de %d domaines (skip=%s)…", total, skip_validate)

    for i, (rank, domain) in enumerate(entries, 1):
        if i % 500 == 0:
            log.info("  %d/%d  exclus jusqu'ici : %d", i, total, excluded)

        if skip_validate:
            corpus.append({"rank": rank, "domain": domain, "ns": [], "valid": True})
            continue

        valid = check_domain_a(domain, resolver)
        if not valid:
            excluded += 1
            log.debug("  EXCLUS (pas de A) : %s", domain)
            continue

        ns_list = resolve_ns(domain, resolver)
        corpus.append({"rank": rank, "domain": domain, "ns": ns_list, "valid": True})

        # Petite pause pour ne pas surcharger les résolveurs publics
        if i % 100 == 0:
            time.sleep(0.1)

    log.info("Validation terminée : %d actifs, %d exclus (%.1f%%)",
             len(corpus), excluded, 100 * excluded / total if total else 0)
    return corpus


# ──────────────────────────────────────────────────────────────────────────────
# Delta (comparaison avec liste précédente)
# ──────────────────────────────────────────────────────────────────────────────

def compute_delta(
    new_domains: set[str],
    prev_file: Path,
) -> dict:
    """Compare avec la liste précédente et retourne un résumé du delta."""
    if not prev_file.exists():
        return {"added": len(new_domains), "removed": 0, "stable": 0}

    prev_domains: set[str] = set()
    with open(prev_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prev_domains.add(row["domain"])

    added   = new_domains - prev_domains
    removed = prev_domains - new_domains
    stable  = new_domains & prev_domains

    log.info("Delta : +%d  -%d  stables=%d  (%.2f%% de changement)",
             len(added), len(removed), len(stable),
             100 * len(added) / len(new_domains) if new_domains else 0)
    return {"added": len(added), "removed": len(removed), "stable": len(stable)}


# ──────────────────────────────────────────────────────────────────────────────
# Sauvegarde
# ──────────────────────────────────────────────────────────────────────────────

def save_corpus(
    corpus: list[dict],
    list_id: str,
    date_str: str,
    delta: dict,
    output_dir: Path,
) -> tuple[Path, Path]:
    """Sauvegarde corpus en CSV et métadonnées en JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # CSV principal
    csv_path = output_dir / "tranco_corpus.csv"
    # Garde la copie datée pour l'historique
    dated_csv = output_dir / f"tranco_{date_str}_{list_id}.csv"

    fieldnames = ["rank", "domain", "ns"]
    for path in (csv_path, dated_csv):
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for entry in corpus:
                writer.writerow({
                    "rank":   entry["rank"],
                    "domain": entry["domain"],
                    "ns":     "|".join(entry["ns"]),
                })
    log.info("CSV sauvegardé : %s  (%d domaines)", csv_path, len(corpus))

    # JSON métadonnées
    meta = {
        "list_id":    list_id,
        "date":       date_str,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total":      len(corpus),
        "delta":      delta,
    }
    meta_path = output_dir / "tranco_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2))
    log.info("Métadonnées : %s", meta_path)

    return csv_path, meta_path


# ──────────────────────────────────────────────────────────────────────────────
# Point d'entrée
# ──────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Télécharge et valide la liste Tranco Top 10K pour le pipeline DNS."
    )
    parser.add_argument(
        "--list-id", type=str, default=None,
        help="Identifiant Tranco spécifique (ex: ABCD1). Défaut : liste la plus récente."
    )
    parser.add_argument(
        "--output", type=str, default="data/processed",
        help="Répertoire de sortie (défaut : data/processed)"
    )
    parser.add_argument(
        "--no-validate", action="store_true",
        help="Sauter la validation DNS (mode rapide / test)"
    )
    args = parser.parse_args()

    output_dir = Path(args.output)

    # 1. Identifier la liste
    if args.list_id:
        list_id  = args.list_id
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log.info("Utilisation liste Tranco spécifiée : %s", list_id)
    else:
        list_id, date_str = get_latest_list_id()

    # 2. Téléchargement
    entries = download_tranco(list_id)
    if not entries:
        log.error("Aucun domaine téléchargé — arrêt.")
        return 1

    # 3. Validation DNS
    corpus = validate_corpus(entries, skip_validate=args.no_validate)
    if not corpus:
        log.error("Corpus vide après validation — arrêt.")
        return 1

    # 4. Delta
    prev_csv = output_dir / "tranco_corpus.csv"
    delta = compute_delta({e["domain"] for e in corpus}, prev_csv)

    # 5. Sauvegarde
    csv_path, meta_path = save_corpus(corpus, list_id, date_str, delta, output_dir)

    log.info("Étape 1 terminée — %d domaines prêts dans %s", len(corpus), csv_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
