# Reading Note - Seeing the World with RIPE Atlas

**Bibliographic Reference**:
Edgecast / Verizon Digital Media Services. (2017, December 8). Seeing the World with RIPE Atlas. *RIPE Labs*. https://labs.ripe.net/author/verizon_digital/seeing-the-world-with-ripe-atlas/

**Theme**:
This practitioner article describes how Edgecast (a commercial CDN operator, then part of Verizon Digital Media Services, now Edgio) uses RIPE Atlas traceroute measurements to optimize the geographic catchment of its anycast CDN Points of Presence (PoPs). The article introduces a structured methodology for probing anycast catchment via traceroutes, correlating penultimate hop information with internal BGP data, testing six grouping strategies for probes, and applying a normalized scoring framework to evaluate the impact of BGP route changes on client experience.

**Relevance to thesis**:
This article bridges the academic anycast DNS measurement methodology (Bortzmeyer 2013, Finnegan 2018) and the industrial CDN optimization context, showing how geographic DNS routing directly translates to user experience. The anycast catchment measurement methodology using RIPE Atlas traceroutes is directly applicable to our thesis's analysis of geographic variation in DNS responses. The scoring framework for measuring improvement or degradation provides a model for quantifying spatial DNS variation effects.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.5 (Anycast DNS and CDN geographic routing)
- Section 2.5.4 (CDN strategies and DNS geolocation)
- Section 4 (Methodology: geographic variation measurement framework)

---

## Article Content

### Research Objective(s)

**Problem**: Commercial CDN operators use anycast IP routing to direct client requests to the nearest PoP, but "nearest" is defined by BGP topology rather than geographic proximity. Without empirical measurement, operators cannot know which clients are routed to which PoP (the "catchment"), whether changes in BGP routing improve or degrade client experience across different networks, or which grouping of clients best captures homogeneous routing behavior.

**Research questions**:
1. How can RIPE Atlas traceroute measurements be used to map the anycast catchment of each CDN PoP?
2. Which client grouping strategy (country, AS, IP prefix, geolocation, BGP path, combinations) produces the most coherent and actionable catchment groups?
3. How can the impact of BGP route changes on CDN client experience be quantified in a normalized, comparable way?

### Background

Edgecast operates an anycast CDN where multiple PoPs share the same IP address block, with BGP routing directing clients to different PoPs depending on network topology. The set of clients routed to a given PoP is called its "catchment." Edgecast hosts 12 RIPE Atlas anchors within its network infrastructure, providing high-capacity measurement points with direct visibility into its own routing. RIPE Atlas probes outside Edgecast's network serve as representative client populations distributed across the Internet. The challenge of anycast catchment measurement is that clients cannot directly observe which PoP serves them — only network-level inference (traceroutes, BGP data) reveals the routing.

### Methodology

- **Study type**: Operational measurement study (industrial practitioner, not peer-reviewed)
- **Tools used**: RIPE Atlas (traceroute measurements from probes to Edgecast anycast addresses), internal BGP routing tables (Edgecast), RIPE Atlas anchor hosting (12 anchors in Edgecast PoPs)
- **Scale**: Global RIPE Atlas probe deployment; 12 Edgecast-hosted RIPE Atlas anchors; 6 probe grouping strategies tested; scoring framework applied across North American network
- **Measurement protocol**:
  1. RIPE Atlas probes perform traceroutes to Edgecast anycast IP addresses
  2. The penultimate hop of each traceroute (the last router before the Edgecast PoP) is correlated with Edgecast's internal BGP data to identify which PoP received the traffic
  3. RTT to each PoP is recorded per probe
  4. Probes are grouped using 6 strategies: by country, by Autonomous System (AS), by IP prefix, by geolocation, by BGP path, and by combinations thereof
  5. Grouping strategies are compared for within-group RTT consistency and group size manageability
  6. A scoring framework is applied: for each BGP route change, RTT improvements and degradations across probes are normalized via a logistic curve, weighted by estimated AS traffic importance, and aggregated into a score from +1 (uniform improvement) to -1 (uniform degradation)
- **Data collected**: Per-probe traceroute paths, penultimate hop IP, RTT to PoP, BGP next-hop per probe, geographic location per probe

### Main Results

1. **Penultimate hop as PoP identifier**: The penultimate hop of a traceroute from an external RIPE Atlas probe to an Edgecast anycast address reliably identifies which PoP served the request, when correlated with Edgecast's internal BGP topology. This is the key methodological contribution enabling catchment mapping without requiring any change to the DNS or CDN infrastructure.
2. **Geolocation-based grouping as optimal strategy**: Among the six tested grouping strategies, geolocation-based grouping provides the best trade-off between group size (sufficient probes per group for statistical validity), RTT consistency within groups (clients in the same geolocation group experience similar routing), and BGP path similarity. Country-level grouping is too coarse (merges probes with very different routing), while IP-prefix grouping is too fine-grained (groups with insufficient probe counts).
3. **Scoring framework normalizes heterogeneous impacts**: The logistic-curve normalization combined with AS traffic weighting produces a score that is comparable across route changes affecting different numbers of probes with different traffic volumes. This prevents a large-scale minor improvement from dominating a small-scale severe degradation in the aggregate score.
4. **RIPE Atlas anchors as strategic internal vantage points**: Edgecast's 12 hosted RIPE Atlas anchors provide high-volume measurement capacity from within the CDN network, enabling precise internal routing characterization that complements the external probe perspective.
5. **Future expansion priorities**: The methodology was applied primarily to North America at the time of writing; planned extensions include IPv6 catchment characterization and geographic expansion to Europe and Asia-Pacific, where routing complexity increases with intercontinental BGP paths.

### Authors' Conclusion

RIPE Atlas provides the geographic diversity of vantage points necessary for industrial CDN catchment optimization. The combination of external probes (for client perspective) and internal anchors (for network perspective) creates a complete picture of anycast routing. Geolocation-based probe grouping is the recommended strategy for balancing statistical validity with operational actionability. The normalized scoring framework enables consistent comparison of routing changes across diverse network conditions, supporting data-driven BGP engineering decisions. The article demonstrates that investment in RIPE Atlas anchor hosting by network operators directly improves their ability to measure and optimize their own infrastructure.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- Anycast catchment: the set of clients/probes routed to a specific PoP; the fundamental unit of geographic analysis for anycast services
- Penultimate hop analysis: using the second-to-last router in a traceroute to identify the entry point into a target network — applicable to anycast authoritative DNS servers as well as CDN PoPs
- Probe grouping strategy: the choice of grouping unit (country, AS, prefix, geolocation) critically affects the statistical validity and interpretability of geographic DNS variation measurements
- Logistic normalization + traffic weighting: a principled approach to scoring the impact of routing changes across heterogeneous client populations

**Applicable methods**:
- Apply penultimate hop analysis to RIPE Atlas traceroutes toward anycast authoritative name servers (e.g., root servers, TLD servers, large CDN authoritative servers) to identify which anycast instance serves each probe
- Use geolocation-based probe grouping as the primary geographic unit for aggregating RIPE Atlas DNS measurement results, with AS-level grouping as a secondary analysis
- Adapt the scoring framework concept to quantify geographic variation in DNS responses: a domain that returns different IP addresses to probes in different geolocations scores higher on "geographic variation" than one returning uniform responses

**Important statistics**:
- 6 grouping strategies tested: country, AS, IP prefix, geolocation, BGP path, combinations
- Geolocation-based grouping identified as optimal trade-off
- 12 RIPE Atlas anchors hosted by Edgecast within its CDN network
- Scoring range: +1 (uniform improvement) to -1 (uniform degradation)

**Identified limitations (gaps to fill)**:
- North America focus at time of writing; global applicability of the geolocation grouping finding not validated
- No DNS-specific analysis: the article focuses on traceroutes and BGP, not DNS query/response pairs; extending the methodology to DNS measurements is a contribution our thesis can make
- Temporal dimension absent: the article measures catchment at a point in time; our thesis adds longitudinal tracking

### Personal Critique

**Strengths**:
- Industrial perspective provides ground-truth validation: Edgecast can correlate RIPE Atlas observations with internal BGP data, allowing direct verification of the penultimate hop methodology
- Systematic comparison of 6 grouping strategies is a genuine methodological contribution applicable beyond CDN contexts
- Scoring framework is well-designed: logistic normalization prevents extreme values from dominating, and traffic weighting reflects operational reality
- 12 hosted anchors demonstrate the value of CDN operators investing in measurement infrastructure

**Weaknesses**:
- Non-peer-reviewed practitioner article: methodology details are described in general terms without statistical validation of the grouping strategy comparison
- DNS measurement perspective absent: the article is entirely traceroute/BGP-focused, missing the DNS query layer that is the primary interest for our thesis
- No open dataset or code: reproducibility is limited

**Links to other papers**:
- Bortzmeyer 2013 (RIPE Atlas anycast NSID): DNS-layer anycast identification complements the traceroute-layer approach here; combining both gives the most complete anycast characterization
- Finnegan 2018 (RIPE Atlas anycast DNS): applies similar anycast catchment analysis to DNS-specific use case with "id.server" / NSID queries
- Nosyk et al. 2024 (RIPE Atlas DITL): provides current probe and anchor availability context

**Open questions**:
- Does the optimal probe grouping strategy (geolocation) from the CDN traceroute context generalize to DNS query response analysis?
- Can the penultimate hop technique identify anycast instances of authoritative DNS servers in the same way it identifies CDN PoPs — or do DNS anycast deployments differ architecturally?

### Key Quotes

> "Edgecast hosts 12 RIPE Atlas anchors, providing high-capacity measurement points with direct visibility into its own routing."

> "The penultimate hop of each traceroute reliably identifies which PoP served the request, when correlated with Edgecast's internal BGP topology."

> "Geolocation-based grouping provides the best trade-off between group size, RTT consistency within groups, and BGP path similarity."

> "Improvements normalized via logistic curve, weighted by AS traffic importance, score from +1 (uniform improvement) to -1 (uniform degradation)."

---

## Use in Thesis

**Relevant sections**:
- Section 2.5 (Anycast DNS and CDN geographic routing): Use the catchment concept and geolocation grouping finding to frame how CDN operators use geographic routing, motivating our measurement of geographic DNS variation
- Section 2.5.4 (CDN strategies by actor): Cite Edgecast/Edgio as an example of industrial CDN using RIPE Atlas for routing optimization
- Section 4 (Methodology): Adopt geolocation-based grouping as the primary geographic unit for aggregating RIPE Atlas probe results; consider penultimate hop analysis for anycast server identification

**Points to develop**:
- Position our DNS measurement approach as the DNS-layer complement to this traceroute-layer CDN catchment methodology
- Use the scoring framework concept as inspiration for quantifying geographic variation in DNS responses across Tranco domains

**Cross-references**:
- Fiche Bortzmeyer 2013: DNS-layer NSID technique provides what traceroutes cannot — explicit anycast instance identity without BGP correlation
- Fiche Finnegan 2018: DNS-specific application of anycast catchment analysis

---

**Tags**: #anycast #cdn #ripe-atlas #traceroute #catchment #bgp #geolocation #edgecast #ixp #geographic-routing #scoring-framework
**Status**: [X] Read / [X] Filed
