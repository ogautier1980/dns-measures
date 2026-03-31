# Chapter 3 - Methodology

> **Note on sourcing.** This chapter describes the technical methodology of the measurement campaign as actually implemented and deployed. Sources from the bibliography are cited where the methodology is directly informed by or adapted from prior work. General software engineering choices (API usage, data format parameters, statistical tests) are not attributed to sources.

---

## 3.1 Overview

### 3.1.1 Methodological Objective

The overarching methodological objective of this thesis is to capture the **geographic and temporal diversity of DNS responses** for a representative corpus of popular domains, using geographically distributed active measurements, in a manner that is reproducible, ethically sound, and practically feasible within the available resource budget. The system must answer four empirical research questions:

- **Q1**: What proportion of Tranco top-ranked domains return geographically differentiated DNS responses, and what infrastructure mechanisms explain the differentiation?
- **Q2**: What is the temporal stability of DNS responses for popular domains at day, week, and month timescales?
- **Q3**: Do the geographic biases of the RIPE Atlas probe distribution significantly limit the ability to observe geographic DNS variation?
- **Q4**: What is the measurable impact of resolver type --- local ISP resolver versus public DNS service --- on the DNS responses observed?

### 3.1.2 System Architecture

The measurement system is organised in five sequential stages, inspired by the architecture of OpenINTEL (van Rijswijk-Deij et al., 2016) but adapted to the constraints and capabilities of the RIPE Atlas platform:

1. **Domain corpus preparation**: Retrieval and filtering of the Tranco Top 10,000 domain list.
2. **Measurement scheduling**: Configuration and deployment of RIPE Atlas DNS measurement campaigns.
3. **Data collection**: Automated daily retrieval of measurement results via the RIPE Atlas REST API.
4. **Storage and preprocessing**: Parsing, validation, and archival in Parquet format.
5. **Analysis**: Quantitative analysis addressing Q1--Q4.

The key design trade-off throughout is the three-way tension between **domain coverage** (how many domains are measured), **geographic coverage** (how many geographically distributed probes), and **temporal resolution** (measurement frequency), all bounded by the finite RIPE Atlas credit budget. The system is fully configurable via `--max-domains` and `--total-probes` parameters; the default operating point is **500 domains × 50 probes**, generating approximately 250,000 credits per day. Figure 3.1 presents the five-stage pipeline architecture.

### 3.1.3 Infrastructure

The entire pipeline runs as a **Docker container** on a Raspberry Pi 5 (ARM64 architecture), operating continuously and autonomously. This choice reflects the need for a low-cost, always-on measurement platform that can sustain a three-month measurement campaign without manual intervention.

The container image is based on `python:3.11-slim-bookworm` and is compiled natively for the ARM64 architecture, ensuring full compatibility with the Raspberry Pi 5 hardware. The image contains only the dependencies required for the pipeline (dnspython, pandas, pyarrow, scipy, matplotlib, rclone), keeping its footprint under 1 GB.

Data persistence is managed through Docker named volumes, which survive container restarts and image updates. Collected results are automatically synchronised daily to cloud storage via **rclone**, which is configured to target two destinations simultaneously: Microsoft OneDrive (UNamur institutional account) and Google Drive (personal account, 2 TB available). This dual-destination strategy ensures redundancy: if one service is temporarily unavailable, the other retains a complete copy of all results.

The pipeline is orchestrated by a cron daemon running inside the container, with the following schedule (all times UTC):

| Time (UTC) | Day | Action |
|---|---|---|
| 05:00 | Monday | Weekly Tranco list refresh |
| 06:00 | Daily | Fetch RIPE Atlas results + Parquet parsing |
| 07:00 | Daily | Cloud sync (Parquet + raw JSON → OneDrive + Google Drive) |
| 08:00 | Sunday | Q1--Q4 analysis + figure generation |
| 09:00 | Sunday | Cloud sync (reports + figures → OneDrive + Google Drive) |
| 04:00 | 1st of month | Log rotation |

The pipeline source code is available at https://github.com/ogautier-unam/dns-pipeline and implements the six Python scripts described in the following sections.

---

## 3.2 Domain Corpus Selection

### 3.2.1 Tranco List Configuration

The domain corpus is the **Tranco Top 10,000** list, retrieved via the Tranco API at `https://tranco-list.eu`. The choice of Tranco over commercial ranking lists (Alexa, Cisco Umbrella, Majestic) is motivated in Chapter 2 (Section 2.7) and rests on three properties established by Le Pochat et al. (2019): stability (0.6% daily change versus approximately 50% for post-2018 Alexa), manipulation resistance (quadrupled manipulation effort relative to single-source lists), and archivability (each generated list is assigned a unique identifier retrievable indefinitely via permalink).

The `fetch_tranco.py` script retrieves the most recent available list, falling back up to seven days if the current day's list has not yet been published. The exact Tranco list identifier and generation date are recorded in `tranco_meta.json` alongside the corpus, ensuring full reproducibility.

The list is **updated weekly** (each Monday at 05:00 UTC) to capture the slow evolution of the popular-domain corpus while limiting the rate of change introduced by list updates. Each weekly update computes the delta of added and removed domains relative to the previous week's list. Domains that exit the Top 10K during the measurement campaign are retained in active measurement for two additional weeks to capture any transitional DNS behaviour.

### 3.2.2 Domain Corpus Size

The measurement corpus targets the **top 500 domains** from the Tranco Top 10,000 list. Although Tranco provides a 10K list, the RIPE Atlas credit system imposes a hard practical constraint: at 10 credits per probe per measurement instance, running 10,000 domains daily with 50 probes would consume 5,000,000 credits per day, draining a typical research allocation within days. The selection of 500 domains represents a deliberate balance between three competing requirements:

**Representativeness**: The Tranco Top 500 concentrates the domains responsible for the large majority of global web traffic --- precisely the CDN-backed services (streaming platforms, search engines, social networks, cloud providers) that exhibit the richest geographic DNS variation. Studies by Calder et al. (2015) and Wang et al. (2018) confirm that CDN routing diversity is most pronounced in this top-ranked tier.

**Feasibility**: At 50 probes per measurement, one A record query per domain per day, the Top 500 corpus generates approximately 25,000 measurement results per day and consumes 250,000 RIPE Atlas credits. This is sustainable over a 90-day measurement period.

**Configurability**: The pipeline exposes `--max-domains` and `--total-probes` parameters. If the available credit balance allows, the corpus can be extended to 1,000 or 2,000 domains without any other modification.

### 3.2.3 Domain Filtering and Validation

Before the measurement campaign begins, each domain in the Tranco Top 10K list is pre-validated by `fetch_tranco.py` in two steps:

**Technical validity**: A DNS A record query is issued against Google Public DNS (8.8.8.8) and Cloudflare DNS (1.1.1.1) as reference resolvers. Domains returning `NXDOMAIN` or `SERVFAIL` are excluded. Based on the filtering rates reported by Le Pochat et al. (2019) for the Tranco Top 10K, approximately 500--600 domains are expected to be excluded (5--6% of 10K), yielding a final measurement corpus of approximately 9,400--9,500 active domains.

**Authoritative server pre-resolution**: The authoritative name servers for each domain are identified by resolving the domain's NS records from the same reference resolvers. This pre-resolution step maps each domain to its authoritative server set and is repeated weekly in synchrony with the Tranco list update. The resulting corpus is saved as `tranco_corpus.csv` with fields `rank`, `domain`, and `ns` (pipe-separated list of authoritative nameserver hostnames).

---

## 3.3 RIPE Atlas Measurement Configuration

### 3.3.1 Probe Selection

Probe selection is implemented in `create_ripe_measurements.py` and follows the stratified-sampling protocol recommended by Bajpai et al. (2017), adapted to the geographic diversity requirements of this thesis. The selection proceeds in three steps.

**Step 1 --- System tag filtering**: All probes must satisfy the following RIPE Atlas system tags:

- `system-ipv4-works`: IPv4 connectivity verified by built-in platform measurements.
- `system-resolves-a-correctly`: The probe's local resolver returns correct A records.

Hardware version v3 or later is required. Holterbach et al. (2015) show that v1 and v2 probes experience timing precision degradation under concurrent measurement load, while v3 probes experience negligible degradation.

**Step 2 --- Geographic stratification**: To compensate for RIPE Atlas's documented geographic concentration (91% of dual-stacked probes in the RIPE and ARIN regions, per Bajpai et al., 2017), probe allocation is stratified by continent with inverse-weighted over-representation of underrepresented regions:

| Region | Atlas distribution | Allocated probes | This study |
|---|---|---|---|
| Europe | ~40% | 15 | 30% |
| North America | ~28% | 12 | 25% |
| Asia-Pacific | ~16% | 10 | 20% |
| South America | ~8% | 6 | 10% |
| Africa | ~5% | 5 | 10% |
| Oceania | ~3% | 2 | 5% |
| **Total** | **100%** | **50** | **100%** |

The proportional allocation preserves the relative weighting from prior work (Bajpai et al., 2017) while scaling the total to 50 probes for budget compatibility. The probe count is configurable via `--total-probes`; the proportions are applied dynamically.

**Step 3 --- AS diversity**: Within each geographic stratum, probes are selected using a round-robin algorithm over distinct Autonomous Systems, preferring one probe per AS over multiple probes within the same AS. The selected probe set is saved as `selected_probes_<date>.json` for full reproducibility.

### 3.3.2 Primary Campaign: Direct Authoritative DNS Queries

The primary measurement campaign queries authoritative name servers directly, bypassing recursive resolvers. This design choice is motivated by two findings from the literature:

1. **Resolver centralization** (Xu et al., 2023): Over 90% of forwarding resolvers are backed by fewer than 5% of indirect recursive resolvers. Querying through probe resolvers would collapse the geographic diversity of probe vantage points into a small number of centralised resolution paths, making geographic DNS variation invisible.

2. **Cache state divergence**: Probes using local resolvers have heterogeneous cache states, introducing variation that mimics geographic routing differences but is actually an artefact of cache timing. Direct authoritative queries bypass resolver caches entirely.

For each domain in the corpus, the primary authoritative name server identified during pre-resolution is used as the measurement target. The RIPE Atlas DNS measurement is configured as follows:

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
  "description": "DNS geo-diversity - auth - <domain> - <YYYY-MM-DD>"
}
```

Key parameter justifications:

**`set_nsid_bit: true`**: The NSID option (RFC 5001) is included in every query, following the methodology of Bortzmeyer (2013) and Finnegan (2018). The NSID string returned by the authoritative server identifies which physical anycast instance responded, providing the anycast routing dimension of geographic DNS variation.

**`include_abuf: true`**: The raw DNS response packet (base64-encoded) is included in the result, enabling full parsing of all DNS sections, extraction of TTL values, and NSID option decoding. The `parse_dns_results.py` script decodes the ABUF binary structure directly to extract OPT record NSID data (RFC 5001, option code 3).

**`interval: 86400`** (86,400 seconds = 24 hours): Daily measurements provide the temporal resolution needed to detect day-to-day DNS changes while remaining within the credit budget.

### 3.3.3 Supplementary Campaign for Q4: Resolver Comparison

To address Q4, a supplementary one-off measurement campaign is conducted on a subset of **100 domains** drawn from the top of the primary corpus. This campaign provides four simultaneous resolver-type observations from the same 50 probes:

| Campaign | Target | `use_probe_resolver` | Resolver |
|---|---|---|---|
| `isp_local` | --- | `true` | Probe's local ISP resolver |
| `google` | 8.8.8.8 | `false` | Google Public DNS |
| `cloudflare` | 1.1.1.1 | `false` | Cloudflare DNS |
| `quad9` | 9.9.9.9 | `false` | Quad9 |

The Q4 campaign uses `set_rd_bit: true` (recursion desired) and a larger UDP payload size (4096 bytes) appropriate for recursive resolver queries. Measurements are configured as one-off (`is_oneoff: true`) to avoid continuous credit consumption.

This four-way comparison allows direct testing of whether the choice of resolver affects the CDN-assigned IP addresses observed from each geographic vantage point, and whether the local ISP resolver produces results closer to the authoritative response than centralised public DNS services.

### 3.3.4 Credit Budget

The RIPE Atlas credit consumption is estimated as follows (10 credits per probe per measurement instance):

| Campaign | Domains | Probes | Frequency | Credits |
|---|---|---|---|---|
| Primary A record (direct auth) | 500 | 50 | daily | 250,000 / day |
| Q4 resolver comparison (one-off) | 100 | 50 | once | 200,000 total |
| 90-day primary campaign total | — | — | — | ~22,500,000 |

For context, RIPE Atlas free research allocations are typically in the order of 1,000,000--10,000,000 credits; a RIPE NCC research credit grant (available to academic researchers) can cover the full 90-day budget. The pipeline parameters `--max-domains` and `--total-probes` allow scaling to match the available balance: for example, `--max-domains 100 --total-probes 20` reduces daily consumption to 20,000 credits while retaining full pipeline functionality.

The credit budget is monitored by the log output of `create_ripe_measurements.py`, which prints the estimated consumption at each invocation before any measurements are created.

---

## 3.4 Data Collection and Processing

### 3.4.1 Daily Collection Pipeline

Measurement results are collected from the RIPE Atlas REST API by `fetch_ripe_atlas.py` on a daily schedule at 06:00 UTC, retrieving results for the previous calendar day. The script reads the measurement plan from `measurements.json` (produced by `create_ripe_measurements.py`) and iterates over all active measurement identifiers.

The collection is fully paginated, following RIPE Atlas API `next` links until all results for the time window are retrieved. Error handling includes automatic retry with exponential backoff (up to 5 attempts, base delay 2 seconds, doubling on each retry) and explicit handling of HTTP 429 rate-limit responses (waits for the `Retry-After` header duration before retrying). Failed measurement IDs are recorded in `fetch_errors_<date>.json` for post-hoc investigation. To avoid redundant downloads, already-fetched files are skipped unless the `--force` flag is specified.

Raw results are saved as JSON files in `data/raw/msm_<id>_<date>.json`.

### 3.4.2 Parsing and Field Extraction

Each raw RIPE Atlas DNS result is parsed by `parse_dns_results.py`, which extracts the following fields into a structured Parquet record:

| Field | Type | Description |
|---|---|---|
| `msm_id` | int64 | RIPE Atlas measurement ID |
| `prb_id` | int32 | RIPE Atlas probe ID |
| `timestamp` | int64 | Actual measurement time (Unix epoch) |
| `date` | string | ISO date (YYYY-MM-DD) |
| `country_code` | string | ISO 3166-1 alpha-2 country code |
| `asn_v4` | int32 | Probe Autonomous System Number |
| `continent` | string | Continent code (EU/NA/SA/AF/AP/OC) |
| `query_domain` | string | Queried domain name |
| `rcode` | int16 | DNS response code (0 = NOERROR) |
| `answer_count` | int16 | Number of A/AAAA records returned |
| `answer_ips` | string | Pipe-separated list of returned IP addresses |
| `ttl_min` | int32 | Minimum TTL across answer records |
| `rt_ms` | float32 | Response time in milliseconds |
| `nsid_str` | string | NSID value (ASCII, if returned) |
| `nsid_hex` | string | NSID value (hex encoding) |
| `abuf_size` | int32 | DNS response packet size in bytes |
| `resolver_ip` | string | Target resolver IP (Q4 campaign only) |
| `use_probe_resolver` | bool | True for ISP local resolver campaign |

The NSID value is extracted by decoding the raw ABUF binary field: the script walks the DNS packet structure to locate the OPT record (type 41) in the Additional section, then parses EDNS0 options to extract option code 3 (NSID, RFC 5001).

### 3.4.3 Data Validation

The following validation filters are applied during parsing:

**RCODE filtering**: Only results with `rcode = 0` (NOERROR) and `answer_count > 0` are used for Q1 and Q2 content analysis. Results with `rcode != 0` are retained in the Parquet dataset with their specific error codes for reliability and censorship analysis.

**Deduplication**: The cumulative Parquet file (`dns_results.parquet`) is deduplicated on `(msm_id, prb_id, timestamp)` on each daily append to prevent double-counting in case of re-fetch.

### 3.4.4 Storage Architecture

Results are stored in a single-tier Parquet architecture optimised for the analytical query patterns of the analysis phase:

**Cumulative Parquet file** (`data/processed/dns_results.parquet`): All parsed results are appended daily to a single Parquet file using pyarrow with a fixed schema. This file grows at approximately 3--5 MB/month for the primary campaign (500 domains × 50 probes × 30 days, after columnar compression with dictionary encoding for repeated string values such as `country_code`, `continent`, and `answer_ips`).

**Daily archives** (`data/processed/dns_results_<date>.parquet`): Individual daily Parquet files are also retained for point-in-time analysis and as a recovery mechanism in case of cumulative file corruption.

**Raw JSON files** (`data/raw/msm_<id>_<date>.json`): Raw RIPE Atlas JSON results are retained locally for 7 days, then deleted after cloud synchronisation. This rolling window allows re-parsing with updated schema if needed, while controlling local storage consumption on the Raspberry Pi.

**Cloud backup**: All Parquet files, daily archives, and reports are synchronised daily to two cloud destinations via rclone: Microsoft OneDrive (UNamur institutional account) and Google Drive (personal account). The `sync_cloud.sh` script detects which remotes are configured and synchronises to all available destinations in parallel. The rclone configuration is persisted in a Docker named volume, surviving container updates.

**Storage estimate** for a three-month campaign (500 domains × 50 probes):

| Tier | Volume | Location |
|---|---|---|
| Raw JSON (7-day rolling) | ~350 MB | Pi local |
| Cumulative Parquet | ~15 MB | Pi + OneDrive + Google Drive |
| Daily Parquet archives | ~45 MB | Pi + OneDrive + Google Drive |
| Reports and figures | ~50 MB | Pi + OneDrive + Google Drive |

---

## 3.5 Analysis Methods

### 3.5.1 Q1 --- Geographic Diversity of DNS Responses

**Objective**: For each domain in the corpus, determine whether the set of IP addresses returned varies systematically by the geographic location of the querying probe.

**Step 1 --- Compute per-domain IP diversity**: For each domain and each measurement day, the probe set is partitioned by continent. For each continent, the set of unique IP addresses returned is computed from all probes in that continent. A domain is classified as **geographically diverse** if at least two continents receive distinct IP address sets on the same day.

**Step 2 --- Aggregate over time**: A domain is classified as exhibiting geographic diversity if it returns geographically differentiated responses on at least one measurement day. The `pct_geo_diverse` metric gives the percentage of days on which geographic differentiation is observed, characterising the consistency of differentiation over time.

**Step 3 --- NSID analysis**: For domains with geographic IP variation, the presence of NSID values is used to distinguish between anycast instance selection (different NSID per region, indicating different anycast PoP) and DNS-based CDN routing (uniform NSID with varying A records, indicating CDN geographic database lookup).

**Key metrics**:
- Total proportion of domains exhibiting geographic diversity
- Distribution of the number of distinct IP address sets across continents
- Top domains by geographic diversity score
- Proportion of geographically diverse domains returning NSID values

### 3.5.2 Q2 --- Temporal Stability

**Objective**: Quantify the rate of change of DNS responses for each domain over time.

**Step 1 --- Per-probe change detection**: For each (domain, probe) pair, consecutive daily observations are compared. A change event is recorded when the `answer_ips` value differs between two consecutive measurement days.

**Step 2 --- Change rate computation**: The per-domain change rate is the proportion of consecutive-day pairs for which at least one probe observes a change. This is computed at three temporal windows: daily (consecutive days), weekly (observations 7 days apart), and monthly (observations 30 days apart).

**Step 3 --- Distribution analysis**: The distribution of per-domain change rates is computed across the full corpus, identifying the proportions of fully stable, occasionally changing, and highly volatile domains.

**Key metrics**:
- Distribution of per-domain daily change rates
- Proportion of fully stable domains (0% change rate)
- Median change rate across the corpus
- Stability breakdown by temporal window (day/week/month)

### 3.5.3 Q3 --- Assessment of RIPE Atlas Geographic Bias

**Objective**: Evaluate whether the geographic concentration of RIPE Atlas probes in Europe and North America significantly limits the ability to observe geographic DNS variation.

**Method**: The probe distribution actually achieved at deployment is compared to the target allocation from Section 3.3.1. For each continent, the coverage rate (proportion of domains observed by at least one probe) and the mean number of unique IP addresses observed per domain are computed.

A **Mann-Whitney U test** (non-parametric, for independent samples) compares the distribution of unique IPs observed per domain between Europe+North America probes and probes from all other regions. A statistically significant difference (p < 0.05) indicates that the geographic stratification captures meaningfully different DNS responses from underrepresented regions.

**Key metrics**:
- Actual probe distribution by continent at deployment
- Per-continent domain coverage rate
- Mean unique IPs per domain per continent
- Mann-Whitney U statistic and p-value (EU+NA vs. other regions)

### 3.5.4 Q4 --- Impact of Resolver Choice

**Objective**: Quantify the impact of resolver type on DNS responses, comparing local ISP resolvers with three major public DNS services.

This analysis uses the supplementary Q4 measurement campaign (Section 3.3.3), which provides four simultaneous observations for 100 domains from the same 50 probes.

**Step 1 --- Per-resolver statistics**: For each resolver type (`isp_local`, `google`, `cloudflare`, `quad9`), the following metrics are computed: error rate (proportion of RCODE != 0 responses), median RTT, and mean answer count.

**Step 2 --- Divergence analysis**: For each domain and each probe, the `answer_ips` returned by the local ISP resolver is compared against each public DNS service. A divergence event is recorded when the IP sets differ. The per-comparison divergence rate is the proportion of (domain, probe) pairs showing divergence.

**Step 3 --- Statistical validation**: For each pairwise comparison (ISP local vs. each public resolver), the Mann-Whitney U test is applied to the distribution of RTT values across all probes.

**Key metrics**:
- Error rate and median RTT per resolver type
- Pairwise IP divergence rate: ISP local vs. Google, Cloudflare, Quad9
- Geographic disaggregation of divergence rates by continent

---

## 3.6 Ethical Considerations and Reproducibility

### 3.6.1 Ethical Design

The measurement design follows the ethical framework of Kisteleki et al. (2016) and the principles of the Menlo Report (2012):

**Probe host protection**: All query targets are publicly accessible domains from the Tranco Top 10K corpus. Direct authoritative queries for A records are indistinguishable from normal client DNS traffic.

**Infrastructure impact**: The measurement frequency (once per domain per day, 50 probes, 500 domains) generates approximately 25,000 queries per day --- negligible compared to OpenINTEL's production campaign of several hundred million queries per day (van Rijswijk-Deij et al., 2016).

**Transparency**: All measurements are tagged with a project description in RIPE Atlas, allowing authoritative server operators to identify the measurement source. The measurement plan (`measurements.json`) records all active measurement IDs.

**Data minimisation**: Raw results are retained locally for 7 days only, then deleted after cloud synchronisation. The published dataset uses aggregated statistics.

### 3.6.2 Scientific Reproducibility

**Fixed domain corpus**: The Tranco list identifier recorded in `tranco_meta.json` for each measurement week enables exact reproduction of the domain corpus.

**Measurement traceability**: All RIPE Atlas measurement IDs are recorded in `measurements.json`. Any researcher with a RIPE Atlas account can retrieve the original raw results using these IDs.

**Probe set reproducibility**: The selected probe IDs and their metadata (country, ASN, hardware version) are saved in `selected_probes_<date>.json`.

**Software versioning**: The analysis pipeline is published at https://github.com/ogautier-unam/dns-pipeline. The `requirements.txt` file specifies exact package versions (Python 3.11, dnspython, pandas, pyarrow, scipy, matplotlib) to eliminate software version ambiguity.

**Infrastructure reproducibility**: The Docker container image built from the published `Dockerfile` provides a fully reproducible execution environment across x86_64 and ARM64 architectures, ensuring that the pipeline can be redeployed from source on any compatible host.
