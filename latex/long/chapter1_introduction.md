# Chapter 1 - Introduction

> **Note on sourcing.** The introduction draws on the 22 primary sources listed in the thesis bibliography to motivate the research and position the contribution. Deep technical analysis of these sources is reserved for Chapter 2 (State of the Art). Where specific empirical findings or citations are used in this chapter, they are attributed explicitly; general DNS background knowledge is presented without citation, as it derives from the DNS protocol specifications (RFC 1034, RFC 1035) rather than from the listed sources.

---

## 1.1 Context and Motivation

### 1.1.1 The DNS: Critical Infrastructure of the Internet

The Domain Name System (DNS), specified in 1983 by Paul Mockapetris in RFC 1034 and RFC 1035, is the distributed directory service that underlies virtually every networked application on the Internet. Its function — translating human-readable domain names such as `www.example.com` into machine-routable information such as IPv4 and IPv6 addresses, mail server designations, and cryptographic key references — is so fundamental that van Rijswijk-Deij et al. (2016) characterise it as a service on which "almost all networked services depend". The scale of this dependency is correspondingly enormous: the *.com* Top-Level Domain alone contained approximately 123 million registered names during the 2015–2016 period studied by van Rijswijk-Deij et al. (2016), and OpenINTEL's measurement infrastructure must process at least 1.85 billion DNS queries per day for *.com* alone to achieve full daily coverage.

The criticality of the DNS is most visible when it fails. The Facebook BGP misconfiguration of October 4, 2021 — which withdrew the BGP routes to Facebook's authoritative name servers, making the domain unresolvable from any resolver worldwide — illustrates what Xu et al. (2023) document empirically: when over 98% of all global domains depend on a single DNS provider, a provider-level failure propagates immediately and universally. The Akamai DNS outage of June 2021 and the Fastly CDN outage of the same month produced comparable effects, crippling access to large portions of the web for millions of users. In each case, the DNS was the critical failure point: not the application servers, not the network, but the name resolution layer that clients depend on before any application connection can be established.

Despite this criticality, the DNS has historically received less systematic measurement attention than other Internet infrastructure layers. Bortzmeyer (n.d., tutorial) observes that the DNS is "often forgotten in studies of Internet resilience and quality of service" — functioning so transparently in normal operation that its role is fully recognised only in failure. This relative neglect is reflected in the state of measurement infrastructure: as of this thesis's writing, the most comprehensive longitudinal DNS measurement system — OpenINTEL, developed at the University of Twente (van Rijswijk-Deij et al., 2016) — measures over 50% of the global DNS namespace daily, but does so from **a single vantage point in the Netherlands**. The geographic dimension of DNS responses is not captured.

### 1.1.2 The Ephemeral Nature of DNS Data

A fundamental characteristic of the DNS that motivates archival measurement is the **ephemeral nature of DNS data**. DNS resource records — the atomic units of information in the DNS — carry a Time To Live (TTL) field that governs how long resolvers and caches may retain them. When a TTL expires, the record is discarded; subsequent queries retrieve a fresh response from the authoritative server, which may contain different information. Zone administrators can modify records at any time: a domain that resolved to a server cluster in Europe this morning may resolve to a server cluster in Asia this afternoon, and the DNS infrastructure itself retains no trace of the previous configuration.

This ephemerality creates a structural gap in Internet research. As the official thesis subject statement (Dejaeghere and Rochet, 2025) articulates: "in certain research domains, it is interesting to be able to obtain the DNS information provided at a given period." The use cases are varied but share a common dependency on historical DNS data:

**Network simulation**: Researchers developing Internet simulators — for evaluating routing protocols, security mechanisms, or traffic engineering policies — need realistic DNS data for their simulated networks. Simulating the Internet as it existed two years ago requires knowing what addresses the DNS returned for major domains at that time, from diverse geographic vantage points. Without archival DNS data, these simulations rely on present-day snapshots that do not reflect the historical state of the network (Dejaeghere and Rochet, 2025).

**Security forensics**: Malicious infrastructure — command-and-control servers for botnets, phishing domains, spam networks — frequently changes its DNS configuration to evade detection and blacklisting. Van der Toorn et al. (2018) demonstrate that snowshoe spam domains are detectable from their DNS patterns as much as 100 days before appearing on blacklists, but only if historical DNS data is available for analysis. Without longitudinal archival, post-incident investigation cannot reconstruct the full temporal evolution of malicious DNS configurations.

**Infrastructure evolution studies**: Long-term trends in DNS configuration — the adoption of cloud email services (van Rijswijk-Deij et al., 2016), the migration of domains between DNS providers, the deployment of DNSSEC — are only observable through continuous longitudinal measurement. Point-in-time studies capture a static snapshot; only sustained active measurement captures the dynamics.

### 1.1.3 The Geographic Dimension: A Neglected Aspect

Beyond the temporal dimension, DNS responses exhibit a **geographic dimension** that single-vantage-point measurement cannot capture. The authoritative name server for a domain does not necessarily return the same response to all clients: it may return different IP addresses, or redirect through different CNAME chains, depending on the inferred geographic location of the querying resolver. Three distinct mechanisms produce this geographic variation:

**CDN-based geographic routing**: Large web services — streaming platforms, search engines, social networks — deploy Content Delivery Networks with server clusters distributed across multiple continents. DNS is the primary mechanism for directing clients to the appropriate cluster: when the CDN's authoritative server receives a DNS query, it infers the client's location from the querying resolver's IP address and returns the address of the nearest server cluster. Li and Huang (2025) find that this geographic routing operates at continent-level granularity for the Twitch CDN: distinct IP address sets are assigned to clients in Europe, North America, and Asia-Pacific. Hours et al. (2016) causally confirm the performance rationale: clients using local ISP resolvers are assigned Akamai CDN servers that are, on average, 20 ms closer in round-trip time than servers assigned to clients using Google Public DNS, translating to a 14% throughput improvement. DNS-based CDN routing thus produces **systematically different** DNS responses from different geographic vantage points.

**IP anycast routing**: DNS root servers, TLD servers, and large public resolvers (Google 8.8.8.8, Cloudflare 1.1.1.1) employ IP anycast: a single global IP address is announced from multiple geographically distributed Points of Presence (PoPs), and BGP routing directs each client to the "nearest" PoP in BGP path-length terms. Koch et al. (2021) demonstrate that more than 95% of users experience some geographic inflation when accessing DNS root servers — being routed to a PoP that is farther than the geographically closest one — because BGP metrics do not correspond to geographic distance. Bortzmeyer (2013) documents this counter-intuitively for the .fr TLD: North American probes route 55% of their queries to the Paris PoP rather than to any transatlantic alternative, due to BGP peering arrangements. Anycast thus creates **BGP attraction basins** — geographic regions whose traffic converges on the same physical instance — that do not respect continental boundaries.

**EDNS Client Subnet (ECS)**: RFC 7871 (Contavalli et al., 2016) specifies the EDNS Client Subnet extension, which allows a recursive resolver to embed a truncated version of the client's IP prefix in its query to the authoritative CDN server. ECS enables the CDN to perform geographic routing based on the end client's network location rather than the resolver's location — partially solving the remote DNS problem identified by Wang et al. (2018), wherein centralized public resolvers (Google 8.8.8.8, Cloudflare 1.1.1.1) cause CDN servers to assign geographically inappropriate replicas. However, ECS carries significant privacy implications (the client prefix is exposed to the authoritative server and on-path observers) and is not universally deployed: Bortzmeyer (n.d., tutorial) reports that only a small fraction of RIPE Atlas probes in Belgium use resolvers that forward ECS options.

The practical consequence of these three mechanisms is that DNS responses for popular domains are **geographically heterogeneous**: clients at different locations receive different responses, reflecting different CDN server assignments, different anycast routing paths, and different resolver configurations. OpenINTEL, despite measuring 50% of the global DNS namespace daily, cannot observe this geographic variation because it operates from a single point in the Netherlands (van Rijswijk-Deij et al., 2016; van Rijswijk-Deij, 2018). The fraction of popular domains that return geographically differentiated responses, the magnitude of that differentiation, the mechanisms that drive it, and its temporal stability remain empirically uncharacterised at population scale. This is the research gap that this thesis addresses.

### 1.1.4 Implications for Research and Practice

The absence of a systematic, longitudinal, spatially distributed DNS measurement dataset constrains multiple research communities:

**Network performance research** cannot retrospectively validate whether CDN operators actually optimised their geographic routing policies over time, or identify which network regions consistently receive suboptimal server assignments. Calder et al. (2015) show empirically that 20% of clients accessing Microsoft's Bing CDN are directed to suboptimal front-end servers, with potential latency savings of 7–100 ms if DNS-based routing were applied. Identifying and quantifying such routing inefficiencies at scale requires distributed measurement data.

**DNS centralisation research** can document that 10 DNS providers host 48.5% of all gTLD domains (Xu et al., 2023), but cannot determine whether this centralisation has a geographic dimension — whether specific regions are more heavily dependent on specific providers, or whether provider failures would have asymmetric geographic impact. Addressing this requires measurement from diverse geographic vantage points.

**Internet simulation** requires historically accurate DNS data from multiple geographic perspectives to construct realistic network models. A simulation of Internet-circa-2023 from a Tokyo vantage point requires knowing what DNS responses a Tokyo client would have received at that time — data that is neither available from OpenINTEL (single Dutch vantage point) nor reconstructible from existing passive DNS datasets (which observe only queries that naturally flowed through specific observation points).

**Policy and sovereignty debates** around DNS infrastructure — including questions of which nations' citizens depend on DNS infrastructure under foreign jurisdiction, and what the geographic exposure of national DNS infrastructure is — require geographically distributed empirical data. Xu et al. (2023) document that over 60% of DNS provider pairs share underlying infrastructure, but the geographic distribution of this shared dependency has not been characterised.

---

## 1.2 Research Problem

### 1.2.1 Main Research Question

This thesis addresses the following main research question:

*How can one design and deploy a distributed DNS measurement system that captures the geographic and temporal diversity of DNS responses for the most popular domains on the web, in a manner that is ethically sound, reproducible, and useful to the research community?*

The question has two inseparable dimensions: the **engineering dimension** (how to build the system) and the **empirical dimension** (what the system reveals about DNS behaviour). The engineering choices — platform, domain corpus, measurement parameters, data format — are motivated by and evaluated against the empirical goals: producing data that accurately characterises the geographic and temporal structure of popular-domain DNS responses.

### 1.2.2 Secondary Research Questions

The main question decomposes into four operational sub-questions that the measurement campaign and analysis directly address:

**Q1 — Geographic diversity**: What proportion of Tranco top-ranked domains return different DNS responses depending on the geographic location of the querying client, and what infrastructure mechanisms (CDN-based routing, anycast, ECS) explain the observed differentiation?

This question quantifies the scale of the phenomenon. If a large proportion of popular domains return identical responses regardless of query origin, then single-vantage-point measurement captures the essential picture and geographically distributed measurement adds little. If, conversely, a substantial proportion return geographically differentiated responses, then the single-vantage-point approach of OpenINTEL systematically misses a critical dimension of the DNS. The answer determines how significant the research gap is in quantitative terms, and guides the interpretation of any DNS study that does not account for geographic variation.

**Q2 — Temporal stability**: What is the temporal stability of DNS responses for popular domains over a multi-month measurement period? Do changes occur at day, week, or month timescales, and are they correlated with identifiable infrastructure events?

This question characterises the dynamics of the DNS at the population level. DNS resource records carry TTLs that reflect administrator intent about how frequently records should be refreshed, but the actual rate of content change — when the *substance* of records changes, not merely their cached lifetime — has not been characterised at the scale of the Tranco top list. Understanding temporal dynamics informs the appropriate measurement frequency for longitudinal archival: if records change rarely, weekly measurements suffice; if records change daily, daily measurement is required.

**Q3 — Geographic bias of RIPE Atlas**: Do the documented geographic biases of the RIPE Atlas probe distribution — 91% of probes in Europe and North America (Bajpai et al., 2017) — significantly affect the ability to observe geographic DNS response variation?

RIPE Atlas is the only platform with sufficient probe count (approximately 12,892 probes in 178 countries as of Nosyk et al., 2024) and built-in DNS measurement support to enable the distributed measurement campaign this thesis requires. However, its geographic distribution is heavily skewed toward Europe and North America. This question evaluates whether probes from underrepresented regions (Africa, Latin America, Southeast Asia, Oceania) produce systematically different DNS observations — indicating that the platform bias limits the validity of global inferences — or whether they corroborate patterns observed in the majority regions, indicating that the bias is acceptable for the study's purposes.

**Q4 — Impact of resolver choice**: What is the measurable impact of resolver choice — local ISP resolver versus public DNS service — on the DNS responses observed, and does it interact with the geographic location of the probe?

The remote DNS problem (Wang et al., 2018) predicts that probes using centralized public resolvers (Google 8.8.8.8, Cloudflare 1.1.1.1) should receive geographically inappropriate CDN assignments relative to probes using local ISP resolvers. This question empirically tests this prediction in the RIPE Atlas context. Xu et al. (2023) further show that over 90% of forwarding resolvers are backed by fewer than 5% of indirect recursive resolvers, meaning that resolver centralisation may cause probes at geographically diverse locations to receive convergent DNS responses — not because the DNS is geographically uniform, but because their resolvers all converge on the same infrastructure. Measuring the impact of this convergence is both practically important (for interpreting the measurement results) and scientifically significant (validating the centralisation thesis of Xu et al., 2023 from a client perspective).

---

## 1.3 Thesis Objectives

### 1.3.1 General Objective

The general objective of this thesis is to design, implement, and operate a **geographically distributed active DNS measurement system** that:

- Measures DNS responses for a representative, stable, and reproducible corpus of popular domains (the Tranco Top list, Le Pochat et al., 2019);
- Collects measurements from a globally distributed set of RIPE Atlas probes selected to maximise geographic coverage while controlling for known platform biases (Bajpai et al., 2017; Nosyk et al., 2024);
- Repeats measurements over a multi-month period to enable temporal analysis;
- Stores results in structured, archivable formats conforming to FAIR data principles (Findable, Accessible, Interoperable, Reusable);
- Analyses the collected data to provide quantitative answers to questions Q1–Q4.

### 1.3.2 Specific Objectives

**Objective 1 — Design an optimal measurement methodology**

The measurement methodology must balance competing constraints: geographic coverage (more probes = better coverage), domain coverage (more domains = more representative corpus), measurement frequency (more frequent = better temporal resolution), and resource consumption (all three dimensions are bounded by the finite RIPE Atlas credit budget). Designing the optimal point in this multidimensional space requires understanding the cost model of RIPE Atlas measurements (Holterbach et al., 2015; Nosyk et al., 2024), the geographic distribution of available probes (Bajpai et al., 2017), and the stability characteristics of the Tranco list (Le Pochat et al., 2019). The measurement methodology must also specify EDNS options (including NSID for anycast instance identification, following Bortzmeyer, 2013 and Finnegan, 2018) and resolver targeting (direct authoritative queries to bypass resolver centralization effects).

**Objective 2 — Implement a robust collection and processing pipeline**

The engineering implementation must reliably collect measurement results via the RIPE Atlas API, parse and validate DNS responses (filtering invalid responses, identifying in-path proxy effects following Jones et al., 2016), and store results in a two-tier format: Apache Avro for long-term archival and Apache Parquet for efficient columnar analytics, following the storage architecture of OpenINTEL (van Rijswijk-Deij et al., 2016). The pipeline must be sufficiently automated to operate over a three-month measurement period with minimal manual intervention.

**Objective 3 — Quantitatively analyse the collected data**

The analysis must produce empirical answers to Q1–Q4: quantifying the proportion of domains with geographically differentiated responses, characterising the distribution and magnitude of geographic variation, measuring the rate and pattern of temporal change, evaluating the effect of geographic probe bias and resolver choice, and identifying the DNS mechanisms (CDN routing, anycast, ECS) responsible for observed variation.

**Objective 4 — Publish data and methodology**

To fulfil the scientific contribution goals of the thesis, the measurement dataset must be published with a permanent identifier (DOI), the methodology must be documented to enable independent replication, and the analysis code must be made openly available. These commitments follow the FAIR data principles and the reproducibility norms of Internet measurement research (van Rijswijk-Deij et al., 2016; Le Pochat et al., 2019).

---

## 1.4 Challenges and Constraints

### 1.4.1 Technical Challenges

**Data volume**: A measurement campaign of 10,000 Tranco domains × 100 RIPE Atlas probes × one measurement per day × 90 days produces approximately 90 million individual DNS query-response records. Each record includes the queried domain, record type, DNS response (potentially multiple resource records), query and response timing, probe metadata (geographic location, ASN, resolver), and EDNS option results (NSID string, ECS scope). After parsing and enrichment, this produces on the order of 20–30 GB of compressed data. The pipeline must handle this volume with sufficient efficiency to process each day's measurements before the next measurement cycle begins.

**Measurement quality and reliability**: Holterbach et al. (2015) demonstrate that simultaneous measurements from multiple RIPE Atlas probes can be desynchronised by up to one hour under high platform load, and that concurrent measurements from other users degrade timing precision by more than 1 ms in the median and more than 7 ms at the 95th percentile. Bortzmeyer (n.d., tutorial) identifies additional quality issues: lying resolvers that return incorrect responses, DNS interception by in-path proxies (Jones et al., 2016), DNSSEC validation failures that produce `SERVFAIL` responses misidentified as unavailability, and cache divergence between probes that confounds geographic and temporal variation. Rigorous filtering and validation are required to distinguish genuine DNS variation from measurement artefacts.

**Infrastructure heterogeneity**: RIPE Atlas probes span three hardware generations with substantially different computing power (Holterbach et al., 2015): Versions 1 and 2 are resource-constrained devices (167 MHz CPU, 8–16 MB RAM) susceptible to timing degradation under concurrent measurement load; Version 3 devices (400 MHz CPU, 32 MB RAM) are more reliable but not immune. Probes also use heterogeneous local resolvers — ISP resolvers, corporate gateways, misconfigured devices — with different caching policies, DNSSEC validation support, and ECS forwarding behaviour (Bajpai et al., 2017). This heterogeneity must be characterised and controlled in the analysis.

### 1.4.2 Operational Constraints

**RIPE Atlas credit budget**: The measurement campaign is bounded by a finite RIPE Atlas credit allocation. The credit cost of each measurement depends on the measurement type, the number of probes, and the scheduling mode: scheduled recurring measurements cost approximately half as much as equivalent one-off measurements (Holterbach et al., 2015). The credit constraint imposes a three-way trade-off between domain coverage (number of domains), geographic coverage (number of probes), and temporal resolution (measurement frequency). Optimising this trade-off within budget while respecting the RIPE Atlas measurement quotas is a central design challenge of the methodology (described in Chapter 3).

**Geographic distribution bias**: As documented by Bajpai et al. (2017) and confirmed by Nosyk et al. (2024), approximately 91% of dual-stacked RIPE Atlas probes are concentrated in the RIPE (Europe/Middle East) and ARIN (North America) regions. Africa, Latin America, Central Asia, and Oceania are substantially underrepresented relative to their shares of the global Internet user population. This concentration means that results will be statistically robust for Europe and North America but are based on smaller samples for other regions. Geographic stratification — selecting probes to ensure minimum coverage of each inhabited continent — mitigates but cannot eliminate this structural limitation.

**Measurement duration**: A Master 60 thesis at the University of Namur imposes a strict time constraint. The measurement period is limited to approximately three months of continuous collection, compared to the ten-plus years of continuous operation achieved by OpenINTEL (van Rijswijk-Deij et al., 2016; van Rijswijk-Deij, 2018). This three-month window enables meaningful temporal analysis at day and week timescales but cannot capture annual seasonality, multi-year trends, or the long-term evolution of DNS infrastructure.

### 1.4.3 Ethical Constraints

Active DNS measurements using volunteer-hosted infrastructure raise ethical responsibilities that must be explicitly built into the research design. Kisteleki et al. (2016) establish the primary ethical framework for RIPE Atlas measurements, grounded in the Menlo Report (2012) and the Belmont Report (1978): RIPE Atlas probe hosts are volunteers whose internet connections generate the measurement traffic, and researchers bear responsibility for ensuring that traffic is benign, proportionate, and does not expose probe hosts to legal or social risk.

For this thesis, three ethical design choices follow from this framework:

**Impact on DNS infrastructure**: van Rijswijk-Deij et al. (2016) demonstrate that OpenINTEL's measurements — 1.85 billion queries per day — represent only 0.3%–1.6% of total DNS traffic at the measured authoritative servers, confirming that well-paced active measurement has negligible infrastructure impact. This thesis's measurement campaign is orders of magnitude smaller and must similarly be paced to avoid creating an undue burden on measured authoritative servers.

**Query target selection**: Following the principles of Kisteleki et al. (2016), the domain corpus is drawn exclusively from the Tranco list of popular, publicly accessible domains. No politically sensitive, censored, or jurisdictionally restricted domains are included: measuring access to blocked content from probes in restrictive jurisdictions could expose probe hosts to legal risk, as illustrated by the "Ebonia" case described in Kisteleki et al. (2016).

**Probe host privacy**: Raw probe IP addresses are not published in the dataset; results are aggregated at country and ASN level for public release, preserving the statistical value of the data while protecting the network location of individual volunteer probe hosts.

---

## 1.5 Methodological Approach

### 1.5.1 Choice of Domain Corpus: The Tranco List

The thesis uses the **Tranco Top list** (Le Pochat et al., 2019) as its domain corpus. This choice is motivated by three requirements identified by the research design:

**Stability for longitudinal analysis**: The domain corpus must remain stable over the three-month measurement period, so that the same domains are measured across all campaign repetitions and temporal comparisons are meaningful. Tranco's 30-day aggregation window produces a list that changes by only 0.6% per day, compared to approximately 50% for the Alexa list after its methodology change in 2018 (Le Pochat et al., 2019). This stability is indispensable: a corpus that changes by 50% daily cannot serve as the foundation for temporal comparison.

**Manipulation resistance for result validity**: Le Pochat et al. (2019) demonstrate that every major commercial domain ranking list can be manipulated at low cost — a single HTTP request suffices to alter a domain's Alexa rank. A manipulated domain list would bias the DNS measurement results toward adversarially placed domains, compromising the scientific validity of the study. Tranco's multi-source aggregation over a 30-day window requires at least four times more effort to manipulate than single-source lists.

**Reproducibility for scientific replication**: Historical Tranco lists are archived and retrievable via a stable URL that includes the list generation parameters, enabling other researchers to obtain the exact domain set used in this study and replicate the measurements. This archivability is a prerequisite for scientific reproducibility that commercial lists — which overwrite their previous version daily — cannot provide.

This thesis focuses on the Tranco Top 10,000 domains, balancing representativeness (capturing the major web services responsible for the largest fraction of Internet traffic) with feasibility within the available RIPE Atlas credit budget.

### 1.5.2 Choice of Measurement Platform: RIPE Atlas

The thesis uses **RIPE Atlas** as its distributed measurement infrastructure, a choice that Bortzmeyer (n.d., tutorial) explicitly recommends as the preferred platform for distributed DNS measurements. Four properties make RIPE Atlas uniquely suitable:

**Geographic distribution**: With approximately 12,892 active probes across 178 countries (Nosyk et al., 2024), RIPE Atlas provides a globally distributed vantage point network that cannot be replicated with academic infrastructure. No alternative platform — CAIDA Archipelago (~170 monitors), SamKnows (~70,000 probes but ISP-deployed), PlanetLab (~300 vantage points) — offers comparable geographic coverage with built-in DNS measurement support (Bajpai et al., 2017; Cicalese et al., 2015).

**Native DNS measurement support**: RIPE Atlas provides built-in DNS measurement types supporting all standard query types (A, AAAA, NS, MX, SOA), DNSSEC validation flags, and EDNS options including NSID (for anycast instance identification) and ECS (for client-subnet-aware routing analysis). This native support avoids the complexity and potential inconsistency of implementing DNS measurement from scratch.

**Community validation**: RIPE Atlas has been used in over 600 academic publications, ensuring that its measurement artefacts, biases, and limitations are well characterised (Nosyk et al., 2024; Holterbach et al., 2015; Bajpai et al., 2017). Results obtained from RIPE Atlas are directly comparable with the existing literature.

**Accessible resource model**: RIPE Atlas operates on a credit economy in which probe hosts earn credits that can be shared with the research community. Stéphane Bortzmeyer confirmed in correspondence with the thesis supervisors (Dejaeghere, 2025) that researchers can readily obtain measurement credits by describing their study to the RIPE Atlas community, making the platform financially accessible to academic research projects.

### 1.5.3 System Architecture Overview

The measurement system follows an architecture inspired by OpenINTEL (van Rijswijk-Deij et al., 2016) but adapted to the constraints and capabilities of RIPE Atlas:

**Domain corpus preparation**: The Tranco Top 10,000 list is retrieved via the Tranco API using a fixed version identifier for reproducibility; domains are filtered for validity and pre-resolved to identify their authoritative name servers.

**Measurement scheduling**: RIPE Atlas user-defined DNS measurements are configured to query each domain's authoritative name servers directly — bypassing local resolvers to control for resolver centralization effects (Xu et al., 2023) — from a geographically stratified probe set. Measurements include the NSID EDNS option to capture anycast instance information (Bortzmeyer, 2013; Finnegan, 2018) and are scheduled as recurring daily campaigns to minimise credit consumption (Holterbach et al., 2015).

**Data collection**: Measurement results are retrieved via the RIPE Atlas REST API and validated. Probes with known system failures (identified via RIPE Atlas system tags following Bajpai et al., 2017) are excluded; in-path proxy signatures (as described by Jones et al., 2016) are flagged.

**Storage**: Results are serialised in Apache Avro format for archival and converted to Apache Parquet for efficient columnar analysis, directly following the data architecture of OpenINTEL (van Rijswijk-Deij et al., 2016).

**Analysis**: The collected dataset is analysed to answer questions Q1–Q4 using geographic aggregation (by continent, country, and ASN), temporal comparison (daily, weekly, monthly), and mechanism attribution (NSID-based anycast instance mapping, CNAME chain analysis, ECS scope analysis).

### 1.5.4 Ethical and Scientific Compliance

**Ethics**: The measurement design complies with the RIPE Atlas ethical guidelines (Kisteleki et al., 2016) and the Menlo Report (2012) framework: all query targets are publicly accessible domains; measurement frequency is set to respect DNS TTLs and avoid server overloading; and no sensitive or politically controversial content is queried.

**Reproducibility**: The measurement methodology and analysis code are documented and published following FAIR data principles. The specific Tranco list version, RIPE Atlas measurement identifiers, probe selection criteria, and analysis scripts are included in the supplementary materials to enable independent replication.

---

## 1.6 Thesis Structure

This thesis is organised in five chapters:

**Chapter 1 — Introduction** (this chapter): Motivates the research by identifying the gap between existing DNS measurement infrastructure and the geographic variation question; states the research questions; describes the objectives, challenges, and methodological approach; and previews the thesis structure.

**Chapter 2 — State of the Art**: Reviews the existing literature across five technical domains directly relevant to the thesis: (1) DNS measurement paradigms — active versus passive, and the OpenINTEL infrastructure; (2) the RIPE Atlas distributed measurement platform and its capabilities, biases, and limitations; (3) anycast routing in DNS infrastructure and the NSID-based instance identification methodology; (4) CDN DNS-based geographic routing, the remote DNS problem, and EDNS Client Subnet; (5) domain ranking lists, from the limitations of commercial lists to the Tranco methodology; (6) DNS infrastructure centralisation; and (7) DNS security dimensions that affect measurement validity. The chapter concludes with a gap analysis that formally positions the thesis contribution.

**Chapter 3 — Methodology**: Describes the measurement methodology in full operational detail: domain corpus selection (Tranco Top 10K, version identifier, filtering criteria); RIPE Atlas probe selection (system tag filters, geographic stratification protocol, probe count per region); DNS measurement configuration (query types, EDNS options, target selection — authoritative versus resolver, scheduling); data collection pipeline (API integration, validation, error handling); storage architecture (Avro schema, Parquet conversion, metadata schema); and analysis methods for each of the four research questions.

**Chapter 4 — Results** *(to be completed after data collection)*: Presents the empirical findings of the measurement campaign — descriptive statistics of the collected dataset; quantitative results for Q1 (geographic diversity), Q2 (temporal stability), Q3 (RIPE Atlas bias assessment), and Q4 (resolver impact); geographic and temporal visualisations; and illustrative case studies of domains exhibiting extreme geographic variation or notable temporal dynamics.

**Chapter 5 — Discussion and Conclusion** *(to be completed after analysis)*: Interprets the results in the context of the state of the art; discusses the limitations of the study (three-month temporal window, RIPE Atlas geographic bias, authoritative query methodology); evaluates the generalisation of findings beyond the Tranco Top 10K corpus; identifies future research directions; and summarises the thesis's contributions to the measurement community.

---

## 1.7 Expected Contributions and Impact

### 1.7.1 Scientific Contributions

**Primary empirical contribution**: This thesis will produce the first systematic, population-scale characterisation of geographic DNS response variation for popular domains, validated over a multi-month longitudinal measurement campaign. Where existing literature contains individual case studies of anycast routing (Bortzmeyer, 2013 for d.nic.fr with ~500 probes; Finnegan, 2018 for UncensoredDNS with 500 probes; Calder et al., 2015 for Microsoft Bing) and individual CDN routing studies (Hours et al., 2016; Li et al., 2025), none has characterised **what proportion of the popular-domain corpus returns geographically differentiated DNS responses**, which mechanisms account for that differentiation, and how the differentiation distributes across geographic regions. Answering these questions at the scale of 10,000 domains and 100+ global vantage points constitutes the novel empirical contribution.

**Methodological contribution**: The measurement methodology developed in this thesis — combining direct authoritative server queries (to bypass resolver centralization), NSID-based anycast tracking, geographically stratified probe selection, and a reproducible Tranco-based domain corpus — addresses three gaps identified in the existing literature (Section 2.10 of Chapter 2) and can be adopted by future measurement studies as a validated protocol.

**Dataset contribution**: The collected dataset — approximately 90 million DNS measurement records covering 10,000 Tranco domains from 100+ globally distributed RIPE Atlas probes over three months, archived in Avro/Parquet format with full metadata — will be published with a permanent DOI on Zenodo. This makes the dataset the first publicly available longitudinal, geographically distributed DNS dataset for the popular-domain tier, directly addressing the data availability gap motivating this thesis.

### 1.7.2 Impact for the Research Community

**Network simulation**: Researchers developing Internet simulators will be able to use the collected dataset to configure realistic DNS responses for simulations representing Internet states from the measurement period and from multiple geographic perspectives.

**CDN and routing research**: Researchers studying CDN performance, anycast routing efficiency, and geographic routing optimisation will have empirical ground truth for the DNS dimension of client routing at population scale.

**DNS security**: Security researchers investigating large-scale DNS manipulation, geographic censorship patterns, or DNS infrastructure resilience will have a baseline dataset of correct DNS responses from diverse vantage points against which anomalous behaviour can be detected.

**DNS infrastructure policy**: Policymakers and regulators addressing digital sovereignty, Internet resilience, and the geographic concentration of critical Internet infrastructure will have empirical data on the geographic structure of DNS dependency at the level of popular domains.

---

## 1.8 Work Organisation

### 1.8.1 Project Phases

The work is organised in five successive phases aligned with the thesis chapter structure:

**Phase 1 — Literature review and familiarisation** (weeks 1–6, January–February 2026): Reading and annotation of the 22 primary sources; construction of the bibliography and source fiches; drafting of Chapter 2 (State of the Art).

**Phase 2 — Design and pilot** (weeks 7–10, February–March 2026): Design of the measurement methodology; implementation of the data collection pipeline; pilot campaign (500 domains, 10 probes, 7 days) to validate technical parameters and estimate credit consumption; drafting of Chapter 3 (Methodology).

**Phase 3 — Full measurement campaign** (weeks 11–22, March–June 2026): Daily automated measurements; monitoring of credit consumption and probe availability; adjustment of measurement parameters if anomalies are detected; incremental validation of collected data.

**Phase 4 — Analysis** (weeks 23–26, June 2026): Complete analysis addressing Q1–Q4; generation of visualisations and statistical results; drafting of Chapter 4 (Results).

**Phase 5 — Discussion, revision, and defence** (weeks 27–30, June–July 2026): Drafting Chapter 5 (Discussion and Conclusion); complete thesis revision; dataset and code publication; preparation of the oral defence.

### 1.8.2 Success Criteria

The thesis will be considered successful against the following measurable criteria:

**Technical**: At least 85% of scheduled measurements produce valid, parseable DNS responses; at least 95% of Tranco Top 10K domains are covered in the dataset; at least four inhabited continents are represented by RIPE Atlas probes in the final probe selection.

**Scientific**: Quantitative answers to all four research questions (Q1–Q4) are provided with appropriate statistical characterisation (confidence intervals, statistical tests where applicable); the methodological contribution is sufficiently documented to enable independent replication.

**Academic**: A complete five-chapter thesis is submitted in conformance with the University of Namur Master 60 format requirements; the dataset is published with a permanent DOI before the oral defence; ethical guidelines (Kisteleki et al., 2016; Menlo Report, 2012) are demonstrably respected in the measurement design.

---

## Bibliography

*(Full references in the thesis bibliography file)*

- Bajpai, V., Jacob Eravuchira, S., Schönwälder, J., Kisteleki, R., & Aben, E. (2017). Vantage Point Selection for IPv6 Measurements: Benefits and Limitations of RIPE Atlas Tags. IM 2017.
- Bortzmeyer, S. (n.d.). DNS Measurements with RIPE Atlas (Tutorial). RIPE presentation.
- Bortzmeyer, S. (2013). Using RIPE Atlas to Find the Most Popular Instances of a DNS Anycast Name Server. *RIPE Labs*.
- Calder, M., Flavel, A., Katz-Bassett, E., Mahajan, R., & Padhye, J. (2015). Analyzing the Performance of an Anycast CDN. IMC 2015.
- Cicalese, D., Augé, J., Joumblatt, D., Friedman, T., & Rossi, D. (2015). Characterizing IPv4 Anycast Adoption and Deployment. CoNEXT 2015.
- Contavalli, C., van der Gaast, W., Lawrence, D., & Kumari, W. (2016). RFC 7871: Client Subnet in DNS Queries. IETF.
- Dejaeghere, J., & Rochet, F. (2025). Thesis subject: DNS Measurements in Space and Time. University of Namur (internal document).
- Finnegan, K. (2018). Measuring Anycast DNS Services Using RIPE Atlas. *RIPE Labs*.
- Holterbach, T., Pelsser, C., Bush, R., & Vanbever, L. (2015). Quantifying Interference between Measurements on the RIPE Atlas Platform. IMC 2015.
- Hours, H., Biersack, E., Loiseau, P., Finamore, A., & Mellia, M. (2016). A Study of the Impact of DNS Resolvers on CDN Performance Using a Causal Approach. Computer Networks.
- Jones, B., Feamster, N., Paxson, V., Weaver, N., & Allman, M. (2016). Detecting DNS Root Manipulation. PAM 2016.
- Kisteleki, R. et al. (2016). Ethics of RIPE Atlas Measurements. *RIPE Labs*.
- Koch, T., Li, K., Ardi, C., Katz-Bassett, E., Calder, M., & Heidemann, J. (2021). Anycast in Context: A Tale of Two Systems. ACM SIGCOMM 2021.
- Le Pochat, V., Van Goethem, T., Tajalizadehkhoob, S., Korczyński, M., & Joosen, W. (2019). Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation. NDSS 2019.
- Li, X. et al. (2025). Measurement and Analysis of a Global-Scale CDN. AINTEC 2025.
- Nosyk, Y. et al. (2024). Day in the Life of RIPE Atlas: Operational Insights and Applications in Network Measurements. arXiv:2511.22474.
- van der Toorn, O., van Rijswijk-Deij, R., Geesink, B., & Sperotto, A. (2018). Melting the Snow: Using Active DNS Measurements to Detect Snowshoe Spam Domains. NOMS 2018.
- van Rijswijk-Deij, R., Jonker, M., Sperotto, A., & Pras, A. (2016). A High-Performance, Scalable Infrastructure for Large-Scale Active DNS Measurements. IEEE JSAC.
- van Rijswijk-Deij, R. (2018). The Ongoing Story of OpenINTEL. NLnet Labs Blog.
- Wang, Z., Huang, J., & Rose, S. (2018). Evolution and Challenges of DNS-Based CDNs. Digital Communications and Networks.
- Xu, C. et al. (2023). Measuring the Centrality of DNS Infrastructure in the Wild. Applied Sciences.
