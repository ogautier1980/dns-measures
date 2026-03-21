# Fiche de lecture - Anycast in Context: Root DNS vs CDN

**Référence bibliographique** :
Koch, T., Li, K., Ardi, C., Katz-Bassett, E., Calder, M., & Heidemann, J. (2021). *Anycast in Context: A Tale of Two Systems*. Proceedings of the 2021 ACM SIGCOMM Conference, 398-417. https://doi.org/10.1145/3452296.3472891

**Thème** :
Comparaison inflation anycast dans root DNS vs Microsoft CDN - contexte applicatif crucial

**Intérêt pour le mémoire** :
Montre que inflation anycast dépend fortement du contexte : root DNS (>95% users inflated mais caching = impact minimal) vs CDN (35% inflated, peering extensif limite impact). Pertinent pour comprendre que diversité géographique DNS queries dépend routing anycast + économie service.

---

## Contexte de lecture
**Date** : 21 mars 2026
**Sections** : 2.6 (Anycast, CDN), 2.1 (Root DNS)

---

## Contenu

### Objectifs

**Paradoxe** : Anycast criticized (SIGCOMM 2018 "hundreds of ms inflation") mais adoption croissante production

**Questions** :
1. Inflation anycast = inhérente ou dépend contexte ?
2. Impact réel inflation sur users (pas juste recursive resolvers) ?
3. Pourquoi anycast continue expansion malgré inefficiency ?

**Systèmes comparés** :
- **Root DNS** : 13 letters, 6-254 sites/letter, diverse deployments
- **Microsoft CDN** : >100 sites, multiple rings, latency-sensitive content

### Méthodologie

**Échelle exceptionnelle** :
- **Root DNS** : 51.9B queries/jour (DITL 2018), millions recursives, tous users worldwide
- **Microsoft CDN** : >1B users, 15K ⟨region,AS⟩ locations, hundreds countries
- **RIPE Atlas** : 7K pings, 1K probes, 500+ ASes (calibration)

**Datasets** :
- DITL 2018 (48h captures, 11/13 root letters)
- Microsoft proprietary (TCP RTT logs, client-side measurements)
- ISI packet captures (100M queries)
- APNIC user population estimates (reproducibility)

**Preprocessing DITL** :
- Remove 31B NXDOMAIN (28% Chromium hijack detection)
- Remove 2B PTR queries
- Remove private IPs (7%)
- IPv4 only (exclude 12% v6)
- Final: ~19B queries
- Join with Microsoft user counts (DITL∩CDN dataset)

**Metrics** :
- **Geographic Inflation (GI)** : distance vs closest site (speed of light in fiber)
- **Latency Inflation (LI)** : measured RTT vs optimal
- User-weighted (pas juste recursive-weighted comme prior work)

### Résultats Root DNS

**Inflation très répandue** :
- **>95% users** experience some inflation to individual root letters
- **40% users** : >100ms inflation to some letters
- **But** : per-query average inflation lower (recursives prefer best letters)
- **10% users** : >100ms inflation average across queries

**Context crucial** :
- Users interact with root **once per day** (median)
- Caching DNS records (long TTLs) = delay minimal
- Root DNS latency **hardly matters** to users
- Preferential querying by recursives reduces impact

### Résultats Microsoft CDN

**Inflation limitée** :
- **35% users** experience any inflation
- Inflation amount **smaller** than root DNS
- Extensive **peering + engineering** investment control inflation
- Latency **matters** : several RTTs per page load (vs root 1/day)

**Economic incentives** :
- CDN: latency = competitive advantage → optimize
- Root DNS: latency doesn't matter (caching) → focus DDoS resilience, availability

**Engineering differences** :
- CDN: extensive AS-level connectivity, peering agreements
- Root DNS: expansion driven by DDoS mitigation, geographic diversity (not latency)

### Conclusions

**Key finding** : **Context matters**
- Anycast inflation ≠ inherent technical limitation
- Depends on **economic incentives** + **engineering investment**
- Root DNS: high inflation acceptable (caching mitigates)
- CDN: low inflation achievable (when latency matters)

**Takeaway** :
- Prior claims "anycast inefficient" = **single application**, not anycast potential
- Where latency counts, anycast performance **can be quite good**
- Cannot generalize anycast performance across services

---

## Analyse personnelle

### Pour le mémoire

**Concepts clés** :
- **Context-dependent performance** : anycast = pas bon/mauvais absolu
- **Economic incentives** drive optimization (CDN) or not (root DNS)
- **Caching** crucial DNS performance (amortizes latency)
- **User vs recursive** metrics = different conclusions
- **AS-level connectivity** + peering = control inflation

**Chiffres** :
- **>95%** users inflated (root DNS individual letters)
- **35%** users inflated (Microsoft CDN)
- **>1B** users analyzed (CDN)
- **51.9B** queries/day (root DNS)
- **100+** CDN sites, **6-254** root sites/letter
- **1/day** median user root DNS interaction

**Méthodes** :
- User-weighted analysis (pas juste recursive-weighted)
- Join passive (DITL) + proprietary (Microsoft users)
- Geographic + latency inflation metrics
- AS-level connectivity analysis

**Limites** :
- Microsoft CDN = proprietary (reproducibility limitée)
- APNIC data = approximation (public resolvers problem)
- Cannot generalize to all anycast services

### Critique

**Forces** :
- ✅ **Largest anycast study** to date (billions queries, billion users)
- ✅ **Fair comparison** : same methodology root DNS vs CDN
- ✅ **User-centric** : weight by users, not recursives
- ✅ **Context emphasis** : demonstrates importance application characteristics
- ✅ **Complete root DNS** : 11/13 letters (prior work = 1 letter)
- ✅ **Economic angle** : explains why inflation differs

**Faiblesses** :
- ⚠️ **Proprietary data** : Microsoft CDN not reproducible
- ⚠️ **Temporal snapshot** : 2018 DITL, 2019-2021 CDN
- ⚠️ **Single CDN** : Microsoft only (generalization ?)
- ⚠️ **IPv4 bias** : excludes 12% v6 traffic
- ⚠️ **Preprocessing** : removes 60%+ queries (justified but aggressive)

### Liens

**vs Calder 2015** :
- Calder : 20% Bing CDN users suboptimal
- Koch : 35% Microsoft CDN inflated (consistent)
- Both : anycast works for majority, problems minority

**vs Nosyk 2024 (RIPE Atlas)** :
- Koch : RIPE Atlas coverage not representative (3.7K ASes)
- Nosyk : 12.9K probes, 178 countries
- Koch dataset : 22K ASes, 224 countries (DITL >> RIPE Atlas)

**vs Xu 2023 (Centralization)** :
- Xu : backend infrastructure centralisé
- Koch : frontend routing (anycast) context-dependent
- Complémentarité : centralisation + routing = multi-layer challenges

**Notre mémoire** :
- Koch : geographic routing matters, context crucial
- Nous : RIPE Atlas distributed measurements reveal geographic variations
- Lien : anycast routing geography-dependent → distributed vantage points essential

### Citations

> "We reassess anycast performance [...] We show that inflation is very common in root DNS, affecting more than 95% of users. However, we then show root DNS latency hardly matters to users because caching is so effective." (Abstract)

> "Only 35% of CDN users experience any inflation, and the amount they experience is smaller than for root DNS. We show that CDN anycast latency has little inflation due to extensive peering and engineering." (Abstract)

> "These results suggest prior claims of anycast inefficiency reflect experiments on a single application rather than anycast's technical potential, and they demonstrate the importance of context when measuring system performance." (Abstract)

> "Most users interact with the root DNS once per day [...] Delay is minimal due to caching of root DNS records with long TTLs at recursive resolvers." (§4)

> "Microsoft is able to control inflation through extensive peering and engineering investment, even though inefficiency increases with larger deployments." (§7.1)

---

## Utilisation mémoire

**Sections** :
- **2.1 (Root DNS)** : Anycast deployment, inflation acceptable (caching)
- **2.6 (CDN/Anycast)** : Context-dependent performance, engineering matters
- **7 (Discussion)** : Geographic diversity + economic incentives

**Points** :
- Anycast routing = geography-dependent (Koch confirme)
- Context crucial : root DNS (1/day) vs CDN (several RTTs/page)
- RIPE Atlas (12.9K points) complements DITL global view
- Distributed measurements reveal variations anycast routing

**Notre contribution** :
- Koch : context matters (application characteristics)
- Nous : geographic context matters (vantage point location)
- RIPE Atlas = distributed context for observing anycast behavior

---

**Tags** : #anycast #root-dns #cdn #inflation #latency #context #economic-incentives #peering #microsoft #ditl #sigcomm2021

**Statut** : [X] Lu / [X] Fiché / [ ] Intégré

**Date** : 21 mars 2026
