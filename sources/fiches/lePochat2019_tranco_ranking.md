# Reading Note - Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation

**Bibliographic Reference**:
Le Pochat, V., Van Goethem, T., Tajalizadehkhoob, S., Korczyński, M., & Joosen, W. (2019). Tranco: A research-oriented top sites ranking hardened against manipulation. In *Proceedings of the 26th Annual Network and Distributed System Security Symposium (NDSS 2019)*. Internet Society. https://dx.doi.org/10.14722/ndss.2019.23386

**Theme**:
This paper systematically analyses the four most widely used website popularity rankings (Alexa, Cisco Umbrella, Majestic, and Quantcast) and demonstrates that all four exhibit serious deficiencies — low inter-list similarity, poor stability, inclusion of non-responsive and malicious domains, and susceptibility to adversarial manipulation. The authors then propose Tranco, a new aggregated ranking designed to be more stable, more representative, and substantially harder to manipulate than any individual list.

**Relevance to thesis**:
Our thesis uses the Tranco list as the primary domain selection mechanism for DNS measurements, following the recommendation of this paper. Understanding why Tranco was designed, what properties it optimises for, and what residual limitations it carries is essential for justifying our domain selection methodology and for correctly interpreting the representativeness of our measurements relative to the broader Web.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.6 (Domain lists and their properties — Tranco vs alternatives)
- Section 3.x (Methodology — domain selection and justification)
- Section 2.7 (Biases in domain lists and their consequences for DNS measurement studies)

---

## Article Content

### Research Objective(s)

**Problem**: Security and network measurement researchers rely on website popularity rankings (primarily Alexa) to select representative domain sets for their studies. However, these rankings are commercial products with undisclosed methodologies, are susceptible to manipulation, and may produce significantly different results depending on which list is chosen — undermining the reproducibility and validity of research that relies on them.

**Research questions**:
1. Do the four major website popularity rankings agree on which domains are popular, and are they stable over time?
2. Are these rankings susceptible to adversarial manipulation, and if so, how easily?
3. Can an improved, manipulation-resistant ranking be constructed that is more suitable for research purposes?

### Background

Website popularity rankings are used pervasively in security and network measurement research: 133 top-tier studies over four years relied on at least one of the four main rankings studied in this paper. Alexa (Amazon subsidiary) ranks domains by a proprietary combination of unique visitors and page views collected from a browser extension panel estimated at around 570,000 Chrome users. Cisco Umbrella ranks domains by unique IP addresses issuing DNS queries to its OpenDNS resolvers (claimed 65 million users). Majestic ranks domains by the number of class-C subnets linking to them (backlink-based, 450 billion URLs crawled over 120 days). Quantcast ranks US-traffic websites using a mix of directly instrumented sites and estimates from ISP/toolbar data. All four providers apply undisclosed normalisation procedures. The commercial nature of these rankings means that incentives to manipulate them exist both for individual domain owners (seeking whitelist status) and for adversaries seeking to bias research conclusions.

### Methodology

- **Study type**: Empirical analysis (longitudinal measurement + manipulation experiments)
- **Tools used**: Daily list downloads (January 1 – November 30, 2018); distributed crawler (10 machines, 4 CPU cores, 8 GB RAM each; Ubuntu 16.04, Chromium 66 headless mode); Google Safe Browsing API; rank-biased overlap (RBO) similarity metric; HTTP status code analysis
- **Scale**: 10 months of daily snapshots of all four lists; one full crawl of all listed domains on May 11, 2018; analysis of approximately 2.82 million unique domains across all four lists combined; 133 security studies reviewed
- **Measurement protocol**: Five properties were measured for each list: (1) Similarity — inter-list overlap using rank-biased overlap (RBO); (2) Stability — day-to-day intersection percentage; (3) Representativeness — TLD distribution, ASN concentration, hosting entity diversity; (4) Responsiveness — HTTP status codes and page sizes from live crawl; (5) Benignness — Google Safe Browsing flags. Manipulation experiments involved generating traffic to specific domains through minimal HTTP requests and measuring resulting rank changes.
- **Data collected**: Daily list snapshots; crawled HTTP responses for all listed domains; Safe Browsing flags; rank changes following manipulation attempts

### Main Results

1. **Low inter-list similarity**: The four lists combined contain approximately 2.82 million unique sites but agree on only about 70,000. Even weighting top ranks heavily with rank-biased overlap (RBO), similarity between any two lists ranges from only 4.5% to 33%, demonstrating that the choice of list fundamentally changes the domain set studied. Switching lists can alter the apparent prevalence of web trackers, security vulnerabilities, or other features by large margins.
2. **Poor and deteriorating stability**: Until January 30, 2018, Alexa was relatively stable (approximately 1% daily change). After that date, Alexa silently changed to a one-day averaging window, causing approximately 50% of the top million to change every single day. Majestic and Quantcast are most stable (approximately 1% daily change). Umbrella changes on average 10% per day.
3. **Poor representativeness and responsiveness**: 28% of Umbrella-listed domains could not be reached (name resolution failure, mostly for internal domains like *.ec2.internal). Only 49% of Umbrella-listed domains responded with HTTP 200. 5% of Alexa's and Quantcast's domains were unreachable. For Majestic, 11% were unreachable. Many "popular" domains contain no content (pages under 512 bytes).
4. **Malicious domains present on all lists**: The Majestic list contained 2,162 domains flagged by Google Safe Browsing as malware, social engineering hosts, or potentially harmful applications (0.22% of the list). Alexa's top 10,000 included 4 social engineering sites. This is particularly dangerous given the widespread practice of whitelisting popular domains in security tools (e.g., Quad9 whitelists all of Majestic's list).
5. **Trivial manipulation**: An adversary can enter Alexa's top million with a single HTTP request from a browser with the Alexa extension. The authors empirically validated reaching a rank as good as 28,798 through automated means. Tranco, by aggregating multiple lists over a configurable multi-day window using a Dowdall rule scoring function, requires at least four times more effort to achieve the same rank and varies by only 0.6% daily.

### Authors' Conclusion

The authors conclude that existing website popularity rankings are fundamentally unsuitable as research instruments in their raw form due to instability, low inter-list agreement, inclusion of non-representative and malicious domains, and trivial susceptibility to manipulation. They propose Tranco as a community resource: an aggregated, archived, and reproducible ranking available at https://tranco-list.eu that addresses these limitations. Tranco aggregates Alexa, Umbrella, Majestic, and Quantcast over a configurable time window using rank aggregation (Dowdall rule), resulting in a list that is stable, manipulation-resistant, and identifiable by a permanent URL for reproducibility.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- The five properties framework for evaluating domain lists (similarity, stability, representativeness, responsiveness, benignness) — useful for justifying our choice of Tranco in the methodology chapter
- Manipulation susceptibility as a reason why any single commercial list is unsuitable for reproducible research
- The reproducibility advantage of Tranco: a specific Tranco list can be retrieved by identifier, making study replication possible years after publication

**Applicable methods**:
- When selecting our domain sample, specify the exact Tranco list identifier (date, configuration, number of domains) so that the study is reproducible
- Consider the TLD distribution and hosting entity concentration in our sampled domains, as these may affect DNS measurement results (e.g., CDN-hosted domains have different DNS resolution patterns than self-hosted ones)
- Filter unreachable domains before measurements (as approximately 5% of Alexa domains are unresolvable) to avoid polluting DNS measurement statistics with NXDOMAIN and connection-refused results

**Important statistics**:
- 133 top-tier studies over four years relied on at least one of the four main rankings
- The four lists together contain approximately 2.82 million unique sites but agree on only approximately 70,000 (about 2.5%)
- Alexa changed approximately 50% of its top million every day after January 30, 2018
- Majestic contained 2,162 malicious domains (0.22% of its list); Umbrella had 1,011
- Umbrella: only 49% of domains respond with HTTP 200; 28% fail name resolution
- Tranco varies by only 0.6% daily, requiring at least 4x manipulation effort compared to Alexa

**Identified limitations (gaps to fill)**:
- Tranco itself inherits biases from the component lists it aggregates — including geographic bias towards English-speaking and Western domains, and overrepresentation of CDN-hosted content
- The aggregation methodology (Dowdall rule, configurable window) introduces its own design choices that affect list composition
- No ground truth for "true" domain popularity exists, making it impossible to verify how well any list represents actual Internet usage

### Personal Critique

**Strengths**:
- Rigorous empirical analysis across five distinct properties over a 10-month longitudinal dataset
- First empirical proof that Alexa rankings can be trivially manipulated (a single HTTP request suffices)
- Practical contribution: Tranco is publicly available, actively maintained, and has been widely adopted by the research community

**Weaknesses**:
- The paper does not fully characterise how Tranco's geographic and linguistic biases compare to those of its component lists; it improves on stability and manipulation resistance but may not improve representativeness for non-Western domains
- Quantcast was subsequently dramatically reduced in scope (from approximately 520,000 to approximately 40,000 domains after November 14, 2018); Tranco configurations that include Quantcast after this date may be less representative
- The manipulation experiments were conducted against commercial lists; Tranco's resistance to manipulation was estimated theoretically rather than empirically validated against active adversaries

**Links to other papers**:
- vanRijswijk et al. (2016/2018 OpenINTEL): OpenINTEL uses the Alexa list as its domain selection source — the biases documented here apply to OpenINTEL's historical measurements and should be noted when interpreting OpenINTEL results compared to our Tranco-based measurements
- Holterbach et al. (2015): Measurement validity concerns — parallel to the domain list validity concerns raised here; both papers argue for explicit awareness of the methodological assumptions underlying measurements

**Open questions**:
- How does the Tranco list's composition evolve over multi-year timescales, and does it adequately capture newly popular domains (e.g., TikTok-era domains versus YouTube-era domains)?
- Should our thesis use a fixed historical Tranco list (for reproducibility) or a current list (for contemporary relevance), and what is the trade-off between these two choices?
- Do DNS measurement results (e.g., NXDOMAIN rates, TTL distributions, resolver behaviour) differ systematically between Tranco-listed and Alexa-listed domains, given the different composition of the two lists?

### Key Quotes

> "We found that 133 top-tier studies over the past four years based their experiments and conclusions on the data from these rankings. Their validity and by extension that of the research that relies on them, should however be questioned."

> "Half of the Alexa list changes every day and the Umbrella list only has 49% real sites, as well as security implementations, e.g. the Majestic list contains 2,162 malicious domains despite being used as a whitelist."

> "We are the first to empirically validate that the ranks of domains in each of the lists are easily altered, in the case of Alexa through as little as a single HTTP request."

> "Tranco [...] varies only by 0.6% daily and requires at least the quadrupled manipulation effort to achieve the same rank as in existing lists."

---

## Use in Thesis

**Relevant sections**:
- Section 2.6 (Domain lists): Cite as the primary reference for understanding the limitations of Alexa and other commercial lists, and the rationale for using Tranco; include key statistics (similarity, stability, benignness)
- Section 2.7 (Biases in domain lists): Use the five-property framework to discuss residual biases in Tranco, particularly geographic and linguistic overrepresentation of certain regions and the CDN concentration effect
- Section 3.x (Methodology — domain selection): Cite when justifying the use of Tranco and when specifying the exact list version used (by Tranco identifier and date)

**Points to develop**:
- Discuss the specific Tranco configuration parameters chosen for our study (time window, component lists, number of domains) and their implications for measurement coverage
- Quantify the potential impact of Tranco's residual biases on our DNS measurement results, particularly for non-Western TLDs and country-code domain names

**Cross-references**:
- vanRijswijk2016_openintel_infrastructure.md (uses Alexa as domain source — biases documented here apply)
- vanRijswijk2018_openintel_ongoing.md (longitudinal study using Alexa — same concern applies over time)

---

**Tags**: #tranco #alexa #domain-ranking #measurement-methodology #manipulation #stability #representativeness #reproducibility #security-research
**Status**: [X] Read / [X] Filed
