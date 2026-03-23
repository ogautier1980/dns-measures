# Reading Note - RIPEn at Home: Surveying Internal Domain Names using RIPE Atlas

**Bibliographic Reference**:
Boswell, E., & Perkins, C. (2024). RIPEn at home – Surveying internal domain names using RIPE Atlas. *Proceedings of the Network Traffic Measurement and Analysis Conference (TMA 2024)*. IFIP. ISBN: 978-3-903176-64-5.

**Theme**:
This paper uses active DNS measurements on RIPE Atlas to survey the internal domain names used by home network gateways. It develops a methodology for detecting internal names — those resolved locally and not by the global DNS — using traceroute-based gateway discovery, reverse DNS queries, and BIND CHAOS TXT fingerprinting. The study determines which of these internal names are at risk of DNS name collision if their top-level domains are or become delegated in the public DNS.

**Relevance to thesis**:
This paper is relevant to a thesis on distributed DNS measurements because it demonstrates a sophisticated active measurement methodology on RIPE Atlas that combines multiple DNS query types (rDNS, CHAOS TXT, A records) to characterise per-probe network environments. It also illustrates how the home-network concentration of RIPE Atlas probes — a well-known property of the platform — can be leveraged as a feature rather than treated only as a bias. The name collision risk analysis connects to broader DNS infrastructure security and stability concerns.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.4 (RIPE Atlas infrastructure and measurement capabilities)
- Section 3.X (Active DNS measurement methodology using RIPE Atlas)
- Section 2.1 (DNS fundamentals: internal names, TLDs, name collisions)

---

## Article Content

### Research Objective(s)

**Problem**: Many home network gateways use internal domain names (e.g., `fritz.box`) resolved locally rather than by the global DNS. If a top-level domain used internally is later delegated in the public DNS, queries accidentally sent to a public resolver can resolve to a different (potentially malicious) address — a "name collision." There is no comprehensive survey of which internal names are used in home networks, and which are at collision risk.

**Research questions**:
1. What internal domain names are used by RIPE Atlas probes' home gateway networks, and which top-level domains do they use?
2. Which of these internal names are currently at risk of name collision (i.e., the name is unregistered but registrable in the public DNS)?
3. Which names could become vulnerable if their currently-undelegated TLD is added to the public DNS?

### Background

The Domain Name System (DNS) is globally distributed and hierarchically organised, managed at the root by ICANN/IANA. Internal domain names are resolved by local nameservers and typically use TLDs not present in the public DNS. Name collisions occur when an internal name is also resolved in the global DNS, potentially spoofing local resources. The expansion of new generic TLDs (starting in 2013) dramatically increased the risk: ICANN added 1,241 new gTLDs by November 2023, and the delegation of the `.box` TLD in August 2023 created a concrete collision risk for AVM FRITZ!Box home gateways (the most popular gateway model in Germany), since `fritz.box` was not pre-registered by AVM and was acquired by domain speculators in January–February 2024. RIPE Atlas, with approximately 12,000 probes as of early 2024, many located in home networks, is well suited for client-side measurement of internal names.

### Methodology

- **Study type**: Active measurement / empirical survey
- **Tools used**: RIPE Atlas measurement API; traceroute, DNS (rDNS, CHAOS TXT, A record queries)
- **Scale**: All available IPv4 RIPE Atlas probes tested in early 2024; gateway addresses found for 7,441 probes (traceroute method) and 6,045 probes (local resolver method); 4,305 probes with internal names detected; 3,092 distinct internal names discovered
- **Measurement protocol**: Four-step procedure:
  1. Detect gateway address: via traceroute (last private address in the path) or local DNS resolver address
  2. BIND fingerprinting: CHAOS TXT queries for `hostname.bind` and `version.bind` to classify gateway models by response code pattern (gateway profile)
  3. Reverse DNS (rDNS) queries: probes query their resolver for the PTR record of the gateway IP; any response resolving to a private address is classified as an internal name
  4. Gateway profile fingerprinting: aggregate rDNS results from probes with the same gateway profile to increase coverage
- **Data collected**: Internal domain names per probe; TLD distribution; name collision risk (unregistered-but-registrable vs undelegated TLDs)

### Main Results

1. **Scale of internal name usage**: 3,092 distinct internal names were found, used by 4,305 probes (50.86% of probes tested). 1,146 names (37.06%) occur only once, suggesting they are unique to individual networks.
2. **Top internal names**: All top 10 full domain names are FRITZ!Box-related (e.g., `fritz.box`, `myfritz.box`, `wpad.fritz.box`), reflecting the gateway's popularity in Europe and the tendency of a single rDNS query to a FRITZ!Box to return multiple names.
3. **Top TLDs**: The most common undelegated TLDs are `box`, `lan`, and `nas`, followed by `hole` (PiHole ad blocker) and `home`. `local` (mDNS) and `localdomain` also appear.
4. **Current collision risk**: Of 1,766 names with a public TLD, 1,687 (95.53%) have a resolvable public-suffix subdomain (i.e., cannot be independently registered). 66 names (3.74% of names with public TLD; 2.13% of all names) are unregistered and registrable — these are currently at collision risk.
5. **Future collision risk from undelegated TLDs**: 1,326 names (42.88%) use a TLD not currently in the public DNS. Of these, 1,067 (34.51% of all names) use a TLD that is neither delegated nor a special-use domain name — these would be at collision risk if their TLD is delegated in future.
6. **Special-use name adoption is low**: Only 24 probes use `home.arpa` (the IETF-standardised special-use alternative to `home`), and only one top-10 TLD (`local`, for mDNS) is a recognised special-use name.

### Authors' Conclusion

RIPE Atlas active measurements can effectively detect internal domain names used in home network environments, revealing a substantial and diverse ecosystem of internally-used names. The dominant presence of FRITZ!Box-related names reflects both the gateway's market share and the richness of names it exposes via rDNS. A significant fraction of these internal names — 34.51% — could face name collision risk if their TLD is delegated, while 2.13% face current collision risk. The low adoption of standardised special-use names (like `home.arpa`) suggests that the industry has not converged on safe internal naming practices. The authors plan to expand gateway fingerprinting coverage and improve representativeness in future work.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- Active measurement methodology combining traceroute, rDNS, and CHAOS TXT queries as a multi-step DNS fingerprinting pipeline
- RIPE Atlas's high concentration of home network probes is a feature for studying end-user DNS behaviour, not just a sampling bias
- Name collision risk as a security consequence of the mismatch between internal DNS namespaces and evolving public TLD delegations

**Applicable methods**:
- CHAOS TXT queries (`hostname.bind`, `version.bind`) as a lightweight probe-level fingerprinting technique to classify resolver/gateway types without requiring full DNS resolution testing
- Gateway profile clustering to aggregate results across probes with similar network environments — a form of stratified analysis applicable to broader DNS measurement studies
- Combining traceroute results with DNS queries to construct a richer picture of the per-probe network environment

**Important statistics**:
- 50.86% of RIPE Atlas probes tested had detectable internal names in early 2024
- 34.51% of discovered internal names use an undelegated TLD at risk of future collision
- 2.13% of internal names are currently registrable (immediate collision risk)
- RIPE Atlas has ~12,000 probes as of early 2024
- 37.06% of discovered names appear at only one probe — suggesting high diversity of home network configurations

**Identified limitations (gaps to fill)**:
- mDNS names (`local` TLD) cannot be detected as RIPE Atlas does not support mDNS queries, creating a systematic blind spot
- RIPE Atlas probes are operated by technically sophisticated users; results may not be representative of average home networks
- The study cannot detect ongoing vs potential name collisions (it cannot determine if the internal and public names are controlled by the same entity)

### Personal Critique

**Strengths**:
- Novel and well-designed active measurement methodology that creatively uses multiple DNS query types in combination
- Concrete security-relevant findings (the fritz.box collision case) ground the abstract collision risk in a real recent incident
- Thorough comparison with prior passive measurement studies (root server logs, resolver logs) identifies what client-side active measurement adds

**Weaknesses**:
- Sample representativeness is limited by the technically-skewed RIPE Atlas user base; the authors acknowledge this
- mDNS (the `local` TLD) is excluded by platform limitations, underestimating one important category of internal name
- Results are a one-time snapshot (early 2024) with no longitudinal comparison; internal name usage patterns may evolve

**Links to other papers**:
- Bajpai et al. (2017, RIPE Atlas tags): This paper's home-network probe concentration is characterised quantitatively in that work
- Bortzmeyer (DNS tutorial): CHAOS TXT and rDNS query techniques described here are variants of the DNS measurement types described in the tutorial
- Randall et al. (IMC 2021, DNS interception): Uses CHAOS TXT queries similarly to detect DNS interception by home gateways

**Open questions**:
- What is the longitudinal trend in internal name usage? Have new gateway models introduced new TLDs since the FRITZ!Box-era studies?
- Can machine learning on CHAOS TXT response fingerprints be used to automatically classify gateway models at scale across RIPE Atlas probes?

### Key Quotes

> "We find 3092 internal names used by 4305 probes. Of these, 2.13% are currently vulnerable to collision (e.g. unregistered subdomains of existing TLDs), and 34.51% use an undelegated TLD and could be vulnerable if it is delegated."

> "All top 10 full domain names appear to be related to the FRITZ!Box. This is likely due to its popularity in Europe (where many RIPE Atlas probes are located), and because a single rDNS query to a FRITZ!Box often returns multiple names."

> "Only 24 probes use the special-use alternative to home (home.arpa), and only one top 10 TLD (local, for multicast DNS) is a special-use name."

---

## Use in Thesis

**Relevant sections**:
- Section 2.1/2.2 (DNS fundamentals and name collision security): Cite as motivation for understanding how local DNS resolution differs from global DNS behaviour
- Section 2.4 (RIPE Atlas capabilities): Reference the use of CHAOS TXT and rDNS measurement types as examples of non-standard DNS measurement approaches on RIPE Atlas
- Section 3.X (Methodology): The multi-step measurement pipeline is a methodological model for combining different DNS query types in a single campaign

**Points to develop**:
- Discuss how the presence of internal names and non-standard resolvers in home networks constitutes a source of noise in DNS measurement campaigns targeting public DNS infrastructure
- Use the FRITZ!Box prevalence finding to illustrate how gateway model distribution affects the DNS measurement environment on RIPE Atlas

**Cross-references**:
- `bajpai2017_ripeatlas_tags.md`: Home network probe characterisation on RIPE Atlas
- `bortzmeyer_dns_measurements_atlas_tutorial.md`: DNS query types available on RIPE Atlas
- `holterbach2015_ripeatlas_interference.md`: Data quality issues on RIPE Atlas probes

---

**Tags**: #ripe-atlas #dns #home-network #internal-names #name-collision #security #measurement-methodology #chaos-txt #rdns
**Status**: [X] Read / [X] Filed
