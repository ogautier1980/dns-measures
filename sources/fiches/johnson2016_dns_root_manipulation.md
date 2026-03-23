# Reading Note - Detecting DNS Root Manipulation

**Bibliographic Reference**:
Jones, B., Feamster, N., Paxson, V., Weaver, N., & Allman, M. (2016). Detecting DNS root manipulation. In *Passive and Active Measurement (PAM 2016)*, Lecture Notes in Computer Science. Springer. [Princeton University / International Computer Science Institute / University of California, Berkeley]

**Theme**:
This paper develops and validates techniques to detect unauthorised manipulation of DNS root server traffic — including transparent in-path proxies, DNS response injection, and BGP route hijacking — using a combination of large-scale RIPE Atlas measurements and BGP routing table analysis. The authors focus on the B root server (the only non-anycasted root) as a ground-truth reference and identify a small but significant number of ISPs that intercept or redirect root DNS queries.

**Relevance to thesis**:
Our thesis uses RIPE Atlas to make active DNS measurements across geographic locations and relies on the integrity of DNS resolution for valid results. This paper demonstrates that DNS responses observed at probe locations may not originate from the expected authoritative servers, which is a direct threat to measurement validity. The detection methodology — comparing ping RTT to DNS query RTT — is relevant to our own work on DNS latency measurement and serves as a reference for the security dimension of our state-of-the-art chapter.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.9 (DNS security: DNSSEC, manipulation, censorship)
- Section 2.4 (RIPE Atlas measurement capabilities and limitations)
- Section 3.x (Methodology: measurement validity and data quality)

---

## Article Content

### Research Objective(s)

**Problem**: Entities operating unauthorised DNS root servers can completely control name resolution for any client within their network, enabling censorship, redirection, and man-in-the-middle attacks. The prevalence of such manipulation in the wild is poorly understood, and systematic methods to detect it at Internet scale are lacking.

**Research questions**:
1. Can we detect in-path DNS proxies and unauthorised root mirrors using latency anomalies observable from RIPE Atlas probes?
2. How prevalent is DNS root manipulation across the global Internet, and what forms does it take?

### Background

The DNS root comprises 13 server addresses (a through m root-servers.net) run by 12 organisations. All but one (B root, operated by the University of Southern California from Los Angeles, USA) use IP anycast to distribute their service globally. Resolvers hardwire the IP addresses of these 13 servers. An attacker can manipulate root DNS resolution through three mechanisms: (1) deploying an in-path transparent proxy that intercepts DNS root queries, (2) injecting fake DNS responses before legitimate replies arrive, or (3) hijacking BGP routes to redirect traffic for root server IP prefixes to unauthorised replicas. Countries such as China, Pakistan, and Turkey have historically manipulated DNS to impose censorship, sometimes inadvertently affecting resolution for other countries. The paper focuses on network-level manipulation, not host-level malware.

### Methodology

- **Study type**: Active measurement + control-plane analysis (observational/empirical)
- **Tools used**: RIPE Atlas (approximately 8,000 probes in 2,755 ASes across 189 countries), RIPE RIS (Routing Information Service), RouteViews BGP data, MaxMind geolocation
- **Scale**: 6,546 Atlas probes providing ping measurements to B root; 6,135 probes providing HOSTNAME.BIND DNS queries; 5,929 probes providing both; one week of data (July 6–13, 2014)
- **Measurement protocol**: Three complementary detection techniques were employed: (1) Anomalous latency detection — comparing ICMP ping RTT to the singular B root versus DNS query RTT; a DNS response arriving significantly faster than the ping suggests an in-path proxy. (2) Server identity verification — issuing HOSTNAME.BIND DNS queries (special queries that ask a server to identify itself) from Atlas probes; replies not matching the pattern "bx" (b0–b9) indicate proxy or mirror presence. (3) BGP routing analysis — checking RouteViews and RIPE RIS RIBs for anomalous AS paths or more-specific prefixes for B root's IP prefix. Traceroutes from probes to B and L roots were also analysed to detect shared infrastructure.
- **Data collected**: ICMP ping RTTs to B root (continuous, every 4 minutes per probe); one HOSTNAME.BIND response per probe; traceroutes to B and L root (every 30 minutes per probe); BGP routing tables and updates from RouteViews and RIPE RIS

### Main Results

1. **In-path DNS proxies detected**: Eleven HOSTNAME.BIND responses did not match the expected "bx" pattern. Ten of these coincide with ISPs deliberately intercepting DNS root queries — confirmed by the HOSTNAME.BIND response naming the ISP's own server (e.g., "dns3.wnanchi.com" for a Kenyan ISP). This indicates intentional interposition for performance or policy reasons.
2. **Latency anomaly confirms proxy presence**: For the Kenyan ISP example, DNS query RTT to "B root" was 14 ms, while ping RTT to the actual B root in Los Angeles was 318 ms — an implausible difference (factor of ~23x) that confirms a local proxy answers DNS queries rather than the real root.
3. **DNS root mirror discovered**: Analysis of RTT distributions from Asian probes to B root versus L root (150 anycast sites) revealed a clear outlier — a probe with anomalously low B root RTT that matches L root RTT, indicating the probe's queries are answered by a local root mirror rather than the authentic B root in Los Angeles.
4. **BGP hijacking not observed**: No evidence of BGP route hijacking affecting the B root prefix was found in the RouteViews or RIPE RIS data during the measurement period, though the method's coverage is limited to publicly visible BGP advertisements.
5. **Geolocation inconsistency as a confounder**: 1.7% of Atlas probes (106 probes) showed inconsistent geolocation information between Atlas's own data and MaxMind, complicating the latency-based detection for those probes.

### Authors' Conclusion

The authors conclude that DNS root manipulation is present but not widespread; they find ten ISPs using in-path DNS proxies (possibly for performance improvement or censorship) and one DNS root mirror. They emphasise that their two independent detection techniques (latency anomaly and HOSTNAME.BIND identity) agree on all findings, increasing confidence in the results. They acknowledge that their methods may underestimate DNS proxies (since proxies can correctly forward HOSTNAME.BIND responses) and note that future work should extend coverage to all DNS root letters and all ASes.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- DNS root manipulation as a threat to measurement validity — RIPE Atlas probes may be behind proxies that intercept and answer DNS queries before they reach authoritative servers
- Latency-comparison technique (ping vs DNS query) as a tool to detect proxy presence — applicable in our thesis when validating measurement integrity
- HOSTNAME.BIND queries as a lightweight server identity check for DNS measurement validation

**Applicable methods**:
- Cross-check DNS response times against ICMP ping times in our dataset to flag probes potentially behind transparent DNS proxies
- Use HOSTNAME.BIND or similar identity probes to validate that DNS responses originate from expected authoritative infrastructure
- Complement RIPE Atlas measurements with BGP data from RIPE RIS to contextualise routing anomalies

**Important statistics**:
- 10 ISPs found to operate in-path DNS proxies across approximately 6,000 probes surveyed (~0.2% of probes affected)
- 1 DNS root mirror identified in Asia
- Latency gap between proxy-answered DNS query (14 ms) and legitimate ping to B root (318 ms) — a factor of approximately 23x
- 5,929 Atlas probes provided both ping and HOSTNAME.BIND data, covering 2,755 ASes in 189 countries

**Identified limitations (gaps to fill)**:
- Coverage limited to probes already in the RIPE Atlas network; ASes without Atlas probes are unobservable
- The study focuses exclusively on B root; manipulation affecting other (anycasted) root letters is harder to detect
- Results are from 2014; the landscape of DNS manipulation may have changed significantly, especially in countries with documented censorship regimes

### Personal Critique

**Strengths**:
- Two independent detection techniques that cross-validate each other, increasing result reliability
- Broad geographic coverage (189 countries, 2,755 ASes) using RIPE Atlas
- Methodology is transparent and reproducible; the specific queries and thresholds are clearly described

**Weaknesses**:
- The paper studies only the B root; the method cannot be directly applied to anycasted root letters without modification
- DNS proxy detection via HOSTNAME.BIND is evadable — a sophisticated proxy could forward or spoof HOSTNAME.BIND responses
- Measurement period is one week in July 2014; longitudinal analysis is absent
- BGP analysis is limited to publicly visible routes; internal hijacking within an ISP would be invisible

**Links to other papers**:
- Holterbach et al. (2015): The synchrony and precision issues on RIPE Atlas could affect the latency-comparison technique used here — probe delays could be mistaken for proxying
- Koch et al. (2021): Anycast routing to root servers is the normal case; this paper identifies deviations from expected anycast routing as a manipulation signal
- Hours et al. (2016): DNS proxies at the ISP level, as detected here, would affect CDN resolver-location mapping in ways similar to public resolver use

**Open questions**:
- How has the prevalence of in-path DNS proxies evolved since 2014, particularly with the spread of DNS-over-HTTPS (DoH) and DNS-over-TLS (DoT)?
- Can the latency-comparison technique be adapted to detect manipulation of TLD or second-level domain name servers, not just the root?
- Do any of the Atlas probes in our thesis dataset show evidence of being behind DNS proxies?

### Key Quotes

> "Entities operating unauthorized root servers can completely control the entire Internet name space for any systems within their sphere, including blocking access to sites by disrupting their name resolution, or arbitrarily interposing on communication by redirecting through man-in-the-middle proxies."

> "We find one ISP that redirects clients at the IP layer to an unauthorized root replica. Further, we find several ISPs prevent direct access to the authorized root servers by interposing on DNS lookup with proxies."

> "The fact that two independent techniques detected the same ten DNS proxies increases our confidence in the result."

---

## Use in Thesis

**Relevant sections**:
- Section 2.9 (DNS security): Cite as a key empirical study of DNS root manipulation prevalence; describes both the threat model and detection methodology
- Section 2.4 (RIPE Atlas as a measurement platform): Reference as evidence that Atlas probes can be behind DNS proxies, which is a measurement validity concern
- Section 3.x (Methodology — data quality): Reference the latency-comparison technique as a validation step we can apply to our own dataset

**Points to develop**:
- Assess whether the probes selected for our thesis measurements show any signs of proxy presence, using the latency-comparison heuristic
- Discuss the broader implication: even "active" DNS measurements may not reach the intended authoritative server if the probe is behind a transparent proxy

**Cross-references**:
- holterbach2015_ripeatlas_interference.md (RIPE Atlas measurement validity — complementary concern)
- koch2021_anycast_context.md (anycast root DNS routing — what "normal" looks like, enabling detection of deviations)

---

**Tags**: #dns-security #dns-root #manipulation #ripe-atlas #anycast #bgp-hijacking #transparent-proxy #censorship #measurement-validity
**Status**: [X] Read / [X] Filed
