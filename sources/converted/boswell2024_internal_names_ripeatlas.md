RIPEn at Home – Surveying Internal Domain Names
               using RIPE Atlas
                                Elizabeth Boswell                                       Colin Perkins
                               University of Glasgow                                University of Glasgow



   Abstract—Internal domain names are domain names that are             in October 2013 [7]. As of November 2023, there are 1241
resolved locally and not by the global DNS. Name collisions occur       new gTLDs [8]. There was a concern that if common internal
if an internal name is resolved in the global DNS, e.g. if queries      TLDs are added to the DNS, these names could resolve in two
are accidentally sent to a public resolver. This can lead to security
issues. While previous studies of name collisions used passive          different ways depending on where the query is sent. Studies
measurement data, we use active measurements on RIPE Atlas to           from the time [1] [9] [10], which find a large variety of internal
survey the use of internal names in home networks. We discover          names, use root server data and other passive measurement
3092 names, used by 4305 probes, of which 34.51% are at risk            sources. We perform active client-side measurements, as they
of collision if their top-level domain is delegated.                    can capture internal names that don’t frequently appear in
                        I. Introduction                                 root server logs because the queries are usually answered by
                                                                        the local resolver. We focus on internal names used by home
   Many home networks let users refer to the gateway using an           gateways, so we use the RIPE Atlas measurement network [11],
internal domain name that the gateway resolves to its own local         which has many vantage points in home networks. We also
address [1]. These internal names often use top-level domains           provide an update on the usage of internal names, over 10
(TLDs) that don’t exist in the public DNS. If the TLD doesn’t           years after the introduction of new gTLDs.
exist, any query for the name that is inadvertently sent to the            We structure the remainder of this paper as follows. In
public DNS will fail [2] [3]. However, this practice can cause          section II we present background information on the DNS,
issues if the TLD is delegated, as a recent case has shown.             name collisions, and RIPE Atlas. Our method for detecting
   AVM FRITZ!Box home gateways, one of the most popular                 internal names on RIPE Atlas is described in section III, the
home gateways in Germany, use internal names under the                  results are discussed in section IV. Related work is discussed
box TLD (e.g. fritz.box) for the gateway’s configuration                in section V and we conclude in section VI.
page and other features. The box TLD was added to the DNS
root in August 2023 [4], and advertised to the general public
                                                                                               II. Background
on 18 January 2024 [5] [6]. AVM did not appear to register
fritz.box and other related names, and for several weeks in                The Domain Name System (DNS) [12] is a globally
January and February 2024, several such names were owned by             distributed system mapping domain names to IP addresses
likely domain speculators. This is a security risk, as queries for      and other data. It is organised hierarchically, different parts
fritz.box could accidentally be sent to the public DNS,                 of the namespace are controlled by different entities. The
e.g. when using a public resolver. The public fritz.box                 root of the DNS is managed by the Internet Corporation for
domain could spoof the home gateway, e.g. to steal login                Assigned Names and Numbers (ICANN) [13] through the
credentials, misguide users to install malicious software, or           Internet Assigned Numbers Authority (IANA) [14]. Absent any
otherwise interfere with the home network.                              caching, regular DNS queries are first sent to a DNS root server,
   There is no comprehensive survey of which internal names             which refers the DNS resolver to the nameserver responsible
are used by home gateways, and which of these names are                 for the name’s TLD (e.g. com). The TLD nameserver refers
vulnerable to name collision. In this paper we use RIPE Atlas           the resolver to a nameserver lower in the hierarchy, and so on,
to survey internal names used in the probes’ local networks. We         until a nameserver responds with the queried data.
develop a way to find internal names, and then determine which             Some networks use internal domain names to refer to local
names are vulnerable to name collision, and which names could           devices such as the gateway. Instead of being sent to the DNS,
be vulnerable if the TLD is delegated.                                  a local nameserver responds to queries for these names [1].
   We find 3092 internal names used by 4305 RIPE Atlas probes.             The use of internal names can lead to name collisions,
Of these, 2.13% are currently vulnerable to collision (e.g.             where an internal name also exists in the global DNS and
unregistered subdomains of existing TLDs), and 34.51% use               is inadvertently resolved in the global DNS [15]. If the
an undelegated TLD and could be vulnerable if it is delegated.          two responses differ, e.g. if example.net is resolved to
   Internal domain names were studied extensively due to the            192.168.1.1 locally but to 203.0.113.2 by the global DNS,
introduction of new generic top-level domains (gTLDs), starting         and if the internal and global name are not controlled by the
978-3-903176-64-5 ©2024 IFIP                                            same entity, the global name can spoof the local resource [16].
   RIPE Atlas [11] is a global Internet measurement network,                                                     Table I
consisting of ∼12,000 probes, which are custom measurement                              Results of the internal name detection (GW = Gateway).
devices or virtual machines located in various networks. Probes
                                                                                               Probe      rDNS        GW         %           Names
are used as vantage points for measurements such as traceroute                                 GW         resp.       profile    of probes   found
or DNS queries. The large number of probes, many of which                                      found      probes      probes     with GW
are located in home networks, make it a suitable choice for                        TR GW       7441       2573        63         35.43%      1344
client-side measurements of internal names.                                        Res. GW     6045       3872        100        65.71%      2574

                           III. Methodology
                                                                                  response is an internal name4.
                              Detect gateway address;
                    Send query for version.bind and hostname.bind
                                                                                  4. Gateway profile fingerprinting: If a probe didn’t receive a
                                                                                  response to its rDNS query, we gather the names from rDNS
                   response
  record probe,     received Send rDNS query for gateway   could not              responses received by probes with the same gateway profile.
gateway address,                                         detect internal
      name                             address                                    The probe sends A record queries for all such names that were
                                                             name
                                     no response
              response                                                            received by two different probes. If the response contains a
               received query rDNS responses from probes no response              local address and is different from the response from the global
                              with same gateway profile
                                                                                  DNS, the name is an internal name. This step doesn’t discover
                                                                                  any new names, but it finds more probes using internal names.
             Figure 1. Procedure for detecting internal names.
                                                                                                             IV. Results
   We don’t know beforehand which internal names a RIPE                           A. Internal name detection
Atlas probe uses, and the large number of possible names makes
                                                                                     We performed the internal name detection on all available
it unfeasible to exhaustively query them. Instead, we detect
                                                                                  IPv4 probes in early 2024. The results are shown in Table I.
internal names using traceroutes and DNS based fingerprinting.
                                                                                  We found gateway addresses for 7441 probes using traceroute
Note that we couldn’t detect multicast DNS names [17], as
                                                                                  (method a) and 6045 probes using DNS (method b). However,
RIPE Atlas doesn’t support mDNS queries.
                                                                                  only 2573 probes received a response for their rDNS query for
   We use CHAOS TXT queries for hostname.bind and
                                                                                  the traceroute gateway address, while 3872 received a response
version.bind for gateway fingerprinting. Some BIND re-
                                                                                  for the local resolver address. Note that the gateway IP addresses
solvers respond to these queries with their hostname and version
                                                                                  often differ: none of the addresses match for 2104/5021 probes
of BIND [18]. Many resolvers don’t respond, but their response
                                                                                  for which we could determine a gateway address with both
codes (e.g. NXDOMAIN, SERVFAIL) can differ. Two gateways
                                                                                  methods. The gateway profile fingerprinting step added another
with the same responses to the BIND queries and the same
                                                                                  102 probes. In total, we found 3092 internal names, used by
local address, determined using the same method (see below),
                                                                                  4305 probes (50.86% of probes tested).
have the same gateway profile. We assume they are more likely
                                                                                     Figure 2 shows the top 10 internal full, second+top-level and
to be the same gateway model and use the same internal name.
                                                                                  top-level domains, by number of probes using them. All top 10
   Our method, as shown in Figure 1, is:
                                                                                  full domain names appear to be related to the FRITZ!Box. This
1. Detect gateway address: Home gateways often integrate a
                                                                                  is likely due to its popularity in Europe (where many RIPE
NAT44, so we assume the gateway is a NAT44 or behind it1.
                                                                                  Atlas probes are located), and because a single rDNS query to
We estimate the local address of the probe’s home gateway (if
                                                                                  a FRITZ!Box often returns multiple names. Five of the top 10
present). We do this in two different ways, so steps 2-4 are
                                                                                  second+top-level domains are also likely FRITZ!Box-related,
performed twice. The two methods are:
                                                                                  alongside other names such as pi.hole (PiHole ad blocker).
   a) Traceroute We assume the gateway is the last private
                                                                                     The most common TLDs are box, lan and nas. In fifth place
address2 in an IPv4 traceroute starting at the probe3.
                                                                                  is home, which was found to be used internally so frequently
   b) Local resolver We assume the gateway has the same
                                                                                  [1] that ICANN has indefinitely delayed its delegation due
address as the probe’s DNS resolver, provided it has a private,
                                                                                  to the collision risk [21]. Some common public TLDs (com,
non-loopback address.
                                                                                  net, org) are also used. This is partly because some RIPE
The next steps use the probes with gateways found in step 1.
                                                                                  Atlas users use their own domain name internally. In fact, 1146
2. BIND queries: Each probe sends CHAOS TXT queries for
                                                                                  names (37.06%) only occur once and might be unique to the
version.bind and hostname.bind to its default resolver(s).
                                                                                  probe’s network. This is likely more common on RIPE Atlas
3. rDNS queries: Each probe sends a reverse DNS (rDNS)
                                                                                  than average, due to its more technical user base.
query for its gateway address to its default resolver(s). Any
                                                                                  B. Current Collision Risk
   1this will also detect non-residential NAT gateways, but more fine-grained
detection of home gateways is out of scope for this work.                           1766 names (57.12%) have a TLD in the public DNS. We
   2defined as being in the IANA Special-Purpose Address Registry [19] [20]       check how many of these names are at risk of name collision,
   3Probes could be behind a carrier-grade NAT, so a better choice might be the
last address in the probes’ private address range, but this could be inaccurate     4We don’t verify that the response comes from the gateway - this is
as many probes’ local networks appear to use several private prefixes.            challenging because some gateways appear to spoof the source address.
                                    Full Domains                                        Second + Top Level Domains                           Top Level Domains
            fritz.box.                                                 fritz.box                                              box
         myfritz.box.                                              myfritz.box                                                lan
      www.fritz.box.                                                 wpad.box                                                 nas
 www.myfritz.box.                                                      fritz.nas                                             hole
     wpad.fritz.box.                                             fritz-nas.box                                             home
           wpad.box.                                                     pi.hole                                             com
             fritz.nas.                                              router.lan                                               net
 fritz-nas.fritz.box.                                      unifi.localdomain                                                local
      www.fritz.nas.                                           livebox.home                                          localdomain
       fritz-nas.box.                                            OpenWrt.lan                                                  org
                          0   100 200 300 400 500 600                              0   100 200 300 400 500 600                      0   100 200 300 400 500 600 700
                                      Probes                                                    Probes                                            Probes

                                                   Figure 2. Top 10 internal full, second level and top-level domains.



i.e. are unregistered but registrable. We only consider potential           The TLDs lan, home, local, localdomain, router and
name collisions and not ongoing name collisions: it is difficult internal do appear in the results of some or all aforemen-
to determine whether the internal and global name are owned by tioned studies [2] [3] [1] [25], suggesting more persistent
the same party (which would be an intentional name collision). use. The 26 names using internal and the 96 names using
   Subdomains of public suffixes [22] [23] are registrable by in- home are at lower risk of collision; ICANN has proposed
dividuals. We thus extract the subdomain of the public suffix of reserving internal for internal use [26], and indefinitely
the name and check if it resolves by querying for an SOA record. delayed delegation of home [21]. However, home isn’t a special-
We don’t check if the full domain name resolves because a use domain name [24] designated for internal use. Special-use
domain owner might use a subdomain internally, e.g. the owner names aren’t widely used: only 24 probes use the special-use
of example.co.uk might use gw.example.co.uk internally alternative to home (home.arpa [27]), and only one top 10
without adding it to the DNS. This name wouldn’t resolve, TLD (local, for multicast DNS [17]) is a special-use name.
but can’t be registered; only the domain owner can add new
                                                                                                 V. Related Work
subdomains. In this case we would check if example.co.uk
(subdomain of the public suffix co.uk) resolves.                            Some past studies of root server and resolver logs discuss
   Out of the 1766 names with a public TLD, 1687 (95.53%)                queries  for internal names. ICANN commissioned [1] [10] to
have a resolvable public suffix subdomain. 66 names (3.74%,              determine   the collision risk of new gTLDs. Interisle Consulting
2.13% of all names) don’t resolve and could be registered. We            Group   [1]  find a "substantial" collision potential, especially for
couldn’t assess the collision risk for the remaining 13 names.           home   and  corp.  JAS Global Advisors [10] present a "controlled
                                                                         interruption" approach for safe delegation. Verisign [9] analyse
              lan                                                        which proposed new gTLDs are used internally, and quantify
              nas                                                        the risk of delegation. These studies focus on the collision risk
             hole
           home                                                          of new gTLDs; to the best of our knowledge, ours is the first
            local
TLD




   localdomain                                                           study of the collision risk of names used by home gateways.
          router
                ip                                      Number of Probes Other studies of root server [2] [3] and resolver logs [25] also
                 1                                      Unique Names
        internal                                                         find queries for invalid TLDs, including TLDs found by us.
                   0      100       200        300      400         500     Chen et al. [16] evaluate security risks of client-side name
                                                                         collisions by searching root server logs for common internal
                     Figure 3. Top 10 undelegated TLDs.                  domain names, and analysing the services using these names.
                                                                            Our study involves a form of gateway fingerprinting – other
                                                                         studies of home gateway fingerprinting use web interfaces
C. Undelegated TLDs
                                                                         [28] or port scanning [29]. Randall et al. [30] use CHAOS TXT
   1326 names (42.88%) use a TLD that’s not in the public queries to detect DNS interception by home gateways.
DNS. Of these internal names, 1067 (34.51% of all names)
are not subdomains of special-use domain names [24], and are                                      VI. Conclusions
thus at risk of collision if their TLD is added to the DNS.                 We detect internal domain names used by RIPE Atlas probes
   Figure 3 shows the top 10 non-delegated TLDs (including and determine their name collision risk. We discover 3092
special-use names), by number of probes that use them. After names, used by 4305 probes. Of these, 66 names are at risk
lan, the most common TLD is nas, mostly from fritz.nas of collision, 1067 names could be at risk if their TLD is
and www.fritz.nas. It is likely related to the Network delegated. Individuals hosting a RIPE Atlas probe are likely
Attached Storage feature of the FRITZ!Box. This TLD doesn’t more technical than the average Internet user. It is thus unclear
appear in the top results of past studies of invalid TLDs reaching how representative our results are of internal names in other
root servers [2] [3] [1] or recursive resolvers [25]. This could home networks. However, the large number of names with
be because these studies are over 10 years old, because RIPE undelegated TLDs shows that name collisions in home networks
Atlas has overproportionately many FRITZ!Boxes, or because warrant further study. In future work, we will increase the
these queries don’t often reach the root servers. Regardless, this number of probes found through gateway fingerprinting, and
is another potential name collision for FRITZ!Box gateways. explore ways to achieve more representative results.
                              References                                       [18] Internet Systems Consortium, “BIND 9 Configuration Reference,”
                                                                                    https://bind9.readthedocs.io/en/latest/reference.html#built-in-server-
 [1] Interisle Consulting Group, “Name Collision in the DNS,” Name Collision        information-zones, Apr. 2024.
     Study Report Version 1.5, Aug. 2013.                                      [19] IANA,       “IANA      IPv4     Special-Purpose    Address      Registry,”
 [2] D. Wessels and M. Fomenkov, “Wow, That’s a Lot of Packets,” in Passive         https://www.iana.org/assignments/iana-ipv4-special-registry/iana-
     and Active Network Measurement Workshop (PAM), Apr. 2003.                      ipv4-special-registry.xhtml.
 [3] S. Castro, D. Wessels, M. Fomenkov, and K. Claffy, “A day at the root     [20] ——,        “IANA      IPv6     Special-Purpose     Address      Registry,”
     of the internet,” ACM SIGCOMM Computer Communication Review,                   https://www.iana.org/assignments/iana-ipv6-special-registry/iana-
     vol. 38, no. 5, pp. 41–46, Sep. 2008.                                          ipv6-special-registry.xhtml.
 [4] “Box | ICANN New gTLDs,” https://newgtlds.icann.org/en/program-           [21] ICANN, “Approved Board Resolutions | Regular Meeting of the
     status/sunrise-claims-periods/box.                                             ICANN         Board,”     https://www.icann.org/en/board-activities-and-
 [5] “Introducing .Box – A New Era in Domain Names Powered by 3DNS,”                meetings/materials/approved-board-resolutions-regular-meeting-of-the-
     https://3dns.box/blog/posts/introducing-box-tld/.                              icann-board-04-02-2018-en#2.c.
 [6] Chainwire, “Introducing .box – The World’s First Blockchain Native,       [22] “Public Suffix List,” https://publicsuffix.org/.
     DNS Routable Domain,” https://decrypt.co/213372/introducing-box-the-      [23] S. McQuistin, P. Snyder, C. Perkins, H. Haddadi, and G. Tyson, “A First
     worlds-first-blockchain-native-dns-routable-domain, Jan. 2024.                 Look at the Privacy Harms of the Public Suffix List,” in Proceedings
 [7] ICANN, “About the Program | ICANN New gTLDs,”                                  of the 2023 ACM on Internet Measurement Conference, ser. IMC ’23.
     https://newgtlds.icann.org/en/about/program.                                   New York, NY, USA: Association for Computing Machinery, Oct. 2023,
 [8] ——,        “Program      Statistics   |    ICANN         New   gTLDs,”         pp. 383–390.
     https://newgtlds.icann.org/en/program-status/statistics.                  [24] IANA,              “Special-Use               Domain             Names,”
 [9] Verisign Labs, “New gTLD Security, Stability, Resiliency Update:               https://www.iana.org/assignments/special-use-domain-names/special-
     Exploratory Consumer Impact Analysis,” Verisign Labs Technical Report          use-domain-names.xhtml.
     1130008 Version 1.1, Aug. 2013.                                           [25] H. Gao, V. Yegneswaran, Y. Chen, P. Porras, S. Ghosh, J. Jiang, and
[10] JAS Global Advisors, “Mitigating the Risk of DNS Namespace Collisions          H. Duan, “An empirical reexamination of global DNS behavior,” in
     - A Study on Namespace Collisions in the Global Internet DNS                   Proceedings of the ACM SIGCOMM 2013 Conference on SIGCOMM,
     Namespace and a Framework for Risk Mitigation,” Final Report, Oct.             ser. SIGCOMM ’13. New York, NY, USA: Association for Computing
     2015.                                                                          Machinery, Aug. 2013, pp. 267–278.
[11] “RIPE Atlas,” https://www.ripe.net/analyse/internet-measurements/atlas.   [26] “ICANN Seeks Feedback on Proposed Top-Level Domain String for
[12] P. Mockapetris, “Domain names - concepts and facilities,” Internet             Private Use,” https://www.icann.org/en/announcements/details/icann-
     Engineering Task Force, Request for Comments RFC 1034, Nov. 1987.              seeks-feedback-on-proposed-top-level-domain-string-for-private-use-24-
[13] ICANN, “Acronyms and Terms,” https://www.icann.org/en/icann-                   01-2024-en.
     acronyms-and-terms/internet-assigned-numbers-authority-en.                [27] P. Pfister and T. Lemon, “Special-Use Domain ’home.arpa.’,” Internet
[14] “Root Zone Management,” https://www.iana.org/domains/root.                     Engineering Task Force, Request for Comments RFC 8375, May 2018.
[15] ICANN, “Name Collision Occurrence Management Framework,” Jul.             [28] M. Niemietz and J. Schwenk, “Owning Your Home Network: Router
     2014.                                                                          Security Revisited,” in Web 2.0 Security and Privacy Workshop, San
[16] Q. A. Chen, M. Thomas, E. Osterweil, Y. Cao, J. You, and Z. M. Mao,            Jose, CA, May 2015.
     “Client-side Name Collision Vulnerability in the New gTLD Era: A          [29] T. Papastergiou, R. Perdisci, and M. Antonakakis, “Returning to Port:
     Systematic Study,” in Proceedings of the 2017 ACM SIGSAC Conference            Efficient Detection of Home Router Devices,” in 2022 IEEE Conference
     on Computer and Communications Security, ser. CCS ’17. New York,               on Communications and Network Security (CNS), Oct. 2022, pp. 172–180.
     NY, USA: Association for Computing Machinery, Oct. 2017, pp. 941–         [30] A. Randall, E. Liu, R. Padmanabhan, G. Akiwate, G. M. Voelker,
     956.                                                                           S. Savage, and A. Schulman, “Home is where the hĳacking is:
[17] S. Cheshire and M. Krochmal, “Multicast DNS,” Internet Engineering             Understanding DNS interception by residential routers,” in Proceedings
     Task Force, Request for Comments RFC 6762, Feb. 2013.                          of the 21st ACM Internet Measurement Conference, ser. IMC ’21. New
                                                                                    York, NY, USA: Association for Computing Machinery, Nov. 2021, pp.
                                                                                    390–397.
