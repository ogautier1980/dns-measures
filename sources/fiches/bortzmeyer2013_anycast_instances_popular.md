# Reading Note - Using RIPE Atlas to Find the Most Popular Instances of a DNS Anycast Name Server

**Bibliographic Reference**:
Bortzmeyer, S. (2013, May 3). Using RIPE Atlas to Find the Most Popular Instances of a DNS Anycast Name Server. *RIPE Labs*. https://labs.ripe.net/author/stephane_bortzmeyer/using-ripe-atlas-user-defined-measurements-to-find-the-most-popular-instances-of-a-dns-anycast-name-server/

**Theme**:
This practitioner article describes an early application of RIPE Atlas user-defined measurements to characterize the anycast instance distribution of d.nic.fr, the .fr TLD's anycast authoritative name server. Using the NSID option (RFC 5001) on approximately 500 IPv4 and IPv6 probes across six measurement runs, the author maps which physical anycast instances receive DNS queries from different world regions, revealing counter-intuitive BGP routing patterns including transatlantic routing and significant IPv4/IPv6 divergence.

**Relevance to thesis**:
This article is one of the earliest documented uses of RIPE Atlas for anycast DNS instance characterization, establishing the NSID-based methodology that subsequent work (Finnegan 2018, Edgecast 2017) has built upon. The BGP attraction basin concept and the IPv4/IPv6 routing divergence finding are directly relevant to our thesis's analysis of geographic variation in DNS responses. The Python code approach via the RIPE Atlas REST API previews the programmatic methodology we will use.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.4 (RIPE Atlas: early DNS measurement applications)
- Section 2.5 (Anycast DNS: BGP routing and geographic variation)
- Section 4 (Methodology: NSID-based anycast instance tracking)

---

## Article Content

### Research Objective(s)

**Problem**: For the .fr TLD authoritative name server (d.nic.fr), which is deployed as an anycast service across multiple global instances, it is not known which instance receives the most queries from different world regions, nor whether IPv4 and IPv6 routing produce consistent instance selection. Traditional monitoring tools cannot answer this because anycast is transparent to the DNS client — all instances share the same IP address.

**Research questions**:
1. Which anycast instances of d.nic.fr receive the highest traffic share globally, and does the distribution differ by world region?
2. Do IPv4 and IPv6 routing produce consistent anycast instance selection, or do they exhibit significant divergence?
3. Does the geographic location of a probe predict its anycast instance routing, or do BGP attraction basins create counter-intuitive transatlantic routing patterns?

### Background

DNS anycast uses a single globally announced IP address with BGP routing directing each query to the "closest" instance as defined by BGP path selection — not geographic proximity. The .fr TLD operates its authoritative name server (d.nic.fr) as an anycast service with instances in multiple cities (Paris, Frankfurt, and others). The NSID option (RFC 5001) was designed to allow operators to identify which name server instance responded, by including a server-defined identifier string in the DNS response's OPT record. RIPE Atlas, at the time of writing in 2013, had grown to approximately 5,000 probes — fewer than today's 12,900 but sufficient for regional characterization. This article represents an early exploration of user-defined DNS measurements on RIPE Atlas.

### Methodology

- **Study type**: Empirical active measurement, exploratory
- **Tools used**: RIPE Atlas (user-defined DNS measurements), RIPE Atlas REST API (Python), NSID option (RFC 5001)
- **Scale**: 6 measurement runs; approximately 500 probes per run (IPv4 and IPv6 separately); global coverage with regional breakdowns (North America, Asia-Pacific, Europe)
- **Measurement protocol**: Each probe sends a DNS query to d.nic.fr's anycast IP with the NSID option enabled. The response OPT record contains an NSID string identifying the responding instance (e.g., "dns.th2.nic.fr" for Paris, "dns.fra.nic.fr" for Frankfurt). Results are retrieved via the RIPE Atlas REST API and aggregated by world region and protocol (IPv4/IPv6). Python code was written to retrieve and parse results.
- **Data collected**: Per-probe NSID string (anycast instance identifier), probe geographic location (country/region), protocol (IPv4 or IPv6), aggregated into percentage share per instance per region

### Main Results

1. **Global IPv4 distribution**: The Paris instance (dns.th2.nic.fr) and Frankfurt instance (dns.fra.nic.fr) each receive approximately 36% of global IPv4 queries, making them co-dominant globally, with remaining instances sharing the other 28%.
2. **North America counter-intuitive routing**: Despite geographic distance, the Paris instance receives approximately 55% of North American IPv4 queries, and Frankfurt receives 33%. North American probes are predominantly routed to European instances rather than any local or transatlantic alternative — a clear demonstration of BGP attraction basins overriding geographic proximity.
3. **Asia-Pacific routing**: The Paris instance receives approximately 38% of Asia-Pacific IPv4 queries and Frankfurt approximately 32%, again showing European instance dominance even for Pacific-region probes.
4. **IPv4/IPv6 divergence**: IPv6 shows a markedly different distribution: Frankfurt receives 36% of global IPv6 queries compared to only 17% for Paris — the order of dominance reverses between protocols. This significant divergence indicates that IPv4 and IPv6 BGP routing for the same anycast service can produce substantially different traffic distributions.
5. **BGP attraction basins as the explanatory mechanism**: The routing patterns cannot be explained by geographic proximity alone. BGP path selection, peering agreements, and the specific prefix announcements made by each instance determine which probes are "attracted" to which instance. The same physical network can route IPv4 and IPv6 traffic to different continents.

### Authors' Conclusion

The RIPE Atlas + NSID methodology enables precise, regionally disaggregated characterization of anycast DNS instance traffic distribution. The results for d.nic.fr reveal that BGP attraction basins create large-scale routing patterns that are counter-intuitive from a geographic standpoint — North American and Asia-Pacific probes predominantly reach European instances. The IPv4/IPv6 divergence finding (Paris dominant in IPv4, Frankfurt in IPv6) is particularly significant, suggesting that dual-stack measurement is essential for accurate anycast characterization. The availability of Python code and the RIPE Atlas REST API makes this methodology accessible and reproducible.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- BGP attraction basins: the geographic regions whose traffic is attracted to a specific anycast instance, determined by BGP topology rather than physical proximity; instances can attract traffic from distant continents
- IPv4/IPv6 anycast divergence: the same anycast service can route IPv4 and IPv6 traffic to different instances; dual-stack measurement is required to capture the full picture
- NSID (RFC 5001) as the primary anycast instance identification mechanism in active DNS measurements
- Regional disaggregation of results: global percentages mask regional routing patterns; results must be broken down by continent/region to reveal BGP attraction effects

**Applicable methods**:
- Include NSID option in all RIPE Atlas DNS measurements targeting anycast services (authoritative name servers, public resolvers) to track which instance responds per probe per query
- Run IPv4 and IPv6 measurements separately and compare to detect divergence — important for both our anycast analysis and the general IPv6 adoption dimension of our thesis
- Aggregate results by geographic region (continent, country) rather than reporting only global averages
- Use Python + RIPE Atlas REST API as the standard programmatic interface for retrieving and processing measurement results

**Important statistics**:
- Paris (th2): 36% globally (IPv4), Frankfurt (fra): 36% globally (IPv4)
- North America IPv4: Paris 55%, Frankfurt 33% (counter-intuitive)
- Asia-Pacific IPv4: Paris ~38%, Frankfurt ~32%
- IPv6 global: Frankfurt 36%, Paris 17% (order reversal vs. IPv4)
- 6 measurement runs, ~500 probes each

**Identified limitations (gaps to fill)**:
- Static snapshot: six measurement runs provide a point-in-time view; BGP topology changes over time would alter catchment boundaries — longitudinal tracking (our thesis's temporal dimension) would capture this evolution
- No latency measurement: the article identifies which instance responds but not the RTT, leaving the performance implications of BGP routing patterns unmeasured
- 500 probes in 2013 vs. 12,900 probes today: the methodology is more powerful with current RIPE Atlas infrastructure

### Personal Critique

**Strengths**:
- Pioneer work: one of the first documented uses of RIPE Atlas for anycast DNS instance characterization, establishing a methodology still in use today
- Clean and reproducible methodology: NSID + RIPE Atlas REST API + Python is a minimal, well-defined approach
- Surprising findings: the North American routing to Paris and the IPv4/IPv6 divergence are counterintuitive and empirically important
- Accessible to practitioners: the article explains BGP attraction basins intuitively without requiring deep BGP expertise

**Weaknesses**:
- Blog post format: no statistical confidence intervals, no discussion of probe representativeness or measurement bias
- Only one anycast service measured (d.nic.fr): the findings may not generalize to other anycast DNS services with different PoP deployments and peering strategies
- No temporal analysis: BGP routing is dynamic; the results represent a moment that may not be stable

**Links to other papers**:
- Finnegan 2018 (RIPE Atlas anycast DNS): directly extends this methodology with a larger probe set and a practical IXP use case, adding "id.server" CHAOS queries as an alternative to NSID
- Edgecast 2017 (RIPE Atlas CDN catchment): industrial-scale extension with a scoring framework for PoP optimization, building on the same anycast characterization principle
- Nosyk et al. 2024 (RIPE Atlas DITL): provides current platform scale data (12,900 probes vs. ~5,000 in 2013) that would amplify the resolution of this methodology today

**Open questions**:
- Has the .fr TLD anycast distribution changed substantially since 2013 as AFNIC has added or reconfigured PoPs?
- Does the IPv4/IPv6 divergence pattern hold across other TLD anycast name servers, or is it specific to d.nic.fr's peering configuration?
- Can BGP attraction basin boundaries be correlated with specific IXP peering relationships to explain the routing patterns mechanistically?

### Key Quotes

> "BGP attraction basins determine traffic distribution independently of geographic proximity."

> "Despite geographic distance, the Paris instance receives approximately 55% of North American IPv4 queries — a clear demonstration of BGP attraction basins overriding geographic proximity."

> "IPv6 shows a markedly different distribution: Frankfurt receives 36% of global IPv6 queries compared to only 17% for Paris — the order of dominance reverses between protocols."

> "The same physical network can route IPv4 and IPv6 traffic to different continents."

---

## Use in Thesis

**Relevant sections**:
- Section 2.5 (Anycast DNS): Use BGP attraction basin concept and IPv4/IPv6 divergence finding to explain why geographic DNS variation requires empirical measurement rather than assumption
- Section 2.4 (RIPE Atlas history): Cite as an early seminal use of RIPE Atlas for DNS anycast characterization
- Section 4 (Methodology): Justify NSID inclusion in measurements; justify separate IPv4 and IPv6 measurement runs; justify regional rather than global result aggregation

**Points to develop**:
- Contrast 2013 probe count (~500) with current count (12,900) to show how RIPE Atlas has matured as a measurement infrastructure since the methodology was established
- Use the North America to Paris routing result as a motivating example of why geographic proximity assumptions fail in DNS measurement

**Cross-references**:
- Fiche Finnegan 2018: extension of the same methodology with larger scale and "id.server" alternative
- Fiche Edgecast 2017: industrial application of anycast catchment analysis with a scoring framework

---

**Tags**: #anycast #dns #ripe-atlas #nsid #bgp #attraction-basins #ipv6 #geographic-routing #fr-tld #afnic
**Status**: [X] Read / [X] Filed
