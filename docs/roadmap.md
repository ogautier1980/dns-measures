# Roadmap - Plan de réalisation du mémoire

**Titre** : Mesures DNS dans l'espace et le temps
**Auteur** : Olivier Gautier
**Promoteurs** : Fl. Rochet - J. Dejaeghere
**Co-promoteur** : Pierre Luycx
**Programme** : Master 60 en Sciences Informatiques
**Date de création** : 20 janvier 2026
**Dernière mise à jour** : 20 janvier 2026

---

## Vue d'ensemble

Ce document présente la méthodologie complète et les étapes à suivre pour réaliser le mémoire sur les mesures DNS distribuées géographiquement et temporellement, en conformité avec les exigences du programme Master 60 de la Faculté d'Informatique de l'UNamur.

### Objectif principal

Développer un **système d'archivage DNS** qui capture la diversité géographique des réponses DNS dans le temps, en utilisant la liste Tranco et RIPE Atlas, afin de fournir des données de recherche pour la simulation réseau.

### Question de recherche

**Question principale** : Comment concevoir et déployer un système de mesures DNS distribuées géographiquement qui capture la diversité spatiale et temporelle des réponses DNS pour les domaines web les plus populaires ?

**Questions secondaires** :
1. Quelle proportion de domaines retourne des réponses DNS différentes selon la localisation géographique ?
2. Quelle est la stabilité temporelle des enregistrements DNS pour les domaines populaires ?
3. Comment optimiser l'utilisation des crédits RIPE Atlas pour maximiser la couverture géographique et temporelle ?
4. Comment structurer les données collectées pour faciliter leur exploitation par d'autres chercheurs ?

### Défis clés

1. **Volume de données** : Gestion de millions de requêtes DNS
2. **Distribution géographique** : Mesures depuis différents points sur Terre via RIPE Atlas
3. **Optimisation** : Utilisation efficace des crédits RIPE Atlas disponibles
4. **Partage de données** : Concevoir une structure facilitant l'accès pour les chercheurs (conformité FAIR)
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

### 2.1 Configuration RIPE Atlas

**Crédits disponibles** : Crédits RIPE Atlas déjà obtenus ✓

**Actions** :
1. **Planification utilisation des crédits**
   - Estimer la consommation par type de mesure
   - Définir priorités selon budget disponible
   - Planifier sur 3-6 mois de collecte

2. **Configuration compte RIPE**
   - Vérifier solde de crédits actuel
   - Configurer clés API
   - Tester mesures pilotes

3. **Validation éthique**
   - Documenter l'approche de mesure
   - Confirmer conformité avec [Ethics of RIPE Atlas Measurements](https://labs.ripe.net/author/kistel/ethics-of-ripe-atlas-measurements/)
   - Éviter surcharge serveurs DNS

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

**Conformité** : Structure conforme au Guide du mémoire UNamur et template LaTeX fourni.
**Format** : Maximum 100 pages (hors annexes), recto-verso, police Atkinson Hyperlegible.

#### Éléments préliminaires

**Page de garde** (template fourni) :
- Titre du mémoire
- Auteur : Olivier Gautier
- Diplôme : Master 60 en Sciences Informatiques
- Année académique : 2025-2026
- Promoteur : Fl. Rochet
- Co-promoteurs : J. Dejaeghere - Pierre Luycx
- Signature promoteur pour accord de dépôt

**Remerciements** :
- Personnes ayant contribué au travail
- Promoteurs, collègues, RIPE Atlas team, etc.

**Résumé et Abstract** :
- Maximum ½ page chacun (1 page au total)
- Résumé en français
- Abstract en anglais
- Mots-clés / Keywords (3-5 termes)

**Table des matières** :
- Générée automatiquement par LaTeX
- Numérotation limitée à 3 niveaux (ex: 2.1.1)

**Glossaire/Acronymes** (optionnel) :
- DNS, CDN, TLD, DNSSEC, ECS, etc.

#### Chapitre 1 : Introduction (2-3 pages)

**Contenu obligatoire** :
- Définition claire de l'objet du travail
- Mise en contexte de la problématique étudiée
- **Question de recherche explicite**
- Méthode de travail, outils et sources utilisés
- Présentation brève du cheminement du travail (structure)

**Éléments spécifiques** :
- Contexte : importance mesures DNS pour recherche en sécurité/réseaux
- Motivation : limites des approches existantes (coût Passive DNS, centralisation OpenINTEL)
- Objectif : système accessible et reproductible
- Contribution originale et personnelle

#### Chapitre 2 : État de l'art

**Contenu obligatoire** :
- État des connaissances existantes sur le sujet
- **Justification de la problématique** (pertinence et intérêt)
- **Synthèse** (pas un catalogue de références)
- Esprit critique : forces/faiblesses des approches

**Organisation** :
- Toujours un paragraphe introductif avant chaque section
- Section 2.1 : Système DNS (rappels techniques)
- Section 2.2 : Mesures DNS actives vs passives
- Section 2.3 : Infrastructure OpenINTEL
- Section 2.4 : Liste Tranco pour classement sites
- Section 2.5 : RIPE Atlas et mesures distribuées
- Section 2.6 : Travaux connexes (CDN, géo-localisation, DNSSEC)
- Section 2.7 : Synthèse et positionnement

**Rédaction** :
- Écriture scientifique objective (forme passive en français)
- Citations systématiques avec renvois [Auteur, Année]
- Démontrer esprit critique et analytique

#### Chapitre 3 : Question de recherche et hypothèses

**Contenu** :
- **Question de recherche principale** (formulée clairement)
- Questions secondaires si applicable
- Hypothèses de travail
- Lien avec l'état de l'art
- Justification de la méthode choisie

#### Chapitre 4 : Méthodologie

**Contenu obligatoire** :
- Description et **justification** de la méthodologie
- Public-cible / données visées (domaines Tranco, sondes RIPE)
- Étapes de conception du système
- Méthode de collecte de données (RIPE Atlas API)
- Description des analyses prévues

**Sections spécifiques** :
- Section 4.1 : Sélection des domaines (Tranco)
- Section 4.2 : Stratégie de mesure RIPE Atlas
- Section 4.3 : Sélection des sondes (distribution géographique)
- Section 4.4 : Types de requêtes DNS
- Section 4.5 : Fréquence et durée des mesures
- Section 4.6 : Stockage et traitement des données
- Section 4.7 : Considérations éthiques

#### Chapitre 5 : Implémentation

**Contenu** :
- Architecture du système
- Technologies utilisées (Python, bibliothèques)
- Composants principaux
- Workflow de mesure détaillé
- Formats de données (JSON, Parquet)
- Défis techniques rencontrés et solutions

**Écriture objective** : Description factuelle sans interprétation.

#### Chapitre 6 : Résultats

**Contenu obligatoire** :
- **Description objective des données récoltées** (pas d'interprétation)
- Présentation du dataset (chiffres clés, statistiques descriptives)
- Analyse de la diversité géographique (tableaux, graphiques)
- Analyse de la stabilité temporelle
- Études de cas (CDN, mail, DNSSEC)

**Figures et tableaux** :
- Toutes les figures doivent être référencées dans le texte
- Légendes claires et complètes
- Format vectoriel (PDF) pour qualité publication

#### Chapitre 7 : Discussion

**Contenu obligatoire** :
- **Interprétation des résultats** en lien avec :
  - L'état de l'art
  - La question de recherche
  - Les hypothèses
- Implications pratiques pour la recherche
- Implications pour la société (impact sociétal potentiel)
- Comparaison avec travaux similaires (OpenINTEL, etc.)

**≠ Conclusion** : La discussion interprète, la conclusion synthétise.

#### Chapitre 8 : Conclusion (3 pages max)

**Contenu obligatoire** :
- Récapitulation des axes essentiels du travail
- **Réponse à la question de recherche**
- Mise en évidence de l'apport original
- **Critique de la recherche** (limites identifiées)
- Pistes non explorées mais pertinentes (avec justification)
- **Perspectives futures** et ouverture
- Ce qui serait fait différemment avec le recul

#### Bibliographie

**Exigences** :
- Références scientifiques uniquement
- Utilisation **BibTeX** (recommandé avec LaTeX)
- Toutes les références citées dans le texte
- Tous les renvois dans le texte ont une entrée bibliographique
- Format conforme (voir Guide mémoire p.19-20)
- Validation par promoteurs

#### Annexes

**Contenu** :
- Informations complémentaires (non indispensables au raisonnement)
- Code source (extraits significatifs, pas l'intégralité)
- Configuration système complète
- Tableaux statistiques détaillés
- Résultats supplémentaires
- Documentation API

**Organisation** :
- Annexes numérotées (Annexe A, B, C...)
- Table des annexes
- Renvois explicites dans le texte principal

### 5.4 Rédaction LaTeX

**Template obligatoire** : Utiliser le template fourni dans `docs/Template/` (déjà conforme aux exigences).

**Structure des fichiers** (dans `latex/`) :
```
latex/
├── main.tex                   # Document principal (basé sur template)
├── couverture.tex            # Page de garde (du template)
├── configListing.tex         # Configuration code (du template)
├── bibliography.bib          # Références bibliographiques (BibTeX)
├── chapters/
│   ├── 01-introduction.tex
│   ├── 02-etat-art.tex
│   ├── 03-question-recherche.tex
│   ├── 04-methodologie.tex
│   ├── 05-implementation.tex
│   ├── 06-resultats.tex
│   ├── 07-discussion.tex
│   └── 08-conclusion.tex
├── img/                      # Images et logos
│   └── FAC_informatique.png  # Logo faculté (du template)
└── figures/                  # Figures et graphiques générés
    ├── architecture.pdf
    ├── workflow.pdf
    └── ...
```

**Configuration template** (à personnaliser dans `main.tex`) :
```latex
\newcommand{\titreMemoire}{Mesures DNS dans l'espace et le temps}
\newcommand{\auteurMemoire}{Olivier Gautier}
\renewcommand{\diplome}{Mémoire présenté en vue de l'obtention du grade de Master 60 en Sciences Informatiques}
\newcommand{\anneeacademique}{2025-2026}
\newcommand{\promoteur}{Fl. Rochet}
\newcommand{\copromoteur}{J. Dejaeghere - Pierre Luycx}
```

**Bonnes pratiques rédaction** :

1. **Style d'écriture** (Master 60 en français) :
   - Forme passive privilégiée : "Les données ont été collectées..."
   - Phrases courtes (max 3 lignes)
   - Pas de formulation négative complexe
   - Précision scientifique des termes
   - Pas de généralisation sans références

2. **Citations et références** :
   - Utiliser BibTeX systématiquement
   - Format : [Auteur, Année] ou [Auteur, Année, p.X]
   - Exemple : `\cite{vanRijswijk2016}` → [van Rijswijk-Deij et al., 2016]
   - Gérer avec Zotero pour faciliter la gestion

3. **Figures et code** :
   - Package `listings` pour code (déjà configuré dans template)
   - Package `algorithm2e` pour pseudo-code
   - Insérer extraits courts dans texte, code complet en annexes
   - Toutes figures en format vectoriel (PDF) si possible
   - Référencer : `\ref{fig:mafigure}`, `\pageref{fig:mafigure}`

4. **Numérotation** :
   - Maximum 3 niveaux : 2.1.1 (éviter 2.1.1.1.1)
   - Cohérence dans toute la structure

**Outils recommandés** :
- **Overleaf** : Édition LaTeX en ligne collaborative
- **Zotero** : Gestion bibliographie (export BibTeX)
- **DeepL** : Traduction si besoin (avec validation humaine)
- **Grammarly** : Correction orthographique (avec prudence)

**Compilation LaTeX** (voir `claude.md`) :
```bash
# Méthode recommandée (gère automatiquement les passes)
latexmk -pdf -interaction=nonstopmode main.tex

# Méthode manuelle (TOUJOURS 2 passes minimum, 3-4 avec bibliographie)
pdflatex main.tex
biber main          # ou bibtex main si utilisation BibTeX classique
pdflatex main.tex
pdflatex main.tex   # 2e passe pour table des matières et références
```

**Livrables Phase 5** :
- Mémoire complet en LaTeX (sources + PDF)
- Version PDF finale signée par promoteur
- Présentation soutenance (20 min)
- Notes personnelles pour questions jury

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

## Phase 7 : Préparation et défense du mémoire

**Durée estimée** : 2-3 semaines

### 7.1 Modalités de dépôt (Master 60)

**Date limite pour session juin 2026** : **02 juin 2026 à midi**

**4 éléments obligatoires à rendre** :

1. **Exemplaire papier** (1 exemplaire) :
   - Déposé au bureau du secrétariat facultaire
   - **Reliure collée** (pas de couverture plastique)
   - **Page de garde signée par le promoteur** (accord de dépôt)
   - Format A4, recto-verso
   - Max 100 pages hors annexes

2. **Version PDF** :
   - Envoyée à `secretariat.info@unamur.be`
   - Même contenu que version papier

3. **Résumé + Abstract** (1 page Word max) :
   - Résumé en français (½ page max)
   - Abstract en anglais (½ page max)
   - Envoyé à `secretariat.info@unamur.be`

4. **Formulaire Webcampus** :
   - Compléter dans l'espace UE INFOM010
   - Informations : titre, promoteurs, résumé, langue, confidentialité
   - Import vers SIGALE et site BUMP

**Accord promoteur obligatoire** : La signature sur la page de garde atteste de l'accord du promoteur pour le dépôt (cf. REE art. 40).

### 7.2 Préparation de la présentation

**Format défense Master 60** :
- **Durée présentation** : 20 minutes maximum
- **Démonstration** (optionnel) : +10 minutes max (prévenir secrétariat)
- **Questions-réponses** : Variable selon jury
- **Défense publique** : Ouverture au public

**Structure recommandée présentation (20 min)** :

1. **Introduction** (2-3 min)
   - Contexte et motivation
   - **Question de recherche claire**
   - Objectifs du travail

2. **État de l'art** (2 min)
   - Travaux existants (OpenINTEL, Passive DNS)
   - Limitations identifiées
   - Positionnement de votre contribution

3. **Méthodologie** (4-5 min)
   - Question de recherche et hypothèses
   - Architecture système
   - Stratégie de mesure RIPE Atlas
   - Choix techniques justifiés

4. **Résultats** (6-7 min)
   - Dataset collecté (chiffres clés)
   - Analyse diversité géographique (figures marquantes)
   - Analyse stabilité temporelle
   - Études de cas significatives (CDN, etc.)

5. **Discussion** (3 min)
   - Interprétation résultats
   - Contributions originales
   - Limites identifiées
   - Implications pour la recherche

6. **Conclusion** (1-2 min)
   - Réponse à la question de recherche
   - Perspectives futures
   - Ouverture

**Conseils préparation** (cf. Guide mémoire p.23-24) :

1. **Contenu** :
   - Sélectionner informations essentielles (pas un copier-coller du mémoire)
   - Mettre en avant votre **contribution personnelle**
   - Montrer maîtrise de la problématique
   - Préparer réponses aux questions prévisibles

2. **Support visuel** :
   - 10-15 transparents (PowerPoint ou Beamer LaTeX)
   - Structure claire et lisible
   - Pas de lecture textuelle des slides
   - Plan de présentation au début (guide pour public)
   - Figures/graphiques de qualité

3. **Répétition** :
   - **Répéter 5-10 fois minimum** devant proches/collègues
   - Vérifier timing (strict 20 min)
   - Tester cohérence discours
   - Anticiper questions et préparer réponses

**Questions fréquentes à anticiper** :
- Pourquoi RIPE Atlas plutôt que scan direct de résolveurs ?
- Comment avez-vous géré les limitations de crédits RIPE ?
- Quelle est la représentativité géographique réelle de vos mesures ?
- Comment validez-vous la qualité et l'exactitude des données ?
- Quel est l'impact de vos mesures sur l'infrastructure DNS ?
- Quelles sont les applications concrètes de vos données ?
- Comment amélioreriez-vous le système avec le recul ?
- Quelles sont les limites principales de votre approche ?

### 7.3 Démonstration (optionnel)

**Si démonstration prévue** :
- **Prévenir le secrétariat au moment du dépôt**
- Durée max : 10 minutes (en plus des 20 min de présentation)
- L'horaire sera adapté en conséquence

**Démo possible** :
- Interface de requête du dataset
- Visualisation interactive géographique
- Exemple d'analyse en temps réel
- Reproduction d'une mesure RIPE Atlas

**Préparation** :
- Tester démo **10x minimum** avant la défense
- Préparer screenshots de backup (si problème technique)
- Avoir données de test prêtes et chargées
- Vérifier compatibilité matériel salle de défense

### 7.4 Déroulement du jour J

**Timing défense** :

1. **Avant votre entrée** (huis clos jury) :
   - Promoteur présente objectifs et contexte du travail
   - Jury donne note provisoire sur base du texte écrit

2. **Défense publique** (vous + audience + jury) :
   - Vous présentez votre travail (20 min)
   - Démonstration si applicable (+10 min)
   - Questions-réponses avec jury

3. **Après votre sortie** (huis clos jury) :
   - Jury délibère et propose note finale
   - Appréciation communiquée si président le souhaite
   - Note officielle lors de proclamation session

### 7.5 Critères d'évaluation du jury

**Objectifs d'apprentissage évalués** :
- ✓ Connaissances approfondies dans la thématique
- ✓ Travail original et personnel
- ✓ Intégration et mobilisation connaissances (revue critique littérature)
- ✓ Esprit critique et systématique
- ✓ Autonomie dans le travail
- ✓ Communication écrite scientifique (style, rigueur, clarté)
- ✓ Communication orale des résultats

**Échelle de notation** (guide indicatif) :
- **10/20** : Objectifs minima atteints sans originalité
- **12/20** : Objectifs atteints correctement
- **14/20** : Travail élégant avec originalité
- **16/20** : Apport personnel significatif (synthèse, implémentation)
- **18/20** : Travail exceptionnel et publiable

### 7.6 Checklist finale dépôt

**Documents à préparer** :
- ☐ Mémoire LaTeX compilé PDF (version finale relue)
- ☐ Exemplaire papier imprimé et relié (reliure collée)
- ☐ **Page de garde signée par promoteur** (accord dépôt)
- ☐ PDF identique envoyé à `secretariat.info@unamur.be`
- ☐ Résumé + Abstract (1 page Word) envoyé au secrétariat
- ☐ Formulaire Webcampus INFOM010 complété
- ☐ Code source GitHub à jour et documenté
- ☐ Dataset publié (Zenodo ou autre) si applicable
- ☐ Présentation PowerPoint/Beamer (20 min)
- ☐ Notes personnelles pour questions jury
- ☐ Démonstration testée (si applicable)
- ☐ Vérification anti-plagiat effectuée
- ☐ Relecture par tiers (orthographe, cohérence)

**Validation finale** :
- ☐ Promoteur a relu version finale
- ☐ Promoteur a donné accord formel pour dépôt
- ☐ Toutes références bibliographiques vérifiées
- ☐ Toutes figures/tableaux référencées dans texte
- ☐ Annexes numérotées et référencées
- ☐ Table des matières générée (2 passes LaTeX minimum)
- ☐ Format conforme (100 pages max, police Atkinson, marges correctes)

---

## Recommandations transversales

### Gestion de projet

**Outil de suivi** :
- Utiliser `claude.md` pour journal quotidien/hebdomadaire
- Créer issues GitHub pour tâches
- Planifier sprints de 2 semaines
- Revues régulières avec promoteurs

**Réunions avec promoteurs** :
- **Fréquence minimale** : 1 fois par mois (cf. Guide mémoire)
- **Recommandé** : Bi-hebdomadaire pour suivi actif
- Préparer points de discussion en avance
- Documenter décisions prises
- Envoyer brouillons **suffisamment tôt** pour relecture
- Identifier bloqueurs rapidement
- **Initiative étudiante** : C'est à vous de solliciter les rencontres

**Rôle du promoteur** (cf. Guide mémoire) :
- Orientation et conseil (pas réalisation)
- Aide à définir question de départ, problématique, méthode
- Critique et apprécie l'avancement
- Lit parties au fur et à mesure
- Relit version finale avant dépôt
- **Donne ou non l'accord pour le dépôt** (responsabilité académique)

**Gestion du temps** :
- Timeboxing strict par phase
- **Planning Gantt recommandé** (outil : http://www.gantt.com/fr/)
- Identifier dépendances critiques
- Prévoir marge pour imprévus (20%)
- **Rédaction prend toujours plus de temps que prévu**
- Fixer dates de relecture avec promoteur en avance

### Communication scientifique

**Post-its du mémoire** (cf. Guide p.16-18 - à garder en tête) :

1. **Planning et suivi** :
   - Tenir planning à jour
   - Respecter délais (rédaction prend du temps)
   - Professors en congé été (anticiper pour session septembre)

2. **Écriture scientifique** :
   - Forme passive en français ("les données ont été collectées")
   - Phrases courtes et structures simples
   - Pas de récit personnel, écriture objective
   - Attention orthographe et grammaire

3. **Esprit de synthèse** :
   - Qualité > quantité (100 pages max suffisent)
   - Aller à l'essentiel
   - Reformuler avec vos mots (éviter phrases toutes faites)
   - **Citations systématiques** (plagiat = 0/20)

4. **Table des matières** :
   - Fil conducteur indispensable
   - Établir structure complète avant d'écrire
   - Faire valider par promoteur dès le début
   - Adapter en cours de route si nécessaire

5. **Rôle de chercheur** :
   - Rigueur, honnêteté, esprit critique
   - Écriture objective appuyée sur faits
   - Éviter "je pense que..." sans fondement
   - Argumenter avec données vérifiables

6. **Garder traces** :
   - Carnet de notes tout au long du projet
   - Documenter lectures, réflexions, résultats
   - Classer par mots-clés ou code couleur
   - Gain de temps pour rédaction finale

7. **Sauvegardes multiples** :
   - Clé USB + cloud (Drive, OneDrive) + email
   - **"Pas de sauvegardes excessives, que du temps gaspillé à refaire"**
   - Vérifier intégrité régulièrement

**Documenter au fur et à mesure** :
- **Ne pas attendre la fin pour écrire**
- Rédiger sections méthodologie dès Phase 2
- Documenter choix techniques immédiatement
- Maintenir log de décisions
- **Introduction et conclusion en fin** (besoin vue d'ensemble)
- Fiches de lecture pour état de l'art (cf. Guide p.21-22)

**Figures et visualisations** :
- Créer figures publication-ready dès le départ
- Utiliser matplotlib avec style scientifique
- Sauvegarder scripts de génération
- Format vectoriel (PDF/SVG) pour LaTeX
- **Toutes figures référencées dans texte** (obligation)
- Légendes claires et auto-suffisantes

**Bibliographie** (cf. Guide p.19-20) :
- Maintenir `latex/bibliography.bib` à jour avec **BibTeX**
- Utiliser gestionnaire références (**Zotero recommandé**)
- Citer au fur et à mesure de la lecture
- **Références scientifiques uniquement**
- Vérifier complétude avant rédaction finale
- **Consulter promoteur pour valider bibliographie**
- Toute référence citée doit être consultée
- Tout renvoi dans texte doit avoir entrée bibliographique

### Éthique et intégrité académique

**Plagiat** (cf. Guide p.3, 9) :
- **INTERDIT et PUNISSABLE** (note 0/20 possible)
- Citer systématiquement toutes les sources
- Reformuler avec vos propres mots
- Ressources UNamur : https://www.unamur.be/plagiat
- Vérification anti-plagiat avant dépôt

**Transparence** :
- Documenter toutes les décisions méthodologiques
- Partager code et données (principe FAIR)
- **Signaler limitations honnêtement** (attendu en conclusion)
- Citer tous les travaux utilisés
- Éviter généralisation abusive sans références

**Respect infrastructure DNS** :
- Suivre bonnes pratiques RIPE Atlas
- **Ne pas surcharger serveurs** (éthique mesures)
- Documenter impact du système
- Respecter quotas et limites
- Impact minimal sur infrastructure (cf. OpenINTEL : 0.3-1.6%)

**Reproductibilité** :
- Environnement Docker versionné
- Requirements.txt figé (versions exactes)
- Seed pour random si utilisé
- Instructions pas-à-pas dans README
- Code commenté et documenté
- Dataset partagé avec metadata complet

---

## Checklist des livrables par phase

### Phase 1 : Familiarisation
- ☐ Notes de lecture articles principaux
- ☐ Synthèse état de l'art
- ☐ Tableau comparatif approches
- ☐ Liste RFCs pertinents

### Phase 2 : Conception
- ☐ Configuration RIPE vérifiée (crédits disponibles ✓)
- ☐ Document architecture système
- ☐ Stratégie de mesure validée avec promoteurs
- ☐ Planning utilisation crédits sur 3-6 mois
- ☐ **Table des matières validée par promoteurs**

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
- ☐ **État de l'art rédigé** (synthèse, pas catalogue)
- ☐ **Question de recherche formulée clairement**
- ☐ **Méthodologie rédigée et justifiée**
- ☐ **Résultats décrits objectivement** (sans interprétation)
- ☐ **Discussion rédigée** (interprétation résultats)
- ☐ **Introduction et conclusion rédigées** (en fin de travail)
- ☐ Mémoire LaTeX complet (template UNamur utilisé)
- ☐ Figures publication-ready référencées dans texte
- ☐ Bibliographie complète BibTeX validée par promoteurs
- ☐ Relecture complète (orthographe, cohérence)
- ☐ Vérification anti-plagiat
- ☐ **Accord promoteur pour dépôt** (signature page de garde)

### Phase 6 : Partage données
- ☐ Dataset publié Zenodo avec DOI (principe FAIR)
- ☐ Code GitHub public et documenté
- ☐ Documentation complète données (README, metadata)
- ☐ API de requête (optionnel)
- ☐ Licence appropriée (CC-BY données, MIT/Apache code)

### Phase 7 : Dépôt et soutenance
- ☐ **4 éléments dépôt rendus avant 02 juin 2026 12h00** :
  - ☐ Exemplaire papier relié (reliure collée, page garde signée)
  - ☐ PDF envoyé secretariat.info@unamur.be
  - ☐ Résumé + Abstract (1 page Word) envoyé secrétariat
  - ☐ Formulaire Webcampus INFOM010 complété
- ☐ Présentation 20 min préparée (PowerPoint ou Beamer)
- ☐ **Répétition présentation 5-10 fois minimum**
- ☐ Démonstration testée 10x si applicable (prévenir secrétariat)
- ☐ Questions jury anticipées et réponses préparées
- ☐ Notes personnelles pour questions

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

## Contacts et ressources UNamur

### Encadrement académique

**Promoteur** :
- Fl. Rochet

**Co-promoteurs** :
- J. Dejaeghere
- Pierre Luycx

**Coordinatrice pédagogique** :
- Fanny Boraita : fanny.boraita@unamur.be (bureau 309)
- Aide méthodologique (structure mémoire, rédaction, etc.)
- Gestion attribution sujets et validation dépôts

**Vice-doyen** :
- Marie-Ange Remiche : vice-doyen.info@unamur.be (bureau 206)
- Responsable procédure et calendrier mémoires

**Secrétariat facultaire** :
- Email : secretariat.info@unamur.be (bureau 202a)
- Conseil stages, composition jury, horaires

### Ressources UNamur

**Page mémoire faculté** :
- https://www.info.unamur.be/memoires/
- Sujets, promoteurs, template LaTeX, guide, calendrier

**Ressources plagiat** :
- https://www.unamur.be/plagiat
- Documentation sensibilisation propriété intellectuelle

**Outils recommandés** :
- Overleaf (LaTeX en ligne)
- Zotero (gestion bibliographie)
- DeepL (traduction avec validation)
- Grammarly (correction orthographique)

**Calendrier Master 60** :
- Dépôt session juin 2026 : **02 juin 2026 à midi**
- Dépôt session septembre 2026 : 18 août 2026 à midi

---

**Dernière mise à jour** : 20 janvier 2026
**Auteur du mémoire** : Olivier Gautier
**Promoteur** : Fl. Rochet
**Co-promoteurs** : J. Dejaeghere - Pierre Luycx
**Programme** : Master 60 en Sciences Informatiques - UNamur
**Roadmap rédigé avec** : Claude Sonnet 4.5

---

## Note de mise à jour

Ce roadmap a été mis à jour pour intégrer :
- ✅ Instructions du Guide du mémoire UNamur (2025-2026)
- ✅ Présentation méthodologique Master 60 (22/10/2025)
- ✅ Template LaTeX officiel fourni (docs/Template/)
- ✅ Suppression point crédits RIPE (déjà acquis)
- ✅ Conformité exigences Master 60
- ✅ Structure mémoire détaillée selon guide
- ✅ Modalités dépôt et défense précises
- ✅ Critères évaluation jury
- ✅ Bonnes pratiques rédaction scientifique
