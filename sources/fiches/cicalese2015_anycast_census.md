# Reading Note - Characterizing IPv4 Anycast Adoption and Deployment

**Bibliographic Reference**:
Cicalese, D., Augé, J., Joumblatt, D., Friedman, T., & Rossi, D. (2015). Characterizing IPv4 anycast adoption and deployment. *Proceedings of the 11th ACM Conference on Emerging Networking Experiments and Technologies (CoNEXT '15)*. https://doi.org/10.1145/2716281.2836101

**Theme**:
This paper presents the first Internet-wide census of IPv4 anycast adoption, going beyond the traditional focus on DNS to characterise anycast usage across all TCP services. Using a distributed measurement system running on PlanetLab, the authors conduct four full IPv4 censuses and apply a novel protocol-agnostic technique for anycast detection, enumeration, and geolocation (based on speed-of-light violation between vantage points). They find approximately 1,000 IP/24 anycast subnets in use by major Internet operators for a diverse range of services.

**Relevance to thesis**:
Understanding the prevalence and geographic structure of anycast deployments is foundational for any thesis studying DNS measurements across distributed vantage points, because DNS infrastructure — especially root servers and large authoritative nameservers — is one of the primary use cases for anycast. This paper's census methodology (latency-based anycast detection from geographically distributed vantage points) is directly analogous to the problem of identifying which DNS resolvers or authoritative servers use anycast routing when conducting RIPE Atlas measurements.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 2.2 (Anycast in DNS and CDN infrastructure)
- Section 2.4 (Measurement platforms and methodologies for anycast characterisation)
- Section 4.X (Interpreting geographic variation in DNS measurement results)

---

## Article Content

### Research Objective(s)

**Problem**: While IP anycast has historically been studied primarily in the context of DNS (particularly root servers), its adoption has expanded significantly to CDNs, cloud services, DDoS protection, and other TCP-based services. No Internet-wide census of IPv4 anycast deployment had been conducted, leaving the scientific community without an accurate picture of the current anycast landscape.

**Research questions**:
1. How many IPv4 prefixes are anycast, and which operators use them?
2. What is the geographic footprint of anycast deployments (how many replicas, where are they located)?
3. What services — beyond DNS — are being served over anycast, and by which categories of operator?

### Background

Two distinct anycast paradigms exist: Layer-7 (L7) anycast, which uses DNS or HTTP redirection to map clients to servers (as used by Akamai, Google, etc.), and IP-layer (L3/L4) anycast, where the same IP prefix is announced from multiple locations and BGP routes packets to the nearest replica. Prior studies of IP anycast focused almost exclusively on DNS, particularly root servers, using DNS-specific CHAOS queries for detection. Application-level CDN mapping research used EDNS Client Subnet (ECS) to geolocate PoPs. The authors' previous work introduced a protocol-agnostic technique for IP anycast detection, enumeration, and geolocation based on speed-of-light constraint violations between latency measurements from geographically dispersed vantage points; this paper scales that technique to an Internet-wide census.

### Methodology

- **Study type**: Internet-scale census / active measurement
- **Tools used**: Custom distributed scanner (fastping/TDMI) on PlanetLab nodes (~300 active VPs); IPv4 hitlist (from CAIDA); nmap for port scanning; custom anycast geolocation algorithm (Maximum Independent Set problem solver); city-level geolocation database
- **Scale**: Four full IPv4 censuses; ~10^7 target IP/32 addresses (one per /24 subnet, covering the entire routable IPv4 address space); ~10^2 PlanetLab vantage points; each census completed in under 5 hours
- **Measurement protocol**:
  - Each PlanetLab VP sends ICMP latency probes to all ~10^7 target IPs
  - ICMP replies received; ICMP error senders added to a greylist to avoid re-probing
  - Anycast detection: if latency from two geographically separated VPs to the same target violates the speed-of-light constraint (i.e., their minimum-latency disks do not intersect), the target is anycast (two VPs are contacting different replicas)
  - Replica enumeration: Maximum Independent Set (MIS) problem solved on the set of non-overlapping disks to conservatively enumerate the minimum number of distinct replicas
  - Geolocation: maximum likelihood estimator biased toward city population in the smallest latency-bounding disk; ~75% city-level accuracy verified against ground truth CDNs (CloudFlare, Edgecast)
  - TCP port scanning (nmap) on anycast IPs to characterise services
- **Data collected**: Anycast IP/24 prefixes; number of replicas per deployment; geographic distribution of replicas; open TCP ports and service fingerprints; operator categories (ISP, CDN, cloud, equipment vendor)

### Main Results

1. **Scale of anycast adoption**: Approximately 10^3 (order of magnitude) IP/24 subnets are anycast in the current IPv4 Internet — roughly 0.1% of the routable IPv4 address space, but covering a significant fraction of Internet traffic volume.
2. **Geographic footprint**: Anycast deployments conservatively have on average ~10 replicas; the true number is likely higher given the conservative MIS enumeration approach and the limited (~10^2) number of vantage points.
3. **Operator diversity**: Major operators using anycast include tier-1 ISPs, over-the-top content providers, cloud service providers, and network equipment vendors — not just DNS operators.
4. **Service diversity**: TCP port scanning reveals over 10,000 open ports on anycast IPs, mapping to approximately 500 well-known service types. HTTP and HTTPS are the most common, served by anycast CDNs whose websites appear in the Alexa top-100k list.
5. **ASN concentration**: Anycast is used by ASes in the CAIDA top-10 rank (by customer cone size), and by ASes serving HTTP/HTTPS content for top-100k Alexa websites — the most Internet-traffic-significant operators.
6. **Measurement platform choice**: PlanetLab was preferred over RIPE Atlas, MLab, and Archipelago for this census due to its larger number of geographically dispersed vantage points and software control flexibility. RIPE Atlas was noted to have fewer VPs (~8,000 but predominantly residential) and less flexibility for scanning-style censuses. For O(10^7) targets, the authors trade completeness for scale compared to DNS-specific studies using O(10^4)–O(10^5) VPs.

### Authors' Conclusion

The authors present the first comprehensive picture of IPv4 anycast adoption across the Internet, revealing that anycast usage has expanded far beyond DNS to serve a broad range of TCP services from major Internet operators. The city-level geolocation technique achieves ~75% accuracy against ground-truth CDN data, enabling meaningful geographic characterisation of anycast deployments. The conservative enumeration yields an average of ~10 replicas per anycast deployment. The main contribution is demonstrating that IP anycast is a pervasive, protocol-agnostic routing strategy used by the most traffic-significant operators in the Internet ecosystem.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- Speed-of-light violation as the fundamental detection principle for anycast from distributed vantage points — directly applicable to interpreting geographic variation in DNS query latency from RIPE Atlas probes
- The distinction between the number of anycast replicas (enumerated conservatively) and the number of probe vantage points needed to observe them: O(10^2) VPs can detect anycast deployments but underestimate the number of replicas
- The trade-off between census completeness and scale: more vantage points improve anycast replica enumeration but at measurement cost proportional to VP count × target count

**Applicable methods**:
- Latency-based anycast detection: if two geographically separated RIPE Atlas probes report substantially different latencies to the same target IP, the target is likely anycast and the probes are hitting different replicas — relevant for interpreting per-probe DNS response variation
- MIS-based conservative replica enumeration as a lower bound on the true number of anycast instances
- Combining active latency measurements with TCP port scanning to characterise the services behind detected anycast deployments

**Important statistics**:
- ~10^3 IP/24 anycast subnets found in the IPv4 Internet
- ~10 replicas per anycast deployment on average (conservative estimate)
- ~75% city-level geolocation accuracy against CDN ground truth
- Median geolocation error: 350 km (for incorrectly geolocated anycast replicas)
- Entire IPv4 address space census completed in under 5 hours using ~10^2 PlanetLab VPs

**Identified limitations (gaps to fill)**:
- O(10^2) PlanetLab VPs are insufficient to achieve high recall on anycast replica enumeration; studies focused on individual targets (e.g., DNS root servers) use O(10^4)–O(10^5) VPs for ~90% recall
- The census captures a point-in-time snapshot; anycast deployments change as operators add/remove PoPs
- IPv6 anycast is not addressed in this paper

### Personal Critique

**Strengths**:
- First Internet-wide census of IPv4 anycast — establishes an empirical baseline for all subsequent anycast research
- Protocol-agnostic methodology makes the technique applicable beyond DNS; validated against known CDN ground truths
- Honest about limitations: conservative enumeration, vantage point constraints, and accuracy bounds are clearly quantified

**Weaknesses**:
- PlanetLab's ~300 active VPs are geographically biased toward research institutions (universities), which may miss anycast replicas in regions underrepresented in academic networks
- The conservative MIS enumeration systematically underestimates the number of replicas, especially for densely deployed anycast networks (e.g., Cloudflare)
- IPv6 anycast is entirely excluded; as IPv6 adoption grows, this is an increasingly significant omission

**Links to other papers**:
- Calder et al. (IMC 2015, anycast CDN performance): Complements this census with a deep performance analysis of one specific anycast CDN deployment
- Koch et al. (anycast context): Addresses how to interpret anycast measurements given the geographic routing context of vantage points
- Bajpai et al. (2017, RIPE Atlas tags): The RIPE Atlas platform whose limitations for census-scale measurements are acknowledged in this paper

**Open questions**:
- How has the number and geographic distribution of anycast deployments evolved since 2015, particularly with the rapid growth of Cloudflare and other cloud/CDN operators?
- Can RIPE Atlas's ~12,000 probes (as of 2024) provide sufficient VP density for anycast census purposes, given the platform improvements since this paper was written?

### Key Quotes

> "We conduct and combine delay measurements from four full censuses, based on which we find about O(10^3) IP/24 subnets to be anycasted."

> "We provide empirical evidence that IP anycast is used by ASes in the CAIDA top-10 rank and by ASes serving content over HTTP and HTTPS for websites in the Alexa top-100 rank."

> "A large number of vantage points is required to provide an accurate picture of anycast deployment, especially in terms of the number of replicas discovered around the world. Related work that focuses on O(1) targets (i.e., DNS root-servers) indeed run measurement campaigns involving from O(10^4) to O(10^5) vantage points to achieve ~90% recall."

---

## Use in Thesis

**Relevant sections**:
- Section 2.2 (Anycast in DNS infrastructure): Cite for the Internet-wide scale of anycast adoption and the operator categories that use it; emphasise that DNS is one use case among many
- Section 2.4 (Measurement methodology for anycast): Reference the speed-of-light violation detection principle as the theoretical basis for interpreting geographic variation in RIPE Atlas DNS measurements
- Section 4.X (Interpreting per-probe DNS response variation): Use the anycast detection framework to contextualise cases where different RIPE Atlas probes receive different DNS responses from nominally the same anycast server

**Points to develop**:
- Explain how the anycast structure of DNS root servers and large authoritative nameservers implies that geographically different RIPE Atlas probes will contact different physical replicas, making geographic variation in DNS responses a fundamental feature rather than measurement noise
- Discuss whether the census-level O(10^2) VP approach provides sufficient recall for characterising the anycast DNS targets used in the thesis measurements

**Cross-references**:
- `calder2015_anycast_cdn_performance.md`: Performance analysis of a specific anycast CDN, complementing this census
- `bajpai2017_ripeatlas_tags.md`: RIPE Atlas probe capabilities and limitations for anycast studies
- `finnegan2018_anycast_dns_atlas.md`: RIPE Atlas-based anycast characterisation for DNS specifically

---

**Tags**: #anycast #census #ipv4 #dns #cdn #measurement #planetlab #geolocation #bgp #speed-of-light
**Status**: [X] Read / [X] Filed
