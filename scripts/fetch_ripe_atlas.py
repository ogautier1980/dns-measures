#!/usr/bin/env python3
"""
Étape 3 du pipeline — Récupération quotidienne des résultats RIPE Atlas.

Fonctionnement :
  1. Lit measurements.json (plan créé par create_ripe_measurements.py)
  2. Pour chaque measurement ID, télécharge les résultats JSON de la journée
  3. Pagination automatique, retry exponentiel, gestion du rate-limit (HTTP 429)
  4. Sauvegarde chaque résultat dans data/raw/msm_<id>_<date>.json

Usage :
  # Fetch toutes les mesures d'hier
  python fetch_ripe_atlas.py --plan data/processed/measurements.json --date yesterday

  # Fetch un seul measurement ID
  python fetch_ripe_atlas.py --msm-id 12345678 --start 2026-03-31 --stop 2026-04-01

  # Fetch toute la campagne (date auto = hier)
  python fetch_ripe_atlas.py --plan data/processed/measurements.json

Variables d'environnement :
  RIPE_ATLAS_API_KEY   Clé API RIPE Atlas
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
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

API_BASE  = "https://atlas.ripe.net/api/v2"
API_KEY   = os.getenv("RIPE_ATLAS_API_KEY", "")

# Retry config
MAX_RETRIES      = 5
RETRY_BASE_DELAY = 2.0   # secondes (doublement exponentiel)
RATE_LIMIT_WAIT  = 60.0  # secondes d'attente sur HTTP 429
PAGE_DELAY       = 0.3   # délai entre pages


# ──────────────────────────────────────────────────────────────────────────────
# Fetch avec retry
# ──────────────────────────────────────────────────────────────────────────────

def _get_with_retry(url: str, params: dict | None = None) -> requests.Response:
    """
    GET avec retry exponentiel.
    Gère les cas HTTP 429 (rate limit), 5xx (erreurs serveur), timeouts.
    """
    headers = {"Authorization": f"Key {API_KEY}"} if API_KEY else {}
    delay   = RETRY_BASE_DELAY

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=90)

            if r.status_code == 429:
                wait = float(r.headers.get("Retry-After", RATE_LIMIT_WAIT))
                log.warning("Rate limit (429) — attente %.0fs avant retry…", wait)
                time.sleep(wait)
                continue

            if r.status_code in (500, 502, 503, 504):
                log.warning("Erreur serveur (%d) — retry %d/%d dans %.0fs…",
                            r.status_code, attempt, MAX_RETRIES, delay)
                time.sleep(delay)
                delay *= 2
                continue

            r.raise_for_status()
            return r

        except requests.exceptions.Timeout:
            log.warning("Timeout — retry %d/%d dans %.0fs…", attempt, MAX_RETRIES, delay)
            time.sleep(delay)
            delay *= 2
        except requests.exceptions.ConnectionError as exc:
            log.warning("Connexion échouée (%s) — retry %d/%d dans %.0fs…",
                        exc, attempt, MAX_RETRIES, delay)
            time.sleep(delay)
            delay *= 2

    raise RuntimeError(f"Impossible de récupérer {url} après {MAX_RETRIES} tentatives")


# ──────────────────────────────────────────────────────────────────────────────
# Fetch d'un measurement
# ──────────────────────────────────────────────────────────────────────────────

def fetch_measurement_results(
    msm_id: int,
    start: datetime,
    stop: datetime,
    output_dir: Path,
    force: bool = False,
) -> Path | None:
    """
    Télécharge tous les résultats d'une mesure entre start et stop.
    Retourne le chemin du fichier JSON créé, ou None si déjà existant et force=False.
    """
    date_str = start.strftime("%Y-%m-%d")
    out_file = output_dir / f"msm_{msm_id}_{date_str}.json"

    if out_file.exists() and not force:
        log.debug("  Déjà présent : %s — ignoré (--force pour refetch)", out_file)
        return out_file

    params = {
        "start":  int(start.timestamp()),
        "stop":   int(stop.timestamp()),
        "format": "json",
    }
    url     = f"{API_BASE}/measurements/{msm_id}/results/"
    results = []

    log.info("Fetch msm %d  [%s → %s]…", msm_id, start.date(), stop.date())

    while url:
        r    = _get_with_retry(url, params=params)
        data = r.json()

        # L'API retourne soit une liste directe, soit {"results": [...], "next": ...}
        if isinstance(data, list):
            results.extend(data)
            url = None
        else:
            results.extend(data.get("results", []))
            url = data.get("next")

        params = {}   # l'URL suivante contient déjà les paramètres
        time.sleep(PAGE_DELAY)

    output_dir.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(results))
    log.info("  → %d résultats  %s", len(results), out_file)
    return out_file


# ──────────────────────────────────────────────────────────────────────────────
# Fetch de toute une campagne depuis le plan
# ──────────────────────────────────────────────────────────────────────────────

def fetch_campaign(
    plan_path: Path,
    start: datetime,
    stop: datetime,
    output_dir: Path,
    force: bool = False,
    campaign: str = "all",
) -> list[Path]:
    """
    Lit measurements.json et fetch tous les IDs de mesures.
    campaign : "all" | "authoritative" | "q4"
    """
    plan      = json.loads(plan_path.read_text())
    msm_ids   = []

    if campaign in ("all", "authoritative"):
        for m in plan.get("authoritative", {}).get("measurements", []):
            mid = m.get("msm_id")
            if mid:
                msm_ids.append(mid)

    if campaign in ("all", "q4"):
        for m in plan.get("q4_resolver_comparison", {}).get("measurements", []):
            mid = m.get("msm_id")
            if mid:
                msm_ids.append(mid)

    # Dédupliquer (plusieurs domaines peuvent partager un msm_id si batch)
    msm_ids = sorted(set(msm_ids))
    log.info("Plan : %d measurement IDs à fetcher (campagne=%s)", len(msm_ids), campaign)

    fetched = []
    errors  = []

    for i, msm_id in enumerate(msm_ids, 1):
        try:
            path = fetch_measurement_results(msm_id, start, stop, output_dir, force)
            if path:
                fetched.append(path)
        except Exception as exc:
            log.error("  Erreur msm %d : %s", msm_id, exc)
            errors.append(msm_id)

        if i % 50 == 0:
            log.info("  Progression : %d/%d  erreurs=%d", i, len(msm_ids), len(errors))

    log.info("Fetch terminé : %d fichiers  %d erreurs", len(fetched), len(errors))

    if errors:
        err_path = output_dir / f"fetch_errors_{start.strftime('%Y-%m-%d')}.json"
        err_path.write_text(json.dumps({"failed_msm_ids": errors}))
        log.warning("IDs en échec sauvegardés : %s", err_path)

    return fetched


# ──────────────────────────────────────────────────────────────────────────────
# Point d'entrée
# ──────────────────────────────────────────────────────────────────────────────

def parse_date_arg(s: str) -> datetime:
    """Accepte 'yesterday', 'today', ou 'YYYY-MM-DD'."""
    if s == "yesterday":
        d = datetime.now(timezone.utc) - timedelta(days=1)
        return d.replace(hour=0, minute=0, second=0, microsecond=0)
    if s == "today":
        d = datetime.now(timezone.utc)
        return d.replace(hour=0, minute=0, second=0, microsecond=0)
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch quotidien des résultats RIPE Atlas"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--plan", type=str,
        help="Fichier JSON du plan de mesures (sortie de create_ripe_measurements.py)"
    )
    group.add_argument(
        "--msm-id", type=int,
        help="ID d'une mesure unique à fetcher"
    )
    parser.add_argument(
        "--start", type=str, default="yesterday",
        help="Date de début : YYYY-MM-DD | yesterday | today (défaut: yesterday)"
    )
    parser.add_argument(
        "--stop", type=str, default=None,
        help="Date de fin : YYYY-MM-DD (défaut: start + 1 jour)"
    )
    parser.add_argument(
        "--output", type=str, default="data/raw",
        help="Répertoire de sortie des JSON bruts (défaut: data/raw)"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Re-télécharge même si le fichier existe déjà"
    )
    parser.add_argument(
        "--campaign", choices=["all", "authoritative", "q4"], default="all",
        help="Quelle campagne fetcher (défaut: all)"
    )
    args = parser.parse_args()

    start      = parse_date_arg(args.start)
    stop       = parse_date_arg(args.stop) if args.stop else start + timedelta(days=1)
    output_dir = Path(args.output)

    if not API_KEY:
        log.warning("RIPE_ATLAS_API_KEY non définie — les requêtes seront anonymes (rate limit réduit)")

    if args.msm_id:
        fetch_measurement_results(args.msm_id, start, stop, output_dir, args.force)
        return 0

    if args.plan:
        plan_path = Path(args.plan)
        if not plan_path.exists():
            log.error("Plan introuvable : %s", plan_path)
            return 1
        fetch_campaign(plan_path, start, stop, output_dir, args.force, args.campaign)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
