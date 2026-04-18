# Déploiement du pipeline DNS sur Raspberry Pi 5

Ce container tourne de manière autonome et gère l'intégralité du cycle :
téléchargement Tranco → création mesures RIPE Atlas → collecte quotidienne → parsing → analyse.

## Prérequis sur le Raspberry Pi 5

### 1. Installer Docker

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Se déconnecter et reconnecter pour appliquer les droits
```

Vérifier :
```bash
docker --version         # Docker 24+ recommandé
docker compose version   # Compose v2 requis (pas docker-compose v1)
```

### 2. Configurer la clé API RIPE Atlas

À la racine du projet, créer le fichier `.env` :
```bash
echo "RIPE_ATLAS_API_KEY=5241ce15-313b-4e98-b6c2-560fd71db8cd" > .env
chmod 600 .env
```

---

## Déploiement

### Option A — Depuis le dépôt Git (recommandé)

```bash
# Cloner le projet sur le Pi
git clone https://github.com/ogautier1980/dns-measures.git
cd dns-measures

# Créer le .env
echo "RIPE_ATLAS_API_KEY=5241ce15-313b-4e98-b6c2-560fd71db8cd" > .env

# Construire et démarrer (la première fois, ~5 minutes)
docker compose -f docker-compose.pipeline.yml up -d --build

# Suivre les logs en temps réel
docker logs -f dns-pipeline
```

### Option B — Image pré-construite (depuis un autre poste)

Sur votre poste de développement (x86 ou Mac) avec Docker Buildx installé :
```bash
# Construire pour ARM64 et pousser sur Docker Hub
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -f Dockerfile.pipeline \
  -t votreuser/dns-pipeline:latest \
  --push .
```

Sur le Raspberry Pi :
```bash
# Modifier docker-compose.pipeline.yml : remplacer "build:" par "image: votreuser/dns-pipeline:latest"
docker compose -f docker-compose.pipeline.yml up -d
```

---

## Comportement automatique

### Premier démarrage
Au premier lancement, l'entrypoint détecte qu'aucun plan de mesures n'existe et enchaîne automatiquement :

1. **Téléchargement Tranco Top 10K** — ~30 secondes
2. **Validation DNS** — ~10 minutes (10 000 domaines)
3. **Sélection de 100 sondes RIPE Atlas** — ~30 secondes
4. **Création des campagnes** — ~2 heures (rate limit API : 1 req/s × 10 000 domaines)

### Planification automatique (cron interne)

| Heure UTC | Action |
|-----------|--------|
| Lun 05h00 | Rafraîchissement liste Tranco (hebdomadaire) |
| Tous jours 06h00 | Fetch résultats RIPE Atlas + parsing Parquet |
| Dim 07h00 | Analyse complète Q1–Q4 + figures |
| 1er du mois 04h00 | Rotation des logs |

---

## Commandes utiles

```bash
# Voir les logs en temps réel
docker logs -f dns-pipeline

# Lancer manuellement un fetch (sans attendre le cron)
docker exec dns-pipeline python /app/scripts/pipeline.py daily

# Lancer l'analyse immédiatement
docker exec dns-pipeline python /app/scripts/pipeline.py analyse

# Vérifier l'état des données
docker exec dns-pipeline ls -lh /app/data/processed/
docker exec dns-pipeline ls -lh /app/data/raw/ | tail -20

# Accéder au shell du container
docker exec -it dns-pipeline bash

# Redémarrer le container (sans perdre les données)
docker compose -f docker-compose.pipeline.yml restart

# Mettre à jour les scripts sans reconstruire
git pull
docker compose -f docker-compose.pipeline.yml up -d --build
```

## Récupérer les données sur votre poste de travail

```bash
# Copier le Parquet cumulatif
docker cp dns-pipeline:/app/data/processed/dns_results.parquet ./

# Copier les rapports d'analyse
docker cp dns-pipeline:/app/reports/ ./reports_from_pi/

# Copier les figures pour le LaTeX
docker cp dns-pipeline:/app/latex/figures/ ./latex/figures/
```

Ou utiliser `docker volume` pour monter directement le volume sur un partage NFS/SMB.

---

## Ressources consommées sur le Pi 5

| Ressource | Collecte quotidienne | Analyse hebdomadaire |
|-----------|---------------------|---------------------|
| RAM | ~150 Mo | ~400 Mo |
| CPU | <5% (fetch réseau) | ~50% pendant 2–5 min |
| Stockage/mois | ~500 Mo (raw JSON) + ~50 Mo (Parquet) | — |
| Bande passante | ~200 Mo/jour (fetch RIPE Atlas) | — |

Le Pi 5 gère largement ces charges. La collecte quotidienne est essentiellement de l'attente réseau.

---

## Dépannage

**Le container s'arrête au démarrage**
```bash
docker logs dns-pipeline   # Lire les dernières lignes
```
Cause probable : clé API manquante ou problème réseau lors de l'init.

**Pas de résultats après 24h**
```bash
docker exec dns-pipeline cat /app/logs/pipeline.log | grep -E "ERROR|ERREUR"
```

**Mises à jour**
```bash
git pull
docker compose -f docker-compose.pipeline.yml up -d --build --no-deps dns-pipeline
```
Les volumes de données ne sont pas affectés par la reconstruction de l'image.
