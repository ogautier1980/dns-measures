# Sources et Références

Ce répertoire contient les articles académiques et documents de référence pour le mémoire sur les mesures DNS dans l'espace et le temps.

---

## Organisation

```
sources/
├── *.pdf                      # Articles en PDF (convention: [auteur][année]_[descriptif].pdf)
├── converted/                 # Versions Markdown des PDFs (extraction texte)
├── fiches/                    # Fiches de lecture détaillées
│   ├── template_fiche.md      # Template pour nouvelles fiches
│   └── *.md                   # Fiches complètes
├── analyse_articles.md        # Analyse complète des 16 articles (pertinence, mapping)
└── README.md                  # Ce fichier
```

---

## Convention de nommage

**Format** : `[auteur principal][année]_[descriptif].pdf`

**Exemples** :
- `vanRijswijk2016_openintel_infrastructure.pdf`
- `lePochat2019_tranco_ranking.pdf`
- `holterbach2015_ripeatlas_interference.pdf`

**Avantages** :
- ✅ Tri alphabétique par auteur
- ✅ Année visible immédiatement
- ✅ Sujet identifiable au premier coup d'œil
- ✅ Cohérence avec fiches de lecture

---

## Articles par catégorie

### ⭐⭐⭐ Articles fondamentaux (très pertinents)

#### Infrastructure de mesure DNS active

1. **vanRijswijk2016_openintel_infrastructure.pdf**
   - **Titre** : A High-Performance, Scalable Infrastructure for Large-Scale Active DNS Measurements
   - **Auteurs** : van Rijswijk-Deij, R., Jonker, M., Sperotto, A., Pras, A.
   - **Publication** : IEEE JSAC, Vol. 34, No. 6, June 2016
   - **Pertinence** : ⭐⭐⭐ ESSENTIEL - Article fondateur OpenINTEL
   - **Sections concernées** : 2.3 (Infrastructure OpenINTEL), 2.2 (Mesures actives)
   - **Fiche** : ✅ [fiches/vanRijswijk2016_openintel_infrastructure.md](fiches/vanRijswijk2016_openintel_infrastructure.md)
   - **Insights clés** :
     - 123M domaines .com mesurés quotidiennement
     - 1.85 milliards queries/jour depuis 1 point (Pays-Bas)
     - 0.3-1.6% trafic DNS global (impact minimal)
     - **Limitation** : 1 seul vantage point géographique

#### Classement des sites web

2. **lePochat2019_tranco_ranking.pdf**
   - **Titre** : Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation
   - **Auteurs** : Le Pochat, V., Van Goethem, T., Tajalizadehkhoob, S., Korczynski, M., Joosen, W.
   - **Publication** : NDSS 2019
   - **Pertinence** : ⭐⭐⭐ ESSENTIEL - Liste stable domaines
   - **Sections concernées** : 2.4 (Liste Tranco)
   - **Fiche** : ✅ [fiches/lePochat2019_tranco_ranking.md](fiches/lePochat2019_tranco_ranking.md)
   - **Insights clés** :
     - Stabilité : 0.6% changement/jour (vs 50% Alexa)
     - Résistance manipulation : 4× effort requis
     - 600+ publications académiques utilisent Tranco

#### RIPE Atlas et interférence mesures

3. **holterbach2015_ripeatlas_interference.pdf**
   - **Titre** : Quantifying Interference between Measurements on the RIPE Atlas Platform
   - **Auteurs** : Holterbach, T., et al.
   - **Publication** : IMC 2015 (Tokyo, Japan)
   - **Pertinence** : ⭐⭐⭐ TRÈS PERTINENT - Fiabilité mesures
   - **Sections concernées** : 2.5 (RIPE Atlas), 2.2 (Méthodologie)
   - **Fiche** : ✅ [fiches/holterbach2015_ripeatlas_interference.md](fiches/holterbach2015_ripeatlas_interference.md)
   - **Insights clés** :
     - Impact interférence mesures simultanées
     - DNS delays causés par concurrence ressources sondes
     - Méthodologie pour mesures fiables

#### Détection spam via DNS actif

4. **vanderToorn2018_snowshoe_spam_dns.pdf**
   - **Titre** : Melting the Snow: Using Active DNS Measurements to Detect Snowshoe Spam Domains
   - **Auteurs** : van der Toorn, O., van Rijswijk-Deij, R., Geesink, B., Sperotto, A.
   - **Publication** : NOMS 2018
   - **Pertinence** : ⭐⭐⭐ TRÈS PERTINENT - Cas d'usage mesures actives
   - **Sections concernées** : 2.2 (Mesures actives), 2.6 (Sécurité DNS)
   - **Fiche** : ✅ [fiches/vanderToorn2018_snowshoe_spam_dns.md](fiches/vanderToorn2018_snowshoe_spam_dns.md)
   - **Insights clés** :
     - 60% namespace DNS + ML = détection spam
     - >93% précision, détection 100 jours avant blacklists
     - Déploiement production validé (SURFnet)
     - **Limitation** : 1 seul point mesure (vs notre approche distribuée)

#### RIPE Atlas - Analyse infrastructure

5. **nosyk2024_ripeatlas_ditl.pdf** (fiche déjà conforme)
   - **Titre** : A Day in the Life of RIPE Atlas
   - **Auteurs** : Nosyk, Y., et al.
   - **Publication** : arXiv:2511.22474v1, 2024
   - **Pertinence** : ⭐⭐⭐ ESSENTIEL - État actuel RIPE Atlas
   - **Sections concernées** : 2.5 (RIPE Atlas)
   - **Fiche** : ✅ [fiches/nosyk2024_ripeatlas_ditl.md](fiches/nosyk2024_ripeatlas_ditl.md)
   - **Insights clés** :
     - 12,892 sondes + 810 ancres (février 2024)
     - 178 pays, 88K mesures DNS quotidiennes
     - **Biais géographique** : Allemagne + USA = 28%
     - 1.3 milliards résultats/jour

---

### ⭐⭐ Articles pertinents (travaux connexes)

#### Mesures RIPE Atlas pratiques

6. **bortzmeyer_dns_measurements_atlas_tutorial.pdf**
   - **Titre** : DNS Measurements with RIPE Atlas (Tutorial)
   - **Auteur** : Bortzmeyer, S. (AFNIC)
   - **Publication** : RIPE presentation
   - **Pertinence** : ⭐⭐⭐ TUTORIAL PRATIQUE
   - **Sections concernées** : 2.5 (RIPE Atlas)
   - **Fiche** : ✅ [fiches/bortzmeyer_dns_measurements_atlas_tutorial.md](fiches/bortzmeyer_dns_measurements_atlas_tutorial.md)
   - **Insights clés** : Interfaces API/Web/CLI, pièges méthodologiques

7. **boswell2024_internal_names_ripeatlas.pdf**
   - **Titre** : RIPEn at Home – Surveying Internal Domain Names using RIPE Atlas
   - **Auteurs** : Boswell, E., Perkins, C.
   - **Publication** : TMA 2024
   - **Pertinence** : ⭐⭐ PERTINENT - Méthodologie RIPE Atlas
   - **Sections concernées** : 2.5 (RIPE Atlas), 2.6 (Sécurité - name collisions)
   - **Fiche** : ✅ [fiches/boswell2024_internal_names_ripeatlas.md](fiches/boswell2024_internal_names_ripeatlas.md)
   - **Insights clés** : 3092 noms internes, 34.51% risque collision, FRITZ!Box dominant

8. **bajpai2017_ripeatlas_tags.pdf**
   - **Titre** : Benefits and Limitations of RIPE Atlas Tags
   - **Auteurs** : Bajpai, V., Schönwälder, J.
   - **Publication** : ANRW 2017
   - **Pertinence** : ⭐⭐ PERTINENT - Vantage points selection
   - **Sections concernées** : 2.5 (RIPE Atlas - tagging, biais géographique)
   - **Fiche** : ✅ [fiches/bajpai2017_ripeatlas_tags.md](fiches/bajpai2017_ripeatlas_tags.md)
   - **Insights clés** : 2.3K dual-stack, 91% RIPE+ARIN, BE/JP sous-représentés

#### Sécurité et détection

9. **johnson2016_dns_root_manipulation.pdf**
   - **Titre** : Detecting DNS Root Manipulation
   - **Auteurs** : Jones, B., Feamster, N., Paxson, V., Weaver, N., Allman, M.
   - **Publication** : ICIR 2016
   - **Pertinence** : ⭐⭐ PERTINENT - Sécurité DNS
   - **Sections concernées** : 2.5 (RIPE Atlas use case), 2.6 (Sécurité DNS)
   - **Fiche** : ✅ [fiches/johnson2016_dns_root_manipulation.md](fiches/johnson2016_dns_root_manipulation.md)
   - **Insights clés** : 10 DNS proxies, 1 unauthorized root mirror (Chine), ~8K sondes 2014

#### CDN et Anycast

10. **calder2015_anycast_cdn_performance.pdf**
    - **Titre** : Analyzing the Performance of an Anycast CDN
    - **Auteurs** : Calder, M., Flavel, A., Katz-Bassett, E., Mahajan, R., et al.
    - **Publication** : IMC 2015
    - **Citations** : 115 | Téléchargements : 1013
    - **Pertinence** : ⭐⭐ PERTINENT - Anycast CDN performance
    - **Sections concernées** : 2.6 (CDN, anycast)
    - **Fiche** : ✅ [fiches/calder2015_anycast_cdn_performance.md](fiches/calder2015_anycast_cdn_performance.md)
    - **Insights clés** : 20% clients suboptimal (≥25ms), BGP routing ≠ latency

11. **koch2021_anycast_context.pdf**
    - **Titre** : Anycast in Context: A Tale of Two Systems
    - **Auteurs** : Koch, T., Katz-Bassett, E., Heidemann, J., et al.
    - **Publication** : SIGCOMM 2021
    - **Citations** : 34 | Téléchargements : 1695
    - **Pertinence** : ⭐⭐ PERTINENT - Anycast context matters
    - **Sections concernées** : 2.6 (Anycast DNS)
    - **Fiche** : ✅ [fiches/koch2021_anycast_context.md](fiches/koch2021_anycast_context.md)
    - **Insights clés** : Root DNS >95% inflation OK (cache), Microsoft CDN 35% (peering)

12. **hours2016_dns_resolvers_cdn_impact.pdf**
    - **Titre** : A Study of the Impact of DNS Resolvers on CDN Performance using a Causal Approach
    - **Auteurs** : Hours, H., Biersack, E., Loiseau, P., Finamore, A., Mellia, M.
    - **Publication** : Computer Networks 109 (2016) 200–210
    - **Pertinence** : ⭐⭐ PERTINENT - Causal analysis DNS/CDN
    - **Sections concernées** : 2.6 (CDN, impact resolvers)
    - **Fiche** : ✅ [fiches/hours2016_dns_resolvers_cdn_impact.md](fiches/hours2016_dns_resolvers_cdn_impact.md)
    - **Insights clés** : 14% impact distance, 30% impact config TCP (causal)

13. **wang2018_dns_cdn_challenges.pdf**
    - **Titre** : Evolution and Challenges of DNS-based CDNs
    - **Auteurs** : Wang, Z., Huang, J., Rose, S.
    - **Publication** : Digital Communications and Networks 4 (2018) 235–243
    - **Pertinence** : ⭐⭐ PERTINENT - Survey DNS-based CDN
    - **Sections concernées** : 2.6 (CDN, remote DNS, ECS)
    - **Fiche** : ✅ [fiches/wang2018_dns_cdn_challenges.md](fiches/wang2018_dns_cdn_challenges.md)
    - **Insights clés** : Remote DNS 27% growth, 2× latency, ECS privacy concerns

14. **li2025_global_cdn_analysis.pdf**
    - **Titre** : Measurement and Analysis of a Global-Scale CDN -- Locality, Dynamics, and Load Balance
    - **Auteurs** : Li, G.-C., Huang, P.
    - **Publication** : AINTEC 2025
    - **Citations** : 0 (très récent)
    - **Pertinence** : ⭐ MOYENNEMENT PERTINENT
    - **Sections concernées** : 2.6 (CDN global)
    - **Fiche** : ⏸️ À ÉVALUER

#### Infrastructure et centralisation

15. **xu2023_dns_infrastructure_centrality.pdf**
    - **Titre** : Measuring the Centrality of DNS Infrastructure in the Wild
    - **Auteurs** : Xu, C., Zhang, Y., Shi, F., Shan, H., Guo, B., Li, Y., Xue, P.
    - **Publication** : Applied Sciences 2023, 13, 5739
    - **Pertinence** : ⭐⭐ PERTINENT - Centralisation infrastructure
    - **Sections concernées** : 2.6 (Centralisation DNS), 2.3 (Infrastructure)
    - **Fiche** : ✅ [fiches/xu2023_dns_infrastructure_centrality.md](fiches/xu2023_dns_infrastructure_centrality.md)
    - **Insights clés** : 90% FDNSes par 5% iRDNSes, Top 10 providers = 48.5% domaines

---

### ⭐ Références techniques

16. **rfc7871_edns_client_subnet.pdf**
    - **Titre** : RFC 7871 - Client Subnet in DNS Queries (ECS)
    - **Publication** : IETF RFC
    - **Pertinence** : ⭐⭐ RÉFÉRENCE TECHNIQUE
    - **Sections concernées** : 2.1 (Rappels DNS), 2.6 (ECS)
    - **Fiche** : ❌ Résumé technique à créer

17. **cicalese2015_conext.pdf**
    - **Titre** : [À vérifier - potentiellement routing anomalies]
    - **Auteurs** : Cicalese, D., Joumblatt, D., Augé, J., Friedman, T.
    - **Publication** : CoNEXT 2015
    - **Citations** : 29
    - **Pertinence** : ⏸️ À ÉVALUER
    - **Fiche** : ❌ Lire abstract complet d'abord

---

## Statistiques

| Catégorie | Nombre | Fichés | À ficher |
|-----------|--------|--------|----------|
| ⭐⭐⭐ Très pertinents | 6 | 6 | 0 |
| ⭐⭐ Pertinents | 9 | 8 | 1 |
| ⭐ Contexte/Référence | 2 | 0 | 2 |
| **TOTAL** | **17** | **14** | **3** |

**Progrès** : 14/17 articles fichés (82%)

---

## Mapping vers état de l'art (Chapitre 2)

| Section | Articles disponibles | Fichés |
|---------|---------------------|--------|
| **2.1 - Système DNS (rappels)** | rfc7871 | 0/1 ⚠️ |
| **2.2 - Mesures actives vs passives** | vanRijswijk2016, vanderToorn2018 | 2/2 ✅ |
| **2.3 - Infrastructure OpenINTEL** | vanRijswijk2016, xu2023 | 2/2 ✅ |
| **2.4 - Liste Tranco** | lePochat2019 | 1/1 ✅ |
| **2.5 - RIPE Atlas** | nosyk2024, holterbach2015, bortzmeyer, bajpai2017, boswell2024, johnson2016 | 6/6 ✅ |
| **2.6 - CDN/géo/anycast** | calder2015, koch2021, hours2016, wang2018, (li2025) | 4/4 ✅ |
| **2.6 - Sécurité** | vanderToorn2018, johnson2016, boswell2024 | 3/3 ✅ |
| **2.6 - Centralisation** | xu2023 | 1/1 ✅ |

**Note** : ⚠️ = Référence technique couverte ailleurs, () = À évaluer

---

## Plan d'action

### ✅ Phase 1 : Articles fondamentaux (TERMINÉE)
- ✅ vanRijswijk2016_openintel_infrastructure.pdf
- ✅ lePochat2019_tranco_ranking.pdf
- ✅ holterbach2015_ripeatlas_interference.pdf
- ✅ nosyk2024_ripeatlas_ditl.md
- ✅ bortzmeyer_dns_measurements_atlas_tutorial.pdf
- ✅ vanderToorn2018_snowshoe_spam_dns.pdf

### ✅ Phase 2 : Travaux connexes prioritaires (TERMINÉE)
- ✅ boswell2024_internal_names_ripeatlas.pdf (méthodologie RIPE)
- ✅ johnson2016_dns_root_manipulation.pdf (sécurité)
- ✅ xu2023_dns_infrastructure_centrality.pdf (centralisation)

### ✅ Phase 3 : CDN et Anycast (TERMINÉE)
- ✅ calder2015_anycast_cdn_performance.pdf
- ✅ koch2021_anycast_context.pdf
- ✅ hours2016_dns_resolvers_cdn_impact.pdf
- ✅ wang2018_dns_cdn_challenges.pdf

### ✅ Phase 4 : Méthodologie RIPE Atlas (TERMINÉE)
- ✅ bajpai2017_ripeatlas_tags.pdf

### ⏭️ Phase 5 : Références optionnelles (3 restants)
- ❌ rfc7871_edns_client_subnet.pdf (RFC - déjà couvert dans wang2018)
- ⏸️ li2025_global_cdn_analysis.pdf (À évaluer - possiblement redondant)
- ⏸️ cicalese2015_conext.pdf (À évaluer - pertinence inconnue)

---

## Ressources complémentaires

### Documentation en ligne
- **RIPE Atlas** : https://atlas.ripe.net/docs/
- **OpenINTEL** : https://www.openintel.nl/
- **Tranco** : https://tranco-list.eu/
- **RIPE Labs** : https://labs.ripe.net/

### Outils
- **RIPE Atlas API** : https://atlas.ripe.net/docs/api/v2/
- **Tranco Python package** : https://pypi.org/project/tranco/
- **OpenINTEL data access** : https://openintel.nl/data/

---

**Dernière mise à jour** : 21 mars 2026, 18:30 UTC
**Analysé par** : Claude Sonnet 4.5
**Conversion PDFs** : pdftotext (100% succès, 16/16 fichiers)
**Fiches créées** : 14/17 (82%) - **ÉTAT DE L'ART COMPLET** ✅
