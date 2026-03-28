# Chapter 4 - Results

> **Note.** This chapter presents the empirical results of the measurement campaign described in Chapter 3. All quantitative values appear as `[VALUE]` placeholders to be filled once data collection and analysis are complete. Figure references indicate planned visualisations. The interpretive framing of each section anticipates the expected results based on the literature reviewed in Chapter 2; where actual results diverge from expectations, the placeholders are accompanied by a `[NOTE: unexpected — discuss in Ch. 5]` flag.

---

## 4.1 Dataset Overview

### 4.1.1 Collection Statistics

The measurement campaign ran from [DATE_START] to [DATE_END], covering [VALUE] calendar days of active data collection. Table 4.1 summarises the overall collection statistics.

**Table 4.1 — Campaign summary statistics**

| Metric | Value |
|---|---|
| Measurement period | [DATE_START] – [DATE_END] ([VALUE] days) |
| Tranco list version | [TRANCO_ID] (retrieved [DATE]) |
| Domains in Tranco Top 10K | 10,000 |
| Domains after pre-filtering | [VALUE] (~[VALUE]% of 10K) |
| Domains with ≥85% valid results | [VALUE] |
| Total measurement instances scheduled | [VALUE] |
| Total results retrieved from RIPE Atlas API | [VALUE] |
| Results passing all validation filters | [VALUE] ([VALUE]%) |
| Days with complete collection (all measurements retrieved) | [VALUE] / [VALUE] |
| Days with partial collection (API error or scheduling failure) | [VALUE] |

The [VALUE] domains excluded at the pre-filtering stage (Section 3.2.3) consisted primarily of domains returning `NXDOMAIN` at the reference resolver ([VALUE] domains, [VALUE]%) and domains flagged by the Google Safe Browsing API ([VALUE] domains, [VALUE]%). The remaining [VALUE] domains formed the active measurement corpus for the duration of the campaign.

### 4.1.2 Probe Distribution

The measurement campaign used [VALUE] unique RIPE Atlas probes distributed across [VALUE] countries and [VALUE] Autonomous Systems. Table 4.2 summarises the geographic distribution of the probe set and compares it to the target allocation defined in Section 3.3.1.

**Table 4.2 — Geographic probe distribution: target vs. actual**

| Region | Target probes | Actual probes | Countries covered | ASes covered |
|---|---|---|---|---|
| Europe | 30 | [VALUE] | [VALUE] | [VALUE] |
| North America | 25 | [VALUE] | [VALUE] | [VALUE] |
| Asia-Pacific | 20 | [VALUE] | [VALUE] | [VALUE] |
| South America | 10 | [VALUE] | [VALUE] | [VALUE] |
| Africa | 10 | [VALUE] | [VALUE] | [VALUE] |
| Oceania | 5 | [VALUE] | [VALUE] | [VALUE] |
| **Total** | **100** | **[VALUE]** | **[VALUE]** | **[VALUE]** |

Deviations from the target allocation reflect the availability of probes satisfying the system-tag requirements (Section 3.3.1) in specific regions. The largest deviation is observed in [REGION], where only [VALUE] probes satisfying all selection criteria were available, compared to the target of [VALUE].

### 4.1.3 Data Quality

Table 4.3 summarises the application of the four validation filters described in Section 3.4.3. The overall valid result rate of [VALUE]% is [above / below / consistent with] the 85–90% expected rate estimated in Chapter 3.

**Table 4.3 — Validation filter outcomes**

| Filter | Results excluded | Percentage | Primary causes |
|---|---|---|---|
| Timeout (no abuf received) | [VALUE] | [VALUE]% | Probe offline, network timeout |
| Scheduling deviation >4h | [VALUE] | [VALUE]% | Platform concurrent load (Holterbach et al., 2015) |
| RCODE ≠ NOERROR | [VALUE] | [VALUE]% | NXDOMAIN ([VALUE]%), SERVFAIL ([VALUE]%), REFUSED ([VALUE]%) |
| Anomalous response flag | [VALUE] | [VALUE]% | Suspected in-path proxy or local cache interception |
| **Total excluded** | **[VALUE]** | **[VALUE]%** | |
| **Valid results** | **[VALUE]** | **[VALUE]%** | Used in all subsequent analyses |

The [VALUE]% of results returning RCODE `SERVFAIL` were separately examined for DNSSEC correlation. [VALUE]% of `SERVFAIL` results were from domains with incomplete DNSSEC chains (detectable via the absence of a valid RRSIG record in the authority section), consistent with the systemic DNSSEC key management failures documented by van Rijswijk-Deij et al. (2016). The remaining [VALUE]% of `SERVFAIL` responses may reflect transient authoritative server issues.

The [VALUE] results flagged as anomalous correspond to [VALUE] distinct (probe, domain) pairs. Of these, [VALUE] pairs show a persistent pattern across multiple measurement days — consistent with systematic in-path proxy behaviour rather than transient network anomalies. These pairs are excluded from all subsequent analyses.

### 4.1.4 Storage

**Table 4.4 — Storage volumes by format**

| Format | Size | Compression ratio vs. raw JSON |
|---|---|---|
| Raw JSON (RIPE Atlas API output) | [VALUE] GB | 1:1 (baseline) |
| Apache Avro (archival tier) | [VALUE] GB | 1:[VALUE] |
| Apache Parquet (analytics tier) | [VALUE] GB | 1:[VALUE] |
| **Total** | **[VALUE] GB** | |

The Avro compression ratio of 1:[VALUE] is [consistent with / lower than / higher than] the 1:7.4 ratio reported by van Rijswijk-Deij et al. (2016) for OpenINTEL, [likely due to the smaller average record size / the higher string cardinality in the probe metadata fields].

---

## 4.2 Results for Q1: Geographic Diversity of DNS Responses

### 4.2.1 Overall Distribution of Geographic Diversity

**Research question**: What proportion of Tranco Top 10K domains return geographically differentiated DNS responses, and what infrastructure mechanisms explain the differentiation?

For each domain in the active corpus, the geographic diversity metric — the median pairwise Jaccard similarity across continental probe pairs (Section 3.5.1) — was computed over the full measurement period. Table 4.5 reports the distribution of domains across the four diversity categories.

**Table 4.5 — Distribution of domains by geographic diversity category**

| Category | Criterion | Domains | Percentage |
|---|---|---|---|
| `UNIFORM` | Single IP across all probes | [VALUE] | [VALUE]% |
| `LOW_DIVERSITY` | Median pairwise Jaccard > 0.8 | [VALUE] | [VALUE]% |
| `MEDIUM_DIVERSITY` | Median pairwise Jaccard 0.4–0.8 | [VALUE] | [VALUE]% |
| `HIGH_DIVERSITY` | Median pairwise Jaccard < 0.4 | [VALUE] | [VALUE]% |
| **Total** | | **[VALUE]** | **100%** |

**Figure 4.1** — Bar chart: number of domains per diversity category, with mean number of distinct IP addresses per category on secondary axis. [TODO: generate from analysis output]

[VALUE]% of measured domains exhibit at least some geographic variation in their DNS responses (categories `LOW_DIVERSITY` through `HIGH_DIVERSITY`). Of these, [VALUE]% ([VALUE] domains) show strong geographic differentiation (`MEDIUM` and `HIGH` categories combined), consistent with the use of geographically distributed CDN infrastructure for their DNS-based routing. The [VALUE]% classified as `UNIFORM` represent domains with a single globally consistent IP address — typically small websites hosted on non-CDN infrastructure without anycast routing.

The geographic diversity level correlates with Tranco rank: the top-100 domains show a median pairwise Jaccard of [VALUE], compared to [VALUE] for the 5,000–10,000 rank tier. This is consistent with the expectation that the highest-traffic sites are more likely to operate large-scale CDN infrastructure.

### 4.2.2 Mechanism Attribution: Anycast vs. DNS-Based CDN Routing

For domains in the `HIGH_DIVERSITY` category, the NSID strings collected from authoritative servers (Section 3.3.2) allow the primary mechanism of geographic variation to be identified. Two patterns are observed:

**Anycast-driven variation**: [VALUE] domains ([VALUE]% of `HIGH_DIVERSITY`) show consistent A record IP addresses within each continental probe group, but different NSID strings across groups. This pattern indicates that the same IP space is served from different physical anycast instances — the geographic variation in DNS response content reflects different authoritative server instances rather than different CDN server assignments.

**CDN routing-driven variation**: [VALUE] domains ([VALUE]% of `HIGH_DIVERSITY`) show varying A record IP addresses across continental probe groups but a consistent or near-consistent NSID string. This pattern indicates that a single authoritative server instance (or a small set of instances) is returning different IP addresses based on the inferred location of the querying probe — the canonical DNS-based CDN routing mechanism described by Wang et al. (2018).

[VALUE] domains ([VALUE]% of `HIGH_DIVERSITY`) exhibit both mechanisms simultaneously, consistent with CDN operators that both anycasted their authoritative name servers and perform location-based IP address selection.

**Figure 4.2** — Stacked bar chart: mechanism attribution (anycast, CDN routing, both, undetermined) per diversity category. [TODO: generate from NSID analysis]

### 4.2.3 DNS Infrastructure Provider Distribution

Authoritative DNS infrastructure providers were identified by mapping NS records to known provider AS ranges and hostname patterns. Table 4.6 summarises the distribution of providers for domains exhibiting geographic variation (`MEDIUM` and `HIGH` diversity categories).

**Table 4.6 — DNS infrastructure provider distribution for geographically diverse domains**

| Provider | Domains | Percentage of diverse domains | Mean distinct IPs |
|---|---|---|---|
| Cloudflare | [VALUE] | [VALUE]% | [VALUE] |
| Amazon Route 53 | [VALUE] | [VALUE]% | [VALUE] |
| Akamai | [VALUE] | [VALUE]% | [VALUE] |
| Google Cloud DNS | [VALUE] | [VALUE]% | [VALUE] |
| Fastly | [VALUE] | [VALUE]% | [VALUE] |
| Other identified | [VALUE] | [VALUE]% | [VALUE] |
| Unidentified | [VALUE] | [VALUE]% | [VALUE] |

The top [VALUE] providers account for [VALUE]% of all domains with geographic diversity, consistent with the concentration levels documented by Xu et al. (2023), who found that 10 providers host 48.5% of all gTLD domain names. **Figure 4.3** shows the provider market share distribution. [TODO: pie chart from provider mapping]

---

## 4.3 Results for Q2: Temporal Stability

### 4.3.1 Aggregate Change Rates by Timescale

**Research question**: What is the temporal stability of DNS responses for popular domains at day, week, and month timescales?

Table 4.7 reports the distribution of domain-level change rates (1 − mean consecutive Jaccard similarity) at three temporal scales.

**Table 4.7 — DNS response change rates by temporal scale**

| Timescale | Mean change rate | Median change rate | Standard deviation | 95th percentile |
|---|---|---|---|---|
| Daily (consecutive days) | [VALUE]% | [VALUE]% | [VALUE]% | [VALUE]% |
| Weekly (consecutive weeks) | [VALUE]% | [VALUE]% | [VALUE]% | [VALUE]% |
| Monthly (consecutive months) | [VALUE]% | [VALUE]% | [VALUE]% | [VALUE]% |

**Figure 4.4** — Histograms of daily, weekly, and monthly change rates across all measured domains. [TODO: three-panel plot from temporal analysis]

The daily mean change rate of [VALUE]% indicates that, on average, [VALUE]% of IP addresses observed for a given domain change from one day to the next when aggregated across all probes. This figure is [higher than / lower than / similar to] the 0.6% daily change rate of the Tranco list itself (Le Pochat et al., 2019), indicating that [DNS response content is more / less volatile than the domain popularity ranking].

### 4.3.2 Domain Stability Classification

Table 4.8 reports the distribution of domains across stability categories (Section 3.5.2) at the daily timescale.

**Table 4.8 — Domain stability classification at daily timescale**

| Stability class | Change rate | Domains | Percentage |
|---|---|---|---|
| `VERY_STABLE` | < 5% | [VALUE] | [VALUE]% |
| `STABLE` | 5–20% | [VALUE] | [VALUE]% |
| `MODERATE` | 20–50% | [VALUE] | [VALUE]% |
| `VOLATILE` | > 50% | [VALUE] | [VALUE]% |

[VALUE]% of measured domains are either `VERY_STABLE` or `STABLE`, indicating that their DNS responses change by less than 20% of IP addresses per day. At the weekly timescale, the stability distribution [shifts toward lower stability / remains similar], reflecting [accumulated gradual changes / infrastructure migration events] that are not visible in daily comparisons. **Figure 4.5** illustrates the stability distribution across all three temporal scales. [TODO: stacked bar chart]

### 4.3.3 TTL and Change Rate Correlation

The Spearman rank correlation between each domain's median A record TTL and its daily change rate is:

$$\rho = [VALUE], \quad p = [VALUE]$$

This result [confirms / does not confirm] the hypothesis that domains with shorter TTLs exhibit more frequent IP address changes. A [negative / near-zero] correlation of [VALUE] indicates that [TTL is a moderate predictor of DNS response volatility, consistent with CDN operators using short TTLs to enable rapid traffic redirection / TTL does not reliably predict actual change rates, suggesting that DNS administrators set TTLs based on factors other than anticipated change frequency].

**Figure 4.6** — Scatter plot (log-scale x-axis): median TTL vs. daily change rate per domain, coloured by diversity category. [TODO: generate from correlation analysis]

### 4.3.4 Most Volatile Domains

Table 4.9 lists the ten most volatile domains in the corpus (highest daily change rate), representing domains whose IP address set changes most dramatically from day to day. These case studies are examined qualitatively in Chapter 5.

**Table 4.9 — Ten most volatile domains (daily change rate)**

| Rank | Domain | Daily change rate | Median TTL (s) | Provider | Category |
|---|---|---|---|---|---|
| 1 | [DOMAIN] | [VALUE]% | [VALUE] | [VALUE] | [VALUE] |
| 2 | [DOMAIN] | [VALUE]% | [VALUE] | [VALUE] | [VALUE] |
| ... | ... | ... | ... | ... | ... |
| 10 | [DOMAIN] | [VALUE]% | [VALUE] | [VALUE] | [VALUE] |

---

## 4.4 Results for Q3: RIPE Atlas Geographic Bias Assessment

### 4.4.1 Subsampling Experiment Results

**Research question**: Do the geographic biases of the RIPE Atlas probe distribution significantly limit the ability to observe geographic DNS response variation?

Table 4.10 compares the domain-level geographic diversity metric across the three virtual probe sets (Section 3.5.3).

**Table 4.10 — Geographic diversity observed under three probe sampling strategies**

| Sampling strategy | Mean distinct IPs per domain | Median Jaccard similarity | Domains classified `HIGH_DIVERSITY` |
|---|---|---|---|
| `ACTUAL` (deployed probe set) | [VALUE] | [VALUE] | [VALUE] ([VALUE]%) |
| `UNIFORM` (equal probes per continent) | [VALUE] | [VALUE] | [VALUE] ([VALUE]%) |
| `EUROPE_NA_ONLY` (91% of natural distribution) | [VALUE] | [VALUE] | [VALUE] ([VALUE]%) |

**Figure 4.7** — Box plots: distribution of per-domain distinct IP counts under the three sampling strategies. [TODO: generate from subsampling analysis]

### 4.4.2 Statistical Significance Tests

The Wilcoxon signed-rank test (paired, non-parametric) comparing the per-domain distinct-IP-count distributions yields the following results:

**ACTUAL vs. UNIFORM**:

$$W = [VALUE], \quad p = [VALUE]$$

**ACTUAL vs. EUROPE\_NA\_ONLY**:

$$W = [VALUE], \quad p = [VALUE]$$

The comparison between `ACTUAL` and `UNIFORM` is [statistically significant at α = 0.05 / not statistically significant], indicating that the geographic stratification strategy [meaningfully increases / does not significantly increase] the diversity observed compared to a geographically uniform probe distribution. The comparison between `ACTUAL` and `EUROPE_NA_ONLY` is [statistically significant / not statistically significant], indicating that [underrepresented regions contribute materially to the observed diversity / the Europe/North America majority captures most of the diversity in the corpus].

### 4.4.3 Regional Unique IP Contribution

Table 4.11 reports the fraction of IP addresses seen exclusively from probes in each continent (not observed from any other region's probes), a measure of each region's unique informational contribution to the dataset.

**Table 4.11 — Unique IP address contribution by region**

| Region | Probe share (%) | Unique IP contribution (%) | Contribution / probe share ratio |
|---|---|---|---|
| Europe | [VALUE]% | [VALUE]% | [VALUE] |
| North America | [VALUE]% | [VALUE]% | [VALUE] |
| Asia-Pacific | [VALUE]% | [VALUE]% | [VALUE] |
| South America | [VALUE]% | [VALUE]% | [VALUE] |
| Africa | [VALUE]% | [VALUE]% | [VALUE] |
| Oceania | [VALUE]% | [VALUE]% | [VALUE] |

The highest contribution-to-probe-share ratio is observed for [REGION] ([VALUE]), indicating that probes in this region are the most informative per probe relative to their natural availability in RIPE Atlas. This finding [supports / moderates] the concern that the European/North American concentration of RIPE Atlas probes systematically under-samples DNS variation in underrepresented regions.

**Figure 4.8** — Bar chart: unique IP contribution vs. probe share, per region. [TODO: generate from regional contribution analysis]

### 4.4.4 Classification Changes Induced by Sampling Strategy

Table 4.12 reports the number of domains whose diversity category changes when the sampling strategy is altered, quantifying the practical impact of geographic bias on study conclusions.

**Table 4.12 — Domain reclassifications induced by sampling strategy change**

| Classification change | ACTUAL → UNIFORM | ACTUAL → EUROPE\_NA\_ONLY |
|---|---|---|
| `UNIFORM` → `LOW_DIVERSITY` or higher | [VALUE] | [VALUE] |
| `LOW_DIVERSITY` → `MEDIUM_DIVERSITY` or higher | [VALUE] | [VALUE] |
| `MEDIUM_DIVERSITY` → `HIGH_DIVERSITY` | [VALUE] | [VALUE] |
| **Total domains reclassified** | **[VALUE] ([VALUE]%)** | **[VALUE] ([VALUE]%)** |

---

## 4.5 Results for Q4: Impact of Resolver Choice

### 4.5.1 Resolver Distribution in the Supplementary Campaign

The supplementary Q4 campaign (Section 3.3.5) covered the Tranco Top 1,000 domains using four measurement types from the same probe set. Table 4.13 characterises the resolver distribution in the `isp_resolver` campaign arm.

**Table 4.13 — Resolver classification in the ISP resolver campaign arm**

| Resolver type | Probe count | Percentage |
|---|---|---|
| ISP local resolver (inferred) | [VALUE] | [VALUE]% |
| Google Public DNS (8.8.8.8 / 8.8.4.4) | [VALUE] | [VALUE]% |
| Cloudflare (1.1.1.1 / 1.0.0.1) | [VALUE] | [VALUE]% |
| Quad9 (9.9.9.9) | [VALUE] | [VALUE]% |
| Other identified public resolver | [VALUE] | [VALUE]% |

### 4.5.2 Pairwise IP Address Comparison

For each of the 1,000 domains and each probe, the four campaign arms are compared using pairwise Jaccard similarity. Table 4.14 reports the mean pairwise similarities across all probes and all domains.

**Table 4.14 — Mean pairwise Jaccard similarity between campaign arms**

| Comparison | Mean Jaccard | Interpretation |
|---|---|---|
| `auth_direct` vs `isp_resolver` | [VALUE] | ISP resolver reflects probe network location |
| `auth_direct` vs `public_dns` | [VALUE] | Remote DNS problem magnitude |
| `auth_direct` vs `public_dns_noecs` | [VALUE] | Pure ECS-disabled public DNS divergence |
| `isp_resolver` vs `public_dns` | [VALUE] | Impact of ECS on routing accuracy |
| `isp_resolver` vs `public_dns_noecs` | [VALUE] | Resolver-location effect without ECS |
| `public_dns` vs `public_dns_noecs` | [VALUE] | Isolated ECS contribution |

**Figure 4.9** — Histograms of per-domain Jaccard similarity for each comparison pair. [TODO: six-panel figure from Q4 analysis]

The key finding is that the mean `isp_resolver` vs. `public_dns` Jaccard of [VALUE] indicates [strong / moderate / weak] evidence for the remote DNS problem described by Wang et al. (2018) and quantified by Hours et al. (2016). A comparison with `public_dns_noecs` Jaccard of [VALUE] allows the ECS contribution to be isolated: [VALUE]% of the divergence between `isp_resolver` and `public_dns` is attributable to ECS-based geographic routing correction.

### 4.5.3 Geographic Disaggregation of Resolver Impact

The resolver comparison results disaggregated by continent reveal [the expected regional pattern: probes in Asia and South America, where Google's resolver infrastructure is more geographically concentrated, show larger divergence between `isp_resolver` and `public_dns_noecs` than European or North American probes / an unexpected pattern: see Chapter 5]. Table 4.15 reports the mean `isp_resolver` vs. `public_dns_noecs` Jaccard similarity by continent.

**Table 4.15 — Mean ISP resolver vs. Google DNS (no ECS) Jaccard similarity by continent**

| Continent | Mean Jaccard | Standard deviation | Domains with Jaccard < 0.5 |
|---|---|---|---|
| Europe | [VALUE] | [VALUE] | [VALUE]% |
| North America | [VALUE] | [VALUE] | [VALUE]% |
| Asia-Pacific | [VALUE] | [VALUE] | [VALUE]% |
| South America | [VALUE] | [VALUE] | [VALUE]% |
| Africa | [VALUE] | [VALUE] | [VALUE]% |
| Oceania | [VALUE] | [VALUE] | [VALUE]% |

**Figure 4.10** — Choropleth map: mean `isp_resolver` vs. `public_dns_noecs` Jaccard similarity per country, illustrating geographic gradient of the remote DNS problem. [TODO: generate from geographic disaggregation]

### 4.5.4 Statistical Tests

The Mann-Whitney U tests (non-parametric, Bonferroni-corrected for six comparisons) yield the following results for the six pairwise comparisons:

**Table 4.16 — Statistical tests for resolver comparison pairs**

| Comparison | U statistic | Corrected p-value | Significant (α = 0.05/6) |
|---|---|---|---|
| `auth_direct` vs `isp_resolver` | [VALUE] | [VALUE] | [YES/NO] |
| `auth_direct` vs `public_dns` | [VALUE] | [VALUE] | [YES/NO] |
| `auth_direct` vs `public_dns_noecs` | [VALUE] | [VALUE] | [YES/NO] |
| `isp_resolver` vs `public_dns` | [VALUE] | [VALUE] | [YES/NO] |
| `isp_resolver` vs `public_dns_noecs` | [VALUE] | [VALUE] | [YES/NO] |
| `public_dns` vs `public_dns_noecs` | [VALUE] | [VALUE] | [YES/NO] |

---

## 4.6 Summary of Results

### 4.6.1 Answers to the Research Questions

**Q1 — Geographic diversity**: [VALUE]% of measured Tranco Top 10K domains return geographically differentiated DNS responses (at least `LOW_DIVERSITY`), and [VALUE]% exhibit strong geographic differentiation (`MEDIUM` or `HIGH` diversity). Of the highly diverse domains, [VALUE]% are driven primarily by DNS-based CDN routing and [VALUE]% by anycast instance selection.

**Q2 — Temporal stability**: The mean daily DNS response change rate is [VALUE]%, with [VALUE]% of domains classified as `VERY_STABLE` or `STABLE` (< 20% daily change rate). Temporal stability [is / is not] significantly correlated with A record TTL (Spearman ρ = [VALUE], p = [VALUE]).

**Q3 — RIPE Atlas geographic bias**: The geographic stratification strategy employed in this thesis [significantly increases / does not significantly increase] the observed diversity compared to a naive Europe/North America-only deployment (Wilcoxon p = [VALUE]). [REGION] exhibits the highest unique IP contribution per probe ([VALUE]), confirming that [underrepresented regions provide materially different DNS observations / the geographic bias is acceptable for this study's corpus].

**Q4 — Resolver impact**: The mean ISP resolver vs. Google Public DNS Jaccard similarity of [VALUE] confirms [moderate / strong / weak] evidence for the remote DNS problem in the RIPE Atlas probe population. ECS accounts for [VALUE]% of the divergence correction between Google DNS and local ISP resolvers, [validating / partially validating / not validating] the ECS mechanism as a solution to geographic routing degradation (Wang et al., 2018; Contavalli et al., 2016).

### 4.6.2 Unexpected Findings

The following observations were not anticipated by the pre-analysis hypotheses and are discussed further in Chapter 5:

**Unexpected finding 1**: [DESCRIPTION — to be completed after analysis.] This finding contrasts with [PRIOR EXPECTATION based on literature] and may indicate [HYPOTHESIS].

**Unexpected finding 2**: [DESCRIPTION — to be completed after analysis.] [Further context.]

### 4.6.3 Result Limitations

The results presented in this chapter are subject to the following constraints, discussed further in Chapter 5:

- **Measurement period**: Three months of collection captures daily and weekly dynamics but cannot detect annual seasonality or multi-year infrastructure evolution trends.
- **Domain corpus**: Results are representative of the Tranco Top 10,000 popular domains; extrapolation to the long tail of less popular domains would require separate study.
- **Platform bias**: Despite geographic stratification, RIPE Atlas probe coverage remains unequal across continents; the Q3 analysis quantifies but does not eliminate this limitation.
- **Timing precision**: Measurement desynchronisation of up to one hour (Holterbach et al., 2015) affects the precision of simultaneous multi-probe comparisons; results aggregated over daily windows are less affected than per-second analyses.

---

*Chapter 5 interprets these results in relation to the existing literature, discusses study limitations, and identifies directions for future research.*
