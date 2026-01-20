# Dockerfile pour le projet de memoire: Mesures DNS dans l'espace et le temps
# Environnement Python complet pour recherche DNS, analyse de donnees et redaction

FROM python:3.11-slim-bookworm

LABEL maintainer="DNS Measures Project"
LABEL description="Environnement de travail pour memoire sur les mesures DNS"

# Eviter les prompts interactifs
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Installation des dependances systeme
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Outils de base
    build-essential \
    git \
    curl \
    wget \
    vim \
    nano \
    # DNS tools
    dnsutils \
    bind9-host \
    whois \
    # LaTeX (pour generation de PDF)
    texlive-full \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-lang-french \
    texlive-bibtex-extra \
    biber \
    latexmk \
    # Conversion de documents
    pandoc \
    # LibreOffice pour docx, pptx, xlsx
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    # PDF tools
    poppler-utils \
    ghostscript \
    qpdf \
    pdftk-java \
    # Image tools
    imagemagick \
    libmagickwand-dev \
    # Fonts
    fonts-liberation \
    fonts-dejavu \
    fonts-freefont-ttf \
    # Compression
    zip \
    unzip \
    # Network tools
    iputils-ping \
    traceroute \
    net-tools \
    # Pour les graphiques
    graphviz \
    # Bibliotheques pour Python packages
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    # Pour weasyprint (PDF generation)
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Configurer ImageMagick pour autoriser la conversion PDF
RUN sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/' /etc/ImageMagick-6/policy.xml || true

# Mettre a jour pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Installation des packages Python
# === DNS et Reseau ===
RUN pip install --no-cache-dir \
    dnspython \
    ripe.atlas.cousteau \
    ripe.atlas.sagan \
    ripe.atlas.tools \
    requests \
    httpx \
    aiohttp \
    asyncio \
    ipaddress \
    netaddr \
    tldextract \
    publicsuffixlist

# === Analyse de donnees ===
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    scipy \
    scikit-learn \
    statsmodels

# === Visualisation ===
RUN pip install --no-cache-dir \
    matplotlib \
    seaborn \
    plotly \
    bokeh \
    altair \
    folium \
    geopandas \
    cartopy

# === PDF - Lecture, ecriture, manipulation ===
RUN pip install --no-cache-dir \
    PyPDF2 \
    pypdf \
    pdfplumber \
    pdf2image \
    pikepdf \
    reportlab \
    weasyprint \
    pdfminer.six \
    fitz \
    pymupdf \
    camelot-py[cv]

# === Documents Office (docx, pptx, xlsx) ===
RUN pip install --no-cache-dir \
    python-docx \
    python-pptx \
    openpyxl \
    xlrd \
    xlsxwriter \
    odfpy \
    docx2pdf \
    mammoth

# === Images ===
RUN pip install --no-cache-dir \
    Pillow \
    opencv-python-headless \
    imageio \
    scikit-image \
    svglib \
    cairosvg

# === LaTeX et Markdown ===
RUN pip install --no-cache-dir \
    pylatex \
    latex \
    markdown \
    markdown2 \
    mistune \
    python-markdown-math

# === OCR et extraction de texte ===
RUN pip install --no-cache-dir \
    pytesseract \
    textract || true

# === Jupyter et notebooks ===
RUN pip install --no-cache-dir \
    jupyter \
    jupyterlab \
    notebook \
    ipywidgets \
    nbconvert

# === Base de donnees et stockage ===
RUN pip install --no-cache-dir \
    sqlalchemy \
    sqlite-utils \
    tinydb \
    h5py \
    pyarrow \
    fastparquet

# === Utilitaires ===
RUN pip install --no-cache-dir \
    python-dateutil \
    pytz \
    tqdm \
    rich \
    click \
    typer \
    pyyaml \
    toml \
    python-dotenv \
    loguru \
    tabulate \
    prettytable

# === Web scraping (pour Tranco list, etc.) ===
RUN pip install --no-cache-dir \
    beautifulsoup4 \
    lxml \
    html5lib \
    selenium

# === Serialisation et formats ===
RUN pip install --no-cache-dir \
    orjson \
    ujson \
    msgpack \
    cbor2

# === Tests et qualite ===
RUN pip install --no-cache-dir \
    pytest \
    pytest-asyncio \
    black \
    isort \
    flake8 \
    mypy

# Installer tesseract pour OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-fra \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Creer le repertoire de travail
WORKDIR /workspace

# Creer des repertoires utiles
RUN mkdir -p /workspace/data \
    /workspace/notebooks \
    /workspace/scripts \
    /workspace/reports \
    /workspace/latex \
    /workspace/output

# Copier les fichiers du projet
COPY . /workspace/

# Exposer le port Jupyter
EXPOSE 8888

# Script d'entree
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh || true

# Commande par defaut
CMD ["bash"]
