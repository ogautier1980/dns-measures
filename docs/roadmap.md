# Roadmap - Plan de réalisation du mémoire

**Titre** : Mesures DNS dans l'espace et le temps
**Promoteurs** : Fl. Rochet - J. Dejaeghere
**Date de création** : 20 janvier 2026

---

## Vue d'ensemble

Ce document présente la méthodologie complète et les étapes à suivre pour réaliser le mémoire sur les mesures DNS distribuées géographiquement et temporellement.

### Objectif principal

Développer un **système d'archivage DNS** qui capture la diversité géographique des réponses DNS dans le temps, en utilisant la liste Tranco et RIPE Atlas, afin de fournir des données de recherche pour la simulation réseau.

### Défis clés

1. **Volume de données** : Gestion de milliards de requêtes DNS quotidiennes
2. **Distribution géographique** : Mesures depuis différents points sur Terre
3. **Optimisation** : Respecter les quotas RIPE Atlas
4. **Partage de données** : Concevoir une structure facilitant l'accès pour les chercheurs
5. **Éthique** : Éviter la surcharge des serveurs DNS et respecter les bonnes pratiques

---

## Phase 1 : Familiarisation et recherche bibliographique

**Durée estimée** : 2-3 semaines

### 1.1 Lecture des articles fondamentaux

#### Article 1 - Infrastructure OpenINTEL
📄 **van Rijswijk-Deij et al. (2016)** - Infrastructure haute performance pour mesures DNS

**Concepts clés à maîtriser** :
- Architecture en 3 étages (collecte, mesure, stockage)
- Utilisation de LDNS pour la robustesse
- Stratégie de distribution de charge (query pacing)
- Format de stockage : Apache Avro → Parquet
- Métriques de performance : 2 milliards de requêtes/jour
- Impact minimal : 0.3-1.6% du trafic DNS global

**Questions à explorer** :
- Comment adapter cette architecture pour des mesures géographiquement distribuées ?
- Quelles optimisations sont possibles avec des contraintes de crédits RIPE ?
- Comment réduire le volume de stockage sans perdre l'information critique ?

#### Article 2 - Liste Tranco
📄 **Le Pochat et al. (2019)** - Classement robuste de sites web

**Concepts clés à maîtriser** :
- Problèmes des listes commerciales (instabilité, manipulation)
- Méthode d'agrégation (Borda count, Dowdall rule)
- Moyennage temporel (30 jours par défaut)
- Filtres de qualité (réactivité, malveillance)
- Amélioration de stabilité : 0.6% vs 50% de changement quotidien

**Questions à explorer** :
- Quelle taille de liste Tranco utiliser ? (Top 1K, 10K, 100K, 1M ?)
- Faut-il appliquer des filtres supplémentaires ?
- Comment gérer les domaines non-réactifs ?
- Quelle fréquence de mise à jour de la liste ?

### 1.2 Recherche complémentaire

**Conférences à explorer** (notes de Pierre) :
- IEEE S&P, NDSS, USENIX Security (sécurité)
- ACM SIGCOMM (réseaux)

**Requêtes Scopus** :
```
REFEID(2-s2.0-85170646912) AND CONFNAME(IEEE Symposium on Security and Privacy)
REFEID(2-s2.0-84976412290) AND CONFNAME(IEEE Symposium on Security and Privacy)
```

**Recherches à effectuer** :
- Passive DNS : technologies existantes et coûts
- ECS (EDNS Client Subnet - RFC 7871) : impact sur les mesures
- Études récentes utilisant RIPE Atlas pour mesures DNS
- Comparaison OpenINTEL vs autres infrastructures

### 1.3 Documentation initiale

**Livrables** :
- Notes de lecture structurées dans `sources/`
- Tableau comparatif des approches existantes
- Liste des RFCs pertinents (DNS, DNSSEC, ECS, etc.)
- Synthèse dans un notebook Jupyter : `notebooks/2026-01-XX_etat_art.ipynb`

---

## Phase 2 : Analyse et conception du système

**Durée estimée** : 3-4 semaines

### 2.1 Contact avec RIPE Atlas

**Recommandation de Stéphane Bortzmeyer** : L'équipe RIPE Atlas est réactive et aide volontiers les chercheurs.

**Actions** :
1. **Demande de crédits supplémentaires**
   - Rédiger description du projet (2-3 paragraphes)
   - Estimer les besoins en crédits
   - Soumettre via liste de diffusion ou contact direct

2. **Discussion sur les quotas**
   - Expliquer le besoin de mesures continues sur longue période
   - Demander exceptions aux quotas standards si nécessaire
   - Explorer possibilité de mesures régulières automatisées

3. **Validation éthique**
   - Documenter l'approche de mesure
   - Confirmer conformité avec [Ethics of RIPE Atlas Measurements](https://labs.ripe.net/author/kistel/ethics-of-ripe-atlas-measurements/)

### 2.2 Conception de la stratégie de mesure

#### 2.2.1 Sélection des domaines

**Option 1 - Approche conservative** :
- Tranco Top 10K
- Mise à jour hebdomadaire
- ~10,000 domaines à mesurer

**Option 2 - Approche équilibrée** (recommandée) :
- Tranco Top 100K
- Mise à jour hebdomadaire
- Filtres : réactivité HTTP, absence de malveillance
- Estimation : ~80,000-90,000 domaines actifs

**Option 3 - Approche ambitieuse** :
- Tranco Top 1M
- Mise à jour mensuelle
- Filtres stricts
- Nécessite validation de faisabilité avec quotas RIPE

**Décision à prendre** : Basée sur les crédits RIPE disponibles et durée du projet

#### 2.2.2 Types de requêtes DNS

**Requêtes minimales** (OpenINTEL style) :
- SOA (Start of Authority)
- A (IPv4)
- AAAA (IPv6)
- NS (Name Servers)
- MX (Mail Exchange)

**Requêtes étendues** (si crédits suffisants) :
- TXT (SPF, DKIM, etc.)
- DNSSEC : DS, DNSKEY, RRSIG
- CAA (Certificate Authority Authorization)

**Gestion ECS** :
- Utiliser option `+subnet=0/0` pour désactiver ECS si nécessaire
- Documenter comportement ECS des résolveurs utilisés

#### 2.2.3 Distribution géographique

**Stratégie de sélection des sondes RIPE** :

**Niveau 1 - Couverture continentale** :
- Europe : 20-30 sondes
- Amérique du Nord : 15-20 sondes
- Asie : 15-20 sondes
- Amérique du Sud : 5-10 sondes
- Afrique : 5-10 sondes
- Océanie : 5-10 sondes

**Niveau 2 - Diversité AS** :
- Sélectionner sondes de différents ASN (Autonomous Systems)
- Éviter concentration chez un seul fournisseur
- Viser 50-100 ASN distincts

**Niveau 3 - Vérification Geo-IP** :
- Valider localisation des sondes avec MaxMind ou autre base Geo-IP
- Documenter précision de localisation

#### 2.2.4 Fréquence des mesures

**Option conservative** :
- Quotidienne pour domaines critiques (Top 1K)
- Hebdomadaire pour reste de la liste
- Permet détection rapide des changements

**Option équilibrée** (recommandée) :
- Mesure complète hebdomadaire
- Rotation quotidienne par sous-ensemble (1/7 de la liste)
- Compromis entre fraîcheur et consommation de crédits

**Option économique** :
- Mesure hebdomadaire uniquement
- Focus sur stabilité temporelle plutôt que réactivité

### 2.3 Architecture du système

#### 2.3.1 Composants principaux

```
┌─────────────────────────────────────────────────────────────┐
│                    Système de mesure DNS                    │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐
│ Input Manager    │  Récupération Tranco, mise à jour liste
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Measurement      │  Orchestration mesures RIPE Atlas
│ Orchestrator     │  • Création mesures
└────────┬─────────┘  • Monitoring progression
         │            • Gestion erreurs
         ▼
┌──────────────────┐
│ Data Collector   │  Récupération résultats
└────────┬─────────┘  • Polling API RIPE
         │            • Validation données
         ▼
┌──────────────────┐
│ Storage Layer    │  Stockage multi-niveaux
└────────┬─────────┘  • Raw : JSON/Avro
         │            • Processed : Parquet
         │            • Metadata : SQLite/PostgreSQL
         ▼
┌──────────────────┐
│ Analysis Layer   │  Outils d'analyse
└──────────────────┘  • Pandas/Polars
                      • Jupyter notebooks
                      • Visualisations
```

#### 2.3.2 Technologies recommandées

**Langage** : Python 3.11
- Ecosystème riche pour DNS et data science
- Bibliothèques RIPE Atlas natives
- Déjà configuré dans l'environnement Docker

**Bibliothèques clés** :
```python
# Mesures RIPE Atlas
ripe.atlas.cousteau  # API pour créer mesures
ripe.atlas.sagan     # Parsing résultats
ripe.atlas.tools     # Outils CLI

# DNS
dnspython            # Manipulation DNS

# Data processing
pandas               # DataFrames
polars              # Alternative haute performance
pyarrow             # Format Parquet

# Storage
sqlite3             # Metadata légère
sqlalchemy          # ORM si besoin PostgreSQL
h5py                # HDF5 pour time-series

# Analysis
numpy, scipy        # Calculs scientifiques
matplotlib, seaborn # Visualisations
```

**Format de stockage** :

**Niveau 1 - Raw data** :
- JSON (résultats bruts RIPE Atlas)
- Un fichier par mesure ou par jour
- Compression gzip
- Archivage dans `data/raw/YYYY/MM/DD/`

**Niveau 2 - Processed data** :
- Apache Parquet (colonnes : timestamp, domain, probe_id, response_type, response_data, latency, etc.)
- Partitionnement par date et type de requête
- Stockage dans `data/processed/`

**Niveau 3 - Metadata** :
- SQLite pour développement
- PostgreSQL pour production (si besoin)
- Tables : domains, probes, measurements, errors

#### 2.3.3 Workflow de mesure

```
1. Input Update (quotidien/hebdomadaire)
   └─> Téléchargement nouvelle liste Tranco
   └─> Calcul delta (nouveaux/supprimés domaines)
   └─> Filtrage (réactivité, malveillance)

2. Measurement Planning
   └─> Sélection domaines à mesurer (rotation si nécessaire)
   └─> Sélection sondes RIPE (distribution géo + AS)
   └─> Création spécifications mesures

3. Measurement Execution
   └─> Soumission mesures via API RIPE Atlas
   └─> Récupération IDs de mesures
   └─> Monitoring progression (polling status)

4. Data Collection
   └─> Récupération résultats (API ou streaming)
   └─> Validation intégrité
   └─> Stockage raw data

5. Data Processing
   └─> Parsing résultats JSON
   └─> Extraction champs pertinents
   └─> Conversion Parquet
   └─> Indexation metadata

6. Analysis & Reporting
   └─> Métriques quotidiennes/hebdomadaires
   └─> Détection anomalies
   └─> Visualisations
   └─> Rapports automatiques
```

### 2.4 Optimisation pour quotas RIPE

**Stratégies d'optimisation** :

1. **Réutilisation de mesures existantes**
   - Vérifier mesures publiques RIPE existantes
   - S'abonner aux résultats plutôt que créer nouvelles mesures

2. **Mesures one-off vs built-in**
   - One-off : mesures ponctuelles (moins de crédits)
   - Built-in : mesures récurrentes (monitoring long-terme)
   - Choix selon durée projet et besoins

3. **Limitation du nombre de sondes**
   - Trouver équilibre couverture géo vs coût
   - Analyse statistique pour déterminer nombre minimal significatif

4. **Batch processing**
   - Regrouper domaines similaires dans une mesure
   - Réduire overhead API

5. **Mesures DNS natives**
   - Utiliser résolveurs sondes plutôt que requêtes directes
   - Potentiellement moins de crédits

**Livrables** :
- Document d'architecture : `docs/architecture.md`
- Diagrammes UML/C4 dans `docs/diagrams/`
- Estimation budgétaire crédits RIPE
- Planning de mesures sur 6-12 mois

---

## Phase 3 : Développement du prototype

**Durée estimée** : 4-6 semaines

### 3.1 Développement itératif

#### Itération 1 - Proof of Concept (Semaine 1-2)

**Objectifs** :
- Tester API RIPE Atlas avec mesures manuelles
- Valider stockage et parsing de résultats
- Mesurer 100-1000 domaines depuis 10-20 sondes

**Scripts à développer** :
```
scripts/
├── 01_fetch_tranco.py       # Téléchargement liste Tranco
├── 02_filter_domains.py     # Filtrage domaines
├── 03_create_measurement.py # Création mesure RIPE
├── 04_collect_results.py    # Récupération résultats
└── 05_store_data.py         # Stockage Parquet
```

**Validation** :
- Mesures complètes sans erreurs
- Données stockées correctement
- Temps d'exécution acceptable
- Consommation crédits conforme

#### Itération 2 - Orchestration (Semaine 3-4)

**Objectifs** :
- Automatiser workflow complet
- Gérer erreurs et retry
- Monitoring et logging
- Mesurer 10K-50K domaines

**Composants** :
- Orchestrateur principal : `scripts/orchestrator.py`
- Configuration : `config.yaml` (domaines, sondes, fréquence)
- Logging : `loguru` vers fichiers rotatifs
- Monitoring : Métriques temps réel (tqdm, rich)

**Fonctionnalités** :
- Reprise après erreur
- Parallélisation si possible
- Rate limiting API
- Alertes (email/Slack) en cas d'échec

#### Itération 3 - Optimisation et scalabilité (Semaine 5-6)

**Objectifs** :
- Optimiser consommation mémoire
- Accélérer traitement
- Scale à liste complète (100K-1M domaines)

**Optimisations** :
- Streaming processing (éviter chargement complet en mémoire)
- Parallélisation I/O et calculs
- Compression agressive
- Cache intelligent

**Tests de charge** :
- Mesure temps d'exécution par taille de liste
- Profiling Python (cProfile, memory_profiler)
- Identification goulots d'étranglement

### 3.2 Développement analyses

**Notebooks d'analyse** (dans `notebooks/`) :

1. **Analyse exploratoire**
   - `2026-XX-XX_exploration_donnees.ipynb`
   - Distribution géographique des réponses
   - Types d'enregistrements par domaine
   - Latences par région

2. **Analyse temporelle**
   - `2026-XX-XX_evolution_temporelle.ipynb`
   - Stabilité des réponses DNS dans le temps
   - Fréquence des changements d'IP
   - Durée de vie TTL observée vs théorique

3. **Analyse géographique**
   - `2026-XX-XX_diversite_geo.ipynb`
   - Variabilité des réponses par localisation
   - CDN detection (même domaine → IPs différentes)
   - Anycast vs Unicast

4. **Métriques qualité**
   - `2026-XX-XX_qualite_donnees.ipynb`
   - Taux de réussite des mesures
   - Erreurs DNS (NXDOMAIN, SERVFAIL, TIMEOUT)
   - Couverture géographique effective

### 3.3 Validation scientifique

**Cas d'usage de validation** :

1. **Étude CDN (style OpenINTEL)**
   - Identifier domaines utilisant CDN
   - Comparer réponses géographiques
   - Validation avec services connus (Cloudflare, Akamai, etc.)

2. **Évolution infrastructure mail**
   - Tracking MX records dans le temps
   - Migration vers cloud email (Google, Microsoft, Yahoo)
   - Adoption SPF/DKIM/DMARC

3. **Déploiement DNSSEC**
   - Mesure progression DNSSEC par TLD
   - Validation signatures
   - Corrélation avec sécurité domaine

**Livrables** :
- Code source documenté dans `scripts/`
- Tests unitaires : `tests/`
- Notebooks d'analyse dans `notebooks/`
- Rapport intermédiaire : `reports/2026-XX-XX_validation_prototype.pdf`

---

## Phase 4 : Collecte de données à grande échelle

**Durée estimée** : 8-12 semaines (peut se chevaucher avec Phase 5)

### 4.1 Déploiement en production

**Environnement** :
- Serveur dédié ou machine virtuelle (24/7)
- Alternative : Utiliser GitHub Actions / GitLab CI pour mesures régulières
- Backup automatique des données

**Configuration finale** :
- Liste Tranco : Top 100K (ou selon validation Phase 3)
- Sondes RIPE : 50-100 sondes (distribution optimale)
- Fréquence : Hebdomadaire (ou rotation quotidienne)
- Types de requêtes : A, AAAA, NS, MX, SOA minimum

**Monitoring continu** :
- Dashboard temps réel (Grafana + InfluxDB optionnel)
- Logs centralisés
- Alertes automatiques
- Rapports hebdomadaires automatiques

### 4.2 Collecte de données

**Durée minimale recommandée** : 3 mois
**Durée idéale** : 6-12 mois

**Métriques à suivre** :
- Nombre de domaines mesurés par semaine
- Nombre de mesures réussies vs échouées
- Crédits RIPE consommés
- Volume de stockage
- Anomalies détectées

**Points de contrôle qualité** :
- Validation échantillon aléatoire chaque semaine
- Vérification cohérence temporelle
- Détection outliers
- Comparaison avec sources externes si disponibles

### 4.3 Gestion des données

**Backup strategy** :
- Backup quotidien incrémental
- Backup hebdomadaire complet
- Stockage redondant (local + cloud : Google Drive, OneDrive, etc.)
- Vérification intégrité (checksums MD5/SHA256)

**Stockage estimé** (pour référence OpenINTEL: 240GB/jour pour .com) :
- Top 10K domaines : ~1-5 GB/semaine
- Top 100K domaines : ~10-50 GB/semaine
- Top 1M domaines : ~100-500 GB/semaine
- Compression : facteur 3-5x

**Livrables** :
- Dataset de mesures DNS (raw + processed)
- Metadata complet (timestamp, sondes, domaines)
- Rapports hebdomadaires de monitoring
- Log complet des opérations

---

## Phase 5 : Analyse et rédaction du mémoire

**Durée estimée** : 6-8 semaines

### 5.1 Analyses approfondies

#### 5.1.1 Analyse de la diversité géographique

**Questions de recherche** :
- Quelle proportion de domaines retourne des IPs différentes selon la localisation ?
- Quels TLDs/providers utilisent le plus de géo-localisation ?
- Corrélation entre taille du domaine (ranking Tranco) et utilisation CDN ?

**Méthodes** :
- Clustering des réponses par domaine
- Calcul distance géographique IP vs sonde
- Visualisations cartographiques (Folium, Plotly)

#### 5.1.2 Analyse de la stabilité temporelle

**Questions de recherche** :
- Quelle est la durée de vie réelle des enregistrements DNS ?
- Fréquence des migrations infrastructure ?
- Prédictibilité des changements (patterns temporels) ?

**Méthodes** :
- Time-series analysis
- Change detection algorithms
- Survival analysis (durée de vie IP)

#### 5.1.3 Comparaison avec état de l'art

**Benchmarks** :
- Comparer avec OpenINTEL (si données accessibles)
- Comparer avec Passive DNS commercial (si budget)
- Valider hypothèses contre DNS publics connus

### 5.2 Évaluation du système

**Métriques de performance** :
- Débit de mesures (domaines/heure)
- Latence de collecte (soumission → résultats)
- Efficacité crédits RIPE (domaines/crédit)
- Couverture géographique atteinte
- Taux de succès des mesures

**Comparaison objectifs initiaux** :
- Objectif vs réalisé (tableau comparatif)
- Limitations rencontrées
- Optimisations appliquées

### 5.3 Structure du mémoire

#### Chapitre 1 : Introduction
- Contexte et motivation
- Problématique
- Objectifs
- Contributions
- Structure du document

#### Chapitre 2 : État de l'art
- Système DNS : rappels et évolutions
- Mesures DNS actives vs passives
- Infrastructures existantes (OpenINTEL, etc.)
- Listes de domaines (Tranco, Alexa, etc.)
- RIPE Atlas et mesures distribuées
- Travaux connexes : géo-localisation, CDN, etc.

#### Chapitre 3 : Méthodologie
- Architecture du système
- Sélection des domaines (Tranco)
- Stratégie de mesure RIPE Atlas
- Gestion des quotas et optimisations
- Stockage et traitement des données
- Considérations éthiques

#### Chapitre 4 : Implémentation
- Technologies utilisées
- Composants du système
- Workflow de mesure
- Formats de données
- Défis techniques et solutions

#### Chapitre 5 : Résultats et analyses
- Présentation du dataset collecté
- Analyse de la diversité géographique
- Analyse de la stabilité temporelle
- Études de cas (CDN, mail, DNSSEC, etc.)
- Validation scientifique

#### Chapitre 6 : Discussion
- Interprétation des résultats
- Comparaison avec état de l'art
- Limites de l'approche
- Implications pour la recherche
- Amélioration possibles

#### Chapitre 7 : Conclusion et perspectives
- Synthèse des contributions
- Réponses aux questions de recherche
- Perspectives futures
- Ouverture

#### Annexes
- Code source (extraits pertinents)
- Configuration système complète
- Résultats détaillés supplémentaires
- Documentation API

### 5.4 Rédaction LaTeX

**Structure des fichiers** (dans `latex/`) :
```
latex/
├── main.tex                   # Document principal
├── preamble.tex              # Packages et configuration
├── bibliography.bib          # Références bibliographiques
├── chapters/
│   ├── 01-introduction.tex
│   ├── 02-etat-art.tex
│   ├── 03-methodologie.tex
│   ├── 04-implementation.tex
│   ├── 05-resultats.tex
│   ├── 06-discussion.tex
│   └── 07-conclusion.tex
├── figures/                  # Figures et graphiques
│   ├── architecture.pdf
│   ├── workflow.pdf
│   └── ...
└── tables/                   # Tableaux
    └── ...
```

**Rappel compilation LaTeX** (voir `claude.md`) :
```bash
# Méthode recommandée
latexmk -pdf -interaction=nonstopmode main.tex

# Méthode manuelle (2 passes minimum, 3-4 avec bibliographie)
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

**Livrables** :
- Mémoire complet en LaTeX
- PDF final du mémoire
- Présentation soutenance (PowerPoint/Beamer)
- Poster scientifique (optionnel)

---

## Phase 6 : Partage et diffusion des données

**Durée estimée** : 2-3 semaines (parallèle à Phase 5)

### 6.1 Conception de la structure de partage

**Options de partage** :

**Option 1 - Dataset statique** :
- Archive Zenodo avec DOI
- Format Parquet compressé
- Metadata CSV
- README documentation
- Licence ouverte (CC-BY ou similaire)

**Option 2 - API de requête** :
- Service web simple (Flask/FastAPI)
- Requêtes par domaine, date, sonde
- Limite rate pour éviter abus
- Documentation OpenAPI/Swagger

**Option 3 - Portail web** (inspiré OpenINTEL) :
- Interface recherche
- Visualisations interactives
- Téléchargement datasets agrégés
- Programme chercheurs visiteurs (données complètes sur demande)

**Recommandation** : Combiner Option 1 (facile) + Option 2 (flexible)

### 6.2 Documentation des données

**Documentation minimale requise** :

1. **README.md** :
   - Description du dataset
   - Méthodologie de collecte
   - Format des fichiers
   - Schéma des données
   - Exemples d'utilisation
   - Citation recommandée
   - Licence

2. **CHANGELOG.md** :
   - Versions successives
   - Modifications apportées
   - Corrections d'erreurs

3. **Metadata.json** :
   - Dates de collecte
   - Nombre de domaines
   - Nombre de sondes
   - Types de requêtes
   - Configuration RIPE Atlas
   - Statistiques globales

4. **Schema definition** :
   - Description des colonnes
   - Types de données
   - Contraintes
   - Relations

### 6.3 Conformité FAIR (Findable, Accessible, Interoperable, Reusable)

**Findable** :
- DOI via Zenodo
- Metadata complet
- Mots-clés pertinents
- Indexation académique

**Accessible** :
- Téléchargement libre (pas d'authentification obligatoire)
- Formats standards
- Documentation claire
- Contact pour support

**Interoperable** :
- Formats ouverts (Parquet, CSV, JSON)
- Standards DNS respectés
- Schéma documenté
- APIs RESTful si applicable

**Reusable** :
- Licence explicite
- Provenance documentée
- Qualité des données évaluée
- Code de traitement partagé (GitHub)

### 6.4 Publication code source

**Repository GitHub** :
```
dns-measures/ (déjà existant)
├── README.md                     # Documentation projet
├── LICENSE                       # Licence open-source
├── scripts/                      # Scripts de mesure
├── notebooks/                    # Analyses Jupyter
├── docs/                         # Documentation complète
├── tests/                        # Tests unitaires
└── examples/                     # Exemples utilisation données
```

**Bonnes pratiques** :
- Licence MIT ou Apache 2.0 pour le code
- Licence CC-BY pour les données
- Documentation API complète
- Exemples d'utilisation
- Instructions reproductibilité

**Livrables** :
- Dataset public sur Zenodo avec DOI
- API de requête (optionnel)
- Code source sur GitHub
- Documentation complète
- Article de données (Data Paper) potentiel

---

## Phase 7 : Préparation soutenance

**Durée estimée** : 2 semaines

### 7.1 Présentation

**Structure recommandée** (15-20 minutes) :

1. **Introduction** (2 min)
   - Contexte et motivation
   - Problématique
   - Objectifs

2. **État de l'art** (2 min)
   - Travaux existants
   - Limitations
   - Positionnement

3. **Méthodologie** (4 min)
   - Architecture système
   - Stratégie de mesure
   - Technologies utilisées

4. **Résultats** (6 min)
   - Dataset collecté (chiffres clés)
   - Analyse diversité géographique
   - Analyse stabilité temporelle
   - Études de cas marquantes

5. **Discussion** (3 min)
   - Contributions
   - Limites
   - Perspectives

6. **Conclusion** (1 min)
   - Synthèse
   - Impact potentiel

**Questions fréquentes à anticiper** :
- Pourquoi RIPE Atlas plutôt que scan résolveurs ?
- Comment gérer les limitations de quotas ?
- Quelle est la représentativité géographique ?
- Comment valider la qualité des données ?
- Quel est l'impact sur infrastructure DNS ?
- Quelles sont les applications pratiques ?
- Comment améliorer le système ?

### 7.2 Démonstration (si applicable)

**Démo possible** :
- Interface de requête dataset
- Visualisation interactive
- Exemple analyse en temps réel

**Préparation** :
- Tester démo 10x avant soutenance
- Préparer screenshots de backup
- Avoir données de test prêtes

### 7.3 Livrables finaux

**Checklist finale** :
- ☐ Mémoire LaTeX compilé (PDF)
- ☐ Code source GitHub à jour
- ☐ Dataset publié Zenodo
- ☐ Présentation PowerPoint/Beamer
- ☐ Notes personnelles pour questions
- ☐ Démonstration testée (si applicable)
- ☐ Remerciements (promoteurs, collègues, RIPE)
- ☐ Vérification plagiat
- ☐ Relecture par tiers

---

## Recommandations transversales

### Gestion de projet

**Outil de suivi** :
- Utiliser `claude.md` pour journal quotidien/hebdomadaire
- Créer issues GitHub pour tâches
- Plannifier sprints de 2 semaines
- Revues régulières avec promoteurs

**Réunions avec promoteurs** :
- Fréquence : Bi-hebdomadaire recommandé
- Préparer points de discussion
- Documenter décisions prises
- Identifier bloqueurs rapidement

**Gestion du temps** :
- Timeboxing strict par phase
- Identifier dépendances critiques
- Prévoir marge pour imprévus (20%)
- Prioriser ruthlessly

### Communication scientifique

**Documenter au fur et à mesure** :
- Ne pas attendre la fin pour écrire
- Rédiger sections méthodologie dès Phase 2
- Documenter choix techniques immédiatement
- Maintenir log de décisions

**Figures et visualisations** :
- Créer figures publication-ready dès le départ
- Utiliser matplotlib avec style scientifique
- Sauvegarder scripts de génération
- Format vectoriel (PDF/SVG) pour LaTeX

**Bibliographie** :
- Maintenir `latex/bibliography.bib` à jour
- Utiliser gestionnaire références (Zotero, Mendeley)
- Citer au fur et à mesure de la lecture
- Vérifier complétude avant rédaction finale

### Éthique et reproductibilité

**Transparence** :
- Documenter toutes les décisions méthodologiques
- Partager code et données
- Signaler limitations honnêtement
- Citer tous les travaux utilisés

**Respect infrastructure DNS** :
- Suivre bonnes pratiques RIPE Atlas
- Ne pas surcharger serveurs
- Documenter impact du système
- Mécanisme opt-out si applicable

**Reproductibilité** :
- Environnement Docker versionnéé
- Requirements.txt figé (versions exactes)
- Seed pour random si utilisé
- Instructions pas-à-pas

---

## Checklist des livrables par phase

### Phase 1 : Familiarisation
- ☐ Notes de lecture articles principaux
- ☐ Synthèse état de l'art
- ☐ Tableau comparatif approches
- ☐ Liste RFCs pertinents

### Phase 2 : Conception
- ☐ Contact RIPE établi
- ☐ Crédits RIPE obtenus
- ☐ Document architecture système
- ☐ Stratégie de mesure validée
- ☐ Estimation budget crédits

### Phase 3 : Développement
- ☐ Scripts de mesure fonctionnels
- ☐ Orchestrateur automatisé
- ☐ Tests unitaires
- ☐ Notebooks d'analyse
- ☐ Validation prototype

### Phase 4 : Collecte
- ☐ Système en production
- ☐ Monitoring actif
- ☐ Dataset de 3-12 mois
- ☐ Rapports hebdomadaires
- ☐ Backup redondant

### Phase 5 : Analyse et rédaction
- ☐ Analyses approfondies complètes
- ☐ Mémoire LaTeX rédigé
- ☐ Figures publication-ready
- ☐ Bibliographie complète
- ☐ Relecture et corrections

### Phase 6 : Partage
- ☐ Dataset publié Zenodo avec DOI
- ☐ Code GitHub public
- ☐ Documentation données
- ☐ API de requête (optionnel)

### Phase 7 : Soutenance
- ☐ Présentation PowerPoint/Beamer
- ☐ Démonstration testée
- ☐ Questions anticipées
- ☐ PDF mémoire finalisé

---

## Ressources et contacts

### Ressources techniques

**RIPE Atlas** :
- Documentation : https://atlas.ripe.net/docs/
- API : https://atlas.ripe.net/docs/api/v2/
- Contact : atlas@ripe.net
- Liste discussion : ripe-atlas@ripe.net

**Tranco** :
- Site officiel : https://tranco-list.eu/
- API : https://tranco-list.eu/api
- GitHub : https://github.com/DistriNet/tranco-list

**Geo-IP** :
- MaxMind : https://www.maxmind.com/
- Alternatives libres : IP2Location Lite

**Résolveurs publics** :
- Liste : https://www.chaz6.com/files/resolv.conf
- GitHub Trickest : https://github.com/trickest/resolvers

### Contacts experts

**Stéphane Bortzmeyer** : stephane+blog@bortzmeyer.org
- Expert DNS français
- Blog : https://www.bortzmeyer.org/

**Équipe RIPE Atlas** : atlas@ripe.net
- Support technique
- Demandes crédits

**OpenINTEL** : https://www.openintel.nl/
- Visiting researcher program
- Comparaison méthodologique

### Conférences et publications

**Conférences cibles** :
- NDSS (Network and Distributed System Security)
- IEEE S&P (Security and Privacy)
- USENIX Security
- ACM SIGCOMM
- IMC (Internet Measurement Conference)

**Revues** :
- IEEE/ACM Transactions on Networking
- ACM SIGCOMM Computer Communication Review
- IEEE Journal on Selected Areas in Communications

---

## Notes finales

### Points de vigilance

⚠️ **Gestion des quotas RIPE** : Contacter équipe RIPE tôt dans le projet
⚠️ **Volume de données** : Prévoir stockage suffisant (500GB-5TB selon échelle)
⚠️ **Durée collecte** : Minimum 3 mois, idéal 6-12 mois pour résultats significatifs
⚠️ **Backup** : Stratégie redondante indispensable (données irremplaçables)
⚠️ **Documentation continue** : Ne pas remettre à la fin

### Critères de succès

✅ **Technique** :
- Système fonctionnel et automatisé
- Dataset de qualité collecté
- Analyses reproductibles

✅ **Scientifique** :
- Contributions originales identifiées
- Validation méthodologique rigoureuse
- Résultats comparables état de l'art

✅ **Partage** :
- Données publiques et accessibles
- Code open-source
- Documentation complète

✅ **Académique** :
- Mémoire de qualité
- Soutenance réussie
- Publication potentielle

---

**Dernière mise à jour** : 20 janvier 2026
**Auteur** : Pierre Luycx (avec assistance Claude Sonnet 4.5)
**Promoteurs** : Fl. Rochet - J. Dejaeghere
