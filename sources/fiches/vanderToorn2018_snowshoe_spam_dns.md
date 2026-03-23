# Reading Note - Melting the Snow: Using Active DNS Measurements to Detect Snowshoe Spam Domains

**Bibliographic Reference**:
van der Toorn, O., van Rijswijk-Deij, R., Geesink, B., & Sperotto, A. (2018). Melting the Snow: Using Active DNS Measurements to Detect Snowshoe Spam Domains. *NOMS 2018 — IEEE/IFIP Network Operations and Management Symposium*. DOI: 10.1109/NOMS.2018.8406264. University of Twente / SURFnet.

**Theme**:
This paper combines large-scale active DNS measurements (from the OpenINTEL platform) with supervised machine learning to detect domains crafted for snowshoe spam — a type of spam that evades reputation-based filters by distributing sending across many hosts. The key insight is that snowshoe domains, in order to appear legitimate, must register and configure DNS domains with unusually large numbers of A and MX records and large SPF TXT records. These DNS "fingerprints" are detectable proactively, before the domains are actually used for spam.

**Relevance to thesis**:
This paper demonstrates a concrete security application of large-scale active DNS measurements, directly using the OpenINTEL dataset that our thesis also engages with. It shows how DNS record structure across millions of domains can be analyzed systematically — via long-tail statistical filtering and machine learning — to detect anomalous configurations. The methodology illustrates the broader value of the DNS as a measurement substrate and the complementarity of active measurements (which detect pre-configured but not-yet-used domains) and passive measurements (which only observe traffic).

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.3 (OpenINTEL — applications of large-scale DNS measurements)
- Section 2.7 (DNS measurement biases and limitations)
- Section 2.9 (DNS security applications)

---

## Article Content

### Research Objective(s)

**Problem**: Snowshoe spam distributes the sending load across a large number of hosts/domains to evade IP-based reputation systems (Real-time Blackhole Lists, RBLs). Anti-abuse vendors estimate that 15% of spam is snowshoe spam. Existing detection methods rely primarily on observing spam traffic (passive detection), which means spam that has already been sent may evade filters until the sending domains are blacklisted — a latency of days to weeks. There is no method to detect snowshoe domains before they are used.

**Research questions**:
1. Can active DNS measurements detect snowshoe spam domains proactively — before they appear on established blacklists?
2. Which DNS-derived features best discriminate between legitimate domains and domains crafted for snowshoe spam?

### Background

Snowshoe spam requires spammers to register and properly configure DNS domains, including SPF (Sender Policy Framework) records, in order to appear legitimate. This creates detectable DNS signatures: large numbers of A records (one per sending host), large numbers of MX records, and large TXT records with SPF configurations listing many IP addresses. Standard passive DNS monitoring (pDNS) can only detect domains that have already generated observable traffic. Active DNS measurements query all registered domains regardless of whether they have been used, enabling proactive detection. OpenINTEL covers more than 60% of the global DNS namespace daily, making it an ideal data source for this type of analysis.

### Methodology

- **Study type**: Security measurement / machine learning classification
- **Tools used**: OpenINTEL (active DNS measurement platform), scikit-learn (Python ML library), multiple blacklists (multi.uribl.com, dbl.spamhaus.org, rbl.rbldns.ru, zen.spamhaus.org), Alexa top 1 million list (for negative training examples)
- **Scale**: OpenINTEL covers >60% of global DNS namespace; daily detections from May 24 to September 5, 2017; training dataset from April 18–24, 2017; evaluation dataset from April 25, 2017
- **Measurement protocol**: (A) Daily OpenINTEL data ingestion; (B) Long-tail analysis — filter domains exceeding the 97th, 98th, 99th, or 99.9th percentile in A record count, MX record count, or TXT record length; (C) Machine learning classifier applied to candidate domains (35 features derived from DNS records); (D) Results stored in a Real-time Blackhole List (RBL). Classifier selected by K-fold cross-validation with precision as the optimization metric (to minimize false positives).
- **Data collected**: 35 features per candidate domain including: number of A records, IPv4 prefixes, IPv6 addresses, MX records, NS records, CNAME records, TXT record lengths, SPF components (number of IP4/IP6/include/CIDR entries), SOA minimum TTL, AS count, country code count, and query/response name matching

### Main Results

1. **Feature discrimination**: At the 90th percentile of A record distribution, snowshoe spam domains have on average 16.2 more A records than legitimate domains. At the 98th percentile of MX record distribution, spam domains have 77 more MX records. The most discriminating single feature is `response_name_matches` (whether the DNS response name matches the query name), followed by `ip4_count` and `mx_count`.

2. **Classifier selection**: The AdaBoost classifier achieves the highest precision among 13 evaluated classifiers. After parameter tuning ("AdaBoost Improved"), it achieves: 6,688 True Positives, 7,842 False Negatives, 110 False Positives, 10,741 True Negatives — corresponding to an accuracy of 68.69% but a precision of 98.38%. The high precision (low false positive rate) is the primary design objective since falsely flagging legitimate domains as spam has high operational cost.

3. **Early detection**: The method detects a significant fraction of malicious domains up to 100 days earlier than existing blacklists. This lead time provides a substantial operational advantage: emails from these domains can be blocked before they appear on public RBLs.

4. **Real-world deployment**: The system was deployed in production at SURFnet (a major Dutch research and education network operator) for a 3-month validation period. The operator decided to keep the system in production based on the results.

5. **Dataset characteristics**: At the 99.9th percentile threshold, approximately 2,700 candidate domains per day; at the 97th percentile, approximately 57,300 candidate domains per day. The choice of threshold trades detection sensitivity against classifier workload.

### Authors' Conclusion

The authors conclude that active DNS measurements can detect snowshoe spam domains proactively with high precision (>93%) and significantly ahead of existing blacklists (up to 100 days). The approach is content-agnostic: it relies solely on DNS record structure, not email content or traffic patterns. The system has been validated in real operational deployment. The combination of OpenINTEL's comprehensive DNS coverage and machine learning over DNS features represents a powerful paradigm for proactive threat detection.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- Active vs. passive DNS measurement: active measurements detect pre-configured domains regardless of whether they have been accessed; passive measurements are usage-biased
- Long-tail analysis as a filtering technique: the vast majority of domains have few records of each type; anomalous behavior appears in the statistical long tail
- The DNS as a security measurement substrate: domain configuration (record types, counts, structure) encodes behavioral patterns exploitable for security analysis

**Applicable methods**:
- Percentile-based thresholding for identifying anomalous domains in large DNS datasets — applicable to identifying domains with unusual CDN configurations or DNSSEC deployment patterns
- K-fold cross-validation with precision-optimized classifier selection: methodology applicable to any binary classification task over DNS features
- Cross-referencing DNS measurements with external blacklists or ground-truth lists (analogous to cross-referencing our DNS measurements with Tranco rankings)

**Important statistics**:
- 15% of spam estimated to be snowshoe spam (Cisco, 2014)
- Precision of >93% (98.38% for best classifier) with very low false positive rate (110 FP out of 17,650 total classifications)
- Up to 100 days earlier detection than public blacklists
- ~2,700 candidate domains per day at 99.9th percentile; ~57,300 at 97th percentile
- OpenINTEL covers >60% of global DNS namespace at time of study (covering .com, .net, .org, .info, .mobi, new gTLDs, selected ccTLDs)

**Identified limitations (gaps to fill)**:
- High false negative rate (7,842 FN): the AdaBoost classifier misses a significant fraction of actual spam domains, suggesting that some snowshoe operators successfully mimic legitimate domain configurations
- Alexa list used as negative training examples is not a reliable benign ground truth (some Alexa domains may themselves be malicious)
- Detection is limited to snowshoe spam; other spam types with different DNS signatures require separate detection approaches
- The 97th percentile threshold is somewhat arbitrary and the optimal value may drift as spammers adapt

### Personal Critique

**Strengths**:
- Strong practical validation: actual production deployment at a major network operator demonstrates real-world utility
- Clear motivation for active vs. passive measurements: the 100-day lead time advantage is a compelling, quantified result
- Ethical analysis included (Section VII): the authors consider the implications of operating a blacklist and discuss responsible disclosure

**Weaknesses**:
- Precision-recall trade-off is imbalanced by design: achieving 98% precision at the cost of 54% recall (missing nearly half of spam domains) may not be acceptable in all deployment contexts
- The Alexa list is used as a negative example set, but Alexa ranks by traffic, not legitimacy, introducing potential noise
- The study period (May–September 2017) may not generalize across seasons or as spammer tactics evolve

**Links to other papers**:
- van Rijswijk-Deij et al. (2016) — OpenINTEL infrastructure: this paper is a direct downstream application of the OpenINTEL platform; understanding the infrastructure is prerequisite to understanding this study
- Perdisci et al. — passive DNS for botnet detection: contrasted as a complementary but usage-dependent approach
- Hao et al. — domain registration history for malicious domain detection: shares the intuition that malicious domains are registered and configured before use

**Open questions**:
- Can the long-tail methodology be adapted to detect CDN misconfiguration (e.g., domains with unusual numbers of geographically dispersed CDN CNAME chains) rather than spam domains?
- How do snowshoe operators adapt their DNS configurations in response to active detection? Is there an evolutionary arms race detectable in longitudinal OpenINTEL data?
- What is the false positive rate in a more representative negative sample (e.g., a random sample of all .com domains, rather than Alexa top 1M)?

### Key Quotes

> "Anti-abuse vendors estimate that 15% of spam can be classified as snowshoe spam."

> "We are able to detect a significant fraction of the malicious domains up to 100 days earlier than existing blacklists, which suggests our method can give us a time advantage in the fight against spam."

> "In spam detection it is far more costly to make an FP, a ham domain marked as spam, than any other error. The cost of making a FP outweighs making a correct classification, a TP."

---

## Use in Thesis

**Relevant sections**:
- Section 2.3 (OpenINTEL applications): Concrete example of how the OpenINTEL dataset enables security research at scale; motivates why comprehensive DNS measurement infrastructure has value beyond operational monitoring
- Section 2.9 (DNS security): Illustrates how DNS data can detect abuse proactively; relevant to broader discussion of DNS as a security measurement substrate
- Section 2.7 (Measurement limitations): The active vs. passive trade-off and the usage bias of passive DNS measurements are directly relevant to our discussion of measurement methodology limitations

**Points to develop**:
- The complementarity of active and passive DNS data: our thesis should explicitly position RIPE Atlas (geographically distributed active measurements) relative to passive DNS and OpenINTEL
- Long-tail analysis as a general technique: domains with unusual DNS behavior (many CDN CNAMEs, unusual TTL patterns) may be detectable via similar percentile filtering in our dataset

**Cross-references**:
- `vanRijswijk2016_openintel_infrastructure.md` — OpenINTEL platform that provides the data
- `lePochat2019_tranco_ranking.md` — domain list methodology: Tranco is a more robust alternative to Alexa for negative training examples

---

**Tags**: #snowshoe-spam #active-DNS #OpenINTEL #machine-learning #AdaBoost #RBL #security #long-tail #SPF #passive-DNS
**Status**: [X] Read / [X] Filed
