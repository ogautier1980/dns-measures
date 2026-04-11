# Claude - Journal de travail et documentation du projet

## ⚡ Reprise rapide de contexte (après rebuild / perte de session)

**Projet** : Mémoire "Mesures DNS dans l'espace et le temps" — Olivier Gautier, Master 60 UNamur 2025-2026.
**Promoteurs** : Fl. Rochet, J. Dejaeghere. **Co-promoteur** : Pierre Luycx.
**Repo GitHub** : https://github.com/ogautier1980/dns-measures.git

### État au 11 avril 2026 — Ce qui est en place

| Version mémoire | Fichier | PDF | Pages |
|---|---|---|---|
| Longue EN | `latex/main_long_en.tex` | `output/memoire_long_en.pdf` | 117 p. |
| Longue FR | `latex/main_fr_long.tex` | `output/memoire_long_fr.pdf` | 137 p. |
| Courte EN | `latex/main.tex` | `output/memoire_court_en.pdf` | 79 p. |
| Courte FR | `latex/main_fr.tex` | `output/memoire_court_fr.pdf` | 73 p. |

**Compilation** : `cd /workspace/latex && make long-en` (ou `make all` pour les 4)

### Pipeline DNS — État au 11 avril 2026

**Deux repos distincts :**
- `/workspace/pipeline-standalone` → repo GitHub `ogautier-unam/dns-pipeline` (code pipeline)
- `/workspace/dns-pipeline` → données locales (volume monté sur le Pi, NON commité)

**Phases de mesure :**
- **Phase pilote** (01–10 avril) : 99 domaines × 50 sondes — terminée, données 02–09/04 dans le parquet
- **Phase principale** (à partir du 11 avril) : 250 domaines × 200 sondes — **ACTIVE**

**Mesures RIPE Atlas — EN COURS de collecte** :

| Question | Type | État | Détails |
|---|---|---|---|
| Q1 (diversité géo) | Périodique auth NS | ✅ Actif | 248/250 mesures Ongoing, fetch quotidien 10h UTC |
| Q2 (stabilité temps) | Périodique auth NS | ✅ Actif | Mêmes mesures |
| Q3 (biais sondes) | Périodique auth NS | ✅ Actif | Mêmes mesures |
| Q4 (comparaison résolveurs) | One-off | ⚠️ Partiel | 8/1000 créées — relancer --q4-resume les prochains jours |

**Architecture pipeline (sur Raspberry Pi à la maison) :**
- Docker container `dns-pipeline` tourne en continu avec watchdog cron
- Cron 10h UTC : `pipeline.py daily` → fetch résultats d'hier + parsing Parquet
- Cron 11h UTC : `sync_cloud.sh daily` → sync Google Drive
- Cron 12h UTC dimanche : `pipeline.py analyse` → Q1-Q4 + figures
- Cron 13h UTC dimanche : `sync_cloud.sh weekly` → sync Google Drive
- Résultats raw : `data/raw/msm_<id>_<date>.json` (conservés 7 jours puis supprimés)
- Résultats parsés : `data/processed/dns_results_<date>.parquet`
- Sync cloud : **Google Drive uniquement** (OneDrive UNamur supprimé — ne fonctionnait pas)

**Crédits RIPE Atlas :**
- Solde : 29,000,000 crédits
- Phase pilote consommée : ~495,000 (Q1-Q3) + ~100,000 (Q4 partiel 50 dom) ≈ 600,000
- Phase principale Q1-Q3 : 250 × 200 × 10 = 500,000 crédits/jour × 49 jours ≈ 24,500,000
- Phase principale Q4 : 250 dom × 200 sondes × 4 résolveurs × 10 crédits ≈ 2,000,000
- Total estimé : ~27,095,000 — dans le budget (29,000,000 disponibles)

**Bugs corrigés (important pour reprises futures) :**
- `parse_dns_results.py` : `--date yesterday` ne fonctionnait pas (glob cherchait "*yesterday*") — corrigé
- `parse_dns_results.py` : `use_probe_resolver` toujours False (non retourné par RIPE Atlas) — corrigé via lookup depuis measurements.json
- `sync_cloud.sh` : `set -e` tuait le cron sur erreur rclone — supprimé
- `entrypoint.sh` : watchdog cron ajouté (relance auto si cron meurt)
- Volumes Docker : noms réels = `dns-pipeline_dns-raw`, `dns-pipeline_dns-processed`, etc.

**Commande de déploiement phase principale (à faire après sync 11h UTC) :**
```bash
cd ~/dns-pipeline && git pull
docker cp scripts/create_ripe_measurements.py dns-pipeline:/app/scripts/
docker cp scripts/stop_all_measurements.py dns-pipeline:/app/scripts/

# 1. Analyse finale sur données pilote
docker exec dns-pipeline python /app/scripts/pipeline.py analyse
docker exec dns-pipeline sync_cloud.sh weekly

# 2. Stopper les mesures pilote
docker exec dns-pipeline python /app/scripts/stop_all_measurements.py

# 3. Lancer la phase principale (250 dom × 200 sondes — valeurs par défaut)
docker exec dns-pipeline python /app/scripts/create_ripe_measurements.py \
  --corpus data/processed/tranco_corpus.csv \
  --output data/processed/measurements.json
```

**Scripts clés dans `pipeline-standalone/scripts/` :**
- `create_ripe_measurements.py` : création mesures (défaut : 250 dom × 200 sondes, stratification pays)
- `stop_all_measurements.py` : arrêt des mesures actives RIPE Atlas
- `fetch_ripe_atlas.py` : fetch résultats par date depuis l'API
- `parse_dns_results.py` : parsing JSON → Parquet
- `pipeline.py` : orchestration (init / daily / analyse / weekly)
- `analyse_dns.py` : analyse Q1-Q4 + figures

### Ce qui reste à faire

1. **Compléter Q4** : relancer `--q4-resume` chaque jour jusqu'à 1000/1000 mesures
2. **Attendre ~7 semaines** de collecte (jusqu'à fin mai 2026)
3. **Remplir chapitre 4** (Résultats) avec les vraies mesures
4. **Remplir chapitre 5** (Conclusion) basé sur les résultats

### Attention — points sensibles
- La version longue FR (`main_fr_long.tex`) compile avec warnings Unicode (non bloquants).
- Ne PAS réécrire les fichiers `latex/long/*-fr.tex` sans demander — ils ont pris du temps à générer.
- Le corpus Tranco est **figé** pour garantir la validité de Q2. Ne pas le régénérer.
- Les données sont sur le Pi (`~/dns-pipeline/`), sync vers `/workspace/dns-pipeline/` via Google Drive.
- Volumes Docker nommés `dns-pipeline_dns-raw`, `dns-pipeline_dns-processed`, `dns-pipeline_dns-logs`, `dns-pipeline_dns-reports`, `dns-pipeline_dns-figures`, `dns-pipeline_rclone-config`.

## Vue d'ensemble du projet

Projet de mémoire : **Mesures DNS dans l'espace et le temps**
- Analyse de données DNS à grande échelle
- Utilisation de RIPE Atlas pour les mesures actives
- Étude de la liste Tranco pour le classement des sites web
- Environnement Docker complet pour recherche et rédaction

## Organisation du projet

```
/workspace/
├── docs/                 # Documentation, roadmap, bibliographie, figures
│   ├── documentation.md  # Guide environnement Docker
│   ├── roadmap.md        # Plan d'exécution du mémoire
│   ├── recherche.md      # Guide bibliographique
│   ├── figures.md        # Plan des figures du mémoire
│   ├── analyse_exemples.md  # Comparaison mémoires UNamur 2022-2024
│   └── mailPierre.md     # Notes réunions avec co-promoteur
├── sources/              # Articles académiques PDF + fiches de lecture
│   ├── *.pdf             # 16 articles (convention auteur+année)
│   ├── fiches/           # Fiches de lecture structurées (~20 fiches)
│   └── README.md         # Catalogue et analyse de pertinence
├── latex/                # Sources LaTeX — 4 versions du mémoire
│   ├── main.tex          # Version courte EN
│   ├── main_fr.tex       # Version courte FR
│   ├── main_long_en.tex  # Version longue EN
│   ├── main_fr_long.tex  # Version longue FR
│   ├── preamble.tex / preamble_fr.tex
│   ├── chapters/         # Chapitres courts (EN + FR)
│   ├── long/             # Chapitres longs (EN + FR)
│   ├── md/en/            # Sources Markdown longues EN
│   ├── md/fr/            # Sources Markdown longues FR
│   ├── figures/          # Figures PNG/PUML
│   ├── img/              # Images (logo UNamur)
│   ├── bibliography.bib  # Bibliographie BibTeX
│   └── convert_md_to_tex.py  # Script conversion MD → LaTeX
├── output/               # PDFs générés (4 versions)
├── scripts/              # Scripts Python analyses et figures
├── data/                 # Données (Docker volume)
├── notebooks/            # Notebooks Jupyter
├── reports/              # Rapports générés
├── examples/md/          # Mémoires UNamur 2022-2024 (texte)
└── readme.md             # Sujet du mémoire
```

### Template LaTeX UNamur
- Auteur : Vincent Englebert, v1.0 (15/10/2025)
- Police obligatoire : **Atkinson Hyperlegible** (accessibilité)
- Repo : `Template-Master-Thesis` (UNamur Computer Science)

## Historique des modifications

### 2026-01-20 - Configuration initiale

**Actions effectuées :**
1. ✅ Suppression de l'installation du CLI Claude Code du Dockerfile
   - Raison : Seule l'extension VSCode est nécessaire
   - L'extension est automatiquement installée via `.devcontainer/devcontainer.json`
   - Suppression de Node.js qui n'était utilisé que pour le CLI

2. ✅ Premier commit et push sur GitHub
   - Repository : `https://github.com/ogautier1980/dns-measures.git`
   - Commit initial avec l'environnement Docker complet

3. ✅ Réorganisation de la structure du projet
   - Création des répertoires sources, reports, latex, output
   - Déplacement des PDF académiques dans sources/
   - Nettoyage des fichiers temporaires
   - Ajout de .gitignore et .dockerignore
   - Création de README.md dans chaque répertoire

4. ✅ Création de la documentation complète
   - Nouveau répertoire `docs/` pour centraliser la documentation
   - `docs/documentation.md` : Documentation complète en Markdown (23KB)
   - `docs/documentation.pdf` : Version PDF générée via pandoc/XeLaTeX (101KB)
   - Suppression de `DOCKER_README.md` redondant
   - Script `docker-entrypoint.sh` conservé (utilisé par Docker)
   - Documentation couvre : structure, outils, utilisation, bonnes pratiques, dépannage

**Configuration actuelle :**
- Image Docker : Python 3.11 slim-bookworm
- Extensions VSCode : Python, Pylance, Jupyter, LaTeX Workshop, Claude Code
- Outils DNS : dnspython, RIPE Atlas tools
- Stack analyse : NumPy, Pandas, SciPy, Scikit-learn
- Visualisation : Matplotlib, Seaborn, Plotly, Folium
- Documents : LaTeX complet, PDF tools, Office tools

### 2026-03-21 - Compilation rigoureuse du mémoire LaTeX

**Actions effectuées :**
1. ✅ Conversion Markdown → LaTeX avec script Python rigoureux
   - Fichier : `latex/convert_md_to_tex.py` (274 lignes)
   - Gestion correcte des caractères spéciaux LaTeX (%, &, #, _, {}, ~, ^)
   - Remplacement systématique des caractères Unicode (box-drawing, flèches, symboles)
   - Protection des blocs de code avant toute transformation
   - Ordre des opérations optimisé pour éviter les conflits
   - Tableaux Markdown mis en commentaire pour révision manuelle

2. ✅ Compilation LaTeX en 4 passes (conformément aux bonnes pratiques)
   - Passe 1 : pdflatex (génération contenu + fichier .toc)
   - Passe 2 : pdflatex (intégration table des matières)
   - Passe 3 : biber (traitement bibliographie)
   - Passe 4 : pdflatex (intégration bibliographie)
   - Passe 5 : pdflatex (finalisation références croisées)

3. ✅ Vérification rigoureuse du contenu généré
   - Texte "Si 80%" maintenant complet (était tronqué à cause du %)
   - Table des matières complète et structurée (48 pages)
   - Bibliographie fonctionnelle avec 18 références
   - 5 chapitres convertis et compilés correctement

4. ✅ Fichiers générés
   - PDF final : `output/memoire_dns_measures_final.pdf` (289 KB, 48 pages)
   - Table des matières : 8 pages avec numérotation romaine
   - Bibliographie : fonctionnelle mais citations marquées TODO
   - Annexes techniques : configuration RIPE Atlas, schéma Avro

**Problèmes corrigés avec rigueur :**
- Échappement systématique du % qui causait troncature du texte
- Gestion des caractères Unicode dans les blocs de code ET le texte normal
- Protection des zones sensibles (code, URLs, gras, italique) avant échappement
- Conversion des tableaux reportée (commentés pour révision manuelle)
- Ordre des passes de compilation respecté (2+ passes obligatoires)

**Problèmes résiduels mineurs :**
- 3 erreurs `\textbf` dans des contextes complexes (PDF généré quand même)
- Tableaux en commentaire à convertir manuellement
- Citations bibliographiques marquées TODO à compléter

### 2026-03-21 (soir) - Conformité stricte au template UNamur + Enrichissement chapitre 2

**Actions effectuées :**
1. ✅ Enrichissement massif du chapitre 2 (État de l'art)
   - Taille initiale : 6,154 mots
   - Taille finale : 17,895 mots
   - Facteur multiplicatif : **2.91× (presque triplé comme demandé)**
   - Ajouts majeurs :
     * Section 2.1.5 : Échelle et statistiques globales du DNS
     * Section 2.2.4 : Défis spécifiques aux mesures DNS distribuées
     * Section 2.3 : Enrichie avec 5 sous-sections détaillées sur OpenINTEL
     * Section 2.4.4-2.4.5 : Alternatives RIPE Atlas et spécifications techniques
     * Section 2.5.2 : EDNS Client Subnet massivement enrichi
     * Section 2.5.4-2.5.5 : Évolution historique CDN et stratégies par acteur
     * Section 2.6 : Enrichie avec comparaison empirique Tranco vs autres listes
     * Section 2.7 : Nouvelles sous-sections 2.7.4 et 2.7.5 sur biais
     * Section 2.8 : Triplée avec synthèse détaillée et gaps identifiés
     * **Section 2.9 (NOUVELLE)** : Sécurité DNS (DNSSEC, DoH/DoT, protocoles émergents)

2. ✅ Mise en conformité STRICTE avec le template officiel UNamur
   - **Police Atkinson Hyperlegible** installée et activée (obligatoire UNamur pour accessibilité)
   - Marges ajustées selon template : [top=2cm, bottom=2.5cm, left=2cm, right=2cm]
   - Page de couverture complète avec logo FAC_informatique.png
   - Section Remerciements rédigée
   - Résumé et Abstract rédigés (½ page chacun, sur 1 page)
   - Liste d'acronymes complète (35 entrées DNS/réseau)
   - Métadonnées correctes : Promoteurs (Fl. Rochet, J. Dejaeghere), Co-promoteur (Pierre Luycx)
   - Diplôme : Master 60 en Sciences Informatiques
   - Année académique : 2025-2026
   - Structure main.tex entièrement restructurée selon template UNamur
   - Preamble.tex complètement refondu et conforme

3. ✅ Fichiers générés
   - PDF conforme UNamur (initial) : `output/memoire_dns_unamur_conforme.pdf` (414 KB, 55 pages)
   - PDF enrichi (final) : `output/memoire_dns_unamur_enriched_final.pdf` (721 KB, 125 pages)
   - Utilise la police Atkinson Hyperlegible (meilleure lisibilité)
   - Inclut toutes les pages préliminaires obligatoires
   - Annexes techniques avec exemples JSON RIPE Atlas et schéma Avro

4. ✅ Amélioration du script de conversion Markdown → LaTeX
   - Correction de l'échappement du caractère `%` dans `\textbf{...}` et `\textit{...}`
   - Suppression des variation selectors Unicode (U+FE0F) qui causaient des erreurs
   - Conversion automatique réussie de tous les chapitres enrichis

5. ✅ Nettoyage complet du projet (2026-03-21 soir)
   - Suppression fichiers temporaires LaTeX (*.aux, *.log, *.out, etc.)
   - Suppression fichiers obsolètes : test_convert.py, chapitre2_BACKUP.md
   - Suppression PDF obsolètes dans output/ (gardé 2 versions : conforme + enriched_final)
   - Suppression répertoire sources/converted/ (conversions automatiques brutes)
   - Amélioration .gitignore (ajout *.bcf, *.run.xml, latex/*_BACKUP.md, latex/test_*.py)
   - Gain d'espace : ~1.2 MB libéré
   - Structure projet maintenant propre et maintenable

**Améliorations qualité substantielles** :
- Chapitre 2 maintenant de qualité académique professionnelle
- Données empiriques concrètes issues des 16 articles sources
- Résultats quantitatifs détaillés (pourcentages, métriques précises)
- Cas d'étude réels (Cloudflare anycast, Akamai géo-routing, Netflix Open Connect)
- Analyse critique approfondie de la littérature avec identification des gaps
- Tableaux comparatifs (RIPE Atlas vs alternatives, Tranco vs Alexa vs autres)

### 2026-03-28 - Organisation 4 versions + nettoyage

**Actions effectuées :**
1. ✅ Création de 4 versions complètes du mémoire
   - Version courte EN : `main.tex` → `output/memoire_court_en.pdf` (79 pages)
   - Version courte FR : `main_fr.tex` → `output/memoire_court_fr.pdf` (73 pages)
   - Version longue EN : `main_long_en.tex` → `output/memoire_long_en.pdf` (117 pages)
   - Version longue FR : `main_fr_long.tex` → `output/memoire_long_fr.pdf` (137 pages)
   - Chapitres longs EN depuis `old/version complete/` (308–579 lignes/chapitre)
   - Chapitres longs FR convertis depuis `latex/md/fr/chapitre*.md` via `convert_md_to_tex.py`

2. ✅ Réorganisation des sources Markdown
   - `latex/md/en/` : sources longues EN (`chapter*.md`, 289–481 lignes)
   - `latex/md/fr/` : sources longues FR (`chapitre*.md`, 392–1512 lignes)
   - Versions courtes uniquement en LaTeX (`latex/chapters/`)
   - Script `convert_md_to_tex.py` mis à jour pour lire depuis `md/en/`

3. ✅ Nettoyage du projet
   - Suppression `sources/converted/` (textes bruts PDF, régénérables) — ajout `.gitignore`
   - Suppression fichiers redondants : `docs/README.md`, `docs/Template/README.md`, `sources/RECAP_TRAITEMENT.md`
   - Déplacement `sources/analyse_articles.md` → `docs/`
   - Suppression `latex/img/figure1.jpg`, `unamur.png` (non référencés)
   - Suppression artifacts LaTeX dans `output/`

4. ✅ Conversion PDF → Markdown (outils sources)
   - Commande : `for pdf in sources/*.pdf; do pdftotext "$pdf" "sources/converted/${pdf%.pdf}.md"; done`
   - 16/16 articles convertis, fiches de lecture créées dans `sources/fiches/`
   - Articles classés : 6 ⭐⭐⭐ essentiels, 9 ⭐⭐ pertinents, 2 ⭐ références

## Bonnes pratiques

### Compilation LaTeX
- **TOUJOURS faire 2 passes** lors de la compilation LaTeX → PDF
  - 1ère passe : génération du contenu
  - 2ème passe : mise à jour de la table des matières, références croisées
- Pour bibliographie avec BibTeX/Biber : faire 3-4 passes
  ```bash
  pdflatex document.tex
  biber document  # ou bibtex document
  pdflatex document.tex
  pdflatex document.tex
  ```
- Ou utiliser `latexmk` qui gère automatiquement les passes :
  ```bash
  latexmk -pdf -interaction=nonstopmode document.tex
  ```

### Gestion des données
- **Jamais de fichiers temporaires** dans le repository Git
- Données brutes dans `data/raw/`
- Données traitées dans `data/processed/`
- Utiliser le volume Docker `dns-data` pour la persistance

### Analyses et notebooks
- Notebooks Jupyter dans `notebooks/` pour exploration
- Scripts Python production dans `scripts/`
- Nommer les fichiers avec des dates : `2026-01-20_analyse_tranco.ipynb`
- Toujours inclure des commentaires et markdown dans les notebooks

### Documentation
- Mettre à jour ce fichier `CLAUDE.md` après chaque session importante
- `docs/documentation.md` : guide environnement Docker
- Documenter les décisions importantes et leur raison

### Commits Git
- Commits atomiques et descriptifs
- Messages en français pour ce projet
- Toujours inclure `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`
- Ne pas commiter les fichiers dans `.gitignore`

### Organisation des sources
- Articles PDF dans `sources/`
- Nommer clairement : `sources/auteur_année_titre.pdf`
- Garder une liste des références dans `sources/README.md`

## Prochaines étapes

### Accompli ✅
- [x] Créer le squelette LaTeX du mémoire (2026-03-21)
- [x] Mettre en conformité avec template UNamur (2026-03-21)
- [x] Enrichir substantiellement le chapitre 2 (×3 en volume) (2026-03-21)
- [x] Générer les 4 versions du mémoire (Long/Court × EN/FR) (2026-03-28)
- [x] Organiser les sources Markdown dans `latex/md/` (2026-03-28)
- [x] Implémenter les scripts de récupération RIPE Atlas (pipeline-standalone/scripts/) (2026-04-01)
- [x] Créer le pipeline d'analyse Tranco + corpus 100 domaines (2026-04-01)
- [x] Lancer la collecte RIPE Atlas Q1/Q2/Q3 — 99 mesures périodiques actives depuis 01/04
- [x] Lancer Q4 partiellement — 85/200 mesures créées

### À faire — avril-mai 2026
- [ ] **Déployer phase principale** : stopper mesures pilote + relancer 250 dom × 200 sondes (voir commandes dans section pipeline ci-dessus)
- [ ] **Attendre ~7 semaines** de collecte (jusqu'à fin mai 2026)
- [ ] Remplir chapitre 4 avec les vrais résultats une fois collecte suffisante
- [ ] Remplir chapitre 5 avec discussion basée sur résultats
- [ ] Compléter les fiches de lecture restantes (14/20 articles non encore fichés)

## Dépannage

### Problèmes courants
- **Port Jupyter déjà utilisé** : Modifier le port dans `docker-compose.yml`
- **Extension Claude Code non installée** : Rebuild du container Dev Container
- **Erreur LaTeX** : Vérifier que `texlive-full` est bien installé

## Ressources

### Documentation
- RIPE Atlas API : https://atlas.ripe.net/docs/api/v2/
- Tranco List : https://tranco-list.eu/
- dnspython : https://dnspython.readthedocs.io/

### Articles de référence
Voir `sources/README.md` pour la liste complète et annotée.
