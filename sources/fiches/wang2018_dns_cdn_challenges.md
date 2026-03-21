# Fiche de lecture - Evolution and Challenges of DNS-based CDNs

**Référence bibliographique** :
Wang, Z., Huang, J., & Rose, S. (2018). *Evolution and challenges of DNS-based CDNs*. Digital Communications and Networks, 4(4), 235-243. https://doi.org/10.1016/j.dcan.2017.07.005

**Thème** :
Survey complet DNS-based CDNs : problème remote DNS, solutions (ECS, Name Extension, Direct Resolution), privacy concerns (client location + redirection enumeration)

**Intérêt pour le mémoire** :
Synthèse état de l'art 2018 sur redirection DNS/CDN. Identifie **paradoxe remote DNS** : adoption croissante (27%/an) DNS publics (Google, OpenDNS) dégrade performance CDN (113% distance si mismatch 2 units). Solutions (ECS) posent problèmes privacy. Pertinent pour comprendre trade-offs performance vs privacy et impact choix DNS resolver sur diversité géographique réponses.

---

## Contexte de lecture

**Date de lecture** : 21 mars 2026
**Section du mémoire** :
- Section 2.6 (CDN, DNS resolvers, remote DNS problem, ECS)

---

## Contenu de l'article

### Objectif(s) / Question(s) de recherche

**Problème central** : **Remote DNS issue** :
- DNS-based CDNs = méthode redirection **la plus populaire** (Akamai, Limelight, Mirror Image)
- Assume : **DNS recursive server proche client**
- Réalité : **Adoption croissante remote DNS** (Google 8.8.8.8, OpenDNS, etc.)
  - 2012 : **8.6% users** public DNS, **27% annual growth**
  - Google DNS : **74% annual increase**
- Conséquence : CDN redirige vers serveur proche **DNS resolver**, pas proche **client**
  - → **Performance degradation** significative

**Questions de recherche** :
1. Comment résoudre **remote DNS problem** sans casser infrastructure DNS existante ?
2. Quelles **implications privacy** des solutions proposées ?
3. Quels **trade-offs** entre performance CDN, simplicité déploiement, et privacy ?

**Objectif paper** :
- ✅ **First comprehensive survey** DNS-based CDNs
- ✅ Synthèse **state-of-art solutions** remote DNS (ECS, Name Extension, Direct Resolution)
- ✅ Identification **privacy concerns** : client location + redirection enumeration
- ✅ Comparaison systématique 7 solutions selon 5 métriques
- ✅ Modèle conceptuel CDN performance (Weibull, Lognormal distributions)

### Méthodologie

- **Type d'étude** : Survey + analyse comparative + modélisation théorique
- **Pas de mesures empiriques** : synthèse littérature existante (2017-2018)
- **Sources** :
  - Publications académiques (Calder 2015, Otto 2012, etc.)
  - RFCs (EDNS, ECS)
  - Industry reports (Google, Akamai, CDN providers)

- **Approche** :
  1. **Taxonomie** mécanismes redirection CDN (4 types)
  2. **Analyse** remote DNS problem
  3. **Synthèse** 3 solutions proposées récentes
  4. **Identification** 2 privacy concerns
  5. **Comparaison** 7 solutions selon 5 métriques
  6. **Modélisation** CDN performance (distributions probability)

**Framework d'analyse (5 métriques)** :

| Métrique | Description |
|----------|-------------|
| **Client complexity** | Overhead stub resolver (IoT, mobile) |
| **Intermediate transparency** | Compatibilité middle-boxes (recursive servers) |
| **CDN performance** | Précision client location → optimal server |
| **Client location privacy** | Information leaked in-path (recursive → authoritative) |
| **Redirection privacy** | Difficulté enumeration complete CDN mapping |

### Résultats principaux

#### 1. Taxonomie mécanismes redirection CDN (Section 2)

**4 approches** :

**HTTP redirection** :
- Web server → HTTP headers (301, 302)
- ❌ Extra round-trip delay
- ❌ Heavy processing overhead
- Utilisation : limitée

**URL rewriting** :
- Origin server rewrites embedded objects URLs
- ❌ URL parsing delay
- ❌ Rewritten URLs non-cacheable
- Utilisation : objets embarqués

**Anycast** (Section 2.3) :
- Network layer, transparent
- Same IP → multiple servers (BGP routing)
- ✅ Simple, scalable, DDoS-resilient
- ❌ Performance-agnostic (BGP ≠ latency-aware)
- ❌ 20% clients suboptimal (Calder 2015)
- ❌ Routing changes → TCP session disruptions
- Utilisation : CloudFlare, root DNS (12/13)

**DNS-based redirection** (Section 2.4) :
- ✅ **Most popular** (Akamai, Limelight, Mirror Image)
- ✅ **Transparent** to end users
- ✅ **Simple** : uses existing DNS infrastructure
- ✅ **Flexible** : TTL tuning (static vs dynamic)
- Mécanisme : CNAME content → CDN domain → IP optimal server
- TTL small → dynamic redirection (zero TTL = per-request)

#### 2. Remote DNS problem (Section 3.1)

**False assumption** : DNS recursive server **proximate** to client

**Réalité adoption public DNS** :
- **2012** : 8.6% users (Google, OpenDNS, Level3)
- **Growth** : 27% annual (Google 74% annual)
- Motivations : availability, stability, security (vs ISP DNS)

**Impact mesuré** (Otto 2012) :
- **ISP DNS** : 80% locations similarity with clients
- **Public DNS** : 90% locations **NO similarity** with clients
- **HTTP latency** : Public DNS = **2× latency** vs ISP DNS
- Explication : sub-optimal redirection (servers far from clients)

**Afrique study** (2019) :
- Remote DNS → **+100 ms** DNS resolution delay (50% probes)
- Geographic mismatch critique

**Local DNS clusters** :
- Behind local DNS : clusters hosts (size, geography unknown)
- CDN cannot optimize without knowledge → suboptimal

#### 3. Solutions remote DNS (Section 3.2)

**Solution 1 : ECS (EDNS-Client-Subnet)** - RFC 7871

**Principe** :
- DNS recursive server inclut **client IP prefix** in DNS query (EDNS0 OPT record)
- Authoritative server uses **client location** (not resolver location) for redirection

**Avantages** :
- ✅ Résout remote DNS problem (client location accurate)
- ✅ Standardisé (Google proposal, IETF accepted)

**Limitations** :

*Deployment complexity* :
- ❌ **End users** : upgrade stub resolvers (browsers, email clients)
- ❌ **Recursive servers** : ECS support (implementation barely available 2017)
- ❌ **Authoritative servers** : ECS compatibility
- ❌ **Middle-boxes** : forward ECS payloads unmodified
- → **Joint effort** all parties (non-trivial)

*Cache efficiency* :
- ❌ **1-to-1 caching** → **1-to-many** (ECS scope dimension)
- ❌ Cache expanded by **factor of ECS scopes**
- ❌ Vulnerability DoS attacks (bypass caching, flood authoritative)

*Transition challenges* :
- ❌ **No signaling** ECS support upstream → downstream
- ❌ ECS-compliant clients → non-ECS recursive servers = **wasted payload**
- ❌ ECS recursive → non-ECS authoritative = **privacy leak** unnecessary

*Privacy concerns* (Section 4.1) :
- ❌ **Client location exposed** to authoritative servers + on-path eavesdroppers
- Trade-off : **longer prefix** = better CDN, worse privacy
- Conventional DNS : client **hidden** by recursive server (behavioral privacy)
- ECS : client visible → monitoring, recording, analysis possible

*Redirection enumeration* (Section 4.2) :
- ❌ **Easy enumeration** CDN mapping (Calder 2016)
  - Routable /24 prefixes → **1 day** enumerate Google
- ❌ Reveals CDN infrastructure, serving strategy
- ❌ Risk DDoS attacks (complete mapping known)
- ❌ Violates CDN provider privacy

**Solution 2 : Name Extension**

**Principe** :
- Client encodes location in **DNS query name** (prefix original name)
- Recursive server handles as normal (transparent)
- Authoritative server extracts location from query name

**Avantages** :
- ✅ **End-to-end** extension (client ↔ authoritative)
- ✅ **No intermediate support** required (DNS recursive unchanged)
- ✅ Lower deployment obstacles vs ECS

**Limitations** :
- ❌ Similar **privacy issues** as ECS (location exposed)
- ❌ Scope-based redirection → **enumeration possible**
- ❌ Client complexity slightly higher (encoding)

**Solution 3 : Direct Resolution**

**Principe** :
- Recursive server translates content domain → CDN domain
- **Client itself** contacts CDN authoritative server (not via recursive)
- Redirection based on **client location** (not resolver)

**Avantages** :
- ✅ Better optimization (client location accurate)
- ✅ Outperforms remote DNS + even local DNS (some cases)

**Limitations** :
- ❌ **Client complexity increased** : more queries, caching overhead
- ❌ **Privacy reduced** : full client IP visible (not just prefix like ECS)
- ❌ Client must handle DNS resolution complexity

#### 4. Privacy solution : Client Pseudononymizing (Section 4.3)

**Principe** :
- Client uses **pseudonymizing identifier** (not IP prefix) in DNS requests
- **Trustworthy third party** : maintains IP ↔ pseudonym mapping
- Authoritative server forwards to third party for redirection decision
- Third party returns CDN selection (secure lookup)

**Avantages** :
- ✅ **Client location privacy** preserved (on-path cannot see IP)
- ✅ **Redirection privacy** preserved (no enumeration)
- ✅ **CDN performance** maintained (third party knows real location)

**Limitations** :
- ❌ **Extra latency** : authoritative → third party lookup
- ❌ **Bottleneck** : third party = critical infrastructure
- ❌ **Trust** : requires trustworthy third party

**Optimizations** :
- Clouding third party infrastructure (reduce latency)
- Piggyback predicted results
- Validity time → enable caching

#### 5. Comparaison systématique (Section 5, Table 1)

**7 solutions analysées** :

| Solution | Client complexity | Intermediate transp. | CDN perf. | Client priv. | Redir. priv. |
|----------|-------------------|----------------------|-----------|--------------|--------------|
| **Local server** | Low | Good | Medium | Medium | Good |
| **Remote server** | Low | Good | **Bad** | **Good** | Good |
| **Client server** | **High** | Good | **Good** | **Bad** | Good |
| **ECS** | Low | **Bad** | **Good** | **Bad** | **Bad** |
| **Direct Resolution** | Medium | Good | **Good** | **Bad** | Good |
| **Name Extension** | Low | Good | **Good** | **Bad** | **Bad** |
| **Client pseudononymizing** | Low | **Bad** | **Good** | **Good** | **Good** |

**Insights** :

**Local server** :
- ✅ Default choice most users (majority)
- ⚠️ Proximity not always guaranteed (cellular DNS = suboptimal)
- Balance : medium CDN perf, medium client privacy
- Public DNS study (2011) : ISP DNS better than Google/OpenDNS

**Remote server** :
- ❌ **Worst CDN performance** (location mismatch)
- ✅ Best client privacy (client hidden)
- Growing adoption despite performance penalty

**Client server** :
- ✅ Optimal CDN (co-location client + server)
- ❌ Rare in practice (high complexity, uneconomical)
- ❌ Worst client privacy (full IP exposed)

**ECS** :
- ✅ Best CDN performance (accurate client location)
- ❌ Worst client privacy (IP prefix exposed)
- ❌ Worst redirection privacy (easy enumeration)
- ❌ Bad intermediate transparency (recursive server modifications)

**Direct Resolution** :
- ✅ Best CDN performance
- ⚠️ Medium complexity (client handles resolution)
- ❌ Worst client privacy (full IP, not just prefix)
- ✅ Good redirection privacy (single IP-based, no enumeration)

**Name Extension** :
- Similar to ECS but better intermediate transparency
- ❌ Same privacy issues (location exposed, enumeration)

**Client pseudononymizing** :
- ✅ **Only solution** preserving both privacies + CDN performance
- ❌ Requires trustworthy third party (infrastructure cost)
- ❌ Extra latency

#### 6. Modélisation CDN performance (Section 5.3)

**Modèle conceptuel** : Impact location mismatch (client ↔ recursive server) on CDN performance

**Distributions testées** : Weibull, Lognormal (distance recursive ↔ CDN server)

**Hypothèses** :
- Optimal CDN : server proche requestor
- Distance distribution f(x) : prob(co-location) ≈ 0, prob(infinite distance) ≈ 0
- Peak probability at x_max (most likely distance)

**Résultats (Figures 3-6)** :

**Weibull distribution** (λ=1.09, k=5) :
- Location mismatch **0.2 units** : CDN distance increase **< 5%**
- Location mismatch **2 units** : CDN distance increase **113%**
- → Performance penalty grows **rapidly** with mismatch

**Lognormal distribution** (μ=0.5493, σ=1.0481) :
- Similar curve, **steeper slope** (near-field effects)
- Confirms rapid degradation with mismatch

**Implications** :
- Explains **remote server poor performance** (large mismatch)
- Explains **local server medium performance** (small but non-zero mismatch)
- Matches empirical measurements (Otto 2012, others)

### Conclusion des auteurs

**Contributions** :
1. ✅ **First comprehensive survey** DNS-based CDNs
2. ✅ **State-of-art solutions** remote DNS problem (ECS, Name Extension, Direct Resolution)
3. ✅ **Privacy identification** : client location + redirection enumeration
4. ✅ **Systematic comparison** 7 solutions, 5 metrics
5. ✅ **Conceptual model** CDN performance (quantifies mismatch impact)

**Key findings** :

**Remote DNS = growing problem** :
- 8.6% users public DNS (2012), 27% annual growth
- Performance penalty severe (2× latency, 113% distance increase)

**Solutions trade-offs** :
- **ECS** : best CDN performance, worst privacy
- **Local DNS** : balance performance + privacy (majority users)
- **Client pseudononymizing** : best privacy + CDN, but infrastructure cost

**Privacy overlooked** :
- Most prior works ignore privacy
- ECS enables enumeration (1 day Google CDN mapping)
- Client location exposure → behavioral tracking

**Design guidelines** :
- CDN providers : consider privacy-preserving solutions
- Users : understand trade-off public DNS (security) vs ISP DNS (performance)
- Researchers : need better solutions (privacy + performance + simplicity)

**Limitations** :
- Survey 2017-2018 (évolution depuis ?)
- No empirical measurements (synthesis only)
- Model simpliste (distributions assumptions)

---

## Analyse personnelle

### Que garder pour le mémoire

**Concepts clés** :
- **Remote DNS paradox** : adoption croissante (security) dégrade CDN performance
- **Trade-off triangle** : CDN performance ↔ client privacy ↔ deployment simplicity
- **ECS** = solution dominante (IETF) mais privacy concerns majeurs
- **Location mismatch** = performance penalty exponential (113% si 2 units)
- **Redirection enumeration** = privacy threat (1 day CDN mapping)

**Chiffres essentiels** :
- **8.6%** users public DNS (2012), **27% annual growth**, Google **74% annual**
- **2× latency** public DNS vs ISP DNS (Otto 2012)
- **+100 ms** DNS delay Afrique (50% probes) due to remote DNS
- **113%** CDN distance increase si location mismatch 2 units (model)
- **1 day** enumerate Google CDN mapping avec ECS (Calder 2016)
- **90%** locations no similarity public DNS vs clients (Otto)

**Taxonomie solutions** (7) :
1. Local server (majority users, default)
2. Remote server (growing, poor CDN perf)
3. Client server (rare, high complexity)
4. ECS (IETF, best CDN, worst privacy)
5. Direct Resolution (client-side, medium complexity)
6. Name Extension (similar ECS, better transparency)
7. Client pseudononymizing (best privacy, infrastructure cost)

**Limites pour nous** :
- Survey 2017-2018 (évolution ECS adoption ?)
- Pas mesures empiriques (synthesis only)
- Model théorique (Weibull, Lognormal = assumptions)
- Focus CDN performance (pas DNS query time, cache effects)

### Critique personnelle

**Forces** :
- ✅ **Comprehensive survey** : first systematic DNS-based CDN overview
- ✅ **Multi-dimensional analysis** : 5 metrics × 7 solutions
- ✅ **Privacy emphasis** : identifies overlooked threats (enumeration)
- ✅ **Practical model** : quantifies mismatch impact (113%)
- ✅ **Design guidelines** : actionable for CDN providers
- ✅ **Honest trade-offs** : no silver bullet (performance vs privacy)

**Faiblesses** :
- ⚠️ **No empirical data** : survey only, no measurements
- ⚠️ **Model simpliste** : distributions assumptions not validated
- ⚠️ **Snapshot 2017** : ECS adoption evolved since ?
- ⚠️ **Limited solutions** : ignores hybrid approaches
- ⚠️ **Privacy light** : mentions concerns but no deep analysis
- ⚠️ **No temporal evolution** : adoption trends predictions ?

**Lien avec autres articles** :

- **Hours 2016 (DNS resolvers CDN)** :
  - Hours : causal analysis LDNS vs GDNS (14% distance, 30% config)
  - Wang : survey solutions remote DNS problem
  - Cohérence : remote DNS = performance penalty confirmed
  - Wang modèle (113%) > Hours empirique (14%) → depends context

- **Calder 2015 (Anycast)** :
  - Wang : anycast = 20% suboptimal, session disruptions
  - Calder : confirms 20% suboptimal empirically
  - Wang : DNS-based redirection preferred despite anycast simplicity

- **Xu 2023 (Centralization)** :
  - Xu : DNS infrastructure centralized (oligopoly)
  - Wang : public DNS adoption 27% annual (Google, OpenDNS)
  - Paradoxe : centralization + remote DNS = double performance threat

- **Nosyk 2024 (RIPE Atlas)** :
  - Nosyk : RIPE Atlas 12.9K vantage points
  - Wang : local vs remote DNS = location matters
  - Notre mémoire : RIPE Atlas peut mesurer variations remote DNS impact

**Questions ouvertes** :
1. **ECS adoption 2018-2024** : déploiement généralisé ? Privacy résolu ?
2. **Public DNS trends** : 27% growth continue ? Saturation ?
3. **IPv6 impact** : ECS patterns IPv6 vs IPv4 ?
4. **Hybrid solutions** : combining privacy + performance ?
5. **Client awareness** : users comprennent trade-off DNS choice ?
6. **CDN evolution** : edge computing reduce remote DNS impact ?

### Citations importantes

> "DNS-based server redirecting is considered the most popular means of deploying CDNs. However, with the increasing use of remote DNS, DNS-based CDNs face a great challenge in performance degradation." (Abstract)

> "According to a 2012 study, the public DNS user base grew by 27% annually, and 8.6% of users in the sample relied on a public DNS service." (Section 3.1)

> "ISP DNS was shown to have some similarity with clients in at least 80% of locations, and there was no similarity between public DNS and client for 90% of locations. [...] For HTTP performance, public DNS was found to yield doubled latencies compared with clients and ISP DNS." (Section 3.1)

**Sur modèle performance** :
> "The expected distance between a client and a CDN surrogate server increases by less than 5% when the DNS recursive server is 0.2 units away from the client. The CDN performance penalty grows rapidly with the increase in location mismatch. E.g., the expected distance between the client and the CDN surrogate server increases by 113% when the DNS recursive server is 2 units away from the client." (Section 5.3)

**Sur privacy ECS** :
> "ECS makes client location information visible to the DNS authoritative server and on-path eavesdroppers. Thus, client location privacy, which is well protected by remote DNS, is almost invalidated by ECS." (Introduction)

**Sur redirection enumeration** :
> "By using routable/24 client prefixes, queries against Google were reported as taking about a day to enumerate. The efficiency of ECS-based redirection enumeration highlights the privacy issue with any IP block-based redirection mechanism." (Section 4.2)

---

## Utilisation dans le mémoire

**Sections concernées** :
- **Section 2.6 (CDN, DNS resolvers)** : Remote DNS problem, ECS, trade-offs
- **Section 7 (Discussion)** : Privacy vs performance, distributed measurements value

**Points à développer** :

**État de l'art** :
- DNS-based CDN = most popular (Akamai, etc.)
- Remote DNS problem = growing (27% annual public DNS adoption)
- Performance penalty severe (2× latency, 113% distance model)
- ECS = solution IETF mais privacy concerns (enumeration 1 day)
- Trade-off insoluble : performance vs privacy vs simplicity

**Notre contribution** :
- Wang : remote DNS = location mismatch → performance degradation
- Notre approche : RIPE Atlas 12.9K vantage points → mesure impact distributed
- Geographic diversity queries → révèle variations redirection selon resolver location
- Quantifier empiriquement remote DNS impact à l'échelle globale

**Discussion** :
- Wang modélise impact théorique (113% distance si mismatch 2 units)
- RIPE Atlas peut mesurer impact **réel** : probes different locations + different DNS resolvers
- Identifier si public DNS (Google) vraiment 2× latency vs local (Otto 2012)
- Complémentarité : survey (Wang) + empirical distributed measurements (nous)

**Méthodologie** :
- Inspiration 5 metrics framework (complexity, transparency, performance, privacy)
- RIPE Atlas peut tester solutions (local DNS, public DNS, ECS-enabled)
- Measure redirection variations géographiques

**Limitations** :
- RIPE Atlas probes = fixed locations (not all users)
- But 178 countries → better coverage than Otto 2012 sample

---

**Tags** : #dns #cdn #remote-dns #ecs #edns-client-subnet #privacy #performance #survey #google-dns #public-dns #redirection #enumeration #location-privacy

**Statut** : [X] Lu (PDF via MD) / [X] Fiché / [ ] Intégré mémoire

**Date fiche** : 21 mars 2026
