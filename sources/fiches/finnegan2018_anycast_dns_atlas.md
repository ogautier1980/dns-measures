# Reading Note - Measuring Anycast DNS Services Using RIPE Atlas

**Bibliographic Reference**:
Finnegan, K. (2018, October 1). Measuring Anycast DNS Services Using RIPE Atlas. *RIPE Labs*. https://labs.ripe.net/author/kenneth_finnegan/measuring-anycast-dns-services-using-ripe-atlas/

**Theme**:
This practitioner article presents a step-by-step methodology for characterizing the global performance and geographic distribution of anycast DNS services using RIPE Atlas probes. It covers anycast DNS fundamentals, the use of the CHAOS class "id.server" query and the NSID option to identify which anycast instance responds, and a practical deployment of 500 RIPE Atlas probes to evaluate an anycast DNS candidate for an Internet Exchange Point.

**Relevance to thesis**:
Anycast is the dominant delivery mechanism for public DNS resolvers (8.8.8.8, 1.1.1.1) and authoritative name servers (root servers, TLD servers). Measuring which anycast instance responds to a given probe is essential for understanding geographic variation in DNS responses — a core theme of our thesis. The "id.server" CHAOS query and NSID option described here are the principal techniques for anycast instance identification in active DNS measurement campaigns using RIPE Atlas.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.4 (RIPE Atlas: DNS measurement capabilities)
- Section 2.5 (Anycast DNS and geographic routing)
- Section 4 (Methodology: anycast instance identification)

---

## Article Content

### Research Objective(s)

**Problem**: Anycast DNS services expose a single global IP address, but BGP routing delivers queries to one of many geographically distributed instances. Network operators and researchers need practical methods to determine which instance serves traffic from a given location, both to characterize the geographic catchment of each instance and to identify gaps in coverage that could be filled by new Points of Presence (PoPs).

**Research questions**:
1. How can one identify which anycast instance of a DNS service is reached from a given geographic location using RIPE Atlas?
2. What is the geographic catchment distribution of a specific anycast DNS service, and does it exhibit counter-intuitive BGP routing patterns?
3. Which anycast DNS services have coverage gaps that make them good candidates for a new PoP at a specific Internet Exchange?

### Background

Anycast DNS assigns one global IP address to multiple physical servers (instances) distributed worldwide. BGP routing protocol directs each client to the "nearest" instance in terms of BGP path length, not geographic proximity. This means that geographic proximity and traffic routing can diverge significantly — a phenomenon determined by "BGP attraction basins." Major public DNS resolvers (Google 8.8.8.8, Cloudflare 1.1.1.1) and all DNS root servers use anycast. The article was written in the context of evaluating DNS services for the Fremont Cabal Internet Exchange (FCIX) in California, seeking anycast providers with limited West Coast presence who would benefit from a new PoP.

### Methodology

- **Study type**: Operational measurement / practitioner guide
- **Tools used**: RIPE Atlas (probe deployment and DNS measurements), RIPE Atlas API (measurement creation and result retrieval)
- **Scale**: 500 RIPE Atlas probes (250 worldwide + 250 United States-focused), querying multiple anycast DNS services
- **Measurement protocol**: Three-step process:
  1. Identify candidate anycast DNS services by querying their published service IPs
  2. Send CHAOS class TXT queries for "id.server" (RFC 4892) to each service IP — these queries bypass the cache (being non-standard) and return an instance identifier (typically an IATA airport code indicating the PoP location); alternatively, use NSID option (RFC 5001) on any query type, which works even when "id.server" is not implemented
  3. Deploy 500 RIPE Atlas probes (global + US-biased split) and collect instance identifier responses to map geographic catchment per anycast instance
- **Data collected**: Per-probe anycast instance identifier (IATA airport code or NSID string), mapped to geographic location of probe, used to derive instance catchment percentages

### Main Results

1. **Anycast instance identification via "id.server" CHAOS query**: Querying for "id.server" in the CHAOS class returns a text string identifying the specific anycast instance (e.g., "dns.th2.nic.fr" for Paris or "dns.fra.nic.fr" for Frankfurt). This query type bypasses DNS caching because CHAOS class records are not cached by resolvers, ensuring that each probe's response reflects its actual BGP-routed instance.
2. **NSID as a universal alternative**: The NSID option (RFC 5001) can be added to any DNS query (A, AAAA, etc.) and returns an instance identifier in the OPT record without requiring CHAOS class support. This makes it applicable to services that do not implement "id.server" but do return NSID strings.
3. **UncensoredDNS catchment example (91.239.100.100)**: Measurement with 500 probes showed strong European instance coverage but very limited West Coast of North America presence — exactly the geographic gap that a Fremont IXP PoP would address. This demonstrated the practical utility of the methodology for IXP peering decisions.
4. **BGP routing diverges from geographic proximity**: Even for probes physically located in California, BGP routing may direct queries to European instances if the routing path to a European PoP is shorter in BGP hop count. This counter-intuitive behavior must be accounted for when interpreting anycast catchment measurements.
5. **500-probe split strategy**: Using 250 global probes captures worldwide distribution, while 250 US-focused probes provides statistical resolution sufficient to identify regional gaps within a single country — demonstrating the value of geographically targeted probe selection.

### Authors' Conclusion

RIPE Atlas provides an accessible and sufficiently large probe network to characterize anycast DNS instance catchments at global and regional granularity. The combination of "id.server" CHAOS queries (or NSID) with a well-chosen probe set enables network operators to make data-driven decisions about anycast PoP placement. The methodology is practical, low-cost in terms of RIPE Atlas credits, and reproducible. The article implicitly concludes that anycast DNS geographic performance is frequently counter-intuitive and requires empirical measurement rather than assumption based on geographic proximity.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- "id.server" CHAOS class TXT query (RFC 4892): the standard mechanism for anycast instance identification in DNS measurements; cache-bypassing by design
- NSID option (RFC 5001): universal alternative to "id.server", applicable to any query type, included in the OPT record of DNS responses
- BGP attraction basins: the BGP routing construct that determines which anycast instance a probe reaches, independent of geographic proximity
- Anycast catchment: the set of network locations (probes, clients) routed to a specific anycast instance; varies with BGP topology changes

**Applicable methods**:
- In our RIPE Atlas DNS measurements: add NSID option to all queries to capture which anycast instance of the target's authoritative name server or public resolver responds — this adds a geographic routing layer to our DNS response analysis
- Dual probe strategy (global + region-specific): when a specific region is of interest, allocate a disproportionate share of probes to that region while maintaining global coverage
- IATA airport code decoding: map instance identifiers to physical PoP locations for geographic visualization

**Important statistics**:
- 500 probes (250 global + 250 US) sufficient for regional anycast characterization
- UncensoredDNS: strong European presence, near-absence on US West Coast — illustrates measurable geographic gaps

**Identified limitations (gaps to fill)**:
- Single-point-in-time measurement: anycast catchments change with BGP updates, peering changes, and new PoP deployments; temporal tracking requires repeated measurements — our thesis's longitudinal dimension addresses this
- Not all anycast DNS services implement "id.server" or return NSID; some services are opaque to these techniques
- The article does not quantify latency differences between instances — an important complement to catchment analysis

### Personal Critique

**Strengths**:
- Practical, step-by-step methodology directly applicable to our RIPE Atlas measurement campaign
- Motivating real-world use case (IXP PoP placement) grounds the methodology in operational relevance
- Clear explanation of "id.server" vs. NSID trade-offs
- Demonstrates that 500 probes provide sufficient resolution for both global and regional (US) analysis

**Weaknesses**:
- Blog post / practitioner article: not peer-reviewed, no statistical analysis of result uncertainty
- Results presented for only one DNS service (UncensoredDNS); broader comparative analysis would strengthen the methodology
- No latency or RTT data accompanying the catchment measurements — geographic routing and performance are decoupled

**Links to other papers**:
- Bortzmeyer 2013 (RIPE Atlas anycast instances, d.nic.fr): earlier application of the same NSID methodology to the .fr TLD anycast name server, providing quantitative catchment results (36% Paris, 36% Frankfurt globally)
- Edgecast 2017 (RIPE Atlas CDN catchment): extends this methodology to commercial CDN anycast with a scoring framework for PoP optimization
- Nosyk et al. 2024 (RIPE Atlas DITL): operational context for probe availability and geographic distribution

**Open questions**:
- How frequently do anycast catchment boundaries shift for major public DNS resolvers (8.8.8.8, 1.1.1.1), and can RIPE Atlas detect these shifts in near-real-time?
- Does the anycast instance that serves the DNS query for a domain's name server match the anycast instance that ultimately serves the domain's content (CDN PoP)? Measuring both via RIPE Atlas would reveal DNS-to-content routing consistency.

### Key Quotes

> "Anycast DNS assigns one global IP address to multiple physical servers distributed worldwide; BGP routing directs each client to the nearest instance in terms of BGP path length, not geographic proximity."

> "Querying 'id.server' in the CHAOS class returns a text string identifying the specific anycast instance, bypassing DNS caching because CHAOS class records are not cached by resolvers."

> "The NSID option (RFC 5001) can be added to any DNS query and returns an instance identifier in the OPT record, applicable to services that do not implement 'id.server'."

> "UncensoredDNS showed strong European coverage but very limited West Coast presence — exactly the geographic gap that a Fremont IXP PoP would address."

---

## Use in Thesis

**Relevant sections**:
- Section 2.4 (RIPE Atlas DNS capabilities): Describe "id.server" CHAOS and NSID as standard DNS instance identification techniques
- Section 2.5 (Anycast DNS): Explain BGP attraction basins and why geographic proximity does not guarantee local instance routing
- Section 4 (Methodology): Specify inclusion of NSID option in all RIPE Atlas DNS measurements to capture anycast routing information alongside DNS response content

**Points to develop**:
- Add NSID to the measurement specification in Chapter 4 to enable anycast instance tracking across the Tranco domain list
- Use anycast catchment analysis as one dimension of the spatial variation analysis (which domains' authoritative servers show geographic routing variation)

**Cross-references**:
- Fiche Bortzmeyer 2013: quantitative anycast catchment results using the same methodology on d.nic.fr
- Fiche Edgecast 2017: industrial extension of catchment measurement to CDN PoP optimization

---

**Tags**: #anycast #dns #ripe-atlas #bgp #id-server #nsid #catchment #geographic-routing #ixp
**Status**: [X] Read / [X] Filed
