#!/usr/bin/env python3
"""
Orchestrateur quotidien du pipeline DNS.

Enchaîne les 5 étapes dans l'ordre, avec journalisation structurée.
Conçu pour être lancé par cron ou manuellement.

Modes :
  init       — Initialisation complète (étapes 1+2) : télécharge Tranco et crée les mesures
  daily      — Collecte quotidienne (étapes 3+4) : fetch résultats + parsing
  analyse    — Analyse seule (étape 5)
  full       — Pipeline complet (étapes 1→5) — à utiliser au premier lancement

Usage :
  python pipeline.py init      # à faire une seule fois au démarrage
  python pipeline.py daily     # à planifier via cron (tous les jours)
  python pipeline.py analyse   # après accumulation de données
  python pipeline.py full      # tout enchaîner

Options communes :
  --dry-run    Ne pas créer de mesures RIPE Atlas (mode test)
  --date DATE  Date à fetcher (défaut: yesterday) pour le mode daily
  --verbose    Logging DEBUG

Exemple cron (chaque jour à 06h00) :
  0 6 * * * cd /workspace && python scripts/pipeline.py daily >> logs/pipeline.log 2>&1
"""

import argparse
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  [pipeline]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Chemins par défaut ────────────────────────────────────────────────────────
SCRIPTS_DIR   = Path(__file__).parent
DATA_RAW      = Path("data/raw")
DATA_PROC     = Path("data/processed")
REPORTS_DIR   = Path("reports")
FIGURES_DIR   = Path("latex/figures")
PLAN_FILE     = DATA_PROC / "measurements.json"
CORPUS_FILE   = DATA_PROC / "tranco_corpus.csv"
PARQUET_FILE  = DATA_PROC / "dns_results.parquet"
LOGS_DIR      = Path("logs")


# ──────────────────────────────────────────────────────────────────────────────
# Exécution d'un sous-script
# ──────────────────────────────────────────────────────────────────────────────

def run_step(name: str, args: list[str], step_num: int) -> bool:
    """
    Lance un script Python en sous-processus.
    Retourne True si succès, False sinon.
    """
    cmd = [sys.executable] + args
    log.info("── Étape %d : %s ──", step_num, name)
    log.info("   Commande : %s", " ".join(cmd))

    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        log.info("   ✓ Étape %d terminée avec succès", step_num)
        return True
    else:
        log.error("   ✗ Étape %d ÉCHOUÉE (code %d)", step_num, result.returncode)
        return False


# ──────────────────────────────────────────────────────────────────────────────
# Modes du pipeline
# ──────────────────────────────────────────────────────────────────────────────

def mode_init(dry_run: bool) -> int:
    """
    Initialisation du pipeline :
      1. Télécharge et valide la liste Tranco Top 10K
      2. Sélectionne les sondes et crée les campagnes RIPE Atlas
    """
    log.info("=== MODE INIT : Initialisation du pipeline ===")

    # Étape 1 — Tranco
    ok = run_step(
        "Récupération Tranco Top 10K",
        [str(SCRIPTS_DIR / "fetch_tranco.py"),
         "--output", str(DATA_PROC)],
        step_num=1,
    )
    if not ok:
        log.error("Arrêt : étape 1 échouée.")
        return 1

    # Étape 2 — Créer les mesures RIPE Atlas
    step2_args = [
        str(SCRIPTS_DIR / "create_ripe_measurements.py"),
        "--corpus", str(CORPUS_FILE),
        "--output", str(PLAN_FILE),
    ]
    if dry_run:
        step2_args.append("--dry-run")

    ok = run_step(
        "Création des campagnes RIPE Atlas",
        step2_args,
        step_num=2,
    )
    if not ok:
        log.error("Arrêt : étape 2 échouée.")
        return 1

    log.info("=== INIT terminé — campagnes actives dans %s ===", PLAN_FILE)
    log.info("Lancez 'python pipeline.py daily' le lendemain pour fetcher les premiers résultats.")
    return 0


def mode_daily(date: str) -> int:
    """
    Pipeline quotidien :
      3. Fetch les résultats de la journée précédente
      4. Parse et archive en Parquet
    """
    log.info("=== MODE DAILY : date=%s ===", date)

    if not PLAN_FILE.exists():
        log.error("Plan de mesures introuvable : %s — lancez d'abord 'pipeline.py init'", PLAN_FILE)
        return 1

    # Étape 3 — Fetch
    ok = run_step(
        f"Fetch résultats RIPE Atlas ({date})",
        [str(SCRIPTS_DIR / "fetch_ripe_atlas.py"),
         "--plan", str(PLAN_FILE),
         "--start", date,
         "--output", str(DATA_RAW)],
        step_num=3,
    )
    if not ok:
        log.warning("Étape 3 en erreur — on continue quand même pour parser les fichiers existants")

    # Étape 4 — Parse
    ok = run_step(
        f"Parsing JSON → Parquet ({date})",
        [str(SCRIPTS_DIR / "parse_dns_results.py"),
         "--input", str(DATA_RAW),
         "--output", str(DATA_PROC),
         "--date", date],
        step_num=4,
    )
    if not ok:
        log.error("Arrêt : étape 4 échouée.")
        return 1

    log.info("=== DAILY terminé pour %s ===", date)
    return 0


def mode_analyse(questions: str) -> int:
    """
    Étape 5 — Analyse Q1–Q4.
    """
    log.info("=== MODE ANALYSE : questions=%s ===", questions)

    if not PARQUET_FILE.exists():
        log.error("Données introuvables : %s — lancez d'abord le pipeline daily", PARQUET_FILE)
        return 1

    ok = run_step(
        "Analyse quantitative Q1–Q4",
        [str(SCRIPTS_DIR / "analyse_dns.py"),
         "--data", str(PARQUET_FILE),
         "--output", str(REPORTS_DIR),
         "--figures", str(FIGURES_DIR),
         "--questions", questions],
        step_num=5,
    )
    return 0 if ok else 1


def mode_full(dry_run: bool, date: str) -> int:
    """Enchaîne init + daily + analyse."""
    log.info("=== MODE FULL ===")
    steps = [
        lambda: mode_init(dry_run),
        lambda: mode_daily(date),
        lambda: mode_analyse("q1,q2,q3,q4"),
    ]
    for step in steps:
        rc = step()
        if rc != 0:
            return rc
    return 0


# ──────────────────────────────────────────────────────────────────────────────
# Renouvellement hebdomadaire du corpus Tranco
# ──────────────────────────────────────────────────────────────────────────────

def mode_weekly_refresh(dry_run: bool) -> int:
    """
    Rafraîchit la liste Tranco et met à jour les mesures si le corpus a changé.
    À planifier chaque lundi.
    """
    log.info("=== MODE WEEKLY REFRESH ===")

    ok = run_step(
        "Rafraîchissement Tranco (hebdomadaire)",
        [str(SCRIPTS_DIR / "fetch_tranco.py"),
         "--output", str(DATA_PROC)],
        step_num=1,
    )
    if not ok:
        return 1

    # Recrée les mesures pour les nouveaux domaines
    step2_args = [
        str(SCRIPTS_DIR / "create_ripe_measurements.py"),
        "--corpus", str(CORPUS_FILE),
        "--output", str(DATA_PROC / "measurements_new.json"),
    ]
    if dry_run:
        step2_args.append("--dry-run")

    ok = run_step("Mise à jour mesures RIPE Atlas", step2_args, step_num=2)
    return 0 if ok else 1


# ──────────────────────────────────────────────────────────────────────────────
# Point d'entrée
# ──────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Orchestrateur du pipeline DNS"
    )
    parser.add_argument(
        "mode",
        choices=["init", "daily", "analyse", "full", "weekly"],
        help="Mode d'exécution"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Ne pas créer de mesures RIPE Atlas (mode test)"
    )
    parser.add_argument(
        "--date", type=str, default="yesterday",
        help="Date à fetcher pour le mode daily (défaut: yesterday)"
    )
    parser.add_argument(
        "--questions", type=str, default="q1,q2,q3,q4",
        help="Questions pour le mode analyse"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Logging DEBUG"
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Créer les répertoires nécessaires
    for d in (DATA_RAW, DATA_PROC, REPORTS_DIR, LOGS_DIR):
        d.mkdir(parents=True, exist_ok=True)

    log.info("Pipeline DNS — démarrage  mode=%s  %s",
             args.mode, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))

    if args.mode == "init":
        return mode_init(args.dry_run)
    elif args.mode == "daily":
        return mode_daily(args.date)
    elif args.mode == "analyse":
        return mode_analyse(args.questions)
    elif args.mode == "full":
        return mode_full(args.dry_run, args.date)
    elif args.mode == "weekly":
        return mode_weekly_refresh(args.dry_run)

    return 0


if __name__ == "__main__":
    sys.exit(main())
