# Analyse des articles PDF - État de l'art DNS

**Date d'analyse** : 21 mars 2026
**Objectif** : Identifier les articles pertinents pour l'état de l'art du mémoire "Mesures DNS dans l'espace et le temps"

---

## Articles analysés et classement par pertinence

### ⭐⭐⭐ TRÈS PERTINENTS (à ficher en priorité)

#### 1. **A High-Performance, Scalable Infrastructure for Large-Scale Active DNS Measurements**
- **Auteurs** : van Rijswijk-Deij, R., Jonker, M., Sperotto, A., Pras, A.
- **Publication** : IEEE JSAC, Vol. 34, No. 6, June 2016
- **Fichier actuel** : `A High-Performance, Scalable Infrastructure for Large-Scale Active DNS Measurements.pdf`
- **Nouveau nom** : `vanRijswijk2016_openintel_infrastructure.pdf`
- **Pertinence** : ⭐⭐⭐ ESSENTIEL
- **Section(s)** : 2.3 (Infrastructure OpenINTEL)
- **Raison** : Article fondateur OpenINTEL - architecture mesures DNS actives à grande échelle
- **Statut fiche** : ✅ DÉJÀ FICHÉE (`sources/fiches/vanRijswijk2016_openintel.md`)

#### 2. **TRANCO: A Research-Oriented Top Sites Ranking Hardened Against Manipulation**
- **Auteurs** : Le Pochat, V., Van Goethem, T., et al.
- **Publication** : NDSS 2019
- **Fichier actuel** : `TRANCO A Research-Oriented Top Sites Ranking Hardened Against Manipulation.pdf`
- **Nouveau nom** : `lePochat2019_tranco_ranking.pdf`
- **Pertinence** : ⭐⭐⭐ ESSENTIEL
- **Section(s)** : 2.4 (Liste Tranco)
- **Raison** : Article fondateur Tranco - méthodologie ranking sites web
- **Statut fiche** : ✅ DÉJÀ FICHÉE (`sources/fiches/lePochat2019_tranco.md`)

#### 3. **Quantifying Interference between Measurements on the RIPE Atlas Platform**
- **Auteurs** : Holterbach, T., et al.
- **Publication** : IMC 2015 (October 28-30, 2015, Tokyo, Japan)
- **Fichier actuel** : `Holterbach2015.pdf`
- **Nouveau nom** : `holterbach2015_ripeatlas_interference.pdf`
- **Pertinence** : ⭐⭐⭐ TRÈS PERTINENT
- **Section(s)** : 2.5 (RIPE Atlas), 2.2 (Méthodologie mesures)
- **Raison** : Impact interférence mesures RIPE Atlas - crucial pour fiabilité
- **Statut fiche** : ✅ DÉJÀ FICHÉE (`sources/fiches/holterbach2015_atlas_interference.md`)

#### 4. **Melting the Snow: Using Active DNS Measurements to Detect Snowshoe Spam Domains**
- **Auteurs** : van der Toorn, O., van Rijswijk-Deij, R., Geesink, B., Sperotto, A.
- **Publication** : NOMS 2018
- **Fichier actuel** : `noms2018.pdf`
- **Nouveau nom** : `vanderToorn2018_snowshoe_spam_dns.pdf`
- **Pertinence** : ⭐⭐ PERTINENT (cas d'usage)
- **Section(s)** : 2.2 (Mesures actives), 2.6 (Sécurité DNS)
- **Raison** : Utilisation mesures DNS actives (>60% namespace) + ML pour détection spam
- **Insights** : Active DNS + ML, détection 100 jours avant blacklists, déployé en production
- **Statut fiche** : ❌ À CRÉER

#### 5. **RIPEn at Home – Surveying Internal Domain Names using RIPE Atlas**
- **Auteurs** : Boswell, E., Perkins, C.
- **Publication** : TMA 2024 (Network Traffic Measurement and Analysis Conference)
- **Fichier actuel** : `tma2024poster-final1.pdf`
- **Nouveau nom** : `boswell2024_internal_names_ripeatlas.pdf`
- **Pertinence** : ⭐⭐ PERTINENT (méthodologie)
- **Section(s)** : 2.5 (RIPE Atlas), 2.6 (Sécurité - name collisions)
- **Raison** : Méthodologie mesures RIPE Atlas pour noms internes, name collisions
- **Insights** : 3092 noms internes via 4305 sondes, 34.51% risque collision
- **Statut fiche** : ❌ À CRÉER

---

### ⭐⭐ PERTINENTS (contexte et travaux connexes)

#### 6. **Detecting DNS Root Manipulation**
- **Auteurs** : [À extraire - visible partiellement]
- **Publication** : ICIR
- **Fichier actuel** : `Detecting DNS Root Manipulation.pdf`
- **Nouveau nom** : `johnson2016_dns_root_manipulation.pdf` (année à vérifier)
- **Pertinence** : ⭐⭐ PERTINENT
- **Section(s)** : 2.5 (RIPE Atlas use case), 2.6 (Sécurité DNS)
- **Raison** : Détection serveurs root non autorisés via RIPE Atlas
- **Insights** : Techniques détection manipulation DNS, contrôle namespace
- **Statut fiche** : ❌ À CRÉER

#### 7. **Analyzing the Performance of an Anycast CDN**
- **Auteurs** : Calder, M., Flavel, A., Katz-Bassett, E., Mahajan, R., et al.
- **Publication** : IMC 2015 (October 28-30, 2015, Tokyo, Japan)
- **Citations** : 115 | Téléchargements : 1013
- **Fichier actuel** : `2815675.2815717.pdf`
- **Nouveau nom** : `calder2015_anycast_cdn_performance.pdf`
- **Pertinence** : ⭐⭐ PERTINENT
- **Section(s)** : 2.6 (CDN, anycast, diversité géographique)
- **Raison** : Performance anycast CDN - pertinent pour comprendre diversité géographique DNS
- **Statut fiche** : ❌ À CRÉER

#### 8. **Anycast in Context: A Tale of Two Systems**
- **Auteurs** : Koch, T., Katz-Bassett, E., Heidemann, J., et al.
- **Publication** : SIGCOMM 2021 (August 23-27, 2021, Virtual Event)
- **Citations** : 34 | Téléchargements : 1695
- **Fichier actuel** : `3452296.3472891.pdf`
- **Nouveau nom** : `koch2021_anycast_context.pdf`
- **Pertinence** : ⭐⭐ PERTINENT
- **Section(s)** : 2.6 (Anycast DNS)
- **Raison** : Analyse anycast systems - pertinent pour comprendre routing DNS géographique
- **Statut fiche** : ❌ À CRÉER

#### 9. **A Study of the Impact of DNS Resolvers on CDN Performance using a Causal Approach**
- **Auteurs** : Hours, H., Biersack, E., Loiseau, P., Finamore, A., Mellia, M.
- **Publication** : Computer Networks 109 (2016) 200–210
- **Fichier actuel** : `1-s2.0-S1389128616302006-main.pdf`
- **Nouveau nom** : `hours2016_dns_resolvers_cdn_impact.pdf`
- **Pertinence** : ⭐⭐ PERTINENT
- **Section(s)** : 2.6 (CDN, impact resolvers DNS)
- **Raison** : Impact DNS resolvers sur performance CDN - lien avec diversité géo
- **Insights** : DNS joue rôle important dans CDN pour géolocalisation clients
- **Statut fiche** : ❌ À CRÉER

#### 10. **Evolution and Challenges of DNS-based CDNs**
- **Auteurs** : Wang, Z., Huang, J., Rose, S.
- **Publication** : Digital Communications and Networks 4 (2018) 235–243
- **Fichier actuel** : `1-s2.0-S2352864817300731-main.pdf`
- **Nouveau nom** : `wang2018_dns_cdn_challenges.pdf`
- **Pertinence** : ⭐⭐ PERTINENT
- **Section(s)** : 2.6 (CDN, remote DNS)
- **Raison** : Évolution DNS-based CDNs, problème remote DNS, privacy
- **Insights** : Remote DNS dégrade performance, solutions ECS
- **Statut fiche** : ❌ À CRÉER

#### 11. **Measuring the Centrality of DNS Infrastructure in the Wild**
- **Auteurs** : Xu, C., Zhang, Y., Shi, F., Shan, H., Guo, B., Li, Y., Xue, P.
- **Publication** : Applied Sciences 2023, 13, 5739
- **Fichier actuel** : `applsci-13-05739.pdf`
- **Nouveau nom** : `xu2023_dns_infrastructure_centrality.pdf`
- **Pertinence** : ⭐⭐ PERTINENT
- **Section(s)** : 2.6 (Centralisation DNS), 2.3 (Infrastructure)
- **Raison** : Centralisation infrastructure DNS - 90% forwarding resolvers par 5% indirect resolvers
- **Insights** : Mesure active client-side + server-side, centralisation oligopole
- **Statut fiche** : ❌ À CRÉER

#### 12. **Measurement and Analysis of a Global-Scale CDN -- Locality, Dynamics, and Load Balance**
- **Auteurs** : Li, G.-C., Huang, P.
- **Publication** : AINTEC 2025 (November 25-27, 2025, Manila, Philippines)
- **Citations** : 0 (très récent) | Téléchargements : 118
- **Fichier actuel** : `3763400.3763406.pdf`
- **Nouveau nom** : `li2025_global_cdn_analysis.pdf`
- **Pertinence** : ⭐ MOYENNEMENT PERTINENT (très récent, peu cité)
- **Section(s)** : 2.6 (CDN global)
- **Raison** : Analyse CDN global - locality, dynamics, load balance
- **Statut fiche** : ⏸️ À ÉVALUER (lire résumé complet avant)

---

### ⭐ CONTEXTE (références techniques)

#### 13. **RFC 7871 - Client Subnet in DNS Queries**
- **Publication** : IETF RFC
- **Fichier actuel** : `rfc7871.txt.pdf`
- **Nouveau nom** : `rfc7871_edns_client_subnet.pdf`
- **Pertinence** : ⭐⭐ RÉFÉRENCE TECHNIQUE
- **Section(s)** : 2.1 (Rappels DNS), 2.6 (ECS)
- **Raison** : RFC officiel EDNS Client Subnet - comprendre ECS impact
- **Statut fiche** : ❌ Résumé technique à créer

#### 14. **Benefits and Limitations of RIPE Atlas Tags**
- **Auteurs** : Bajpai, V., Schönwälder, J.
- **Publication** : IM 2017
- **Fichier actuel** : `ripeatlas-im-2017.pdf`
- **Nouveau nom** : `bajpai2017_ripeatlas_tags.pdf`
- **Pertinence** : ⭐ MÉTHODOLOGIE
- **Section(s)** : 2.5 (RIPE Atlas)
- **Raison** : Organisation et tags mesures RIPE Atlas - bonnes pratiques
- **Statut fiche** : ❌ Résumé méthodologique à créer

#### 15. **DNS Measurements with RIPE Atlas** (Tutorial)
- **Auteur** : Bortzmeyer, S. (RIPE presentation)
- **Publication** : RIPE presentation
- **Fichier actuel** : `DNS-Measurements-with-RIPE-Atlas.pdf`
- **Nouveau nom** : `bortzmeyer_dns_measurements_atlas_tutorial.pdf`
- **Pertinence** : ⭐⭐⭐ TUTORIAL PRATIQUE
- **Section(s)** : 2.5 (RIPE Atlas)
- **Raison** : Tutorial pratique mesures DNS avec RIPE Atlas
- **Statut fiche** : ✅ DÉJÀ FICHÉE (`sources/fiches/bortzmeyer_dns_measurements_atlas.md`)

#### 16. **Characterizing Large-Scale Routing Anomalies** (?)
- **Auteurs** : Cicalese, D., Joumblatt, D., Augé, J., Friedman, T.
- **Publication** : CoNEXT 2015 (December 1-4, 2015, Heidelberg, Germany)
- **Citations** : 29 | Téléchargements : 333
- **Fichier actuel** : `2716281.2836101.pdf`
- **Nouveau nom** : `cicalese2015_routing_anomalies.pdf` (titre à vérifier)
- **Pertinence** : ⏸️ À ÉVALUER
- **Section(s)** : Potentiellement 2.6 (si lié DNS/routing)
- **Raison** : Routing anomalies - pertinence DNS à vérifier
- **Statut fiche** : ❌ Lire abstract complet d'abord

---

## Résumé statistique

| Catégorie | Nombre | Fichés | À ficher |
|-----------|--------|--------|----------|
| ⭐⭐⭐ Très pertinents | 5 | 3 | 2 |
| ⭐⭐ Pertinents | 7 | 0 | 7 |
| ⭐ Contexte/Référence | 3 | 1 | 2 |
| ⏸️ À évaluer | 2 | 0 | - |
| **TOTAL** | **16** | **4** | **11** |

---

## Plan d'action recommandé

### Phase 1 : Fiches prioritaires (cette semaine)
1. ✅ `vanRijswijk2016_openintel_infrastructure.pdf` - FAIT
2. ✅ `lePochat2019_tranco_ranking.pdf` - FAIT
3. ✅ `holterbach2015_ripeatlas_interference.pdf` - FAIT
4. ❌ `vanderToorn2018_snowshoe_spam_dns.pdf` - À FAIRE
5. ❌ `boswell2024_internal_names_ripeatlas.pdf` - À FAIRE

### Phase 2 : Travaux connexes CDN/Anycast
6. ❌ `calder2015_anycast_cdn_performance.pdf`
7. ❌ `koch2021_anycast_context.pdf`
8. ❌ `hours2016_dns_resolvers_cdn_impact.pdf`
9. ❌ `wang2018_dns_cdn_challenges.pdf`

### Phase 3 : Infrastructure et centralisation
10. ❌ `xu2023_dns_infrastructure_centrality.pdf`
11. ⏸️ `li2025_global_cdn_analysis.pdf` (évaluer d'abord)

### Phase 4 : Sécurité et détection
12. ❌ `johnson2016_dns_root_manipulation.pdf` (vérifier auteur/année)

### Phase 5 : Références techniques
13. ❌ `rfc7871_edns_client_subnet.pdf` - Résumé technique
14. ❌ `bajpai2017_ripeatlas_tags.pdf` - Méthodologie

### Phase 6 : À évaluer
15. ⏸️ `cicalese2015_routing_anomalies.pdf` - Lire abstract complet
16. ✅ `bortzmeyer_dns_measurements_atlas_tutorial.pdf` - FAIT

---

## Mapping vers structure état de l'art (Chapitre 2)

| Section | Articles identifiés | Statut |
|---------|---------------------|--------|
| **2.1 - Système DNS (rappels)** | RFC 7871 | ⭐ Référence |
| **2.2 - Mesures actives vs passives** | vanRijswijk2016, vanderToorn2018 | 1 fiché, 1 à faire |
| **2.3 - Infrastructure OpenINTEL** | vanRijswijk2016, xu2023 | 1 fiché, 1 à faire |
| **2.4 - Liste Tranco** | lePochat2019 | ✅ Fiché |
| **2.5 - RIPE Atlas** | holterbach2015, bortzmeyer, bajpai2017, boswell2024 | 2 fichés, 2 à faire |
| **2.6 - CDN/géo** | calder2015, koch2021, hours2016, wang2018, li2025 | 0 fiché, 5 à faire |
| **2.6 - Sécurité** | vanderToorn2018, johnson2016, boswell2024 | 0 fiché, 3 à faire |
| **2.6 - Centralisation** | xu2023 | 0 fiché, 1 à faire |

---

## Notes sur le renommage

**Convention de nommage adoptée** :
```
[auteur principal][année]_[mot-clé descriptif].pdf
```

**Exemples** :
- `vanRijswijk2016_openintel_infrastructure.pdf`
- `lePochat2019_tranco_ranking.pdf`
- `holterbach2015_ripeatlas_interference.pdf`

**Avantages** :
- ✅ Tri alphabétique par auteur
- ✅ Année visible immédiatement
- ✅ Sujet identifiable
- ✅ Cohérent avec fiches existantes

---

**Dernière mise à jour** : 21 mars 2026, 14:56 UTC
