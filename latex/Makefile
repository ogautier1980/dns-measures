# Makefile — Compilation LaTeX du mémoire
# 4 versions : Long/Court × EN/FR
#
# Usage :
#   make               → compile toutes les versions
#   make long-en       → version longue EN uniquement
#   make court-fr      → version courte FR uniquement
#   make convert       → Markdown → LaTeX (md/en/ → chapters/)
#   make clean         → supprime les fichiers temporaires
#   make help          → affiche cette aide

LATEXMK  = latexmk -pdf -interaction=nonstopmode -file-line-error
PYTHON   = python3
OUTPUT   = ../output

# ── Fichiers main ──────────────────────────────────────────────────────────────
MAIN_LONG_EN  = main_long_en
MAIN_LONG_FR  = main_fr_long
MAIN_COURT_EN = main
MAIN_COURT_FR = main_fr

# ── Chapitres ──────────────────────────────────────────────────────────────────
CHAPTERS_EN = chapters/01-introduction.tex \
              chapters/02-etat-art.tex \
              chapters/03-methodologie.tex \
              chapters/04-resultats.tex \
              chapters/05-conclusion.tex

CHAPTERS_FR = chapters/01-introduction-fr.tex \
              chapters/02-etat-art-fr.tex \
              chapters/03-methodologie-fr.tex \
              chapters/04-resultats-fr.tex \
              chapters/05-conclusion-fr.tex

CHAPTERS_LONG_EN = long/01-introduction.tex \
                   long/02-state-of-art.tex \
                   long/03-methodology.tex \
                   long/04-results.tex \
                   long/05-conclusion.tex

CHAPTERS_LONG_FR = long/01-introduction-fr.tex \
                   long/02-etat-art-fr.tex \
                   long/03-methodologie-fr.tex \
                   long/04-resultats-fr.tex \
                   long/05-conclusion-fr.tex

# ── Cibles ────────────────────────────────────────────────────────────────────
.PHONY: all long-en long-fr court-en court-fr convert clean cleanall check wordcount help

all: long-en long-fr court-en court-fr

long-en: $(CHAPTERS_LONG_EN)
	$(LATEXMK) $(MAIN_LONG_EN).tex
	cp $(MAIN_LONG_EN).pdf $(OUTPUT)/memoire_long_en.pdf
	@echo "✓ Long EN → $(OUTPUT)/memoire_long_en.pdf"

long-fr: $(CHAPTERS_LONG_FR)
	$(LATEXMK) $(MAIN_LONG_FR).tex
	cp $(MAIN_LONG_FR).pdf $(OUTPUT)/memoire_long_fr.pdf
	@echo "✓ Long FR → $(OUTPUT)/memoire_long_fr.pdf"

court-en: $(CHAPTERS_EN)
	$(LATEXMK) $(MAIN_COURT_EN).tex
	cp $(MAIN_COURT_EN).pdf $(OUTPUT)/memoire_court_en.pdf
	@echo "✓ Court EN → $(OUTPUT)/memoire_court_en.pdf"

court-fr: $(CHAPTERS_FR)
	$(LATEXMK) $(MAIN_COURT_FR).tex
	cp $(MAIN_COURT_FR).pdf $(OUTPUT)/memoire_court_fr.pdf
	@echo "✓ Court FR → $(OUTPUT)/memoire_court_fr.pdf"

convert:
	$(PYTHON) convert_md_to_tex.py
	@echo "✓ Conversion md/en/ → chapters/ terminée"

clean:
	$(LATEXMK) -c $(MAIN_LONG_EN).tex $(MAIN_LONG_FR).tex \
	              $(MAIN_COURT_EN).tex $(MAIN_COURT_FR).tex
	rm -f *.run.xml *.bbl *.bcf chapters/*.aux long/*.aux
	@echo "✓ Fichiers temporaires supprimés"

cleanall: clean
	$(LATEXMK) -C $(MAIN_LONG_EN).tex $(MAIN_LONG_FR).tex \
	              $(MAIN_COURT_EN).tex $(MAIN_COURT_FR).tex
	@echo "✓ Nettoyage complet effectué"

check:
	@echo "=== Vérification des fichiers ==="
	@for f in preamble.tex preamble_fr.tex bibliography.bib \
	          $(MAIN_LONG_EN).tex $(MAIN_LONG_FR).tex \
	          $(MAIN_COURT_EN).tex $(MAIN_COURT_FR).tex; do \
	    test -f $$f && echo "  ✓ $$f" || echo "  ✗ $$f MANQUANT"; \
	done
	@for f in $(CHAPTERS_EN) $(CHAPTERS_FR) $(CHAPTERS_LONG_EN) $(CHAPTERS_LONG_FR); do \
	    test -f $$f && echo "  ✓ $$f" || echo "  ✗ $$f MANQUANT"; \
	done

wordcount:
	@echo "=== Sources longues EN ==="
	@wc -w md/en/*.md
	@echo "=== Sources longues FR ==="
	@wc -w md/fr/*.md

help:
	@echo "Makefile — Compilation du mémoire (4 versions)"
	@echo ""
	@echo "  make              Compile les 4 versions"
	@echo "  make long-en      Version longue EN  → output/memoire_long_en.pdf"
	@echo "  make long-fr      Version longue FR  → output/memoire_long_fr.pdf"
	@echo "  make court-en     Version courte EN  → output/memoire_court_en.pdf"
	@echo "  make court-fr     Version courte FR  → output/memoire_court_fr.pdf"
	@echo "  make convert      Markdown → LaTeX (md/en/ → chapters/)"
	@echo "  make clean        Supprime fichiers temporaires"
	@echo "  make cleanall     Supprime tout (inclut PDF locaux)"
	@echo "  make check        Vérifie présence des fichiers"
	@echo "  make wordcount    Compte les mots des sources Markdown"
