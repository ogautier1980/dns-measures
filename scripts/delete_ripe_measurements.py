#!/usr/bin/env python3
"""
Utilitaire — suppression des mesures RIPE Atlas créées par erreur.

Usage :
  python delete_ripe_measurements.py --plan data/processed/measurements.json
  python delete_ripe_measurements.py --plan data/processed/measurements.json --dry-run
  python delete_ripe_measurements.py --ids 12345,67890

Les mesures one-off terminées ne peuvent pas être supprimées (déjà consommées).
Les mesures récurrentes peuvent être stoppées via STOP (status=Stopped).
"""

import argparse
import json
import logging
import os
import sys
import time
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


def stop_measurement(msm_id: int, dry_run: bool = False) -> bool:
    """Stoppe une mesure récurrente (status → Stopped)."""
    if dry_run:
        log.info("  [DRY-RUN] STOP msm_id=%d", msm_id)
        return True

    url     = f"{API_BASE}/measurements/{msm_id}/"
    headers = {
        "Authorization": f"Key {API_KEY}",
        "Content-Type":  "application/json",
    }
    r = requests.delete(url, headers=headers, timeout=30)

    if r.status_code in (200, 204):
        log.info("  ✓ Stoppée : msm_id=%d", msm_id)
        return True
    elif r.status_code == 404:
        log.warning("  Introuvable (déjà supprimée ?) : msm_id=%d", msm_id)
        return True
    elif r.status_code == 400:
        # Mesure one-off déjà terminée : pas supprimable, mais crédits déjà consommés
        log.warning("  One-off terminée (non supprimable) : msm_id=%d  %s",
                    msm_id, r.text[:100])
        return False
    else:
        log.error("  Erreur API (%d) : msm_id=%d  %s",
                  r.status_code, msm_id, r.text[:200])
        return False


def collect_ids_from_plan(plan_path: Path) -> list[int]:
    """Extrait tous les msm_id du fichier measurements.json."""
    plan = json.loads(plan_path.read_text())
    ids = []

    # Campagne principale
    for m in plan.get("authoritative", {}).get("measurements", []):
        if m.get("msm_id"):
            ids.append(int(m["msm_id"]))

    # Campagne Q4
    for m in plan.get("q4_resolver_comparison", {}).get("measurements", []):
        if m.get("msm_id"):
            ids.append(int(m["msm_id"]))

    # Format ancien (liste plate)
    if isinstance(plan, list):
        for m in plan:
            if m.get("msm_id"):
                ids.append(int(m["msm_id"]))

    return sorted(set(ids))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stoppe/supprime des mesures RIPE Atlas."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--plan", type=str,
        help="Fichier measurements.json (stoppe toutes les mesures du plan)"
    )
    group.add_argument(
        "--ids", type=str,
        help="IDs séparés par des virgules, ex: 12345,67890"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Affiche les opérations sans les exécuter"
    )
    args = parser.parse_args()

    if not API_KEY:
        log.error("RIPE_ATLAS_API_KEY non définie.")
        return 1

    if args.plan:
        plan_path = Path(args.plan)
        if not plan_path.exists():
            log.error("Fichier introuvable : %s", plan_path)
            return 1
        ids = collect_ids_from_plan(plan_path)
    else:
        ids = [int(x.strip()) for x in args.ids.split(",") if x.strip()]

    log.info("Mesures à stopper : %d", len(ids))
    if args.dry_run:
        log.info("[DRY-RUN] Aucune requête envoyée.")

    ok = err = 0
    for msm_id in ids:
        success = stop_measurement(msm_id, dry_run=args.dry_run)
        if success:
            ok += 1
        else:
            err += 1
        if not args.dry_run:
            time.sleep(0.5)

    log.info("Terminé : %d stoppées, %d erreurs", ok, err)
    return 0 if err == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
