#!/bin/bash
set -e

# Script d'entree pour le container Docker
# Projet: Mesures DNS dans l'espace et le temps

echo "================================================"
echo "  Environnement DNS Measures - Memoire"
echo "================================================"
echo ""
echo "Outils disponibles:"
echo "  - Python 3.11 avec bibliotheques DNS, data science, documents"
echo "  - LaTeX complet pour redaction du memoire"
echo "  - LibreOffice pour documents Office"
echo "  - Outils PDF (PyPDF2, pdfplumber, etc.)"
echo "  - Jupyter Lab pour notebooks interactifs"
echo ""
echo "Commandes utiles:"
echo "  jupyter lab --ip=0.0.0.0 --allow-root  # Demarrer Jupyter"
echo "  latexmk -pdf document.tex              # Compiler LaTeX"
echo "  python script.py                       # Executer un script"
echo ""

# Si un argument est passe, l'executer
if [ "$#" -gt 0 ]; then
    exec "$@"
else
    exec /bin/bash
fi
