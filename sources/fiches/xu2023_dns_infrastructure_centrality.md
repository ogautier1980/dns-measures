# Reading Note - Measuring the Centrality of DNS Infrastructure in the Wild

**Bibliographic Reference**:
Xu, C., Zhang, Y., Shi, F., Shan, H., Guo, B., Li, Y., & Xue, P. (2023). Measuring the Centrality of DNS Infrastructure in the Wild. *Applied Sciences*, 13(9), 5739. https://doi.org/10.3390/app13095739

**Theme**:
This paper investigates the degree of centralization in the DNS ecosystem's underlying infrastructure, covering both the client-side (resolver pools) and server-side (authoritative name servers). The authors propose a novel lightweight measurement technique based on NS chain reflection to uncover implicit resolver pool structures invisible to traditional passive analysis. Their Internet-wide active measurement spans over 210 million domain names across 1138 gTLDs.

**Relevance to thesis**:
Understanding DNS infrastructure centralization is directly relevant to a thesis on distributed DNS measurements, as it reveals that the supposedly distributed DNS system is in practice highly concentrated among a small number of providers. This concentration affects the geographic diversity of DNS responses observed from RIPE Atlas probes. Findings on resolver pool structures and authoritative name server concentration inform the design of measurement campaigns, particularly the selection of target domains from the Tranco list and the interpretation of vantage-point diversity.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.1 (DNS ecosystem overview and architecture)
- Section 2.7 (Centralization trends and risks)
- Section 4 (Methodology: resolver-side considerations)

---

## Article Content

### Research Objective(s)

**Problem**: The DNS was designed as a distributed system, yet centralization has emerged through commercial consolidation. The degree of centralization in the supporting infrastructure — resolver pools and authoritative name servers — is not well quantified, and existing passive measurement methods fail to reveal the implicit multi-layer resolver pool structure deployed by major public DNS providers.

**Research questions**:
1. How centralized is the client-side DNS infrastructure in terms of resolver pools, and can a single probing point efficiently uncover implicit resolver pool structures?
2. How centralized is the server-side DNS infrastructure in terms of authoritative name server providers across all gTLDs?
3. What is the degree of shared infrastructure between different DNS service providers, and what are the implications for resilience?

### Background

The DNS resolution model has evolved from a simple client-resolver-authoritative chain into a multi-layer architecture where public DNS providers deploy Forwarding Resolvers (FDNS), Recursive Resolvers (RDNS), Indirect RDNS (iRDNS), and Direct RDNS (dRDNS). These layers form implicit resolver pools that are transparent to end users but critically determine the actual infrastructure dependencies of DNS resolution. Prior work by Schomp et al. introduced a CNAME-chain-based pool discovery method, but this paper demonstrates it is no longer effective across modern providers. On the server side, the concentration of authoritative DNS has been partially explored using TLD zone files, but no study had previously covered all 1138 gTLDs at scale.

### Methodology

- **Study type**: Active measurement (Internet-wide scanning) combined with passive zone file analysis
- **Tools used**: NS chain reflection technique (novel), custom probing infrastructure, DNS zone file collection from 1138 gTLDs
- **Scale**: Internet-wide scan of all routable IPv4 addresses; 210,446,494 domain names from 1138 gTLD zone files; 20 public DNS providers tested for CNAME behavior
- **Measurement protocol**: NS chain reflection sends crafted queries that cause resolvers to reveal their internal structure through the chain of NS referrals observed at the authoritative level; a single probing point suffices to map full resolver pools. For server-side analysis, zone files were downloaded and analyzed to identify name server providers and their IP infrastructure.
- **Data collected**: Resolver pool memberships (FDNS to iRDNS mappings), name server provider market share, shared IP infrastructure across providers, geographic distribution of name server deployments

### Main Results

1. **Client-side concentration**: Over 90% of forwarding resolvers (FDNSes) are backed by fewer than 5% (4,071) of indirect recursive resolvers (iRDNSes), demonstrating extreme concentration in the actual resolution infrastructure even when the visible surface appears diverse.
2. **Server-side concentration**: Only 0.45% (12,679) of all name servers across 1138 gTLDs, operated by just 10 DNS providers, provide authoritative resolution for 48.5% of all domain names — over 100 million domains.
3. **Single-provider dependency**: More than 98% of all domain names rely on a single authoritative name server provider, meaning a failure of that provider causes complete DNS unavailability for the domain.
4. **Shared infrastructure**: 60% of combinations of name server providers share infrastructure directly or indirectly, meaning enterprises that diversify across multiple DNS providers may still implicitly share a common underlying infrastructure, undermining resilience strategies.
5. **CNAME method invalidation**: The CNAME chain-based resolver discovery method proposed by Schomp et al. is no longer effective: public DNS providers fall into three distinct behavioral patterns (Multi-RDNSIP, Single-RDNS, Multi-Query), and most use Single-RDNS resolution that prevents pool discovery via CNAME chains.

### Authors' Conclusion

The DNS infrastructure is substantially more centralized than previously believed, with the failure of a single provider capable of rendering millions of domains unreachable — as demonstrated by real-world outages (Akamai June 2021, Facebook October 2021). The authors argue that the NS chain reflection technique fills a critical methodological gap by enabling active, low-cost, single-point discovery of implicit resolver pools. They call on the Internet community to recognize infrastructure-level centralization as distinct from, and more dangerous than, market-share centralization, and support initiatives like DNS4EU as a structural response.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- FDNS / RDNS / iRDNS / dRDNS taxonomy for client-side DNS infrastructure
- Resolver pool: implicit cooperative structure invisible to clients but determinant for infrastructure dependency
- NS chain reflection as an active measurement technique for resolver pool discovery
- Shared infrastructure as a hidden single point of failure even when provider diversity appears high

**Applicable methods**:
- Active probing from a single vantage point to characterize resolver behavior (applicable to RIPE Atlas probe measurements)
- Zone file analysis for domain-to-provider mapping (complements Tranco-based domain selection)
- Provider-level aggregation of name server measurements rather than per-IP analysis

**Important statistics**:
- 90%+ of FDNSes backed by fewer than 5% of iRDNSes
- Top 10 providers handle 48.5% of all gTLD domain names (>100 million)
- 98%+ of domains rely on a single name server provider
- 60% of provider combinations share underlying infrastructure

**Identified limitations (gaps to fill)**:
- No temporal dimension: measurements represent a point-in-time snapshot, not longitudinal evolution; our thesis adds the time dimension
- No geographic analysis of resolver pool distribution: RIPE Atlas probes distributed across 178 countries could reveal geographic variation in which resolver pools are encountered
- Focus on gTLDs only; ccTLD centralization not covered

### Personal Critique

**Strengths**:
- Novel NS chain reflection method overcomes a demonstrated methodological limitation in prior work
- Exceptional scale: 210+ million domains across 1138 gTLDs is the most comprehensive server-side analysis to date
- Clear practical implications: links measurement results to real-world outage events
- Multi-dimensional analysis (IP, domain, provider, IP provider) avoids single-metric bias

**Weaknesses**:
- Single probing point for active measurements limits geographic perspective on resolver pool behavior; pools may differ depending on the client's location
- Point-in-time snapshot: DNS infrastructure evolves rapidly (CDN shifts, provider acquisitions) and findings may age quickly
- No analysis of ccTLDs, which represent a significant portion of the global DNS and may show different centralization patterns
- The shared infrastructure finding (60%) lacks a precise definition of "direct or indirect" sharing, making it difficult to assess severity

**Links to other papers**:
- Moura et al. (DNS traffic centralization): complementary passive traffic analysis vs. this paper's active infrastructure probing
- Schomp et al. (CNAME chain method): this paper refutes that method's current validity
- Le Pochat et al. / Tranco: domain selection methodology intersects with the zone file analysis used here

**Open questions**:
- Does the resolver pool structure differ depending on the geographic location of the probing point? RIPE Atlas probes distributed worldwide could test this.
- How does DNS infrastructure centralization evolve over time — are the trends accelerating, and which providers are gaining share?

### Key Quotes

> "The DNS infrastructure is much more centralized than previously believed. Over 90% of forwarding resolvers are backed by less than 5% (4071) of indirect resolvers."

> "Merely 0.45% (12,679) of all name servers across 1138 gTLDs, operated by just 10 DNS providers, provide authoritative domain resolution service for 48.5% (more than 100 million) of domain names."

> "60% combinations of name server providers share their infrastructure directly or indirectly, which suggests that enterprises may implicitly rely on the same infrastructure even if they outsource their DNS service to multiple DNS providers."

---

## Use in Thesis

**Relevant sections**:
- Section 2.1 (DNS Architecture): Use taxonomy (FDNS/RDNS/iRDNS/dRDNS) to describe the real-world multi-layer resolver architecture
- Section 2.7 (Centralization): Cite the 48.5% / top-10-providers statistic as empirical evidence of DNS consolidation risk
- Section 4 (Methodology): Discuss how resolver pool concentration affects the interpretation of RIPE Atlas measurements (probes may route through the same iRDNS regardless of geographic location)

**Points to develop**:
- Contrast the "designed as distributed" principle with the empirical centralization findings to frame the research problem
- Use shared infrastructure findings to motivate geographic vantage point diversity as a way to detect hidden dependencies

**Cross-references**:
- Fiche Nosyk 2024 (RIPE Atlas operations): geographic diversity of probes vs. concentration at the resolver infrastructure level
- Fiche van Rijswijk-Deij / OpenINTEL: server-side measurement at scale complements resolver-side analysis

---

**Tags**: #dns-centralization #resolver-pools #active-measurement #infrastructure #anycast #authoritative-nameservers #internet-consolidation
**Status**: [X] Read / [X] Filed
