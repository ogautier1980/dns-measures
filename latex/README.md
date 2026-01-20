# LaTeX - Mémoire

Ce répertoire contient les sources LaTeX du mémoire.

## Structure recommandée

```
latex/
├── main.tex              # Document principal
├── preamble.tex          # Préambule et packages
├── chapters/             # Chapitres du mémoire
│   ├── 01-introduction.tex
│   ├── 02-etat-art.tex
│   ├── 03-methodologie.tex
│   ├── 04-resultats.tex
│   └── 05-conclusion.tex
├── figures/              # Figures et images
├── tables/               # Tableaux
├── bibliography.bib      # Références bibliographiques
└── README.md            # Ce fichier
```

## Compilation

### Méthode recommandée avec latexmk
```bash
latexmk -pdf -interaction=nonstopmode main.tex
```

### Compilation manuelle
```bash
pdflatex main.tex
biber main  # ou: bibtex main
pdflatex main.tex
pdflatex main.tex
```

**Important :** Toujours faire au moins 2 passes pour la table des matières et les références croisées.

## Packages utilisés

- `babel[french]` : Support du français
- `biblatex` : Gestion de la bibliographie
- `graphicx` : Inclusion d'images
- `hyperref` : Liens hypertextes
- Autres à ajouter selon les besoins
