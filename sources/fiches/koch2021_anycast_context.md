# Reading Note - Anycast in Context: A Tale of Two Systems

**Bibliographic Reference**:
Koch, T., Li, K., Ardi, C., Katz-Bassett, E., Calder, M., & Heidemann, J. (2021). Anycast in context: A tale of two systems. In *Proceedings of the 2021 ACM SIGCOMM Conference (SIGCOMM '21)* (pp. 398–417). ACM. https://doi.org/10.1145/3452296.3472891

**Theme**:
This paper provides the largest comparative study of anycast latency and routing inflation to date, examining two contrasting use cases: the DNS root server system and Microsoft's global anycast CDN. The authors demonstrate that while routing inflation affects more than 95% of users reaching root DNS, aggressive caching makes this largely imperceptible to end users; conversely, Microsoft's CDN experiences much less inflation (only 35% of users) because latency directly affects user experience and motivates extensive engineering investment.

**Relevance to thesis**:
Anycast is the dominant deployment strategy for DNS root and TLD servers, and understanding anycast inflation is essential for interpreting geographic variability in DNS response times in our thesis. The paper's finding that root DNS inflation is widespread but practically irrelevant (due to caching) provides important context for evaluating whether DNS round-trip time variation across RIPE Atlas probes reflects real geographic routing differences or merely anycast routing inefficiency.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.4 (Anycast and DNS infrastructure)
- Section 2.4.4 (Alternatives and limitations of RIPE Atlas for anycast studies)
- Section 4.x (Interpretation of geographic DNS latency variation)

---

## Article Content

### Research Objective(s)

**Problem**: Prior work, notably the SIGCOMM 2018 paper "Internet Anycast: Performance, Problems & Potential", argued that anycast inflates latency by hundreds of milliseconds and is therefore inefficient. However, those conclusions were drawn primarily from measurements of root DNS — a system where caching means users rarely wait for DNS responses. The question of whether inflation is inherent to anycast, or is a consequence of the specific application context, remained unanswered.

**Research questions**:
1. How prevalent is anycast routing inflation in the root DNS system, and does it translate into actual user-perceived latency overhead?
2. Is anycast inflation reduced or eliminated in a latency-sensitive CDN application (Microsoft's CDN), and if so, how?

### Background

IP anycast assigns the same IP address to geographically distributed servers. Border Gateway Protocol (BGP) routing determines which physical server a client reaches, based on route preference and topology — not necessarily the geographically or topologically closest site. The DNS root comprises 13 letter servers operated by 12 organisations; as of July 2021, each letter deploys between 6 and 254 anycast sites worldwide. Root DNS records have long TTLs (typically 518,400 seconds / 6 days), enabling recursive resolvers to cache results and serve user queries without contacting the root for extended periods. Microsoft's CDN serves web content (latency-sensitive) to over a billion users from more than 100 front-end sites organised into "rings" of different sizes. Unlike root DNS, every CDN miss involves multiple RTTs to the front-end, making latency directly relevant to user experience.

### Methodology

- **Study type**: Large-scale measurement study (combining packet captures, server logs, client-side instrumentation, and RIPE Atlas supplementary probing)
- **Tools used**: DNS-OARC DITL (Day in the Life of the Internet) packet captures at root servers; Microsoft server-side front-end logs (TCP handshake RTTs); Microsoft client-side measurement system (HTTP image fetch latency); RIPE Atlas (7,000 pings from 1,000 probes to CDN rings for calibration); APNIC Internet population data; ISI/USC local packet captures (approximately 100 million queries, 2018)
- **Scale**: 51.9 billion daily root DNS queries (after filtering); over one billion Microsoft CDN users; 22,243 ASes covered; 224 countries/regions; 2018 DITL captures (48 hours, 12 of 13 root letters)
- **Measurement protocol**: Inflation was measured in two ways: (1) geographic inflation — comparing the distance to the actually assigned root letter site against the distance to the closest deployed site; (2) latency inflation — comparing measured TCP handshake RTTs (from TCP DNS queries) against a lower bound derived from the closest known site. Root DNS query volumes were joined with Microsoft user counts at the recursive resolver /24 level to estimate per-user root DNS query rates. CDN latency was measured directly from server logs and client instrumentation.
- **Data collected**: Root DNS query volumes per recursive (/24); TCP handshake RTTs for DNS-over-TCP queries to root servers; client-to-CDN HTTP latency; RIPE Atlas ping RTTs to CDN rings

### Main Results

1. **Root DNS inflation is nearly universal**: More than 95% of users experience some geographic inflation when querying at least one root letter, and up to 40% of users experience more than 100 ms of inflation to some root letters. When averaged across all root letters (exploiting the fact that recursives preferentially query their best-performing letter), only 10% of users experience more than 100 ms of inflation.
2. **Root DNS inflation is practically irrelevant to users**: Because root DNS records are cached at recursive resolvers with TTLs measured in days, most users interact with the root DNS approximately once per day. The additional latency from inflation is amortised over thousands of cached responses, making its per-query cost negligible.
3. **CDN anycast inflation is much lower**: Only 35% of Microsoft CDN users experience any inflation, and the amounts are smaller than for root DNS. This is attributed to extensive peering agreements and deliberate engineering by Microsoft to minimise BGP path length.
4. **Hypothetical CDN inflation would be catastrophic for UX**: The paper estimates that if Microsoft's CDN were as inflated as individual root letters, each page load would incur hundreds of milliseconds of additional latency — confirming that the low CDN inflation is the product of active optimisation, not a coincidence.
5. **Deployment size and inflation trade-off**: Inflation increases with the number of anycast sites in a deployment — larger deployments are harder to optimise through peering alone. This creates a tension between geographic coverage (which requires more sites) and routing efficiency.

### Authors' Conclusion

The authors conclude that prior claims of anycast inefficiency reflect measurements of a single application (root DNS) in a context where inflation barely matters to users (due to caching), rather than a fundamental limitation of anycast technology. When anycast is used for latency-sensitive applications (CDNs), economically incentivised operators invest in peering and engineering to reduce inflation to acceptable levels. The key lesson is that anycast performance must be evaluated in the context of the specific application and service model — abstract measurements of routing inflation are insufficient without understanding user interaction patterns and caching behaviour.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- Distinction between geographic inflation (site assignment vs closest site) and latency inflation (measured RTT vs lower bound)
- Caching as the dominant factor that decouples root DNS latency from user-perceived performance — highly relevant to interpreting DNS timing measurements from Atlas probes
- The dependence of anycast routing quality on the operator's peering investment and deployment size

**Applicable methods**:
- When analysing geographic variation in DNS response times from RIPE Atlas probes, compute both geographic and latency inflation relative to known anycast site locations
- Supplement RIPE Atlas measurements with DITL data or server-side captures for ground-truth comparison, as the authors do
- Account for caching TTLs when estimating the user-perceived impact of DNS timing differences across probe locations

**Important statistics**:
- More than 95% of users experience some geographic inflation in root DNS queries
- Up to 40% of users experience more than 100 ms inflation to some individual root letters
- Only 10% of users experience more than 100 ms when averaged across all root letters (best-letter selection)
- Only 35% of Microsoft CDN users experience any inflation
- 51.9 billion daily root DNS queries, of which approximately 31 billion are to non-existent domains (discarded)
- 7,000 RIPE Atlas ping measurements used for CDN calibration (1,000 probes, 3 measurements each to each ring)

**Identified limitations (gaps to fill)**:
- RIPE Atlas coverage is approximately 3,700 ASes as of July 2021, versus 22,243 ASes covered by DITL — Atlas substantially underrepresents the global Internet, which is a key limitation for anycast studies
- CDN data is proprietary (Microsoft); results cannot be independently reproduced for other CDNs
- The 2018 DITL data may not reflect current anycast deployments; root DNS has expanded significantly since then

### Personal Critique

**Strengths**:
- The largest anycast study to date in terms of query volume and user coverage
- The comparison between two very different anycast applications (root DNS vs CDN) provides a unique methodological contribution
- Reconciles apparently contradictory prior results by introducing application context as the key variable

**Weaknesses**:
- Relies on proprietary Microsoft CDN data; the CDN findings cannot be independently verified or reproduced
- The 2018 DITL data is used for a 2021 paper; more recent data would be more representative of current deployments
- RIPE Atlas is used only for calibration (7,000 pings) rather than as a primary measurement source — Atlas coverage limitations are acknowledged but not mitigated

**Links to other papers**:
- Holterbach et al. (2015): RIPE Atlas measurement interference — relevant because the 7,000 Atlas pings used here could be affected by concurrent probe load
- Johnson et al. (2016): Detects unauthorised anycast-like mirrors of root DNS — complements this paper's analysis of legitimate root anycast routing
- Hours et al. (2016): CDN routing is affected by DNS resolver choice; this paper examines the anycast routing layer, while Hours et al. examine the DNS resolver layer

**Open questions**:
- How does the anycast inflation picture change for TLD servers (e.g., .com, .org), which are between root DNS and CDNs in terms of latency sensitivity and caching behaviour?
- Does the inflation reduction in Microsoft's CDN hold for other CDNs (Cloudflare, Akamai, Fastly) with similar engineering resources?
- How does IPv6 anycast routing inflation compare to IPv4, given the different routing topology?

### Key Quotes

> "Anycast is used to serve content including web pages and DNS, and anycast deployments are growing. However, prior work examining root DNS suggests anycast deployments incur significant inflation, with users often routed to suboptimal sites."

> "We find that inflation is very common in root DNS, affecting more than 95% of users. However, we then show root DNS latency hardly matters to users because caching is so effective."

> "Perhaps because of this need [latency sensitivity], only 35% of CDN users experience any inflation, and the amount they experience is smaller than for root DNS."

> "A key takeaway from our work is that anycast must be analyzed in the context of the service in which it is used."

---

## Use in Thesis

**Relevant sections**:
- Section 2.4 (Anycast in DNS infrastructure): Cite as the definitive reference on anycast inflation in root DNS; use statistics on the prevalence and magnitude of inflation
- Section 2.4.4 (RIPE Atlas limitations for anycast studies): Cite the acknowledgment that Atlas covers only approximately 3,700 ASes versus 22,000+ in DITL, motivating the use of complementary data sources
- Section 4.x (Results — geographic DNS latency): Use the inflation framework to contextualise geographic variability in observed DNS response times

**Points to develop**:
- Discuss how caching TTLs at recursive resolvers affect the relevance of root DNS latency measurements from RIPE Atlas — and how this differs for TLD and authoritative server queries (shorter TTLs, more direct user impact)
- Use the inflation framework to ask whether geographic RTT differences observed in our measurements reflect true routing inefficiency or legitimate anycast routing behaviour

**Cross-references**:
- johnson2016_dns_root_manipulation.md (what "abnormal" anycast routing to root servers looks like)
- holterbach2015_ripeatlas_interference.md (limitations of RIPE Atlas as a measurement platform)
- cicalese2015_anycast_census.md (anycast census methodology — complements inflation analysis)

---

**Tags**: #anycast #dns-root #cdn #routing-inflation #latency #caching #ripe-atlas #microsoft-cdn #sigcomm
**Status**: [X] Read / [X] Filed
