# Reading Note - DNS Measurements with RIPE Atlas (Tutorial)

**Bibliographic Reference**:
Bortzmeyer, S. (2017). *DNS measurements with RIPE Atlas* [Presentation slides, AFNIC]. Retrieved from RIPE NCC documentation. Presented at RIPE Meeting, October 2017.

**Theme**:
This tutorial presentation by Stéphane Bortzmeyer (AFNIC) introduces the practical mechanics of conducting DNS measurements using RIPE Atlas. It covers the web interface, the REST API, the Magellan command-line tool, and JSON result formats, while also cataloguing common traps — such as probes using non-standard resolvers, lying resolvers, or transparent DNS proxies — that can distort DNS measurement results.

**Relevance to thesis**:
This tutorial is a foundational practical reference for any thesis using RIPE Atlas to conduct distributed DNS measurements. It explains how to query DNS from geographically distributed vantage points, how to interpret the results programmatically, and crucially, what data quality pitfalls to anticipate. The enumerated "traps" (alternative root servers, DNS interception, transparent proxies) are directly relevant to quality filtering in a large-scale DNS measurement campaign.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 3.X (Measurement methodology and tooling)
- Section 2.4 (RIPE Atlas capabilities for DNS measurement)
- Section 4.X (Data quality and result interpretation)

---

## Article Content

### Research Objective(s)

**Problem**: RIPE Atlas supports DNS measurements but the platform's DNS-specific measurement options, result formats, and practical pitfalls are not widely documented in accessible form. Researchers need concrete guidance on how to design, launch, and interpret DNS measurements from distributed vantage points.

**Research questions**:
1. What DNS measurement types and configuration options does RIPE Atlas support?
2. How can measurements be launched and results retrieved programmatically via the API and command-line tools?
3. What are the common traps that can invalidate or bias DNS measurement results from RIPE Atlas probes?

### Background

The Domain Name System (DNS) is a critical part of Internet infrastructure, as necessary as IP routing yet frequently overlooked in resilience and quality-of-service studies. RIPE Atlas probes can perform DNS measurements as one of their core measurement types, querying arbitrary DNS names using UDP or TCP, for both IPv4 and IPv6 transports. Results are returned in a structured JSON format containing full DNS response information including answer counts, record data, and query timing. The platform's measurement API allows fine-grained control over probe selection, query parameters, and scheduling.

### Methodology

- **Study type**: Tutorial / practitioner presentation
- **Tools used**: RIPE Atlas web interface, RIPE Atlas REST API v2, Magellan (`ripe-atlas` CLI tool), `atlas-resolve` custom tool
- **Scale**: Demonstrations use samples of 10 probes; production campaigns can target thousands of probes
- **Measurement protocol**: DNS measurements configured via JSON API definitions specifying protocol (UDP/TCP), address family (IPv4/IPv6), query name, query type (A, AAAA, etc.), query class (IN), and whether to use the probe's local resolver (`use_probe_resolver`) or a specified target resolver
- **Data collected**: JSON result objects containing DNS response sections (ANCOUNT, ARCOUNT), raw answer buffer (`abuf`), query timing, source IP, probe ID, and measurement ID

### Main Results

1. **Measurement configuration flexibility**: RIPE Atlas DNS measurements support a wide range of options, including choice of transport protocol (UDP/TCP), address family (af: 4 or 6), query type, query class, recursive/iterative resolution, and use of the probe's default local resolver or a specified target.
2. **Probe tag filtering for DNS**: When selecting probes via the API, system tags such as `system-resolves-a-correctly` and `system-resolves-aaaa-correctly` can be included to restrict the probe set to those with known functional DNS resolution.
3. **Magellan CLI tool**: The `ripe-atlas measure dns` command provides dig-like output from multiple probes simultaneously, making rapid exploratory DNS measurement straightforward from the command line. Example: measuring `lqdn.net` from probe #29198 with full DNS response details including query time (386 ms) and server IP.
4. **Custom tooling (`atlas-resolve`)**: The `atlas-resolve` tool allows querying specific record types (e.g., AAAA) from a fixed country set (e.g., `--country FR`) and returns grouped results (e.g., 9 occurrences of a single IPv6 answer from 10 French probes).
5. **Common traps identified**:
   - Some probes use non-standard resolvers, including alternative DNS roots or "lying resolvers" that return fabricated answers (e.g., for censorship or parental control)
   - Some networks intercept and rewrite DNS traffic transparently, meaning the probe's query reaches a different resolver than the one the probe believes it is using
   - Some networks deploy transparent DNS proxies that modify or forward queries in unexpected ways
6. **Use cases enumerated**: Measuring censorship by country (selecting probes by geographic location), checking different anycast instances of a DNS server, and verifying that a domain resolves correctly worldwide ("many zones have all eggs in the same basket").

### Authors' Conclusion

RIPE Atlas provides a powerful and accessible platform for conducting distributed DNS measurements across a globally distributed set of vantage points. The combination of a web interface, a REST API, and command-line tools (Magellan, custom scripts) enables both exploratory and systematic DNS measurement campaigns. However, researchers must be aware of data quality issues stemming from non-standard resolvers, DNS interception, and transparent proxies — these traps can cause results to misrepresent the actual DNS behaviour of the network path under study.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- `use_probe_resolver: True` setting causes DNS queries to go through the probe's local ISP resolver — this is the mode most relevant to studying end-user DNS resolution behaviour
- System tag filtering (`system-resolves-a-correctly`) as a pre-selection step to exclude probes with known DNS resolution failures
- The JSON `abuf` field contains the raw base64-encoded DNS response buffer, enabling full post-hoc parsing of all DNS sections

**Applicable methods**:
- Using the RIPE Atlas REST API with structured JSON measurement definitions for programmatic DNS measurement campaigns
- Tag-based probe filtering at measurement launch time to control vantage point quality
- Combining passive probe-level metadata (from the probe archive) with active DNS measurement results for per-probe quality assessment

**Important statistics**:
- Measurements can be configured with `requested: 10` probes up to thousands; one-off (`is_oneoff: True`) or recurring measurements are both supported
- Query timing is reported per-probe (e.g., 386 ms observed in the example), enabling latency-based analysis
- Results include the source IP of the probe, enabling geolocation-based aggregation

**Identified limitations (gaps to fill)**:
- The tutorial does not quantify the prevalence of the identified traps (lying resolvers, interception) across the RIPE Atlas probe population — this is a significant gap for result interpretation
- No guidance is given on how to detect or filter out affected probes post-measurement; this requires cross-referencing with other datasets or validation queries

### Personal Critique

**Strengths**:
- Highly practical: provides real API call examples, actual CLI output, and concrete JSON result structures
- Concisely identifies the most important data quality pitfalls in DNS measurements from RIPE Atlas
- Useful enumeration of real-world use cases that align directly with thesis measurement scenarios

**Weaknesses**:
- This is a presentation (slide deck converted to text), not a peer-reviewed paper; it lacks empirical depth and quantitative analysis
- The trap enumeration is qualitative — no estimates of how many probes are affected by each trap type
- The tutorial is from 2017; some API details and tool versions may have changed

**Links to other papers**:
- Bajpai et al. (2017, RIPE Atlas tags): Provides the technical underpinning for the probe tag filtering recommended in this tutorial
- Holterbach et al. (2015, RIPE Atlas interference): Quantifies one form of measurement quality degradation on RIPE Atlas probes
- Randall et al. (IMC 2021, DNS interception): Directly studies the home gateway DNS interception trap mentioned in this tutorial

**Open questions**:
- What fraction of RIPE Atlas probes are affected by transparent DNS proxying or lying resolver behaviour, and does this fraction vary by country or ASN?
- How can the raw `abuf` DNS response buffer be parsed efficiently at scale to detect anomalous resolver behaviour?

### Key Quotes

> "Some probes use strange resolvers (alternative roots, lying resolvers...)."

> "Some networks intercept and rewrite DNS traffic, some have transparent proxies."

> "Test that your domain name resolves from everywhere. (Many zones have all eggs in the same basket.)"

---

## Use in Thesis

**Relevant sections**:
- Section 3.X (Measurement methodology): Cite as practical reference for RIPE Atlas DNS measurement API usage and result format
- Section 3.X (Data quality): Reference the enumerated traps when describing result filtering and quality control procedures
- Section 2.4 (RIPE Atlas capabilities): Cite for the DNS measurement type description and supported configuration options

**Points to develop**:
- Describe how the thesis measurement campaigns use the RIPE Atlas API, following the JSON measurement definition pattern described here
- Explain quality control steps taken to detect and exclude probes affected by lying resolvers or transparent DNS proxies

**Cross-references**:
- `bajpai2017_ripeatlas_tags.md`: Tag-based probe selection methodology
- `holterbach2015_ripeatlas_interference.md`: Measurement quality on RIPE Atlas probes
- `nosyk2024_ripeatlas_ditl.md`: Large-scale practical DNS measurement campaign on RIPE Atlas

---

**Tags**: #ripe-atlas #dns #measurement-methodology #tutorial #api #data-quality #transparent-proxy #lying-resolver
**Status**: [X] Read / [X] Filed
