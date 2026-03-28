# Dockerfile — Mesures DNS dans l'espace et le temps
# Environnement de travail : Python 3.11, LaTeX, DNS tools, analyse de données

FROM python:3.11-slim-bookworm

LABEL maintainer="DNS Measures Project"
LABEL description="Environnement de travail pour mémoire sur les mesures DNS"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# ── Dépendances système ────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Outils de base
    build-essential git curl wget vim nano \
    # DNS tools
    dnsutils bind9-host whois \
    # LaTeX complet (compilation mémoire)
    texlive-full texlive-latex-extra texlive-fonts-extra \
    texlive-lang-french texlive-bibtex-extra biber latexmk \
    # Conversion de documents
    pandoc \
    # LibreOffice (conversion docx/pptx → PDF)
    libreoffice libreoffice-writer libreoffice-calc libreoffice-impress \
    # PDF tools (pdftotext, ghostscript, qpdf)
    poppler-utils ghostscript qpdf pdftk-java \
    # Images et schémas
    imagemagick libmagickwand-dev graphviz plantuml \
    # Fonts
    fonts-liberation fonts-dejavu fonts-freefont-ttf \
    # OCR
    tesseract-ocr tesseract-ocr-fra tesseract-ocr-eng \
    # Compression
    zip unzip \
    # Réseau
    iputils-ping traceroute net-tools \
    # Bibliothèques C pour packages Python
    libffi-dev libssl-dev libxml2-dev libxslt1-dev \
    libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev \
    # WeasyPrint / Cairo
    libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Autoriser ImageMagick à lire/écrire des PDF
RUN sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/' \
    /etc/ImageMagick-6/policy.xml || true

# ── Python ─────────────────────────────────────────────────────────────────────
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# ── Workspace ──────────────────────────────────────────────────────────────────
WORKDIR /workspace

RUN mkdir -p data/raw data/processed notebooks scripts reports latex output

COPY . /workspace/

EXPOSE 8888

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh || true

CMD ["bash"]
