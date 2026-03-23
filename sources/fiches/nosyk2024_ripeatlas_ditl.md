# Reading Note - Day in the Life of RIPE Atlas: Operational Insights and Applications in Network Measurements

**Bibliographic Reference**:
Nosyk, Y., Tashiro, M., Lone, Q., Kisteleki, R., Duda, A., & Korczyński, M. (2024). Day in the Life of RIPE Atlas: Operational Insights and Applications in Network Measurements. *arXiv preprint* arXiv:2511.22474v1. https://arxiv.org/html/2511.22474v1

**Theme**:
This paper provides the first systematic operational analysis of the RIPE Atlas distributed measurement platform, characterizing its infrastructure (probes, anchors, measurement types, geographic distribution) using a full 24-hour dataset from February 21, 2024. It combines quantitative characterization with five practical case studies demonstrating how the platform can be used for DNS manipulation detection, routing analysis, IPv6 compliance, and regional connectivity mapping.

**Relevance to thesis**:
RIPE Atlas is the primary measurement infrastructure for this thesis on distributed DNS measurements in space and time. This paper provides authoritative operational data on the platform's capabilities, geographic biases, and best practices for DNS measurement campaigns. It supplies concrete statistics (12,900 probes, 178 countries, 88,000 daily DNS measurements) that directly inform the methodology chapter's probe selection strategy and the discussion of geographic representativeness limitations.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.4 (RIPE Atlas platform — state of the art)
- Section 4 (Methodology: probe selection, credit optimization, reproducibility)
- Section 7 (Discussion: geographic bias limitations)

---

## Article Content

### Research Objective(s)

**Problem**: RIPE Atlas has operated for approximately 15 years and is widely used in network measurement research, yet no prior study had systematically characterized its operational properties — how measurements are distributed by type, which geographies are represented, what the typical measurement volume is, and what the platform's structural biases are. This gap makes it difficult for researchers to use the platform efficiently or to assess the representativeness of their results.

**Research questions**:
1. What is the operational profile of RIPE Atlas in terms of infrastructure, measurement types, and geographic distribution of vantage points?
2. How are measurement credits used across user-defined, anchor mesh, and built-in measurement categories, and what is the efficiency of each?
3. What practical applications can be demonstrated using existing RIPE Atlas measurements, particularly for DNS and routing analysis?

### Background

The Internet is a critical shared infrastructure whose behavior is increasingly difficult to observe from any single vantage point. Distributed measurement platforms — RIPE Atlas, M-Lab, CAIDA Ark — address this by aggregating observations from geographically diverse hosts. RIPE Atlas, operated by the RIPE NCC, consists of lightweight hardware probes deployed voluntarily in homes, universities, and ISPs worldwide, plus higher-capacity anchors hosted by institutions. Probes support ping, traceroute, DNS, TLS, HTTP, and NTP measurements, accessible via a public REST API with a credit-based system. Prior work has used RIPE Atlas for specific case studies (BGP routing, CDN performance, DNS censorship), but the platform's own operational characteristics had never been studied as a primary research object.

### Methodology

- **Study type**: Empirical large-scale analysis with five applied case studies
- **Tools used**: RIPE Atlas REST API (data collection), MaxMind GeoLite2 (IP geolocation), Python (statistical analysis)
- **Scale**: 12,892 active probes + 810 active anchors; 178 countries; 50,885 unique measurements; >1.3 billion results in 24 hours
- **Measurement protocol**: A representative 24-hour window (February 21, 2024) was selected based on normal operational metrics. All measurements active that day were retrieved via the API and classified by type (User-Defined, Anchor Mesh, Built-in), measurement protocol (DNS, ping, traceroute, HTTP, TLS, NTP), and geographic properties.
- **Data collected**: Per-probe country and AS assignment, IPv4/IPv6 dual-stack status, measurement type distributions, result counts per measurement category, geographic coverage per region and continent

### Main Results

1. **Geographic concentration**: Germany and the United States together account for 28% of all probes and anchors. Thirty-four countries have only a single probe or anchor. Coverage is strong in Europe and North America but severely limited in Africa, South Asia, and South America — a structural bias inherited from the volunteer deployment model.
2. **IPv6 adoption asymmetry**: 46.5% of standard probes support dual-stack (IPv4 + IPv6), compared to 92% of anchors. This reflects the institutional hosting of anchors versus residential hosting of probes, where ISP IPv6 deployment varies widely.
3. **DNS as a dominant measurement type**: On February 21, 2024, approximately 88,000 DNS measurements were active — on par with ping (87,900) and far exceeding traceroute. DNS measurements are thus one of the two most common use cases on the platform.
4. **Anchor mesh efficiency**: User-defined measurements account for 76.7% of total measurement count but generate a minority of results. Anchor mesh measurements, though fewer in number, generate 67.5% of all results due to the full mesh interconnection of 810 anchors. Built-in measurements (0.5% of count) generate 21.1% of results, highlighting that reusing existing high-density measurements is far more credit-efficient than launching new ones.
5. **DNS manipulation detection via built-in measurements**: Analysis of built-in measurements targeting DNS root servers revealed systematic DNS response injection in China (69% of probes blocked for Meta services) and Iran, demonstrating the platform's utility for detecting censorship and DNS manipulation at scale.

### Authors' Conclusion

RIPE Atlas is a powerful and underutilized resource for network measurement research. Its 1.3 billion daily results make it one of the densest sources of active Internet measurement data available. However, the geographic bias toward Europe and North America is a structural limitation that researchers must explicitly account for when interpreting results. The authors provide concrete guidelines for efficient platform use: examine existing measurements before launching new ones, prefer recurring measurements, use descriptive tags, include measurement IDs in publications for reproducibility. The five case studies demonstrate that significant research insights can be extracted from existing data without consuming additional measurement credits.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- Probe vs. anchor distinction: probes are lightweight and residentially hosted; anchors are high-capacity and institutionally hosted — different representativeness profiles for DNS measurements
- Dual-stack coverage: anchors (92%) are more reliable for IPv6 DNS measurements than standard probes (46.5%)
- Anchor mesh: the full mesh of ~810 anchors provides a dense, globally distributed baseline that can be leveraged without spending user credits
- Built-in measurements (DNSMON): continuous monitoring of root servers and ccTLDs provides a longitudinal DNS baseline that can serve as a reference for our measurements

**Applicable methods**:
- Probe selection strategy: balance geographic diversity (counteract Europe/NA bias) with AS-level diversity to avoid correlated measurements
- Credit optimization: check DNSMON and existing UDMs for overlapping domain coverage before launching new measurements
- Recurring measurements rather than multiple one-shot runs to reduce per-result credit cost and enable temporal analysis
- Systematic tagging (e.g., `thesis-dns-geo`, `tranco-YYYY-MM-DD`) for retrievability and reproducibility

**Important statistics**:
- 12,900 active probes, 810 anchors as of February 2024
- 178 countries covered
- Germany + USA = 28% of vantage points (geographic bias benchmark)
- 88,000 DNS measurements active in a single day
- 69% of Chinese probes blocked for Meta DNS queries
- 46.5% of probes dual-stack; 92% of anchors dual-stack
- ~26,000 results per measurement on average; 1.3 billion results per day

**Identified limitations (gaps to fill)**:
- Single-day snapshot: no longitudinal analysis of platform evolution or measurement stability over time — our thesis explicitly addresses the temporal dimension
- No inter-platform comparison (M-Lab, CAIDA Ark) that would contextualize RIPE Atlas's biases relative to alternatives
- Geographic bias remains unresolved at the structural level; results from underrepresented regions (Africa, South Asia) must be interpreted with caution

### Personal Critique

**Strengths**:
- First systematic operational analysis of the platform, filling a clear gap in the literature
- Massive dataset (1.3 billion results, 50,000+ measurements) provides reliable characterization statistics
- DNS manipulation case study (China/Iran) is directly relevant to thesis themes and demonstrates geographic variation in DNS responses
- Practical guidelines are actionable and based on empirical efficiency data, not theoretical recommendations
- Authors include RIPE NCC staff (Kisteleki), lending direct institutional knowledge to the analysis

**Weaknesses**:
- Temporal scope limited to 24 hours prevents analysis of trends, seasonality, or probe churn over time
- Credit cost model not discussed: researchers designing studies need this information to estimate feasibility but must look elsewhere
- DNS case study (censorship detection) is methodologically shallow — the paper demonstrates the capability without providing a replicable methodology for DNS-specific analysis
- Geographic bias is identified but no mitigation strategy is proposed beyond encouragement to deploy more probes

**Links to other papers**:
- Van Rijswijk-Deij et al. (OpenINTEL): OpenINTEL measures from a single centralized vantage point (exhaustive TLD coverage) while RIPE Atlas measures from 12,900 distributed points (geographic diversity) — the two approaches are complementary, and our thesis combines both dimensions
- Le Pochat et al. (Tranco): Tranco provides the stable domain list that RIPE Atlas probes will query; the combination of Tranco stability and RIPE Atlas geographic diversity is the core methodological contribution of the thesis

**Open questions**:
- How many RIPE Atlas credits are required to measure the Tranco top 10,000 domains from 500 probes at weekly intervals?
- Can the geographic bias be statistically corrected through stratified weighting, and if so, what is the minimum number of probes per region for reliable inference?
- Do resolver pool concentration findings (Xu et al. 2023) mean that geographically diverse RIPE Atlas probes may still converge on the same iRDNS infrastructure, reducing the effective vantage point diversity?

### Key Quotes

> "Germany and the United States host substantially more vantage points than any other country, both accounting for 28% of probes and anchors."

> "DNS measurements allow for analysis of how DNS responses vary depending on the geographic area where the probes are located."

> "The great majority of ongoing measurements were user-defined, with most being pings (87.9K) and DNS measurements (88K)."

> "Built-in measurements revealed response injection targeting popular domains in China and Iran, with 69% of probes from China experiencing blocking of Meta services."

> "Researchers should examine existing measurements before launching new ones and prefer recurring measurements over multiple one-offs."

> "34 countries having only one probe or anchor, highlighting a strong bias towards Europe and North America."

---

## Use in Thesis

**Relevant sections**:
- Section 2.4 (RIPE Atlas state of the art): Infrastructure description, capabilities, DNS use cases, geographic coverage statistics
- Section 4 (Methodology): Probe selection criteria (geography, AS, dual-stack), credit optimization strategy, reproducibility practices (tags, measurement IDs)
- Section 7 (Discussion): Geographic bias as a limitation of our results, comparison with OpenINTEL's complementary approach

**Points to develop**:
- Probe vs. anchor tradeoffs for our specific DNS measurement use case (latency, reliability, IPv6 support)
- Strategy to compensate for the Europe/NA bias: oversample underrepresented regions in probe selection, apply stratified analysis in results
- Justification for recurring measurements over the study period (temporal dimension of the thesis)

**Cross-references**:
- Fiche Xu 2023 (DNS infrastructure centrality): resolver pool concentration may limit the effective geographic diversity achievable even with 500+ RIPE Atlas probes
- Fiche van Rijswijk-Deij 2018 (OpenINTEL): contrasting centralized exhaustive measurement with distributed selective measurement

---

**Tags**: #ripe-atlas #dns #distributed-measurement #infrastructure #geographic-bias #best-practices #dns-manipulation #methodology
**Status**: [X] Read / [X] Filed
