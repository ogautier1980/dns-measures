# Reading Note - Client Subnet in DNS Queries (RFC 7871 / EDNS Client Subnet)

**Bibliographic Reference**:
Contavalli, C., van der Gaast, W., Lawrence, D., & Kumari, W. (2016). *Client Subnet in DNS Queries*. Internet Engineering Task Force (IETF), Request for Comments: 7871, Category: Informational, ISSN: 2070-1721. https://www.rfc-editor.org/info/rfc7871

**Theme**:
RFC 7871 specifies the EDNS Client Subnet (ECS) extension, an EDNS0 option that allows DNS recursive resolvers to forward a truncated version of the client's IP address prefix to authoritative nameservers. The goal is to enable authoritative nameservers to return geographically tailored DNS responses — particularly important for CDN server selection — when the recursive resolver is topologically distant from the end user. The RFC also documents known privacy and security trade-offs associated with the mechanism.

**Relevance to thesis**:
ECS is a central mechanism linking DNS resolution and geographic routing, which sits at the heart of our thesis on distributed DNS measurements. When RIPE Atlas probes issue DNS queries, whether ECS is present and what prefix is forwarded directly affects which CDN server (and therefore which IP address) the probe receives in response. Understanding ECS is essential for interpreting geographic variability in DNS responses across our probe set and for understanding why measurements from different vantage points may yield different DNS answers for the same domain.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.5 (EDNS Client Subnet — geographic routing and DNS)
- Section 2.4 (CDN and DNS-based server selection)
- Section 3 (Methodology — interpreting geographic variation in DNS answers)

---

## Article Content

### Research Objective(s)

**Problem**: Many authoritative nameservers return location-sensitive DNS responses to direct users to the closest CDN edge server. These servers use the source IP of the incoming query to infer the client's location. However, when queries arrive from a centralized recursive resolver (e.g., Google 8.8.8.8, OpenDNS) that is geographically remote from the end user, the authoritative nameserver uses the resolver's IP rather than the client's IP — resulting in suboptimal server selection and degraded performance.

**Research questions**:
1. How can a recursive resolver communicate the originating client's network location to an authoritative nameserver while traversing intermediate DNS infrastructure?
2. How should responses carrying ECS-scoped answers be cached efficiently without inflating cache size or enabling cache pollution?

### Background

The DNS query/response model traditionally protects client privacy by having recursive resolvers shield end-user IP addresses from authoritative nameservers. This design works well when resolvers are topologically close to their clients (e.g., ISP-operated resolvers). However, the rise of large centralized public DNS resolvers (Google 8.8.8.8, Cloudflare 1.1.1.1, OpenDNS) has created a class of resolvers that serve clients spread across diverse geographies. For CDN operators who rely on DNS to route users to the nearest edge server, the resolver's IP is an unreliable proxy for the client's actual location. ECS was first deployed informally by major operators and later documented in this RFC; the authors acknowledge it describes existing deployed practice rather than a design proposal.

### Methodology

- **Study type**: Standards track / protocol specification (Informational RFC)
- **Tools used**: N/A (protocol specification); at least a dozen client and server implementations existed at time of publication
- **Scale**: Protocol in production use by major operators (Google, Akamai) at the time of publication (May 2016)
- **Measurement protocol**: N/A (RFC specifies behavior, not measurement)
- **Data collected**: N/A

### Main Results

1. **ECS option format**: ECS is carried as an EDNS0 OPT record. The option contains: (a) FAMILY (address family: IPv4 or IPv6), (b) SOURCE PREFIX-LENGTH (bits of the client address forwarded), (c) SCOPE PREFIX-LENGTH (bits of the address space to which the response applies, set by the authoritative nameserver), and (d) ADDRESS (the truncated client IP prefix).

2. **Origination behavior**: Recursive resolvers that implement ECS SHOULD forward the client's IP address truncated to a privacy-preserving prefix (e.g., /24 for IPv4, /48 for IPv6) rather than the full address. Stub resolvers and forwarding resolvers may also originate ECS options, but this is optional.

3. **Authoritative nameserver behavior**: An ECS-aware authoritative nameserver uses the ADDRESS field to select an appropriate response and includes an ECS option in the reply with SCOPE PREFIX-LENGTH set to indicate how many bits of the client address were actually used in the decision. A scope of /0 means the response applies globally and is not location-specific.

4. **Caching implications**: ECS breaks the standard one-DNS-record-per-question caching model. Caches must store separate entries per ECS scope, keyed by (question, ECS prefix). This can significantly inflate cache size at intermediate resolvers. The RFC provides detailed rules for when a cached ECS response may be used to answer a new query with a different ECS prefix.

5. **Privacy and security concerns**: ECS makes the client's network location visible to authoritative nameservers and any on-path observers. The RFC explicitly acknowledges this as a privacy shortcoming and recommends that ECS be disabled by default, enabled only when its benefits are clear. Additional security risks include birthday attacks on scoped DNS responses and cache pollution attacks exploiting the expanded per-scope cache model.

### Authors' Conclusion

The authors conclude that ECS represents a pragmatic engineering trade-off: it improves CDN performance for users of centralized resolvers by providing the authoritative nameserver with better location information, but at the cost of reduced user privacy and increased cache complexity. The RFC recommends conservative deployment: ECS should not be sent to authoritative servers that do not benefit from it (probing and whitelisting mechanisms are specified). The authors acknowledge that a revised, privacy-preserving approach will be needed, and invite future IETF work.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- The fundamental mismatch between recursive resolver location and end-user location — this explains geographic variation in CDN-related DNS answers
- SOURCE PREFIX-LENGTH vs. SCOPE PREFIX-LENGTH distinction: authoritative nameservers reveal how fine-grained their geographic routing actually is
- The ECS privacy–performance trade-off: forwarding more address bits improves routing precision but reduces privacy

**Applicable methods**:
- Interpreting SCOPE PREFIX-LENGTH in DNS responses as an indicator of geographic granularity used by CDN authoritative nameservers
- Using RIPE Atlas probes (which have real, geographically diverse IP addresses) to measure whether ECS is honored and what geographic precision is employed
- Comparing DNS responses received by probes using their own resolver vs. a public resolver (with or without ECS) to quantify the impact of remote DNS on CDN selection

**Important statistics**:
- SOURCE PREFIX-LENGTH recommendation: /24 for IPv4, /48 for IPv6 (balancing location precision with privacy)
- At least a dozen implementations of ECS existed in production by May 2016
- Only one stub resolver (getdns) was known to support ECS anonymity/opt-out at publication time

**Identified limitations (gaps to fill)**:
- The RFC does not specify a mechanism for a downstream party to signal ECS support to an upstream party, creating waste when ECS-compliant resolvers contact non-compliant nameservers
- No empirical data is provided on the actual geographic accuracy improvement achieved by ECS deployment — this remains an open measurement question
- Opt-out support is nearly absent from deployed implementations, undermining the privacy recommendations

### Personal Critique

**Strengths**:
- Thorough specification of option format, caching rules, and transitivity behavior across multiple resolver types
- Honest acknowledgment of privacy shortcomings and explicit privacy note at the beginning — unusual for an RFC
- Documents existing deployed practice rather than a theoretical proposal, providing grounding in real-world implementation experience

**Weaknesses**:
- No quantitative evaluation of the performance improvement ECS actually delivers in practice
- Cache inflation is identified as a concern but is not analyzed quantitatively
- The opt-out/anonymity mechanism is acknowledged as nearly non-functional in practice

**Links to other papers**:
- Wang et al. (2018) — DNS-CDN challenges: places ECS in the broader context of remote DNS problem solutions and compares it to name extension and direct resolution approaches
- Li et al. (2025) — Twitch CDN: ECS is the underlying mechanism that would allow the CDN authoritative servers to return continent-appropriate assignments when queried through remote resolvers
- Hours et al. (2016) — DNS resolvers and CDN performance: empirically measures the impact of resolver choice (ISP vs. public) on CDN server selection, directly motivating ECS

**Open questions**:
- How widely is ECS actually deployed in practice as of 2024–2026? What fraction of authoritative nameservers for top domains respond with non-zero SCOPE PREFIX-LENGTH?
- When RIPE Atlas probes use their local resolver, do those resolvers forward ECS? If not, do probes receive globally uniform DNS answers for CDN domains?
- How does ECS interact with DNSSEC? The RFC notes DNSSEC considerations but does not address signed ECS-scoped responses.

### Key Quotes

> "Many Authoritative Nameservers today return different responses based on the perceived topological location of the user. These servers use the IP address of the incoming query to identify that location."

> "We recommend that the feature be turned off by default in all nameserver software, and that operators only enable it explicitly in those circumstances where it provides a clear benefit for their clients."

> "If we were just beginning to design this mechanism, and not documenting existing protocol, it is unlikely that we would have done things exactly this way."

---

## Use in Thesis

**Relevant sections**:
- Section 2.5 (EDNS Client Subnet): Primary reference for defining ECS, its format, operation, and trade-offs
- Section 2.4 (CDN and DNS routing): Foundation for explaining why different probes may receive different DNS answers for the same domain
- Section 3 (Methodology): Justification for considering ECS behavior when designing measurement methodology; need to check whether probes' resolvers support ECS

**Points to develop**:
- Measurement of ECS deployment prevalence across the Tranco top domains using RIPE Atlas: do authoritative nameservers for popular domains actually use ECS, and at what prefix granularity?
- The privacy–performance trade-off in the context of distributed measurement: RIPE Atlas probes issuing ECS queries from diverse locations could enumerate CDN mapping tables (redirection privacy concern from Wang et al.)

**Cross-references**:
- `wang2018_dns_cdn_challenges.md` — systematic comparison of ECS with alternative remote DNS solutions
- `li2025_twitch_cdn_global.md` — empirical CDN measurement where ECS would affect results
- `hours2016_dns_resolvers_cdn_impact.md` — empirical evidence for the remote DNS problem that ECS aims to solve

---

**Tags**: #ECS #EDNS #RFC #DNS-privacy #CDN #geographic-routing #caching #remote-DNS #protocol
**Status**: [X] Read / [X] Filed
