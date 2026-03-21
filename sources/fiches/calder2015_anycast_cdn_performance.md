# Fiche de lecture - Analyzing Anycast CDN Performance

**Référence bibliographique** :
Calder, M., Flavel, A., Katz-Bassett, E., Mahajan, R., & Padhye, J. (2015). *Analyzing the Performance of an Anycast CDN*. Proceedings of the 2015 Internet Measurement Conference (IMC '15), 531-537. https://doi.org/10.1145/2815675.2815717

**Thème** :
Performance anycast CDN (Bing) vs unicast DNS-based redirection via mesures client-side

**Intérêt pour le mémoire** :
Démontre que routing anycast (utilisé par DNS root servers, CDNs) = simple mais suboptimal pour 20% clients. Pertinent pour comprendre diversité géographique réponses DNS et impact routing sur performance. Lien avec notre étude variations géographiques.

---

## Contexte de lecture

**Date de lecture** : 21 mars 2026
**Section du mémoire** :
- Section 2.6 (CDN, anycast, diversité géographique)

---

## Contenu de l'article

### Objectif(s) / Question(s) de recherche

**Questions** :
1. Anycast dirige-t-il clients vers front-ends **proches** ?
2. Quel **impact performance** si anycast redirige mal ?
3. **Gains potentiels** DNS-based unicast vs anycast ?

**Contexte CDN** :
- **DNS-based** (Akamai) : contrôle fin, near-real-time, mais infrastructure complexe/coûteuse
- **Anycast** (CloudFlare, Microsoft Bing) : simple, scalable, DDoS-resilient, **mais** :
  - Performance-agnostic (BGP routing, pas optimisation latence)
  - Unaware of server load
  - Routing changes → TCP sessions terminate

**Trade-off** : Simplicité opérationnelle vs contrôle précis client-front-end mapping

### Méthodologie

- **Type d'étude** : Mesures actives client-side (JavaScript beacon) + logs passifs
- **CDN** : Microsoft Bing anycast CDN (dozens front-ends, global, même AS)
- **Échelle** : **Millions queries** (mars-avril 2015)
- **Outils** :
  - JavaScript beacon injecté dans résultats recherche
  - W3C Resource Timing API (accurate latency measurements)
  - DNS authoritative logs
  - Passive server logs (client IP, location, front-end used)

**Protocole mesure** :
1. **Beacon** : 4 URLs fetched après page load
   - 1 anycast front-end (production)
   - 1 geographically closest (unicast)
   - 2 random nearby (weighted by distance)
2. **Warm-up request** : cache DNS (remove DNS lookup latency)
3. **Resource Timing API** : précision > JavaScript primitive timings
4. **Aggregation** : /24 prefixes (localisés), weighted by query volume

**Routing configuration** :
- **Anycast** : même IP annoncée depuis multiples locations (BGP best path)
- **Unicast** : /24 prefix unique par front-end, announced only closest peering point

**Front-end selection** :
- 10 closest front-ends per LDNS (geolocation)
- Justification : Figure 1 montre diminishing returns après 5 front-ends

### Résultats principaux

#### 1. Anycast performance globale

**Chiffre clé (Figure 3)** :
- **~80% requests** : anycast performs **as well as best** unicast
- **20% requests** : anycast **≥25ms slower** than best unicast
- **~10% requests** : anycast **≥100ms slower**

**Interprétation** :
- Anycast = **généralement bien** (80% optimal)
- **Mais** 20% clients suboptimal → gains potentiels DNS redirection

#### 2. Client distance to front-ends

**Figure 2 - Distance nearest front-ends (median, weighted by query volume)** :
- **1st closest** : 280 km
- **2nd closest** : 700 km
- **4th closest** : 1,300 km

**CDN deployment comparison** :
- Bing CDN : dozens locations (similar Level3, MaxCDN)
- Smaller deployments : CloudFront (37), CacheFly (41), CloudFlare (43), EdgeCast (31)
- Larger : Level3 (62), CDNify (17-62 range)

#### 3. Anycast inefficiencies = stable

**Key finding** :
- Inefficiencies **stable enough** for **prediction scheme**
- History-based DNS redirection can improve **15-20% clients**

**Implication** :
- Hybrid approach viable : anycast (80%) + DNS redirection (20% underserved)
- Simple prediction = practical solution

#### 4. Anycast vs DNS trade-offs

**Anycast advantages** :
- ✅ Simple to operate, scalable
- ✅ DDoS resilient
- ✅ Per-client redirection (not per-LDNS like DNS)
- ✅ Works well for **most** clients

**Anycast limitations** :
- ❌ Performance-agnostic (BGP routing, not latency-aware)
- ❌ Unaware server load
- ❌ Routing changes → TCP session disruptions
- ❌ **20% clients suboptimal** mapping

**DNS advantages** :
- ✅ Fine-grained control, near-real-time
- ✅ Performance-based decisions

**DNS limitations** :
- ❌ Complex infrastructure, expensive
- ❌ Per-LDNS granularity (not per-client)
- ❌ Public resolvers (Google DNS, OpenDNS) = geographically disparate clients
- ⚠️ ECS (EDNS Client Subnet) = partial solution but not widely adopted (2015)

### Conclusion des auteurs

**Contributions** :
1. ✅ **First study** anycast CDN performance (client-side measurements)
2. ✅ **Quantification** anycast inefficiency : 20% clients suboptimal
3. ✅ **Practical insight** : hybrid anycast + DNS redirection viable

**Mixed picture** :
- Anycast delivers optimal performance **for most** clients
- But **20% underserved** → room for improvement
- Simple prediction scheme → improve 15-20% clients

**Limitations** :
- Study tied to **Bing CDN deployment** (2015)
- Specific conclusions may not generalize all CDNs
- But reveals important insights CDN performance

---

## Analyse personnelle

### Que garder pour le mémoire

**Concepts clés** :
- **Anycast routing** = simple mais performance-agnostic
- **BGP best path** ≠ lowest latency path
- **Geographic diversity** front-ends crucial
- **Client-side measurements** révèlent performance réelle
- **80/20 rule** : anycast OK pour majorité, problématique pour minorité significative

**Chiffres importants** :
- **20%** clients anycast suboptimal (≥25ms slower)
- **10%** clients anycast very poor (≥100ms slower)
- **15-20%** clients améliorables via DNS redirection
- **280 km** median distance nearest front-end
- **Millions** queries analysées

**Méthodes applicables** :
- JavaScript beacon pour mesures client-side
- W3C Resource Timing API (accurate latency)
- Warm-up requests (remove DNS lookup bias)
- Aggregation /24 prefixes weighted by volume
- Comparison anycast vs unicast alternatives

**Limites pour nous** :
- Étude 2015 (10 ans) → évolution anycast ?
- Bing CDN spécifique → généralisation ?
- Focus latency (pas availability, security)
- ECS adoption limitée 2015 → maintenant plus répandu ?

### Critique personnelle

**Forces** :
- ✅ **Large scale** : millions queries, real production CDN
- ✅ **Client-side** : real-world performance (not synthetic probes)
- ✅ **Mixed methods** : active beacon + passive logs
- ✅ **Practical** : hybrid solution proposed (actionable)
- ✅ **Honest** : anycast works for most, but admits 20% problem
- ✅ **Rigorous** : W3C API, warm-up, weighted aggregation

**Faiblesses** :
- ⚠️ **Single CDN** : Bing only, generalization unclear
- ⚠️ **Temporal snapshot** : mars-avril 2015, no longitudinal
- ⚠️ **No causality** : why anycast fails for 20% ? (routing policies, peering, etc.)
- ⚠️ **Limited geographic analysis** : aggregate results, not per-region breakdown
- ⚠️ **ECS discussion light** : mentions ECS but doesn't test impact
- ⚠️ **Security/DDoS** : claims resilience but no empirical validation

**Lien avec autres articles** :

- **Nosyk 2024 (RIPE Atlas)** :
  - RIPE Atlas = distributed vantage points (12.9K)
  - Calder : anycast = geography matters (20% suboptimal)
  - Notre mémoire : RIPE Atlas peut révéler variations anycast routing

- **Xu 2023 (Centralization)** :
  - Xu : DNS backend centralisé (oligopole)
  - Calder : Frontend routing (anycast) aussi problématique
  - Double challenge : backend centralized + frontend suboptimal

- **OpenINTEL (vanRijswijk 2016)** :
  - OpenINTEL : 1 point mesure (Pays-Bas)
  - Calder : geographic diversity crucial (20% impact)
  - Argument pour distributed measurements

- **Boswell 2024, Johnson 2016** :
  - Geographic bias manifeste (FRITZ!Box Europe, China mirror)
  - Calder : routing geography-dependent
  - Cohérence : location matters across DNS layers

**Questions ouvertes** :
1. **Évolution 2015-2024** : Anycast performance improved ?
2. **ECS adoption impact** : Résout-il problème 20% suboptimal ?
3. **Geographic breakdown** : Quelles régions plus affectées ?
4. **Root causes** : Pourquoi BGP routing suboptimal pour 20% ?
5. **IPv6** : Anycast performance IPv6 vs IPv4 ?
6. **Prediction scheme** : Details algorithm ? Deployed production ?

### Citations importantes

> "Anycast is simple to operate, scalable, and naturally resilient to DDoS attacks. This simplicity, however, comes at the cost of precise control of client redirection." (Abstract)

> "We find that anycast usually performs well despite the lack of precise control but that it directs roughly 20% of clients to a suboptimal front-end." (Abstract)

> "Most of the time, in most regions, anycast does well, performing as well as the best of the three nearby unicast front-ends. However, anycast is at least 25ms slower for 20% of requests, and just below 10% of anycast measurements are 100ms or more slower than the best unicast for the client." (Section 5)

> "We demonstrate that the anycast inefficiencies are stable enough that we can use a simple prediction scheme to drive DNS redirection for clients underserved by anycast, improving performance of 15%-20% of clients." (Abstract)

**Sur trade-offs** :
> "Content delivery networks must balance a number of trade-offs when deciding how to direct a client to a CDN server. Whereas DNS-based redirection requires a complex global traffic manager, anycast depends on BGP to direct a client to a CDN front-end." (Abstract)

---

## Utilisation dans le mémoire

**Sections concernées** :
- **Section 2.6 (CDN, anycast)** : Performance anycast, limitations
- **Section 7 (Discussion)** : Geographic diversity importance, RIPE Atlas value

**Points à développer** :

**État de l'art** :
- Anycast = trade-off simplicité vs performance
- 20% clients suboptimal → distributed measurements crucial
- BGP routing geography-dependent
- DNS root servers use anycast (12/13) → same limitations apply

**Notre contribution** :
- RIPE Atlas 12.9K vantage points → can reveal anycast routing variations
- Geographic diversity queries → observe which clients get suboptimal routing
- Tranco + RIPE Atlas → analyze variations across geographic locations

**Discussion** :
- Calder montre **why** geographic diversity matters (20% impact)
- Notre approche : mesurer variations **caused by** anycast routing
- OpenINTEL (1 point) = cannot observe geographic diversity
- RIPE Atlas (distributed) = ideal for studying anycast behavior

**Limitations** :
- RIPE Atlas probes = fixed locations (not all client populations)
- But 178 countries → better coverage than single vantage point

---

**Tags** : #anycast #cdn #performance #bgp-routing #latency #geographic-diversity #dns #client-side-measurement #microsoft-bing

**Statut** : [X] Lu (PDF via MD) / [X] Fiché / [ ] Intégré mémoire

**Date fiche** : 21 mars 2026
