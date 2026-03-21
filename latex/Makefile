# Makefile pour compilation LaTeX du mémoire
# Auteur: Olivier Gautier

# Fichier principal
MAIN = main
OUTPUT = memoire_dns_measures

# Commandes
LATEXMK = latexmk
PDFLATEX = pdflatex
BIBER = biber
PYTHON = python3

# Options latexmk
LATEXMK_OPTS = -pdf -interaction=nonstopmode -file-line-error

# Fichiers source
CHAPTERS = chapters/01-introduction.tex \
           chapters/02-etat-art.tex \
           chapters/03-methodologie.tex \
           chapters/04-resultats.tex \
           chapters/05-conclusion.tex

MD_SOURCES = chapitre1_introduction.md \
             chapitre2_etat_art.md \
             chapitre3_methodologie.md \
             chapitre4_resultats.md \
             chapitre5_conclusion.md

# Cible par défaut
.PHONY: all
all: pdf

# Compilation PDF complète (recommandé)
.PHONY: pdf
pdf: $(CHAPTERS)
	$(LATEXMK) $(LATEXMK_OPTS) $(MAIN).tex
	@echo "✓ Compilation terminée: $(MAIN).pdf"

# Conversion Markdown → LaTeX
.PHONY: convert
convert:
	$(PYTHON) convert_md_to_tex.py
	@echo "✓ Conversion Markdown → LaTeX terminée"

# Compilation manuelle (2 passes minimum)
.PHONY: manual
manual: $(CHAPTERS)
	$(PDFLATEX) -interaction=nonstopmode $(MAIN).tex
	$(BIBER) $(MAIN)
	$(PDFLATEX) -interaction=nonstopmode $(MAIN).tex
	$(PDFLATEX) -interaction=nonstopmode $(MAIN).tex
	@echo "✓ Compilation manuelle terminée"

# Nettoyage fichiers temporaires
.PHONY: clean
clean:
	$(LATEXMK) -c $(MAIN).tex
	rm -f $(MAIN).run.xml $(MAIN).bbl $(MAIN).bcf
	rm -f *.aux *.log *.out *.toc *.lof *.lot
	rm -f chapters/*.aux
	@echo "✓ Fichiers temporaires supprimés"

# Nettoyage complet (inclut PDF)
.PHONY: cleanall
cleanall: clean
	$(LATEXMK) -C $(MAIN).tex
	rm -f $(MAIN).pdf
	@echo "✓ Nettoyage complet effectué"

# Compilation rapide (draft mode)
.PHONY: draft
draft: $(CHAPTERS)
	$(PDFLATEX) -draftmode -interaction=nonstopmode $(MAIN).tex
	@echo "✓ Compilation draft terminée"

# Vérification LaTeX (sans compilation)
.PHONY: check
check:
	@echo "Vérification présence des fichiers..."
	@test -f $(MAIN).tex && echo "  ✓ $(MAIN).tex" || echo "  ✗ $(MAIN).tex MANQUANT"
	@test -f preamble.tex && echo "  ✓ preamble.tex" || echo "  ✗ preamble.tex MANQUANT"
	@test -f bibliography.bib && echo "  ✓ bibliography.bib" || echo "  ✗ bibliography.bib MANQUANT"
	@for chapter in $(CHAPTERS); do \
		test -f $$chapter && echo "  ✓ $$chapter" || echo "  ✗ $$chapter MANQUANT"; \
	done

# Conversion + Compilation
.PHONY: rebuild
rebuild: convert pdf

# Afficher les erreurs de compilation
.PHONY: errors
errors:
	@grep -i "error\|warning" $(MAIN).log | head -20 || echo "Aucune erreur trouvée"

# Compter les mots (approximatif)
.PHONY: wordcount
wordcount:
	@echo "Comptage des mots (approximatif):"
	@for md in $(MD_SOURCES); do \
		count=$$(wc -w < $$md); \
		echo "  $$md: $$count mots"; \
	done
	@total=$$(cat $(MD_SOURCES) | wc -w); \
	echo "  TOTAL: $$total mots"

# Aide
.PHONY: help
help:
	@echo "Makefile pour compilation LaTeX du mémoire"
	@echo ""
	@echo "Cibles disponibles:"
	@echo "  make          - Compile le PDF (latexmk)"
	@echo "  make pdf      - Identique à 'make'"
	@echo "  make manual   - Compilation manuelle (pdflatex + biber)"
	@echo "  make convert  - Convertit Markdown → LaTeX"
	@echo "  make rebuild  - Conversion + Compilation"
	@echo "  make draft    - Compilation rapide (draft mode)"
	@echo "  make clean    - Supprime fichiers temporaires"
	@echo "  make cleanall - Supprime tout (inclut PDF)"
	@echo "  make check    - Vérifie présence des fichiers"
	@echo "  make errors   - Affiche erreurs de compilation"
	@echo "  make wordcount- Compte les mots (sources Markdown)"
	@echo "  make help     - Affiche cette aide"

# Règle pour générer les chapitres .tex depuis .md
chapters/%.tex: %.md
	$(PYTHON) convert_md_to_tex.py
