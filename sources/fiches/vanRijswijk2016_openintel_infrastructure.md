# Reading Note - A High-Performance, Scalable Infrastructure for Large-Scale Active DNS Measurements

**Bibliographic Reference**:
van Rijswijk-Deij, R., Jonker, M., Sperotto, A., & Pras, A. (2016). A High-Performance, Scalable Infrastructure for Large-Scale Active DNS Measurements. *IEEE Journal on Selected Areas in Communications*, 34(6), 1877–1888. https://doi.org/10.1109/JSAC.2016.2558918

**Theme**:
This paper describes the design, implementation, and operational experience of OpenINTEL, a large-scale active DNS measurement infrastructure capable of querying all registered domain names under major top-level domains (TLDs) once per day. The system addresses the engineering challenges of scale (1.85 billion queries per day for .com alone), data storage (240 GB+ per day), and infrastructure impact, while making the resulting dataset publicly available to the research community.

**Relevance to thesis**:
OpenINTEL is one of the two primary large-scale DNS measurement platforms (alongside RIPE Atlas) that our thesis builds upon. While RIPE Atlas measures DNS from geographically distributed vantage points, OpenINTEL provides comprehensive longitudinal coverage of domain-level DNS data. Understanding OpenINTEL's architecture, dataset structure (Apache Avro/Parquet), and coverage is essential for our thesis's methodology chapter and for contextualizing our own measurements within the broader DNS research landscape.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.3 (OpenINTEL — large-scale DNS measurement infrastructure)
- Section 2.1 (DNS fundamentals and measurement challenges)
- Section 3 (Methodology — data sources and complementarity with RIPE Atlas)

---

## Article Content

### Research Objective(s)

**Problem**: The DNS contains enormous amounts of information about Internet operations, security, and evolution, but measuring it comprehensively at scale is extremely challenging. Prior DNS measurement studies had limited scope in terms of time, record types covered, or number of domains. No existing platform performed daily active measurements across the full domain name space of major TLDs.

**Research questions**:
1. How can one perform daily active DNS measurements for all registered domains in a major TLD (specifically .com with 123 million names) without imposing unacceptable load on the global DNS infrastructure?
2. How can the collected data (hundreds of gigabytes per day) be stored and analyzed efficiently over multi-year periods?

### Background

The DNS maps human-readable domain names to machine-readable data (IP addresses, mail server designations, etc.). Its content reveals operational practices (cloud service adoption, protocol deployment), security posture (botnet infrastructure, phishing domains, DNSSEC adoption), and Internet evolution over time. Previous measurement studies were either passive (relying on observed traffic at recursive resolvers) or limited in scope, covering only a subset of TLDs or a small number of record types. The authors target the three largest generic TLDs — .com, .net, and .org — which together cover approximately 50% of the global DNS namespace.

### Methodology

- **Study type**: Infrastructure design and measurement study
- **Tools used**: Custom C-based cluster manager and worker nodes, LDNS (DNS query library), Unbound (local recursive resolver per worker), Apache Avro (raw storage), Apache Parquet (columnar analysis format), Apache Impala (SQL analytics), OpenStack (private cloud VM infrastructure)
- **Scale**: 123 million names in .com; 14 query types per domain per day; estimated 1.85 billion queries per day for .com alone; data collected from March 2015 onward
- **Measurement protocol**: Stage I retrieves daily zone files (AXFR or equivalent) from TLD registry operators; computes daily delta (added/removed domains). Stage II distributes work in chunks to a cloud of worker nodes; each node runs a local Unbound resolver to cache infrastructure data and reduce load on authoritative servers. Worker nodes issue 14 query types (A, AAAA, MX, NS, SOA, TXT, DNSKEY, DS, NSEC, NSEC3, CNAME, etc.) for each domain. Results are enriched with IP-to-AS and GeoIP metadata. Stage III stores results in Avro format and converts to Parquet for analysis.
- **Data collected**: All DNS resource records in the answer section of each query (including DNSSEC signatures and full CNAME chains), with per-domain timestamps enabling daily time series

### Main Results

1. **Performance at scale**: The system successfully measures .com (123M names) within a 24-hour window. Stage II measurement duration scales approximately linearly with TLD size; .org (10M names) is measured in roughly 2 hours, with .com taking proportionally longer. Variability in Stage I running time is caused by intermittent throttling from registry operators.

2. **Infrastructure impact**: By using local Unbound resolvers on each worker node (caching infrastructure data) and distributing queries over multiple authoritative nameservers using Unbound's RTT-based selection, the system keeps per-authoritative-server query rates at acceptable levels. Queries to top-level domain servers are distributed broadly, preventing hotspots. Load is below thresholds that would constitute a distributed denial-of-service scenario.

3. **Storage efficiency**: Apache Avro with compression reduces storage to manageable levels. A two-tiered approach (Avro for long-term archival; Parquet for efficient analysis) allows both standalone analysis tools and Hadoop-based batch analytics. Analyses over 511 billion data points complete in under 2 hours using Apache Impala.

4. **Case study — cloud email adoption**: Using 10 months of data (March 2015 – January 2016), the system reveals that Google dominates cloud email services (via MX records), growing faster than Microsoft and Yahoo. The fraction of domains using cloud email services and the adoption of Sender Policy Framework (SPF) for spam prevention can both be tracked daily.

5. **Data sharing**: The authors commit to making the dataset available to the research community. OpenINTEL data has since been used in dozens of published studies on DNSSEC deployment, IPv6 adoption, botnet infrastructure, and domain abuse.

### Authors' Conclusion

The authors demonstrate that daily active DNS measurement at the scale of the global TLD namespace is feasible with commodity cloud infrastructure and off-the-shelf DNS software. The system avoids the complexity of bare-metal DNS implementations while achieving sufficient throughput, and its impact on the global DNS infrastructure is acceptable. The resulting dataset is uniquely valuable for studying Internet evolution over time. Open data access is presented as a key contribution to the research community.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- The distinction between active DNS measurement (querying authoritative servers directly, as OpenINTEL does) and passive DNS measurement (observing traffic at recursive resolvers): our thesis uses both via OpenINTEL (active, comprehensive) and RIPE Atlas (active, geographically distributed)
- Daily temporal granularity as the baseline for tracking DNS evolution — enables detection of changes in CDN assignments, DNSSEC deployment, and domain abuse
- The challenge of pacing measurements to avoid overloading authoritative nameservers: this ethical constraint is analogous to the rate-limiting considerations we must apply with RIPE Atlas

**Applicable methods**:
- Apache Avro schema design for DNS records: directly relevant to our data processing pipeline for RIPE Atlas measurement results
- Zone file ingestion (AXFR) as a source of domain names: complements our Tranco-based domain selection
- Multi-tier storage strategy (raw format + columnar analysis format): applicable to our own data pipeline

**Important statistics**:
- .com TLD: 123 million registered names at time of measurement (2015–2016)
- 14 query types performed per domain per day
- Estimated 1.85 billion queries per day for .com alone
- ~240 GB of raw data per day for .com
- 511 billion data points analyzed in under 2 hours using Apache Impala
- .com, .net, .org together comprise ~50% of the global DNS namespace

**Identified limitations (gaps to fill)**:
- OpenINTEL queries from a single (or limited number of) vantage points: it captures the global DNS namespace but not geographic variation in DNS responses
- No measurement of how responses differ depending on the querying IP address (i.e., no geographic diversity in query sources) — this is precisely the gap that RIPE Atlas fills
- TTL values and caching behavior are observed but the system cannot control them; fresh data collection depends on resolver cache expiry

### Personal Critique

**Strengths**:
- Engineering rigor: every design choice (DNS software, scalability approach, data format) is motivated by explicit goals and trade-offs
- Practical validation through case studies: cloud email adoption trends demonstrate the dataset's research value
- Open data access philosophy: by making data available, the authors multiply the impact of the infrastructure

**Weaknesses**:
- Single geographic vantage point: OpenINTEL measures what a domain publishes globally, not what different users see depending on their location (CDN-related geographic variation is invisible)
- Zone file dependency: measuring .com requires access to the ICANN-regulated zone file, which is available under contract. ccTLDs without public zone files cannot be measured this way
- The paper focuses on infrastructure; in-depth analysis of the collected data (trends, security findings) is deferred to subsequent publications

**Links to other papers**:
- van der Toorn et al. (2018) — Snowshoe spam detection: directly uses the OpenINTEL dataset to detect malicious domain configurations at scale
- van Rijswijk-Deij et al. (2018) — OpenINTEL ongoing (SIGCOMM IMC): follow-up paper documenting extended coverage and research applications
- RIPE Atlas papers: RIPE Atlas provides the geographic dimension that OpenINTEL lacks; the two platforms are complementary

**Open questions**:
- How does OpenINTEL's coverage (currently 60%+ of global namespace) compare to Tranco top-N domain lists? Is there significant overlap between high-Tranco-ranked domains and those covered by OpenINTEL?
- Can OpenINTEL data be used to pre-screen which domains exhibit geographic DNS variation (e.g., via CNAME to CDN providers) before issuing targeted RIPE Atlas measurements?

### Key Quotes

> "The Domain Name System (DNS), plays a crucial role in the day-to-day operation of the Internet. It performs the vital task of translating human readable names – such as www.example.com – into machine readable information."

> "Our research goal is to perform daily active measurements of all domains in the main top-level domains (TLDs) on the Internet (including .com, .net and .org, together comprising 50% of the global DNS name space) and to collect this data over long periods of time potentially spanning multiple years."

> "The analyses we performed for the case studies discussed in Section V took under 2 hours each, processing over 511 billion data points."

---

## Use in Thesis

**Relevant sections**:
- Section 2.3 (OpenINTEL): Primary reference for describing the OpenINTEL platform — its architecture, scale, data formats, and research value
- Section 2.1 (DNS measurement challenges): The 14 query types, pacing constraints, and storage challenges described here are directly relevant to general DNS measurement methodology
- Section 3 (Methodology): Justification for using OpenINTEL data as a complement to RIPE Atlas; explanation of Avro/Parquet data formats in our pipeline

**Points to develop**:
- The complementarity between OpenINTEL (broad coverage, single vantage point) and RIPE Atlas (geographic diversity, targeted domains): our thesis exploits both dimensions
- How to select a domain list from the Tranco top rankings that maximizes overlap with OpenINTEL coverage for cross-validation

**Cross-references**:
- `vanderToorn2018_snowshoe_spam_dns.md` — downstream use of OpenINTEL data for security research
- `vanRijswijk2018_openintel_ongoing.md` — extended OpenINTEL coverage and methodology updates
- `lePochat2019_tranco_ranking.md` — domain list selection; Tranco vs. zone-file-based domain selection

---

**Tags**: #OpenINTEL #active-DNS #large-scale #TLD #infrastructure #Avro #Parquet #Hadoop #DNSSEC #longitudinal
**Status**: [X] Read / [X] Filed
