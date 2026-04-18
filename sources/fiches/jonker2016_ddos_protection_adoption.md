# Reading Note - Measuring the Adoption of DDoS Protection Services

**Bibliographic Reference**:
Jonker, M., Sperotto, A., van Rijswijk-Deij, R., Sadre, R., & Pras, A. (2016). Measuring the adoption of DDoS protection services. *Proceedings of the 2016 ACM Internet Measurement Conference (IMC '16)*, 279–285. https://doi.org/10.1145/2987443.2987487

**Theme**:
First large-scale, longitudinal study of the adoption of cloud-based DDoS Protection Services (DPS), using 1.5 years of active DNS measurements covering >50% of the global namespace. Identifies DNS-based traffic diversion as the key observable indicator of DPS adoption, and reveals that adoption is led by large web hosters rather than individual domain owners.

**Relevance to thesis**:
Demonstrates that active DNS measurement at scale (via OpenINTEL) can reveal not just DNS resolution behaviour but also higher-level infrastructure decisions (security outsourcing). Directly cited in the thesis as a use case for OpenINTEL longitudinal data showing adoption trends invisible to passive or point-in-time measurement.

---

## Reading Context

**Date**: April 2026
**Thesis sections**:
- Section 2.2 (DNS Measurement Paradigms — OpenINTEL use case)
- Section 2.3 (CDN/anycast routing — DNS-based traffic diversion)

---

## Article Content

### Research Objective(s)

**Problem**: DDoS Protection Services (DPS) redirect client traffic through cleansing infrastructure, typically via DNS-based traffic diversion (changing DNS records to point to DPS infrastructure). Whether adoption of these services was growing, who was adopting them, and at what rate was unknown at population scale.

**Research questions**:
1. How widespread is the adoption of cloud-based DPS among popular domains?
2. What traffic diversion mechanisms (DNS CNAME/A record changes, BGP) are most used?
3. Who drives adoption — individual domain owners or large hosting providers?

### Background

DDoS attacks have grown steadily in frequency and intensity. Cloud-based DPS providers (Akamai, Cloudflare, Incapsula, Neustar, Verisign, etc.) offer traffic diversion services: during an attack, DNS records are updated to route traffic through the DPS scrubbing infrastructure before forwarding clean traffic to the origin. This DNS-mediated diversion leaves a detectable fingerprint in DNS responses — specifically in A records (pointing to DPS IP ranges) or CNAME records (pointing to DPS-managed names) — making active DNS measurement an effective observation tool.

### Methodology

- **Data source**: OpenINTEL daily snapshots of .com, .net, .org (1.5 years), and .nl (6 months); Alexa Top 1M
- **DPS identification**: DNS fingerprinting — matching A records against known DPS IP ranges and CNAME patterns for 9 providers (Akamai, CenturyLink, Cloudflare, DOSarrest, F5, Incapsula, Level 3, Neustar, Verisign)
- **Scale**: ~100 million domain names per day over 1.5 years
- **Analysis**: Adoption rate over time; provider market share; domain owner type (individual vs. large hoster)

### Main Results

1. DPS adoption grew by **1.24×** over the 1.5-year measurement period, against only 1.09× growth of the overall namespace — adoption outpaces namespace growth
2. **Cloudflare** dominates by number of domains protected; Akamai leads in terms of traffic volume
3. Adoption is driven primarily by **large web hosters and domainers** activating/deactivating protection in bulk, not by individual domain owners
4. DNS-based diversion (CNAME and A-record changes) is the dominant mechanism; BGP-based diversion is rarer
5. On-demand activation patterns are visible: some domains switch DPS protection on and off in response to attack events

### Authors' Conclusion

DPS adoption is growing faster than the namespace itself, with a small number of large providers capturing most of the market. The DNS fingerprinting approach is effective for population-scale monitoring of DPS deployment. Future work should correlate DPS activation events with DDoS attack reports to validate temporal patterns.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- DNS records (A, CNAME) as observable indicators of infrastructure decisions beyond simple name resolution
- OpenINTEL longitudinal data enables population-scale adoption trend analysis
- DNS-based traffic diversion is the dominant DPS mechanism, linking this work to CDN routing concepts in Chapter 2

**Important statistics**:
- 1.24× DPS adoption growth over 1.5 years (vs 1.09× namespace growth)
- 9 major DPS providers studied
- Dataset covers >50% of global namespace in daily snapshots

**Identified limitations**:
- BGP-based diversion not directly observable via DNS
- DPS identification relies on IP range and CNAME heuristics that may miss new providers
- Cannot distinguish on-demand from always-on protection from DNS data alone

### Personal Critique

**Strengths**:
- Clean, intuitive methodology (DNS fingerprinting of DPS infrastructure)
- Large-scale and longitudinal — credible population-level estimates
- Practical relevance: reveals market dynamics of a growing security sector

**Weaknesses**:
- Coverage limited to .com/.net/.org/.nl — country-code TLDs largely excluded
- Heuristic-based DPS identification may produce false positives/negatives for new providers
- Cannot measure DPS effectiveness (only adoption)

**Links to other papers**:
- van Rijswijk-Deij 2016 (OpenINTEL infrastructure): Data platform used in this study
- Chung 2017 (DNSSEC ecosystem): Parallel OpenINTEL use case for security infrastructure monitoring
- Li 2025 / Hours 2016 (CDN routing): DNS-based traffic diversion mechanisms overlap with CDN routing techniques

### Key Quotes

> "Our results show that DPS adoption has grown by 1.24× during our measurement period, a prominent trend compared to the overall expansion of the namespace."

> "Our study also reveals that adoption is often led by big players such as large Web hosters, which activate or deactivate DDoS protection in bulk."

---

## Use in Thesis

**Relevant sections**:
- Section 2.2 (OpenINTEL): Cite as second concrete use case of longitudinal OpenINTEL data — DDoS protection adoption tracking invisible to passive or point-in-time measurement
- Section 2.3 (CDN/anycast): DNS-based traffic diversion mechanism is shared with CDN routing

**BibTeX key**: `Jonker2016`

---

**Tags**: #ddos #protection-services #dns #openintel #longitudinal #cloudflare #traffic-diversion #adoption
**Status**: [X] Read / [X] Filed
