# Reading Note - Ethics of RIPE Atlas Measurements

**Bibliographic Reference**:
Kisteleki, R. (with contributions from Karrenberg, D., Aben, E., Bush, R., Manojlovic, V., Kühne, M., & Bortzmeyer, S.) (2016, November 7). Ethics of RIPE Atlas Measurements. *RIPE Labs*. https://labs.ripe.net/author/kistel/ethics-of-ripe-atlas-measurements/

**Theme**:
This practitioner article addresses the ethical responsibilities of RIPE Atlas users when designing and running active measurements. Using concrete case studies — including a politically sensitive censorship study ("Ebonia" case) and a Google search term study — the article argues that researchers must consider their impact on volunteer probe hosts, whose internet connections are used to generate measurement traffic. The article situates RIPE Atlas measurement ethics within broader frameworks (Belmont Report, Menlo Report, Allman & Partridge 2016) and describes the institutional safeguards RIPE NCC has implemented (HTTP measurement restrictions, access termination for abuse).

**Relevance to thesis**:
Any thesis chapter describing a distributed DNS measurement campaign using RIPE Atlas must address the ethical dimension of using volunteer infrastructure. This article is the primary reference for justifying and framing the ethical precautions taken in our measurement methodology: choice of benign query targets, avoidance of sensitive domains, awareness of probe host exposure, and compliance with RIPE NCC acceptable use policies.

---

## Reading Context

**Date**: 22 March 2026
**Thesis sections**:
- Section 4 (Methodology: ethical considerations for RIPE Atlas DNS measurements)
- Section 2.4 (RIPE Atlas: platform description and constraints)

---

## Article Content

### Research Objective(s)

**Problem**: RIPE Atlas probes are hosted by volunteers who allow the RIPE NCC to use their internet connection for measurement traffic. Researchers who create user-defined measurements must balance scientific goals against the interests and potential exposure of these volunteers. There is no formal binding ethics process for RIPE Atlas users, yet some measurement types can expose probe hosts to legal or social risk (e.g., measuring access to censored or sensitive content from a probe in a politically repressive jurisdiction).

**Research questions**:
1. What ethical principles should guide RIPE Atlas users when designing measurements, particularly those touching on politically or legally sensitive topics?
2. How does the "volunteer" nature of probe hosting change the ethical calculus compared to passive data collection or server-side measurements?
3. What institutional safeguards can a measurement platform operator (RIPE NCC) implement to protect volunteer probe hosts?

### Background

RIPE Atlas consists of thousands of probes hosted voluntarily by individuals, ISPs, IXPs, and academic institutions worldwide. Probe hosts consent to receiving and generating measurement traffic, but this consent has limits — particularly when measurements could expose the host to legal jeopardy in their jurisdiction. The article was written in a period of growing awareness of internet measurement ethics, following controversies such as the Facebook emotional contagion study and increasing academic scrutiny of internet research methods. The Menlo Report (2012), developed by CAIDA and DHS, extended the human-subject research ethics framework of the Belmont Report (1978) to ICT research. Allman and Partridge (2016) proposed that measurement papers include a formal ethical review section. This article applies these emerging frameworks specifically to RIPE Atlas.

### Methodology

- **Study type**: Policy/practitioner article with illustrative case studies
- **Tools used**: N/A (no empirical measurement; analytical and normative)
- **Scale**: N/A
- **Case studies presented**:
  1. **"Ebonia" case**: A researcher planned to measure access to socially sensitive websites from probes in a politically volatile region. Colleagues pointed out that probe hosts in that region could face serious legal consequences if their connection was used for such measurements — even though the probe hosts themselves were not making the requests. The study design was revised.
  2. **Google Search Study**: Researchers wanted to compare search results across regions using RIPE Atlas probes. RIPE NCC required that only "risk-free search terms such as 'cat' and 'dog'" be used rather than politically or legally sensitive queries.
  3. **Censorship research**: Multiple studies examined DNS manipulation and government-level DNS hijacking (Turkey, Iran) using RIPE Atlas. These required careful consideration of probe host exposure and jurisdiction-specific legal risk.
- **Ethical frameworks cited**:
  - Belmont Report (1978): Foundational principles for human-subject research (beneficence, justice, respect for persons)
  - Menlo Report (2012): Extension of Belmont principles to ICT and internet research
  - Allman & Partridge (2016): Proposal for formal ethical review sections in measurement papers (ACM SIGCOMM)
  - Rogaway (cryptography ethics): Argument that scientists have societal obligations because their work transforms society

### Main Results

1. **Researcher responsibility toward probe hosts**: Probe hosts are not passive infrastructure; they are volunteers whose internet connections and potentially their legal standing are affected by the measurements run through their probes. Researchers must ask: "Will the volunteers be OK with the traffic you generate from their Internet connection?"
2. **Institutional safeguards implemented by RIPE NCC**: HTTP measurements are restricted to RIPE Atlas anchors (trusted destinations only); access to the platform can be terminated for abusive research; capability features can be removed if their misuse creates complaints.
3. **Three truths from Rogaway's cryptography ethics framework** (applied to measurement research):
   - Scientific work transforms society
   - This transformation can be positive or negative
   - Researchers bring unique and essential perspectives to public discourse — and bear corresponding responsibility
4. **Practical checklist for RIPE Atlas users**:
   - Consider whether the volunteer probe hosts will be exposed to risk by the measurement
   - Check whether your organization's ethics or IRB policies apply
   - Be especially cautious when you have elevated privileges or additional credits
   - Understand that RIPE NCC can terminate access for unethical behavior
5. **Formal IRB process not required but recommended**: The article does not mandate institutional review but encourages researchers to consult ethics review processes when measurements could constitute human-subject research.

### Authors' Conclusion

Ethical measurement on RIPE Atlas requires shared responsibility: RIPE NCC considers ethical impact in platform design and feature decisions, but individual users must internalize the same responsibility. The probe host is not merely a network endpoint but a person whose rights and safety must be considered. The article advocates for a culture of ethical self-regulation among RIPE Atlas users, grounded in established frameworks (Menlo, Belmont) and illustrated through concrete case studies where ethical review led to meaningful changes in research design.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- Probe hosts as volunteers with rights and potential legal exposure — not passive infrastructure
- The "Ebonia" case as a canonical example of jurisdiction-specific risk in distributed internet measurement
- Menlo Report (2012) as the primary ethical framework for ICT/internet research, extending Belmont principles
- Researcher responsibility scales with privilege: more credits = more power = more ethical responsibility
- RIPE NCC institutional safeguards (HTTP restriction to anchors, access termination) as evidence of platform-level ethics governance

**Applicable methods**:
- In the thesis methodology chapter: cite this article when justifying the choice of benign, non-sensitive DNS query targets (popular domains from the Tranco list, not politically sensitive or censored content)
- Reference the Menlo Report framework for our ethical self-assessment: our measurements query publicly accessible DNS infrastructure, generate no traffic to probe hosts beyond normal DNS queries, and do not expose probe hosts to legal risk
- Justify not querying domains that are censored or geopolitically sensitive as a deliberate ethical design choice, not merely a technical limitation

**Important statistics / facts**:
- HTTP measurements in RIPE Atlas: restricted to anchors only (institutional safeguard)
- References: Belmont Report (1978), Menlo Report (2012), Allman & Partridge ACM SIGCOMM (2016), Rogaway cryptography ethics
- Contributors include Randy Bush, Stéphane Bortzmeyer, Vesna Manojlovic — leading figures in internet measurement and DNS communities
- Platform reach justification: all case studies show RIPE Atlas enables research that would be impossible without distributed volunteers

**Identified limitations (gaps to fill)**:
- No formal enforceable ethics process: the article is advisory; RIPE NCC has no IRB-equivalent body that reviews measurement proposals before they run
- Retroactive enforcement only: access termination happens after complaints, not before potentially harmful measurements
- The definition of "acceptable" measurements is left partly to user judgment — creating a gray area for edge cases

### Personal Critique

**Strengths**:
- Timely and practical: written at a moment when internet measurement ethics was emerging as a formal concern; directly useful for methodology sections
- Concrete case studies: the Ebonia and Google Search examples make the ethical principles tangible rather than abstract
- Authoritative contributors: the co-authorship list includes the leading DNS and internet measurement practitioners at RIPE NCC
- Honest about platform limitations: the article acknowledges that RIPE NCC cannot guarantee ethical behavior by all users

**Weaknesses**:
- Blog post format: not peer-reviewed; no formal analysis of how often ethical violations occur or are detected
- Advisory only: the guidelines are recommendations, not requirements, and enforcement is reactive
- No coverage of data privacy: the article focuses on probe host risk but does not address the privacy implications for the network endpoints (domains/servers) being measured

**Links to other papers**:
- Bortzmeyer (RIPE Atlas DNS Tutorial): explicitly mentions ethical considerations as part of measurement best practice — consistent with this article's framing
- Holterbach et al. 2015 (RIPE Atlas interference): demonstrates how RIPE Atlas measurements can produce unintended side effects (routing interference) — a different dimension of measurement ethics
- Nosyk et al. 2024 (RIPE Atlas DITL): provides operational context showing 12,900 probe hosts whose volunteer participation must be respected

**Open questions**:
- Has RIPE NCC formalized an ethics review process since 2016, given the increased scale and sensitivity of measurements now possible with 12,900 probes?
- How should the ethical framework be adapted for measurements targeting DNS censorship — where the research value is highest but probe host risk is also highest?

### Key Quotes

> "Spend some time thinking about whether the volunteers will be OK with the traffic you generate from their Internet connection."

> "The RIPE NCC may terminate your access to RIPE Atlas when your research creates complaints about unethical behaviour."

> "RIPE NCC insisted on risk-free search terms such as 'cat' and 'dog'."

> "Researchers bring essential perspectives to public discourse — and bear corresponding responsibility."

---

## Use in Thesis

**Relevant sections**:
- Section 4 (Methodology — ethical considerations): Primary citation for justifying our ethical design choices in the RIPE Atlas measurement campaign; cite alongside Menlo Report
- Section 2.4 (RIPE Atlas platform): Mention HTTP measurement restrictions and the volunteer nature of probe hosting as constraints that shape what measurements are ethically permissible

**Points to develop**:
- Explicitly state that our domain corpus (Tranco top list) was chosen to include only popular, publicly accessible domains and excludes politically sensitive, censored, or jurisdiction-restricted content — a deliberate ethical choice grounded in the principles articulated in this article
- Note that our measurements generate only standard DNS queries (A, AAAA, NS record types) and do not expose probe hosts to legal risk, consistent with RIPE NCC acceptable use guidelines

**Cross-references**:
- Fiche Bortzmeyer (DNS tutorial): ethical measurement section
- Fiche Holterbach 2015: unintended measurement effects on third parties
- Fiche Nosyk 2024: operational scale — the 12,900 volunteer probe hosts whose rights this article protects

---

**Tags**: #ethics #ripe-atlas #measurement-responsibility #menlo-report #censorship #volunteer-probes #IRB #methodology
**Status**: [X] Read / [X] Filed
