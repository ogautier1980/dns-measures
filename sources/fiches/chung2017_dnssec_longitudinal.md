# Reading Note - A Longitudinal, End-to-End View of the DNSSEC Ecosystem

**Bibliographic Reference**:
Chung, T., van Rijswijk-Deij, R., Chandrasekaran, B., Choffnes, D., Levin, D., Maggs, B. M., Mislove, A., & Wilson, C. (2017). A longitudinal, end-to-end view of the DNSSEC ecosystem. *Proceedings of the 26th USENIX Security Symposium*, 1307–1322. **Distinguished Paper Award.**

**Theme**:
First large-scale, longitudinal measurement study of DNSSEC management quality across the full .com, .org, and .net ecosystems over 21 months. Reveals pervasive mismanagement of the DNSSEC PKI by domain operators and resolver operators alike, using OpenINTEL data supplemented by active resolver measurements.

**Relevance to thesis**:
This paper demonstrates the power of longitudinal active DNS measurement (via OpenINTEL) to uncover systemic infrastructure failures invisible to point-in-time snapshots — directly motivating the temporal stability dimension (Q2) of this thesis. It also provides empirical grounding for the claim that DNS infrastructure management has real, measurable quality problems at scale.

---

## Reading Context

**Date**: April 2026
**Thesis sections**:
- Section 2.2 (DNS Measurement Paradigms — OpenINTEL use case)
- Section 2.1 (DNS Background — DNSSEC record types)

---

## Article Content

### Research Objective(s)

**Problem**: DNSSEC is designed to protect DNS integrity via a hierarchical PKI, but whether domain operators and resolvers actually manage it correctly at population scale was unknown.

**Research questions**:
1. Do authoritative name servers correctly publish all DNSSEC records required for validation?
2. Do domains use sufficiently strong cryptographic keys?
3. Do recursive resolvers actually validate DNSSEC signatures?

### Background

DNSSEC extends DNS with a hierarchical PKI: each zone signs its records and publishes the signing keys (DNSKEY), while the parent zone signs the child's key hash (DS record), creating a chain of trust from the root down. For validation to work, three parties must perform their role correctly: (1) the authoritative server must publish complete, valid records and signatures; (2) the parent zone must correctly delegate (DS record); and (3) the recursive resolver must actually attempt validation. This paper is the first to measure all three simultaneously at large scale and longitudinally.

### Methodology

- **Data source**: OpenINTEL daily snapshots of all DNSSEC-enabled domains under .com, .org, .net (21 months, covering ~50% of global namespace)
- **Supplementary data**: Active measurements of 59,000+ DNS resolvers worldwide
- **Analysis**: Key algorithm and key size classification; DS-DNSKEY consistency checking; resolver behaviour probing (DO-bit, validation of intentionally broken signatures)
- **Scale**: Tens of millions of DNSSEC-signed domains; 21-month longitudinal window

### Main Results

1. **31%** of DNSSEC-supporting domains fail to publish all records required for end-to-end validation (missing RRSIG, DS, or DNSKEY records)
2. **39%** of domains use insufficiently strong key-signing keys (RSA < 2048 bits or weak algorithms)
3. **82%** of resolvers request DNSSEC records (set the DO bit), but only **12%** actually validate them
4. Key management failures are systemic and persistent — not random errors — and invisible without longitudinal data
5. Several large DNS hosting providers are responsible for the majority of misconfigurations, amplifying the impact of their errors

### Authors' Conclusion

DNSSEC management is broadly dysfunctional. The root cause is the absence of automated key management tooling and auditing at both the authoritative and resolver levels. The authors call for improved automation (analogous to Let's Encrypt for TLS) and continuous monitoring infrastructure.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- Longitudinal active measurement (OpenINTEL) as the only method capable of detecting persistent, systemic DNS infrastructure failures
- The gap between "DNSSEC-enabled" and "DNSSEC-correctly-managed" is large and measurable
- Resolver behaviour (validation rate) cannot be inferred from authoritative-side data alone

**Important statistics**:
- 31% of DNSSEC domains have incomplete records
- 39% use weak KSKs
- Only 12% of resolvers validate DNSSEC despite 82% requesting records
- Study covers 21 months of OpenINTEL data for .com/.org/.net

**Identified limitations**:
- Study covers only .com, .org, .net — country-code TLDs not included
- Resolver sample may not be representative of end-user resolver distribution

### Personal Critique

**Strengths**:
- First end-to-end, longitudinal view — strong novelty
- Distinguished Paper Award at USENIX Security 2017
- Combines two complementary data sources (passive OpenINTEL + active resolver probing)
- Actionable policy recommendations

**Weaknesses**:
- Limited to DNSSEC-signed domains (subset of all domains)
- Resolver probing methodology may not generalise to all resolver types

**Links to other papers**:
- van Rijswijk-Deij 2016 (OpenINTEL infrastructure): Provides the data platform used in this study
- van der Toorn 2018 (snowshoe spam): Another longitudinal OpenINTEL use case showing security insight from DNS data

### Key Quotes

> "31% of domains that support DNSSEC fail to publish all relevant records required for validation."

> "Although 82% of resolvers in our study request DNSSEC records, only 12% of them actually attempt to validate them."

> "These results highlight systemic problems, which motivate improved automation and auditing of DNSSEC management."

---

## Use in Thesis

**Relevant sections**:
- Section 2.2 (OpenINTEL): Cite as concrete example of what longitudinal active DNS measurement reveals — systemic DNSSEC key management failures invisible to point-in-time studies
- Section 2.1.1 (DNSKEY/DS/RRSIG record types): Cite for empirical evidence of why these records matter

**BibTeX key**: `Chung2017`

---

**Tags**: #dnssec #longitudinal #openintel #key-management #resolver #security #pki
**Status**: [X] Read / [X] Filed
