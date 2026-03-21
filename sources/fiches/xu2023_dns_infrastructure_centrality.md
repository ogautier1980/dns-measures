# Fiche de lecture - Measuring DNS Infrastructure Centrality

**Référence bibliographique** :
Xu, C., Zhang, Y., Shi, F., Shan, H., Guo, B., Li, Y., & Xue, P. (2023). *Measuring the Centrality of DNS Infrastructure in the Wild*. Applied Sciences, 13(9), 5739. https://doi.org/10.3390/app13095739

**Thème** :
Centralisation infrastructure DNS (client-side + server-side) via mesures actives Internet-wide

**Intérêt pour le mémoire** :
Quantification oligopole DNS infrastructure. Révèle concentration extrême : 90% forwarding resolvers par 5% indirect resolvers, 48.5% domaines par top 10 providers. Implications sécurité (single point of failure) et complémentarité avec notre approche distribuée RIPE Atlas.

---

## Contexte de lecture

**Date de lecture** : 21 mars 2026
**Section du mémoire** :
- Section 2.3 (Infrastructure DNS - centralisation)
- Section 2.6 (État de l'art - concentration providers)

---

## Contenu de l'article

### Objectif(s) / Question(s) de recherche

**Problème** : Centralisation DNS ecosystem = risques :
- **Single point of failure** (Akamai outage 17 juin 2021 → Google, Amazon, Cloudflare inaccessibles)
- **Enterprise failures** (Facebook outage 4 octobre 2021 → BGP mistake + DNS authoritatives down)
- **Privacy** concerns (eavesdropping centralisé)
- **Oligopoly** market → EU lance DNS4EU Infrastructure Project

**Gap littérature** :
- Études précédentes = concentration traffic DNS OU market share OU name servers
- **Manque** : centralisation **infrastructure DNS** elle-même
- Challenge : resolver pools = multiples layers, transparents aux clients

**Questions** :
1. Quel degré centralisation infrastructure client-side (resolver pools) ?
2. Quel degré centralisation infrastructure server-side (authoritative name servers) ?
3. Combien providers dominent infrastructure backing ?

### Méthodologie

- **Type d'étude** : Active measurements Internet-wide + zone file analysis
- **Innovation** : Novel resolver pool discovery method (**NS chain reflecting**)
- **Échelle** :
  - **Client-side** : scan toutes adresses IPv4 routable
  - **Server-side** : analyse 1,138 gTLDs zone files (210,446,494 domain names)
- **Outils** :
  - Active measurement (single probing point)
  - Zone file analysis
  - IP geolocation, AS mapping
- **Période** : 2023 (received 10 avril, accepted 3 mai, published 6 mai)

**Taxonomy DNS (Schomp et al.)** :
- **FDNS** (Forwarding DNS) : reçoit queries, forward vers RDNS
- **RDNS** (Recursive DNS) : execute resolution, contact ADNS
  - **iRDNS** (indirect RDNS) : hidden, backend
  - **dRDNS** (direct RDNS) : visible clients
- **ADNS** (Authoritative DNS) : maintient records domaine

**Resolver pool** : implicit collaborative relationship entre RDNS du même provider

**Méthode CNAME chain** (Schomp 2013) :
- Idée : "RDNS sending request ≠ RDNS resolving CNAME redirection"
- **Limitation** (découverte auteurs) : patterns CNAME varient selon providers
- 20 public DNS testés → 3 patterns :
  1. **Multi-RDNSIP** : Google, Level3 (2/20)
  2. **Single-RDNS** : Cloudflare, OpenDNS, etc. (14/20)
  3. **Multi-Query** : Quad9, Tencent, AliDNS, Yandex, AdGuard, DNSDB (6/20)
- **Conclusion** : CNAME method ineffective modern DNS

**Méthode NS chain reflecting** (proposée) :
- Novel, lightweight, single probing point
- Exploite NS records chains (analogique CNAME mais name servers)
- Fast, low-cost
- Identifie resolver pool structure

### Résultats principaux

#### 1. Client-side centralization (Resolver Pools)

**Chiffre clé** :
- **>90% forwarding resolvers** backed by **<5% (4,071) indirect resolvers**
- Concentration extrême infrastructure client-side

**Implications** :
- Petit nombre iRDNS supporte majorité FDNSs
- Providers utilisent shared infrastructure massive
- Single point of failure pour 90%+ users

#### 2. Server-side centralization (Authoritative Name Servers)

**Chiffres clés** :
- **210,446,494 domain names** analysés (1,138 gTLDs)
- **0.45% (12,679) all name servers** = tous name servers top providers
- **Top 10 DNS providers** servent **48.5%** (>100M) domain names
- **>98% domain names** rely on **single name server provider**

**Shared infrastructure** :
- **60% combinations** name server providers **share infrastructure** (directly or indirectly)
- Enterprises using multiple providers → may implicitly rely on **same infrastructure**

#### 3. Leading DNS Providers

**Top providers** (non exhaustive, article mentionne) :
- Google Public DNS
- Cloudflare
- OpenDNS
- Quad9
- Level3
- Yandex
- Tencent
- AliDNS
- AdGuard DNS
- 114DNS
- (+ autres, total 20 testés)

**Geographic distribution, IP infrastructure, load balancing** explorés mais détails dans sections 5-6 (non lues complètement).

### Conclusion des auteurs

**Contributions** :
1. ✅ **Novel measurement approach** : NS chain reflecting (léger, single probing point)
2. ✅ **Comprehensive analysis** : client-side + server-side centralization
3. ✅ **Quantification centrality** : multiple dimensions (IP, domain, provider, AS)
4. ✅ **Insights inédits** :
   - 90% FDNSes par 5% iRDNSes
   - 98% domains = single provider
   - 60% provider combinations = shared infrastructure

**Implications** :
- DNS infrastructure **much more centralized** than previously believed
- Oligopoly risk confirmed empirically
- Single points of failure systémiques
- Multi-provider strategy ≠ true redundancy (shared infrastructure)

**Limitations** :
- Méthode active = snapshot 2023 (pas évolution temporelle)
- IPv4 uniquement (pas IPv6)
- Zone files = gTLDs (pas ccTLDs complets)

---

## Analyse personnelle

### Que garder pour le mémoire

**Concepts clés** :
- **DNS centralization** = oligopole infrastructure (pas juste market share)
- **Resolver pools** = hidden collaborative infrastructure
- **Shared infrastructure** = redundancy illusoire (multi-provider)
- **Single point of failure** = risque systémique confirmé

**Chiffres essentiels** :
- **90%** FDNSes → 5% iRDNSes
- **48.5%** domaines → Top 10 providers
- **98%** domaines → single provider
- **60%** provider combos → shared infra
- **210M** domaines analysés
- **1,138 gTLDs** zone files

**Limites pertinentes** :
- Active measurement = point-in-time (évolution ?)
- IPv4 only (IPv6 centralisation différente ?)
- gTLDs focus (ccTLDs patterns ?)
- Resolver pool discovery = heuristic (validation ?)

### Critique personnelle

**Forces** :
- ✅ **Novel method** : NS chain reflecting (advance over CNAME)
- ✅ **Comprehensive** : client + server sides
- ✅ **Large scale** : 210M domains, Internet-wide scan
- ✅ **Multi-dimensional** : IP, domain, provider, AS
- ✅ **Timely** : 2023 data (récent)
- ✅ **Alarming findings** : 90%/5% = concentration extrême

**Faiblesses** :
- ⚠️ **No temporal analysis** : snapshot, pas évolution
- ⚠️ **IPv4 bias** : IPv6 potentially different patterns
- ⚠️ **Method validation** : NS chain reflecting = black box (pas open source visible ?)
- ⚠️ **Provider identification** : comment mapper IP → provider ?
- ⚠️ **Geographic analysis light** : mentions geo-distribution mais peu détails
- ⚠️ **No privacy analysis** : implications eavesdropping non quantifiées

**Lien avec autres articles** :

- **OpenINTEL (van Rijswijk-Deij 2016)** :
  - OpenINTEL = centralisé (1 point mesure)
  - Xu : DNS **backend** aussi centralisé (oligopole providers)
  - Ironie : infrastructure "distribuée" DNS = highly centralized

- **RIPE Atlas (Nosyk 2024)** :
  - RIPE = 12.9K sondes distribuées (géo-diversity)
  - Xu : DNS providers = concentrés malgré distribution apparente
  - Notre mémoire : RIPE Atlas = antidote centralisation (vantage points distribués)

- **Boswell 2024, Johnson 2016** :
  - Boswell : internal names, client-side
  - Johnson : root manipulation
  - Xu : infrastructure centralization (systemic)
  - Complémentarité : threats multiples niveaux

**Questions ouvertes** :
1. **Évolution** : Centralisation augmente ou stable ?
2. **IPv6** : Patterns différents IPv4 vs IPv6 ?
3. **CDN impact** : CDNs contribuent centralisation ?
4. **Geographic diversity** : Providers concentrés géographiquement aussi ?
5. **Resilience** : Comment mesurer vraie redundancy ?
6. **Regulatory** : EU DNS4EU efficace contre oligopole ?

### Citations importantes

> "The centralization of the global DNS ecosystem may accelerate the creation of an oligopoly market, thereby, increasing the risk of a single point of failure and network traffic manipulation." (Abstract)

> "Our measurement results show that the DNS infrastructure is much more centralized than previously believed. Over 90% of forwarding resolvers are backed by less than 5% (4071) of indirect resolvers." (Abstract)

> "Merely 0.45% (12,679) of all name servers across 1138 gTLDs, operated by just 10 DNS providers, provide authoritative domain resolution service for 48.5% (more than 100 million) of domain names." (Abstract)

> "We found that 60% combinations of name server providers share their infrastructure directly or indirectly, which suggests that enterprises may implicitly rely on the same infrastructure even if they outsource their DNS service to multiple DNS providers." (Introduction)

**Sur outages réels** :
> "On 17 June 2021, the Akamai DNS outage left numerous top websites and online services inaccessible, including Google, Amazon, Steam, Cloudflare, and FedEx." (Introduction)

> "Facebook experienced the most influential outage in the entire history of the Internet on 4 October 2021, which was caused by a mistake in BGP updating that resulted in the authoritative DNS service outage." (Introduction)

---

## Utilisation dans le mémoire

**Sections concernées** :
- **Section 2.3 (Infrastructure)** : Centralisation vs distribution DNS
- **Section 2.6 (État de l'art)** : Oligopole providers, concentration infrastructure
- **Section 7 (Discussion)** : Notre approche = antidote centralisation

**Points à développer** :

**État de l'art** :
- DNS infrastructure = paradoxe : designed distributed, actually centralized
- 90% FDNSes / 5% iRDNSes = concentration backend
- Multi-provider strategy = false security (shared infrastructure)
- Outages réels (Akamai, Facebook) = proof centralization risk

**Notre contribution** :
- RIPE Atlas (12.9K sondes, 178 pays) = distributed measurements
- Antidote centralisation : vantage points géographiquement distribués
- Diversité géographique DNS responses = invisible à infrastructure centralisée
- Complémentarité :
  - Xu : centralisation backend infrastructure
  - Nous : diversité frontend responses (client perspective)

**Discussion** :
- Xu montre **why** distributed measurements matter (centralization risk)
- Notre approche : observer variations **malgré** backend centralisé
- Geographic diversity queries → révèle comportements invisibles à single vantage point
- Trade-off : OpenINTEL (centralized but comprehensive) vs RIPE (distributed but sampled)

**Références croisées** :
- OpenINTEL : Centralized measurement platform
- RIPE Atlas : Distributed measurement (counter-centralization)
- Nosyk 2024 : RIPE Atlas capabilities
- Boswell 2024 : Client-side diversity

---

**Tags** : #dns-infrastructure #centralization #oligopoly #resolver-pools #name-servers #security #single-point-failure #measurement #active-measurement #zone-files

**Statut** : [X] Lu (PDF via MD - partial) / [X] Fiché / [ ] Intégré mémoire

**Date fiche** : 21 mars 2026

**Note** : Fiche basée sur Abstract + Introduction + Methodology + Results summary. Sections 5-6 (detailed analysis) à lire pour chiffres complets IP/AS/geo-distribution si nécessaire ultérieurement.
