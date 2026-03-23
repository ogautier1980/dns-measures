# Reading Note - Analyzing the Performance of an Anycast CDN

**Bibliographic Reference**:
Calder, M., Flavel, A., Katz-Bassett, E., Mahajan, R., & Padhye, J. (2015). Analyzing the performance of an anycast CDN. *Proceedings of the 2015 Internet Measurement Conference (IMC '15)*, 531–537. https://doi.org/10.1145/2815675.2815717

**Theme**:
This paper examines the performance implications of using IP anycast for client-to-front-end redirection in a large-scale, latency-sensitive CDN (Bing Search). It compares anycast-selected front-ends against geographically optimal unicast front-ends using both passive server-side logs and active JavaScript-beacon measurements from millions of real clients. It further tests whether a history-based prediction scheme can identify clients poorly served by anycast and redirect them via DNS instead.

**Relevance to thesis**:
This paper is directly relevant to a DNS measurements thesis because anycast is the dominant delivery architecture for global DNS resolver infrastructure (e.g., root servers, large public resolvers). The performance analysis of anycast routing — including the finding that ~20% of clients are directed to suboptimal servers — directly informs how DNS query latency varies across geographic locations. The use of RIPE Atlas traceroutes to diagnose poor anycast routing cases also illustrates a complementary use of the platform alongside passive CDN measurement data.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.2 (Anycast in DNS infrastructure)
- Section 2.5 (CDN DNS redirection: EDNS Client Subnet and anycast)
- Section 4.X (Analysis of DNS resolution latency variation by location)

---

## Article Content

### Research Objective(s)

**Problem**: Anycast is increasingly used by CDNs (and by DNS infrastructure operators) as an operationally simple alternative to DNS-based unicast redirection. However, anycast defers routing decisions to BGP, which is performance-agnostic, potentially directing clients to suboptimal front-ends. The performance cost of this lack of control has not been systematically quantified for a production, latency-sensitive CDN.

**Research questions**:
1. How often does anycast direct clients to a suboptimal front-end, and by how much does this degrade latency?
2. Can the anycast inefficiencies be predicted from historical data to enable targeted DNS-based redirection for affected clients?
3. What are the structural causes of poor anycast routing for specific client populations?

### Background

CDNs direct clients to front-end servers using two primary mechanisms: DNS-based unicast redirection (pioneered by Akamai) and IP anycast. DNS redirection requires complex global traffic management infrastructure but allows fine-grained, near-real-time control at LDNS granularity. EDNS Client Subnet (ECS) partially addresses the LDNS-client distance problem by forwarding a portion of the client's IP address to the authoritative resolver. Anycast is simpler to operate — the same IP prefix is announced from multiple locations, and BGP routes each client to the nearest replica according to BGP path metrics. Companies including Cloudflare, CacheFly, Edgecast, and Microsoft use anycast CDNs. Well-known challenges of anycast include its unawareness of network performance, server load, and the risk of cascading overload when withdrawing a route.

### Methodology

- **Study type**: Measurement study combining passive and active data; production CDN experiment
- **Tools used**: Bing server-side logs; JavaScript beacon injected into Bing search result pages; custom authoritative DNS infrastructure; RIPE Atlas (for traceroute-based diagnostic case studies); W3C Resource Timing API
- **Scale**: Millions of search queries over March–April 2015; Bing CDN with dozens of front-end locations worldwide; measurements aggregated by /24 client prefix; data weighted by query volume from each prefix
- **Measurement protocol**:
  - *Passive*: Bing server logs record client IP, location, and which front-end was selected by anycast, for every search query in the first week of April 2015
  - *Active*: JavaScript beacon injected into a small fraction of search results; after page load, the beacon measures TCP-level latency to four URLs: (a) the anycast-selected front-end, (b) the geographically closest front-end (by geolocation of the LDNS), and (c-d) two randomly selected front-ends from the 10 closest candidates (weighted by proximity); results reported to a backend using a globally unique per-URL identifier to join HTTP and DNS log data
- **Data collected**: Client-to-front-end latency (anycast vs unicast); front-end selection geography; /24-level aggregated performance distributions

### Main Results

1. **Anycast performance is mostly good but not universally so**: For the majority of clients, anycast performs comparably to the best available unicast front-end. However, anycast is at least 25 ms slower than the best unicast alternative for approximately 20% of client requests, and at least 100 ms slower for nearly 10% of requests.
2. **Suboptimal routing is stable**: The clients poorly served by anycast tend to be consistently directed to the same suboptimal front-end over time. This stability makes the inefficiency predictable.
3. **History-based prediction is effective**: A simple prediction scheme using historical anycast performance data can identify 15–20% of clients who would benefit from DNS-based redirection to a better front-end. Applying DNS redirection for these clients improves their performance while allowing the remaining 80–85% to continue using anycast.
4. **Structural causes of poor routing**: Two common patterns were identified using RIPE Atlas traceroutes from within the same ISP-metro areas as affected clients: (a) BGP's lack of insight into underlying network topology causes anycast to route clients through a suboptimal path to a distant front-end despite a geographically closer one being available; (b) clients enter the CDN's backbone at an inefficient peering point and traverse long internal paths.
5. **CDN size context**: The Bing CDN has dozens of front-end locations — a scale similar to other major CDNs (Level3: 62 locations, Cloudflare: 43 locations, EdgeCast: 31 locations). The median distance from a client (weighted by Bing query volume) to the nearest front-end is 280 km, to the second nearest is 700 km, and to the fourth nearest is 1,300 km.
6. **RIPE Atlas complementary role**: RIPE Atlas traceroutes issued from probes within the same ISP-metro areas as poorly-served Bing clients revealed routing anomalies that explain the latency penalties, demonstrating the value of combining production CDN data with independent measurement infrastructure.

### Authors' Conclusion

Anycast CDN routing delivers good performance for the majority of clients, but approximately 20% experience measurable latency penalties due to BGP's performance-agnostic routing decisions. These inefficiencies are stable enough to be predicted from historical data, enabling a hybrid approach where DNS-based redirection improves performance for underserved clients while anycast continues to serve the majority. The authors position this as the first systematic study of anycast performance in a production, latency-sensitive CDN, and note that their conclusions are specific to the Bing CDN's current front-end deployment geography.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- Anycast routing inefficiency: approximately 20% of clients are directed to suboptimal servers by BGP, with latency penalties exceeding 25 ms — a finding applicable to anycast DNS resolver deployments
- The stability of anycast routing patterns: the same clients tend to be consistently mis-routed, making performance prediction feasible
- RIPE Atlas as a diagnostic complement to production CDN measurement data (traceroutes from probes within specific ISP-metro areas)

**Applicable methods**:
- Comparing anycast-selected server latency against geographically optimal unicast latency as a measure of anycast routing efficiency — this approach can be adapted for anycast DNS root server studies
- Aggregating client measurements by /24 prefix to balance statistical robustness with geographic granularity
- Using RIPE Atlas traceroutes to diagnose specific routing anomalies identified in production measurements

**Important statistics**:
- ~20% of clients experience anycast latency at least 25 ms worse than the best unicast alternative
- ~10% of clients experience anycast latency at least 100 ms worse than the best unicast alternative
- DNS-based redirection can improve performance for 15–20% of clients using a history-based prediction scheme
- Median distance from Bing clients (weighted by query volume) to nearest front-end: 280 km; to second nearest: 700 km

**Identified limitations (gaps to fill)**:
- The study is specific to Bing's CDN deployment; generalising to other CDN sizes, front-end distributions, or anycast deployments (especially DNS infrastructure like root servers or large public resolvers) requires additional work
- The JavaScript beacon measurement does not capture DNS lookup latency (it is explicitly excluded to isolate path latency); DNS resolution time itself is not measured
- RIPE Atlas is used only for diagnostic traceroutes on specific problem cases, not as a primary measurement source

### Personal Critique

**Strengths**:
- Rare access to production CDN data at massive scale (millions of queries) combined with active client-side measurements gives unusually high statistical power
- The hybrid anycast + DNS redirection proposal is practically actionable and directly demonstrated to be effective
- RIPE Atlas used creatively for diagnosis rather than as the primary measurement platform

**Weaknesses**:
- Results are tied to a specific CDN (Bing) and a specific time period (March–April 2015); the front-end geography and routing environment may have changed since
- The active beacon measurement excludes DNS resolution latency, meaning the total user-perceived latency improvement from DNS redirection is not fully captured
- The paper is a short paper (7 pages); many methodological details are necessarily brief

**Links to other papers**:
- Cicalese et al. (CoNEXT 2015, anycast census): Provides the broad Internet-scale context for anycast deployment that this CDN-specific study lacks
- Koch et al. (anycast context): Examines how geographic routing context affects anycast performance interpretation
- Hours et al. (DNS resolvers and CDN impact): Studies the DNS resolver side of the CDN redirection problem from a complementary angle

**Open questions**:
- How does the ~20% anycast mis-routing rate compare for anycast DNS infrastructure (root servers, public resolvers) vs anycast CDN front-ends?
- Has the growth of EDNS Client Subnet (ECS) adoption since 2015 reduced the frequency of anycast routing inefficiencies for DNS-using CDNs?

### Key Quotes

> "We find that anycast usually performs well despite the lack of precise control but that it directs roughly 20% of clients to a suboptimal front-end."

> "The anycast inefficiencies are stable enough that we can use a simple prediction scheme to drive DNS redirection for clients underserved by anycast, improving performance of 15%-20% of clients."

> "We used the RIPE Atlas testbed, a network of over 8000 probes predominantly hosted in home networks. We issued traceroutes from Atlas probes hosted within the same ISP-metro area pairs where we have observed clients with poor performance."

---

## Use in Thesis

**Relevant sections**:
- Section 2.2 (DNS anycast infrastructure): Cite the 20% mis-routing finding as evidence that anycast routing is not performance-optimal by design, with direct implications for DNS resolver and root server infrastructure
- Section 2.5 (CDN redirection mechanisms): Discuss as context for why DNS-based redirection (and ECS) remain relevant even in an anycast world
- Section 4.X (Results): If measuring latency variation across RIPE Atlas probes to anycast DNS targets, this paper provides a methodological and empirical baseline

**Points to develop**:
- Discuss whether the anycast mis-routing patterns observed for CDNs also apply to anycast DNS infrastructure (root servers, large public resolvers)
- Use the CDN front-end distance statistics (median 280 km to nearest) as a comparator for DNS resolver proximity

**Cross-references**:
- `cicalese2015_anycast_census.md`: Internet-scale anycast census complementing this CDN-specific study
- `hours2016_dns_resolvers_cdn_impact.md`: DNS resolver impact on CDN server selection
- `koch2021_anycast_context.md`: Anycast routing context and geographic interpretation

---

**Tags**: #anycast #cdn #dns-redirection #performance #ripe-atlas #bgp #measurement #bing #edns-client-subnet
**Status**: [X] Read / [X] Filed
