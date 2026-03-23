# Reading Note - Measurement and Analysis of a Global-Scale CDN – Locality, Dynamics, and Load Balance

**Bibliographic Reference**:
Li, G.-C., & Huang, P. (2025). Measurement and Analysis of a Global-Scale CDN – Locality, Dynamics, and Load Balance. In *Proceedings of the 20th Asian Internet Engineering Conference (AINTEC '25)*, November 25–27, 2025, Manila, Philippines. ACM. https://doi.org/10.1145/3763400.3763406

**Theme**:
This paper presents a large-scale, global measurement study of Twitch's Content Delivery Network (CDN). Using an enhanced version of the open-source Kukudy crawler combined with a commercial VPN service, the authors map 2,166 edge servers across five continents over a 30-day period. The study characterizes three salient CDN properties: geographic locality of server assignment, temporal dynamics in cluster rotation, and uniform load distribution across the hierarchy.

**Relevance to thesis**:
This paper directly illustrates how DNS-based server selection drives CDN performance at a global scale, a central theme of our thesis on distributed DNS measurements. The crawling methodology — rotating through 686 VPN nodes from geographically diverse locations — is methodologically analogous to using RIPE Atlas probes for distributed DNS measurements. The paper's findings on geographic locality and temporal dynamics of CDN server assignments provide empirical grounding for understanding how DNS responses vary in space and time, which is the core research question of our thesis.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.4 (CDN and DNS-based routing)
- Section 2.5 (EDNS Client Subnet and geographic routing)
- Section 3 (Methodology for distributed DNS measurements)

---

## Article Content

### Research Objective(s)

**Problem**: CDN design depends on two factors — the scale and geographic distribution of servers, and the server selection strategy. Empirical knowledge of real-world CDN architectures is scarce, particularly for live video streaming services that have strict latency requirements. Furthermore, existing studies either cover limited geographic regions (primarily Europe) or short time windows.

**Research questions**:
1. How are Twitch's CDN edge servers distributed globally, and what geographic locality does the assignment strategy exhibit?
2. How do server cluster assignments change over time (temporal dynamics), and is the load distributed uniformly across the CDN hierarchy?

### Background

DNS-based CDN server selection relies on the IP address of the DNS recursive resolver to infer the client's geographic location and return the IP address of an appropriate edge server. For live video streaming, latency is particularly critical, making CDN design central to quality of experience. Previous studies have examined CDNs for services like Google, Bing, and Akamai, but live streaming CDNs remain undercharacterized. The Kukudy crawler was previously used to study Twitch's CDN in Europe in 2023; this work extends it globally and longitudinally.

### Methodology

- **Study type**: Active measurement / network crawling
- **Tools used**: Enhanced Kukudy crawler, NordVPN (686 nodes), Twitch public APIs, rDNS lookups via IPinfo.io
- **Scale**: 686 VPN nodes across 5 continents, top 2,000 Twitch channels, 31 daily snapshots over August 15 – September 15, 2024
- **Measurement protocol**: Each VPN node queries Twitch's API for channel URLs; the returned URLs reveal the edge server hostname and cluster. VPN traversal order is randomly shuffled daily to cover peak and off-peak hours. Crawling 2,000 channels per node takes approximately 80 seconds; total crawl time is ~19 hours per daily snapshot.
- **Data collected**: Edge server hostnames (from which cluster IDs and geographic locations are derived), per-viewer server assignments, daily snapshots enabling time-series analysis

### Main Results

1. **Global CDN scale**: 2,166 edge servers in 64 clusters were discovered. Distribution: Europe 1,022 servers (23 clusters), North America 537 (18 clusters), Asia 363 (13 clusters), South America 216 (8 clusters), Oceania 28 (2 clusters). The discovered set represents 57–79% of registered clusters and 35–57% of registered servers per continent, consistent with prior work using Kukudy.
2. **Geographic locality**: Viewers are assigned servers from clusters within the same continent in the vast majority of cases. A continent-level viewer-server heatmap confirms that cross-continental assignments are rare and occur mainly for under-resourced regions (e.g., some Oceania viewers are served from Asia).
3. **Two-level hierarchy**: Server selection operates in two levels — a cluster is first selected from a "super set" of clusters, then an individual edge server is selected within that cluster. This two-level structure is analogous to Akamai's documented architecture.
4. **Temporal dynamics**: The set of active clusters observed on any given day is a subset of a fixed, larger "super set." Different subsets are observed on different days, indicating a slow rotation of clusters in and out of service. This was not quantified in prior Europe-only studies.
5. **Load balancing**: At both levels of the hierarchy, server and cluster selection is close to uniform random, meaning load is distributed approximately evenly. This was confirmed by statistical analysis of the daily assignment data across the 31-day period.

### Authors' Conclusion

The authors conclude that Twitch's CDN operates according to three design principles: continent-level geographic locality, slow temporal rotation of active cluster subsets, and approximately uniform random load balancing at both hierarchy levels. The measurement methodology — daily global crawls with randomized VPN traversal — proves sufficient to characterize these properties efficiently, requiring only the top 2,000 channels (rather than 50,000) to achieve complete CDN coverage. The tool, methodology, and findings are presented as useful baselines for cost-effective long-term CDN monitoring.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- Continent-level geographic locality as the primary dimension of CDN server selection
- Two-level CDN hierarchy (cluster selection followed by individual server selection)
- Temporal dynamics: rotating cluster subsets imply that single-snapshot measurements underestimate CDN scope

**Applicable methods**:
- Randomized traversal of vantage points (VPN nodes / RIPE Atlas probes) to avoid time-of-day bias in measurements
- Coverage saturation analysis: 2,000 channels suffice to achieve 100% CDN server coverage, analogous to determining how many domains suffice for DNS diversity
- rDNS-based validation of actively discovered servers against a ground-truth registry (IPinfo.io)

**Important statistics**:
- 2,166 edge servers in 64 clusters across 5 continents (30-day union)
- Crawling top 2,000 channels reveals 100% of servers observed when crawling all 50,000 channels
- 686 VPN nodes distributed across Europe (349), North America (182), Asia (44), Oceania (24), South America (15)
- ~8 KB download and ~2 KB upload traffic per channel request; total ~200 KB/s downlink, 50 KB/s uplink

**Identified limitations (gaps to fill)**:
- VPN node distribution is biased toward Europe and North America (reflecting NordVPN infrastructure), potentially missing servers in underrepresented regions
- The study does not directly measure DNS responses; CDN server discovery is inferred from Twitch API responses rather than from DNS query/response pairs
- No measurement of end-to-end latency or quality of experience from each vantage point
- The 30-day window may not capture longer-term CDN evolution (e.g., seasonal demand shifts)

### Personal Critique

**Strengths**:
- Most geographically and temporally comprehensive Twitch CDN measurement to date
- Efficient methodology: randomized VPN shuffling removes time-of-day bias; coverage saturation test validates the 2,000-channel threshold
- Clear quantitative characterization of all three CDN properties with supporting data

**Weaknesses**:
- DNS is not directly observed: the paper measures CDN server assignments via application-layer API calls, not by capturing DNS responses. The DNS resolution step is opaque.
- VPN-based vantage points differ fundamentally from RIPE Atlas probes: VPN nodes share /24 subnets within NordVPN's infrastructure, which may not faithfully represent end-user IP diversity
- Comparison with IPinfo.io ground truth shows only 35–57% of registered servers were observed as active, raising questions about what the remaining servers do and when

**Links to other papers**:
- Wang et al. (2018) — DNS-based CDN challenges: provides the theoretical framework for understanding why CDN server selection via DNS degrades when recursive resolvers are remote
- RFC 7871 (ECS) — Contavalli et al. (2016): the EDNS Client Subnet extension that attempts to fix the geographic mismatch this paper implicitly illustrates
- Calder et al. (2015) — ECS-based enumeration of Google's CDN: similar methodology of enumerating CDN servers from diverse vantage points

**Open questions**:
- Would RIPE Atlas probes (which have real, geographically diverse IP addresses rather than VPN-based ones) reveal a different CDN structure for Twitch?
- How does TTL-based caching affect the temporal dynamics observed? If DNS TTLs are short, does the CDN rotation correspond to TTL expiry cycles?

### Key Quotes

> "We conducted a 30-day, global-scale crawl that mapped 2166 edge servers across major continents. The effort, as far as we know, is the most widespread in time-span and geo-diversity in recent years."

> "The system maintains the viewer-server proximity at the continent granularity. There is a slow rotation of the server clusters over time, and the load distribution is approximately uniform random at both levels of the hierarchy."

---

## Use in Thesis

**Relevant sections**:
- Section 2.4 (CDN architectures): Empirical evidence of two-level CDN hierarchy and continent-granularity geographic routing in a major live streaming service
- Section 2.5 (DNS and CDN): Illustration of how CDN server selection is intertwined with DNS resolution and geographic information
- Section 3 (Methodology): Justification for using geographically diverse vantage points and repeated measurements over time; the coverage saturation concept (how many vantage points / domains are sufficient?)

**Points to develop**:
- The gap between VPN-based vantage points and real-user IP addresses: our RIPE Atlas probes close this gap by using real, diverse IP addresses
- The temporal dimension: our thesis emphasizes DNS measurements "in space and time"; the cluster rotation finding provides strong motivation for longitudinal measurements

**Cross-references**:
- `wang2018_dns_cdn_challenges.md` — theoretical context for DNS-CDN interaction
- `rfc7871_edns_client_subnet.md` — the ECS mechanism that addresses geographic mismatch
- `calder2015_anycast_cdn_performance.md` — related CDN measurement methodology

---

**Tags**: #CDN #twitch #live-streaming #server-selection #geographic-locality #measurement #VPN #load-balance #temporal-dynamics
**Status**: [X] Read / [X] Filed
