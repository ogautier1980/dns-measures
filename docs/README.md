# Documentation du projet DNS Measures

Ce répertoire contient la documentation complète de l'environnement de travail.

## Fichiers

- **[documentation.md](documentation.md)** - Documentation complète (source Markdown)
- **[documentation.pdf](documentation.pdf)** - Documentation complète (PDF généré)

## Contenu de la documentation

La documentation couvre :

1. **Introduction** - Objectifs du projet et composants
2. **Structure du projet** - Organisation des répertoires
3. **Environnement Docker** - Outils et bibliothèques installés
4. **Utilisation** - Commandes et workflows
5. **Configuration RIPE Atlas** - Setup de l'API
6. **Bonnes pratiques** - Conventions et recommandations
7. **Dépannage** - Solutions aux problèmes courants
8. **Scripts utilitaires** - Documentation des scripts
9. **Références** - Articles et ressources
10. **Annexes** - Variables, ports, volumes

## Mise à jour de la documentation

Pour mettre à jour la documentation et régénérer le PDF :

```bash
# Éditer le fichier Markdown
nano docs/documentation.md

# Régénérer le PDF
cd docs
pandoc documentation.md -o documentation.pdf \
  --pdf-engine=xelatex \
  --toc \
  --number-sections
```

**Important** : La compilation se fait en 2 passes automatiquement via pandoc.

## Format

- **Source** : Markdown avec YAML front matter
- **Conversion** : Pandoc → XeLaTeX → PDF
- **Table des matières** : Générée automatiquement
- **Numérotation** : Sections numérotées automatiquement
