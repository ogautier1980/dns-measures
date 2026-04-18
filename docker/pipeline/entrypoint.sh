#!/bin/bash
# Entrypoint du container pipeline DNS
# Rôle : initialisation au premier démarrage, puis lancement du cron daemon

set -e

LOG=/app/logs/pipeline.log
PLAN=/app/data/processed/measurements.json
CORPUS=/app/data/processed/tranco_corpus.csv

# S'assurer que les répertoires existent (en cas de volume vide)
mkdir -p /app/data/raw /app/data/processed /app/reports /app/latex/figures /app/logs

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S UTC')] $*" | tee -a "$LOG"
}

log "=== Démarrage du pipeline de mesures DNS ==="
log "Architecture : $(uname -m)"
log "Python : $(python --version)"

# ── Vérification de la clé API ─────────────────────────────────────────────────
if [ -z "$RIPE_ATLAS_API_KEY" ]; then
    log "ATTENTION : RIPE_ATLAS_API_KEY non définie."
    log "  → Définissez-la via --env-file .env ou -e RIPE_ATLAS_API_KEY=xxxx"
    log "  → Le pipeline fonctionnera en mode anonyme (rate limit réduit)"
fi

# Écrire la clé dans un .env accessible aux scripts Python
if [ -n "$RIPE_ATLAS_API_KEY" ]; then
    echo "RIPE_ATLAS_API_KEY=${RIPE_ATLAS_API_KEY}" > /app/.env
    log "Clé API écrite dans /app/.env"
fi

# ── Initialisation au premier lancement ───────────────────────────────────────
if [ ! -f "$PLAN" ]; then
    log "Premier démarrage détecté — lancement de l'initialisation…"
    log "Étape 1 : récupération de la liste Tranco Top 10K"
    python /app/scripts/fetch_tranco.py \
        --output /app/data/processed \
        >> "$LOG" 2>&1

    if [ $? -ne 0 ]; then
        log "ERREUR : échec de fetch_tranco.py — vérifiez la connectivité réseau."
        log "Vous pouvez relancer manuellement : docker exec dns-pipeline python /app/scripts/pipeline.py init"
    else
        log "Étape 2 : création des campagnes RIPE Atlas"
        python /app/scripts/create_ripe_measurements.py \
            --corpus "$CORPUS" \
            --output "$PLAN" \
            >> "$LOG" 2>&1

        if [ $? -ne 0 ]; then
            log "ERREUR : échec de create_ripe_measurements.py"
        else
            log "Initialisation terminée — campagnes actives."
            log "Le premier fetch automatique aura lieu demain matin à 06h00 UTC."
        fi
    fi
else
    log "Plan de mesures existant trouvé : $PLAN"
    log "Passage direct au mode cron (collecte quotidienne active)"
fi

# ── Injecter les variables d'environnement dans l'environnement cron ──────────
# cron ne reçoit pas les variables d'environnement du shell parent
printenv | grep -v "no_proxy" > /etc/environment

# ── Lancement du cron daemon ──────────────────────────────────────────────────
log "Démarrage du cron daemon…"
cron

log "Pipeline actif — collecte quotidienne planifiée à 06h00 UTC"
log "Logs dans : $LOG"
log "Pour surveiller : docker logs -f dns-pipeline"
log ""

# Garder le container vivant en suivant les logs
tail -f "$LOG"
