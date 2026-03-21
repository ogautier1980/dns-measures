# Fiche de lecture - OpenINTEL Infrastructure

**Référence bibliographique** :
van Rijswijk-Deij, R., Jonker, M., Sperotto, A., & Pras, A. (2016). A High-Performance, Scalable Infrastructure for Large-Scale Active DNS Measurements. *IEEE Journal on Selected Areas in Communications*, 34(6), 1877–1888. https://doi.org/10.1109/JSAC.2016.2558918

**Thème** : Infrastructure de mesures DNS actives à grande échelle

**Intérêt pour le mémoire** :
Article fondateur décrivant OpenINTEL, l'infrastructure de référence pour mesures DNS à grande échelle. Base architecturale et méthodologique directe pour notre projet. Permet de positionner notre contribution (ajout de la diversité géographique via RIPE Atlas).

---

## Contexte de lecture

**Date de lecture** : 20 janvier 2026
**Section du mémoire** : 2.3 (État de l'art - Infrastructure OpenINTEL)

---

## Contenu de l'article

### Objectif(s) / Question(s) de recherche

**Question principale** : "How can one perform a daily active DNS measurement of a significant proportion of all domains on the Internet?"

**Objectif** : Collecter quotidiennement les données DNS pour TOUS les domaines des principaux TLDs (.com, .net, .org = 50% du DNS global) sur de longues périodes (plusieurs années).

**Motivation** :
- DNS éphémère : pas d'historique des changements
- Besoin de simuler Internet dans un état passé
- Infrastructures existantes mesurent depuis un seul point
- **Problème** : Réponses DNS varient selon localisation géographique (CDN, optimisation latence)

### Cadre global d'explication

**Contexte DNS** :
- DNS = infrastructure critique d'Internet
- Contenu DNS révèle pratiques opérationnelles (IPv6, DNSSEC, cloud services, etc.)
- Mesures DNS = fenêtre sur évolution d'Internet

**Limitation travaux existants** :
- Portée limitée en temps, couverture DNS ou nombre de domaines
- Pas de mesures continues à grande échelle
- Pas de prise en compte diversité géographique

### Méthodologie

**Type d'étude** : Développement infrastructure + validation expérimentale

**Architecture système (3 étages)** :

#### Stage I - Input Data Collection
- Collecte zones DNS TLD (2x/jour)
- Calcul delta quotidien (domaines ajoutés/supprimés)
- Base de données par TLD (état actuel + historique)

#### Stage II - Measurement
- **Cluster manager** : orchestration, distribution travail
- **Worker nodes** (VMs) :
  - Queries DNS multithreadées
  - Resolver local Unbound (cache + distribution queries)
  - Utilise LDNS pour robustesse
  - Enrichissement métadonnées (IP-to-AS, GeoIP)
- **Metadata server** : IP-to-AS mappings, GeoIP

#### Stage III - Storage and Analysis
- **Stockage 2 tiers** :
  1. Apache Avro (archivage long terme, compression 1:7.4)
  2. Apache Parquet (analyse Hadoop, columnar storage)
- **Analyse** : Apache Impala (requêtes SQL batch)

**Outils utilisés** :
- LDNS : parsing DNS, génération queries
- Unbound : résolution récursive, caching
- Apache Avro : sérialisation données structurées
- Apache Parquet : stockage columnar pour analytics
- Apache Impala : requêtes SQL sur Hadoop
- OpenStack : infrastructure cloud privée

**Échelle mesures (pour .com)** :
- 123M domaines
- 14 queries/domaine + 1 query récursion = 15 queries/domaine
- Total : ~1.85 milliards queries/jour
- Stockage : >240GB/jour compressé

**Protocole de mesure** :
- Fréquence : 1x/jour (exactement toutes les 24h)
- Types de requêtes : voir Table I (SOA, NS, A, AAAA, MX, TXT, DS, SPF, DNSKEY, NSEC3)
- Distribution géographique : **UN SEUL point de mesure** (limitation reconnue)

**Données collectées** :
- Resource records (answer section)
- Signatures DNSSEC
- CNAME chains complètes
- Métadonnées : IP-to-AS, GeoIP

### Résultats principaux

#### Performance (Mars-Décembre 2015)

**TLD .com** :
- 123M domaines
- 80 worker VMs
- Durée moyenne batch : 54 min (σ = 6 min)
- Durée totale mesure/jour : 17h 10 min (σ = 2h 23 min)
- ✅ Dans fenêtre 24h avec marge confortable

**TLD .net** :
- 15.6M domaines
- 10 worker VMs
- Durée totale : 14h 29 min (σ = 2h 15 min)

**TLD .org** :
- 10.9M domaines
- 10 worker VMs
- Durée totale : 7h 19 min (σ = 57 min)

**Résultats collectés (31 déc 2015)** :
- .com : 141M résultats pour 119.4M domaines (11.68 résultats/domaine)
- Taux échec : 0.92% (.com), 1.05% (.net), 1.47% (.org)
- Compression : 1:7.4 stable
- Total données : >10TB compressé depuis février 2015

#### Impact sur infrastructure DNS globale

**Analyse trafic réseau** (sampling 1:100) :

**Top talkers** :
- 13 serveurs gTLD (.com/.net) : ~400 queries/sec chacun
- **Impact estimé** : 0.3-1.6% du trafic DNS global
- Charge max serveur individuel : <400 pps
- Validation Verisign : trafic visible mais non problématique

**Distribution queries** :
- 99%+ des flows : <100 pps
- Seulement 35 IPs : >100 pps (serveurs gTLD + domain parking)
- Pas de surcharge identifiée

**Caching efficace** :
- Unbound distribue queries sur multiples name servers
- TTL 24h pour cache infrastructure
- Réduction charge serveurs autoritatifs

#### Scalabilité démontrée

✅ **Goal G2** : Mesure .com (123M noms) réussie
✅ **Goal G4** : 1 mesure/domaine/24h respecté
✅ **Goal G5** : >1 an de données collectées
✅ **Goal G6** : Analyse efficace (511B data points en <2h)
✅ **Challenge C2** : Impact DNS acceptable (0.3-1.6%)

### Conclusion des auteurs

**Contributions principales** :
1. ✅ Scalabilité : Mesure .com (123M domaines) quotidiennement
2. ✅ Impact contrôlé : 0.3-1.6% trafic DNS global (acceptable)
3. ✅ Stockage efficace : Avro + Parquet, compression 1:7.4
4. ✅ Système robuste : 10 mois opération continue sans incident majeur

**Validation** : 2 case studies cloud email (Google, Microsoft, Yahoo)
- Microsoft Office 365 croît plus vite que Google
- SPF usage : 92.4% (Microsoft) vs 34.4% (Google)

**Data sharing** :
- Portal web : http://www.openintel.nl/
- Programme chercheurs visiteurs
- Datasets agrégés publics

**Limites reconnues** :
- ❌ **UN SEUL point de mesure** géographique
- Pas de diversité géographique des réponses DNS
- Performance dégradée pour domaines distants (Chine)

**Travaux futurs** :
- Expansion à d'autres TLDs (ccTLDs, new gTLDs)
- Distribution géographique des workers (amélioration performance)
- Collaboration avec CSIRTs (sécurité, forensics)

---

## Analyse personnelle

### Que garder pour le mémoire

**Concepts clés à réutiliser** :
- ✅ Architecture 3 étages (Input - Measurement - Storage)
- ✅ Approche distribuée (manager + workers)
- ✅ Stockage 2 tiers (Avro archivage + Parquet analytics)
- ✅ Utilisation LDNS + Unbound (robustesse)
- ✅ Query pacing via resolver (pas de rate limiting actif)
- ✅ Enrichissement métadonnées (IP-to-AS, GeoIP)
- ✅ Caching infrastructure (TTL 24h)

**Méthodes applicables** :
- Chunk-based work distribution
- Multithreading pour queries DNS
- Monitoring batch duration pour scaling
- Failover automatique (chunk reassignment)
- Validation impact réseau (flow analysis)

**Chiffres/statistiques importantes** :
- 14 queries/domaine (types de records)
- 1.85B queries/jour pour .com
- 0.3-1.6% trafic DNS global = acceptable
- Compression 1:7.4 pour stockage
- <1% domaines en échec (lame delegations)
- 400 pps max par serveur gTLD
- 511B data points analysés en <2h (Impala)

**Limites identifiées (gaps à combler)** :
- ❌ **UN SEUL vantage point géographique** ← Notre contribution !
- ❌ Pas de mesure diversité géographique réponses DNS
- ❌ Performance dégradée pour domaines distants
- ❌ Pas adapté pour mesures sensibles à la localisation (CDN, ECS)

### Critique personnelle

**Forces de l'article** :
- ✅ Méthodologie très détaillée et reproductible
- ✅ Validation expérimentale solide (10 mois données)
- ✅ Analyse d'impact réseau rigoureuse
- ✅ Design scalable et robuste (prouvé)
- ✅ Case studies pertinents (cloud email)
- ✅ Open science (data sharing)
- ✅ Publication IEEE JSAC (journal prestigieux)

**Faiblesses identifiées** :
- ⚠️ Limitation majeure : un seul point de mesure
- ⚠️ Pas d'analyse ECS (EDNS Client Subnet) impact
- ⚠️ Pas de comparaison quantitative avec Passive DNS
- ⚠️ Données limitées aux 3 gTLDs (.com, .net, .org)
- ⚠️ Pas de discussion coût infrastructure (ressources nécessaires)
- ⚠️ Analyse case studies superficielle (pourrait être plus approfondie)

**Lien avec autres articles lus** :
- À compléter après lecture Tranco (Le Pochat 2019)
- À compléter après lecture RIPE Atlas papers

**Questions ouvertes** :
1. **Comment adapter pour mesures distribuées géographiquement ?**
   → Notre contribution : utiliser RIPE Atlas
2. Quel impact ajout mesures géographiques sur volume données ?
3. Comment optimiser avec crédits RIPE limités vs infrastructure dédiée ?
4. ECS deployment affecte-t-il mesures centralisées ?
5. Comparaison coût OpenINTEL vs approche RIPE Atlas ?

### Citations importantes

> "The DNS has been the focus of, or used in, past measurement studies. These studies, however, had a limited scope, in time, coverage of DNS records or number of domains measured." (p. 1877)

> "Our research goal is to perform daily active measurements of all domains in the main top-level domains (TLDs) on the Internet (including .com, .net and .org, together comprising 50% of the global DNS name space)" (p. 1877)

> "Measuring the DNS is a potent tool for studying the day-to-day evolution of the Internet." (p. 1886)

> "Given the size of our daily dataset and the large amounts of queries we produce, we believe that unbridled duplication of our infrastructure would add an unwanted burden on the DNS system." (p. 1886)

**Sur limitation géographique** :
> "Certain researchers have already envisaged archiving parts of DNS data for research purposes [1]. However, the approach presented in [1] measures DNS information from a single point on the Internet. Yet, the information returned by DNS can vary depending on the location of the client (for example to minimize latency, to provide a local version of the service). It therefore seems interesting to capture the **geographic diversity** of DNS responses over time." (p. 1877)

**Sur impact DNS** :
> "A conservative estimate is that this requires one additional query per domain. Thus, querying every domain in .com requires at least 1.85B queries per day." (p. 1878)

> "Given that the measurement generates some 2 billion queries per day, this would account for between 0.3% and 1.6% of all queries." (p. 1883)

---

## Utilisation dans le mémoire

### Sections concernées

- **Section 2.2** : Mesures actives vs passives
  Citer comme exemple infrastructure mesures actives à grande échelle

- **Section 2.3** : Infrastructure OpenINTEL (section dédiée)
  Description architecture, performance, limitations

- **Section 3** : Question de recherche
  Utiliser limitation reconnue pour justifier notre approche

- **Section 4** : Méthodologie
  Réutiliser patterns architecture (3 stages, workers, storage)
  Comparer/contraster avec notre approche RIPE Atlas

- **Section 7** : Discussion
  Comparer résultats, discuter complémentarité
  Avantages/inconvénients approche centralisée vs distribuée

### Points à développer

**Dans état de l'art** :
- Architecture détaillée OpenINTEL (Figure 1)
- Technologies utilisées (LDNS, Unbound, Avro, Parquet)
- Métriques performance (1.85B queries/jour, 0.3-1.6% trafic)
- Stratégie query pacing (Unbound RTT-based selection)
- Impact minimal sur DNS global (400 pps max)

**Pour notre méthodologie** :
- Inspiration architecture 3 stages adaptée à RIPE Atlas
- Stratégie de mesure (quels types de queries ?)
- Gestion crédits RIPE (équivalent query pacing)
- Stockage données (reprendre Avro + Parquet ?)

**Pour discussion/comparaison** :
- Tableau comparatif OpenINTEL vs notre approche :
  | Critère | OpenINTEL | Notre approche |
  |---------|-----------|----------------|
  | Vantage points | 1 (Pays-Bas) | Multiple (RIPE sondes) |
  | Contrôle infra | Total | Limité (crédits) |
  | Diversité géo | ❌ Non | ✅ Oui |
  | Scalabilité | Très haute | Limitée (crédits) |
  | Coût | Infrastructure dédiée | Crédits RIPE |
  | Couverture TLDs | .com, .net, .org | À définir |

### Références croisées

**Articles à lire ensuite** :
- [ ] Le Pochat (2019) - Tranco (déjà disponible)
- [ ] RIPE Atlas documentation officielle
- [ ] Papers utilisant RIPE Atlas pour DNS
- [ ] Études CDN et géo-localisation DNS
- [ ] RFC 7871 (EDNS Client Subnet - ECS)

**Auteurs à suivre** :
- Roland van Rijswijk-Deij (auteur principal OpenINTEL)
- Mattijs Jonker (co-auteur, DNS measurements)
- Chercher leurs publications récentes (2016-2026)

---

**Tags** : #dns #openintel #active-measurement #infrastructure #architecture #scalability #baseline

**Statut** : [X] Lu / [ ] Relu / [X] Fiché / [ ] Intégré mémoire

**Prochaines étapes** :
1. ✅ Fiche complétée
2. ⏭️ Lire article Tranco (Le Pochat 2019)
3. ⏭️ Chercher citations "Cited by" sur IEEE Xplore
4. ⏭️ Chercher travaux van Rijswijk-Deij 2016-2026
5. ⏭️ Comparer avec autres infrastructures DNS
