# Reading Note - Domain Names: Implementation and Specification (RFC 1035)

**Bibliographic Reference**:
Mockapetris, P. (1987). *Domain Names - Implementation and Specification*. Internet Engineering Task Force (IETF), Request for Comments: 1035, STD 13. https://www.rfc-editor.org/rfc/rfc1035 — DOI: 10.17487/RFC1035

**Theme**:
RFC 1035 is the companion implementation specification to RFC 1034. It defines the DNS wire format (message structure, header flags, question/answer/authority/additional sections), the complete set of standard resource record types (A, NS, CNAME, SOA, MX, PTR, TXT, etc.), transport rules (UDP/TCP), and master file format. Together with RFC 1034, it forms STD 13, the core DNS standard.

**Relevance to thesis**:
RFC 1035 defines the exact binary format of the DNS queries and responses that RIPE Atlas probes send and receive. Understanding the message structure — particularly the header flags (QR, AA, RD, RA, RCODE), the question and answer sections, and the RR wire format — is necessary for correctly interpreting raw RIPE Atlas DNS measurement results. The RR types defined here (A, AAAA via RFC 3596, NS, CNAME) are the primary objects of measurement in this thesis.

---

## Reading Context

**Date**: 23 March 2026
**Thesis sections**:
- Section 2.1 (DNS protocol fundamentals)
- Section 3 (Methodology — query types, response parsing, validation filters)
- Appendix (Avro schema for DNS measurement records)

---

## Article Content

### Research Objective(s)

RFC 1035 provides the implementation-level specification needed to build interoperable DNS software. Its goals are:
1. Define an unambiguous wire format for DNS messages exchanged between resolvers and nameservers.
2. Specify the standard resource record types and their RDATA formats.
3. Specify transport behaviour (UDP preference, TCP fallback, message size limits).
4. Define the master file format for zone data.

### Background

RFC 1035 assumes familiarity with the concepts of RFC 1034. It supersedes the earlier RFC 882/883 pair. The wire format was designed for efficiency on the low-bandwidth networks of 1987: name compression reduces message size by replacing repeated domain name labels with back-references.

### Methodology

- **Type**: Protocol specification (Standards Track, STD 13)
- **Tools**: N/A
- **Scale**: Internet-wide
- **Data**: N/A

### Main Results

1. **Message format**: A DNS message has five sections:
   - *Header*: 12 bytes fixed. Contains ID (query/response matching), QR (query/response bit), OPCODE, AA (authoritative answer), TC (truncated), RD (recursion desired), RA (recursion available), RCODE (response code: NOERROR=0, FORMERR=1, SERVFAIL=2, NXDOMAIN=3, NOTIMP=4, REFUSED=5).
   - *Question*: QNAME + QTYPE + QCLASS.
   - *Answer*: RRs directly answering the question.
   - *Authority*: NS records for the zone.
   - *Additional*: Glue records and supplementary data.

2. **Standard RR types** (RDATA formats defined):
   - **A** (type 1): 32-bit IPv4 address
   - **NS** (type 2): nameserver delegation — authoritative nameserver for a zone
   - **CNAME** (type 5): canonical name alias — redirects to another name
   - **SOA** (type 6): start of authority — zone metadata (serial, refresh, retry, expire, minimum TTL)
   - **PTR** (type 12): reverse DNS pointer
   - **MX** (type 15): mail exchanger with preference value
   - **TXT** (type 16): free-form text strings

3. **Transport**: DNS uses UDP port 53 by default, with a 512-byte message size limit (before EDNS0). If the response is truncated (TC bit set), the client SHOULD retry over TCP port 53. TCP is also mandatory for zone transfers (AXFR).

4. **Name compression**: A name in a message may be replaced by a 2-byte pointer (high bits 11) to an earlier occurrence in the same message. This significantly reduces message size for responses with multiple RRs sharing domain name components.

5. **Size limits** (original, pre-EDNS0):
   - Labels: max 63 octets
   - Names: max 255 octets
   - UDP messages: max 512 octets
   - TTL: 32-bit unsigned integer (seconds)

6. **RCODE semantics** relevant to measurement:
   - NOERROR (0): query answered successfully
   - NXDOMAIN (3): domain does not exist — key signal for domain liveness
   - SERVFAIL (2): server failure — indicates resolver or delegation chain error
   - REFUSED (5): server refuses to answer — indicates access control

### Authors' Conclusion

RFC 1035 provides a complete and self-consistent specification sufficient to implement interoperable DNS software. The wire format has remained stable for nearly 40 years; extensions (EDNS0 via RFC 2671/6891, DNSSEC via RFC 4033-4035, AAAA via RFC 3596) use the defined extension mechanisms without breaking the core format.

---

## Personal Analysis

### Key Takeaways for the Thesis

**Key concepts to reuse**:
- **Header flags as measurement signals**: AA bit distinguishes authoritative from cached answers; RD/RA bits indicate whether recursion was requested/available; RCODE indicates query outcome
- **RCODE classification**: our validation filter maps RCODE values to result categories (NOERROR → valid; NXDOMAIN → domain inactive; SERVFAIL/REFUSED → infrastructure error)
- **CNAME chains**: CDN-served domains often return CNAME records pointing to CDN-managed names; measurement must follow chains to reach final A records
- **TC bit**: if a probe receives a truncated UDP response, RIPE Atlas may or may not retry over TCP — relevant for interpreting missing or incomplete answers

**Applicable methods**:
- Parsing RIPE Atlas DNS result JSON: fields map directly to RFC 1035 message sections (answers array, authority array, additional array, header flags)
- Filtering by RCODE: SERVFAIL and REFUSED responses excluded from geographic analysis; NXDOMAIN used for domain liveness monitoring

**Important statistics**:
- Original UDP message size limit: 512 bytes (extended to 4096 by EDNS0)
- DNS port: UDP/TCP 53
- Standard RCODE values: 0 (NOERROR), 1 (FORMERR), 2 (SERVFAIL), 3 (NXDOMAIN), 4 (NOTIMP), 5 (REFUSED)

**Identified limitations (gaps to fill)**:
- 512-byte UDP limit predates large DNSSEC responses; EDNS0 (RFC 6891) is required in practice
- AAAA records (IPv6) not defined here — added by RFC 3596
- No treatment of anycast, CDN routing, or geographic diversity — the entire subject of this thesis

### Personal Critique

**Strengths**:
- Precise binary-level specification — no ambiguity in message parsing
- Name compression is elegant and effective
- RCODE design has proven sufficient for 40 years with only minor extensions

**Weaknesses**:
- 512-byte UDP limit was a serious constraint before EDNS0 (1999)
- No authentication mechanism — DNSSEC required a full extension (RFC 4033-4035)
- Master file format is informal and implementation-divergent in practice

**Links to other papers**:
- RFC 1034 (Mockapetris, 1987) — conceptual companion; must be read together
- RFC 7871 (Contavalli et al., 2016) — EDNS0 OPT record used by ECS extends the additional section defined here
- Holterbach et al. (2015) — interference affects timing of the UDP exchanges defined here
- Bortzmeyer tutorial (n.d.) — practical RIPE Atlas DNS queries use RFC 1035 message format

### Key Quotes

> "The domain system is a mixture of functions and data types which are an official protocol and functions and data types which are still experimental."

> "UDP is preferred over TCP because it is faster; the amount of data returned in a response is small."

---

## Use in Thesis

**Relevant sections**:
- Section 2.1: DNS wire format, RR types (A, NS, CNAME, SOA, MX), RCODE semantics
- Section 3 (Methodology): query design (QTYPE=A/AAAA/NS), response parsing, RCODE-based validation filters
- Appendix (Avro schema): field names and types derived from RFC 1035 message structure (rcode, answer_ips, answer_ttl, etc.)

**Points to develop**:
- RCODE distribution as a data quality metric across the probe set
- CNAME chain length as an indicator of CDN redirection depth

**Cross-references**:
- `rfc1034_domain_concepts.md` — namespace model underlying the wire format
- `rfc7871_edns_client_subnet.md` — EDNS0 OPT record extends RFC 1035 messages
- `bortzmeyer_dns_measurements_atlas_tutorial.md` — practical query construction using RFC 1035 types

---

**Tags**: #DNS #RFC #wire-format #RCODE #RR-types #A-record #CNAME #UDP #TCP #foundational
**Status**: [X] Read / [X] Filed
