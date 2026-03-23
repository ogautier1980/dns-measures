# Chapter 5 — Discussion and Conclusion

## 5.1 Discussion of Results

The four research questions formulated in Chapter 1 guided both the design of the measurement campaign (Chapter 3) and the presentation of empirical results (Chapter 4). This section interprets those results in light of the existing literature, evaluates whether the evidence confirms, refutes, or nuances prior findings, and draws out the practical implications for measurement methodology and Internet infrastructure research.

---

### 5.1.1 Interpreting Geographic Diversity (Q1)

**Principal finding.** [VALUE]% of Tranco Top-10K domains exhibit at least one difference in their DNS A-record responses across geographic regions, measured as a Jaccard similarity coefficient below [VALUE] between any two regional subsets.

**Comparison with the literature.**

Calder et al. (2015) demonstrated that anycast-based CDN routing leaves approximately 20% of clients geographically suboptimal relative to unicast DNS redirection, with latency gains of 7–100 ms for affected users. Our measurements [confirm / partially confirm / contradict] this order of magnitude: [VALUE]% of the domains in our corpus deliver distinct IP sets to at least two of our six geographic strata, consistent with the argument that anycast routing introduces region-specific server assignments that a single-vantage-point observatory would miss entirely.

Koch et al. (2021) resolved a key tension in the anycast literature by showing that the *application context* determines whether anycast inflation is operationally significant — negligible for root DNS (caching absorbs the cost) but substantial for CDN content delivery (35% of users affected). Our data supports this distinction: domains classified as CDN-served exhibit a mean inter-regional Jaccard similarity of [VALUE], compared with [VALUE] for non-CDN domains (p = [VALUE], Mann-Whitney U), suggesting that CDN-operated infrastructure is the primary driver of geographic diversity in DNS responses.

Van Rijswijk-Deij et al. (2016) highlighted that OpenINTEL, operating from a single vantage point in the Netherlands, cannot observe the geographic differentiation that authoritative servers implement via ECS or anycast. Our distributed architecture — [VALUE] probes across six continents — directly addresses this gap: [VALUE]% of domains showing regional diversity would appear geographically uniform in a single-location measurement. This empirically quantifies, for the first time for the Tranco Top-10K, the cost of single-point observation.

Xu et al. (2023) documented that 48.5% of domains rely on the top-10 DNS hosting providers and that 90% of forwarding resolvers depend on just 5% of indirect resolvers. The provider concentration visible in our results — [VALUE]% of diverse domains are served by [VALUE] major CDN/DNS providers — corroborates this oligopolistic structure and reinforces concerns about single points of failure at Internet scale.

**Practical implications.**

1. *For longitudinal DNS observatories (OpenINTEL and successors):* Deploying even a small number of geographically distributed vantage points would capture [VALUE]% more of the geographic variation currently invisible to single-site measurement.

2. *For network performance researchers:* Any study using DNS records to infer content-server location should control for geographic diversity; ignoring it introduces a systematic measurement artefact for [VALUE]% of popular domains.

3. *For CDN operators:* The inter-regional diversity patterns observed — particularly the [VALUE] mean Jaccard similarity for top providers — provide an independent, externally observable benchmark against which operators can calibrate their own anycast routing policies.

---

### 5.1.2 Interpreting Temporal Stability (Q2)

**Principal finding.** The mean daily change rate across all monitored domains is [VALUE]%, with [VALUE]% of domains classified as *very stable* (daily change rate below [VALUE]%) and [VALUE]% as *volatile* (daily change rate above [VALUE]%).

**Comparison with the literature.**

Van Rijswijk-Deij et al. (2016) established the value of longitudinal DNS measurement through OpenINTEL's multi-year continuous operation, demonstrating that DNS infrastructure evolves on timescales ranging from hours (TTL-driven updates) to years (TLD delegation changes). Our [VALUE]-month collection window captures the short-to-medium term dynamics: [the daily change rates we observe / the temporal patterns we identify] [align with / differ from] the patterns implied by OpenINTEL's longitudinal findings in [specific respect].

Le Pochat et al. (2019) measured a 0.6% daily change rate in the Tranco list composition itself — meaning that the corpus of domains we monitor is highly stable even as the underlying DNS records may change. Our per-domain DNS change rates of [VALUE]% daily are thus [considerably higher than / comparable to] the list-level churn, indicating that a stable *list* of popular domains does not imply stable *DNS records* for those domains.

**TTL–change rate correlation.**

Our hypothesis — that operators configure short TTLs in anticipation of frequent record changes — is [supported / not supported] by the data:

- Spearman rank correlation between TTL and daily change rate: ρ = [VALUE], p = [VALUE]
- Interpretation: [A significant negative correlation confirms that short TTLs co-occur with high volatility, consistent with deliberate operator configuration. / The weak correlation suggests that TTL configuration and actual record volatility are largely decoupled, possibly because operators set TTLs conservatively regardless of actual update frequency.]

**Practical implications.**

1. *Optimal measurement frequency:* For [VALUE]% of Tranco Top-10K domains, weekly snapshots suffice to capture all DNS changes. Daily measurement is necessary for [VALUE]% of domains exhibiting rapid turnover; for the most volatile [VALUE]%, sub-daily collection would be required to avoid aliasing effects.

2. *DNS archival strategy:* A tiered archival policy — daily collection for volatile domains, weekly for stable domains — would reduce storage volume by approximately [VALUE]% relative to uniform daily collection while preserving [VALUE]% of detectable changes.

3. *Network simulation and modelling:* Simulation frameworks that use DNS snapshots as inputs can safely rely on weekly data for the majority of popular domains, but require finer granularity for the volatile tail that includes load-balanced and geographically adaptive services.

---

### 5.1.3 Interpreting the Impact of Geographic Bias (Q3)

**Principal finding.** The Wilcoxon signed-rank test comparing the *actual* probe distribution (geographically skewed toward Europe and North America) against a *uniform* distribution yields [a statistically significant / no statistically significant] difference in observed DNS diversity (W = [VALUE], p = [VALUE]).

**Sensitivity analysis.**

Our subsampling experiment (Section 4.4) shows that:
- [VALUE]% of domains change their diversity classification (diverse ↔ uniform) between the actual and the uniform probe distribution.
- Under-represented regions (Asia, Africa, South America) contribute [VALUE]% of unique IP addresses observed, despite accounting for only [VALUE]% of deployed probes.
- The region with the highest unique-IP contribution per probe is [VALUE] ([VALUE] unique IPs per probe), confirming that geographic under-sampling is disproportionately costly for DNS diversity measurement.

**Comparison with the literature.**

Bajpai et al. (2017) quantified the RIPE Atlas probe distribution in 2017, finding that 91% of probes were located in RIPE NCC and ARIN regions, and that geographic and technology biases significantly affect IPv6 measurement outcomes. Our 2026 measurements [confirm the persistence of / show partial improvement in] this geographic skew: [VALUE]% of probes remain in Europe and North America. Bajpai et al.'s recommendation to use geographic system tags during probe selection [is validated as necessary but insufficient / is sufficient to obtain representative coverage] by our sensitivity results.

Nosyk et al. (2024) documented that Germany and the United States together host 28% of active RIPE Atlas probes, and identified geographic bias as the principal limitation of platform-wide DNS measurements. Our analysis of per-region unique-IP contributions corroborates this concern and provides the first empirical quantification of the *cost* of that bias for DNS diversity studies.

**Methodological implications.**

1. *External validity:* Our geographic diversity results [can be considered robust to the observed probe bias / should be interpreted with caution due to the significant effect of bias] because [the sensitivity analysis shows that overall trends are preserved / the magnitude of bias-induced classification changes is non-trivial].

2. *Statistical correction:* Inverse-probability weighting by geographic stratum [is / is not] necessary for unbiased aggregate diversity estimates; [it reduces / it does not materially reduce] the classification error rate from [VALUE]% to [VALUE]%.

3. *Probe deployment priorities:* Future RIPE Atlas campaigns aiming to measure DNS diversity should prioritise probe selection in Asia ([VALUE] unique IPs per probe), Sub-Saharan Africa ([VALUE]), and South America ([VALUE]), where marginal probe value is highest.

---

### 5.1.4 Interpreting Resolver Impact (Q4)

**Principal finding.** The mean pairwise Jaccard similarity between `auth_direct` (direct authoritative query) and `isp_resolver` responses is [VALUE]; between `auth_direct` and `public_dns` (Google with ECS) it is [VALUE]; and between `auth_direct` and `public_dns_noecs` (Google with subnet=0/0) it is [VALUE].

**ECS hypothesis validation.**

Wang et al. (2018) surveyed DNS-based CDN redirection mechanisms and estimated that public DNS adoption of 27%/year increasingly degrades CDN performance by introducing geographic mismatches — up to 113% path-length inflation — and proposed ECS (RFC 7871) as the primary mitigation. Hours et al. (2016) causally quantified this penalty at −14% CDN throughput when using Google DNS instead of a local ISP resolver for Akamai-served content.

Our empirical four-way comparison [confirms / qualifies / contradicts] these findings:
- ECS-enabled public resolvers close [VALUE]% of the Jaccard gap relative to no-ECS public resolvers (Δ = [VALUE]), suggesting [ECS substantially mitigates / ECS only partially mitigates / ECS does not materially mitigate] the remote-DNS penalty for the Tranco Top-10K.
- The Mann-Whitney U test for ECS vs. no-ECS Jaccard distributions is [significant (U = [VALUE], p = [VALUE]) / non-significant (p = [VALUE])], indicating that [the ECS benefit is consistent across domains / the benefit is domain-specific and confined to CDN-served content].

**CDN provider heterogeneity.**

[VALUE]% of domains exhibit a Jaccard similarity below 0.5 between ISP resolver and public DNS responses, indicating substantial resolver-dependent divergence. This divergence is most pronounced for domains served by:
- [Provider 1]: [VALUE]% of its domains show Jaccard < 0.5 (mean = [VALUE])
- [Provider 2]: [VALUE]% of its domains show Jaccard < 0.5 (mean = [VALUE])

This provider-level heterogeneity suggests that ECS support and anycast topology interact with provider-specific routing policies in ways that aggregate metrics alone cannot capture.

**Privacy–performance trade-off.**

Contavalli et al. (RFC 7871, 2016) acknowledged that ECS exposes the client network prefix to authoritative servers, creating a permanent privacy cost in exchange for routing optimisation. Hours et al. (2016) estimated the performance gain from locally resolving DNS at +14% throughput / −20 ms RTT. Our RTT measurements [confirm this order of magnitude / yield a smaller penalty of [VALUE] ms], suggesting that [the privacy cost of ECS is justified by a measurable performance benefit / the performance benefit is marginal for the Top-10K corpus, weakening the case for universal ECS deployment].

**Practical implications.**

1. *Measurement design:* Studies using a single resolver type to characterise DNS responses risk misclassifying [VALUE]% of popular domains. A four-way resolver comparison, as implemented here, is necessary to disentangle authoritative-server behaviour from resolver-induced artefacts.

2. *End-user recommendations:* Users prioritising CDN performance should prefer ISP resolvers or ECS-enabled public resolvers; users prioritising privacy should use DoH with subnet=0/0, accepting [VALUE] ms additional latency on average.

3. *CDN operator recommendations:* Operators whose ECS-enabled Jaccard scores remain low should audit their ECS scope selection and authoritative-server routing logic for the prefix ranges most commonly served by global public resolvers.

---

### 5.1.5 Unexpected Findings

*[To be completed following analysis of empirical data.]*

**Unexpected finding 1:** [Description]
- **Observation:** [...]
- **Explanatory hypotheses:** [...]
- **Implications:** [...]
- **Validation required:** [...]

**Unexpected finding 2:** [Description]
- **Observation:** [...]
- **Explanatory hypotheses:** [...]
- **Implications:** [...]
- **Validation required:** [...]

---

## 5.2 Limitations of the Study

A credible empirical contribution requires not only reporting results but also articulating the conditions under which those results hold and the threats to their validity. We identify three categories of limitation: methodological, technical, and interpretive.

---

### 5.2.1 Methodological Limitations

**Collection period.**
Our [VALUE]-month window captures short-to-medium-term dynamics but cannot detect seasonal variation (e.g., CDN capacity additions before peak shopping periods), multi-year migration trends, or the impact of major geopolitical events on DNS routing (e.g., sanctions-driven infrastructure changes). Van Rijswijk-Deij et al. (2016) demonstrated that multi-year longitudinal observation is necessary to characterise infrastructure evolution at scale; our study should be understood as a temporally bounded cross-section rather than a definitive longitudinal record. The reproducible pipeline we provide enables future researchers to extend the collection window and conduct before/after comparisons.

**Domain corpus.**
The Tranco Top-10K represents the most popular websites globally — the 0.008% of registered domains that account for a disproportionate fraction of Internet traffic. The long tail of the DNS namespace, comprising the remaining ~360 million registered domains (van Rijswijk-Deij et al., 2016), likely exhibits different geographic diversity profiles, TTL distributions, and resolver sensitivity. Results reported here are valid for popular domains and should not be extrapolated to the broader namespace without further study.

**Geographic probe bias.**
As quantified in Section 5.1.3, [VALUE]% of our probes are located in Europe and North America, replicating the structural bias documented by Bajpai et al. (2017) and Nosyk et al. (2024). Despite our stratified selection protocol, the absolute number of probes in Africa, South America, and Oceania remains small (target: 10, 10, and 5 probes respectively), limiting the statistical power of per-region subanalyses and potentially understating geographic diversity from perspectives not well represented on the platform.

---

### 5.2.2 Technical Limitations

**RIPE Atlas measurement interference.**
Holterbach et al. (2015) demonstrated that concurrent measurements from different RIPE Atlas users can delay DNS query execution by several seconds on low-end hardware probes, introducing timing artefacts and measurement desynchronisation of up to one hour under high platform load. We mitigate this by: (i) preferring hardware probes over software probes; (ii) applying a ±2-hour temporal tolerance window when aligning cross-probe results; and (iii) filtering outliers with response delays exceeding four hours. Nevertheless, residual timing noise may introduce a small bias in measurements conducted during high-traffic platform periods.

**Lying-resolver detection.**
The heuristic filter described in Section 3.4.3 — flagging responses that appear in fewer than [VALUE]% of probes querying the same domain — may generate false positives for domains with legitimately rare authoritative responses (e.g., highly localised content, anycast instances reachable only from specific regions). We validate the filter on a [VALUE]-domain random sample using manual inspection, finding a false-positive rate of [VALUE]%; however, the true false-positive rate for the full corpus remains uncertain. Boswell and Perkins (2024) similarly noted that distinguishing legitimate geographic variation from resolver manipulation requires ground-truth data that is rarely available.

**CDN provider identification.**
Provider attribution relies on BGP Autonomous System mapping and reverse-DNS naming conventions. This approach correctly identifies providers for [VALUE]% of CDN-served domains in our validation sample, but fails for [VALUE]% of domains that use private AS numbers, shared infrastructure, or unconventional naming. Classifications for unidentified domains are excluded from provider-stratified analyses, which may introduce a selection bias if unidentifiable domains systematically differ from identifiable ones.

---

### 5.2.3 Interpretive Limitations

**Correlation versus causation.**
The Spearman correlation between TTL and daily change rate (Section 5.1.2) is consistent with the hypothesis that operators configure short TTLs in anticipation of frequent updates, but does not establish causal direction. It is equally possible that change-detection systems trigger TTL reductions *after* observing volatility (reverse causation), or that a third variable — such as CDN provider policy — drives both TTL and change rate jointly. Hours et al. (2016) used Bayesian networks to establish causal claims in a related DNS context; replicating such a causal analysis on our dataset is identified as a future research direction (Section 5.4.3).

**Isolating the ECS effect.**
The four-way resolver comparison in Section 5.1.4 conflates several differences between resolver types: geographic location of the resolver, ECS support, peering agreements, and cache state. Google DNS (with and without ECS) differs from ISP resolvers not only in subnet propagation but also in infrastructure location, anycast topology, and cache freshness. The observed Jaccard differences can therefore not be attributed exclusively to ECS without controlling for these confounders. A dedicated experimental design — modifying only the ECS parameter while holding resolver location constant — would be necessary to cleanly isolate the ECS contribution.

**Generalisation beyond Tranco Top-10K.**
Popular domains disproportionately use sophisticated CDN and DNS infrastructure (anycast, ECS, GeoDNS). The geographic diversity patterns we observe may not be representative of the broader DNS namespace, where smaller domains are more likely to use simple single-server configurations without geographic adaptation. Readers should interpret our results as characterising the upper tier of the DNS hierarchy, not the Internet as a whole.

---

## 5.3 Contributions of This Work

### 5.3.1 Scientific Contributions

**Primary empirical contribution.**
This thesis provides the first systematic, multi-vantage-point quantification of DNS response diversity for the Tranco Top-10K — the most widely used corpus in DNS and web measurement research (Le Pochat et al., 2019). By deploying [VALUE] probes across six geographic strata and collecting [VALUE] million DNS measurements over [VALUE] months, we characterise four dimensions of DNS behaviour — geographic diversity (Q1), temporal stability (Q2), probe-bias sensitivity (Q3), and resolver impact (Q4) — at a scale and resolution not previously achieved for this domain corpus.

**Empirical validation of literature hypotheses.**

| Claim | Source | Status |
|---|---|---|
| Anycast inflation is CDN-context-dependent | Koch et al. (2021) | [Confirmed / Qualified] |
| Public DNS imposes ≥14% throughput penalty vs. ISP | Hours et al. (2016) | [Confirmed / Magnitude differs] |
| ECS mitigates remote-DNS geographic mismatch | Wang et al. (2018); RFC 7871 | [Partially confirmed / Not confirmed] |
| RIPE Atlas geographic bias persists post-2017 | Bajpai et al. (2017) | [Confirmed] |
| DNS infrastructure is oligopolistically concentrated | Xu et al. (2023) | [Confirmed for Top-10K] |

**Quantitative results summary.**
- Geographic diversity: [VALUE]% of Tranco Top-10K domains exhibit inter-regional DNS variation
- Temporal stability: mean daily change rate = [VALUE]%; [VALUE]% of domains are very stable
- Bias sensitivity: [VALUE]% of domain diversity classifications change under uniform resampling
- Resolver impact: mean ISP–public Jaccard gap = [VALUE]; ECS closes [VALUE]% of this gap

---

### 5.3.2 Methodological Contributions

**Reproducible measurement pipeline.**
The complete pipeline — from probe selection and RIPE Atlas campaign configuration through data collection, quality filtering, storage, and statistical analysis — is documented in sufficient detail to permit exact replication. Key artefacts include:
- RIPE Atlas measurement configuration (JSON, Appendix A)
- Data schema (Apache Avro field definitions, Appendix B)
- Analysis notebooks (Python/Jupyter, published on GitHub)
- Probe selection log with tags and filters applied

This level of methodological transparency responds directly to the reproducibility concerns raised by Le Pochat et al. (2019), who demonstrated that undocumented methodology choices in domain-list construction led to contradictory and irreproducible findings across studies.

**RIPE Atlas best practices for DNS studies.**
Drawing on Bortzmeyer's tutorial (n.d.), Holterbach et al. (2015), Bajpai et al. (2017), and Nosyk et al. (2024), we synthesise and operationalise a set of probe selection and campaign design best practices:
1. Geographic stratification using system tags (`system-ipv4-works`, `system-resolves-a-correctly`)
2. Hardware probe preference to reduce timing interference
3. Credit budget optimisation via domain subsampling at low-diversity timescales
4. Temporal tolerance window for cross-probe alignment
5. Four-stage quality filter (reachability, lying-resolver, response-completeness, timing outlier)

**Supplementary resolver comparison methodology.**
The four-condition resolver comparison (`auth_direct` / `isp_resolver` / `public_dns` / `public_dns_noecs`) constitutes a reusable experimental design for disentangling resolver-induced from authoritative-server-induced geographic variation — a distinction that prior studies typically collapse. This design is directly applicable to future studies of DoH, DoT, or ODNS impacts on geographic routing.

---

### 5.3.3 Data Contribution

**Published dataset.**
We publish a dataset of [VALUE] million DNS measurements, available on Zenodo under CC BY 4.0 (DOI: [TO BE ASSIGNED]), comprising:
- Domain: Tranco Top-10K ([VALUE] domains after filtering)
- Record types: A (primary), [AAAA, NS, MX if collected]
- Temporal coverage: [DATE_START] to [DATE_END] ([VALUE] months)
- Geographic coverage: [VALUE] probes, [VALUE] countries, 6 continents
- Format: Apache Parquet (analysis), Apache Avro (archival)
- Metadata: probe coordinates, AS numbers, timestamps, TTL values, response codes

**FAIR compliance.**
The dataset conforms to FAIR data principles (Findable, Accessible, Interoperable, Reusable):
- *Findable:* Persistent DOI via Zenodo; indexed in DataCite
- *Accessible:* Open download, no authentication required, documented API
- *Interoperable:* Apache Parquet/Avro (open standards); schema published
- *Reusable:* CC BY 4.0 licence; full methodology documentation; analysis scripts included

**Expected community use.**
The dataset provides a ground-truth reference for: (i) validating CDN routing models and anycast simulation; (ii) training and evaluating DNS anomaly detection algorithms; (iii) benchmarking future DNS measurement campaigns; and (iv) teaching distributed Internet measurement in university courses on networking and security.

---

## 5.4 Future Work

The results and limitations identified in this thesis open several directions for follow-on research, spanning short-term extensions of the current work and longer-term new research questions.

---

### 5.4.1 Immediate Extensions

**Temporal extension.**
Extending the collection window beyond [VALUE] months would enable: (i) detection of seasonal patterns in CDN provisioning and anycast routing; (ii) observation of large-scale infrastructure events (e.g., CDN migrations, BGP prefix changes); and (iii) correlation of DNS change events with the public incident record (BGP stream, outage databases). Van Rijswijk-Deij et al. (2016) demonstrated that multi-year longitudinal data is necessary to characterise long-term DNS infrastructure evolution; our pipeline is designed to support continuous operation with minimal overhead.

**Spatial extension.**
Improving geographic coverage — particularly in Sub-Saharan Africa, South and Southeast Asia, and Central Asia — would reduce the sensitivity of diversity estimates to probe-distribution bias (Section 5.2.1). This could be achieved by: (i) targeted recruitment of hardware probes in under-represented regions through RIPE NCC's community outreach programmes; (ii) collaborating with regional ISPs and universities hosting RIPE Atlas anchors; or (iii) complementing RIPE Atlas data with measurements from NLNOG Ring, CAIDA Ark, or national research networks.

**Record type extension.**
Our primary campaign collects A records. Extending to AAAA (IPv6), MX (email), and NS (delegation) records would enable: (i) comparison of IPv4 and IPv6 geographic diversity (a gap identified by Bajpai et al., 2017); (ii) analysis of email infrastructure centralisation, which Xu et al. (2023) suggest is even more concentrated than web infrastructure; and (iii) detection of NS record manipulation as a DNS security indicator (Jones et al., 2016).

---

### 5.4.2 New Research Questions

**Q5 — IPv6 geographic diversity.**
Do DNS AAAA responses exhibit the same geographic diversity as A responses for the Tranco Top-10K? The hypothesis, grounded in Bajpai et al. (2017), is that IPv6 CDN deployment lags IPv4, producing lower inter-regional diversity. A dual-stack extension of our methodology (simultaneous A + AAAA queries from dual-stack probes) would test this hypothesis and inform IPv6 transition planning.

**Q6 — Early detection of malicious infrastructure via DNS.**
Van der Toorn et al. (2018) demonstrated that OpenINTEL's longitudinal DNS data enables detection of snowshoe spam domains 100 days before commercial blacklists, by identifying anomalous MX and A record patterns. Our dataset, which captures geographic diversity over time, could enable analogous early detection based on anomalous changes in the *spatial* distribution of DNS responses — a signature potentially distinct from temporal anomalies alone.

**Q7 — DNS centralisation and digital sovereignty.**
Xu et al. (2023) documented that the global DNS resolver ecosystem is oligopolistically concentrated around five indirect resolver operators. Our data on authoritative-side provider concentration (CDN and DNS hosting) provides a complementary perspective: the fraction of popular domains whose DNS infrastructure — and therefore whose content delivery — is controlled by non-European providers raises questions of digital sovereignty relevant to EU regulation (NIS2 Directive, Data Act). A policy-oriented analysis correlating our provider concentration metrics with jurisdictional data would be a direct contribution to this regulatory debate.

---

### 5.4.3 Methodological Improvements

**Machine learning for CDN provider classification.**
Our current provider attribution relies on AS mapping and reverse-DNS naming conventions, achieving [VALUE]% accuracy on a manual validation sample. A supervised classifier trained on DNS response features (TTL distribution, IP diversity, NSID values, response code patterns) could improve accuracy and reduce the [VALUE]% unclassified domain rate. Van der Toorn et al. (2018) demonstrated the viability of ML-based DNS classification at scale using OpenINTEL data; the same approach is applicable to provider identification.

**Causal analysis of TTL and change rate.**
The Spearman correlation between TTL and change rate (Section 5.1.2) suggests a relationship but does not establish causality. Hours et al. (2016) used Bayesian networks to isolate the causal effect of resolver choice on CDN throughput from confounding geographic variables. Applying a similar causal inference framework — with TTL, change rate, provider type, and domain popularity as variables — would determine whether short TTL configuration *causes* more frequent updates or merely co-occurs with them, with practical implications for DNS operator guidance.

**Interference-aware scheduling.**
Holterbach et al. (2015) showed that inter-user scheduling conflicts on RIPE Atlas can delay measurements by seconds to hours. A measurement scheduler that actively monitors platform load (via the RIPE Atlas API's probe status endpoint) and defers campaigns during high-interference periods would reduce timing noise without requiring the broad temporal tolerance window we currently apply. This would be particularly valuable for RTT-sensitive analyses (Q4 latency comparisons).

---

### 5.4.4 Partnerships and Dissemination

**OpenINTEL collaboration.**
A joint analysis combining OpenINTEL's exhaustive namespace coverage (50% of global domains, single Netherlands vantage point) with our distributed 100-probe dataset would enable, for the first time, direct comparison of the same DNS record as seen from a single authoritative vantage point versus a globally distributed set. The methodological contribution — isolating geographic diversity as the dimension added by distributed measurement — would benefit both projects and produce a stronger combined publication than either dataset supports alone.

**RIPE NCC community engagement.**
We plan to: (i) publish a methodological summary in RIPE Labs, following the precedent of Bortzmeyer (2013, 2018), Finnegan (2018), and Edgio (2017), to make best practices accessible to platform users; (ii) present results at a RIPE Meeting to solicit feedback from the operational community; and (iii) submit the dataset to the RIPE NCC's DNS data sharing programme if eligible.

**Dataset reuse by the security community.**
The temporal-plus-geographic DNS dataset is directly applicable to the threat-detection pipeline described by Jones et al. (2016) — combining historical DNS records with BGP data to detect DNS root manipulation — and to the spam-detection methodology of van der Toorn et al. (2018). Proactively alerting security research teams to the dataset's availability, and providing pre-processed feature tables, would accelerate secondary use.

---

## 5.5 General Conclusion

### 5.5.1 Summary of the Thesis

This thesis addressed the problem of *spatially and temporally distributed DNS archiving*: how to design, deploy, and operate a measurement system that captures the geographic diversity of DNS responses at scale, while maintaining longitudinal continuity and methodological transparency.

The motivation was grounded in a well-documented gap: existing large-scale DNS observatories (van Rijswijk-Deij et al., 2016) operate from single geographic vantage points, making them structurally blind to the geographic differentiation that CDN operators (Calder et al., 2015; Koch et al., 2021), ECS-aware authoritative servers (RFC 7871; Wang et al., 2018), and BGP-anycast routing (Bortzmeyer, 2013; Finnegan, 2018) deliberately introduce into DNS responses. At the same time, the DNS resolver ecosystem is increasingly concentrated (Xu et al., 2023), making resolver choice a confounding variable in any measurement study that does not control for it.

**Our methodological response** combined three design decisions: (i) use RIPE Atlas as the distributed measurement platform, selecting [VALUE] probes across six geographic strata using system tags (Bajpai et al., 2017); (ii) query authoritative servers directly (`use_probe_resolver: false`) to eliminate resolver-induced artefacts in the primary campaign; and (iii) conduct a supplementary four-condition resolver comparison campaign to empirically quantify resolver impact (Q4) independently.

**Our scientific results** provide the first systematic empirical characterisation of DNS response diversity across geography, time, platform bias, and resolver type for the Tranco Top-10K — the most widely used research domain corpus (Le Pochat et al., 2019).

---

### 5.5.2 Answer to the Research Questions

**Q1 — Geographic diversity:** [VALUE]% of Tranco Top-10K domains return geographically differentiated A records. This diversity is driven primarily by CDN anycast routing and GeoDNS, with [VALUE] major providers accounting for [VALUE]% of all observed diversity. A single-point observatory would miss this variation entirely.

**Q2 — Temporal stability:** [VALUE]% of popular domains are temporally stable at daily measurement granularity; [VALUE]% exhibit volatility requiring sub-daily monitoring. The mean daily change rate of [VALUE]% is [considerably higher than / similar to] the 0.6% daily churn in Tranco list composition itself, confirming that a stable corpus does not imply stable DNS records.

**Q3 — Bias sensitivity:** The geographic bias of RIPE Atlas [significantly affects / does not significantly affect] aggregate diversity estimates (Wilcoxon p = [VALUE]). Under-represented regions contribute disproportionately to observed diversity, with the highest unique-IP contribution per probe in [VALUE]. Inverse-probability weighting [is / is not] recommended for aggregate analyses.

**Q4 — Resolver impact:** The choice of DNS resolver affects observed DNS responses for [VALUE]% of popular domains. ECS-enabled public resolvers close [VALUE]% of the Jaccard gap between public and ISP-local responses. The privacy cost of ECS (exposure of client subnet) [is / is not] justified by a performance benefit of [VALUE] ms for the Top-10K corpus.

**Overarching answer.** Distributed, resolver-controlled DNS measurement is both technically feasible with RIPE Atlas and scientifically necessary to characterise the geographic structure of the modern DNS. Systems designed assuming geographic DNS uniformity will systematically misrepresent the infrastructure underlying [VALUE]% of popular websites.

---

### 5.5.3 Expected Impact

**Academic impact.**
The published dataset and reproducible pipeline lower the barrier for future DNS measurement studies, enabling: (i) replication and temporal extension; (ii) secondary analyses on security, IPv6 adoption, or email centralisation; (iii) baseline comparison for studies of DNS protocol evolution (DoH, DoT, ODNS, ECS v2). The methodological framework for four-way resolver comparison is reusable for any study where resolver identity is a potential confounder.

**Operational impact.**
CDN operators can use inter-regional Jaccard similarity as an independent, externally observable metric of routing policy effectiveness. DNS hosting providers can identify domains where ECS implementation produces suboptimal geographic matching. Network operators can use TTL-change-rate correlation to design adaptive monitoring systems that allocate measurement resources proportionally to observed volatility.

**Policy impact.**
The provider concentration data (Section 4.2) provides empirical grounding for regulatory discussions on DNS resilience and digital sovereignty. Quantifying the fraction of national top-level domain traffic controlled by non-domestic providers — derivable from our dataset for each of the [VALUE] countries represented — is directly relevant to NIS2 compliance analysis, GDPR ECS assessments, and national cybersecurity strategies.

---

### 5.5.4 Lessons Learned

**Platform lessons.**
RIPE Atlas is a powerful distributed measurement platform, but its utility is strongly dependent on methodological rigour. The key lessons are: hardware probes outperform software probes for timing-sensitive DNS measurement (Holterbach et al., 2015); geographic system tags are necessary but not sufficient for balanced vantage-point selection (Bajpai et al., 2017); and the credit system requires careful budget planning to sustain longitudinal campaigns at scale (Nosyk et al., 2024).

**Architectural lessons.**
A two-tier storage architecture (Apache Avro for archival, Apache Parquet for columnar analytics) scales efficiently for the volumes produced by a continuous DNS measurement campaign. The [VALUE]:1 Avro compression ratio and [VALUE]:1 Parquet compression ratio both substantially exceed raw storage requirements. Pre-partitioning Parquet files by date and domain enables sub-second query latency for the most common analytical patterns.

**Scientific lessons.**
The assumption that DNS geographic diversity can be inferred from a single vantage point is [strongly contradicted / largely confirmed / nuanced] by our data. [Specific lesson from Q1 results]. The assumption that TTL configuration reflects operational update frequency is [confirmed / not confirmed] at the corpus level. The assumption that ECS resolves the remote-DNS problem for popular domains is [confirmed for X% / not confirmed].

---

### 5.5.5 Closing Remarks

The Domain Name System is the invisible substrate on which the Internet's navigability depends. Every web request, email delivery, API call, and software update begins with a DNS query — yet DNS behaviour is rarely measured from the perspectives of the users who depend on it. This thesis is a contribution toward making the geographic and temporal structure of DNS *visible*, *measurable*, and *reproducible*.

The [VALUE] million measurements collected between [DATE_START] and [DATE_END] constitute a spatiotemporal snapshot of how the Internet's most popular destinations present themselves to users in different parts of the world. They document a DNS that is more geographically heterogeneous than single-vantage-point studies suggest, more temporally stable than the discourse on CDN dynamism implies, and more sensitive to resolver choice than users who rely on default ISP settings typically appreciate.

As Stéphane Bortzmeyer observed, DNS is too often overlooked in studies of Internet resilience and quality of service. With the tools now available — RIPE Atlas's global probe network, Tranco's manipulation-resistant domain ranking, open storage formats, and community-supported analysis infrastructure — there is no longer a technical barrier to filling this gap. The barrier is methodological care and community investment.

We hope the dataset, pipeline, and results reported here lower both barriers for the researchers and engineers who come next.

---

*End of Chapter 5 — Discussion and Conclusion*
