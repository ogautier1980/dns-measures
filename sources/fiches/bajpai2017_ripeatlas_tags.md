# Fiche de lecture - Vantage Point Selection for IPv6 Measurements

**Référence bibliographique** :
Bajpai, V., Eravuchira, S. J., Schönwälder, J., Kisteleki, R., & Aben, E. (2017). *Vantage Point Selection for IPv6 Measurements: Benefits and Limitations of RIPE Atlas Tags*. Proceedings of the Applied Networking Research Workshop (ANRW '17), 1-7. https://doi.org/10.1145/3106328.3106334

**Thème** :
Mécanisme tagging RIPE Atlas (system tags + user tags) pour sélection fine vantage points, focus IPv6 dual-stack probes profiling

**Intérêt pour le mémoire** :
Quantification précise dual-stack probes RIPE Atlas (2017) : 2.3K probes (26%), 88 pays, 822 ASNs, 83% access networks, 782 homes. Révèle biais géographiques (91% RIPE+ARIN), sous-représentation IPv6 (BE 57.4% users mais 2.8% probes, JP 19.8% users mais 1.4% probes). User tags stales (2.8% hosts update) vs system tags automatiques (updated every 4h). Méthodologie sélection vantage points applicable pour notre étude géographique DNS.

---

## Contexte de lecture

**Date de lecture** : 21 mars 2026
**Section du mémoire** :
- Section 2.5 (RIPE Atlas - tagging mechanism, vantage points selection)
- Section 7 (Discussion - geographic bias, probe distribution)

---

## Contenu de l'article

### Objectif(s) / Question(s) de recherche

**Problème** : Sélection vantage points RIPE Atlas **limitée** avant tags :
- Geographic filters (lat/lon) : coarse-grained
- Network prefix filters (AS, IP) : pas de capacité fine-grained (IPv4 vs IPv6, access technology, etc.)
- **Challenge** : profiler probes selon capacités réseau (dual-stack, IPv6 works, etc.)

**Innovation RIPE Atlas** (July 2014) : **Tagging mechanism**
- **System tags** : automatiques, basés sur mesures built-in (updated every 4h)
- **User tags** : manuels, dépendent participation hosts

**Questions de recherche** :
1. System tags vs user tags : **stabilité, précision** ?
2. **Dual-stack probes** : combien, où (regions), quels networks ?
3. **Geographic bias** : distribution reflète-t-elle IPv6 user population ?
4. **Access technology** : DSL vs cable vs fiber ?
5. **IPv6 performance** : comparable IPv4 ?

**Objectif paper** :
- Profile **ALL dual-stacked RIPE Atlas probes** (2017)
- Quantify **region-based** and **network-based** diversity
- Identify **underrepresented** countries (IPv6 users vs probes)
- Validate system tags usefulness vs user tags limitations

### Méthodologie

- **Type d'étude** : Analyse platform-wide RIPE Atlas metadata + active measurements
- **Échelle** :
  - **9.1K probes** connected (January 2017), 20.7K registered total
  - **2.3K dual-stacked probes** (25.99% connected non-anchored)
  - **88 countries**, **822 ASNs**

- **Outils utilisés** :
  - **RIPE Atlas Probe Archive API** [1] : probe metadata since March 2014
  - **RIPE Atlas Probe API** [4] : current probe status, tags, geolocation
  - **RIPE Data API** [25] : RIR mapping (WHOIS lookups)
  - **PeeringDB** [30] : AS network type classification
  - **APNIC dataset** [28] : IPv6 user population estimates

- **Protocole** :

**1. System tags analysis** (Section III) :
- Extract probe archive API (Mar 2014 - Jan 2017)
- Timeseries top 10 system tags
- Distribution all system tags across connected probes

**2. Dual-stack definition** :
- Probes tagged `system-ipv4-works` **AND** `system-ipv6-works`
- **Same ASN** over IPv4 and IPv6 (filters out 6in4 tunnels like Hurricane Electric)
- Ensures **native connectivity** both protocols

**3. Region-based analysis** (Section IV) :
- Map IP endpoint → RIR allocation (RIPE Data API + WHOIS)
- Cluster probes by RIR region
- Split by country (probe host registration + auto-geolocation)
- Correlation: % dual-stack probes vs % IPv6 users (APNIC dataset)

**4. Network-based analysis** (Section V) :
- Cluster probes by origin AS
- Map ASN → network type (PeeringDB) : ISP, content, university, IXP, NIC
- **Residential probes identification** :
  - Provision one-off traceroutes to RIPE Atlas anchors (ICMP Paris probing)
  - Residential = hop1 private IPv4 (RFC1918), hop2 public IPv4
  - Eliminates business lines (multiple NAT hops)

**5. Access technology classification** :
- DSL, cable, fiber
- Heuristic : UPnP discovery (WAN interface gateway)
- Validation : known ISP deployment patterns

**6. IPv6 performance** :
- Latencies IPv6 vs IPv4 to RIPE Atlas anchors
- Comparison RTT distributions

**7. User tags analysis** (Section VI) :
- Extract user tags updates history
- % probe hosts updating tags
- Staleness assessment

### Résultats principaux

#### 1. System tags overview (Section III, Figures 2-3)

**Top 10 system tags** (Jan 2017, sorted by # connected probes) :

| System tag | # Probes | Description |
|------------|----------|-------------|
| `system-ipv4-capable` | 9,045 | IPv4 interface exists |
| `system-ipv4-works` | 8,743 | IPv4 connectivity works |
| `system-resolves-a-correctly` | 8,305 | DNS A records resolved |
| `system-resolves-aaaa-correctly` | 8,236 | DNS AAAA records resolved |
| `system-ipv4-rfc1918` | 6,715 | Behind NAT (private IPv4) |
| `system-v3` | 6,660 | Hardware version 3 |
| `system-ipv6-capable` | 3,640 | IPv6 interface exists |
| `system-ipv6-works` | 3,050 | IPv6 connectivity works |
| `system-v2` | 1,427 | Hardware version 2 |
| `system-v1` | 767 | Hardware version 1 |

**Other tags** :
- `system-ipv6-doesnt-work` : 501
- `system-ipv6-ula` : 433 (ULA addresses)
- `system-resolver-mangles-case` : 407 (DNS case mangling for security)
- `system-doesnt-resolve-aaaa` : 142
- `system-ipv4-doesnt-work` : 63
- `system-dns-problem-suspected` : 1
- `system-firewall-problem-suspected` : (mentioned, count not shown)

**Insights** :
- **IPv6 capable** (3,640) > **IPv6 works** (3,050) : gap = 590 probes
  - Bortzmeyer 2013 : 10% probes believe IPv6 but fail measurements
  - Tags `*-works` = more accurate than `*-capable`
- **IPv4 works** (8,743) >> **IPv6 works** (3,050) : 2.9× difference
- Hardware versions : v3 (6,660) > v2 (1,427) > v1 (767)
  - Previous study [19, 20] : v1/v2 load issues (hardware limitations)

#### 2. Dual-stack probes evolution (Section III, Figure 4)

**Definition** : `system-ipv4-works` AND `system-ipv6-works` AND same ASN IPv4/IPv6

**Evolution** (August 2014 - January 2017) :
- **Aug 2014** : ~500 dual-stack probes
- **Jan 2017** : **2,301 dual-stack probes** (25.99% of 8,855 connected non-anchored)

**Growth** : ~4.6× en 2.5 ans

**Comparison** :
- RIPE Atlas dual-stack : **2,301** (Jan 2017)
- CAIDA Ark dual-stack : **77** out of 170 total (Jan 2017)
- → RIPE Atlas = **30× more** dual-stack vantage points than Ark

#### 3. Region-based analysis (Section IV)

**RIR distribution** (Figure 5) :

| RIR | # Probes | % |
|-----|----------|---|
| **RIPE** | 1,489 | 64.7% |
| **ARIN** | 606 | 26.3% |
| APNIC | 106 | 4.6% |
| LACNIC | 30 | 1.3% |
| AFRINIC | 30 | 1.3% |

**Insight** : **91%** dual-stack probes dans RIPE + ARIN (Europe + North America)

**Country distribution** (Figure 6, top 20) :

| Country | # Probes | % |
|---------|----------|---|
| **DE** (Germany) | 489 | 21.3% |
| **US** (United States) | 343 | 13.2% |
| **FR** (France) | 304 | 10.8% |
| **GB** (United Kingdom) | 248 | 7.0% |
| **NL** (Netherlands) | 161 | 6.6% |
| **CH** (Switzerland) | 151 | 3.8% |
| **BE** (Belgium) | 88 | 2.8% |
| **CZ** (Czech Republic) | 65 | 2.3% |
| **RU** (Russia) | 53 | 2.2% |
| **CA** (Canada) | 51 | 1.9% |
| NO (Norway) | 44 | 1.8% |
| AT (Austria) | 42 | 1.4% |
| FI (Finland) | 33 | 1.4% |
| GR (Greece) | 32 | 1.4% |
| **JP** (Japan) | 32 | 1.4% |
| SE (Sweden) | 31 | 1.3% |
| IT (Italy) | 31 | 1.3% |
| AU (Australia) | 31 | ... |
| DK (Denmark) | 25 | ... |
| SI (Slovenia) | 24 | ... |
| **OTHERS** | 23 | 14.9% |

**Total** : **88 countries**

**Geographic bias identification** (Figure 7) :

**Correlation % IPv6 users (APNIC) vs % dual-stack probes** :

**Top 10 underrepresented countries** :

| Country | IPv6 users % | Probes % | Delta | # IPv6 users (est.) |
|---------|--------------|----------|-------|---------------------|
| **BE** (Belgium) | **57.4%** | **2.8%** | **-54.6 pp** | ~6M |
| LU (Luxembourg) | 34.2% | 0.6% | -33.6 pp | ~200K |
| **GR** (Greece) | 33.7% | 1.4% | -32.3 pp | ~3.7M |
| CH (Switzerland) | 34.3% | 3.8% | -30.5 pp | ~2.9M |
| PT (Portugal) | 29.2% | 0.7% | -28.5 pp | ~3.1M |
| **IN** (India) | 22.0% | 0.1% | **-21.9 pp** | **~290M** |
| US (United States) | 33.2% | 13.2% | -20.0 pp | ~108M |
| EC (Ecuador) | 18.8% | 0.1% | -18.7 pp | ~3.2M |
| DE (Germany) | 39.9% | 21.3% | -18.6 pp | ~33M |
| **JP** (Japan) | **19.8%** | **1.4%** | **-18.4 pp** | **~22M** |

**Insight majeur** :
- **BE** : leader IPv6 adoption (57.4%, Google stats Jan 2017), mais seulement 88 probes (2.8%)
- **JP** : 22M IPv6 users (19.8% penetration), mais seulement 32 probes (1.4%)
- **IN** : 290M IPv6 users (largest absolute number), mais seulement ~2-3 probes (0.1%)
- → **Severe geographic bias** : probe deployment ≠ IPv6 user population

#### 4. Network-based analysis (Section V)

**AS distribution** (Figure 8, top 20) :

| ASN | Name | # Probes | % |
|-----|------|----------|---|
| AS3320 | DTAG (Deutsche Telekom) | 181 | 8.3% |
| AS7922 | COMCAST | 169 | 7.7% |
| AS12322 | PROXAD (Free, France) | 96 | 4.4% |
| AS3265 | XS4ALL (Netherlands) | 71 | 3.2% |
| AS3215 | Orange France | 71 | 3.2% |
| AS6830 | LGI (Liberty Global) | 32 | 1.5% |
| AS31334 | Kabel Deutschland | 32 | 1.5% |
| AS20712 | ... | 28 | 1.3% |
| AS5607 | BSKYB (UK) | 27 | 1.2% |
| AS5432 | BELGACOM (Belgium) | 25 | 1.1% |
| AS3303 | SWISSCOM | 23 | 1.1% |
| AS6848 | TELENET (Belgium) | 21 | 1.0% |
| AS7018 | AT&T | 19 | 0.9% |
| **OTHERS** | (many) | 49.6% | ... |

**Total** : **822 ASNs**

**Network type classification** (Figure 9, via PeeringDB) :

| Network type | # Probes | % (of mapped) |
|--------------|----------|---------------|
| **ISP/NSP** | **1,540** | **83%** |
| Content providers | ... | ... |
| Universities | ... | ... |
| IXPs | ... | ... |

**Mapping coverage** : 80.7% probes mapped (19.3% missing in PeeringDB)

**Insight** : **83% dual-stack probes in ISP/NSP** → ideal for measuring native IPv6 ISP performance

**Residential probes identification** (Figure 10) :

**Heuristic** : hop1 = private IPv4 (RFC1918), hop2 = public IPv4

**Results** :
- **782 residential dual-stack probes** (60.5% of ISP-hosted 1,540)
- 782 homes avec native IPv6 connectivity

**Access technology breakdown** :

| Technology | # Probes | % |
|------------|----------|---|
| **DSL** | ~260 | ~33% |
| **Cable** | ~260 | ~33% |
| **Fiber** | ~260 | ~33% |

**Even split** across DSL, cable, fiber

**IPv6 vs IPv4 latency** :
- Traceroutes to RIPE Atlas anchors
- **IPv6 latencies comparable to IPv4**
- **IPv4 marginally better** (few ms)
- No significant inflation IPv6

#### 5. User tags analysis (Section VI)

**Key finding** :
- **Only 2.8% probe hosts** ever update their user tags
- **Manual process** = dependency on host proactive participation
- → **Staleness problem** : user tags do not reflect current network situation

**System tags advantages** :
- **Automatically assigned** (no host action needed)
- **Frequently updated** (every 4 hours)
- **Stable and accurate** (derived from continuous built-in measurements)

**Implication** :
- **System tags >> user tags** for vantage point selection
- User tags may be outdated, unreliable
- Future studies should prioritize system tags

### Conclusion des auteurs

**Contributions** :
1. ✅ **First comprehensive profiling** all dual-stacked RIPE Atlas probes (2017)
2. ✅ **Quantification** : 2.3K probes (26%), 88 countries, 822 ASNs
3. ✅ **Geographic bias identified** : 91% RIPE+ARIN, underrepresentation BE/JP/IN
4. ✅ **Network diversity** : 83% ISP, 782 homes, even split DSL/cable/fiber
5. ✅ **IPv6 performance** : comparable IPv4 (marginally better IPv4)
6. ✅ **System tags validation** : stable, accurate, updated every 4h
7. ✅ **User tags limitation** : only 2.8% hosts update → staleness

**Key findings** :

**RIPE Atlas = richest IPv6 measurement platform** :
- 2.3K dual-stack > CAIDA Ark 77 dual-stack (30×)
- 88 countries, 822 ASNs
- 782 residential probes native IPv6

**Geographic bias severe** :
- 91% probes Europe + North America
- BE 57.4% IPv6 users but 2.8% probes
- JP 22M IPv6 users but 1.4% probes
- Need more probes underrepresented countries

**Network diversity good** :
- 83% ISP-hosted
- 60.5% residential (782 homes)
- Even split access technologies (DSL/cable/fiber)

**System tags >> user tags** :
- Auto-assigned, updated 4h
- User tags stale (2.8% hosts update)

**Implications** :
- **Researchers** : use system tags for vantage point selection
- **RIPE Atlas** : deploy more probes BE, JP, IN (underrepresented)
- **IPv6 studies** : RIPE Atlas = best platform (2.3K dual-stack)

**Limitations** :
- Snapshot Jan 2017 (évolution since ?)
- PeeringDB mapping 80.7% (19.3% missing)
- Residential heuristic excludes multi-NAT, no-NAT homes (coverage vs accuracy trade-off)

---

## Analyse personnelle

### Que garder pour le mémoire

**Concepts clés** :
- **System tags** = vantage point selection fine-grained (IPv4-works, IPv6-works, etc.)
- **Dual-stack definition** : same ASN IPv4/IPv6 (filters tunnels)
- **Geographic bias** : probe deployment ≠ IPv6 user population
- **Residential probes** : hop1 private, hop2 public (782 homes native IPv6)
- **User tags staleness** : 2.8% hosts update (manual process unreliable)

**Chiffres essentiels** :
- **2,301 dual-stack probes** (25.99% connected, Jan 2017)
- **88 countries**, **822 ASNs**
- **91%** probes RIPE + ARIN regions
- **83%** probes ISP/NSP networks
- **782 residential** dual-stack (DSL/cable/fiber even split)
- **BE** : 57.4% IPv6 users, 2.8% probes (-54.6 pp)
- **JP** : 19.8% IPv6 users, 1.4% probes (22M users, 32 probes)
- **IN** : 22% IPv6 users, 0.1% probes (290M users, ~2-3 probes)
- **2.8%** probe hosts update user tags
- System tags updated **every 4 hours**
- RIPE Atlas **30×** more dual-stack than CAIDA Ark (2,301 vs 77)

**Méthodes applicables** :
- System tags vantage point selection (filter by capabilities)
- RIR/country mapping via RIPE Data API + WHOIS
- AS classification via PeeringDB
- Residential probes identification (traceroute heuristic)
- IPv6 user population correlation (APNIC dataset)

**Limites pour nous** :
- Étude Jan 2017 (7 ans) → RIPE Atlas now 12.9K probes (Nosyk 2024)
- Dual-stack % evolved ? (26% → ?)
- Geographic bias improved ? (BE, JP, IN more probes ?)
- User tags still stale ?

### Critique personnelle

**Forces** :
- ✅ **Comprehensive profiling** : ALL dual-stack probes analyzed (not sample)
- ✅ **Multi-dimensional** : region + network + access technology
- ✅ **Actionable** : identifies underrepresented countries (BE, JP, IN)
- ✅ **Validation** system tags (vs user tags staleness)
- ✅ **Rigorous heuristics** : residential probes, access technology
- ✅ **Correlation external data** : APNIC IPv6 users, PeeringDB
- ✅ **Honest limitations** : PeeringDB coverage, heuristic trade-offs

**Faiblesses** :
- ⚠️ **Snapshot Jan 2017** : no temporal evolution (how bias changed ?)
- ⚠️ **Residential heuristic** : excludes multi-NAT, no-NAT (accuracy vs coverage)
- ⚠️ **PeeringDB mapping** : 19.3% probes unmapped (missing AS data)
- ⚠️ **IPv6 performance light** : latency comparison brief (no deep analysis)
- ⚠️ **No user tags deep dive** : mentions 2.8% but no staleness examples
- ⚠️ **No recommendations** : how to incentivize probes underrepresented countries ?

**Lien avec autres articles** :

- **Nosyk 2024 (RIPE Atlas DITL)** :
  - Bajpai 2017 : 9.1K probes total, 2.3K dual-stack (26%)
  - Nosyk 2024 : 12.9K probes total, dual-stack % not reported
  - Geographic bias persistent ? (Nosyk : DE+US = 28% vantage points)
  - Validation : geographic bias still exists 2024

- **Holterbach 2015 (Interference)** :
  - Holterbach : hardware v1/v2 load issues (timing delays)
  - Bajpai : confirms v1 (767), v2 (1,427) < v3 (6,660)
  - System tags enable hardware-based calibration (filter old probes)

- **Boswell 2024 (Internal Names)** :
  - Boswell : FRITZ!Box dominates Europe (geographic bias)
  - Bajpai : DE 21.3% probes (Deutsche Telekom, Kabel Deutschland)
  - Cohérence : Germany over-represented RIPE Atlas

- **Johnson 2016 (DNS Root)** :
  - Johnson : ~8K probes (2014), 189 countries
  - Bajpai : 9.1K probes (2017), 88 countries dual-stack
  - Evolution : total probes +14%, but dual-stack coverage < total

**Questions ouvertes** :
1. **Evolution 2017-2024** : Dual-stack % now ? (26% → ?)
2. **Geographic bias improved** : BE, JP, IN more probes deployed ?
3. **User tags 2024** : Still 2.8% update rate ? Staleness worse ?
4. **IPv6 performance** : Deeper analysis latency, reachability ?
5. **System tags new** : Additional tags since 2017 ?
6. **Incentives** : How to attract probe hosts underrepresented countries ?

### Citations importantes

> "RIPE Atlas with ∼9.1K hardware probes (as of Jan 2017) is the largest open platform today. It plays a critical role in not only providing operational support to network operators but also facilitating measurement-based research." (Section II)

> "Around 25.99% (2301 / 8855) of all connected non-anchored probes are dual-stacked as of Jan 2017. To put numbers into perspective, this is more than the number of CAIDA Ark dual-stacked probes (77 out of 170 as of Jan 2017) with native IPv6 connectivity." (Section III)

> "∼91% of the dual-stacked probes are connected within the RIPE and ARIN region." (Section IV)

**Sur geographic bias** :
> "For instance, we know that Belgium with ∼48.5% penetration is currently leading IPv6 adoption rates (as of Jan 2017) according to Google IPv6 adoption statistics. However, it does not even fall within the top 5 countries with the largest number of dual-stacked probes. As such, the probe deployment likely does not reflect the dual-stacked user population across the globe." (Section IV)

> "It can be seen that JP with ∼19% IPv6 usage ratio and ∼22M IPv6 users serve only ∼1.4% (31/2301) dual-stacked probes. We hope this analysis will help improve the deployment of probes in such underrepresented countries with a large IPv6 userbase." (Section IV)

**Sur user tags** :
> "The accuracy of user tags on the other hand is largely dependent on the proactive participation of hosts to not only tag, but also update their tags as and when network environments around the probe change. This may therefore lead to stale user tags that do not reflect the current network situation of the probe. [...] We show that only ∼2.8% of probe hosts ever update their user tags." (Abstract + Section VI)

---

## Utilisation dans le mémoire

**Sections concernées** :
- **Section 2.5 (RIPE Atlas)** : Tagging mechanism, system tags, vantage point selection
- **Section 7 (Discussion)** : Geographic bias, probe distribution, limitations

**Points à développer** :

**État de l'art** :
- RIPE Atlas tags = fine-grained vantage point selection (beyond geo + AS filters)
- System tags automated (4h updates) >> user tags manual (2.8% hosts update)
- 2.3K dual-stack probes (2017) = richest IPv6 measurement source (30× CAIDA Ark)
- Geographic bias severe : 91% RIPE+ARIN, underrepresentation BE/JP/IN

**Notre contribution** :
- Bajpai 2017 : profiling dual-stack probes, identifies bias
- Notre approche : use system tags for DNS measurements vantage point selection
- Filter probes by capabilities (IPv4-works, IPv6-works, resolves-AAAA, etc.)
- Acknowledge geographic bias in results interpretation

**Discussion** :
- Geographic diversity DNS responses may reflect probe distribution bias
- 91% probes Europe+North America → results may not generalize globally
- Underrepresentation BE/JP/IN → limited coverage high-IPv6-adoption countries
- Trade-off : RIPE Atlas largest platform but geographic bias exists
- Compare Nosyk 2024 (12.9K probes) : bias improved or persistent ?

**Méthodologie** :
- Use system tags for probe selection (avoid user tags staleness)
- Document probe distribution (countries, ASNs) for transparency
- Acknowledge limitations geographic coverage
- Consider weighting results by IPv6 user population (APNIC)

**Limitations** :
- Geographic bias inherent RIPE Atlas (not our fault, but must acknowledge)
- 91% probes RIPE+ARIN → limited global representativeness
- Underrepresented countries results less reliable

---

**Tags** : #ripe-atlas #system-tags #user-tags #vantage-points #ipv6 #dual-stack #geographic-bias #residential-probes #access-technology #probe-selection

**Statut** : [X] Lu (PDF via MD) / [X] Fiché / [ ] Intégré mémoire

**Date fiche** : 21 mars 2026
