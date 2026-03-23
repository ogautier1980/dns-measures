# Reading Note - Vantage Point Selection for IPv6 Measurements: Benefits and Limitations of RIPE Atlas Tags

**Bibliographic Reference**:
Bajpai, V., Eravuchira, S. J., Schönwälder, J., Kisteleki, R., & Aben, E. (2017). Vantage point selection for IPv6 measurements: Benefits and limitations of RIPE Atlas tags. *Proceedings of the Applied Networking Research Workshop (ANRW '17)*, 1–7. https://doi.org/10.1145/3106328.3106334

**Theme**:
This paper evaluates the RIPE Atlas tagging mechanism — introduced in July 2014 — as a tool for fine-grained vantage point selection in Internet measurement studies. It distinguishes between automatically generated system tags and manually assigned user tags, assessing their stability and accuracy. A case study applies system tags to identify and profile dual-stacked (IPv4 + IPv6) probes across geographic regions and autonomous systems.

**Relevance to thesis**:
This paper is directly relevant to any distributed DNS measurement study using RIPE Atlas, as it characterises the tagging mechanisms available for selecting probes with specific connectivity and DNS-resolution capabilities. Understanding which system tags (e.g., `system-resolves-a-correctly`, `system-ipv6-works`) are reliable is essential for designing valid DNS measurement campaigns. The analysis of geographic and network-level probe bias also informs how to contextualise spatial variation in DNS resolution results.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.4 (RIPE Atlas infrastructure and capabilities)
- Section 3.X (Probe selection methodology)
- Section 4.X (Bias analysis and geographic representativeness)

---

## Article Content

### Research Objective(s)

**Problem**: Before 2014, RIPE Atlas probe selection was limited to geographic (latitude/longitude) or network-origin (ASN/prefix) filters. The tagging system introduced in July 2014 offers finer-grained selection, but the reliability and practical value of these tags — particularly user-assigned ones — was unknown.

**Research questions**:
1. Are RIPE Atlas system tags reliable and stable enough to support rigorous vantage point selection?
2. How geographically and topologically diverse are the dual-stacked probes identified using system tags, and which regions are underrepresented?
3. How stale are user-assigned tags, and can they be trusted for measurement design?

### Background

RIPE Atlas is the largest open Internet measurement platform, with approximately 9,100 connected hardware probes as of January 2017 out of 20,785 registered. Probes perform built-in measurements including ping, traceroute, DNS queries (for all root servers), SSL certificate checks, and HTTP tests. The tagging mechanism, introduced in July 2014, enables filtering probes on connectivity characteristics. System tags are derived automatically from built-in measurements and refreshed every 4 hours, while user tags require volunteers to maintain them proactively. Competing platforms (SamKnows, BISmark, Archipelago/Ark, DIMES, iPlane) have between 170 and 70,000 vantage points but are less open or geographically diverse.

### Methodology

- **Study type**: Empirical measurement / longitudinal analysis
- **Tools used**: RIPE Atlas probe archive API, RIPE Atlas measurement API, APNIC IPv6 user population dataset
- **Scale**: 9,100 connected probes; 2,301 dual-stacked probes; 88 countries; 822 ASNs
- **Measurement protocol**: System tags assessed via the probe metadata archive (covering March 2014 to January 2017); dual-stacked probes defined as those tagged with both `system-ipv4-works` and `system-ipv6-works` and sharing the same ASN on both protocol versions (to exclude tunnel-based IPv6); user tag update frequency estimated from historical probe metadata
- **Data collected**: System tag time series; ASN and country distribution of dual-stacked probes; latency measurements (IPv4 vs IPv6) from dual-stacked probes to RIPE Atlas anchors; user tag update histories

### Main Results

1. **System tag reliability**: System tags are updated every 4 hours from live built-in measurement results, making them stable and accurate. Key DNS-relevant tags include `system-resolves-a-correctly` (8,305 probes), `system-resolves-aaaa-correctly` (8,236 probes), and `system-ipv6-works` (3,050 probes) as of January 2017.
2. **User tag staleness**: Only approximately 2.8% of probe hosts ever update their user tags, so user tags tend to become stale and cannot be reliably used for precise vantage point selection.
3. **Dual-stacked probe share**: Approximately 25.99% (2,301 out of 8,855) of connected non-anchored probes are dual-stacked, spanning 88 countries and 822 ASNs.
4. **Regional concentration**: Approximately 91% of dual-stacked probes are concentrated in the RIPE (Europe/Middle East) and ARIN (North America) regions; Africa, Latin America, and most of Asia are severely underrepresented.
5. **Home network deployments**: Approximately 83% of dual-stacked probes are in access networks; 782 probes are in home networks, evenly split across DSL, cable, and fibre connections.
6. **Geographic gaps identified**: Correlation against APNIC IPv6 user population estimates shows that Belgium (BE) and Japan (JP) are significantly underrepresented relative to their actual IPv6 user populations, pointing to structural sampling bias.

### Authors' Conclusion

System tags have substantially improved vantage point selection by providing stable, automatically updated, and accurate labels for probe DNS resolution and IP connectivity characteristics. User tags are largely unreliable due to infrequent maintenance. The dual-stacked probe dataset is the richest available for IPv6 measurement studies but remains concentrated in Europe and North America. The authors call for greater probe deployment in underrepresented regions and recommend using system tags — specifically the `-works` variants — for measurement design rather than the less-reliable `-capable` variants.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- System tags as a reliable, auto-updated mechanism for selecting probes with specific DNS/connectivity characteristics
- The distinction between `system-ipvX-capable` and `system-ipvX-works`: always prefer `-works` for DNS measurement studies, since capability does not guarantee functional connectivity
- Geographic and ASN-level bias inherent in RIPE Atlas probe distribution must be acknowledged and mitigated in DNS measurement design

**Applicable methods**:
- Using `system-resolves-a-correctly` and `system-resolves-aaaa-correctly` tags to filter probes for DNS measurement campaigns targeting authoritative or recursive resolvers
- Correlation of measurement results against external population or usage statistics (e.g., APNIC data) to contextualise geographic underrepresentation
- Stratified probe selection by ASN and country to mitigate regional bias

**Important statistics**:
- 9,100 connected probes as of January 2017 (out of 20,785 registered); note that this has grown to ~12,000+ by 2024
- 25.99% of connected probes are dual-stacked — relevant for IPv6 DNS resolution measurement studies
- Only 2.8% of probe hosts ever update their user tags
- System tags are refreshed every 4 hours
- 88 countries and 822 ASNs covered by dual-stacked probes, but ~91% are in Europe and North America

**Identified limitations (gaps to fill)**:
- RIPE Atlas is heavily concentrated in Europe and North America; DNS measurement campaigns targeting global diversity need explicit mitigation strategies
- The paper focuses on IPv6 connectivity; direct analysis of DNS resolver behaviour quality (e.g., NXDOMAIN handling, TTL compliance, EDNS support) beyond tag classification is not addressed

### Personal Critique

**Strengths**:
- Rigorous longitudinal analysis of tag reliability using the full probe archive since March 2014
- Clear and actionable guidance: prefer system tags over user tags; use `-works` over `-capable`
- Cross-validation against APNIC IPv6 adoption data gives the geographic bias analysis empirical grounding

**Weaknesses**:
- The paper focuses on IPv6 connectivity; DNS-specific measurement quality (resolver fidelity, caching behaviour, EDNS compliance) is not analysed beyond tag classification
- Probe counts from 2017 are outdated; the RIPE Atlas infrastructure has grown substantially since
- User tag staleness is identified but no remediation mechanism is proposed

**Links to other papers**:
- Bortzmeyer (DNS measurements with RIPE Atlas tutorial): Provides practical DNS measurement design guidance on the same platform
- Nosyk et al. (RIPE Atlas DITL): Uses RIPE Atlas at scale for DNS measurements — tag-based probe filtering described here is directly applicable
- Holterbach et al. (RIPE Atlas interference): Addresses a complementary concern: when concurrent measurements on the same probe degrade result quality

**Open questions**:
- How has the geographic distribution of probes evolved since 2017, particularly in underrepresented regions?
- For DNS-specific measurements, what additional per-probe quality indicators (beyond the system tags described) could be derived from historical measurement results to filter out noisy vantage points?

### Key Quotes

> "Only ~2.8% of probe hosts ever update their user tags which may lead to user tags that tend to become stale over time."

> "System tags on the other hand being automatically assigned and frequently updated (every 4 hours) are stable and accurate."

> "By applying a correlation against APNIC IPv6 user population estimate, we further reveal underrepresented countries (such as BE and JP) which would benefit from deployment of more probes for IPv6 measurement studies."

---

## Use in Thesis

**Relevant sections**:
- Section 2.4 (RIPE Atlas infrastructure): Cite for probe count statistics, tag system description, built-in measurement types, and comparison with competing platforms
- Section 3.X (Methodology): Use to justify probe selection strategy based on system tags; explicitly warn against user tag reliance
- Section 4.X (Results/bias analysis): Reference when discussing geographic and topological bias in DNS measurement results

**Points to develop**:
- Explain why DNS measurement campaigns in the thesis use system tags (`system-resolves-a-correctly`, `system-ipv6-works`) and not user tags
- Discuss how the European concentration of probes may affect spatial representativeness of DNS resolution latency or NXDOMAIN behaviour results

**Cross-references**:
- `bortzmeyer_dns_measurements_atlas_tutorial.md`: Practical complement for DNS measurement API usage
- `nosyk2024_ripeatlas_ditl.md`: Large-scale DNS measurement campaign benefiting from tag-based probe selection
- `holterbach2015_ripeatlas_interference.md`: Probe-level measurement quality concerns complementing this paper

---

**Tags**: #ripe-atlas #vantage-points #ipv6 #probe-selection #system-tags #measurement-bias #dns #methodology
**Status**: [X] Read / [X] Filed
