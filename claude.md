# Claude - Journal de travail et documentation du projet

## Vue d'ensemble du projet

Projet de mémoire : **Mesures DNS dans l'espace et le temps**
- Analyse de données DNS à grande échelle
- Utilisation de RIPE Atlas pour les mesures actives
- Étude de la liste Tranco pour le classement des sites web
- Environnement Docker complet pour recherche et rédaction

## Organisation du projet

```
/workspace/
├── docs/                 # Documentation complète du projet (MD + PDF)
├── sources/              # Articles académiques et références PDF
├── data/                 # Données brutes et traitées (persisté via Docker volume)
├── notebooks/            # Notebooks Jupyter pour analyses exploratoires
├── scripts/              # Scripts Python pour analyses et traitements
├── reports/              # Rapports générés et analyses finales
├── latex/                # Sources LaTeX du mémoire
├── output/               # Fichiers de sortie (PDF, graphiques, etc.)
├── .devcontainer/        # Configuration VSCode Dev Container
├── .claude/              # Configuration Claude Code
├── Dockerfile            # Image Docker principale
├── docker-compose.yml    # Orchestration des services
├── docker-entrypoint.sh  # Script d'entrée du container
├── requirements.txt      # Dépendances Python
├── readme.md             # Sujet du mémoire
└── claude.md            # Ce fichier - journal et bonnes pratiques
```

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
- Mettre à jour ce fichier `claude.md` après chaque session importante
- README.md : documentation utilisateur
- DOCKER_README.md : guide spécifique Docker
- Documenter les décisions importantes et leur raison

### Commits Git
- Commits atomiques et descriptifs
- Messages en français pour ce projet
- Toujours inclure `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`
- Ne pas commiter les fichiers dans `.gitignore`

### Organisation des sources
- Articles PDF dans `sources/`
- Nommer clairement : `sources/auteur_année_titre.pdf`
- Garder une liste des références dans `sources/README.md`

## Prochaines étapes

### À faire
- [ ] Créer le squelette LaTeX du mémoire
- [ ] Implémenter les scripts de récupération RIPE Atlas
- [ ] Créer le pipeline d'analyse Tranco
- [ ] Mettre en place les tests automatisés

### Idées et notes
- Considérer l'ajout de pre-commit hooks pour validation
- Explorer l'utilisation de DVC (Data Version Control) si données volumineuses
- Possibilité d'ajouter des dashboards interactifs avec Plotly Dash

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
