# Chapitre 1 - Introduction

## 1.1 Contexte et motivation

### 1.1.1 Le DNS : infrastructure critique d'Internet

Le Domain Name System (DNS), créé en 1983 par Paul Mockapetris, constitue aujourd'hui l'une des infrastructures les plus critiques d'Internet. Son rôle fondamental consiste à traduire les noms de domaine lisibles par l'humain (comme `www.example.com`) en adresses IP utilisables par les machines (comme `93.184.216.34`). Cette fonction de "répertoire téléphonique d'Internet" est si essentielle qu'une défaillance du DNS peut rendre inaccessibles des pans entiers du web, comme l'a démontré la panne historique de Facebook le 4 octobre 2021.

Pourtant, malgré son importance, le DNS demeure **souvent oublié dans les études sur la résilience et la qualité de service d'Internet** (Bortzmeyer, tutorial RIPE Atlas). Cette infrastructure invisible fonctionne si efficacement en arrière-plan que son rôle n'est pleinement reconnu que lorsqu'elle fait défaut.

### 1.1.2 L'information DNS : une donnée éphémère

Le DNS présente une caractéristique unique et problématique pour la recherche : son contenu est **éphémère**. Les administrateurs de zones DNS peuvent modifier à tout moment les enregistrements associés à leurs domaines, **sans qu'aucun historique des changements ne soit automatiquement conservé**. Un domaine qui pointait hier vers un serveur en Europe peut aujourd'hui pointer vers un serveur en Asie, et cette transition ne laisse aucune trace dans l'infrastructure DNS elle-même.

Cette nature éphémère pose un défi majeur pour la recherche académique et l'investigation de sécurité. Comment étudier l'évolution de l'infrastructure Internet si nous ne pouvons pas "remonter le temps" pour observer l'état du DNS à une date donnée ? Comment analyser rétrospectivement un incident de sécurité si les enregistrements DNS critiques ont disparu entre-temps ?

**Exemple concret** : Un chercheur étudiant la propagation d'une campagne de phishing en mars 2024 ne peut plus, en mars 2026, déterminer quelles adresses IP étaient associées aux domaines malveillants utilisés, car ces enregistrements ont été modifiés ou supprimés depuis longtemps.

### 1.1.3 La diversité géographique : une dimension négligée

Au-delà du problème temporel, la recherche DNS fait face à une **limitation spatiale** tout aussi importante. Les réponses DNS ne sont pas uniformes : elles **varient selon la localisation géographique du client** qui effectue la requête.

**Trois mécanismes principaux** expliquent cette diversité :

**1. Content Delivery Networks (CDN)** : Les grands services web (Google, Facebook, Netflix) utilisent des CDN pour distribuer leur contenu depuis des serveurs géographiquement proches des utilisateurs. Lorsqu'un utilisateur en France interroge le DNS pour `www.netflix.com`, il reçoit l'adresse IP d'un serveur européen. Un utilisateur au Japon recevra l'adresse d'un serveur asiatique. Cette optimisation, transparente pour l'utilisateur, réduit drastiquement les temps de latence et améliore l'expérience utilisateur.

**2. Anycast DNS** : Les serveurs DNS racines et de nombreux services utilisent le routage anycast, où une même adresse IP est annoncée depuis plusieurs localisations géographiques. Le routage BGP (Border Gateway Protocol) dirige automatiquement les requêtes vers le serveur le plus "proche" selon des métriques réseau. Mais "proche" au sens BGP ne signifie pas nécessairement "proche" géographiquement, comme l'ont démontré Koch et al. (2021) : plus de 95% des utilisateurs accédant aux serveurs DNS racines subissent une certaine "inflation" de latence, le routage BGP optimisant pour des métriques réseau plutôt que pour la proximité géographique pure.

**3. EDNS Client Subnet (ECS)** : Pour contourner le problème des DNS publics distants (Google DNS 8.8.8.8 utilisé par un client français), l'extension ECS permet au resolver d'inclure le préfixe IP du client dans la requête DNS envoyée au serveur autoritaire. Le serveur peut ainsi géolocaliser le client réel plutôt que le resolver, et retourner une réponse optimisée. Cependant, ECS pose des **problèmes de confidentialité** : le préfixe IP du client est exposé aux serveurs autoritaires et aux intermédiaires réseau (Wang et al., 2018).

**Le problème** : Les infrastructures de mesures DNS existantes, comme OpenINTEL (van Rijswijk-Deij et al., 2016), mesurent depuis **un point unique** (Pays-Bas). Elles collectent quotidiennement les enregistrements DNS de 123 millions de domaines, mais ne capturent qu'une **seule perspective géographique**. La diversité réelle des réponses DNS à travers le monde reste **invisible**.

### 1.1.4 Implications pour la recherche et la sécurité

L'absence d'archivage DNS spatialement et temporellement distribué limite sévèrement plusieurs domaines de recherche :

**Recherche en performance réseau** : Impossible de valider rétrospectivement si un CDN a effectivement optimisé ses redirections DNS pour minimiser la latence globale. Les chercheurs ne peuvent analyser que l'état actuel, pas l'évolution historique.

**Sécurité et investigation d'incidents** : Les domaines malveillants (phishing, C&C de botnets) changent fréquemment d'adresses IP pour échapper aux blacklists. Sans historique DNS géographiquement distribué, il est impossible de cartographier complètement l'infrastructure d'une campagne d'attaque passée.

**Études de centralisation** : Xu et al. (2023) ont révélé qu'une poignée de providers DNS (Cloudflare, Google, AWS) gèrent plus de 48% des domaines mondiaux. Mais cette centralisation varie-t-elle géographiquement ? Les domaines chinois dépendent-ils des mêmes providers que les domaines européens ? Sans mesures distribuées, cette question reste sans réponse.

**Simulation réseau** : Les chercheurs développant des simulateurs réseau ou des environnements de test ont besoin de données DNS réalistes pour reproduire fidèlement Internet tel qu'il était à une date donnée, depuis différentes localisations. Sans archivage DNS spatio-temporel, ces simulations reposent sur des approximations.

---

## 1.2 Problématique de recherche

### 1.2.1 Question principale

Comment concevoir et déployer un **système d'archivage DNS** qui capture la **diversité géographique** des réponses DNS dans le temps, pour les domaines web les plus populaires, de manière éthique, reproductible et exploitable par la communauté scientifique ?

### 1.2.2 Questions secondaires

Cette question principale se décline en quatre sous-questions opérationnelles que notre travail vise à répondre empiriquement :

**Q1 : Diversité géographique**
Quelle proportion de domaines Tranco Top 10K retourne des réponses DNS différentes selon la localisation géographique du client ?

Cette question quantifie l'ampleur du phénomène. Si 80% des domaines populaires retournent la même adresse IP quelle que soit la localisation du client, alors la dimension géographique est secondaire. Si au contraire 80% varient significativement, alors mesurer depuis un point unique (comme OpenINTEL) perd une information critique.

**Q2 : Stabilité temporelle**
Quelle est la stabilité temporelle des enregistrements DNS pour ces domaines ? Observe-t-on des variations jour/semaine/mois ?

Cette question éclaire la dynamique temporelle du DNS. Les enregistrements DNS sont-ils majoritairement stables (changements rares, planifiés) ou volatiles (changements fréquents, imprévisibles) ? La réponse détermine la fréquence de mesure optimale pour un archivage DNS efficace.

**Q3 : Biais géographiques**
Les biais géographiques de RIPE Atlas (91% des sondes en Europe + Amérique du Nord) impactent-ils significativement l'observation de la diversité ?

RIPE Atlas, notre infrastructure de mesures distribuées, présente un biais géographique documenté (Bajpai et al., 2017). Cette question évalue si ce biais limite la validité de nos observations. Si les sondes asiatiques et africaines (minoritaires) apportent des réponses DNS radicalement différentes, alors notre échantillon est biaisé. Si au contraire elles confirment les tendances observées en Europe/Amérique du Nord, le biais est acceptable.

**Q4 : Impact du choix de resolver**
Quel est l'impact du choix de resolver (ISP local vs DNS public comme Google 8.8.8.8) sur les adresses IP observées ?

Cette question dissocie deux sources de variabilité : la localisation géographique du client et le type de resolver utilisé. Les DNS publics (Google, Cloudflare) supportant ECS devraient théoriquement retourner des réponses similaires aux resolvers ISP locaux. Mais qu'en est-il empiriquement ? Cette validation est cruciale pour interpréter correctement nos résultats.

---

## 1.3 Objectifs du mémoire

### 1.3.1 Objectif général

Développer un système opérationnel de mesures DNS distribuées géographiquement qui :
- Archive les réponses DNS pour les domaines Tranco Top 10K
- Mesure depuis ~100 vantage points répartis sur 6 continents (via RIPE Atlas)
- Collecte quotidiennement pendant 3 mois minimum
- Stocke les données dans un format réutilisable (FAIR principles)
- Analyse quantitativement la diversité géographique et la stabilité temporelle

### 1.3.2 Objectifs spécifiques

**1. Concevoir une méthodologie de mesure optimale**
- Sélectionner les domaines à mesurer (Tranco Top 10K)
- Choisir les vantage points RIPE Atlas (critères géographiques, techniques)
- Définir les paramètres DNS (types de requêtes, fréquence, options EDNS)
- Optimiser l'utilisation des crédits RIPE Atlas disponibles

**2. Implémenter un pipeline de collecte et traitement robuste**
- Collecte automatisée via API RIPE Atlas
- Parsing et validation des résultats DNS (filtrage lying resolvers, erreurs)
- Enrichissement métadonnées (GeoIP, AS mapping)
- Stockage 2-tiers (Avro pour archivage, Parquet pour analytics)

**3. Analyser quantitativement les données collectées**
- Mesurer la diversité géographique (proportion domaines variant selon localisation)
- Quantifier la stabilité temporelle (taux de changement jour/semaine/mois)
- Évaluer l'impact du biais géographique RIPE Atlas
- Comparer resolvers ISP vs DNS publics

**4. Partager les données et la méthodologie**
- Publier le dataset sur Zenodo (DOI permanent)
- Documenter complètement la méthodologie (reproductibilité)
- Fournir le code source (GitHub)
- Respecter les principes FAIR (Findable, Accessible, Interoperable, Reusable)

### 1.3.3 Contributions attendues

**Contribution scientifique principale** : Première quantification empirique de la diversité géographique des réponses DNS pour les domaines populaires, sur une période longitudinale de 3 mois.

**Contributions secondaires** :
- Méthodologie reproductible pour mesures DNS distribuées avec RIPE Atlas
- Dataset public réutilisable pour la communauté scientifique
- Validation empirique (ou invalidation) des hypothèses sur ECS et CDN
- Recommandations pour futures infrastructures de mesures DNS distribuées

---

## 1.4 Défis et contraintes

### 1.4.1 Défis techniques

**1. Volume de données**
- 10,000 domaines × 100 sondes × 1 mesure/jour × 90 jours = **90 millions de résultats**
- Après parsing : ~20 GB compressé (Avro) + métadonnées
- Pipeline de traitement devant gérer quotidiennement >1M résultats

**2. Qualité et fiabilité des mesures**
- Interférence entre mesures concurrentes sur RIPE Atlas (Holterbach et al., 2015)
- Désynchronisation scheduling (jusqu'à 1h de décalage possible)
- Lying resolvers et interception DNS réseau (Bortzmeyer, tutorial)
- Nécessité de filtrage et validation rigoureux

**3. Hétérogénéité de l'infrastructure**
- Sondes RIPE Atlas de différentes générations (v1-v5)
- Hardware variable (impact timing selon Holterbach et al.)
- Resolvers hétérogènes (ISP locaux, Google DNS, Cloudflare, etc.)
- Nécessité de normalisation et stratification dans l'analyse

### 1.4.2 Contraintes opérationnelles

**1. Crédits RIPE Atlas limités**
- Budget fixe alloué au projet
- Nécessité d'optimisation :
  - Vérifier mesures existantes avant de lancer (réutilisation)
  - Privilégier mesures récurrentes vs one-shot multiples
  - Ajuster dynamiquement selon consommation observée

**2. Distribution géographique biaisée**
- 91% sondes RIPE Atlas en Europe + Amérique du Nord (Bajpai et al., 2017)
- Sous-représentation Asie, Afrique, Amérique du Sud
- Stratégie de pondération nécessaire pour compenser

**3. Durée limitée du projet**
- Mémoire Master 60 : contrainte temporelle stricte
- Collecte limitée à 3 mois (vs années pour OpenINTEL)
- Trade-off entre profondeur temporelle et autres dimensions

### 1.4.3 Défis éthiques et déontologiques

**1. Impact sur les serveurs DNS cibles**
- Éviter surcharge serveurs autoritaires
- Respecter TTL (pas de requêtes plus fréquentes que recommandé)
- Fréquence modérée : 1 mesure/jour maximum

**2. Vie privée et anonymisation**
- Sondes RIPE Atlas = infrastructure volontaire mais données sensibles
- Pas de publication adresses IP sondes individuelles
- Agrégation statistique uniquement

**3. Reproductibilité vs confidentialité**
- Équilibre entre :
  - Partage complet données (reproductibilité scientifique)
  - Protection vie privée participants RIPE Atlas
- Solution : Anonymisation + agrégation + métadonnées détaillées

---

## 1.5 Approche méthodologique

### 1.5.1 Choix de la liste Tranco

Nous utilisons la **liste Tranco** (Le Pochat et al., 2019) plutôt que les listes commerciales pour trois raisons principales :

**Stabilité** : Tranco change seulement 0.6% quotidiennement vs 50% pour Alexa. Cette stabilité est cruciale pour une étude longitudinale : nous suivons les mêmes domaines dans le temps sans bruit dû à l'instabilité de la liste.

**Résistance à la manipulation** : Tranco requiert 4× plus d'effort pour manipulation que les listes individuelles. Alexa peut être manipulé avec une seule requête HTTP, rendant la liste peu fiable pour la recherche académique.

**Reproductibilité** : Permalinks Tranco (ex: liste `8QNZ`) permettent de citer précisément la version utilisée, garantissant que d'autres chercheurs peuvent reproduire exactement notre sélection de domaines.

Nous nous concentrons sur le **Top 10K** pour équilibrer représentativité (capture les sites majeurs) et faisabilité (compatible avec les crédits RIPE Atlas disponibles).

### 1.5.2 Choix de RIPE Atlas

RIPE Atlas est la plateforme de mesures Internet distribuées la plus adaptée à notre projet :

**Distribution géographique** : 12,900 sondes actives dans 178 pays (Nosyk et al., 2024), offrant une couverture mondiale impossible à obtenir avec une infrastructure propriétaire.

**Mesures DNS natives** : Support complet des mesures DNS (A, AAAA, NS, MX, etc.) avec options avancées (NSID, EDNS, raw DNS answers).

**Accessibilité** : Crédits RIPE Atlas alloués au projet, évitant le coût prohibitif d'une infrastructure dédiée comme OpenINTEL.

**Communauté scientifique** : 600+ publications académiques utilisent RIPE Atlas, garantissant la validité scientifique de nos mesures et la comparabilité avec d'autres travaux.

**Limites acceptées** :
- Biais géographique (91% Europe+NA) → Mitigation par pondération
- Interférence mesures concurrentes → Mitigation par sélection hardware récent
- Crédits limités → Optimisation stratégie de mesure

### 1.5.3 Architecture du système

Notre système s'inspire de l'architecture OpenINTEL (van Rijswijk-Deij et al., 2016) mais l'adapte aux contraintes de RIPE Atlas :

**Étape 1 - Input Data** : Téléchargement hebdomadaire liste Tranco, filtrage domaines invalides/malveillants.

**Étape 2 - Measurement Scheduling** : Configuration mesures RIPE Atlas (100 sondes, 1×/jour, filtres géographiques et techniques).

**Étape 3 - Data Collection** : Collecte quotidienne résultats via API RIPE Atlas.

**Étape 4 - Storage** : Stockage 2-tiers (Apache Avro pour archivage long terme, Apache Parquet pour analytics).

**Étape 5 - Analysis** : Analyses quantitatives répondant aux questions Q1-Q4.

Cette architecture modulaire facilite la maintenance, le débogage et l'extension future du système.

### 1.5.4 Conformité éthique et scientifique

**Éthique** : Conformité complète aux RIPE Atlas Ethics Guidelines :
- Impact minimal sur serveurs DNS (fréquence modérée)
- Transparence mesures (descriptions claires, tags)
- Respect vie privée (anonymisation, agrégation)

**Reproductibilité** : Application stricte des principes FAIR :
- **Findable** : DOI Zenodo, métadonnées riches
- **Accessible** : Données publiques, formats ouverts
- **Interoperable** : Vocabulaire standard, APIs documentées
- **Reusable** : Licence claire (CC BY 4.0), provenance complète

---

## 1.6 Structure du mémoire

Le présent mémoire s'organise en cinq chapitres complémentaires :

**Chapitre 1 - Introduction** (présent chapitre)
Contextualise la problématique, formule les questions de recherche, définit les objectifs et présente l'approche générale.

**Chapitre 2 - État de l'art**
Analyse critique de la littérature scientifique sur :
- Les infrastructures de mesures DNS (OpenINTEL, RIPE Atlas)
- Les listes de classement de sites (Tranco)
- Les travaux connexes sur CDN, anycast et diversité géographique
- La centralisation de l'infrastructure DNS
- Les aspects sécurité et détection

**Chapitre 3 - Méthodologie**
Décrit en détail :
- La sélection des domaines (Tranco Top 10K, filtres)
- La configuration des mesures RIPE Atlas (sondes, paramètres DNS)
- Le pipeline de collecte et traitement (parsing, filtrage, stockage)
- Les méthodes d'analyse pour chaque question de recherche (Q1-Q4)
- Les considérations éthiques et de reproductibilité

**Chapitre 4 - Résultats** (à rédiger après collecte des données)
Présentera :
- Les statistiques descriptives du dataset collecté
- Les résultats quantitatifs pour Q1-Q4
- Les visualisations et analyses statistiques
- Les cas d'étude illustratifs

**Chapitre 5 - Discussion et conclusion** (à rédiger après analyse)
Discutera :
- L'interprétation des résultats
- Les limitations de l'étude
- Les implications pour la recherche et la pratique
- Les perspectives futures

---

## 1.7 Contributions et impact attendus

### 1.7.1 Contributions scientifiques

**Contribution empirique principale** : Première quantification systématique de la diversité géographique des réponses DNS pour les domaines populaires, validée sur 3 mois de collecte continue avec ~100 vantage points mondiaux.

**Dataset public** : Publication d'un dataset unique combinant :
- 90 millions de mesures DNS
- Couverture Tranco Top 10K
- Distribution géographique mondiale
- Période longitudinale 3 mois
- Format FAIR (Avro + Parquet, métadonnées complètes, DOI Zenodo)

**Méthodologie reproductible** : Documentation complète permettant à d'autres chercheurs de :
- Reproduire exactement notre étude
- Étendre à d'autres domaines (Top 100K, domaines spécifiques)
- Adapter à d'autres plateformes (M-Lab, PlanetLab)
- Comparer avec futures mesures (évolution temporelle)

### 1.7.2 Impact pour la communauté

**Recherche en performance réseau** : Les chercheurs étudiant les CDN, l'anycast et l'optimisation de latence disposeront d'un dataset validé pour tester leurs hypothèses et modèles.

**Sécurité et forensics** : Les équipes d'investigation pourront corréler nos données historiques avec des incidents de sécurité passés, cartographiant l'infrastructure de campagnes malveillantes.

**Simulation et émulation** : Les développeurs d'environnements de test réseau pourront utiliser nos données pour configurer des simulations DNS réalistes, reproduisant fidèlement Internet tel qu'il était à une date donnée.

**Politiques publiques** : Les régulateurs et décideurs politiques disposeront de données objectives sur la centralisation géographique de l'infrastructure DNS, informant les débats sur la souveraineté numérique.

### 1.7.3 Perspectives futures

Ce travail pose les fondations pour des études longitudinales plus ambitieuses :

**Extension temporelle** : Notre collecte de 3 mois peut être étendue à plusieurs années, révélant des tendances à long terme (migrations cloud, évolution CDN, consolidation providers).

**Extension spatiale** : L'ajout de sondes RIPE Atlas dans les régions sous-représentées (Afrique, Asie centrale) améliorerait la couverture géographique.

**Extension thématique** : La méthodologie peut être appliquée à :
- Domaines spécifiques (services gouvernementaux, infrastructure critique)
- Types d'enregistrements DNS (AAAA pour IPv6, MX pour email, NS pour délégation)
- Protocoles avancés (DNS-over-HTTPS, DNS-over-TLS, DNSSEC)

**Corrélation avec événements** : Nos données peuvent être corrélées avec :
- Événements géopolitiques (censure DNS, blocages régionaux)
- Incidents techniques (pannes CDN, misconfigurations BGP)
- Campagnes malveillantes (phishing, DDoS, C&C)

---

## 1.8 Organisation du travail

### 1.8.1 Phases du projet

Le projet s'est déroulé en cinq phases successives :

**Phase 1 - Familiarisation** (4 semaines, janvier-février 2026)
- Lecture articles fondamentaux (OpenINTEL, Tranco, RIPE Atlas)
- Recherche bibliographique complémentaire (CDN, anycast, ECS)
- Rédaction Chapitre 2 (État de l'art)

**Phase 2 - Conception** (3 semaines, février-mars 2026)
- Définition méthodologie détaillée
- Développement pipeline collecte/traitement
- Tests pilotes (500 domaines, 10 sondes, 7 jours)
- Rédaction Chapitre 3 (Méthodologie)

**Phase 3 - Collecte** (12 semaines, mars-juin 2026)
- Mesures quotidiennes automatisées
- Monitoring consommation crédits
- Ajustements si nécessaire

**Phase 4 - Analyse** (4 semaines, juin 2026)
- Analyses Q1-Q4
- Génération visualisations
- Interprétation résultats
- Rédaction Chapitre 4 (Résultats)

**Phase 5 - Finalisation** (3 semaines, juin-juillet 2026)
- Discussion et conclusion
- Révision complète mémoire
- Préparation défense
- Rédaction Chapitre 5

### 1.8.2 Critères de réussite

**Technique** :
- ✅ Collecte ≥85% résultats valides (taux exclusion <15%)
- ✅ Couverture ≥95% domaines Tranco Top 10K
- ✅ Distribution géographique ≥4 continents représentés

**Scientifique** :
- ✅ Réponses quantitatives aux 4 questions de recherche
- ✅ Validation statistique (tests appropriés, p-values)
- ✅ Contribution originale (diversité géographique + temporelle)

**Académique** :
- ✅ Mémoire complet et structuré (5 chapitres)
- ✅ Dataset public et reproductible (FAIR principles)
- ✅ Respect éthique et déontologie
- ✅ Défense publique réussie

---

**Fin du Chapitre 1 - Introduction**
