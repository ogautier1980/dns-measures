# Chapter 3 - Methodology

> **Note on sourcing.** This chapter describes the technical methodology of the thesis measurement campaign. Sources from the bibliography are cited where the methodology is directly informed by or adapted from prior work. General software engineering choices (API usage, data format parameters, statistical tests) are not attributed to sources.

---

## 3.1 Overview

### 3.1.1 Methodological Objective

The overarching methodological objective of this thesis is to capture the **geographic and temporal diversity of DNS responses** for a representative corpus of popular domains, using geographically distributed active measurements, in a manner that is reproducible, ethically sound, and practically feasible within the available resource budget. The system must answer four empirical research questions:

- **Q1**: What proportion of Tranco top-ranked domains return geographically differentiated DNS responses, and what infrastructure mechanisms explain the differentiation?
- **Q2**: What is the temporal stability of DNS responses for popular domains at day, week, and month timescales?
- **Q3**: Do the geographic biases of the RIPE Atlas probe distribution significantly limit the ability to observe geographic DNS variation?
- **Q4**: What is the measurable impact of resolver type — local ISP resolver versus public DNS service — on the DNS responses observed?

### 3.1.2 System Architecture

The measurement system is organised in five sequential stages, inspired by the architecture of OpenINTEL (van Rijswijk-Deij et al., 2016) but adapted to the constraints and capabilities of the RIPE Atlas platform:

1. **Domain corpus preparation**: Retrieval and filtering of the Tranco Top 10,000 domain list.
2. **Measurement scheduling**: Configuration and deployment of RIPE Atlas DNS measurement campaigns.
3. **Data collection**: Automated daily retrieval of measurement results via the RIPE Atlas REST API.
4. **Storage and preprocessing**: Parsing, validation, and archival in Avro/Parquet format.
5. **Analysis**: Quantitative analysis addressing Q1–Q4.

The key design trade-off throughout is the three-way tension between **domain coverage** (how many domains are measured), **geographic coverage** (how many geographically distributed probes), and **temporal resolution** (measurement frequency), all bounded by the finite RIPE Atlas credit budget. The configuration described in this chapter targets 10,000 domains × 100 probes × once daily as the primary operating point, with a supplementary resolver-comparison campaign for Q4.

---

## 3.2 Domain Corpus Selection

### 3.2.1 Tranco List Configuration

The domain corpus is the **Tranco Top 10,000** list, retrieved via the Tranco API at https://tranco-list.eu. The choice of Tranco over commercial ranking lists (Alexa, Cisco Umbrella, Majestic) is motivated in Chapter 2 (Section 2.7) and rests on three properties established by Le Pochat et al. (2019): stability (0.6% daily change versus approximately 50% for post-2018 Alexa), manipulation resistance (quadrupled manipulation effort relative to single-source lists), and archivability (each generated list is assigned a unique identifier — e.g., `8QNZ` — retrievable indefinitely via permalink).

The Tranco list is generated with the following fixed configuration to ensure reproducibility:

```
List size:          10,000 domains
Averaging window:   30 days (Tranco default)
Aggregation method: Dowdall rule (weights rank as 1/rank_i per source)
Sources:            Alexa, Cisco Umbrella, Majestic, Quantcast
Filters:            responsiveness (HTTP 200), safe browsing (Google Safe Browsing API)
```

The Dowdall rule was chosen over the Borda count because its 1/rank weighting more closely reflects the Zipfian distribution of Internet traffic: the difference between ranks 1 and 2 is treated as more significant than the difference between ranks 999 and 1,000.

The list is **updated weekly** (each Monday) to capture the slow evolution of the popular-domain corpus while limiting the rate of change introduced by list updates. The stable 0.6% daily change rate of Tranco (Le Pochat et al., 2019) means that even weekly updates produce minimal domain set churn. Each weekly update records the exact Tranco list identifier used, the list generation timestamp, and the delta of added and removed domains relative to the previous week's list. Domains that exit the Top 10K during the measurement campaign are retained in active measurement for two additional weeks to capture any transitional DNS behaviour.

### 3.2.2 Domain Corpus Size

The choice of 10,000 domains balances three competing requirements:

**Representativeness**: The Tranco Top 10K contains the domains responsible for the large majority of global web traffic, including major CDN-backed services (streaming platforms, search engines, social networks, cloud providers) that are expected to exhibit the richest geographic DNS variation. The Top 1K would be sufficient to study the largest infrastructure operators but would miss the diversity of deployment patterns across the broader popular-domain tier.

**Feasibility**: At 100 probes per measurement, one measurement type (A record), and one measurement per domain per day, the Top 10K corpus generates approximately one million measurement results per day. This volume is manageable within the available RIPE Atlas credit budget (van Rijswijk-Deij et al., 2016, for budget modelling reference). The Top 100K would be an order of magnitude larger and would require substantially more credits.

**Established precedent**: The Tranco Top 10K is the standard corpus size used in DNS measurement and web measurement studies (Calder et al., 2015; Wang et al., 2018), enabling direct comparison with prior work.

### 3.2.3 Domain Filtering

Before the measurement campaign begins, each domain in the Tranco Top 10K list is pre-validated in three steps:

**Technical validity**: A DNS A record query is issued from the local measurement infrastructure. Domains returning `NXDOMAIN` or `SERVFAIL` — indicating unregistered or broken domains — are excluded. Domains with no A record (e.g., MX-only or NS-only domains) are excluded from A record measurements but retained in the NS record measurement set.

**Security filtering**: Domains flagged by the Google Safe Browsing API as hosting malware, phishing, or unwanted software are excluded. This filter protects both the probe hosts (whose connections generate the measurement traffic, per Kisteleki et al., 2016) and the integrity of the corpus as a baseline for legitimate Internet infrastructure.

**Authoritative server pre-resolution**: For the primary campaign (direct authoritative queries, described in Section 3.3.2), the authoritative name servers for each domain are identified by resolving the domain's NS records from a reference resolver. This pre-resolution step maps each domain to its authoritative server set and is repeated weekly in synchrony with the Tranco list update.

Based on the filtering rates reported by Le Pochat et al. (2019) for the Tranco Top 10K, approximately 500–600 domains are expected to be excluded (5–6% of 10K), yielding a final measurement corpus of approximately 9,400–9,500 active domains.

---

## 3.3 RIPE Atlas Measurement Configuration

### 3.3.1 Probe Selection

Probe selection follows the stratified-sampling protocol recommended by Bajpai et al. (2017) and adapted to the geographic diversity requirements of this thesis:

**Step 1 — System tag filtering**: All probes must satisfy the following RIPE Atlas system tags, which are automatically maintained by the platform and refreshed every four hours:

- `system-ipv4-works`: IPv4 connectivity verified by built-in platform measurements.
- `system-resolves-a-correctly`: The probe's local resolver returns correct A records (excludes lying resolvers and probes using alternative root servers).

For the primary campaign (direct authoritative queries), `system-resolves-a-correctly` is less critical than for resolver-based measurements, but is retained as a general connectivity health indicator. For the supplementary Q4 campaign (Section 3.3.5), this tag is strictly required.

Hardware version v3 or later is required. Holterbach et al. (2015) show that v1 and v2 probes (Lantronix XPort Pro, 167 MHz CPU) experience timing precision degradation of 1.1–1.2 ms in the median and 7.3–7.7 ms at the 95th percentile under concurrent measurement load, while v3 probes (TP-Link TL-MR3020, 400 MHz CPU) experience negligible degradation (0.06 ms median). Since precision is less critical for DNS content analysis (A record IP addresses) than for timing measurements (traceroute), this filter is applied as a preference rather than a hard requirement, with v1/v2 probes excluded when sufficient v3+ alternatives are available in the geographic stratum.

**Step 2 — Geographic stratification**: To compensate for RIPE Atlas's documented geographic concentration (91% of dual-stacked probes in the RIPE and ARIN regions, per Bajpai et al., 2017), probe allocation is stratified by continent with inverse-weighted over-representation of underrepresented regions:

| Region | Atlas distribution | Allocated probes | Allocation |
|---|---|---|---|
| Europe | ~40% | 30 | 30% |
| North America | ~28% | 25 | 25% |
| Asia-Pacific | ~16% | 20 | 20% |
| South America | ~8% | 10 | 10% |
| Africa | ~5% | 10 | 10% |
| Oceania | ~3% | 5 | 5% |
| **Total** | **100%** | **100** | **100%** |

Africa and South America are allocated twice their natural share in the Atlas distribution to ensure that under-represented regions contribute sufficient observations for regional analysis. This stratification is implemented by issuing separate probe selection API queries per geographic region, using RIPE Atlas's built-in region filtering.

**Step 3 — AS diversity**: Within each geographic stratum, probes are selected to maximise the number of distinct Autonomous Systems represented, following the recommendation of Bajpai et al. (2017). A minimum of one probe per distinct AS is preferred over multiple probes per AS within the same city. This ensures that the measurement dataset captures the network-level diversity of DNS resolution paths within each region, not merely its geographic diversity.

### 3.3.2 Primary Campaign: Direct Authoritative DNS Queries

The primary measurement campaign queries authoritative name servers directly, bypassing recursive resolvers. This design choice is motivated by two findings from the literature:

1. **Resolver centralization** (Xu et al., 2023): Over 90% of forwarding resolvers are backed by fewer than 5% of indirect recursive resolvers. Querying through probe resolvers would collapse the geographic diversity of probe vantage points into a small number of centralised resolution paths, making geographic DNS variation invisible.

2. **Cache state divergence** (Section 2.2.4): Probes using local resolvers have heterogeneous cache states, introducing variation that mimics geographic routing differences but is actually an artefact of cache timing. Direct authoritative queries bypass resolver caches entirely, ensuring that each measurement reflects the current authoritative response to the probe's network location.

For each domain in the corpus, measurements target the primary authoritative name server identified in the pre-resolution step (Section 3.2.3). The RIPE Atlas DNS measurement is configured as follows:

```json
{
  "type": "dns",
  "af": 4,
  "target": "<authoritative_ns_ip>",
  "query_type": "A",
  "query_class": "IN",
  "query_argument": "<domain>",
  "use_probe_resolver": false,
  "set_rd_bit": false,
  "set_nsid_bit": true,
  "set_do_bit": false,
  "set_cd_bit": false,
  "protocol": "UDP",
  "udp_payload_size": 1024,
  "include_abuf": true,
  "retry": 2,
  "timeout": 5000,
  "is_oneoff": false,
  "interval": 86400,
  "description": "Thesis DNS geo-diversity - authoritative - <domain> - <YYYY-MM-DD>"
}
```

Key parameter justifications:

**`use_probe_resolver: false` with explicit authoritative target**: Queries are sent directly to the authoritative name server. The `RD` (Recursion Desired) flag is set to false (`set_rd_bit: false`) because authoritative servers should not recurse; they return the authoritative answer for the queried domain directly.

**`set_nsid_bit: true`**: The NSID option (RFC 5001) is included in every query, following the methodology of Bortzmeyer (2013) and Finnegan (2018). The NSID string returned by the authoritative server identifies which physical anycast instance responded, providing the anycast routing dimension of geographic DNS variation alongside the IP address content dimension.

**`set_do_bit: false`**: The DNSSEC OK flag is not set in the primary campaign, to avoid DNSSEC-induced `SERVFAIL` responses from domains with broken signing chains being misinterpreted as unavailability (Section 2.9.1). A secondary measurement batch with `set_do_bit: true` is included for DNSSEC characterisation.

**`interval: 86400`** (86,400 seconds = 24 hours): Daily measurements provide the temporal resolution needed to detect day-to-day DNS changes while remaining within credit budget. The daily interval also respects the spirit of DNS TTL values: most popular domains have A record TTLs between 60 seconds and 3,600 seconds, making more frequent measurement redundant for content analysis (though not for timing analysis).

**`include_abuf: true`**: The raw DNS response packet (base64-encoded) is included in the result, enabling full parsing of all DNS sections (answer, authority, additional), extraction of TTL values, and NSID option data.

**Tags**: Each measurement is tagged with `thesis-dns-geo` (project identifier) and `tranco-<date>` (Tranco list version date), enabling reliable retrieval via the RIPE Atlas API.

### 3.3.3 Record Types Measured

In addition to A records (the primary measurement type), the following record types are measured for each domain in weekly batches:

- **AAAA records**: IPv6 addresses, to enable parallel analysis of IPv4/IPv6 anycast divergence (Bortzmeyer, 2013). These measurements are run with the same probe set and direct authoritative targeting.
- **NS records**: Identify the authoritative DNS provider for each domain. Essential for server-side centralisation analysis (Xu et al., 2023) and for tracking provider migrations over time.

MX and DNSKEY records (included in the OpenINTEL query set of van Rijswijk-Deij et al., 2016) are measured quarterly rather than daily, given their lower expected change rate and the credit cost of including them in the daily campaign.

### 3.3.4 Managing Measurement Interference and Scheduling

Holterbach et al. (2015) demonstrate two forms of interference on the RIPE Atlas platform: timing precision degradation and temporal desynchronisation between probes. Two mitigation strategies are applied:

**Timing interference mitigation**: As noted above, v3+ probe hardware is preferred (Holterbach et al., 2015). DNS content measurements (which IP address is returned) are not sensitive to sub-millisecond timing differences; only RTT analysis (used for Q4 supplementary comparison) requires high timing precision.

**Scheduling desynchronisation mitigation**: Since concurrent platform load can desynchronise measurements by up to one hour (Holterbach et al., 2015), results are validated post-collection using a timing window of ±2 hours around the scheduled measurement time. Results arriving more than 4 hours outside the scheduled window are flagged as `REJECTED` and excluded from temporal analyses that require simultaneous multi-probe observations. The exact result timestamps are used for all temporal analysis — not the scheduled time.

Measurements are scheduled at **02:00 UTC** daily, which corresponds to off-peak hours across Europe (03:00–04:00 local time) and North America (21:00–22:00 Eastern), reducing the probability of concurrent load from other high-volume RIPE Atlas campaigns.

### 3.3.5 Supplementary Campaign for Q4: Resolver Comparison

To address Q4 (impact of resolver choice), a supplementary measurement campaign is conducted in parallel with the primary campaign for a subset of 1,000 domains drawn from the primary corpus (the Tranco Top 1,000, updated weekly). This supplementary campaign uses `use_probe_resolver: true` — querying through the probe's local ISP resolver — so that the DNS response reflects the CDN routing decision made based on the resolver's IP rather than the probe's network location.

A second supplementary set uses an explicit public DNS resolver (Google Public DNS at 8.8.8.8) as the target (`use_probe_resolver: false`, target = 8.8.8.8), enabling a three-way comparison for the same domains, from the same probes, at the same time:

1. **Direct authoritative** (primary campaign): Response from authoritative server based on probe's network location.
2. **Local ISP resolver**: Response as CDN sees it for the probe's local resolver.
3. **Google Public DNS (8.8.8.8)**: Response as CDN sees it for a centralised public resolver.

This three-way comparison directly tests the predictions of the remote DNS problem (Wang et al., 2018) and the ECS hypothesis (Contavalli et al., 2016): the local ISP resolver should produce CDN assignments similar to the authoritative response (because the ISP resolver's IP is geographically close to the probe), while Google Public DNS should produce more uniform, geographically neutral assignments — unless ECS is active, in which case the Google Public DNS response should converge toward the local resolver response.

For the ECS dimension, a fourth measurement is added: the same domain queried through Google Public DNS with the ECS opt-out option (`subnet=0/0`), which instructs the resolver to suppress ECS forwarding (Bortzmeyer, n.d., tutorial; Contavalli et al., 2016). The difference between Google DNS with and without ECS measures the pure ECS contribution to geographic routing accuracy.

### 3.3.6 Credit Budget Estimation

The RIPE Atlas credit consumption is estimated as follows. For DNS measurements, the approximate cost is 10 credits per probe per measurement instance (RIPE NCC, credit documentation). For recurring daily measurements:

| Campaign | Domains | Probes | Days | Credits/day | Total |
|---|---|---|---|---|---|
| Primary (A, direct) | 9,500 | 100 | 90 | 950,000 | ~85.5M |
| Primary (AAAA, direct) | 9,500 | 100 | 90 | 950,000 | ~85.5M |
| NS records (weekly) | 9,500 | 100 | 13 weeks | 950,000/week | ~12.4M |
| Q4 supplementary (3 types) | 1,000 | 100 | 90 | 300,000 | ~27M |
| **Total** | | | | | **~210M** |

This estimate is conservative (assumes all domains are active and all probes respond). In practice, the effective credit consumption will be lower due to probe failures, measurement errors, and the exclusion of filtered domains. The credit budget is monitored weekly, with contingency adjustments: if consumption exceeds budget, the A record campaign takes priority over AAAA and NS campaigns; if under budget, the domain corpus is expanded or the measurement frequency increased.

---

## 3.4 Data Collection and Processing

### 3.4.1 Daily Collection Pipeline

Measurement results are collected from the RIPE Atlas REST API on a daily schedule, retrieving results for the previous calendar day. The collection script queries each active measurement identifier (stored in a manifest file), retrieves all results in the specified time window, and writes them to local storage as raw JSON. Error handling includes automatic retry (three attempts with exponential backoff) and an alert if more than 10% of measurements fail to return results for a given day.

```python
# Pseudocode: daily collection
def collect_daily(msm_ids, target_date):
    start = target_date.replace(hour=0, minute=0, second=0)
    stop  = target_date.replace(hour=23, minute=59, second=59)
    for msm_id in msm_ids:
        results = atlas_api.get_results(msm_id, start=start, stop=stop)
        write_raw(results, path=f"data/raw/{target_date}/{msm_id}.json")
```

### 3.4.2 Parsing and Field Extraction

Each raw RIPE Atlas DNS result is a JSON object containing measurement metadata, probe metadata, and the raw DNS response (`abuf` field, base64-encoded). The parsing pipeline extracts the following fields:

**Measurement metadata**: `msm_id`, `prb_id`, `timestamp` (Unix epoch, actual measurement time).

**Probe metadata**: `from` (probe source IP), `af` (address family, 4 or 6). The probe's country, geographic coordinates, and ASN are retrieved from the RIPE Atlas probe metadata API and joined to the result on `prb_id`.

**Resolver metadata** (for resolver-based campaigns only): `dst_addr` (resolver IP), enriched with GeoIP country and ASN via the MaxMind GeoLite2 database (or equivalent open-access database).

**DNS response**: The `abuf` field is base64-decoded and parsed using the `dnspython` library to extract:
- `rcode`: DNS response code (NOERROR=0, NXDOMAIN=3, SERVFAIL=2, etc.)
- `flags`: DNS header flags (QR, AA, RD, RA, TC, AD)
- `answer_records`: List of resource records in the Answer section, each with `rdtype`, `rdataset` (for A records: list of IP addresses), and `ttl`
- `nsid`: NSID option value from the OPT record (empty string if not returned)
- `rt`: Response time in milliseconds (from the RIPE Atlas outer JSON, not from the abuf)

### 3.4.3 Data Validation and Filtering

Four validation filters are applied in sequence:

**Filter 1 — Result completeness**: Results missing the `abuf` field (no DNS response received within the timeout) are classified as `TIMEOUT` and excluded from content analysis. They are retained as observations of DNS non-responsiveness for reliability analysis.

**Filter 2 — Timing validation**: Results whose actual timestamp deviates from the scheduled measurement time by more than four hours are classified as `SCHED_REJECTED`. Timestamps deviating by two to four hours receive a `SCHED_WARNING` flag and are retained but annotated (Holterbach et al., 2015).

**Filter 3 — DNS response code**: Results with `rcode != NOERROR` are classified by their specific error code (`NXDOMAIN`, `SERVFAIL`, `REFUSED`, etc.). For Q1 and Q2, only `NOERROR` results with at least one answer record are used. `SERVFAIL` results are separately analysed for DNSSEC correlation (Section 3.5). In the context of Q3 and geographic filtering (Section 2.9.3), `NXDOMAIN`/`REFUSED` results from specific countries may represent intentional censorship rather than measurement failure and are handled explicitly.

**Filter 4 — Anomalous response detection**: For direct authoritative measurements, results that return IP addresses inconsistent with the queried domain's known address space are flagged for manual inspection. This filter catches cases where an in-path proxy or network appliance intercepts the query and substitutes a synthetic response — analogous to the proxy detection methodology of Jones et al. (2016) applied to authoritative queries rather than root server queries. Consistency across multiple probes in the same region is used as a cross-validation signal: if 90%+ of probes in the same geographic region return the same set of IP addresses but one probe returns a disjoint set, the outlier is flagged as a potential proxy.

Expected filter rates based on comparable measurement studies:

| Filter | Expected exclusion rate |
|---|---|
| Timeout (no result) | 1–3% |
| Timing deviation >4h | ~1% |
| RCODE ≠ NOERROR | 2–5% |
| Anomalous response flag | <1% |
| **Usable results** | **~90–95%** |

### 3.4.4 Metadata Enrichment

Probe metadata (geographic coordinates, country, ASN) is enriched from two sources: the RIPE Atlas probe metadata API (primary source, updated daily) and the MaxMind GeoLite2 City database (secondary cross-validation). Jones et al. (2016) note that 1.7% of RIPE Atlas probes have inconsistent geolocation between Atlas metadata and MaxMind, motivating this cross-validation step. Probes with conflicting country assignments between the two sources are flagged and their results excluded from country-level geographic analysis (but retained for AS-level analysis using the RIPE Atlas-provided ASN, which is more reliable than IP geolocation for ASN mapping).

Authoritative server NSID strings are mapped to physical PoP locations using the naming conventions described by Bortzmeyer (2013) and Finnegan (2018): IATA airport codes (e.g., `ams` → Amsterdam Schiphol, `fra` → Frankfurt) and city abbreviations (e.g., `par` → Paris, `sin` → Singapore). A lookup table of known NSID strings is maintained and updated as new instances are encountered.

### 3.4.5 Storage Architecture

Results are stored in a two-tier architecture following the design of OpenINTEL (van Rijswijk-Deij et al., 2016):

**Tier 1 — Long-term archival (Apache Avro)**: Parsed results are serialised in Apache Avro format using a fixed schema that includes all extracted fields plus validation flags. Avro's binary encoding with snappy compression achieves a compression ratio of approximately 7:1 compared to raw JSON (van Rijswijk-Deij et al., 2016), reducing daily storage from approximately 2 GB (raw JSON) to approximately 280 MB. Avro's self-describing schema ensures that files remain interpretable without external schema documentation.

The Avro schema captures the following fields per record:

| Field | Type | Description |
|---|---|---|
| `msm_id` | long | RIPE Atlas measurement ID |
| `prb_id` | long | RIPE Atlas probe ID |
| `timestamp` | long | Actual measurement time (Unix epoch) |
| `domain` | string | Queried domain name |
| `query_type` | string | A, AAAA, or NS |
| `campaign_type` | string | `auth_direct`, `isp_resolver`, `public_dns`, `public_dns_noecs` |
| `probe_country` | string | ISO 3166-1 alpha-2 country code (Atlas metadata) |
| `probe_asn` | long | Autonomous System Number (Atlas metadata) |
| `probe_lat` | double | Probe latitude |
| `probe_lon` | double | Probe longitude |
| `resolver_ip` | string | Resolver IP (null for `auth_direct` campaign) |
| `target_ip` | string | Target IP (authoritative server or resolver) |
| `rcode` | int | DNS response code |
| `answer_ips` | array[string] | A/AAAA records returned |
| `answer_ttl` | long | TTL of answer records |
| `nsid` | string | NSID option value (empty if not present) |
| `rt_ms` | double | Response time in milliseconds |
| `valid` | boolean | Passes all validation filters |
| `validation_flag` | string | VALID / TIMEOUT / SCHED_REJECTED / RCODE_ERROR / ANOMALOUS |

**Tier 2 — Analytics (Apache Parquet)**: Validated Avro records are converted daily to Apache Parquet format, partitioned by year/month/day using Hive-style directory naming (`year=2026/month=03/day=21/`). Parquet's columnar storage format enables efficient execution of the analytical queries used in the analysis phase (filtering by domain, aggregating over time periods, grouping by probe geography) without reading all fields for all records. The storage overhead of Parquet relative to Avro is minimal (~30% reduction in file size for the DNS result schema, which has many repeated string values amenable to dictionary encoding).

**Storage estimate**: For the primary campaign (10K domains × 100 probes × 90 days × 2 address families), the total storage requirement is approximately:
- Raw JSON: ~180 GB
- Avro: ~24 GB
- Parquet: ~18 GB
- **Total: ~220 GB** (of which Avro and Parquet represent the long-term archive at ~42 GB)

---

## 3.5 Analysis Methods

### 3.5.1 Q1 — Geographic Diversity of DNS Responses

**Objective**: For each domain in the corpus, determine whether the set of IP addresses returned varies systematically by the geographic location of the querying probe, and characterise the pattern of variation.

**Step 1 — Compute per-domain IP diversity**: For each domain and each measurement day, the set of unique IP addresses returned across all probes is computed. The **number of distinct IP addresses** observed provides a first-order diversity index: a domain returning a single IP address from all probes globally exhibits no geographic variation; a domain returning 50 distinct IPs exhibits substantial variation.

**Step 2 — Compute inter-region diversity**: For each domain, the probe set is partitioned by geographic region (using the continent-level grouping from Section 3.3.1). For each pair of regions, the Jaccard similarity between their respective IP address sets is computed:

$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$

A Jaccard similarity of 1.0 indicates identical IP sets across regions (no geographic differentiation); a Jaccard similarity of 0 indicates fully disjoint IP sets (complete geographic differentiation). The **median pairwise Jaccard similarity across all region pairs** serves as the primary geographic diversity metric per domain per day.

**Step 3 — Classification**: Domains are classified into four geographic diversity categories:

| Category | Criterion | Interpretation |
|---|---|---|
| `UNIFORM` | Single IP across all probes | No geographic routing |
| `LOW_DIVERSITY` | Median pairwise Jaccard > 0.8 | Minimal variation (round-robin or load balancing) |
| `MEDIUM_DIVERSITY` | Median pairwise Jaccard 0.4–0.8 | Moderate geographic routing |
| `HIGH_DIVERSITY` | Median pairwise Jaccard < 0.4 | Strong geographic routing |

**Step 4 — Mechanism attribution**: For domains in the `HIGH_DIVERSITY` category, the NSID strings returned by the authoritative server across probes are analysed to determine whether geographic IP variation is driven by anycast instance selection (different NSID per region → different anycast PoP routing) or by DNS-based CDN routing (same NSID but different IP addresses → CDN geographic database lookup). The two mechanisms are distinguishable because anycast instance variation is visible in the NSID field, while CDN routing variation is visible in the A record content with a constant NSID.

**Key metrics**:
- Distribution of domains across the four diversity categories
- Proportion of `HIGH_DIVERSITY` domains attributable to anycast versus DNS-based CDN routing
- Geographic diversity as a function of Tranco rank (do top-100 domains show more or less diversity than top-5K?)

### 3.5.2 Q2 — Temporal Stability

**Objective**: Quantify the temporal stability of DNS responses for each domain, characterising the rate and timescale of IP address change.

**Step 1 — Compute per-probe temporal stability**: For each domain and each probe, the time series of A record IP address sets is extracted over the measurement period. Consecutive daily observations are compared using Jaccard similarity; the **mean Jaccard similarity across consecutive days** is the probe-level daily stability index. A stability index of 1.0 indicates no change; 0.5 indicates that half the IP addresses change each day.

**Step 2 — Aggregate across probes**: The domain-level stability index is the median of probe-level stability indices across all probes. This aggregation uses the median (rather than mean) to reduce the influence of individual probe failures that produce artificially low stability scores.

**Step 3 — Multi-scale analysis**: The stability analysis is repeated at weekly and monthly timescales, comparing the IP address set observed in one week (the union of all A records seen in that week across all probes) with the set observed in the following week. This captures the difference between high-frequency CDN routing fluctuations (visible at daily timescale) and genuine infrastructure changes such as server migrations (visible at weekly or monthly timescale).

**Step 4 — TTL correlation**: The TTL values of A records are extracted for each domain. A Spearman rank correlation is computed between each domain's median A record TTL and its daily stability index. The hypothesis (motivated by CDN operators' use of short TTLs to enable rapid traffic redirection) is that domains with shorter TTLs exhibit lower daily stability — more frequent IP address changes.

**Key metrics**:
- Distribution of daily stability indices across the domain corpus
- Proportion of domains that are `VERY_STABLE` (<5% change rate), `STABLE` (5–20%), `MODERATE` (20–50%), or `VOLATILE` (>50%)
- Spearman correlation between median TTL and daily stability (with 95% confidence interval)
- Top-20 most volatile domains (case studies)

### 3.5.3 Q3 — Assessment of RIPE Atlas Geographic Bias

**Objective**: Evaluate whether the geographic concentration of RIPE Atlas probes in Europe and North America significantly limits the ability to observe geographic DNS variation.

**Method**: The geographic bias assessment uses a **controlled subsampling experiment**. Three virtual probe sets are constructed from the full measurement dataset:

1. **ACTUAL**: The full probe set as deployed (with natural RIPE Atlas geographic distribution).
2. **EUROPE_NA_ONLY**: Only probes in Europe and North America (simulating a measurement campaign without geographic stratification — the scenario that would arise if a researcher used the RIPE Atlas default worldwide selection without stratification).
3. **UNIFORM**: A resampled probe set with equal numbers of probes per continent (simulating perfect geographic balance).

For each virtual probe set, the domain-level geographic diversity metric (Section 3.5.1) is recomputed. The distribution of diversity categories under ACTUAL, EUROPE_NA_ONLY, and UNIFORM are compared using the Wilcoxon signed-rank test (a non-parametric paired test appropriate for distributions that may not be normal). A statistically significant difference between ACTUAL and EUROPE_NA_ONLY indicates that the geographic stratification strategy meaningfully improves diversity observation; a significant difference between ACTUAL and UNIFORM identifies domains whose diversity classification changes when underrepresented regions are included.

Additionally, the **unique IP contribution** of each region is computed: for each domain, the fraction of observed IP addresses that are seen only from probes in a specific region (and not from any other region's probes) quantifies how much unique information that region provides. A high unique contribution from underrepresented regions (Africa, South America, Southeast Asia) would indicate that the geographic bias materially limits the completeness of the diversity picture.

**Key metrics**:
- Wilcoxon test p-value for ACTUAL vs EUROPE_NA_ONLY (significance of stratification)
- Fraction of domains whose diversity category changes between EUROPE_NA_ONLY and ACTUAL
- Per-region unique IP contribution (% of observed IPs seen only from that region)

### 3.5.4 Q4 — Impact of Resolver Choice

**Objective**: Quantify the impact of resolver type on CDN-assigned IP addresses, and empirically test the ECS hypothesis.

This analysis uses the supplementary Q4 measurement campaign (Section 3.3.5), which provides four simultaneous observations for the Top 1,000 Tranco domains from the same set of probes:

1. `auth_direct`: Direct authoritative query (probe network location determines response)
2. `isp_resolver`: Local ISP resolver (resolver IP determines CDN assignment)
3. `public_dns`: Google Public DNS (8.8.8.8) without explicit ECS opt-out
4. `public_dns_noecs`: Google Public DNS with ECS opt-out (`+subnet=0/0`)

**Step 1 — Pairwise IP set comparison**: For each domain and each probe, the four IP address sets are compared using Jaccard similarity. The critical comparisons are:
- `isp_resolver` vs `auth_direct`: Measures whether the ISP resolver correctly reflects the probe's geographic location (expected: high Jaccard similarity if resolver is geographically close to the probe)
- `public_dns` vs `auth_direct`: Measures the remote DNS problem (expected: lower Jaccard similarity, especially for probes in regions where Google's resolver clusters are distant)
- `public_dns` vs `public_dns_noecs`: Measures the ECS contribution (expected: lower Jaccard when ECS is active, as ECS-based routing should better match the probe location)
- `isp_resolver` vs `public_dns_noecs`: Measures pure resolver-location effect without ECS

**Step 2 — Geographic disaggregation**: The pairwise Jaccard similarities are disaggregated by continent. The remote DNS problem prediction (Wang et al., 2018) is that Google DNS performance relative to ISP DNS should be worst in regions where Google's resolver clusters are geographically concentrated, and best in regions where Google has dense resolver infrastructure.

**Step 3 — Statistical validation**: For each comparison pair, the distribution of per-domain Jaccard similarities across all probes is compared using the Mann-Whitney U test (non-parametric, for independent samples). A Bonferroni correction is applied for the six pairwise comparisons.

**Key metrics**:
- Mean and median pairwise Jaccard similarity for each comparison (global and per continent)
- Proportion of domains where `public_dns` diverges significantly from `isp_resolver` (Jaccard < 0.5)
- ECS contribution: fraction of the divergence between `public_dns` and `isp_resolver` that is reduced when ECS is enabled

---

## 3.6 Ethical Considerations and Reproducibility

### 3.6.1 Ethical Design

The measurement design follows the ethical framework of Kisteleki et al. (2016) and the principles of the Menlo Report (2012):

**Probe host protection**: All query targets are publicly accessible domains from the Tranco Top 10K corpus. No politically sensitive, censored, or jurisdictionally restricted domains are included. Direct authoritative queries for A records are indistinguishable from normal client DNS traffic; they do not create legal or social risk for probe hosts in any jurisdiction.

**Infrastructure impact**: The measurement frequency (once per domain per day) is orders of magnitude below the threshold that would constitute an undue burden on authoritative DNS servers, as established by van Rijswijk-Deij et al. (2016), who show that OpenINTEL's 1.85 billion queries per day represent only 0.3–1.6% of total authoritative server traffic. This thesis's campaign generates approximately one million queries per day — roughly 1,000× fewer.

**Transparency**: All measurements are tagged with `thesis-dns-geo` in RIPE Atlas, allowing authoritative server operators to identify and contact the measurement operator if needed. The measurement description includes a reference to the thesis and its public documentation.

**Data minimisation**: Raw results include probe IP addresses, which are not published. The public dataset uses only aggregated per-country and per-ASN statistics. Individual probe results are retained internally for the duration of the analysis and then anonymised.

### 3.6.2 Scientific Reproducibility

**Fixed domain corpus**: The Tranco list identifier (e.g., `8QNZ`) used for each measurement week is recorded in the dataset metadata, enabling exact reproduction of the domain corpus.

**Measurement traceability**: All RIPE Atlas measurement IDs are recorded in the dataset manifest. Any researcher with a RIPE Atlas account can retrieve the original raw results using these IDs, providing primary source access to the underlying data.

**Software versioning**: The analysis pipeline is published on GitHub with a fixed release tag corresponding to each submitted thesis version. The requirements file specifies exact package versions (Python 3.11, dnspython 2.4.x, pandas 2.1.x, pyarrow 14.x, scipy 1.11.x) to eliminate software version ambiguity.

**Dataset publication**: The final dataset (Avro + Parquet format, with full metadata) is published on Zenodo with a permanent DOI before the oral thesis defence, following the FAIR principles (Findable, Accessible, Interoperable, Reusable) advocated by van Rijswijk-Deij et al. (2016).

**Pilot validation**: Before the three-month production campaign, a seven-day pilot campaign is conducted on a 500-domain subset with 10 probes to validate the measurement configuration, estimate actual credit consumption, and verify the data pipeline end-to-end. The pilot results are included in the public dataset as a separate partition, providing a compact reproducible example of the full methodology.

---
