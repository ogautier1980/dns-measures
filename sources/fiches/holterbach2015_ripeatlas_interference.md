# Reading Note - Quantifying Interference between Measurements on the RIPE Atlas Platform

**Bibliographic Reference**:
Holterbach, T., Pelsser, C., Bush, R., & Vanbever, L. (2015). Quantifying interference between measurements on the RIPE Atlas platform. In *Proceedings of the 2015 Internet Measurement Conference (IMC '15)* (pp. 437–443). ACM. https://doi.org/10.1145/2815675.2815710

**Theme**:
This paper investigates the extent to which concurrent measurements on the RIPE Atlas platform interfere with one another, degrading both the precision of delay measurements and the synchrony of distributed experiments. The authors develop a rigorous methodology using colocated Ring nodes to isolate probe-induced effects from network noise, then quantify interference under controlled load conditions across different probe hardware generations.

**Relevance to thesis**:
Our thesis relies on RIPE Atlas as its primary platform for distributed DNS measurements across geographic locations. Understanding the inherent noise floor introduced by concurrent platform usage is a prerequisite for correctly interpreting DNS timing and synchrony results. The findings reported here — up to 7 ms additional latency at the 95th percentile and desynchronization up to one hour — must be factored into our experimental design and analysis of temporal DNS behaviour.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 3.x (RIPE Atlas methodology and measurement validity)
- Section 4.x (Interpretation of DNS timing results)
- Section 2.4 (State of the art on RIPE Atlas measurement practices)

---

## Article Content

### Research Objective(s)

**Problem**: Public measurement platforms such as RIPE Atlas schedule multiple users' experiments concurrently on the same low-end hardware probes. This raises the question of whether, and by how much, overlapping measurements corrupt each other's results — both in terms of precision (reported delays) and synchrony (the temporal alignment of distributed campaigns).

**Research questions**:
1. Do concurrent measurements launched by different users on the same RIPE Atlas probe significantly alter the delay measurements reported by that probe?
2. Do concurrent measurements desynchronize distributed experiments, and does upgrading probe hardware mitigate this effect?

### Background

RIPE Atlas is composed of low-end embedded devices (probes) deployed in private homes and organisations worldwide. As of April 2015, the platform hosted over 6,700 probes in 197 countries and had executed nearly 30 million individual measurements. Three probe hardware generations exist: v1 and v2 are based on 167 MHz Lantronix XPort Pro CPUs, while v3 uses a 400 MHz TP-Link MR3020 with more RAM and flash. The platform uses a credit system to regulate usage and schedules all users' measurements concurrently without providing feedback about co-resident load. The RIPE Atlas measurement toolkit supports ping, traceroute, DNS, and SSL queries; one-off measurements are near-real-time and more expensive in credits than scheduled ones. The platform was executing 592,000 concurrent individual measurements at the time of data collection (Table 1 of the paper).

### Methodology

- **Study type**: Controlled active measurement / experimental
- **Tools used**: RIPE Atlas REST API, NL Ring nodes (colocated reference nodes in the same LAN as probes), Scamper (for remote pings), custom tooling published openly
- **Scale**: Multiple probes tested per hardware generation (v1, v2, v3); load ranging from 10 to 500 concurrent one-off traceroutes; incoming ping rates from 16 to 1,840 ping/s
- **Measurement protocol**: Delay was measured between an Atlas probe and its colocated Ring node (same LAN, no Internet path) to isolate probe-induced effects from external network variation. Load was induced by launching increasing numbers of one-off traceroutes from the probe (outbound load) or by directing increasing ICMP echo request floods towards the probe (inbound load). Synchrony was measured by tracking the completion time of one-off traceroute campaigns.
- **Data collected**: RTT distributions (median, 95th percentile, standard deviation) before and during load; completion times of distributed one-off experiments under varying concurrent load levels

### Main Results

1. **Precision degradation (outbound load)**: On v1/v2 probes, launching 100 concurrent one-off traceroutes increases the median ping delay by more than 1 ms (v1: +1.10 ms, v2: +1.20 ms) and the 95th percentile by more than 7 ms (v1: +7.30 ms, v2: +7.70 ms). Standard deviation increases by 16.3 ms for v1 and 7.4 ms for v2.
2. **Precision degradation (inbound load)**: Pings directed towards a v2 probe at 400 ping/s increase the median outbound delay by 0.22 ms and the 95th percentile by 2.90 ms; at 1,000 ping/s the probe becomes overloaded, with delays approaching 1,000 ms and 10% packet loss above 1,280 ping/s.
3. **Hardware improvement limits**: v3 probes show dramatically lower sensitivity to load — median delay increases of only 0.06 ms and no standard deviation impact — but upgrading hardware does not solve the synchrony problem.
4. **Desynchronization**: Under heavy concurrent load, one-off traceroute campaigns can complete up to one hour later than intended. Even 10 concurrent traceroutes produce the same magnitude of desynchronization as 100, though for a shorter duration.
5. **Retrospective validity concern**: Because interference is not documented by the platform and probe load is not reported to users, prior research results and the RIPE Atlas historical dataset may have been unknowingly affected by interfering measurements.

### Authors' Conclusion

The authors conclude that measurement interference on RIPE Atlas is a real and significant phenomenon that should be systematically accounted for when designing and analysing experiments on the platform. They identify two mitigation techniques: (1) using v3 probes for precision-sensitive measurements, and (2) scheduling experiments during low-load periods or using the API to check concurrent load. They also call for the platform to provide users with load feedback, and release all measurement and analysis tools for reproducibility.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- Probe load as a confounding variable in distributed measurement campaigns
- Distinction between precision degradation (hardware-dependent) and synchrony degradation (hardware-independent)
- Colocated reference node methodology to isolate probe behaviour from network effects

**Applicable methods**:
- Filtering or flagging measurements made during periods of anomalously high concurrent platform load
- Selecting v3 probes preferentially for delay-sensitive DNS response-time comparisons
- Measuring distribution tails (95th percentile, standard deviation) rather than only medians

**Important statistics**:
- On v2 probes: +1.20 ms median, +7.70 ms at 95th percentile, +7.40 ms standard deviation when sourcing 100 traceroutes
- Desynchronization of up to 1 hour under heavy load, even when campaigns were launched simultaneously
- 592,000 concurrent individual measurements were running at the time of data collection in 2015

**Identified limitations (gaps to fill)**:
- The paper focuses on ping and traceroute interference; DNS measurement interference is noted as less sensitive but not quantified separately — our thesis could explore this directly
- The paper predates significant growth of the Atlas platform (now over 10,000 probes); the interference dynamics may have changed

### Personal Critique

**Strengths**:
- Rigorous colocated measurement design that isolates probe effects from Internet noise
- Systematic quantification across all three hardware generations
- Results published with full tool availability, enabling reproduction

**Weaknesses**:
- Results are from a small number of probes per version (at least two); broader sampling across geographic regions and ISPs could reveal heterogeneity
- The study focuses on v1/v2/v3 hardware; newer probe generations are not covered

**Links to other papers**:
- Koch et al. (2021): Uses RIPE Atlas for anycast inflation measurements; the synchrony limitations noted here are relevant to how Koch interprets geographic routing results
- Johnson et al. (2016): Uses RIPE Atlas for DNS root manipulation detection; probe desynchronisation could affect their latency-based anomaly detection

**Open questions**:
- How do interference effects scale as the Atlas platform grows to 10,000+ probes and more concurrent users?
- Is DNS measurement precision specifically impacted by concurrent traceroute load, as the paper hints but does not quantify?

### Key Quotes

> "We found that overlapping measurements do interfere with each other in at least two ways. First, we show that measurements performed from and towards the platform can significantly increase timings reported by the probe."

> "Measurements are very quickly desynchronized when other measurements are run in parallel. Under heavy load, completion time may be delayed by close to 1 hour."

> "Overall, our results show that measurement interferences should be systematically taken into account when analyzing results from public platforms."

---

## Use in Thesis

**Relevant sections**:
- Section 2.4 (State of the art on RIPE Atlas): Cite as a key limitation of the platform, noting the interference characterisation and the hardware-generation dependency
- Section 3.x (Methodology): Reference when justifying probe selection criteria (preference for v3 probes) and when describing how we control for concurrent load
- Section 4.x (Results): Reference when discussing variance in DNS response time measurements that may reflect probe-induced noise rather than true network conditions

**Points to develop**:
- Discuss whether DNS measurements are less sensitive to interference than ping (as the paper states), and whether this means our DNS timing results are robust to the platform's concurrent load
- Mention the synchrony risk when comparing DNS measurements taken from geographically distributed probes at nominally the same time

**Cross-references**:
- johnson2016_dns_root_manipulation.md (both use RIPE Atlas; synchrony is relevant to their latency-based detection)
- koch2021_anycast_context.md (Atlas used to supplement CDN measurements; interference considerations apply)

---

**Tags**: #ripe-atlas #measurement-methodology #interference #precision #synchrony #probe-hardware #distributed-measurements
**Status**: [X] Read / [X] Filed
