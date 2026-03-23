                                                                                                                              PDF Download
                                                                                                                              3452296.3472891.pdf
                                                                                                                              21 March 2026
                                                                                                                              Total Citations: 34
                                                                                                                              Total Downloads: 1695
    .
    .
        Latest updates: hps://dl.acm.org/doi/10.1145/3452296.3472891




                                                                                                                              .
                                                                                                                              .
                                                                                                                    Published: 09 August 2021
        .
        .
                                                                                                                    .
    RESEARCH-ARTICLE




                                                                                                                    .
                                                                                                                    Citation in BibTeX format
    Anycast In context: a tale of two systems




                                                                                                                    .
                                                                                                                    .
                                                                                                                    SIGCOMM '21: ACM SIGCOMM 2021
                                                                                                                    Conference
    THOMAS KOCH, Columbia University, New York, NY, United States                                                   August 23 - 27, 2021
    .
                                                                                                                    Virtual Event, USA
    ETHAN KATZ-BASSETT, Columbia University, New York, NY, United States




                                                                                                                    .
                                                                                                                    .
                                                                                                                    Conference Sponsors:
    .
    JOHN HEIDEMANN, Information Sciences Institute, Marina del Rey, CA, United States                               SIGCOMM
    .
    MATT CALDER, Columbia University, New York, NY, United States
    .
    CALVIN ARDI
    .
    KE LI, Columbia University, New York, NY, United States
    .
    .
    .
    Open Access Support provided by:
    .
    Columbia University
    .
    Information Sciences Institute
    .
                                                                        SIGCOMM '21: Proceedings of the 2021 ACM SIGCOMM 2021 Conference (August 2021)
                                                                                                                    hps://doi.org/10.1145/3452296.3472891
                                                                                                                                       ISBN: 9781450383837
.
                                Anycast in Context: A Tale of Two Systems
                    Thomas Koch                                                           Ke Li                                         Calvin Ardi
                 Columbia University                                           Columbia University                                         USC/ISI

               Ethan Katz-Bassett                                                   Matt Calder                                     John Heidemann
                 Columbia University                                   Microsoft/Columbia University                                       USC/ISI

ABSTRACT                                                                                            31, 39, 65] and Content Delivery Network (CDN) [16, 21, 30, 65, 75]
Anycast is used to serve content including web pages and DNS, and                                   deployments today, in part because of its ability to improve latency
anycast deployments are growing. However, prior work examining                                      to clients and decrease load on each anycast server [45, 55, 64].
root DNS suggests anycast deployments incur significant inflation,                                     However, studies have argued that anycast often provides sub-
with users often routed to suboptimal sites. We reassess anycast                                    optimal performance compared to the lowest latency one could
performance, first extending prior analysis on inflation in the root                                achieve given deployed sites [51, 54, 67]. Notably, the SIGCOMM
DNS. We show that inflation is very common in root DNS, affecting                                   2018 paper "Internet Anycast: Performance, Problems, & Potential"
more than 95% of users. However, we then show root DNS latency                                      has drawn attention to the fact that anycast can inflate latency by
hardly matters to users because caching is so effective. These find-                                hundreds of milliseconds [51], leaving readers of the paper with
ings lead us to question: is inflation inherent to anycast, or can                                  a poor impression of anycast. Conversely, other work has shown
inflation be limited when it matters? To answer this question, we                                   inflation is quite low in Microsoft’s anycast CDN [16] and Google
consider Microsoft’s anycast CDN serving latency-sensitive con-                                     Public DNS [50], but used different coverage, metrics, and method-
tent. Here, latency matters orders of magnitude more than for root                                  ology, so it is difficult to directly compare results. Perhaps because
DNS. Perhaps because of this need, only 35% of CDN users experi-                                    of the very different takeaways of these studies, we have found that
ence any inflation, and the amount they experience is smaller than                                  some experts in the community have negative opinions of anycast.
for root DNS. We show that CDN anycast latency has little inflation                                 In particular, it seems surprising that anycast continues to see more
due to extensive peering and engineering. These results suggest                                     adoption and growth in production systems – why continue to use
prior claims of anycast inefficiency reflect experiments on a sin-                                  anycast if it causes inflation?
gle application rather than anycast’s technical potential, and they                                    To understand the impact of anycast inefficiency, and its wide
demonstrate the importance of context when measuring system                                         use in spite of inflation, we step back and evaluate anycast as a com-
performance.                                                                                        ponent of actual applications/services. User-affecting performance
                                                                                                    depends on the anycast deployment, how anycast is used within
CCS CONCEPTS                                                                                        the service, and how users interact with the service. To see these
                                                                                                    effects, we consider anycast’s role within two real-world systems:
• Networks → Network performance analysis.
                                                                                                    the root DNS and Microsoft’s anycast CDN serving web content.
                                                                                                    These applications have distinct goals, they are key components
KEYWORDS                                                                                            of the Internet, and they are two of the dominant, most studied
Anycast, root DNS, routing, latency, CDN.                                                           anycast use cases.
ACM Reference Format:                                                                                  We analyze root DNS [39] packet traces which are available
Thomas Koch, Ke Li, Calvin Ardi, Ethan Katz-Bassett, Matt Calder, and John                          via DITL [26] and which are featured in existing anycast studies
Heidemann. 2021. Anycast in Context: A Tale of Two Systems. In ACM                                  [23, 51, 54, 58, 69], with increased coverage compared to prior work.
SIGCOMM 2021 Conference (SIGCOMM ’21), August 23–27, 2021, Virtual                                  The 13 root letters operate independently with diverse deployment
Event, USA. ACM, New York, NY, USA, 20 pages. https://doi.org/10.1145/                              strategies, enabling the study of different anycast deployments
3452296.3472891                                                                                     providing the same service. We analyze two days of unsampled
                                                                                                    packet captures from nearly all root DNS letters, consisting of tens
1     INTRODUCTION                                                                                  of billions of queries from millions of recursive resolvers querying
IP anycast is an approach to routing in which geographically diverse                                on behalf of all users worldwide, giving us broad coverage.
servers known as anycast sites all use the same IP address. It is                                      We also examine Microsoft’s CDN using the same methodol-
used by a number of operational Domain Name System (DNS) [1, 7,                                     ogy we use for the root DNS so we can directly compare results.
                                                                                                    Microsoft’s CDN configures subsets of sites into multiple anycast
Permission to make digital or hard copies of all or part of this work for personal or               “rings” of different sizes, providing deployment diversity, but all
classroom use is granted without fee provided that copies are not made or distributed
for profit or commercial advantage and that copies bear this notice and the full citation
                                                                                                    operated by one organization. We analyze global measurements
on the first page. Copyrights for components of this work owned by others than ACM                  from over a billion Microsoft users in hundreds of countries/regions,
must be honored. Abstracting with credit is permitted. To copy otherwise, or republish,             giving us a complete view of CDN performance.
to post on servers or to redistribute to lists, requires prior specific permission and/or a
fee. Request permissions from permissions@acm.org.                                                     With these measurements, we present the largest study of any-
SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA                                                 cast latency and inflation to date. We first validate and extend prior
© 2021 Association for Computing Machinery.                                                         work on inflation in anycast deployments [51]. Whereas that work
ACM ISBN 978-1-4503-8383-7/21/08. . . $15.00
https://doi.org/10.1145/3452296.3472891
                                                                                                    focused primarily on a single root letter, we analyze almost the




                                                                                              398
SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


whole root DNS. By joining root DNS captures with global-scale                 2     METHODOLOGY AND DATASETS
traces of user behavior, we find that more users than previously               We use a combination of DNS packet captures and global CDN
thought experience some inflation (on average, more than 95%), and             measurements to measure latency and inflation. Root DNS data
as many as 40% of users experience more than 100 ms of inflation               is readily available [26], while CDN data is proprietary. We sup-
to some root letters (§3). However, average inflation per query to             plement these datasets with measurements from RIPE Atlas [71].
the roots is lower than previously thought, since each recursive               We summarize our many data sets’ characteristics, strengths, and
resolver can preferentially query its best performing root letter              weaknesses in Appendix A.
– on average, only 10% of users experience more than 100 ms of
inflation.
    Do recursives have to implement preferential querying strategies
for their users so that inflation does not hurt user performance?              2.1    Root DNS
The answer is a resounding “no” – using new methodology that                   The first of the two systems we discuss, the root DNS, is a criti-
amortizes DNS queries over users who benefit from cached query                 cal part of the global DNS infrastructure. DNS is a fundamental
results, we find differences in latency and inflation among root               lookup service for the Internet, typically mapping hostnames to IP
letters are hardly perceived by users – most users interact with the           addresses [22, 56]. To resolve a name to its result, a user sends DNS
root DNS once per day (§4). Delay is minimal due to caching of                 requests to a recursive resolver (recursive). The recursive queries
root DNS records with long TTLs at recursive resolvers.                        authoritative DNS servers as it walks the DNS tree from root, to
    The inflated anycast routes to root DNS could be a result of               top-level domain (TLD), and down the tree. Recursives cache results
latency not mattering, causing root operators to not optimize for              to answer future requests according to TTLs of records. The root
it, or inflation could be inherent in anycast routing as suggested in          DNS server is provided by 13 letters [39], each with a different
prior work. To determine which is the case, we use measurements                anycast deployment with 6 to 254 anycast sites (as of July 2021),
from Microsoft’s CDN and find that, were latency to Microsoft’s                run by 12 organizations. A root DNS site can be local or global –
CDN to be hypothetically inflated as to individual root letters, it            local sites serve small geographic areas or certain ASes (controlled
would result in hundreds of milliseconds of additional latency per             by restricting the propagation of the anycast BGP announcement
page load. This increased latency would negatively affect the user’s           from the site), while global sites are globally reachable.
overall experience, especially when compared to root DNS. The                     We use three datasets: for end-users, we use long-term packet
key difference is that users incur several RTTs to Microsoft’s CDN             captures from the Information Sciences Institute (ISI) at USC,
when fetching web content, whereas users rarely wait for a query               and DNS and browser measurements from daily use of two of the
to the root DNS because of DNS caching (§5.1).                                 authors. For DNS servers, we use 48-hour packet captures at most
    With this context, we then measure actual inflation in Microsoft’s         root servers from Day in the Life of the Internet (DITL) [26].
CDN and find that inflation is kept comparatively small (§5.2), espe-             Packet captures from ISI provide a local view of root DNS queries.
cially compared to individual root letters. To explain why inflation           The recursive resolver runs BIND v9.11.14. The captures, from 2014
is so different in these deployments, we contrast AS-level connec-             to the present, reflect all traffic (incoming and outgoing) traversing
tivity and inflation between the users, Microsoft’s CDN, and roots.            port 53 of the recursive resolver. We use traces from 2018 (about
We find that Microsoft is able to control inflation through extensive          100 million queries), as they overlap temporally with our other
peering and engineering investment (§7.1), even though inefficiency            datasets. This recursive resolver received queries from hundreds
increases with larger deployments (§7.2). Through discussions with             of users on laptops, and a number of desktop and rack-mounted
operators of root DNS and CDNs, we find recent root DNS expan-                 computers of a network research group, so the results may deviate
sion has (surprisingly) been driven by a desire to reduce latency and          from a typical population. We found no measurement experiments
mitigate DDoS attacks, while CDN expansion is driven by market                 or other obvious anomalies in the period we use.
forces (§7.3).                                                                    We use the 2018 DITL captures, archived by DNS-OARC [26], to
    The comparison between performance in these two deployments                obtain a global view of root DNS use. DITL occurs annually, with
allows us to put results from prior work in perspective [16, 23, 51,           each event including data from most root servers. The 2018 DITL
69]. Even though root inflation is large, users rarely experience it,          took place 2018/04/10-12 and included 12 root letters (all except
making its impact on the average query quite small. In contrast,               G root). Traces from I root are fully anonymized, so we did not
users frequently interact with the CDN, and inflation there is small.          use them. Traces from B root are partially anonymized, but only at
These inflation results make sense, given the economic incentives              the /24 level. Our analysis does not rely on addresses more specific
of the organizations running Microsoft’s CDN and the root DNS.                 than /24, so we use all data from B root and all other roots except
While we expect these results to hold for other latency-sensitive              G and I. Although the 2018 DITL is older than the most recently
services using anycast, as they have similar economic incentives,              available, it is significantly more complete than recent DITLs; in
a key takeaway from our work is that anycast must be analyzed                  Appendix B.3 we conduct analysis on the 2020 DITL and find none
in the context of the service in which it is used (§7.3), and so we            of our main conclusions change.
cannot make definitive statements about generalizability. Hence,                  Since we aim to understand in part how root DNS latency affects
we do not refute past claims that anycast can inflate latencies, but           users, we filter queries in DITL that do not affect user latency and
we expand on these studies to show that, where it counts, anycast              queries generated by recursives about which we have no user data.
performance can be quite good.                                                 We describe this pre-processing of DITL and subsequent joining of
    This paper poses no ethical issues.                                        root query volumes with Microsoft’s CDN user population counts.




                                                                         399
                                                                                                                     SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


    Of the 51.9 billion daily queries to all roots, we discard 31 billion
queries to non-existing domain names and 2 billion PTR queries.
About 28% of non-existing domain name queries are NXDomain
hijacking detection from Chromium-based browsers [4, 34, 73], and
so involve machine startup and not browsing latency. Prior work
                                                                                                    R28
suggests the remainder are generated by other malfunctioning,                                       R47
automated software [28]. Similarly, while PTR queries have some                                     R74
                                                                                                    R95
uses (traceroutes and confirming hostnames during authentication),                                  R110
they are not part of typical user web latency. In Appendix B.1,
we find that including invalid TLD queries significantly changes                              Figure 1: Microsoft’s CDN rings and user populations. Sites in smaller
the conclusions we can draw about how users interact with the                                 rings are also in larger rings, and the legend indicates the number of
root DNS, and we provide more justification for this step. We next                            sites in that ring. We do not show some front-ends too close to each
                                                                                              other to improve readability. User populations are shown as circles,
remove queries from prefixes in private IP space [38] (7% of all
                                                                                              with the radius of the circle proportional to the number of users in
queries). Finally, we analyze only IPv4 data and exclude IPv6 traffic                         that region, demonstrating that Microsoft has deployed front-ends
(12% of queries) because we lack v6 user data.                                                in areas of user concentration.
    Sources of DNS queries in DITL are typically recursive resolvers,
so the captures alone provide no information about how many
                                                                                              are more accurate, but APNIC data is more accessible to other
DNS queries each user makes. To estimate per-user latency, we
                                                                                              researchers and so provides a useful comparison.
augment these traces with the approximate number of Microsoft
users of each recursive, gathered in 2019 (the oldest user data we
have). This user data is from Microsoft DNS data, which counts                                2.2    Microsoft’s CDN
unique IP addresses as “users”. This definition undercounts multiple                          We also analyze Microsoft’s large anycast CDN that serves web
human users that use a single IP address with Network Address                                 content to over a billion users from more than 100 sites. Traffic des-
Translation. Microsoft maps recursives to user IP addresses with an                           tined for Microsoft’s CDN enters its network at a point of presence
existing technique that instruments users to request DNS records                              (PoP) and is routed to one of the anycast sites serving the content
for domains Microsoft controls when users fetch content [17, 53].                             (front-ends). Microsoft organizes its deployment into groups of
    We join the DITL captures and Microsoft user counts by the                                sites, called rings, that conform to varying degrees of regulatory
recursive resolver /24, aggregating DITL query volumes and Mi-                                restrictions (e.g., ISO 9001, HIPAA), each with its own anycast ad-
crosoft user IP counts, each grouped by /24 prefix1 to increase the                           dress. The rings have the property that a site in a smaller ring is
amount of recursives for which we have user data. This aggregation                            also in all larger rings. Other CDNs have to work with similar reg-
is justified since many organizations use colocated servers within                            ulatory restrictions [2]. Hence, traffic from a user prefix destined
the same /24 as recursives [31, 63]. Prior work has also found that                           for Microsoft’s CDN may end up at different front-ends (depending
up to 80% of /24’s are collocated [29]. We provide additional justifi-                        on which ring the application uses), but often will ingress into the
cation for this preprocessing step in Appendix B.2, by showing all                            network at the same PoP. Users are routed to rings via anycast and
addresses in a /24 in DITL are almost always routed to the same                               fetch web content from a front-end via its anycast address. Users
anycast site. For simplicity, we henceforth refer to these /24’s as                           are always routed to the largest allowed ring given the application’s
recursives, even though each /24 may contain several recursives.                              regulatory restrictions (performance differences among rings are
We call this joined dataset of query volumes and user counts by                               not taken into account).
recursive DITL∩CDN.                                                                              Microsoft’s anycast rings provide different size anycast deploy-
    In an effort to make our results more reproducible, and as a point                        ments for study. In Figure 1 we show Microsoft’s front-ends and
of comparison, we also use public Internet population user count                              user concentrations. Rings are named according to the number of
data from APNIC to amortize root DNS queries [37] (i.e., instead                              front-ends they contain, and front-ends are labeled according to
of using proprietary Microsoft data). APNIC obtains these AS user                             the smallest ring to which they belong (or else all front-ends would
population estimates by first gathering lists of IP addresses from                            be labelled as R110). We do not show some front-ends too close to
Google’s Ad delivery network, separated by country. APNIC con-                                each other to improve readability. Circles are average user locations,
verts this distribution of IP addresses to a distribution of ASNs,                            where the radius of the circle is proportional to the population of
normalized by country Internet-user populations. We use the Team-                             users in that region. Figure 1 suggests that front-end locations tend
Cymru IP to ASN mapping to map IP addresses seen in the DITL                                  to be near large populations, providing at least one low latency
captures to their respective ASes [25] and accumulate queries by                              option to most users. Appendix F illustrates latency differences by
ASN. We were able to map 99.4% of DITL IP addresses to an ASN,                                region.
representing 98.6% of DITL query volume. The assumption that                                     User locations are aggregated by region, a geographic area used
recursives are in the same AS as the users they serve is obviously                            internally by Microsoft to break the world into regions that generate
incorrect for public DNS services, but we do not make an effort to                            similar amounts of traffic and so contain similar numbers of users.
correct for these cases. Overall, we believe Microsoft user counts                            A region often corresponds to a large metropolitan area. We refer to
                                                                                              users at the ⟨region, AS⟩ granularity, because users in the same
1 We aggregate user IP addresses by recursive /24 before counting to ensure we do not         ⟨region, AS⟩ location are often routed to the same front-ends and
double-count users.                                                                           so (generally) experience similar latency. There are 508 regions in




                                                                                        400
SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


total: 135 in Europe, 62 in Africa, 102 in Asia, 2 in Antarctica, 137                               rather than try to infer which inflation would exist in an equivalent
in North America, 41 in South America, and 29 in Oceania.                                           unicast deployment. First, coverage of measurement platforms used
   To study performance in Microsoft’s CDN, we use two major data                                   to determine unicast inflation such as RIPE Atlas (vantage points
sources: server-side logs and client-side measurements. Server-side                                 for anycast studies [51, 69]) is not representative [10]. Second, cal-
logs at front-ends collect information about user TCP connections,                                  culating unicast inflation requires knowledge of the best unicast
including the user IP address and TCP handshake RTT. Using these                                    alternative from every recursive seen in DITL to every root letter,
RTTs as latency measurements, we compute median latencies from                                      something that would be difficult to approximate with RIPE Atlas
users in a ⟨region, AS⟩ location to each front-end that serves                                      because some letters do not publish their unicast addresses. Third,
them.2 Microsoft determines the location and AS of users using                                      we find it valuable to compare latency to a theoretical lower bound,
internal databases.                                                                                 since user routes to the best unicast alternative may still be inflated.
   Client-side measurements come from a measurement system                                             We measure two types of inflation for the root DNS, by looking
operated by Microsoft [17]. Latency measurements are the time it                                    at which sites recursive resolvers are directed to. DITL captures are
takes for Microsoft users to fetch a small image via HTTP.3 The                                     a rich source of data because they provide us with a global view
measurement system instructs clients using CDN services to issue                                    of which recursives access which locations (§2.1). Our inflation
measurements to multiple rings, which enables us to remove biases                                   analysis covers 224 countries/regions and 22,243 ASes (Atlas covers
in latency patterns due to services hosted on different rings having                                about 3,700 ASes as of July 2021).
different client footprints (e.g., enterprise versus residential traffic).                             We calculate the first type of inflation – geographic inflation
Microsoft collects latencies of users populations, noting the location                              (Eq. (1)) – over 10 of the 13 root letters, omitting G which does not
and AS of the user. Since these measurements come directly from                                     provide data, H which only had one site in 2018 (and so has zero in-
end-users, we do not know which front-end the user hit. For both                                    flation), and I, where anonymization prevents analysis. Geographic
client-side measurements and server-side logs, we collect statistics                                inflation measures, at a high level, how users are routed to sites
for over a billion users across 15,000 ⟨region, AS⟩ locations.                                      compared to the closest front-end (i.e., efficiency)4 .
   We also use RIPE Atlas to ping anycast rings, because we cannot                                     We calculate the second type of inflation – latency inflation
share absolute latency numbers. We calibrate these results versus                                   (Eq. (2)) – over the root letters mentioned above by looking at
our (private) data measuring latency for CDN users. In total, we                                    the subset of DNS queries that use TCP, using the handshake
collect 7,000 ping measurements to rings from 1,000 RIPE Atlas                                      to capture RTT [57]. Our latency inflation analysis further ex-
probes in more than 500 ASes to augment CDN latency measure-                                        cludes D and L root, due to malformed DITL PCAPs. Latency infla-
ments. (Probes were selected randomly, and measured three times                                     tion uses measured latencies to determine inflation, so it reflects
to each ring.)                                                                                      constraints due to physical rights-of-way and connectivity, bad
                                                                                                    routing, and peering choices. We calculate median latency over
3     ROUTES TO ROOT DNS ARE INFLATED                                                               each ⟨root, resolver /24, anycast site⟩ for which we have
Earlier work has found query distance to the root DNS is often                                      at least 10 measurements, providing us latencies for resolvers rep-
significantly inflated [13, 23, 51, 67, 69]. Similar to this work, we                               resenting 40% of DITL query volume to these roots.
find that queries often travel to distant sites despite the presence
of a geographically closer site. We extend this understanding in a                                  3.1      Methodology
number of ways. While previous work considered only subsets of                                      To calculate geographic inflation, we first geolocate all recursives
root DNS activity and focused on geographic inflation for recursives                                in our DITL∩CDN dataset using MaxMind [41], following prior
rather than users, we calculate inflation for nearly all root letters,                              methodology which affirmed MaxMind to be suitably accurate for
and place inflation in the context of users, rather than recursive                                  geolocating recursive resolvers in order to assess inflation [51]. We
resolvers. These contributions are significant for several reasons.                                 then compute geographic inflation (scaled by the speed of light in
First, considering more root letters allows us to evaluate inflation                                fiber) for each recursive sending queries to root server 𝑗 as
in different deployments, and with most letters we can evaluate
the root DNS system. Since a recursive makes queries to many root                                                             2 ∑︁ 𝑁 (𝑅, 𝑗𝑖 )𝑑 (𝑅, 𝑗𝑖 )
                                                                                                              GI (𝑅, 𝑗) =       (                       − min 𝑑 (𝑅, 𝑗𝑘 ))                 (1)
letters, favoring those with low latency [60], system performance                                                            𝑐𝑓 𝑖      𝑁 (𝑅, 𝑗)            𝑘
and inflation can (and does) differ from component performance.
Second, we weight recursive resolvers by the number of users,                                          where 𝑁 (𝑅, 𝑗𝑖 ) is the number of queries to site 𝑗𝑖 by recursive 𝑅,
                                                                                                               Í
which allows us to see how users are affected by inflation. Finally,                                𝑁 (𝑅, 𝑗) = 𝑖 𝑁 (𝑅, 𝑗𝑖 ) is the total number of queries to all sites 𝑗𝑖
we extend prior work by conducting an analysis of latency (as                                       in root 𝑗 by recursive 𝑅, 𝑐 𝑓 is the speed of light in fiber, the factor
opposed to geographic) inflation with large coverage.                                               of 2 accounts for the round trip latency, 𝑑 (𝑅, 𝑗𝑘 ) is the distance
   Previous studies of anycast have separated inflation into two                                    between the recursive resolver and site 𝑗𝑘 , and both the summation
types, unicast and anycast, in an attempt to tease out how much la-                                 and minimization are over the global sites in this letter deployment
tency anycast specifically adds to queries [13, 16, 51, 69]. For several                            (see Section 2.1 for the distinction between local and global). We
reasons, we choose to consider inflation relative to the deployment,                                only consider global sites, since we do not know which recursives
                                                                                                    can reach local sites. For recursives which can reach a local site
2 We also looked at other percentiles (e.g., 95th ) and found the qualitative results to be         4 It would be interesting to measure topological inflation (extra distance traveled on the
similar.                                                                                            Internet topology, beyond shortest-path propagation-delay), but it would be difficult
3 DNS resolution and TCP connection time are factored out.                                          to do so using existing methods without sacrificing significant coverage.




                                                                                              401
                                                                                                                           SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


but instead reach a global site, Equation (1) (and Equation (2)) may
underestimate actual inflation.
   GI (𝑅, 𝑗) is an approximation of the inflation one would expect                                       1.0
                                                                                                         0.9                                                          B-2
to experience when executing a single query to root deployment 𝑗                                                                                                      A-5
                                                                                                         0.8
from recursive 𝑅, averaged over all sites. The overall geographic                                        0.7
                                                                                                                                                                      M-5




                                                                                          CDF of Users
                                                                                                                                                                      C - 10
inflation of a recursive is then the empirical mean over all roots.                                      0.6                                                          E - 15
Even though queries from the same recursive /24 are usually routed                                       0.5                                                          D - 20
                                                                                                         0.4                                                          K - 52
together, they may be routed to different sites due to load balancing                                                                                                 J - 68
                                                                                                         0.3
in intermediate ASes (see Appendix B.2 for measures of how often                                         0.2
                                                                                                                                                                      F - 94
                                                                                                                                                                      L - 138
this occurs), so we average geographic inflation across sites for                                        0.1                                                          All Roots
a recursive. Geographic inflation is useful to investigate since it                                      0.0
                                                                                                               0   20    40        60         80       100      120         140
shows how our results compare with prior work, how many users                                                           Geographic Inflation per Root Query (ms)

are being inflated, and it gives us a measure of "efficiency" (§7.2) .                                                                   (a)
   We also calculate latency inflation, again considering recursive
querying patterns seen in DITL. We calculate latency inflation                                           1.0
                                                                                                         0.9
LI (𝑅, 𝑗) for users of recursive 𝑅 to root 𝑗 as                                                          0.8
                                                                                                                                                                      B-2
                                                                                                         0.7




                                                                                          CDF of Users
                      ∑︁ 𝑁 (𝑅, 𝑗𝑖 )𝑙 (𝑅, 𝑗𝑖 )                                                                                                                         A-5
                                                  3×2                                                    0.6
                                                                                                                                                                      M-5
        LI (𝑅, 𝑗) =                             −      min 𝑑 (𝑅, 𝑗𝑘 )   (2)                              0.5
                       𝑖
                               𝑁 (𝑅, 𝑗)           2𝑐 𝑓 𝑘                                                                                                              C - 10
                                                                                                         0.4                                                          E - 15
                                                                                                         0.3                                                          K - 52
   where 𝑙 (𝑅, 𝑗𝑖 ) is the median latency of recursive 𝑅 towards root
                                                                                                         0.2                                                          J - 68
site 𝑗𝑖 and the other variables are as in Equation (1). Prior work                                       0.1
                                                                                                                                                                      F - 94
                                                                                                                                                                      All Roots
notes that routes rarely achieve a latency of less than the great circle                                 0.0
                                               2𝑐                   2𝑐                                         0   25   50       75       100       125     150       175         200
distance between the endpoints divided by 3𝑓 [46], so we use 3𝑓                                                          Latency Inflation per Root Query (ms)
to lower bound the best latency recursives could achieve. Latency                                                                        (b)
inflation is a measure of potential performance improvement users                   Figure 2: Inflation measured using geographic information (2a) and
could see due to changes in routing or expanding the physical                       TCP RTT estimates (2b). Generally, larger deployments are more
Internet (e.g., laying fiber).                                                      likely to inflate paths, and inflation in the roots is quite large. The
   One limitation is that we do not account for the fact that the                   legends indicate the number of global sites per letter during the 2018
source addresses of some queries in the DITL traces may be spoofed.                 DITL.
Spoofing is more likely to make our calculated inflation larger,
especially in cases where the spoofer is far away from the physical                 the 95𝑡ℎ percentile C root has 240 ms of latency inflation but
interface it is spoofing (i.e., from our perspective, the route looks               only 70 ms of geographic inflation. However, inflation for the root
inflated when actually the source address was spoofed). We do                       DNS as a whole is not as bad as individual root letters as shown
not attempt to correct for these cases since it would be difficult to               by lines All Roots , which take into account that recursives can
distinguish between legitimately poor routing and spoofed traffic.                  preferentially query low latency root servers [60].
                                                                                       Our latency inflation metric shows C root is more inflated than
3.2    Results                                                                      previously thought, inflating 35% of users by more than 100 ms com-
                                                                                    pared to 20% reported in prior work [51] (although the comparison
Figure 2a demonstrates that the likelihood of a root DNS query
                                                                                    to prior work is not perfect since what was measure is different).
experiencing any geographic inflation (Eq. (1)) roughly grows with
                                                                                    Other prior work found significant inflation in the roots, but it is
deployment size (y-axis intercept), expanding on results in prior
                                                                                    difficult to directly compare results since inflation was presented
work which presented an orthogonal, aggregated view [51]. The
                                                                                    in different ways [23, 69].
 All Roots line takes into account that each recursive spreads                         Clearly, routing to individual root letters often is inflated, with
its queries across different roots. It has the lowest y-intercept of                many queries traveling thousands more kilometers than needed,
any line in Figure 2a, which implies that nearly every recursive                    and being inflated by hundreds of milliseconds for some users.
experiences some inflation to at least one root and that the set of
inflated recursives varies across roots. Hence, our analysis shows                  4      ROOT DNS LATENCY AND INFLATION
that nearly every user will (on average) experience inflation when
                                                                                           HARDLY MATTER
querying the root DNS, and 10.8% of users are likely to be inflated
by more than 2,000 km (20 ms).                                                      With a richer understanding of inflation in the root DNS, one might
   Figure 2b shows that queries to these roots experience frequent                  wonder why inflation in root letters is large given growing deploy-
latency inflation (Eq. (2)), with between 20% and 40% of users expe-                ments and root DNS’s importance in the Internet. We now show
riencing greater than 100 ms of inflation (B root is a clear exception,             that root DNS inflation does not result in much user-visible latency.
but only had 2 sites, so inflation is less meaningful). Latency infla-
tion starts at approximately zero, which follows from our choice                    4.1                  Measuring Root DNS Latency Matters
of “optimal” latency (Eq. (2)). Compared to geographic inflation,                   The root DNS servers host records for TLDs (e.g., COM, ORG).
latency inflation is particularly larger in the tail. For example, at               There are approximately one thousand TLDs, and nearly all of the




                                                                              402
SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


corresponding DNS records have a TTL of two days. Hence, due to                  than a billion users). Our local perspective precisely measures how
shared caches at local resolvers, one might think root DNS latency               root DNS queries are amortized over users browsing sessions, while
trivially does not matter for users. Recent work even suggests the               our global analysis estimates the number of queries users worldwide
root DNS can be done away with entirely [5] or largely replaced                  execute to the roots.
by preemptive caching in recursives [48]. We offer several reasons
why we found it necessary to explicitly measure root DNS latency’s
impact on users, rather than use intuition.                                      4.3    Root DNS Latency Hardly Matter
   First, there is a lot of attention being placed on the root DNS               Local Perspective: To obtain a precise measure of how root DNS
in the professional and research communities. For example, some                  queries are amortized over a small population, we use packet cap-
experts have asked us in conversation why CDNs use anycast, when                 tures of a recursive resolver at ISI (§2.1). We also measure from two
anycast inflates latencies in the root DNS so much. The SIGCOMM                  authors’ computers to observe how an individual user interacts
2018 paper “Internet Anycast: Performance, Problems, & Potential”                with the root servers (with no shared cache), since ISI traces do
has drawn attention to the fact that anycast can inflate latency to              not give us context about user experience. Data from two users
the root DNS by hundreds of milliseconds [51]. Blog posts from the               is limited, which is a reflection of the challenges we identified in
root letters discuss latency improvements and inflation reductions               Section 4.2. However, these experiments offer precise measures of
[3, 14, 61, 79] – why does latency matter to roots? Moreover, over               how these authors interact with root DNS (which no prior work has
the past 5 years the number of root DNS sites has steadily increased             investigated), supplementing the global-scale data used for most of
to more than double, from 516 to 1367. Why is there so much                      the paper.
investment in more sites?                                                            Using traces gathered at ISI, we calculate the number of queries
   Second, there is value in quantitatively analyzing systems, espe-             to any root server as a fraction of user requests to the recursive
cially global systems that operate at scale, even if we can intuitively,         resolver. We call this metric the root cache miss rate, as it approx-
qualitatively reason about these systems without conducting anal-                imates how often a TLD record is not found in the cache of the
ysis. We conduct analysis using data from eleven of thirteen root                recursive in the event of a user query. It is approximate because
letters, giving us a truly global view of how users interact with the            the resolver may have sent multiple root requests per user query,
root DNS. We are aware of only one other study which looked at                   and some root requests may not be triggered by a user query. The
how caching affects root DNS queries [44], but that study is old, is             daily root cache miss rates of the resolver range from 0.1% to 2.5%
limited to one recursive resolver, and does not place DNS queries                (not shown), with a median value of 0.5%. The overall cache miss
in the context of user experience.                                               rate across 2018 was also 0.5%. The particular cache miss rate may
   Third, although TTLs of TLD records are two days, recursive                   vary depending on user querying behavior and recursive resolver
resolver implementations can be buggy. We noticed millions of                    software, but clearly the miss rate is small, due to shared caches.
queries per day for TLD records being sent to the root letters by                Appendix D shows the minimal impact root DNS latency has on
some recursives (§4.3), and found a bug in the popular BIND recur-               users of ISI and a CDF of DNS latency experienced by users at ISI.
sive resolver software that causes unnecessary queries to the roots                  Since the measurements at ISI can only tell us how often root
(Appendix E). Hence, making arguments about root DNS latency                     DNS queries are generated, we next look at how root DNS latency
requires careful analysis.                                                       compares to end-user application latency. On two authors’ work
                                                                                 computers (in separate locations), we direct all DNS traffic to local,
                                                                                 non-forwarding, caching recursive resolvers running BIND 9.16.5
4.2    How We Measure Root DNS                                                   and capture all DNS traffic between the user and the resolver, and
Measuring how root DNS latency affects users poses several chal-                 between the resolver and the Internet.
lenges. To put root DNS latency into context we must understand                      We run the experiment for four weeks and observe a median
(1) how user-application performance is affected when applications               daily root cache miss rate of 1.5% – similar to but larger than the
make root queries, (2) how often end-hosts and recursive resolvers               cache miss rate at ISI. The larger cache miss rate makes sense,
interact with root DNS, given their caches, (3) what the latency is              given the local users do not benefit from shared caches. We also
from the anycast deployment, and (4) how these effects vary by loca-             use browser plugins to measure median daily active browsing time
tion and root letter. These challenges both motivate our subsequent              and median daily cumulative page load time, so we can place DNS
analyses and also highlight the limitations of prior work which do               latency into perspective. Active browsing time is defined as the
not capture these subtleties of root DNS latency [23, 51, 58, 69].               amount of time a user spends interacting with the page (with a 30
   Therefore, precisely determining how root DNS latency affects                 second timeout), whereas page load time is defined as the time until
users would require global, OS-level control to select recursives                the window.onLoad event. Median daily root DNS latency is 1.6%
and view OS DNS caches; global application-level data to see when                of median daily page load time and 0.05% of median daily active
DNS queries are made and how this latency affects application-                   browsing time, meaning that root DNS latency is barely perceptible
performance; global recursive data to see caches, root queries, and              to these users when loading web pages, even without shared caches.
their latencies; and global root traces to see how queries to the                In general, we overestimate the impact of DNS and root DNS latency
roots are routed. As of July 2021, only Google might have this data,             since DNS queries can occur as a result of any application running
and assembling it would be daunting.                                             on the authors’ machines (not just browsing).
   To overcome these challenges we take two perspectives of root                     Global Perspective: Towards obtaining a global view of how
DNS interactions: local (close to the user) and global (across more              users interact with the root DNS, we next look at global querying




                                                                           403
                                                                                                                 SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


                                                                                             The line labeled Ideal does not use DITL query volumes to
                   1.0                                                                    calculate daily user query counts, but instead represents a hypothet-
                                                                                          ical scenario in which each recursive queries for all TLD records
                   0.8
                                                                                          exactly once per TTL, and amortizes these queries uniformly over
    CDF of Users




                   0.6                                                                    their respective user populations (we use Microsoft user counts for
                                                                                           Ideal ). The resulting hypothetical median daily query count of
                   0.4
                                                                                          0.007 could represent a future in which caching works at recursives
                   0.2                                                Ideal               optimally – not querying the roots when not necessary. Ideal
                                                                      CDN
                                                                      APNIC               also demonstrates the degree to which the assumption that recur-
                   0.0
                    10−3   10−2   10−1        100         101   102           103         sives only query once per TTL underestimates the latency users
                                    Queries per User per Day
                                                                                          experience due to the root DNS (§4.2) – the assumption is orders of
Figure 3: A CDF of the number of queries each user executes to the
                                                                                          magnitude off from reality.
roots per day. The CDN and APNIC lines represent different user-
                                                                                             We have shown root DNS latency, and therefore inflated routes
count datasets. The Ideal line presents an idealized assumption                           to the roots, makes no difference to most users. This result raises
about recursive query behavior. Most users wait for less than one
                                                                                          the question – are paths to the roots inflated because anycast intrin-
query to the roots per day, regardless of which user data we use.
                                                                                          sically results in inflation? Or rather, does latency not mattering in
behavior of recursives. As discussed in Section 4.2, it is difficult to                   this setting lead to anycast deployments that are not optimized for
model caching at resolvers and how caching saves users latency,                           latency and hence tend to have inflated routes? To answer these
since caching hides user query patterns (by design) and differs with                      questions, we turn to a new system using anycast to serve latency-
recursive implementation. To overcome this challenge, we use a new                        sensitive content – Microsoft’s CDN.
methodology that amortizes queries over large user populations,
by joining DNS query patterns with user data.                                             5     LATENCY MATTERS FOR MICROSOFT’S
    Given query volumes towards root servers from recursives and                                CDN
user counts using each recursive from the DITL captures (§2.1),
                                                                                          We demonstrate that latency (and hence inflation) does matter for
we estimate the number of queries to the roots that users wait for
                                                                                          Microsoft users when fetching web content, unlike for most users
per day. Figure 3 is a CDF of the expected number of queries per
                                                                                          in the root DNS, principally due to the number of RTTs users incur
user per day, where lines CDN and APNIC use a different user-
                                                                                          when fetching web content.
count dataset (§2.1), and line Ideal uses hypothetical assumptions
which we describe below. Figure 3 demonstrates that most users
wait for no more than one query to the roots per day, regardless of
                                                                                          5.1    RTTs in a Page Load
which user data we use.                                                                   To estimate the latency a user experiences when interacting with
    To generate each line in Figure 3, we divide (i.e., amortize) the                     Microsoft’s CDN (§5.2), we first estimate the number of RTTs re-
number of queries to the root servers made by each recursive by the                       quired to load a typical web page hosted by Microsoft’s CDN.
number of users that recursive represents. We weight this quotient                           The number of RTTs in a page load depends on a variety of
(i.e., daily queries per user) by user count and calculate the resulting                  factors, so we aim to lower bound the number. We lower bound the
CDF. We calculate the number of queries per day each recursive                            number of RTTs since a lower bound is a conservative measure of
makes from DITL by first calculating daily query rates at each site                       the impact of CDN inflation, as the latency inflation accumulates
(i.e., total queries divided by total capture time) and subsequently                      with each additional RTT, and larger pages (more RTTs) would
summing these rates across sites. We include nearly every root                            be impacted more. We provide an estimate of this lower bound
query captured across the root servers, so Figure 3 provides a truly                      based on modeling and evaluation of a set of web pages hosted by
global view of how users interact with the root DNS.                                      Microsoft’s CDN using Selenium (a headless web browser), finding
    The two lines CDN and APNIC correspond to amortizing DITL                             that 10 RTTs is a reasonable estimate. Due to length restrictions,
queries over Microsoft and APNIC user counts, respectively. Hence,                        we include the full details of our measurements and methodology
the set of ‘users’ each line represents is technically different, but we                  in Appendix C.
place them on the same graph for comparison. Even though the two
methodologies of estimating user counts behind root queries are                           5.2    Microsoft’s CDN User Latency
very different ( CDN uses an internal measurement system, while                           We now measure how users are impacted by latency of Microsoft’s
 APNIC uses Internet population estimates by country), amortizing                         CDN. First, using measurements from RIPE Atlas probes, we demon-
queries over these sets of users still yields the same high level                         strate that CDN latency results in significant delay to users when
conclusions about how users interact with the root DNS, suggesting                        fetching web content. Then, using both client-side measurements
that our methodology and conclusions are sound – users rarely                             and server-side logs, we also show that latency usually decreases
interact with the root DNS executing about one query per day at                           with more sites. Consequently, Microsoft has a major incentive to
the median. Users in the tail are likely either spammers, have buggy                      limit inflation experienced by users, and investments in more any-
recursive software, or represent recursives with more users than                          cast sites positively affect user experience much more in the case
DITL∩CDN suggests (e.g., cellular networks). APNIC user estimates                         of Microsoft’s CDN than in the roots. The positive effect on user
are not affected by NATs, and APNIC has a smaller tail.                                   experience has been a major reason for recent expansion (§7.3).




                                                                                    404
SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


                                                                                                                       globally (not shown in figure), so Figure 4a likely underestimates
                                                                   CDN Latency per RTT (ms)                            the latency users typically experience.
                                          0           20           40       60        80      100     120
                                    1.0
                                                                                                    R28
                                                                                                                          Users can experience up to 1,000 ms in anycast latency per page
                                    0.9
                                                                                                    R47                load, and, for large deployments (e.g., R95 ), half of RIPE Atlas
                                    0.8               R74
                                                                                                    R74                probes experience approximately 100 ms of latency per page load
    CDF of RIPE Probes




                                    0.7                                                             R95
                                                R95
                                                             R28                                    R110
                                                                                                                       (Fig. 4a). Therefore, unsurprisingly, latency to Microsoft’s CDN
                                    0.6
                                              R110
                                                                                                                       factors into user experience, and so Microsoft has an incentive to
                                    0.5
                                                           R47                                                         decrease latency for users. The difference in median latency per
                                    0.4
                                                                                                                       page load between R28 and R110 is approximately 100 ms, which
                                    0.3
                                                                                                                       is a measure of how investments in more front-ends can help users.
                                    0.2
                                                                                                                       Similarly, a root deployment with more sites tends to have lower
                                    0.1
                                                                                                                       latency than a root deployment with fewer sites (§7.2), but such
                                    0.0
                                          0          200        400       600      800      1000      1200             reductions in latency hardly affect user experience (§4).
                                                            CDN Latency per Web Page Load (ms)
                                                                                                                          Latency benefits with more sites are not uniform, and perfor-
                                                                             (a)
                                                                                                                       mance falls into one of two “groups” – R28 and R47 have similar
                                               Latency Change per RTT (Smaller Ring - Bigger Ring) (ms)
                                     −10               0          10           20            30             40         aggregate performance, as do R74 , R95 , and R110 . This group-
                                    1.0                                                                                ing corresponds to the way rings “cover” users – R74 provides a
                                    0.9                                                                                significant additional number of Microsoft users with a geographi-
    CDF of (Region, AS) Locations




                                    0.8
                                                                                                                       cally close front-end over R47 (§7.2).
                                    0.7
                                                                                                                          To show how adding front-ends tends to help individual
                                    0.6
                                    0.5
                                                                                                                       ⟨region, AS⟩ locations (in addition to aggregate perfor-
                                    0.4
                                                                                                                       mance), Figure 4b shows the difference in median latency for
                                    0.3                                                        R28 - R47
                                                                                                                       a ⟨region, AS⟩ location from one ring to the next larger ring,
                                    0.2                                                        R47 - R74               calculated using CDN measurements (as opposed to RIPE Atlas
                                    0.1                                                        R74 - R95               probes). Most ⟨region, AS⟩ locations experience either equal or
                                                                                               R95 - R110
                                    0.0                                                                                better latency to the next largest ring, with diminishing returns as
                                     −100         0          100         200            300          400
                                        Latency Change per Page Load (Smaller Ring - Bigger Ring) (ms)
                                                                                                                       more front-ends are added. A small fraction of users experience
                                                                             (b)
                                                                                                                       small increases in latency when moving to larger rings – 90% of
Figure 4: RTTs and latencies per web page load from RIPE probes to                                                     users experience a decrease of at most a few millisecond increase
CDN rings (4a), and change in median latency for Microsoft users                                                       and 99% experience less than a 10 ms increase. Hence, Microsoft
in ⟨region, AS⟩ locations when transitioning rings (4b). Axes with                                                     does not sacrifice fairness for performance improvements.
per-RTT latencies are blue, while axes with per-page-load latencies                                                       We next investigate if Microsoft’s clear incentive to reduce la-
are red. Latencies per page load can be significant, so Microsoft has                                                  tency (and therefore inflation) translates to lower inflation from
an incentive to reduce inflation.                                                                                      users to Microsoft’s CDN than from users to the root DNS.
    Microsoft’s CDN has groups of sites called rings (§2.2). Each
larger ring adds some sites to those of the smaller ring. Each ring                                                    6   ANYCAST INFLATION CAN BE SMALL
provides an IP anycast CDN, so we report results for each of the                                                       We next investigate whether Microsoft’s incentive to reduce infla-
rings individually. Different ring sizes reflect some of the benefit of                                                tion translates to an anycast deployment with less inflation than in
additional anycast locations, but a user’s traffic usually ingresses                                                   the roots, representing the study of anycast CDN inflation with the
to Microsoft’s network at the same PoP regardless of ring, since                                                       best coverage to date – measurements are from billions of users in
all routers announce all rings. Users experience latency from Mi-                                                      hundreds of countries/regions and 59,000 ASes. Critically, we are
crosoft’s as they retrieve web objects (e.g., web pages or supporting                                                  able to directly compare inflation between root DNS and Microsoft’s
data) hosted by Microsoft’s CDN. Hence, in order to assess how                                                         CDN, since we use the same methodology with broad coverage.
Microsoft users experience latency, we must measure what the RTT                                                          To measure anycast inflation for Microsoft’s CDN we use geo-
is from users to front-ends and how many RTTs are incurred when                                                        graphic information and server-side measurements (§2.2). Server-
fetching web content. We use our estimate from Section 5.1 that                                                        side logs give us a global view of which clients hit which front-ends
users incur at least 10 RTTs in a page load. To obtain per-page-load                                                   and the latencies they achieved. Latency is measured via server-side
latency, we scale anycast latency by the number of RTTs.                                                               logging of TCP round-trip times. Front-ends act as TCP proxies for
    In Figure 4a, we show latencies to rings. Figure 4a uses laten-                                                    fetching un-cached content from data centers. Routing over the
cies measured from RIPE Atlas probes (§2.2), as we cannot share                                                        global WAN is near optimal [36], so measuring inflation using la-
absolute latencies from Microsoft measurements since Microsoft                                                         tency to front-ends (as opposed to measuring inflation using end to
considers this data proprietary. Although RIPE Atlas has limited                                                       end latency) captures all routing inefficiency. We also use Microsoft
coverage [10], we compare (but cannot share) to CDN measure-                                                           user locations, which are determined using an internal database.
ments, which contain latencies from all ⟨region, AS⟩ locations                                                            As in Section 3, we calculate both geographic and latency infla-
to all rings. We observed that the distribution of RIPE Atlas probe                                                    tion. We calculate geographic inflation as in Equation (1), except all
latencies is overall somewhat lower than that of Microsoft’s users                                                     users in a ⟨region, AS⟩ location are assigned the mean location




                                                                                                                 405
                                                                                                                        SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


                                                                                                which highlights that even though users have more low latency
                                                                                                options (front-ends), they can still take circuitous routes to close
                   1.0                                                                          front-ends. However, Microsoft is able to keep latency inflation
                   0.9                                                                          below 30 ms for 70% of users in all rings and below 60 ms for 90%
                   0.8                                                                          of users. In Microsoft’s CDN, 99% of users experience less than 100
                   0.7                                                                          ms of inflation, but 10% experience more than 100 ms to the roots.
    CDF of Users




                   0.6                                                                             An interesting takeaway from Figure 5b is that system-wide
                   0.5                                                    R28                   per-query root DNS inflation is quite similar to CDN inflation, a
                   0.4                                                    R47                   fact that is not clear from prior work [16, 51] since prior work used
                   0.3                                                    R74
                                                                          R95
                                                                                                different methodology and looked at fewer root letters. However,
                   0.2
                                                                          R110                  inflation in individual root letters is quite worse than in Microsoft’s
                   0.1                                                    Root DNS              CDN (Fig. 2b). Although inflation in the roots does not matter to
                   0.0
                         0   5    10     15       20       25     30       35        40         most users (§4.3), it is still interesting to see how recursive resolvers
                                   Geographic Inflation per RTT (ms)
                                                                                                can take advantage of the thirteen independent deployments of
                                                   (a)
                                                                                                root letters, and choose which letter is the best for them, in a way
                                                                                                that is not possible in Microsoft’s CDN.
                   1.0                                                                             Compared to prior work which also studied inflation in Mi-
                   0.9                                                                          crosoft’s CDN [16], we find an improvement – 95% of users experi-
                   0.8                                                                          ence inflation under 80 ms now compared to 85% 5 years ago. This
                   0.7
                                                                                                improvement (representing millions of users) is despite the fact
    CDF of Users




                   0.6
                                                                                                that Microsoft’s CDN has more than doubled in size and that we
                   0.5
                                                                          R28                   use a stricter measure of inflation, and is evidence that expansion
                   0.4
                                                                          R47
                   0.3                                                    R74
                                                                                                reduces efficiency (in terms of % of users at their closest site) but
                   0.2                                                    R95                   inflation can be kept low through careful deployment (§7.2). Fig-
                   0.1                                                    R110                  ure 5b also offers a complementary view of inflation compared to
                                                                          Root DNS
                   0.0                                                                          prior work [16], which does not take into account that routing from
                         0   25   50        75      100      125    150   175    200
                                       Latency Inflation per RTT (ms)
                                                                                                a ⟨region, AS⟩ location to all front-ends might be sub-optimal.
                                                                                                   Compared to Figure 5a, Figure 5b demonstrates there is room
                                                   (b)
Figure 5: Inflation measured using geographic information (5a) and
                                                                                                for improvement – at least half of users visit their closest front-end,
CDN server side logs (5b). Inflation is more prevalent for larger                               but those users might take circuitous routes to those front-end as
deployments but is still small for most users.                                                  shown by the low y-axis intercepts in Figure 5b. There is still room
                                                                                                for latency optimization in anycast deployments, which is an active
of users in the ⟨region, AS⟩ location. Anycast inflation results in                             area of research [43, 47, 82].
extra latency for every packet (and corresponding ACK) exchanged
between a client and an anycasted service, resulting in a per RTT                               7     INCENTIVES AND INVESTMENT SHAPE
cost, so we refer to inflation as “per RTT”. Application-layer inter-                                 DEPLOYMENTS AND PATHS
actions may incur this cost multiple times (as in the case of loading
                                                                                                We have definitively answered the questions regarding inflation
a large web object from a CDN) or a single time (as in the case of
                                                                                                that we posed at the end of Section 4.3. We now investigate why
typical DNS request/response over UDP).
                                                                                                inflation is so different in root DNS and Microsoft’s CDN by looking
    Microsoft users usually experience no geographic inflation
                                                                                                at path lengths (§7.1), investigate how geographical differences in
(Fig. 5a, y-axis intercepts), and 85% of users experience less than
                                                                                                deployments affect inflation (§7.2), and present reasons behind the
10 ms (1, 000 𝑘𝑚) of geographic inflation per RTT for all rings.
                                                                                                expansion of both root DNS and CDNs (§7.3).
Conversely, 97% of root DNS users experience some geographic
inflation, and 25% of users experience geographic inflation more
than 10 ms (1, 000 𝑘𝑚) per RTT. The fact that geographic inflation
                                                                                                7.1    Microsoft’s CDN Has Shorter AS Paths, and
is larger and more prevalent in the roots than in Microsoft’s CDN                                      Short AS Paths are More Direct
(at every percentile) suggests Microsoft optimizes its deployment                               CDNs have a financial incentive to keep latency low for users and
to control it (§7).                                                                             have the resources to build efficient systems. Microsoft deploys
    We next calculate latency inflation for each ring as in Equa-                               state-of-the-art network routing automation [68, 80], a global SDN
tion (2). We calculate median latencies over user populations                                   WAN [36, 42], and expensive peering agreements when they make
within a ⟨region, AS⟩ location hitting a front-end in a given ring,                             economic sense and/or help user experience. These strategies result
the assumption being that measurements from some users in a                                     in short, low latency routes between users and Microsoft.
⟨region, AS⟩ location hitting the same site are representative of                                  We can capture some of these engineering efforts by measuring
all users in that ⟨region, AS⟩ location hitting that site. More than                            how Microsoft connects to users. CDNs peer widely with end-user
83% of such medians were taken over more than 500 measurements,                                 networks and so have direct paths to many users [54, 78]. With
so our observations should be robust. There is roughly constant                                 fewer BGP decision points, paths are often less inflated [70]. This
latency inflation as the number of front-ends grows (Fig. 5b),                                  intuition motivates the following investigation of AS path lengths




                                                                                          406
SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


                                                                                                                               Figure 6a shows shorter paths to Microsoft than to the roots.
                                           2 ASes       3 ASes           4 ASes           5+ ASes
                                                                                                                            (Weighting by traffic volumes yielded similar results.) 69% of all
                               1.0
                                                                                                                            paths to Microsoft only traverse two ASes (direct from RIPE Atlas
                                                                                                                            probe AS to destination AS), and only 5% of paths to Microsoft
   Percent of Paths




                               0.8

                               0.6
                                                                                                                            traverse four or more ASes. Conversely, between 5% and 44% paths
                               0.4
                                                                                                                            to root letters only traverse two ASes, and between 12% and 63% of
                               0.2
                                                                                                                            paths to roots traverse four or more ASes.
                               0.0
                                                                                                                               To demonstrate how short AS paths tend to have lower infla-
                                     CDN All  L          F       J   K       D    E         C       M   A      B            tion, Figure 6b shows the correlation between AS path length and
                                        Roots
                                                                                                                            geographic inflation6 . We compare to geographic (as opposed to
                                                                     (a)                                                    latency) inflation since we are able to calculate it for more root let-
                                                                                                                            ters. For the inflation towards destinations in Figure 6b, we use the
                               80
   Geographic Inflation (ms)




                                                                                                            2 ASes          geographic inflation associated with that ⟨region, AS⟩ location
                               60                                                                           3 ASes          calculated for Figure 2 and Figure 5a. The AS path length towards
                                                                                                            4+ ASes
                               40
                                                                                                                            each destination is the most common AS path length measured
                                                                                                                            across RIPE Atlas probes in the same ⟨region, AS⟩ location. Fig-
                               20
                                                                                                                            ure 6b demonstrates that paths that traverse fewer ASes tend to
                                0                                                                                           be inflated less. All Roots shows that this is true globally, across
                                     CDN    All     F        J       K        D       E         C       A      B
                                           Roots                                                                            root letters, and the results for each individual root letter shows
                                                                                                                            geographic inflation is less for paths traversing 2 ASes than it is for
                                                                     (b)                                                    paths traversing more (except for B and E root). The relationship
Figure 6: Distribution of the number of ASes traversed to reach                                                             between inflation and AS path length is very different across root
various destinations (6a) and the correlation between the AS path                                                           letters, which is evidence of different deployment strategies.
length towards a destination and geographic inflation (6b). Microsoft                                                          Overall, our results demonstrate that shorter paths tend to have
is closely connected to many eyeball ASes, and this connectivity                                                            less inflation, users have shorter paths to Microsoft than towards the
correlates with lower inflation. We group paths towards roots and
                                                                                                                            roots, and Microsoft tends to have less inflation across path lengths.
Microsoft by ⟨region, AS⟩ locations, except for ‘All Roots’ which
groups paths by ⟨region, AS, root⟩ locations.
                                                                                                                            We believe these observations are a result of strategic business
                                                                                                                            investments that Microsoft puts toward peering and optimizing its
towards roots and Microsoft and of how path lengths relate to infla-                                                        routing and infrastructure. In addition to shorter AS paths generally
tion, which is summarized by Figure 6. Figure 6 quantifies one key                                                          being less inflated [70], direct paths to Microsoft’s CDN in particular
difference between root DNS and CDN deployments, but publicly                                                               sidestep the challenges of BGP by aligning the best performing
available data cannot capture all of Microsoft’s optimizations.                                                             paths with the BGP decision process [20]. Direct paths will usually
   To quantify differences in AS path length between Microsoft and                                                          be preferred according to BGP’s top criteria, local preference and
roots, Figure 6a shows AS path lengths to roots and Microsoft from                                                          AS path length (because by definition they are the shortest and
RIPE Atlas probes. We use the maximum number of active RIPE                                                                 from a peer, and ASes usually set local preference to prefer peer
Atlas probes for which we can calculate AS paths to all destinations,                                                       routes in the absence of customer routes, which for Microsoft will
amounting to 7,200 RIPE Atlas probes in 158 countries/regions and                                                           only exist during a route leak/hijack). Among the multiple direct
2,400 ASes. Although RIPE Atlas probes do not have representative                                                           paths to Microsoft that a router may learn when its AS connects
coverage [10], it is the best publicly available system, and we are                                                         to Microsoft in different locations, the decision will usually fall
only interested in qualitative, comparative conclusions.                                                                    to lowest IGP cost, choosing the nearest egress into Microsoft.
   Lengths towards Microsoft’s CDN are based on traceroutes from                                                            Microsoft collocates anycast sites with all its peering locations, and
active Atlas probes in August 2020, whereas lengths towards the                                                             so the nearest egress will often (and, in the case of the largest ring,
roots are based on traceroutes from RIPE Atlas probes in April                                                              always) be collocated with the nearest anycast site, aligning early
2018 (the time of DITL).5 We perform IP to AS mapping using                                                                 exit routing with global optimization in a way that is impossible in
Team Cymru [25], removing IP addresses that are private, asso-                                                              the general case or with longer AS paths [70]. At smaller ring sizes,
ciated with IXPs, or not announced publicly by any ASes. We                                                                 Microsoft can use traffic engineering (for example, not announcing
merge AS siblings together into one ‘organization’. We derive sib-                                                          to particular ASes at particular peering points) when it observes
ling data from CAIDA’s AS to organization dataset [15]. We group                                                            an AS making poor routing decisions.
paths by ⟨region, AS⟩ location, except for ‘All Roots’, for which
we group paths by ⟨region, AS, root⟩ location. We assign each                                                               7.2     Larger Deployments are Less Efficient but
⟨region, AS⟩ location equal weight; when a given ⟨region, AS⟩                                                                       Have Lower Latency
location hosts multiple RIPE Atlas probes that measure different                                                            CDN latency in Figure 4a and inflation in Figure 5 reveal a rela-
path lengths to a given destination, the location’s weight is split                                                         tionship that some may find non-intuitive – as deployment size
evenly across the measured lengths.
                                                                                                                            6 The plot is a box-and-whisker, with the 5 horizontal lines from bottom to top for
5 We use AS path lengths from traceroutes towards the roots measured in 2018 in                                             each ⟨deployment, AS path length ⟩ representing minimum, first quartile, median,
Figure 6, so that we can pair AS path length directly with 2018 DITL inflation data.                                        third quartile, and maximum values.




                                                                                                                      407
                                                                                                                                                                                                                 SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


                                                                                                                                                                                         Table 1: Survey results from root DNS operators. Most root letters
                                                                                                                                                                                         indicate DDoS resilience and (surprisingly) latency have been major
                                       B
                                 160                                                                                                         R28
                                                                                                                                                                                         factors for growth, and that future growth will likely slow.
                                 140                                                                                  0.6                                                                                   Past                               Future




                                                                                            Efficiency (% of Users)
    Median Latency (ms)




                                                                                                                                                   R47
                                 120 H                                                                                                                       R74
                                                                                                                                                                                          Reason for Growth Number of Orgs   Future Growth Trend Number of Orgs
                                                                                                                            B                                      R95 R110                     Latency          8           Acceleration of Growth   1
                                 100                                                                                  0.5
                                                                                                                                A
                                                                                                                                                                                           DDoS Resilience       9           Decceleration of Growth  4
                                  80                                                                                                                                                         ISP Resilience      5            Maintain Growth Rate    4
                                                                                                                                    CE                             F
                                                                                                                      0.4                                                                        Other           3                Cannot Share        1
                                  60
                                           M                                                                                                        K
                                  40       A
                                                       D                                    L                         0.3       M                                              L
                                                                                                                                                                                         sites and (low) median latency (approximately 15 ms), but that F
                                               C                 K   IJ
                                  20               E       R28 R47               F                                                       D               J                               root has considerably lower efficiency; hence, low efficiency is not
                                                                          R74    R95 R110
                                       0                   50         100                                                   0                50         100                              necessarily bad. Conversely, high efficiency does not result in low
                                                       Number of Global Sites                                                            Number of Global Sites
                                                                                                                                                                                         latency; for example, 49% of users reach their closest B root site,
                                                                                                     (a)                                                                                 but users still experience a high median latency to B root of 160 ms.
                                                                                                                                                                                         Prior work looked at similar metrics to those in Figure 7a (right) for
                                 1.0                                                                                                                                                     root letters using data from RIPE Atlas and arrived at very different
                                 0.9                                                                                                                                                     conclusions [51], possibly since RIPE Atlas has limited coverage.
                                                                                                                                                                   All Roots
    Percent of User Population




                                 0.8                                                                                                                               R110                     Part of what contributes to low latency is that organizations place
                                 0.7                                                                                                                               L - 138
                                                                                                                                                                                         sites close to users. Figure 7b shows what percent of Microsoft users
                                                                                                                                                                   R95
                                 0.6
                                                                                                                                                                   F - 94                are "covered" by a site in each ring and in a root letter of similar
                                 0.5                                                                                                                               R74                   size, where "covered" means the closest site is within 𝑋 km of
                                 0.4                                                                                                                               J - 68
                                                                                                                                                                                         users (x-axis). Hence, coverage implies there is a reasonably low
                                 0.3                                                                                                                               R47
                                                                                                                                                                   K - 52                latency option for users. Figure 7b is quite surprising – first, the
                                 0.2
                                                                                                                                                                   R28                   root DNS as a whole (All Roots) has impressive coverage – 91% of
                                 0.1                                                                                                                               D - 20
                                                                                                                                                                                         Microsoft users are within 500 km of a root site (not even counting
                                 0.0
                                                           250       500          750    1000 1250 1500                                                      1750       2000             local sites!). Moreover, individual root letters can have even better
                                                                                Coverage Radius of Site (km)
                                                                                                                                                                                         coverage of Microsoft users than rings (L root has 94% of users
                                                                                                    (b)
                                                                                                                                                                                         within 1,000 km whereas R110 has 90%), which is interesting since
Figure 7: Larger deployments lead to lower latency (Fig. 7a-left) since
they offer more low-latency options to users (Fig. 7b). However, fewer                                                                                                                   L root, unlike R110, was not deployed specifically for Microsoft
users visit their closest site (Fig. 7a-right) leading to more inflation.                                                                                                                users. Figure 7b also demonstrates that approximating root DNS
                                                                                                                                                                                         users with Microsoft users (Fig. 2) was fair, since root letters have
increases, inflation increases (less efficiency) but median latency                                                                                                                      decent coverage of Microsoft users. An exception is D root which
decreases. We observe a similar effect in Figure 2 – larger root                                                                                                                         did not have global sites in India at the time, where Microsoft has
deployments tend to have more inflation but have lower latency.                                                                                                                          both anycast sites and a large user population to serve.
Intuitively, larger deployments are less efficient since BGP will
make "wrong" decisions about which routes to export more often,                                                                                                                          7.3    Differing Incentives Lead to Different
and have lower latency since there are more low-latency options                                                                                                                                 Investments and Outcomes
available to users. These results suggest efficiency may not be a
                                                                                                                                                                                         We now discuss how incentives have shaped deployments and how
useful metric for assessing performance.
                                                                                                                                                                                         our findings may extend to other anycast deployments.
    We make these relationships explicit in Figure 7a which shows
median latency and efficiency for each root letter and Microsoft ring.                                                                                                                   7.3.1 Drivers for Growth. We reached out to operators of both root
We define efficiency as the percentage of users with zero geographic                                                                                                                     DNS and Microsoft asking what fueled their recent growth and
inflation (i.e., y-axis intercepts in Figure 2a and Figure 5a) since                                                                                                                     whether they think it will continue. Of the twelve organizations
it is a rough measure of how optimal routing is (routing may not                                                                                                                         running a root DNS letter, 11 responded, and we summarize the
actually be optimal even if there is zero geographic inflation if users                                                                                                                  main reasons root DNS letters expand in Table 1. Principally, roots
take a circuitous route to their closest site). Latency to root letters in                                                                                                               grew to reduce latency and improve DDoS resilience.
Figure 7a is the median latency across all RIPE Atlas probes over an                                                                                                                        Over the past 5 years the number of root DNS sites has more
hour in 2018 (time of DITL) (i.e., median per probe, then a median                                                                                                                       than doubled from 516 to 1367, steadily increasing. Surprisingly,
across probes), and latencies to rings are medians in Figure 4a.                                                                                                                         Table 1 demonstrates latency was a primary reason for expansion
    The trend that efficiency decreases with deployment size is less                                                                                                                     for nearly all root letters. Our results suggest this reasoning does
clear in the root DNS than in Microsoft’s CDN, likely since the                                                                                                                          not stem from caring about user experience (§4.3) but perhaps from
root letters are run by different organizations and so have different                                                                                                                    establishing a competitive benchmark with other root letters.
deployment strategies which also impact latency and inflation. A                                                                                                                            Root operators also indicated growth was driven to improve
counterexample to the trend is F root which had the lowest median                                                                                                                        resilience in two dimensions: DDoS and "ISP" resilience. DDoS
latency (15 ms) in 2018 and good efficiency (39%). F root likely                                                                                                                         resilience refers to increasing overall capacity so root letters can
bucks the trend since F root partners with Cloudflare (a global                                                                                                                          provide service in the face of DDoS attacks. ISP resilience refers to
CDN) and so benefits from a deployment tuned to lowering user                                                                                                                            offering root sites in certain locations and networks so that service
latency. It is interesting that R95 and F root have similar number of                                                                                                                    can still be offered even if connectivity to the rest of the Internet is




                                                                                                                                                                                   408
SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


severed. According to both operator responses and publicly avail-               in the root DNS [13]. Our work supports these conclusions and
able sources, growth additionally stems from open hosting policies              uses them in a larger conversation about anycast in the context
[40, 62, 74] (almost any AS can volunteer to host a new site) and               of applications. We also confirm observations in prior work that
from teaming up with large CDNs like Cloudflare. Root operator                  anycast site affinity is high [12], at least over the duration of DITL.
responses about future plans for growth suggest that the increase
of root DNS sites will slow in the coming years.
   With such decentralized deployment (in part by design to pro-
                                                                                   CDN Anycast. Some CDNs use IP anycast [16, 21, 30, 65, 75].
mote resilience), coordinated optimization of root DNS latency is
                                                                                Some prior work looked at inflation in CDNs [16], finding it to
difficult, even if latency optimization were a goal. By contrast, Mi-
                                                                                be similarly low. Our work presents a much larger study of la-
crosoft’s CDN is latency-sensitive and is centrally run. Operators
                                                                                tency and inflation (more than twice as many front-ends, orders
optimize and monitor latency, thereby minimizing inflation (§6)
                                                                                of magnitude more users and measurements), updating the numer-
with direct paths to many users (§7.1). Unlike some root letters,
                                                                                ical results and lending confidence to the result that inflation is
Microsoft does not (externally) compare latency with other CDNs,
                                                                                low; places performance metrics in the context of user experience;
considering latency proprietary. Construction of new front-ends
                                                                                compares performance to other systems that use anycast; and pro-
often follows business needs to support new markets. These com-
                                                                                vides some evidence of how CDNs can keep inflation low. Other
mercial motivations contrast with the above root DNS reasons for
                                                                                prior work looked at how prefix announcement configurations
expansion, yet the number of front-ends for Microsoft’s CDN has
                                                                                can impact the performance of an anycast CDN [54]. More recent
more than doubled in the past five years.
                                                                                work has investigated how to diagnose and improve anycast perfor-
7.3.2 Other Anycast Systems. A key takeaway from our results                    mance through measurements in production systems [17, 43, 76].
is that one cannot generalize our results to other systems using                Concurrent work examined addressing challenges faced by CDNs,
anycast. Anycast must be assessed in the context of the system in               proposing a scheme to decouple addressing from services that is
which it resides. Prior work took the results of one system (root               compatible with anycast [27]. Our work characterizes, rather than
DNS) and assumed it applied generally to a technique (anycast)                  changes, anycast CDN performance.
which resulted in misleading conclusions [51]. It would be difficult
to even extend our results to systems with similar deployments,
since the degree to which performance improvements are due to                      Recursive Resolvers, The Benefits of Caching, and Web Performance.
the deployment and the degree to which they are due to tuning of                Prior work has looked at statistics and latency implications of local
route configurations is unknown [9].                                            resolvers [18, 44]. We calculate similar statistics using recent data.
   Other systems using anycast include Akamai DNS authoritative                 Some previous work looked at certain pathological behaviors of
resolvers [1], Google Cloud VMs [32], and Google Public DNS                     popular recursives and the implications these behaviors have on
[31]. All of these services have different performance requirements             root DNS load times [34, 49, 73, 81]. We present additional patho-
for users; i.e., they all want inflation to be "low" but how "low"              logical behavior of a popular recursive in Appendix E. Many studies
it needs to be depends on the application. For example, Google                  characterize web performance and consider DNS’s role in a page
Cloud VMs can host game engines which have much stricter latency                load [8, 11, 72], although none consider how root DNS specifically
requirements than fetching HTTP objects. We hope future work                    contributes to page load time and how this relates to user experi-
will take these considerations into account when assessing anycast.             ence. Recent work considers placing DNS in the context of other
                                                                                applications but does not look at root DNS latency in particular [6].
8    RELATED WORK
   Root DNS Anycast. Many prior studies look at latency and in-
flation performance in the root DNS [13, 51, 52, 67, 69]. Our work
builds on these studies, conducting analysis for nearly every root              9   CONCLUSION
letter and calculating inflation for millions of recursives in 35,000           While anycast performance is interesting in its own right, prior
ASes. These larger scale measurements offer broad coverage, en-                 studies have drawn conclusions primarily from anycast for root
able comparisons among root letter deployments, and allow us to                 DNS [51]. We have shown that anycast operates differently in CDNs,
assess inflation in the root DNS system as a whole. We also cal-                with less inflation. Differences stem from the impact the anycast
culate latency inflation differently than in prior work, which we               service’s latency and inflation has on user-perceived latency. Our
believe offers a useful, orthogonal picture of inflation, and calculate         results show the importance of considering multiple subjects in
inflation using the same methodology for both Microsoft’s and                   measurement studies and suggest why anycast continues to see
root DNS, which allows us to compare inflation directly between                 wide, growing deployment.
Microsoft’s CDN and root DNS (not possible with prior studies).                    Acknowledgements. This paper has been partially funded by
Finally, we place latency and inflation in the context of user experi-          NSF CNS-1835253 and NSF CNS-1836872. John Heidemann’s work
ence, while prior work on the root DNS does not. Other prior work               was supported in part by NSF CNS-1925737 and OAC-1739034. We
looks at anycast’s ability defend against DDoS attacks [58, 67]; we             would like to thank our shepherd Xiaowei Yang and the anonymous
do not consider anycast’s performance in this context. Other prior              reviewers for their insightful comments, root DNS operators for
work discussed how ad-hoc anycast deployments can lead to poor                  their feedback on our analysis, and Dave Levin and Marcel Flores
performance and load balancing and is an early study of inflation               for their detailed feedback on an early draft of the paper.




                                                                          409
                                                                                                                             SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


REFERENCES                                                                                           Resolver Perspective. IEEE/ACM Transactions on Networking (Oct. 2014).
 [1] Akamai. 2020. Designing DNS for Availability and Resilience Against DDoS                   [29] Manaf Gharaibeh, Han Zhang, Christos Papadopoulos, and John Heidemann.
     Attacks.        akamai.com/us/en/multimedia/documents/white-paper/akamai-                       2016. Assessing Co-locality of IP Blocks. In Proceedings of 19𝑡ℎ IEEE Global
     designing-dns-for-availability-and-resilience-against-ddos-attacks.pdf                          Internet Symposium (San Francisco, CA, USA). IEEE.
 [2] Akamai. 2021. Akamai Compliance Programs.               akamai.com/us/en/about/            [30] Danilo Giordano, Danilo Cicalese, Alessandro Finamore, Marco Mellia, Maurizio
     compliance/                                                                                     Munafò, Diana Zeaiter Joumblatt, and Dario Rossi. 2016. A First Characterization
 [3] Mehmet Akcin. 2015. Comparing Root Server Performance Around the World.                         of Anycast Traffic from Passive Traces. In Network Traffic Measurement and
     thousandeyes.com/blog/comparing-dns-root-server-performance                                     Analysis Conference (TMA) (Louvain la Neuve, Belgium). IFIP/ACM.
 [4] Adiel Akplogan, Roy Arends, David Conrad, Alain Durand, Paul Hoffman, David                [31] Google. 2020. Google Public DNS. developers.google.com/speed/public-dns
     Huberman, Matt Larson, Sion Lloyd, Terry Manderson, David Soltero, Samaneh                 [32] Google. 2021. Cloud Load Balancing. cloud.google.com/load-balancing
     Tajalizadehkhoob, and Mauricio Vergara Ereche. 2020. Analysis of the Effects               [33] GTmetrix. 2019. The Top 1,000 Sites on the Internet. gtmetrix.com/top1000.html
     of COVID-19-Related Lockdowns on IMRS Traffic. (April 2020). icann.org/en/                 [34] Wes Hardaker. 2020. What’s in a Name? blog.apnic.net/2020/04/13/whats-in-a-
     system/files/files/octo-008-en.pdf                                                              name/
 [5] Mark Allman. 2019. On Eliminating Root Nameservers from the DNS. In Proceed-               [35] John Heidemann, Katia Obraczka, and Joe Touch. 1997. Modelling the Perfor-
     ings of the 18𝑡ℎ ACM Workshop on Hot Topics in Networks (HOTNETS) (Princeton,                   mance of HTTP Over Several Transport Protocols. ACM/IEEE Transactions on
     NJ, USA). ACM.                                                                                  Networking (Oct. 1997).
 [6] Mark Allman. 2020. Putting DNS in Context. In Proceedings of the 2020 Internet             [36] Chi-Yao Hong, Srikanth Kandula, Ratul Mahajan, Ming Zhang, Vijay Gill, Mohan
     Measurement Conference (IMC) (Online). ACM.                                                     Nanduri, and Roger Wattenhofer. 2013. Achieving High Utilization with Software-
 [7] Amazon. 2020. Amazon Route 53 FAQs. aws.amazon.com/route53/faqs/                                Driven WAN. In Proceedings of the 2013 ACM SIGCOMM Conference (Hong Kong).
 [8] Internet Archive. 2020. The HTTP Archive Project. httparchive.org/                              ACM.
 [9] Todd Arnold, Matt Calder, Italo Cunha, Arpit Gupta, Harsha V. Madhyastha,                  [37] Geoff Huston. 2014. How Big is that Network? labs.apnic.net/?p=526
     Michael Schapira, and Ethan Katz-Bassett. 2019. Beating BGP is Harder than we              [38] IANA. 2020. IANA IPv4 Special-Purpose Address Registry. iana.org/assignments/
                                                                                                     iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml
     Thought. In Proceedings of the 18𝑡ℎ ACM Workshop on Hot Topics in Networks
                                                                                                [39] IANA. 2020. Root Servers. root-servers.org
     (HOTNETS) (Princeton, NJ, USA). ACM.
                                                                                                [40] ICANN. 2020. Packet Clearing House. icannwiki.org/Packet_Clearing_House
[10] Todd Arnold, Ege Gürmeriçliler, Georgia Essig, Arpit Gupta, Matt Calder, Vasileios
                                                                                                [41] MaxMind Inc. 2020. IP Geolocation. maxmind.com/en/geoip2-databases
     Giotsas, and Ethan Katz-Bassett. 2020. (How Much) Does a Private WAN Improve
                                                                                                [42] Sushant Jain, Alok Kumar, Subhasree Mandal, Joon Ong, Leon Poutievski, Arjun
     Cloud Performance? In INFOCOM (Online). IEEE.
                                                                                                     Singh, Subbaiah Venkata, Jim Wanderer, Junlan Zhou, and Min Zhu. 2013. B4:
[11] Alemnew Sheferaw Asrese, Pasi Sarolahti, Magnus Boye, and Jorg Ott. 2016.
                                                                                                     Experience with a Globally-Deployed Software Defined WAN. In Proceedings of
     WePR: A Tool for Automated Web Performance Measurement. In 2016 IEEE
                                                                                                     the 2013 ACM SIGCOMM Conference (Hong Kong). ACM.
     Globecom Workshops (Washington D.C., USA). IEEE.
                                                                                                [43] Yuchen Jin, Sundararajan Renganathan, Ganesh Ananthanarayanan, Junchen
[12] Hitesh Ballani and Paul Francis. 2005. Towards a Global IP Anycast Service.
                                                                                                     Jiang, Venkata N Padmanabhan, Manuel Schroder, Matt Calder, and Arvind
     In Proceedings of the 2005 ACM SIGCOMM Conference (Philadelphia, PA, USA).
                                                                                                     Krishnamurthy. 2019. Zooming in on Wide-Area Latencies to a Global Cloud
     ACM.
                                                                                                     Provider. In Proceedings of the 2019 ACM SIGCOMM Conference. ACM.
[13] Hitesh Ballani, Paul Francis, and Sylvia Ratnasamy. 2006. A Measurement-
                                                                                                [44] Jaeyeon Jung, Emil Sit, Hari Balakrishnan, and Robert Morris. 2002. DNS Perfor-
     Based Deployment Proposal for IP Anycast. In Proceedings of the 2006 Internet
                                                                                                     mance and the Effectiveness of Caching. IEEE/ACM Transactions on networking
     Measurement Conference (IMC) (Rio de Janeiro, Brazil). ACM.
                                                                                                     (Feb. 2002).
[14] Ray Bellis. 2015. Researching F-root Anycast Placement Using RIPE At-
                                                                                                [45] Dina Katabi and John Wroclawski. 2000. A Framework for Global IP-Anycast
     las.     labs.ripe.net/author/ray_bellis/researching-f-root-anycast-placement-
                                                                                                     (GIA). In Proceedings of the 2000 ACM SIGCOMM Conference (Stockholm, Sweden).
     using-ripe-atlas/
                                                                                                     ACM.
[15] CAIDA. 2020. Inferred AS to Organization Mapping Dataset. caida.org/data/as-
                                                                                                [46] Ethan Katz-Bassett, John P. John, Arvind Krishnamurthy, David Wetherall,
     organizations/
                                                                                                     Thomas Anderson, and Yatin Chawathe. 2006. Towards IP Geolocation Using De-
[16] Matt Calder, Ashley Flavel, Ethan Katz-Bassett, Ratul Mahajan, and Jitendra
                                                                                                     lay and Topology Measurements. In Proceedings of the 2006 Internet Measurement
     Padhye. 2015. Analyzing the Performance of an Anycast CDN. In Proceedings of
                                                                                                     Conference (IMC) (Rio de Janeiro, Brazil). ACM.
     the 2015 Internet Measurement Conference (IMC) (Tokyo, Japan). ACM.
                                                                                                [47] Rupa Krishnan, Harsha V. Madhyastha, Sridhar Srinivasan, Sushant Jain, Arvind
[17] Matt Calder, Ryan Gao, Manuel Schröder, Ryan Stewart, Jitendra Padhye, Ratul
                                                                                                     Krishnamurthy, Thomas Anderson, and Jie Gao. 2009. Moving Beyond End-to-
     Mahajan, Ganesh Ananthanarayanan, and Ethan Katz-Bassett. 2018. Odin: Mi-
                                                                                                     End Path Information to Optimize CDN Performance. In Proceedings of the 2009
     crosoft’s Scalable Fault-Tolerant CDN Measurement System. In 15𝑡ℎ USENIX                        Internet Measurement Conference (IMC) (Chicago, IL, USA). ACM.
     Symposium on Networked Systems Design and Implementation (NSDI) (Renton,                   [48] W. Kumari and P. Hoffman. 2020. Running a Root Server Local to a Resolver.
     WA, USA). USENIX.                                                                               Technical Report 8806. Internet Request For Comments. www.rfc-editor.org/
[18] Thomas Callahan, Mark Allman, and Michael Rabinovich. 2013. On Modern DNS                       rfc/rfc8806.txt
     Behavior and Properties. ACM SIGCOMM Computer Communication Review (July                   [49] Matthew Lentz, Dave Levin, Jason Castonguay, Neil Spring, and Bobby Bhat-
     2013).                                                                                          tacharjee. 2013. D-mystifying the D-root Address Change. In Proceedings of the
[19] Neal Cardwell, Stefan Savage, and Tom Anderson. 2000. Modelling TCP Latency.                    2013 Internet Measurement Conference (IMC) (Barcelona, Spain). ACM.
     In INFOCOM (Tel-Aviv, Israel). IEEE.                                                       [50] Zhihao Li. 2019. Diagnosing and Improving the Performance of Internet Anycast.
[20] Yi-Ching Chiu, Brandon Schlinker, Abhishek Balaji Radhakrishnan, Ethan Katz-                    Ph.D. Dissertation. University of Maryland, College Park.
     Bassett, and Ramesh Govindan. 2015. Are We One Hop Away from a Better                      [51] Zhihao Li, Dave Levin, Neil Spring, and Bobby Bhattacharjee. 2018. Internet
     Internet? In Proceedings of the 2015 Internet Measurement Conference (IMC) (Tokyo,              Anycast: Performance, Problems, & Potential. In Proceedings of the 2018 ACM
     Japan). ACM.                                                                                    SIGCOMM Conference (Budapest, Hungary). ACM.
[21] Danilo Cicalese, Jordan Augé, Diana Joumblatt, Timur Friedman, and Dario Rossi.            [52] Jinjin Liang, Jian Jiang, Haixin Duan, Kang Li, and Jianping Wu. 2013. Measuring
     2015. Characterizing IPv4 Anycast Adoption and Deployment. In Proceedings of                    Query Latency of Top Level DNS Servers. In International Conference on Passive
     the 11𝑡ℎ ACM Conference on Emerging Networking Experiments and Technologies                     and Active Network Measurement (PAM) (Hong Kong). Springer.
     (CoNEXT) (Heidelberg, Germany). ACM.                                                       [53] Zhuoqing Morley Mao, Charles Cranor, Fred Douglis, Michael Rabinovich, Oliver
[22] Cloudflare. 2020. What is DNS? cloudflare.com/learning/dns/what-is-dns/                         Spatscheck, and Jia Wang. 2002. A Precise and Efficient Evaluation of the Prox-
[23] Lorenzo Colitti, Erik Romijn, Henk Uijterwaal, and Andrei Robachevsky. 2006.                    imity Between Web Clients and their Local DNS Servers. In USENIX Annual
     Evaluating the Effects of Anycast on DNS Root Name Servers. RIPE Document                       Technical Conference (Monterey, CA, USA). USENIX.
     RIPE-393 (Oct. 2006).                                                                      [54] Stephen McQuistin, Sree Priyanka Uppu, and Marcel Flores. 2019. Taming Any-
[24] Gerald Combs. 2020. Tshark. wireshark.org/docs/man-pages/tshark.html                            cast in the Wild Internet. In Proceedings of the 2019 Internet Measurement Confer-
[25] Team Cymru. 2020. IP to ASN Mapping Service. team-cymru.com/community-                          ence (IMC) (Amsterdam, Netherlands). ACM.
     services/ip-asn-mapping/                                                                   [55] Christopher Metz. 2002. IP Anycast Point-To-(Any) Point Communication. IEEE
[26] DNS-OARC. 2018. A Day in the Life of the Internet. dns-oarc.net/oarc/data/                      Internet Computing (Aug. 2002).
     ditl/2018                                                                                  [56] P. Mockapetris. 1987. Domain Names - Implementation and Specification. ietf.
[27] Marwan Fayed, Lorenz Bauer, Vasileios Giotsas, Sami Kerola, Marek Majkowski,                    org/rfc/rfc1035.txt
     Pavel Odinstov, Jakub Sitnicki, Taejoong Chung, Dave Levin, Alan Mislove,                  [57] Giovane C. M. Moura, John Heidemann, Wes Hardaker, Jeroen Bulten, Joao Ceron,
     Christopher A. Wood, and Nick Sullivan. 2021. The Ties that un-Bind: Decoupling                 and Cristian Hesselman. 2020. Old But Gold: Prospecting TCP to Engineer DNS
     IP from Web Services and Sockets for Robust Addressing Agility at CDN-Scale.                    Anycast (extended). ISI-TR-740, USC/Information Sciences Institute, Tech. Report
     In Proceedings of the 2021 ACM SIGCOMM Conference (Online). ACM.                                (2020).
[28] Hongyu Gao, Vinod Yegneswaran, Jian Jiang, Yan Chen, Phillip Porras, Shalini
     Ghosh, and Haixin Duan. 2014. Reexamining DNS from a Global Recursive




                                                                                          410
SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


[58] Giovane C. M. Moura, Ricardo de Oliveira Schmidt, John Heidemann, Wouter B.                      ACM.
     de Vries, Moritz Muller, Lan Wei, and Cristian Hesselman. 2016. Anycast vs.                 [71] RIPE NCC Staff. 2015. RIPE Atlas: A Global Internet Measurement Network.
     DDoS: Evaluating the November 2015 Root DNS Event. In Proceedings of the 2016                    Internet Protocol Journal (2015).
     Internet Measurement Conference (IMC) (Santa Monica, CA, USA). ACM.                         [72] Srikanth Sundaresan, Nazanin Magharei, Nick Feamster, Renata Teixeira, and Sam
[59] Mozilla. 2020. Window: Load Event. developer.mozilla.org/en-US/docs/Web/                         Crawford. 2013. Web Performance Bottlenecks in Broadband Access Networks.
     API/Window/load_event                                                                            In Proceedings of the ACM SIGMETRICS Conference (Pittsburgh, PA, USA). ACM.
[60] Moritz Müller, Giovane C. M. Moura, Ricardo de Oliveira Schmidt, and John                   [73] Matthew Thomas. 2020. Chromium’s Impact on Root DNS Traffic. blog.apnic.
     Heidemann. 2017. Recursives in the Wild: Engineering Authoritative DNS Servers.                  net/2020/08/21/chromiums-impact-on-root-dns-traffic
     In Proceedings of the 2017 Internet Measurement Conference (IMC) (London, United            [74] Verisign. 2021. FAQ on RIRS Node Hosting. verisign.com/en_US/domain-
     Kingdom). ACM.                                                                                   names/internet-resolution/node-hosting/index.xhtml
[61] RIPE NCC. 2006. Evaluating The Effects Of Anycast On DNS Root Nameservers.                  [75] Verizon. 2020. verizondigitalmedia.com/media-platform/delivery/network/
     ripe.net/publications/docs/ripe-393#efficiency                                              [76] Lan Wei, Marcel Flores, Harkeerat Bedi, and John Heidemann. 2020. Bidirec-
[62] RIPE NCC. 2018. Hosting a K-root Node. ripe.net/analyse/dns/k-root/hosting-                      tional Anycast/Unicast Probing (BAUP): Optimizing CDN Anycast. In Network
     a-k-root-node                                                                                    Operations and Management Symposium (Online). IEEE/IFIP.
[63] OpenDNS. 2020. Data Center Locations. opendns.com/data-center-locations/                    [77] Lan Wei and John Heidemann. 2017. Does Anycast Hang Up on You? In Network
[64] Craig Partridge, Trevor Mendez, and Walter Milliken. 1993. Host Anycasting                       Traffic Measurement and Analysis Conference (TMA) (Dublin, Ireland). IFIP/ACM.
     Service. tools.ietf.org/html/rfc1546                                                        [78] Florian Wohlfart, Nikolaos Chatzis, Caglar Dabanoglu, Georg Carle, and Walter
[65] Matthew Prince. 2013. Load Balancing without Load Balancers. blog.cloudflare.                    Willinger. 2018. Leveraging Interconnections for Performance: The Serving In-
     com/cloudflares-architecture-eliminating-single-p/                                               frastructure of a Large CDN. In Proceedings of the 2018 ACM SIGCOMM Conference
[66] Jan Rüth, Christian Bormann, and Oliver Hohlfeld. 2017. Large-Scale Scanning of                  (Budapest, Hungary). ACM.
     TCP’s Initial Window. In Proceedings of the 2017 Internet Measurement Conference            [79] Young Xu. 2017. 2017 Update: Comparing Root Server Performance Glob-
     (IMC) (London, United Kingdom).                                                                  ally. thousandeyes.com/blog/2017-update-comparing-root-server-performance-
[67] Sandeep Sarat, Vasileios Pappas, and Andreas Terzis. 2006. On the Use of Anycast                 globally/
     in DNS. In Proceedings of the ACM SIGMETRICS Conference (Banff, Canada). ACM.               [80] Kok-Kiong Yap, Murtaza Motiwala, Jeremy Rahe, Steve Padgett, Matthew Holli-
[68] Brandon Schlinker, Hyojeong Kim, Timothy Cui, Ethan Katz-Bassett, Harsha V.                      man, Gary Baldus, Marcus Hines, Taeeun Kim, Ashok Narayanan, Ankur Jain,
     Madhyastha, Italo Cunha, James Quinn, Saif Hasan, Petr Lapukhov, and Hongyi                      et al. 2017. Taking the Edge off with Espresso: Scale, Reliability and Programma-
     Zeng. 2017. Engineering Egress with Edge Fabric: Steering Oceans of Content to                   bility for Global Internet Peering. In Proceedings of the 2017 ACM SIGCOMM
     the World. In Proceedings of the 2017 ACM SIGCOMM Conference (Los Angeles,                       Conference (Los Angeles, CA, USA). ACM.
     CA, USA). ACM.                                                                              [81] Yingdi Yu, Duane Wessels, Matt Larson, and Lixia Zhang. 2012. Authority Server
[69] Ricardo de Oliveira Schmidt, John Heidemann, and Jan Harm Kuipers. 2017.                         Selection in DNS Caching Resolvers. ACM SIGCOMM Computer Communication
     Anycast Latency: How Many Sites Are Enough? In International Conference on                       Review (April 2012).
     Passive and Active Network Measurement (PAM) (Sydney, Australia). Springer.                 [82] Yaping Zhu, Benjamin Helsley, Jennifer Rexford, Aspi Siganporia, and Sridhar
[70] Neil Spring, Ratul Mahajan, and Thomas Anderson. 2003. The Causes of Path                        Srinivasan. 2012. LatLong: Diagnosing Wide-Area Latency Changes for CDNs.
     Inflation. In Proceedings of the 2003 conference on Applications, technologies, ar-              IEEE Transactions on Network and Service Management (2012).
     chitectures, and protocols for computer communications (Karlsruhe, Germany).




                                                                                           411
                                                                                                                  SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


                                                                                          latency. This decision has a significant effect on conclusions we can
                   1.0                                                                    draw, decreasing daily query counts to root DNS resolution by 20×.
                                                                                             We base this decision on prior work which investigated the
                   0.8
                                                                                          nature of queries with invalid TLDs landing at the roots. ICANN
    CDF of Users




                   0.6                                                                    has found that 28% of queries for non-existent domains at L root
                                                                                          result from captive-portal detection algorithms in Chromium-based
                   0.4
                                                                                          browsers [4]. Researchers at USC have found that more than 90% of
                   0.2                                                Ideal               single-string (not separated by dots) queries at the root match the
                                                                      CDN
                                                                      APNIC
                                                                                          Chromium captive-portal pattern [34]. We remove captive-portal
                   0.0
                    10−3   10−2   10−1        100         101   102           103
                                                                                          detection queries from consideration since they occur on browser
                                    Queries per User per Day                              startup and network reconnect, not during regular browsing, and
Figure 8: Daily queries by users to the root DNS, calculated by amor-                     they can occur in parallel with browsing.
tizing root DNS requests over user populations, when including or                            Some might argue that queries for invalid TLDs are associated
excluding queries for invalid TLDs. Counting invalid queries dras-
                                                                                          with user latency because typos for URLs (when typing into a
tically increases median daily query counts to 22 ( CDN ), a 20-fold
                                                                                          browser search bar, for example) cause users to generate a query
increase, or to 6 ( APNIC ), a 6-fold increase, depending on which user                   to the root servers. However, typos only generate a query to the
data we use.
                                                                                          root server if the TLD is misspelled (as opposed to the hostname).
   Appendices are supporting material that has not been peer-                             Hence typos, in general, cause users latency, but only specific typos
reviewed.                                                                                 will cause users root latency. Moreover, prior work has found that
                                                                                          approximately 60% of queries for invalid TLDs reaching root servers
A              SUMMARY OF DATA                                                            are for domains such as local, no_dot, belkin, and corp [28]. It is
                                                                                          unlikely these queries are caused by typos, since they are actual (as
We use a myriad of datasets in the work, which is a result of our
                                                                                          opposed to misspelled) words and resemble domains often seen in
presenting answers to the questions we pose in several different
                                                                                          software or in corporate networks. Chromium queries and queries
ways (each with strengths and weaknesses). This approach allows
                                                                                          for a certain set of invalid TLDs therefore account for around 86%
us to overcome the limitations of individual datasets, by combining
                                                                                          of all queries for invalid TLDs at the roots, suggesting the vast
multiple views with different tradeoffs. To aid in comprehensibility,
                                                                                          majority of queries we exclude are not directly associated with user
we summarize each of our datasets in Table 2 and Table 3.
                                                                                          latency.
   As an example of how we use multiple views with different
                                                                                             Nevertheless, it is still valuable to assess how including these
tradeoffs, consider the differences between the DITL packet traces
                                                                                          queries for invalid TLDs changes the conclusions we can make
(containing 51.9 billion queries across 50,000 ASes) and our local
                                                                                          about root DNS latency experienced by users. Figure 8 shows daily
DNS / activity measurements (10 thousand measurements, 2 users).
                                                                                          user latencies due to root DNS resolution when we include requests
DITL allows us to see, globally, how recursive resolvers interact
                                                                                          for invalid TLDs and PTR records in daily query volumes. Using
with the root DNS, allowing us to make definitive statements about
                                                                                           CDN user counts, users experience a median of 22 queries to the
global inflation and query volumes. However, DITL does not tell
                                                                                          root DNS each day – about 20× more than when we exclude requests
us how individual users interact with the root DNS, and translat-
                                                                                          for invalid queries (§4). This drastic 20-fold increase is surprising
ing DITL queries to user experience requires heuristic arguments
                                                                                          given we only (roughly) double the amount of queries by including
about caching (§4.3). Our local DNS and activity measurements,
                                                                                          invalid queries. The difference is best explained by the fact that
although limited, give us precise reference points for how root DNS
                                                                                          a majority of invalid queries are generated by /24s with a large
factors into everyday Internet browsing experience, which we find
                                                                                          number of users. Since the y-axis of Figure 8 is the number of users
valuable.
                                                                                          (not /24s), counting invalid queries shifts the graph far to the right.
B            QUANTIFYING THE IMPACT OF                                                    Hence, counting invalid queries drastically affects the conclusions
                                                                                          we can draw. There is a less severe 6-fold increase in the number
             METHODOLOGICAL DECISIONS                                                     of queries per user per data calculated using APNIC data. Overall,
When analyzing latency and inflation, we often make assumptions                           including invalid TLD queries drastically changes our quantitative
or choose to conduct analysis a certain way. In what follows, we jus-                     conclusions about user interaction with the root DNS but may not
tify our various assumptions and pre-processing steps, and analyze                        change our qualitative conclusions, since 20 queries a day to the
the effects of these assumptions on our results.                                          roots is still small.

B.1                  Effect of Removing Invalid TLD Queries                               B.2    Representativeness of Daily Root Latency
In Section 4 we estimate the number of queries users experience                                  Analysis
due to the root DNS by amortizing queries over user populations.                          In Section 4 we estimate the number of queries users experience due
Out of 51.9 billion daily requests to all roots, we observe 31 billion                    to the root DNS by amortizing queries over user populations. To
daily requests for bogus domain names and 2 billion daily requests                        obtain estimates of user populations, we obtain counts of Microsoft
for PTR records. We choose to not count these towards user query                          users who use recursives (§2.1). Naturally recursives used by Mi-
counts, because we believe many of these queries do not lie on the                        crosoft users and recursives seen in DITL do not overlap perfectly.
critical path of user applications and so do not cause user-facing




                                                                                    412
SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


                                                                                Table 2: Summary of Datasets

                                                                         # of                                                # of
                     Dataset                                                                  Duration        Year                    Technology/Format
                                                                     Measurements                                            ASes

                     Sampled CDN Server-Side Logs (§6)                    11.0 ×109           1 week          2019        59 000      Windows TCP/IP, HTTPService (TCP RTT)
                     Sampled CDN Client-Side Measurements (§5.2)          50.0 ×107           1 week          2019        10 600      Odin [17] (HTTP GET)
                     CDN User Counts (§4.3)                                   —               1 month         2019        39 000      Custom URL DNS Requests
                     APNIC User Counts (§4.3)                                 —               updated daily   2019        23 000      Google Ad Delivery Network
                     DITL Packet Traces (§2.1)                            51.9 ×109           2 days          2018        50 300      Packet Traces
                     DITL ∩ CDN (§3, §4.3, §7)                            18.6 ×109           —               2018–2019   35 500      Root DNS query and user counts
                     RIPE Atlas (§5.2, §7.1)                              10.0 ×103           1 hour          Various      3 300      ping, traceroute
                     USC/ISI (§4.3)                                       10.0 ×107           1 year          2018             1      Packet Traces
                     Local DNS / Activity Measurements (§4.3)             68.0 ×104           1 month         2020             2      Packet Traces, Chrome Webtime Tracker


                                                                     Table 3: Strengths and Weaknesses of Datasets
 Dataset                                                      Strengths                                                        Weaknesses
 Sampled CDN Server-Side Logs (§6)                            Has client to front-end mappings, global coverage                Cannot hold user population fixed across rings
 Sampled CDN Client-Side Measurements (§5.2)                  Can hold user population fixed across rings, global coverage     Do not know which front-end the client reached, smaller scale
 CDN User Counts (§4.3)                                       Precise estimates of user counts, global coverage                Under estimates user counts
 APNIC User Counts (§4.3)                                     Global coverage, publicly accessible                             Not validated, coarse granularity
 DITL Packet Traces (§2.1)                                    Global coverage                                                  Noisy, only above the recursive resolver
 DITL ∩ CDN (§3, §4.3, §7)                                    Global coverage, attributes queries to users                     Excludes v6
 RIPE Atlas (§5.2, §7.1)                                      Historic data, reproducibility                                   Limited coverage
 USC/ISI (§4.3)                                               Precise, below the recursive,                                    Limited coverage, no information about users
 Local DNS / Activity Measurements (§4.3)                     Precise, at the end user                                         Limited coverage, small scale



                                                                                                          and act as recursives for similar sets of users. We now justify this
                   1.0                                                                                    decision and discuss the implications of this preprocessing step on
                                                                                                          the results presented in Section 4.3.
                   0.8
                                                                                                             In Table 4 we summarize the extent to which the recursives
    CDF of Users




                   0.6                                                                                    seen by Microsoft are representative of the recursives seen in DITL,
                                                                                                          and vice-versa, without aggregating by /24. We also display cor-
                   0.4
                                                                                                          responding statistics when aggregating by /24 for comparison in
                   0.2                                                          Ideal                     parentheses. Clearly joining by /24 makes a significant difference,
                                                                                CDN
                                                                                APNIC
                                                                                                          increasing various measures of overlap by tens of percents and in
                   0.0
                    10−3       10−2    10−1        100         101        102           103
                                                                                                          certain cases by up to 64%.
                                         Queries per User per Day                                            As an analogy to Figure 3, in Figure 9 we show the number of
Figure 9: A CDF of the number of queries Microsoft users experience                                       queries each Microsoft user executes to the roots per day without
due to root DNS resolution, per day, without joining recursives by
                                                                                                          aggregating query and user statistics by /24 ( CDN ). We also show
/24 in DITL with recursives seen by Microsoft ( CDN ). This unrep-
resentative analysis yields an estimate of daily user queries far, far
                                                                                                           APNIC as in Figure 3 for comparison, even though APNIC is not
lower than in Section 4.3.                                                                                affected by /24 volume aggregation. Users of CDN only send 0.036
                                                                                                          queries to the roots each day at the median – roughly one 30𝑡ℎ of
Table 4: Statistics displaying the extent to which the recursives of                                      the estimate obtained when aggregating statistics by /24. This small
users in Microsoft’s CDN overlap recursives seen in the 2018 DITL                                         daily user latency makes sense, given that we only capture 8.4% of
captures without users and volumes by /24. Also shown in paren-                                           DITL volume without joining the datasets by /24 (Table 4).
theses are corresponding statistics when joining by /24. Joining the                                         Table 4 and Figure 9, demonstrate that the decision to aggregate
datasets by /24 increases most measures of representation by tens of                                      statistics and join DITL captures with Microsoft user counts by /24
percents, with some measures increased by up to 64%.                                                      led to both much greater representativeness of the analysis and very
 dataset                       Statistic          Percent Overlap (by /24)                                different conclusions about user interactions with the root DNS.
                               DITL Recursives    2.45% (29.3%) of DITL Recursives                        We would now like to justify this decision using measurements. If,
                               DITL Volume        8.4% (72.2%) of DITL Query Volume                       as we assume, IP addresses in the same /24 are colocated, they are
 DITL ∩ CDN
                               CDN Recursives     41.9% (78.8%) of CDN Recursives
                                                                                                          probably routed similarly. Prior work has shown that only a small
                               CDN Volume         47.05% (88.1%) of CDN Query Volume
                                                                                                          fraction of anycast paths are unstable [77], and so we expect that,
                                                                                                          over the course of DITL, IP addresses in the same /24 reach the
To increase the representativeness of our analysis, we aggregate                                          same anycast sites.
Microsoft user counts and DITL query volumes by resolver /24,                                                As a way of quantifying routing similarity in a /24, in Figure 10
and join the two datasets on /24 to create the DITL∩CDN dataset.                                          we show the percent of queries from each /24 in DITL that do not
The intuition behind this preprocessing step is that IP addresses in                                      reach the most “popular” anycast site for each /24 in each root
the same /24 are likely colocated, owned by the same organization,                                        deployment. We label root letters alongside the total number of




                                                                                                   413
                                                                                                                                              SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


                                                                                                      for both 2018 and 2020 DITLs, G root is not included and I root is
                  1.0
                                                                         B Root (2G 2T)               completely anonymized.)
                                                                         A Root (5G 5T)
                  0.8
                                                                         M Root (5G 6T)
                                                                         C Root (10G 10T)
    CDF of /24s




                  0.6                                                    E Root (15G 85T)
                                                                         D Root (20G 117T)
                                                                         K Root (52G 53T)                                1.0
                  0.4                                                    J Root (68G 110T)
                                                                         F Root (94G 141T)                               0.8
                  0.2                                                    L Root (138G 138T)




                                                                                                          CDF of Users
                                                                                                                         0.6
                  0.0
                        0.0            0.2           0.4             0.6           0.8
                                                                                                                         0.4
                        Fraction of Queries Generated by /24 That Did Not Go To Favorite Site
Figure 10: Fractions of queries generated by /24s that do not hit the                                                                                                                       Ideal
                                                                                                                         0.2
most popular site for each /24 and for each root letter in question.                                                                                                                        CDN
The legend indicates the number of global sites (G) and total (global                                                                                                                       APNIC
                                                                                                                         0.0
and local) sites (T). For all root letters, more than 80% of /24s have                                                    10−3      10−2        10−1        100         101         102             103
                                                                                                                                                  Queries per User per Day
all queries visit the most popular site, suggesting queries from the
same /24 are usually routed similarly.                                                                                                                      (a)


sites (local and global) that they had during the 2018 DITL. For each
root letter and for each /24 that queried that root letter in DITL, we                                                   1.0
                                                                                                                         0.9
look at how queries from the /24 are distributed among sites.                                                            0.8
   Let 𝑞𝑖𝑘𝑗 be the number of daily queries from IP 𝑖 in /24 𝑘 toward                                                     0.7


                                                                                                          CDF of Users
                                                                                                                                                                                          M-8
anycast site 𝑗. We then calculate the fraction of queries that do not                                                    0.6                                                              H-8
                                                                                                                         0.5                                                              C - 10
visit the most “popular” site as                                                                                                                                                          D - 23
                                                                                                                         0.4
                                                                                                                                                                                          A - 51
                                                                                                                         0.3
                                                          ∑︁ 𝑞𝑖𝑘𝑗                                                        0.2
                                                                                                                                                                                          K - 75
                                               𝑘                    𝐹                                                                                                                     J - 127
                                             𝑓 =1−                     (3)                                               0.1                                                              All Roots
                                           𝑘
                                      𝑖 𝑄                                                                                0.0
                                                                                                                               0   20       40        60         80       100      120       140
   where 𝑗𝐹 is the favorite site for /24 𝑘 (i.e., the site the /24 queries                                                                 Geographic Inflation per Root Query (ms)

the most), and 𝑄 𝑘 is the total number of queries from /24 𝑘. We plot                                                                                       (b)
these fractions for all /24s in DITL, and for each root deployment.                                   Figure 11: Queries per user per day to the root DNS and inflation of
(We do not include /24s that had only one IP from the /24 visit the                                   root letters calculated using the 2020 DITL. Our high level conclu-
root letter in question.)                                                                             sions about how much inflation is in the root DNS and the number
   For more than 80% of /24s, all queries visit only one site per root                                of queries users experience per day do not change depending on the
                                                                                                      year.
letter, suggesting that queries from the same /24 are routed similarly.
This analysis is slightly biased by the size of the root deployment.                                     For the 2020 DITL specifically, B root was not available at the
For example, two IP addresses selected at random querying B root                                      time of writing (but may be in the future), E root includes only one
would hit the same site half the time, on average. However, even                                      site (out of 132), F root does not include any Cloudflare sites (more
for L root, with 138 sites, more than 90% of /24s direct all queries to                               than half the volume), and L root is completely anonymized (hence
the most popular site. We believe Figure 10 provides evidence that                                    unusable). The 2018 DITL has none of these limitations, and so our
recursives within the same /24 prefix are located near each other,                                    results apply to more letters. Studying the root DNS system as a
and hence serve similar sets of users.                                                                whole is a key strength of our analysis compared to prior work, so
   Even queries from a single IP address within a /24 may reach                                       we feel coverage is more important than having the most up-to-date
multiple sites for a single root over the course of the DITL cap-                                     results for only a subset of root letters.
tures. Such instability can make routing look less coherent across                                       For completeness, and to demonstrate that our larger takeaways
IP addresses in a /24, even if they are all routed the same way. Con-                                 about root DNS latency and inflation do not change significantly
trolling for cases of changing paths for the same IP makes intra-/24                                  from year to year, we calculate queries per day (as in Figure 3) and
routing even more coherent. If we let the distribution of queries                                     inflation (as in Figure 2) for the root letters for which we have data,
generated by an IP address to a root be a point mass, with all the                                    and the results are shown in Figure 11.
queries concentrated at that IP addresses’ favorite site, all queries                                    Our high level conclusions about root DNS latency do not change
from more than 90% of all /24s to all roots are routed to the same                                    when looking at the 2020 DITL – most users still experience about
site (not shown).                                                                                     one DNS query per day, and the number of root queries sent by
                                                                                                      recursives is still far from the ‘ideal’ querying behavior of one
B.3                 Implications of Using the 2018 DITL                                               record per TTL. Inflation results are also similar – individual root
At the time of writing, the 2020 DITL was available to use in the                                     letters have less inflation (for example, D root improved). Average
study, but we chose to use the 2018 study since the 2018 study                                        geographic inflation is almost exactly the same as in 2018, with
had better coverage of root letters. (Neither has perfect coverage –                                  approximately 10% of users experiencing more than 20 ms (2,000
                                                                                                      km) of inflation.




                                                                                                414
SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


C    NUMBER OF RTTS IN A PAGE LOAD                                           with dynamic content suggested to us by a CDN operator. We use
To estimate the latency a user experiences when interacting with             Selenium and Chrome to open web pages and use Tshark [24] to
Microsoft’s CDN (§5.2), we first estimate the number of RTTs re-             capture TCP packets during the page load. When the browser’s
quired to load a typical web page hosted by Microsoft’s CDN. The             loadEventEnd event fires, the whole page has loaded, including
number of RTTs in a page load depends on a variety of factors, so            all dependent resources such as stylesheets and images [59]. So, to
we aim to find a reasonable lower bound on the number of RTTs                calculate the total data size for each connection, we use the ACK
users incur for typical pages. A lower bound on the number of                value in the last packet sent to the server before loadEventEnd
RTTs to load pages is a conservative measure of the impact of                minus the SEQ value in the first packet received from the server.
CDN inflation, as latency inflation accumulates with each addi-              We then calculate the number of RTTs using Equation (4), and add
tional RTT, and larger pages (more RTTs) would be impacted more.             a final two RTTs for TCP and TLS handshakes. We find only a few
We provide an estimate of this lower bound based on modeling                 percent of CDN web pages are loaded within 10 RTTs, and 90% of
and evaluation of a set of web pages hosted by Microsoft’s CDN               all page loads are loaded within 20 RTTs, so 10 RTTs is a reasonable
using Selenium (a headless web browser), finding that 10 RTTs is             lower bound.
a reasonable estimate. We scale latency by the number of RTTs in
Section 5.2 to demonstrate how improvements in latency help users            D                    LATENCY MEASUREMENTS AT A
(and, conversely, how inflation hurts users).                                                     RECURSIVE RESOLVER
   Users incur latency to Microsoft’s CDN when they download                 To obtain a local perspective of how users experience root DNS
web objects via HTTP. We calculate the number of RTTs required               latency, we use packet traces from ISI. Here, we characterize DNS
to download objects in each connection separately, and sum RTTs              and root DNS latencies users experience at the resolver, along with
over connections while accounting for parallel connections. For              a useful visualization of how inconsequential root DNS latency is
a single TCP connection, the number of RTTs during a page load               for users at this resolver. This analysis complements our global
depends on the size of files being downloaded. This relationship is          view of how users interact with the root DNS in Section 4.3, as it
approximated by                                                              demonstrates how often everyday users might send queries to the
                                                                             root relative to other DNS queries.
                                      𝐷
                            𝑁 = 𝑙𝑜𝑔2                             (4)
                                       𝑊
   where 𝑁 is the number of RTTs, 𝐷 is the total number of bytes
sent by the TCP connection from the server to the user, and 𝑊 is                                  1.0
the initial congestion window size in bytes [19, 35]. Although 𝑊
is set by the server, Microsoft and a majority of web pages [66]                                  0.8
                                                                                 CDF of Queries




set this value to approximately 15 kB so we use this value. We
                                                                                                  0.6
do not consider QUIC or persistent connections across pages in
detail here, but larger initial windows will result in fewer RTTs.                                0.4
We test mostly landing pages, for which persistent connections
are uncommon. Moreover, such considerations likely would not                                      0.2
change our qualitative conclusions about how users experience
CDN latency.                                                                                      0.0

   We make the following assumptions to establish a lower bound                                         10−2   10−1   100   101      102   103   104   105
                                                                                                                            Latency (ms)
on 𝑁 : (1) we do not account for connections limited by the receive          Figure 12: CDF of user DNS query latencies seen at a recursive resolve
window or the application, as the RTT-based congestion window                at ISI, over the course of one year. Latencies are measured from the
limitation we calculate is still a lower bound, (2) TCP is always in         timestamp when the recursive resolver receives a client query to the
slow start mode, which implies the window size doubles each RTT              timestamp when the recursive sends a response to that client query.
and serves as a lower bound on the actual behavior of Microsoft’s            The sub-millisecond latency for more than half of queries suggests
standard CUBIC implementation, and (3) all TCP and TLS hand-                 most queries to this recursive are served by the local cache.
shakes after the first do not incur additional RTTs (i.e., they are
                                                                                Figure 12 shows the latencies of all queries seen at the recur-
executed in parallel to other requests).
                                                                             sive resolver over one year, where latencies are measured from the
   Modern browsers can open many TCP connections in parallel,
                                                                             timestamp when the recursive resolver receives a client query to the
to speed up page loads. Summing up RTTs across parallel connec-
                                                                             timestamp when the recursive sends a response to that client query.
tions could therefore drastically overestimate the number of RTTs
                                                                             Latencies are divided into (roughly) 3 regions: sub-millisecond la-
experienced users. To determine the connections over which to
                                                                             tency, low latency (millisecond - tens of milliseconds), and high
accumulate RTTs, we first start by only considering the connec-
                                                                             latency (hundreds of milliseconds). The first region corresponds to
tion with the most data. We then iteratively add connections in
                                                                             cached queries, so roughly half of queries are (probably) cached.
size-order (largest to smallest) that do not overlap temporally with
                                                                             The second region corresponds to DNS resolutions for which the
other connections for which we have accumulated RTTs. The ‘data
                                                                             resolving server was geographically close. Finally, the third region
size’ of a connection may represent one or more application-layer
                                                                             likely corresponds to queries that had to travel to distant servers,
objects.
   We load nine web pages owned by Microsoft, twenty times for               or required a few rounds of recursion to fully resolve the domain.
each page. We choose popular pages hosted on Microsoft’s CDN




                                                                       415
                                                                                                                  SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


                                                                                           Chrome. While loading web pages, we collect network packets on
                 0.999999
                                                                                           port 53 using Tshark [24].
                  0.99999                                                                      For these page loads, we observe 69,215 DNS A & AAAA-type
                   0.9999
                                                                                           requests generated by the recursive resolver. 3,137 of these requests
CDF of Queries




                                                                                           are sent to root servers, and 2,950 of these root DNS queries are
                    0.999                                                                  redundant. Over 70% of redundant requests are AAAA-type. After
                     0.99                                                                  investigating the cause of these redundant queries, we find over 90%
                                                                                           of these redundant requests follow a similar pattern. This pattern
                      0.9
                                                                                           is illustrated by the example in Table 5.
                      0.0
                            0   50   100      150        200       250   300   350
                                                                                               In Table 5, we show queries the recursive resolver makes when
                                           Root DNS Latency (ms)                           a user queries for the A record of bidder.criteo.com. In step 1, the
 Figure 13: Root DNS latency for queries made by users of ISI recursive                    recursive resolver receives a DNS query from a client. According
 resolver during 2018. This plot demonstrates the benefits of caching                      to TTL heuristics, the COM A record is in the cache. In step 3, the
 and high TTLs of TLD records – fewer than 1% of queries generate a
                                                                                           TLD server responds with records of authoritative nameservers for
 root request, and fewer than 0.1% incur latencies greater than 100 ms.
                                                                                           “criteo.com”. Then, the recursive chooses one of them to issue the
 User queries that did not generate a query to a root server were given
 a latency of 0.                                                                           following request to. However, for some reason (e.g., packet loss),
                                                                                           the recursive resolver does not get a response from the nameserver
 The sub-millisecond latency for more than half of queries suggests                        in step 4. Hence, the resolver uses another nameserver in step 5,
 most queries to this recursive are served by the local cache. These                       which it learned in step 3. At the same time, as seen in step 6 to
 latencies are similar to those presented in previous work that also                       11, the recursive sends (redundant) DNS requests to root servers,
 studied a recursive resolver serving a small user population [18].                        querying the AAAA-type records for these nameservers. These re-
 Queries in the second and third regions include queries that did                          quests are redundant since the AAAA record for COM was received
 not query the root (since those records were cached) but did query                        less than two days ago.
 other parts of the DNS hierarchy.                                                             From the pattern demonstrated in Table 5, we hypothesize that
    As discussed in Section 4, root DNS queries make up a small                            redundant requests to the root servers will be generated for certain
 fraction of all queries shown in Figure 12. To visualize just how                         records when the following conditions are met.
 small this fraction is, Figure 13 shows a CDF of root DNS latency                             (1) A query from the recursive resolver to an authoritative name-
 experienced for queries over 2018. Requests that do not generate                                  server times-out.
 a query to a root server are counted as having a root latency of                              (2) The record queried for by the resolver to the root DNS server
 0. Figure 13 demonstrates the benefits of shared caches and high                                  was not included in the Additional Records section of the
 TTLs of TLD records – fewer than 1% of queries generate a root                                    TLD’s response.
 request, and fewer than 0.1% incur latencies greater than 100 ms.
                                                                                               The second condition is also why we were seeing more AAAA-
                                                                                           type redundant requests, because usually there are more A-type
 E                   CASE STUDY: REDUNDANT ROOT DNS                                        records in the Additional Records section than AAAA-type records.
                     QUERIES                                                                   To see how much traffic is caused by our hypothesis in a real
When we investigate the traffic from a recursive resolver to the                           scenario, we analyze packet captures on a recursive resolver (BIND
root servers in Section 4, we see as many as 900 queries to the root                       9.11.17) serving users at ISI. To keep consistent with the other
server in a day for the COM NS record. Given the 2 day TTL of                              analysis we do on this dataset (§4), we use packet captures from
this record, this query frequency is unexpectedly large. This large                        2018. 79.8% of requests to roots are redundant and in the pattern
frequency motivated us to analyze why these requests to roots                              we described. The other 20.2% consists of necessary requests and
occurred. We consider a request to the root to be redundant if a                           requests for which we have no hypothesis as to how they were
query for the same record occurred less than 1 TTL ago. Prior work                         generated. We contacted developers at BIND, who said this may be
has investigated redundant requests to root servers as well, and                           a bug.
our analysis can be considered complementary since we discover                                 Software behavior as described here can lead to orders of magni-
different reasons for redundant requests [28].                                             tude more root DNS requests than would be necessary if recursives
   To observe these redundant requests in a controlled environment,                        queried for the record once per TTL. As demonstrated in Figure 3,
we deploy a BIND instance (the resolver in Section 2.1 runs BIND                           focusing on reducing the number of these queries could both im-
v9.11.17) locally and enable cache and recursion. We do not actually                       prove user experience and reduce load on the root server.
look up the cache of the local BIND instance to see which records
are in it. Instead, we save the TTL of the record and the timestamp                        F    VISUALIZATION OF MICROSOFT CDN
at which we receive the record to know if the record should be in                               PERFORMANCE
BIND’s cache. We use BIND version 9.11.18 and 9.16.1. Because
                                                                                           In Section 2.2 we show the rings of a large anycast CDN and how
9.16.1 is one of the newest releases and 9.11.18 is a release from
                                                                                           users are distributed with respect to those rings. This visualization
several years ago, we can assume that pathological behavior is
                                                                                           does not include any information about latency, so we provide one
common in all versions between these two releases. After deploying
                                                                                           here. In Figure 14 we show front-ends in R110, and associated la-
the instance, we simulate user behavior by opening the top-1000
web pages according to GTmetrix [33] using Selenium and headless                           tency users experience to R110 in each region. Transparent circles




                                                                                     416
SIGCOMM ’21, August 23–27, 2021, Virtual Event, USA


Table 5: Redundant root DNS requests. The last five requests to J root are redundant which may be caused by an unanswered request in step 4.
         Relative
 Step                              From                    To                                 Query name          Query type   Response
         Timestamp (second)
 1       0.00000                   client                  resolver                           bidder.criteo.com   A
 2       0.01589                   resolver                192.42.93.30 (g.gtld)              bidder.criteo.com   A
                                                                                                                               ns23.criteo.com ns22.criteo.com
 3       0.02366                   192.42.93.30 (g.gtld)   resolver                           bidder.criteo.com   A            ns25.criteo.com ns26.criteo.com
                                                                                                                               ns27.criteo.com ns28.criteo.com.
 4       0.02387                   resolver                74.119.119.1 (ns25.criteo.com)     bidder.criteo.com   A
 5       0.82473                   resolver                182.161.73.4 (ns28.criteo.com)     bidder.criteo.com   A
 6       0.82555                   resolver                192.58.128.30 (j.root)             ns22.criteo.com     AAAA
 7       0.82563                   resolver                192.58.128.30 (j.root)             ns23.criteo.com     AAAA
 8       0.82577                   resolver                192.58.128.30 (j.root)             ns27.criteo.com     AAAA
 9       0.82584                   resolver                192.58.128.30 (j.root)             ns25.criteo.com     AAAA
 10      0.82592                   resolver                192.58.128.30 (j.root)             ns26.criteo.com     AAAA
 11      0.82620                   resolver                192.58.128.30 (j.root)             ns28.criteo.com     AAAA


                                                                                                                                                       1.0




                                                                                                                                                       0.8




                                                                                                                                                             Latency (relative)
                                                                                                                                                       0.6




                                                                                                                                                       0.4




                                                                                                                                                       0.2




                                                                                                                                                       0.0

Figure 14: A visualization of front-ends in R110 (purple Xs), and user populations (transparent circles). User populations are colored according
to the relative latency they experience and have size proportional to user population. Red corresponds to high latency, and green corresponds
to low latency. Latency generally gets lower the closer users are to a front-end, and front-ends are concentrated around large user populations.

represent user populations and their radii are proportional to the                       generally gets lower the closer users are to a front-end. The CDN
user population. Population circles are colored according to average                     has focused on deploying front-ends near large user populations,
median latency users in the metro experience to R110 – red indi-                         which has driven latencies quite low for nearly all users.
cates higher latency while green indicates lower latency. Latency




                                                                                   417
