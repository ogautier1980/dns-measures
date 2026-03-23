# Reading Note - Evolution and Challenges of DNS-Based CDNs

**Bibliographic Reference**:
Wang, Z., Huang, J., & Rose, S. (2018). Evolution and challenges of DNS-based CDNs. *Digital Communications and Networks*, 4(4), 235–243. https://doi.org/10.1016/j.dcan.2017.07.005. National Institute of Standards and Technology (NIST) / Chongqing University of Posts and Telecommunications.

**Theme**:
This survey paper systematically reviews DNS-based Content Delivery Network (CDN) technologies, focusing on server selection, server redirecting mechanisms, and the challenges introduced by remote DNS recursive resolvers. The authors analyze the remote DNS problem — where the geographic mismatch between a client and its recursive resolver causes suboptimal CDN server selection — and evaluate state-of-the-art solutions including EDNS Client Subnet (ECS), name extension, and direct resolution. Privacy concerns arising from these solutions are also addressed.

**Relevance to thesis**:
This paper provides the essential theoretical framework for understanding why DNS responses vary depending on the geographic location of both the client and the recursive resolver — the central mechanism driving spatial variation in our distributed DNS measurements. The remote DNS problem and the ECS solution are directly observable phenomena in our RIPE Atlas measurements: probes using distant or public resolvers may receive different CDN-related DNS answers than probes using local ISP resolvers. This paper enables our thesis to contextualize this geographic variation within the CDN performance optimization ecosystem.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.4 (CDN and DNS-based routing)
- Section 2.5 (EDNS Client Subnet — geographic routing)
- Section 2.2 (DNS fundamentals — recursive resolution and caching)

---

## Article Content

### Research Objective(s)

**Problem**: DNS-based CDN server selection assumes the recursive resolver is geographically close to the end user. As public DNS services (Google 8.8.8.8, OpenDNS, Cloudflare 1.1.1.1) are increasingly adopted, this proximity assumption fails, causing the CDN authoritative server to select a surrogate server optimized for the resolver's location rather than the user's location. This "remote DNS problem" results in suboptimal CDN performance, with documented cases of HTTP latency doubling when using public DNS compared to ISP DNS.

**Research questions**:
1. What are the available mechanisms for CDN server redirection, and what are the comparative advantages of DNS-based approaches?
2. What solutions have been proposed or deployed to address the remote DNS problem, and how do they compare in terms of client complexity, transparency, cache efficiency, and privacy?

### Background

CDNs replicate content on geographically distributed surrogate servers to minimize delivery latency and improve scalability. Request routing — the mechanism that directs each user to an optimal surrogate — typically uses the user's network location as the primary input. Four server redirecting mechanisms exist: HTTP redirection (requires extra round-trip), URL rewriting (non-cacheable), anycast (network-layer, limited control), and DNS-based redirecting (the dominant approach). DNS-based CDN redirection exploits the DNS infrastructure's existing global distribution and allows CDN operators to return dynamically selected surrogate server IP addresses in response to DNS queries. CNAME records decouple content domain names from CDN domain names, enabling independent management.

### Methodology

- **Study type**: Survey / analytical comparison
- **Tools used**: Literature analysis; reference to measurement studies (Otto et al. 2012 on public DNS impact; Calder et al. on ECS-based CDN enumeration)
- **Scale**: Survey covers industry deployments (Akamai, Limelight Networks, Mirror Image, Google) and academic proposals
- **Measurement protocol**: N/A (survey); references a 2012 study measuring ISP vs. public DNS CDN similarity at multiple locations
- **Data collected**: N/A (survey); key cited measurement: ISP DNS had similar CDN server selection to clients in at least 80% of locations; public DNS had no similarity to clients for 90% of locations; public DNS doubled HTTP latency compared to ISP DNS or direct client resolution

### Main Results

1. **DNS-based CDN advantages**: DNS-based redirection offers transparency (invisible to users), simplicity (compatible with existing infrastructure), and flexibility (TTL controls cache lifetime). Zero-TTL allows per-request dynamic redirection; large TTLs reduce authoritative server load. CDN providers like Akamai, Limelight, and Mirror Image have adopted this approach as their primary redirection mechanism.

2. **Remote DNS problem severity**: A 2012 study found that ISP DNS and client IP had similar CDN server selection in at least 80% of locations, while public DNS had no similarity with clients for 90% of locations. HTTP performance with public DNS showed doubled latencies compared to ISP DNS or client-direct resolution. The impact worsens as public DNS adoption grows (27% annual growth in public DNS user base as of 2012, with 8.6% of users relying on public DNS).

3. **ECS solution analysis**: ECS (RFC 7871) allows recursive resolvers to forward the client's IP prefix to authoritative nameservers. It requires joint deployment across all parties (stub resolvers, recursive resolvers, authoritative servers, middleboxes). Cache efficiency is compromised: the standard one-to-one DNS caching model expands to a per-scope model, potentially enabling DoS attacks that bypass caching. The transition challenge is that ECS-compliant parties have no way to signal support to upstream parties, causing unnecessary privacy leakage.

4. **Name extension alternative**: Encoding client location in the DNS query name (e.g., prefixing geolocation information onto the query) allows the CDN authoritative server to derive client location without modifying intermediate DNS infrastructure. This approach requires only client-side and authoritative-server-side changes, reducing deployment obstacles compared to ECS. However, cache efficiency is similarly affected and recursive resolvers must handle modified query names correctly.

5. **Direct resolution approach**: The client-side resolver directly contacts the CDN authoritative server (bypassing the standard recursive resolution chain). This provides the most accurate location information (the client's actual IP) but increases client complexity and exposes the full client IP address (reducing privacy more than ECS's truncated prefix approach).

6. **Privacy concerns**: ECS makes client location information visible to authoritative nameservers and on-path observers. Additionally, ECS-enabled queries allow adversaries to enumerate CDN mapping tables efficiently: Calder et al. demonstrated that Google's entire CDN mapping could be enumerated using ECS queries with /24 prefixes in approximately one day. This "redirection privacy" concern is distinct from location privacy and affects CDN operators' competitive and security interests.

### Authors' Conclusion

The authors conclude that DNS-based server redirection remains the dominant and most practical CDN deployment mechanism, but faces two fundamental challenges: the remote DNS problem (degraded performance when resolver and client are geographically distant) and privacy concerns (ECS reveals client location and enables CDN mapping enumeration). ECS is the most widely deployed solution to the remote DNS problem but introduces significant deployment complexity and privacy trade-offs. No current solution simultaneously achieves optimal CDN performance, low client complexity, high intermediate transparency, good cache efficiency, and strong privacy protection.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- The remote DNS problem as the primary source of geographic variation in DNS-CDN interactions — foundational to interpreting why RIPE Atlas probes at different locations receive different DNS answers
- CNAME chain as the mechanism linking content domain names to CDN domain names — our measurements should trace full CNAME chains, not just the initial A record
- TTL as a control mechanism: low TTL values allow frequent CDN updates but increase query load; this temporal dimension connects to our thesis's focus on DNS "in time"

**Applicable methods**:
- Comparing DNS responses received by probes using local ISP resolvers vs. public resolvers (Google 8.8.8.8, Cloudflare 1.1.1.1) to quantify the remote DNS effect on CDN selection
- Analyzing SCOPE PREFIX-LENGTH in ECS responses to determine geographic granularity of CDN routing policies
- Measuring CNAME chain depth across the Tranco top domains to understand the CDN delegation structure

**Important statistics**:
- ISP DNS similar to client in at least 80% of locations; public DNS has no similarity with client in 90% of locations
- Public DNS doubles HTTP latency compared to ISP DNS or direct client resolution
- Public DNS user base grew 27% annually; 8.6% of users relying on public DNS services (2012 data)
- Anycast CDNs directed roughly 20% of clients to suboptimal front ends

**Identified limitations (gaps to fill)**:
- The survey's empirical data is from 2012 studies; public DNS adoption has likely accelerated substantially since then (Cloudflare 1.1.1.1 launched in 2018, after this paper)
- No measurement of ECS deployment rates across the global authoritative nameserver population
- The paper focuses on traditional DNS-based CDN; it does not address DNS over HTTPS/TLS, which changes the resolver visibility model

### Personal Critique

**Strengths**:
- Systematic taxonomy of CDN redirection mechanisms and the five comparison metrics (client complexity, intermediate transparency, deployment cost, cache efficiency, privacy) provide a clean analytical framework
- Clear explanation of the CNAME-based CDN delegation architecture — essential background for any DNS measurement study involving CDN domains
- Balanced treatment of ECS trade-offs, including the often-overlooked redirection privacy (CDN mapping enumeration) concern

**Weaknesses**:
- Survey nature means no original empirical data; relies heavily on cited measurement studies
- The 2012 measurement data on public DNS impact is significantly outdated relative to the 2018 publication date
- Limited coverage of the rapidly evolving DNS privacy landscape (DoH, DoT, DNSSEC are not discussed)

**Links to other papers**:
- RFC 7871 (Contavalli et al., 2016) — ECS specification: this paper surveys ECS as a deployed solution; the RFC provides the normative definition
- Li et al. (2025) — Twitch CDN measurement: empirically demonstrates the CDN architecture this paper describes theoretically
- Hours et al. (2016) — DNS resolvers and CDN impact: provides the empirical basis for several of the performance claims in this survey
- Calder et al. (2015) — ECS-based CDN enumeration: cited for the redirection privacy concern

**Open questions**:
- Has ECS deployment expanded significantly between 2018 and 2026? What fraction of the Tranco top 10,000 domains have ECS-aware authoritative nameservers?
- How does DNS over HTTPS (DoH) change the remote DNS problem? DoH resolvers are typically operated by large tech companies (Cloudflare, Google, Mozilla) and thus likely to be remote from most users.
- Can our RIPE Atlas measurements distinguish between CDN geographic routing granularity (via SCOPE PREFIX-LENGTH) and simple anycast-based routing?

### Key Quotes

> "DNS-based server redirecting is considered the most popular means of deploying CDNs. However, with the increasing use of remote DNS, DNS-based CDNs face a great challenge in performance degradation."

> "The remote DNS issue arises from the false assumption that a DNS recursive server is in proximity to its clients."

> "ISP DNS was shown to have some similarity with clients in at least 80% of locations, and there was no similarity between public DNS and client for 90% of locations."

> "ECS may make [CDN mapping enumeration] possible because it greatly reduces the number of queries. Calder et al. used ECS-enabled queries to measure the redirection mapping of the Google web service... queries against Google were reported as taking about a day to enumerate."

---

## Use in Thesis

**Relevant sections**:
- Section 2.4 (CDN and DNS-based routing): Primary survey reference; provides the taxonomy of CDN redirection mechanisms and the CNAME-based delegation architecture
- Section 2.5 (EDNS Client Subnet): Comparative analysis of ECS vs. alternative approaches; the five-metric comparison framework can structure our discussion
- Section 2.2 (DNS fundamentals): TTL semantics, caching behavior, and the recursive resolution chain are described here in the CDN context

**Points to develop**:
- Updating the empirical picture: our measurements will provide 2024–2026 data on ECS deployment and the remote DNS effect, updating the 2012-era statistics cited in this survey
- Quantifying the spatial dimension of the remote DNS problem using RIPE Atlas: how much does the DNS answer for a CDN domain vary across RIPE Atlas probes as a function of their distance to the resolver?

**Cross-references**:
- `rfc7871_edns_client_subnet.md` — normative ECS specification
- `li2025_twitch_cdn_global.md` — empirical CDN measurement complementing this survey
- `hours2016_dns_resolvers_cdn_impact.md` — empirical quantification of remote DNS performance impact

---

**Tags**: #CDN #DNS-based-redirecting #remote-DNS #ECS #CNAME #TTL #privacy #anycast #HTTP-redirection #survey
**Status**: [X] Read / [X] Filed
