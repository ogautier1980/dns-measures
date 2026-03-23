# Reading Note - The Ongoing Story of OpenINTEL: Measuring the DNS for Research, Policy and Protocol Improvements

**Bibliographic Reference**:
van Rijswijk-Deij, R. (2018, December 4). The Ongoing Story of OpenINTEL: Measuring the DNS for Research, Policy and Protocol Improvements. *NLnet Labs Blog*. https://blog.nlnetlabs.nl/the-ongoing-story-of-openintel/

**Theme**:
This blog post chronicles the development and expansion of OpenINTEL, a large-scale active DNS measurement platform that performs daily forward DNS measurements across major TLDs. The post covers the project's origins in DDoS defense research, its technical evolution from a two-institution prototype to a four-partner infrastructure spanning all generic TLDs, and highlights three landmark academic publications that resulted from its data. It also outlines planned technical improvements for 2019.

**Relevance to thesis**:
OpenINTEL is one of the two primary data sources conceptually underpinning this thesis (alongside RIPE Atlas). As a centralized platform performing exhaustive daily DNS measurements across hundreds of millions of domain names, it represents the "space" (TLD-wide coverage) and "time" (daily snapshots since February 2015) dimensions of DNS measurement at scale. Understanding its architecture, history, and published results directly informs our state of the art chapter and frames the complementarity between OpenINTEL's exhaustive approach and RIPE Atlas's geographically distributed approach.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.3 (OpenINTEL: large-scale passive DNS measurement)
- Section 2.8 (Synthesis and identified gaps)
- Section 4 (Methodology: rationale for combining OpenINTEL-style coverage with RIPE Atlas distribution)

---

## Article Content

### Research Objective(s)

**Problem**: DNS measurement research historically suffered from a lack of continuous, comprehensive, longitudinal data. Passive DNS systems capture only queries that happen to pass through participating resolvers, introducing selection bias. There was no platform performing active daily measurements across the full forward DNS of major TLDs at scale, preventing researchers from tracking DNS changes over time (DNSSEC adoption, CDN delegation patterns, spam campaign infrastructure, etc.).

**Research questions**:
1. How can active DNS measurement be performed at the scale of hundreds of millions of domain names per day in a resource-efficient way?
2. What research questions about DNS security, protocol adoption, and infrastructure evolution become tractable with longitudinal daily DNS data?
3. How should such a measurement infrastructure evolve to support increasingly diverse research needs (RTT, TTL accuracy, DNS stability)?

### Background

OpenINTEL was conceived at the University of Twente (Netherlands) in summer 2014, motivated by an investigation into DDoS protection services and the insight that "what is in the DNS says a lot about how the Internet is used." The founding vision was to build a continuously updated, comprehensive database of forward DNS records that would enable longitudinal studies impossible with passive DNS or one-shot measurement campaigns. The project received institutional backing from SIDN (the .nl registry), SURFnet (the Dutch research network), and later NLnet Labs, creating a public-interest research consortium. The platform received the Research Data Netherlands Prize in November 2018, affirming its value to the academic community.

### Methodology

- **Study type**: Longitudinal active DNS measurement platform (infrastructure description and results summary)
- **Tools used**: LDNS (DNS query library), Unbound (recursive resolver), Hadoop cluster (data storage and processing), custom measurement software
- **Scale**:
  - Launch (February 2015): .com, .net, .org TLDs
  - 2015-2017: expanded to major ccTLDs, additional gTLDs, infrastructure measurements
  - 2018: all gTLDs, NLnet Labs joins as fourth partner
  - Daily measurement volume: hundreds of millions of domain names per day
- **Measurement protocol**: Active forward DNS queries sent daily for every domain name listed in TLD zone files. Queries cover multiple record types (A, AAAA, NS, MX, SOA, DNSKEY, DS, RRSIG, etc.). Results stored in Hadoop for longitudinal analysis. All measurements performed from a single location in the Netherlands.
- **Data collected**: Forward DNS records for all queried domains, with timestamps enabling before/after and trend analysis; from 2019: RTT per query, accurate TTL recording

### Main Results

1. **Timeline and growth**: First complete measurement day: February 21, 2015. Regular daily measurements started March 1, 2015. Hadoop cluster added September 2015 for scalable storage. By 2016-2017, platform covered ccTLDs and gTLDs beyond the original three. By 2018, all gTLDs were included and NLnet Labs had joined as the fourth institutional partner.
2. **DDoS protection research (IMC 2016)**: Using 1.5 years of OpenINTEL data, Mattijs Jonker et al. studied the adoption of DDoS protection services across the DNS landscape, revealing patterns in how domains migrate to protection providers and the concentration of DDoS mitigation infrastructure.
3. **DNSSEC 21-month study (USENIX Security 2017, Distinguished Paper Award)**: A longitudinal analysis of DNSSEC deployment and key management practices over 21 months revealed widespread misconfiguration and key rollover failures that left supposedly DNSSEC-protected domains vulnerable — findings only possible through continuous longitudinal measurement.
4. **Snowshoe spam detection (NOMS 2018, Best Paper Award)**: Van der Toorn et al. demonstrated that DNS data from 180 days of OpenINTEL measurements could detect snowshoe spam campaigns up to several days before they were identified by traditional spam detection systems — an early warning capability with direct operational value.
5. **Planned 2019 improvements**: Infrastructure replacement for higher throughput; addition of RTT measurement per DNS query (enabling latency analysis); accurate TTL recording (previously approximated); DNS stability and hijacking detection capabilities.

### Authors' Conclusion

OpenINTEL has established itself as a unique research infrastructure for the global DNS community, enabling longitudinal studies that reveal DNS behavior over timescales of months to years. The three award-winning publications demonstrate that continuous comprehensive DNS measurement unlocks research questions inaccessible to passive DNS or one-shot studies. The platform's expansion to all gTLDs and the addition of NLnet Labs as a partner in 2018 mark its transition from a prototype to a mature research infrastructure. Future work will add RTT and TTL dimensions to the dataset, further expanding the analytical surface.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- "What is in the DNS says a lot about how the Internet is used" — foundational motivation applicable to our thesis
- Active vs. passive DNS measurement distinction: OpenINTEL is active (sends queries) and thus comprehensive for listed domains; passive DNS only captures organic queries
- Longitudinal measurement as the enabler of temporal analysis — daily snapshots over months/years reveal trends invisible to point-in-time studies
- TLD zone file as the source of domain names to measure: a different (and more exhaustive) domain selection approach than the Tranco popularity ranking

**Applicable methods**:
- Daily recurring measurement runs rather than one-shot campaigns, to enable before/after and trend analysis
- Multi-record-type querying per domain (A, AAAA, NS, MX, DNSKEY) to capture the full DNS profile rather than a single record
- Storing raw results with timestamps in a structured format (Parquet/Hadoop) for longitudinal querying

**Important statistics**:
- First measurement: February 21, 2015 — over 10 years of longitudinal data as of our thesis writing
- 21 months of DNSSEC data sufficient to reveal systemic key management failures (USENIX Security 2017)
- 180 days of data sufficient for snowshoe spam early warning (NOMS 2018)
- 1.5 years of data for DDoS protection service adoption analysis (IMC 2016)

**Identified limitations (gaps to fill)**:
- Single geographic vantage point (Netherlands): all measurements are performed from one location, meaning geographic variation in DNS responses (CDN anycast, geolocation-based routing, EDNS Client Subnet effects) is invisible — this is the core gap our thesis fills with RIPE Atlas
- Coverage limited to TLD-listed domains: domains not listed in zone files (some ccTLDs with restricted zone file access) are not measured
- RTT and TTL accuracy were limitations acknowledged as of 2018 (addressed in 2019 planned work)

### Personal Critique

**Strengths**:
- Three peer-reviewed award-winning publications validate the platform's research value (IMC, USENIX Security, NOMS)
- Long time series (10+ years) is irreplaceable for trend analysis
- Institutional backing (SIDN, SURFnet, NLnet Labs, UTwente) ensures continuity and credibility
- Open data policy enables reproducibility and third-party research

**Weaknesses**:
- Blog post format: lacks the methodological rigor of a peer-reviewed paper (no measurement bias analysis, no comparison with alternative approaches)
- No discussion of measurement overhead or impact on measured name servers (ethical measurement considerations)
- Geographic monoculture (single Netherlands vantage point) is the platform's fundamental limitation for spatial DNS analysis

**Links to other papers**:
- Van Rijswijk-Deij et al. (IMC 2016, OpenINTEL original paper): the peer-reviewed companion to this blog post, with full methodology
- Nosyk et al. 2024 (RIPE Atlas DITL): RIPE Atlas provides the geographic distribution that OpenINTEL lacks; the two platforms are complementary
- Jonker et al. (IMC 2016, DDoS protection): first published result from OpenINTEL data

**Open questions**:
- How does OpenINTEL's single-vantage-point measurement compare to what RIPE Atlas probes observe for the same domain — do the DNS responses differ by location?
- With RTT now recorded per query (post-2019), can OpenINTEL data be used to infer anycast instance selection without geographic probing diversity?

### Key Quotes

> "What is in the DNS says a lot about how the Internet is used."

> "OpenINTEL received the Research Data Netherlands Prize in November 2018."

> "The DNSSEC study over 21 months [received a] USENIX Security 2017 Distinguished Paper Award — findings only possible through continuous longitudinal measurement."

> "Van der Toorn et al. demonstrated that DNS data from 180 days could detect snowshoe spam campaigns up to several days before traditional detection systems."

---

## Use in Thesis

**Relevant sections**:
- Section 2.3 (OpenINTEL): Full description of the platform, its history, architecture, and published results as a key reference for large-scale DNS measurement methodology
- Section 2.8 (Synthesis): Position OpenINTEL as the state-of-the-art in exhaustive longitudinal DNS measurement, and identify the single-vantage-point limitation as the gap our thesis addresses
- Section 4 (Methodology): Contrast OpenINTEL's approach (TLD zone files, single point, all domains) with our approach (Tranco list, RIPE Atlas distributed probes, popular domains)

**Points to develop**:
- The complementarity table: OpenINTEL (exhaustive, centralized, longitudinal) vs. RIPE Atlas (sampled, distributed, geographic) — our thesis combines the temporal depth inspiration of OpenINTEL with the spatial diversity of RIPE Atlas
- Use the DDoS, DNSSEC, and spam results as motivating examples of what longitudinal DNS data enables

**Cross-references**:
- Fiche Nosyk 2024 (RIPE Atlas DITL): the geographic complement to OpenINTEL
- Fiche Xu 2023 (DNS centralization): server-side centralization findings from zone file analysis, methodologically adjacent to OpenINTEL

---

**Tags**: #openintel #dns #longitudinal-measurement #active-measurement #dnssec #ddos #spam-detection #nlnetlabs #temporal-analysis
**Status**: [X] Read / [X] Filed
