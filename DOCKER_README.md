# Docker Environment - Mesures DNS dans l'espace et le temps

## Description

Cet environnement Docker fournit tous les outils necessaires pour travailler sur le memoire "Mesures DNS dans l'espace et le temps".

## Outils inclus

### DNS et Reseau
- `dnspython` - Bibliotheque DNS pour Python
- `ripe.atlas.cousteau` - API RIPE Atlas
- `ripe.atlas.sagan` - Parsing des resultats RIPE Atlas
- `dnsutils`, `bind9-host`, `whois` - Outils CLI

### Analyse de donnees
- `pandas`, `numpy`, `scipy` - Manipulation de donnees
- `scikit-learn`, `statsmodels` - Machine learning et statistiques

### Visualisation
- `matplotlib`, `seaborn` - Graphiques
- `plotly`, `bokeh` - Visualisations interactives
- `folium`, `geopandas` - Cartes geographiques

### Documents
- **PDF**: PyPDF2, pdfplumber, reportlab, weasyprint
- **Word**: python-docx
- **PowerPoint**: python-pptx
- **Excel**: openpyxl, xlrd, xlsxwriter
- **Images**: Pillow, opencv, imagemagick

### LaTeX
- `texlive-full` - Distribution LaTeX complete
- `latexmk` - Compilation automatisee
- `pylatex` - Generation de LaTeX en Python
- `pandoc` - Conversion de documents

### Autres
- `jupyter`, `jupyterlab` - Notebooks interactifs
- `tesseract-ocr` - OCR pour extraction de texte
- `libreoffice` - Conversion de documents Office

## Utilisation

### Construction de l'image

```bash
docker build -t dns-measures .
```

### Demarrage du container (mode interactif)

```bash
docker run -it --rm -v ${PWD}:/workspace dns-measures
```

### Avec Docker Compose

```bash
# Demarrer en mode interactif
docker-compose up -d dns-measures
docker-compose exec dns-measures bash

# Demarrer avec Jupyter Lab
docker-compose --profile jupyter up -d
# Acceder a http://localhost:8889
```

### Commandes utiles dans le container

```bash
# Jupyter Lab
jupyter lab --ip=0.0.0.0 --allow-root

# Compiler un document LaTeX
latexmk -pdf document.tex

# Executer un script Python
python scripts/example_dns_measures.py

# Convertir Markdown en PDF
pandoc document.md -o document.pdf --pdf-engine=xelatex
```

## Structure du projet

```
dns-measures/
├── Dockerfile              # Definition de l'image
├── docker-compose.yml      # Configuration Docker Compose
├── docker-entrypoint.sh    # Script d'entree
├── requirements.txt        # Dependances Python
├── .dockerignore           # Fichiers a ignorer
├── readme.md               # Sujet du memoire
├── scripts/
│   ├── example_dns_measures.py  # Exemple de mesures DNS
│   └── document_utils.py        # Utilitaires documents
├── data/                   # Donnees (cree automatiquement)
├── notebooks/              # Jupyter notebooks
├── latex/                  # Fichiers LaTeX
├── output/                 # Resultats et exports
└── reports/                # Rapports generes
```

## Configuration RIPE Atlas

Pour utiliser l'API RIPE Atlas, vous devez:

1. Creer un compte sur https://atlas.ripe.net/
2. Obtenir une cle API
3. Configurer la cle dans le container:

```bash
export RIPE_ATLAS_API_KEY="votre-cle-api"
```

Ou dans un fichier `.env`:
```
RIPE_ATLAS_API_KEY=votre-cle-api
```

## Exemples d'utilisation

### Mesures DNS avec la Tranco list

```python
from scripts.example_dns_measures import fetch_tranco_list, measure_domains

# Recuperer les 1000 domaines les plus populaires
tranco = fetch_tranco_list(top_n=1000)

# Effectuer des mesures DNS
results = measure_domains(tranco['domain'].tolist())
```

### Manipulation de documents

```python
from scripts.document_utils import (
    pdf_to_text,
    docx_to_pdf,
    compile_latex
)

# Extraire le texte d'un PDF
text = pdf_to_text('article.pdf')

# Convertir Word en PDF
docx_to_pdf('rapport.docx')

# Compiler un document LaTeX
compile_latex('memoire.tex')
```

## Notes

- L'image Docker est volumineuse (~5-8 GB) car elle inclut TeXLive complet
- La premiere construction peut prendre 20-30 minutes
- Les volumes Docker preservent vos donnees entre les sessions
