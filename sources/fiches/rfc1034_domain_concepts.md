# Reading Note - Domain Names: Concepts and Facilities (RFC 1034)

**Bibliographic Reference**:
Mockapetris, P. (1987). *Domain Names - Concepts and Facilities*. Internet Engineering Task Force (IETF), Request for Comments: 1034, STD 13. https://www.rfc-editor.org/rfc/rfc1034 — DOI: 10.17487/RFC1034

**Theme**:
RFC 1034 is the foundational specification of the Domain Name System (DNS). It defines the namespace model, the resource record abstraction, the roles of resolvers and nameservers, and the delegation model underlying the entire DNS hierarchy. Together with RFC 1035, it constitutes the original DNS standard (STD 13), still in force today despite numerous extensions.

**Relevance to thesis**:
RFC 1034 is the primary reference for understanding what DNS is and how it operates. Any distributed measurement of DNS behaviour — geographic routing, TTL dynamics, anycast instance variation, resolver diversity — must be grounded in the conceptual model defined here: zones, delegation, authoritative vs. recursive resolution, caching with TTL, and the distinction between stub resolvers and full resolvers. It is the essential background for the entire thesis.

---

## Reading Context

**Date**: 23 March 2026
**Thesis sections**:
- Section 2.1 (DNS architecture — foundational background)
- Section 2.2 (DNS measurement infrastructure — what is being measured)
- Section 3 (Methodology — what queries types and resolution modes are used)

---

## Article Content

### Research Objective(s)

RFC 1034 does not address a research problem; it defines a standard. Its design goals are:
1. Provide a consistent, hierarchical name space decoupled from network topology.
2. Support a distributed, locally-administered database with global coherence via delegation.
3. Enable general-purpose name service beyond host-to-address mapping (mail routing, service discovery, etc.).
4. Scale to an internet of any size through caching and delegation.

### Background

Prior to DNS, the ARPANET relied on a single centrally-maintained HOSTS.TXT file distributed via FTP to all hosts. By 1983, this approach had become unworkable: update latency, traffic load (quadratic in the number of hosts), and lack of local autonomy motivated the design of a distributed system. RFC 1034 supersedes RFC 882 and RFC 883.

### Methodology

- **Type**: Protocol specification (Standards Track, STD 13)
- **Tools**: N/A — conceptual and protocol design
- **Scale**: Designed for Internet-wide use
- **Data**: N/A

### Main Results

1. **Namespace model**: DNS names are sequences of labels separated by dots, forming a hierarchical tree rooted at "." (the root). Labels are case-insensitive, up to 63 octets each; total name length up to 255 octets. The tree is divided into **zones** administered independently by delegated authorities.

2. **Resource Records (RRs)**: Each node in the name tree may carry a set of typed records: A (IPv4 address), NS (nameserver delegation), CNAME (canonical name alias), MX (mail exchanger), SOA (zone start of authority), and others. Each RR has a **TTL** (Time To Live) controlling how long resolvers may cache it.

3. **Delegation model**: A parent zone delegates authority for a sub-tree by publishing NS records pointing to the child's nameservers. The child zone is authoritative for its portion of the namespace; the parent is not. This creates the distributed administration model.

4. **Resolution modes**:
   - *Recursive resolution*: The resolver asks a nameserver to do the entire lookup on its behalf and return a final answer.
   - *Iterative (referral) resolution*: The resolver queries a nameserver which either answers or returns a referral to another nameserver closer to the answer. Full resolvers typically use iterative queries toward the global hierarchy and offer recursive service to stub resolvers.

5. **Caching**: Resolvers cache responses for the duration of the TTL. Negative caching (absence of a record) is also specified. Caching is the mechanism that makes DNS scalable: the root and TLD nameservers handle only a small fraction of total DNS traffic.

6. **Stub vs. full resolver**: Stub resolvers (on end-user hosts) rely entirely on a local recursive resolver (typically operated by the ISP or a public DNS provider). Full resolvers walk the hierarchy themselves. This distinction is central to the remote-DNS problem addressed by ECS (RFC 7871).

### Authors' Conclusion

Mockapetris concludes that a hierarchical distributed database with delegation and TTL-based caching is the appropriate architecture for Internet-scale name resolution. The design intentionally leaves room for extensibility (new RR types, new query classes) without breaking existing implementations.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- **TTL as a measurement variable**: variation in DNS answer TTLs across time and probes is a primary temporal signal in our measurement campaign
- **Authoritative vs. recursive resolution**: our measurement design explicitly separates direct authoritative queries (bypassing the resolver) from ISP resolver and public DNS resolver queries — a distinction rooted in RFC 1034's model
- **Zone delegation**: understanding that different parts of a domain name may be answered by different authorities is essential for interpreting inconsistent responses across probes

**Applicable methods**:
- Framing geographic DNS variation in terms of which authoritative nameserver a probe reaches (zone delegation + anycast routing)
- Distinguishing CNAME chains from direct A record answers — relevant when measuring CDN-served domains

**Important statistics**:
- Maximum DNS name length: 255 octets; maximum label length: 63 octets
- Original ARPANET HOSTS.TXT: maintained centrally, FTPed to all hosts — linear-to-quadratic bandwidth scaling motivated DNS
- TTL range: 0 (no caching allowed) to 2³²−1 seconds (≈ 136 years)

**Identified limitations (gaps to fill)**:
- RFC 1034 predates CDNs, anycast deployment, and distributed measurement infrastructure — the geographic routing behaviour of modern authoritative nameservers is entirely outside its scope
- No treatment of DNSSEC, DoH, DoT, or ECS — all covered in later RFCs

### Personal Critique

**Strengths**:
- Remarkably clear conceptual design that has remained stable for nearly 40 years
- The separation of concerns between naming (RFC 1034) and wire format (RFC 1035) is a good engineering choice
- Explicit design goals in Section 2.2 make the document's intent clear

**Weaknesses**:
- 1987 assumptions (stable, slow-changing namespace; cooperative participants) do not hold in the modern adversarial Internet
- No treatment of performance, geographic routing, or load distribution

**Links to other papers**:
- RFC 1035 (Mockapetris, 1987) — companion implementation spec
- RFC 7871 (Contavalli et al., 2016) — ECS, addressing the stub/full resolver location mismatch
- Wang et al. (2018) — remote DNS problem arises directly from stub-resolver architecture defined here
- Nosyk et al. (2024) — RIPE Atlas DNS measurements measure the full resolution chain described in RFC 1034

### Key Quotes

> "The primary goal is a consistent name space which will be used for referring to resources."

> "The sheer size of the database and frequency of updates suggest that it must be maintained in a distributed manner, with local caching to improve performance."

> "The domain system is intentionally extensible. Researchers are continuously proposing, implementing and experimenting with new data types, query types, classes, functions, etc."

---

## Use in Thesis

**Relevant sections**:
- Section 2.1: Definition of DNS namespace, RR types (A, NS, CNAME, MX, SOA), TTL, delegation, recursive vs. iterative resolution
- Section 3: Justification for measuring both authoritative and recursive resolution paths

**Points to develop**:
- The TTL mechanism as both a caching tool and a temporal measurement signal (low TTL = frequent updates, high TTL = stable delegation)
- The resolver architecture as the root cause of the geographic routing problem (remote resolver → wrong CDN node)

**Cross-references**:
- `rfc1035_domain_implementation.md` — wire format and RR types
- `rfc7871_edns_client_subnet.md` — ECS as a patch for the stub/full resolver split
- `wang2018_dns_cdn_challenges.md` — remote DNS problem

---

**Tags**: #DNS #RFC #foundational #namespace #TTL #delegation #resolver #caching #authoritative
**Status**: [X] Read / [X] Filed
