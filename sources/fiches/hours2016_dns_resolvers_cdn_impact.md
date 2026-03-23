# Reading Note - A Study of the Impact of DNS Resolvers on CDN Performance Using a Causal Approach

**Bibliographic Reference**:
Hours, H., Biersack, E., Loiseau, P., Finamore, A., & Mellia, M. (2016). A study of the impact of DNS resolvers on CDN performance using a causal approach. *Computer Networks*, 109, 200–210. https://doi.org/10.1016/j.comnet.2016.06.023

**Theme**:
This paper investigates how the choice of DNS resolver — specifically an ISP's local DNS server versus Google's public DNS service — causally affects the download throughput experienced by clients accessing content from the Akamai CDN. The authors construct a Bayesian causal network from passive traffic traces to model structural dependencies between network parameters and to predict the effects of hypothetical interventions on the DNS resolver selection.

**Relevance to thesis**:
Our thesis studies how the DNS resolver choice affects content delivery and geographic routing decisions, a topic directly addressed by this paper. The causal modelling approach — distinguishing correlation from causation in DNS-CDN interactions — provides a methodological benchmark for interpreting our own measurement results. The empirical finding that local ISP resolvers consistently outperform public resolvers for CDN redirection accuracy is a core piece of evidence for our state-of-the-art chapter on DNS and CDN performance.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.5 (EDNS Client Subnet and DNS-based CDN routing)
- Section 2.4 (DNS resolver types and their impact)
- Section 3.x (Methodology: rationale for probe selection near local resolvers)

---

## Article Content

### Research Objective(s)

**Problem**: CDNs rely on the DNS resolver's IP address to geolocate clients and direct them to an optimal server. When clients use a public DNS service (e.g., Google DNS) instead of their ISP's local DNS, the CDN receives the public resolver's IP — which may be far from the client — leading to suboptimal server selection and degraded download performance. The precise causal structure of this degradation, and its magnitude, are not formally characterised.

**Research questions**:
1. Does the use of a public DNS service (Google DNS) cause measurable throughput degradation compared to the local ISP DNS service when accessing Akamai-hosted content?
2. What is the causal mechanism linking DNS resolver choice to download throughput, and which intermediate parameters (e.g., server distance, TCP configuration) mediate this effect?

### Background

CDNs replicate popular content on geographically distributed servers and use DNS-based redirection to direct each client to the closest or most suitable replica. The authoritative CDN DNS server uses the IP address of the client's DNS resolver as a proxy for the client's location. When the resolver is a public service such as Google DNS (8.8.8.8), its IP address may be in a different city, country, or continent from the client, causing the CDN to assign a suboptimal replica. The EDNS Client Subnet (ECS) extension was designed to address this by forwarding a prefix of the client's IP in DNS queries, but Akamai — the CDN studied here — did not support ECS at the time of this study. Several prior studies had observed correlation between resolver type and performance, but none had formally established causality or quantified the mechanistic pathway.

### Methodology

- **Study type**: Passive measurement + causal inference (observational)
- **Tools used**: PC algorithm for causal graph inference, Gaussian copulae for density estimation, Bayesian networks (directed acyclic graphs), do-calculus for intervention prediction
- **Scale**: IP packet traces collected at a Point of Presence (PoP) of a large European ISP; only large TCP transfers to Akamai servers included (to exclude TCP slow-start effects); traces subdivided by DNS resolver type (local ISP DNS vs. Google DNS)
- **Measurement protocol**: Passive capture of TCP flows at an ISP PoP; extraction of 20 network parameters per flow (RTTs, hop counts, TCP window sizes, congestion indicators, throughput, DNS resolver type, server IP, etc.); PC algorithm applied to infer causal graph; do-calculus used to compute counterfactual throughput distributions under hypothetical resolver changes
- **Data collected**: Per-flow TCP statistics including ISP-side and Internet-side RTT averages and standard deviations, hop counts, TCP receive/congestion window sizes, retransmission scores, RTO occurrences, payload size, and measured throughput (Table 1 of the paper)

### Main Results

1. **DNS resolver type causally affects server assignment**: The causal graph confirms that using local ISP DNS (LDNS) leads to the CDN assigning geographically closer servers to clients than using Google DNS (GDNS), resulting in lower ISP-side RTT and fewer hops.
2. **Throughput difference is causally attributable to resolver proximity**: Clients using LDNS experience higher download throughput than clients using GDNS; the causal model quantifies this improvement and attributes it primarily to the reduced ISP-side RTT (isprttavg) caused by being routed to a closer CDN server.
3. **TCP initial congestion window as additional mediator**: The causal model reveals that the TCP parameterisation of servers assigned to GDNS users — specifically the initial congestion window — plays a key role in their lower throughput, independently of the server distance effect. This was an unexpected finding not identifiable through correlation analysis alone.
4. **Counterfactual prediction**: The causal model predicts that if the servers accessed by LDNS users were re-parameterised with the same initial congestion window as those used by GDNS users, the throughput of LDNS users would drop, confirming the congestion window effect is real.
5. **Public DNS structural problem**: The mean ISP-side RTT for GDNS users is systematically higher than for LDNS users, confirming that public resolvers direct clients to more distant CDN replicas — a structural consequence of the CDN's resolver-IP-based geolocation heuristic.

### Authors' Conclusion

The authors conclude that using a public DNS service such as Google DNS causes a measurable and causally verifiable reduction in download throughput when accessing Akamai-hosted content, primarily because the CDN assigns the client to a more distant server. They also discover an independent TCP-level effect related to server congestion window parameterisation. They argue that their causal modelling framework — based on Bayesian networks and do-calculus — is more powerful than correlation-based methods because it can predict the outcomes of interventions and distinguish genuine causal effects from confounded associations.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- DNS resolver IP as a CDN geolocation proxy and its consequences for content delivery quality
- Distinction between local ISP resolvers (accurate geolocation) and public resolvers (potentially inaccurate geolocation) — directly relevant to our probe configuration in RIPE Atlas
- Causal modelling as a method to disentangle confounded effects in network measurement studies

**Applicable methods**:
- When analysing DNS response patterns in our thesis, distinguish between probes using local versus public resolvers, as this affects both CDN redirection and DNS measurement semantics
- Consider using causal or structural analysis rather than purely correlational analysis when interpreting DNS timing and CDN redirection results

**Important statistics**:
- Mean ISP-side RTT (isprttavg): 76 ms overall; Coefficient of Variation 6.1 — indicating high variability driven by resolver-induced routing differences
- Mean Internet-side RTT (inetrttavg): 26 ms — much lower, reflecting that the Internet path beyond the ISP is not the primary source of variability
- Mean throughput (tput): 3.2 Mbps, range 0.006–35 Mbps — wide range attributable in part to DNS-induced server assignment

**Identified limitations (gaps to fill)**:
- The study is limited to one European ISP and one CDN (Akamai); results may not generalise to other ISPs, geographic regions, or CDNs that do support ECS
- The study is passive and observational; no active DNS experiments are used, unlike our RIPE Atlas approach

### Personal Critique

**Strengths**:
- Rigorous causal inference methodology that goes beyond simple correlation
- Formal counterfactual analysis allows quantitative prediction of intervention effects
- Reveals an unexpected TCP-level mechanism that correlation analysis would have missed

**Weaknesses**:
- Data is from a single ISP PoP; geographic and ISP diversity are absent
- The study predates widespread ECS deployment; Akamai subsequently added ECS support, which may alter the resolver-performance relationship
- The causal inference methodology (PC algorithm, Gaussian copulae) is complex and not widely used in network measurement, limiting reproducibility

**Links to other papers**:
- Koch et al. (2021): Also examines CDN routing efficiency; Hours et al. provide the DNS layer mechanism that Koch's anycast analysis abstracts away
- Johnson et al. (2016): DNS manipulation changes the effective resolver; the CDN redirection consequences quantified here would apply in manipulation scenarios
- RFC 7871 (EDNS Client Subnet): The ECS extension is specifically designed to address the problem Hours et al. quantify; reading both together gives a complete picture

**Open questions**:
- Does the throughput gap between local and public DNS persist after widespread ECS adoption? (Akamai now supports ECS)
- How does the effect size change for CDNs that use client-side measurements rather than resolver-IP-based geolocation?
- Would the same causal model, applied to DNS measurement data from RIPE Atlas probes, reveal similar resolver-location dependencies?

### Key Quotes

> "Clients using the DNS service of their ISP (referred to as local DNS) experience higher throughput than the clients using the public DNS service (referred to as Google DNS), we can show that this performance difference is due to the fact that clients using the DNS service of their ISP are redirected to closer servers."

> "The causal model of our system also reveals that the parameterization of TCP (initial congestion window) of the servers accessed by the users of the Google DNS plays a key role in their throughput performance."

> "Being able to predict the effect of interventions, we can use causal models to understand the observed performance of a given system and to design strategies to improve its performance."

---

## Use in Thesis

**Relevant sections**:
- Section 2.5 (EDNS Client Subnet): Cite as empirical evidence of the performance cost of public DNS resolvers in CDN contexts; motivates the ECS mechanism
- Section 2.4 (DNS resolver landscape): Use to characterise the practical impact of resolver choice on content delivery — a concrete example of why resolver type matters for our measurements
- Section 3.x (Methodology): Reference when justifying our approach to recording the resolver type used by each RIPE Atlas probe in DNS measurements

**Points to develop**:
- Discuss how the ECS situation has evolved since 2016 and whether the throughput gap quantified here has narrowed
- Use the causal modelling concept as a framing device to argue that our thesis moves beyond correlation in interpreting DNS measurement results

**Cross-references**:
- rfc7871_edns_client_subnet.md (the technical solution to the problem studied here)
- koch2021_anycast_context.md (CDN routing efficiency from a different angle — anycast rather than DNS-based)
- wang2018_dns_cdn_challenges.md (broader DNS-CDN interaction challenges)

---

**Tags**: #dns-resolvers #cdn #akamai #causal-inference #bayesian-networks #throughput #ecs #public-dns #isp-dns
**Status**: [X] Read / [X] Filed
