                                                                                                                            PDF Download
                                                                                                                            2815675.2815717.pdf
                                                                                                                            21 March 2026
                                                                                                                            Total Citations: 115
                                                                                                                            Total Downloads: 1013
    .
    .
        Latest updates: hps://dl.acm.org/doi/10.1145/2815675.2815717




                                                                                                                            .
                                                                                                                            .
                                                                                                                 Published: 28 October 2015
        .
        .
                                                                                                                 .
    SHORT-PAPER




                                                                                                                 .
                                                                                                                 Citation in BibTeX format
    Analyzing the Performance of an Anycast CDN




                                                                                                                 .
                                                                                                                 .
                                                                                                                 IMC '15: Internet Measurement
                                                                                                                 Conference
    MATT CALDER, University of Southern California, Los Angeles, CA, United States                               October 28 - 30, 2015
    .
                                                                                                                 Tokyo, Japan
    ASHLEY FLAVEL, Microso Corporation, Redmond, WA, United States




                                                                                                                 .
                                                                                                                 .
                                                                                                                 Conference Sponsors:
    .
    ETHAN KATZ-BASSETT, University of Southern California, Los Angeles, CA, United States                        SIGCOMM
                                                                                                                 SIGMETRICS
    .
    RATUL MAHAJAN, Microso Corporation, Redmond, WA, United States
    .
    JITENDRA PADHYE, Microso Corporation, Redmond, WA, United States
    .
    .
    .
    Open Access Support provided by:
    .
    University of Southern California
    .
    Microso Corporation
    .
                                                                        IMC '15: Proceedings of the 2015 Internet Measurement Conference (October 2015)
                                                                                                                   hps://doi.org/10.1145/2815675.2815717
                                                                                                                                      ISBN: 9781450338486
.
                   Analyzing the Performance of an Anycast CDN
     Matt Calder*,† , Ashley Flavel† , Ethan Katz-Bassett* , Ratul Mahajan† , and Jitendra Padhye†
                                                        † Microsoft           * University of Southern California




ABSTRACT                                                                                               Some newer CDNs like CloudFlare rely on anycast [1], announc-
Content delivery networks must balance a number of trade-offs                                       ing the same IP address(es) from multiple locations, leaving the
when deciding how to direct a client to a CDN server. Whereas                                       client-front-end mapping at the mercy of Internet routing protocols.
DNS-based redirection requires a complex global traffic manager,                                    Anycast offers only minimal control over client-front-end mapping
anycast depends on BGP to direct a client to a CDN front-end. Any-                                  and is performance agnostic by design. However, it is easy and
cast is simple to operate, scalable, and naturally resilient to DDoS                                cheap to deploy an anycast-based CDN – it requires no infrastruc-
attacks. This simplicity, however, comes at the cost of precise con-                                ture investment, beyond deploying the front-ends themselves. The
trol of client redirection. We examine the performance implications                                 anycast approach has been shown to be quite robust in practice [23].
of using anycast in a global, latency-sensitive, CDN. We analyze                                       In this paper, we aim to answer the questions: Does anycast direct
millions of client-side measurements from the Bing search service                                   clients to nearby front-ends? What is the performance impact of
to capture anycast versus unicast performance to nearby front-ends.                                 poor redirection, if any? To study these questions, we use data from
We find that anycast usually performs well despite the lack of pre-                                 Bing’s anycast-based CDN [23]. We instrumented the search stack
cise control but that it directs roughly 20% of clients to a suboptimal                             so that a small fraction of search response pages carry a JavaScript
front-end. We also show that the performance of these clients can                                   beacon. After the search results display, the JavaScript measures
be improved through a simple history-based prediction scheme.                                       latency to four front-ends– one selected by anycast, and three nearby
                                                                                                    ones that the JavaScript targets. We compare these latencies to
                                                                                                    understand anycast performance and determine potential gains from
Categories and Subject Descriptors                                                                  deploying a DNS solution.
C.2.5 [Computer-Communication Networks]: Local and Wide-                                               Our results paint a mixed picture of anycast performance. For
Area Networks—Internet; C.4 [Performance of Systems]: Mea-                                          most clients, anycast performs well despite the lack of centralized
surement techniques                                                                                 control. However, anycast directs around 20% of clients to a sub-
                                                                                                    optimal front-end. When anycast does not direct a client to the best
                                                                                                    front-end, we find that the client usually still lands on a nearby alter-
Keywords                                                                                            native front-end. We demonstrate that the anycast inefficiencies are
                                                                                                    stable enough that we can use a simple prediction scheme to drive
Anycast; CDN; Measurement;
                                                                                                    DNS redirection for clients underserved by anycast, improving per-
                                                                                                    formance of 15%-20% of clients. Like any such study, our specific
1.     INTRODUCTION                                                                                 conclusions are closely tied to the current front-end deployment of
   Content delivery networks are a critical part of Internet infras-                                the CDN we measure. However, as the first study of this kind that we
tructure. CDNs deploy front-end servers around the world and                                        are aware of, the results reveal important insights about CDN per-
direct clients to nearby, available front-ends to reduce bandwidth,                                 formance, demonstrating that anycast delivers optimal performance
improve performance, and maintain reliability. We will focus on                                     for most clients.
a CDN architecture which directs the client to a nearby front-end,
which terminates the client’s TCP connection and relays requests to
a backend server in a data center. The key challenge for a CDN is
                                                                                                    2.    CLIENT REDIRECTION
to map each client to the right front-end. For latency-sensitive ser-                                  A CDN can direct a client to a front-end in multiple ways.
vices such as search results, CDNs try to reduce the client-perceived                               DNS: The client will fetch a CDN-hosted resource via a hostname
latency by mapping the client to a nearby front-end.                                                that belongs to the CDN. The client’s local DNS resolver (LDNS),
   CDNs can use several mechanisms to direct the client to a front-                                 typically configured by the client’s ISP, will receive the DNS request
end. The two most popular mechanisms are DNS and anycast.                                           to resolve the hostname and forward it to the CDN’s authoritative
DNS-based redirection was pioneered by Akamai. It offers fine-                                      nameserver. The CDN makes a performance-based decision about
grained and near-real time control over client-front-end mapping,                                   what IP address to return based on which LDNS forwarded the
but requires considerable investment in infrastructure and opera-                                   request. DNS redirection allows relatively precise control to redirect
tions [35].                                                                                         clients on small timescales by using small DNS cache TTL values.
                                                                                                       Since a CDN must make decisions at the granularity of LDNS
Permission to make digital or hard copies of all or part of this work for personal or
                                                                                                    rather than client, DNS-based redirection faces some challenges.
classroom use is granted without fee provided that copies are not made or distributed
for profit or commercial advantage and that copies bear this notice and the full cita-
                                                                                                    An LDNS may be distant from the clients that it serves or may serve
tion on the first page. Copyrights for components of this work owned by others than                 clients distributed over a large geographic region, such that there
ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or re-                is no good single redirection choice an authoritative resolver can
publish, to post on servers or to redistribute to lists, requires prior specific permission         make. This situation is very common with public DNS resolvers
and/or a fee. Request permissions from Permissions@acm.org.                                         such as Google Public DNS and OpenDNS, which serve large, ge-
IMC’15, October 28–30, 2015, Tokyo, Japan.
                                                                                                    ographically disparate sets of clients [17]. A proposed solution to
Copyright is held by the owner/author(s). Publication rights licensed to ACM.
ACM 978-1-4503-3848-6/15/10 ...$15.00.
                                                                                                    this issue is the EDNS client-subnet-prefix standard (ECS) which
DOI: http://dx.doi.org/10.1145/2815675.2815717.                                                     allows a portion of the client’s actual IP address to be forwarded




                                                                                              531
to the authoritative resolver, allowing per-prefix redirection deci-             3.2.1     Passive Measurements
sions [21].                                                                        Bing server logs provide detailed information about client re-
Anycast: Anycast is a routing strategy where the same IP address                 quests for each search query. For our analysis we use the client IP
is announced from many locations throughout the world. Then                      address, location, and what front-end was used during a particular
BGP routes clients to one front-end location based on BGP’s notion               request. This data set was collected on the first week of April 2015
of best path. Because anycast defers client redirection to Internet              and represents many millions of queries.
routing, it offers operational simplicity. Anycast has an advantage
over DNS-based redirection in that each client redirection is handled            3.2.2     Active Measurements
independently – avoiding the LDNS problems described above.                         To actively measure CDN performance from the client, we inject
   Anycast has some well-known challenges. First, anycast is un-                 a JavaScript beacon into a small fraction of Bing Search results.
aware of network performance, just as BGP is, so it does not react               After the results page has completely loaded, the beacon instructs
to changes in network quality along a path. Second, anycast is un-               the client to fetch four test URLs. These URLs trigger a set of DNS
aware of server load. If a particular front-end becomes overloaded,              queries to our authoritative DNS infrastructure. The DNS query
it is difficult to gradually direct traffic away from that front-end,            results are randomized front-end IPs for measurement diversity,
although there has been recent progress in this area [23]. Simply                which we discuss more in § 3.3.
withdrawing the route to take that front-end offline can lead to cas-               The beacon measures the latency to these front-ends by down-
cading overloading of nearby front-ends. Third, anycast routing                  loading the resources pointed to by the URLs, and reports the results
changes can cause ongoing TCP sessions to terminate and need to                  to a backend infrastructure. Our authoritative DNS servers also push
be restarted. In the context of the Web, which is dominated by                   their query logs to the backend storage. Each test URL has a glob-
short flows, this does not appear to be an issue in practice [31, 23].           ally unique identifier, allowing us to join HTTP results from the
Many companies, including Cloudflare, CacheFly, Edgecast, and                    client side with DNS results from the server side [34].
Microsoft, run successful anycast-based CDNs.                                       The JavaScript beacon implements two techniques to improve
Other Redirection Mechanisms: Whereas anycast and DNS direct                     quality of measurements. First, to remove the impact of DNS lookup
a client to a front-end before the client initiates a request, the re-           from our measurements, we first issue a warm-up request so that
sponse from a front-end can also direct the client to a different server         the subsequent test will use the cached DNS response. While DNS
for other resources, using, for example, HTTP status code 3xx or                 latency may be responsible for some aspects of poor Web-browsing
manifest-based redirection common for video [4]. These schemes                   performance [5], in this work we are focusing on the performance
add extra RTTs, and thus are not suitable for latency-sensitive Web              of paths between client and front-ends. We set TTLs longer than
services such as search. We do not consider them further in this                 the duration of the beacon. Second, using JavaScript to measure
paper.                                                                           the elapsed time between the start and end of a fetch is known to not
                                                                                 be a precise measurement of performance [32], whereas the W3C
                                                                                 Resource Timing API [29] provides access to accurate resource
3.    METHODOLOGY                                                                download timing information from compliant Web browsers. The
   Our goal is to answer two questions: 1) How effective is anycast              beacon first records latency using the primitive timings. Upon
in directing clients to nearby front-ends? And 2) How does anycast               completion, if the browser supports the resource timing API, then
performance compare against the more traditional DNS-based uni-                  the beacon substitutes the more accurate values.
cast redirection scheme? We experiment with Bing’s anycast-based                    We study measurements collected from many millions of search
CDN to answer these questions. The CDN has dozens of front end                   queries over March and April 2015. We aggregated client IP ad-
locations around the world, all within the same Microsoft-operated               dresses from measurements into /24 prefixes because they tend to
autonomous system. We use measurements from real clients to                      be localized [27]. To reflect that the number of queries per /24 is
Bing CDN front-ends using anycast and unicast. In § 4, we com-                   heavily skewed across prefixes [35], for both the passive and ac-
pare the size of this CDN to others and show how close clients are               tive measurements, we present some of our results weighting the
to the front ends.                                                               /24s by the number of queries from the prefix in our corresponding
                                                                                 measurements.
3.1     Routing Configuration
   All test front-ends locations have both anycast and unicast IP                3.3     Choice of Front-ends to Measure
addresses.                                                                          The main goal of our measurements is to compare the perfor-
Anycast: Bing is currently an anycast CDN. All production search                 mance achieved by anycast with the performance achieved by di-
traffic is current served using anycast from all front-ends.                     recting clients to their best performing front-end. Measuring from
                                                                                 each client to every front-end would introduce too much overhead,
Unicast: We also assign each front-end location a unique                         but we cannot know a priori which front-end is the best choice for
/24 prefix which does not serve production traffic. Only the routers             a given client at a given point in time.
at the closest peering point to that front-end announce the prefix,                 We use three mechanisms to balance measurement overhead with
forcing traffic to the prefix to ingress near the front-end rather than          measurement accuracy in terms of uncovering the best performing
entering Microsoft’s backbone at a different location and traversing             choices and obtaining sufficient measurements to them. First, for
the backbone to reach the front-end. This routing configuration                  each LDNS, we consider only the ten closest front-ends to the LDNS
allows the best head-to-head comparison between unicast and                      (based on geolocation data) as candidates to consider returning to
anycast redirection, as anycast traffic ingressing at a particular               the clients of that LDNS. Recent work has show that LDNS is a
peering point will also go to the closest front-end.                             good approximation of client location: excluding 8% of demand
                                                                                 from public resolvers, only 11-12% of demand comes from clients
3.2     Data Sets                                                                who are further than 500km from their LDNS [17]. In Figure 1, we
   We use both passive and active measurements in our study, as                  will show that our geolocation data is sufficiently accurate that the
discussed below.                                                                 best front-ends for the clients are generally within that set. Second,




                                                                           532
                           1                                                                                              1
                                                                                                                                     1st Closest
                          0.9
                                                                                                                                    2nd Closest




                                                                                              weighted by query volume
                          0.8                                                                                            0.8        3rd Closest
                                                                                                                                    4th Closest
                          0.7




                                                                                                   CDF of Clients
            CDF of /24s   0.6                                                                                            0.6
                          0.5
                          0.4                                                                                            0.4

                          0.3                         9 front-ends
                                                      7 front-ends
                          0.2                                                                                            0.2
                                                      5 front-ends
                          0.1                         3 front-ends
                                                       1 front-end
                           0                                                                                              0
                                0   50         100          150      200                                                       64     128     256   512   1024 2048 4096 8192

                                         Min Latency (ms)                                                                      Client Distance to Nth Closest Front-end (km)


Figure 1: Diminishing returns of measuring to additional front-ends.              Figure 2: Distances in kilometers (log scale) from volume-weighted
The close grouping of lines for the 5th+ closest front-ends suggests that         clients to nearest front-ends.
measuring to additional front-ends provides negligible benefit.

                                                                                  and ChinaCache’s deployments outside of China) have between 17
to further reduce overhead, each beacon only makes four measure-                  locations (CDNify) and 62 locations (Level3). In terms of number
ments to front-ends: (a) a measurement to the front-end selected                  of locations and regional coverage, the Bing CDN is most similar
by anycast routing; (b) a measurement to the front-end judged to be               to Level3 and MaxCDN. Well-known CDNs with smaller deploy-
geographically closest to the LDNS; and (c-d) measurements to two                 ments include Amazon CloudFront (37 locations), CacheFly (41
front-ends randomly selected from the other nine candidates, with                 locations), CloudFlare (43 locations) and EdgeCast (31 locations).
the likelihood of a front-end being selected weighted by distance                 CloudFlare, CacheFly, and EdgeCast are anycast CDNs.
from the client LDNS (e.g. we return the 3rd closest front-end with                  To give some perspective on the density of front-end distribu-
higher probability than the 4th closest front-end). Third, for most               tion, Figure 2 shows the distance from clients to nearest front-ends,
of our analysis, we aggregate measurements by /24 and consider                    weighted by client Bing query volumes. The median distance of the
distributions of performance to a front-end, so our analysis is robust            nearest front-end is 280 km, of the second nearest is 700 km, and
even if not every client measures to the best front-end every time.               of fourth nearest is 1300 km.
   To partially validate our approach, Figure 1 shows the distribution
of minimum observed latency from a client /24 to a front-end. The
labeled Nth line includes latency measurements from the nearest
                                                                                  5.    ANYCAST PERFORMANCE
N front-ends to the LDNS. The results show decreasing latency                        We use measurements to estimate the performance penalty any-
as we initially include more front-ends, but we see little decrease               cast pays in exchange for simple operation. Figure 3 is based on
after adding five front-ends per prefix, for example. So, we do not               millions of measurements, collected over a period of a few days,
expect that minimum latencies would improve for many prefixes if                  and inspired us to take on this project.
we measured to more than the nearest ten front-ends that we include                  As explained in § 3, each execution of the JavaScript beacon
in our beacon measurements.                                                       yields four measurements, one to the front-end that anycast selects,
                                                                                  and three to nearby unicast front-ends. For each request, we find the
                                                                                  latency difference between anycast and the lowest-latency unicast
4.    CDN SIZE AND GEO-DISTRIBUTION                                               front-end. Figure 3 shows the fraction of requests where anycast
   The results in this paper are specific to Bing’s anycast CDN de-               performance is slower than the best of the three unicast front-ends.
ployment. In this section we characterize the size of the deployment,             Most of the time, in most regions, anycast does well, performing as
showing that our deployment is of a similar scale–a few dozens of                 well as the best of the three nearby unicast front-ends. However,
front-end server locations–to most other CDNs and in particular                   anycast is at least 25ms slower for 20% of requests, and just below
most anycast CDNs, although it is one of the largest deployments                  10% of anycast measurements are 100ms or more slower than the
within that rough scale. We then measure what the distribution of                 best unicast for the client.
these dozens of front-end locations yields in terms of the distance                  This graph suggests possible benefits in using DNS-based redi-
from clients to the nearest front-ends. Our characterization of the               rection for some clients, with anycast for the rest. Note that this
performance of this CDN is an important first step towards under-                 is not an upper bound: to derive that, we would have to poll all
standing anycast performance. An interesting direction for future                 front-ends in each beacon execution, which is too much overhead.
work is to understand how to extend these performance results to                  There is also no guarantee that a deployed DNS-based redirection
CDNs with different numbers and locations of servers and with                     system will be able to achieve the performance improvement seen in
different interdomain connectivity [18].                                          Figure 3 – to do so the DNS-based redirection system would have to
   We compare our CDN to others based on the number of server                     be practically clairvoyant. Nonetheless, this result was sufficiently
locations, which is one factor impacting CDN and anycast per-                     tantalizing for us to study anycast performance in more detail, and
formance. We examine 21 CDNs and content providers for which                      seek ways to improve it.
there is publicly available data [3]. Four CDNs are extreme outliers.             Examples of poor anycast routes: A challenge in understanding
ChinaNetCenter and ChinaCache each have over 100 locations in                     anycast performance is figuring out why clients are being directed
China. Previous research found Google to have over 1000 locations                 to distant or poor performing edges front-ends. To troubleshoot,
worldwide [16], and Akamai is generally known to have over 1000                   we used the RIPE Atlas [2] testbed, a network of over 8000 probes
as well [17]. While this scale of deployment is often the popular                 predominantly hosted in home networks. We issued traceroutes
image of a CDN, it is in fact the exception. Ignoring the large Chi-              from Atlas probes hosted within the same ISP-metro area pairs
nese deployments, the next largest CDNs we found public data for                  where we have observed clients with poor performance. We observe
are CDNetworks (161 locations) and SkyparkCDN (119 locations).                    in our analysis that many instances fall into one of two cases. 1)
The remaining 17 CDNs we examined (including ChinaNetCenter’s                     BGP’s lack of insight into the underlying topology causes anycast




                                                                            533
                                1
                                                                                                                             1

                                                                                                                            0.9
                               0.8
                                                                                                                            0.8


            CCDF of Requests
                                                                                                                            0.7
                               0.6
                                               Europe
                                                World
                                                                                                                            0.6




                                                                                                         CDF
                                         United States
                               0.4                                                                                          0.5

                                                                                                                            0.4
                                                                                                                                                            Weighted Clients Past Closest
                               0.2                                                                                          0.3                                      Clients Past Closest
                                                                                                                                                            Weighted Clients to Front-end
                                                                                                                            0.2                                      Clients to Front-end
                                0
                                                                                                                            0.1
                                     0       20          40     60       80   100
                                                                                                                                   64      128    256       512    1024 2048 4096 8192
                                             Performance difference between
                                                                                                                                                          Distance (km)
                                              anycast and best unicast (ms)

Figure 3: The fraction of requests where the best of three different                      Figure 4: The distance in kilometers (log scale) between clients and the
unicast front-ends out-performed anycast.                                                 anycast front-ends they are directed to.

to make suboptimal choices and 2) intradomain routing policies of                                                            1

ISPs select remote peering points with our network.
                                                                                                                            0.8
   In one interesting example, a client was roughly the same distance
from two border routers announcing the anycast route. Anycast




                                                                                                         Fraction of /24s
                                                                                                                                                                               all
                                                                                                                            0.6
chose to route towards router A. However, internally in our network,                                                                                                       > 10ms
                                                                                                                                                                           > 25ms
router B is very close to a front-end C, whereas router A has a                                                             0.4
                                                                                                                                                                          > 50ms
                                                                                                                                                                          > 100ms
longer intradomain route to the nearest front-end, front-end D. With
anycast, there is no way to communicate [39] this internal topology                                                         0.2

information in a BGP announcement.
                                                                                                                             0
   Several other examples included cases where a client is nearby a




                                                                                                                                       4




                                                                                                                                                      1




                                                                                                                                                                     8




                                                                                                                                                                                   5
                                                                                                                                   /0




                                                                                                                                                  /1




                                                                                                                                                                  /1




                                                                                                                                                                                /2
                                                                                                                                  04




                                                                                                                                                 04




                                                                                                                                                                04




                                                                                                                                                                              04
front-end but the ISP’s internal policy chooses to hand off traffic at a                                                                                      Date

distant peering point. Microsoft intradomain policy then directs the                      Figure 5: Daily poor-path prevalence during April 2015 showing what
client’s request to the front-end nearest to the peering point, not to                    fraction of client /24s see different levels of latency improvement over
the client. Some examples we observed of this was an ISP carrying                         anycast when directed to their best performing unicast front-end.
traffic from a client in Denver to Phoenix and another carrying
traffic from Moscow to Stockholm. In both cases, direct peering
                                                                                          formance.1 Next we examine how common these issues are from
was present at each source city.
                                                                                          day-to-day and how long issues with individual networks persist.
   Intrigued by these sorts of case studies, we sought to understand
                                                                                          Is anycast performance consistently poor? We first consider
anycast performance quantitatively. The first question we ask is
                                                                                          whether significant fractions of clients see consistently poor per-
whether anycast performance is poor simply because it occasionally
                                                                                          formance with anycast. At the end of each day, we analyzed all
directs clients to front-ends that are geographically far away, as was
                                                                                          collected client measurements to find prefixes with room for im-
the case when clients in Moscow went to Stockholm.
                                                                                          provement over anycast performance. For each client /24, we cal-
Does anycast direct clients to nearby front-ends? In a large
                                                                                          culate the median latency between the prefix and each measured
CDN with presence in major metro areas around the world, most
                                                                                          unicast front-end and anycast.
ISPs will see BGP announcements for front-ends from a number of
                                                                                             Figure 5 shows the prevalence of poor anycast performance each
different locations. If peering among these points is uniform, then
                                                                                          day during April 2015. Each line specifies a particular minimum
the ISP’s least cost path from a client to a front-end will often be the
                                                                                          latency improvement, and the figure shows the fraction of client
geographically closest. Since anycast is not load or latency aware,
                                                                                          /24s each day for which some unicast front-end yields at least that
geographic proximity is a good indicator of expected performance.
                                                                                          improvement over anycast. On average, we find that 19% of prefixes
   Figure 4 shows the distribution of the distance from client to
                                                                                          see some performance benefit from going to a specific unicast front-
anycast front-end for all clients in one day of production Bing traffic.
                                                                                          end instead of using anycast. We see 12% of clients with 10ms or
One line weights clients by query volume. Anycast is shown to
                                                                                          more improvement, but only 4% see 50ms or more.
perform 5-10% better at all percentiles when accounting for more
                                                                                             Poor performance is not limited to a few days–it is a daily con-
active clients. We see that about 82% of clients are directed to a
                                                                                          cern. We next examine whether the same client networks experience
front-end within 2000 km while 87% of client volume is within
                                                                                          recurring poor performance. How long does poor performance per-
2000 km.
                                                                                          sist? Are the problems seen in Figure 5 always due to the same
   The second pair of lines in Figure 4, labeled “Past Closest”,
                                                                                          problematic clients?
shows the distribution of the difference between the distance from
                                                                                             Figure 6 shows the duration of poor anycast performance dur-
a client to its closest front-end and the distance from the client to
                                                                                          ing April 2015. For the majority of /24s categorized as having
the front-end anycast directs to. About 55% of clients and weighted
                                                                                          poor-performing paths, those poor-performing paths are short-lived.
clients have distance 0, meaning they are directed to the nearest
                                                                                          Around 60% appear for only one day over the month. Around 10%
front-end. Further, 75% of clients are directed to a front-end within
                                                                                          of /24s show poor performance for 5 days or more. These days
around 400 km and 90% are within 1375 km of their closest. This
                                                                                          are not necessarily consecutive. We see that only 5% of /24s see
supports the idea that, with a dense front-end deployment such as
                                                                                          continuous poor performance over 5 days or more.
is achievable in North America and Europe, anycast directs most
                                                                                             These results show that while there is a persistent amount of poor
clients to a relatively nearby front-end that should be expected to
                                                                                          anycast performance over time, the majority of problems only last
deliver good performance, even if it is not the closest.
   From a geographic view, we found that around 10-15% of /24s                            1 No geolocation database is perfect. A fraction of very long client-to-front-end dis-
are directed to distant front-ends, a likely explanation for poor per-                    tances may be attributable to bad client geolocation data.




                                                                                    534
                                                                                                                                                          1
                                                  1
                                                                                                                                                         0.9




                                                                                                                              CDF of Front-end Changes
                                                                                                                                                         0.8
                                                 0.8
                                                                                                                                                         0.7

             CDF of Client /24s                  0.6
                                                                                                                                                         0.6
                                                                   Max # of Consecutive Days                                                             0.5
                                                                                      # Days
                                                                                                                                                         0.4
                                                 0.4
                                                                                                                                                         0.3
                                                                                                                                                         0.2
                                                 0.2
                                                                                                                                                         0.1
                                                                                                                                                          0
                                                  0
                                                                                                                                                               64   128    256    512    1024 2048 4096 8192
                                                       1     5           10             15
                                                                                                                                                                    Change in client-to-front-end distance
                                                                  Number of Days
                                                                                                                                                                      when the front-end changes (km)

Figure 6: Poor path duration across April 2015. We consider poor                                               Figure 8: The distribution of change in client-to-front-end distance
anycast paths to be those with any latency inflation over a unicast front-                                     (log scale) when when the front-end changes, for the 7% of clients that
end.                                                                                                           change front-end throughout a day.
                                                   1


                                                                                                               6.     ADDRESSING POOR PERFORMANCE
                Cumulative Fraction of Clients




                                                 0.8

                                                                                                                  The previous section showed that anycast often achieves good
                                                 0.6
                                                                                                               performance, but sometimes suffers significantly compared to uni-
                                                                                                               cast beacon measurements. However, the ability for unicast to beat
                                                 0.4
                                                                                                               anycast in a single measurement does not guarantee that this per-
                                                 0.2
                                                                                                               formance is predictable enough to be achievable if a system has to
                                                                                                               return a single unicast front-end to a DNS query. If a particular
                                                   0                                                           front-end outperformed anycast in the past for a client, will it still
                                                   Wed     Thu   Fri     Sat      Sun        Mon   Tue
                                                                   Day of the Week
                                                                                                               if the system returns that front-end next time? Additionally, be-
                                                                                                               cause of DNS’s design, the system does not know which client it
Figure 7: The cumulative fraction of clients that have changed front-
ends at least once by different points in a week                                                               is responding to, and so its response applies either to all clients of
                                                                                                               an LDNS or all clients in a prefix (if using ECS). Can the system
                                                                                                               reliably determine front-ends that will perform well for the set of
for a single day. Next we look at how much of poor performance                                                 clients?
can be attributed to clients frequently switching between good and                                                We evaluate to what degree schemes using DNS and ECS can
poor performing front-ends.                                                                                    improve performance for clients with poor anycast performance.
Front-end Affinity: Recurrent front-end selection changes for user                                             We evaluate (in emulation based on our real user measurements)
over time may indicate route stability issues which can lead to any-                                           a prediction scheme that maps from a client group (clients of an
cast performance problems. We refer to how “attached" particular                                               LDNS or clients within an ECS prefix) to its predicted best front-
clients are to a front-end as front-end affinity. In this section, we                                          end. It updates its mapping every prediction interval, set to one
analyze our passive logs.                                                                                      day in our experiment.2 The scheme chooses to map a client group
   Figure 7 shows the cumulative fraction of clients that have                                                 to the lowest latency front-end across the measurements for that
switched front-ends at least once by that time of the week. Within                                             group, picking either the anycast address or one of the unicast front-
the first day, 7% of clients landed on multiple front-ends. An                                                 ends. We evaluate two prediction metrics to determine the latency
additional 2-4% clients see a front-end change each day until the                                              of a front-end, 25th percentile and median latency from that client
weekend, where there is very little churn, less than .5%. This                                                 group to that front-end. We choose lower percentiles, as analysis
could be from network operators not pushing out changes during                                                 of client data showed that higher percentiles of latency distribu-
the weekend unless they have to. From the weekend to the begin-                                                tions are very noisy (we omit detailed results due to lack of space).
ning of the week, the amount of churn increases again to 2-4% each                                             This noise makes prediction difficult, as it can result in overlap-
day. Across the entire week, 21% of clients landed on multiple                                                 ping performance between two front-ends. The 25th percentile and
front-ends, but the vast majority of clients were stable. We discuss                                           median have lower coefficient of variation, indicating less variation
potential solutions to this more at the end of §6. We observe that                                             and more stability. Our initial evaluation showed that both 25th
the number of client front-end switches is slightly higher in a one                                            percentile and median show very similar performance as prediction
day snapshot compared to the 1.1-4.7% reported in previous work                                                metrics, so we only present results for 25th percentile.
on DNS instance-switches in anycast root nameservers [20, 33]. A                                                  We emulate the performance of such a prediction scheme using
likely contributing factor is that our anycast deployment is around                                            our existing beacon measurements. We base the predictions on one
10 times larger than the number of instances present in K root name                                            day’s beacon measurements. For a given client group, we select
server at the time of that work.                                                                               among the front-ends with 20+ measurements from the clients.
   Figure 8 shows the change in the client-to-front-end distance                                                  We evaluate the performance of the prediction scheme by com-
when the front-end changes. This shows that when the majority of                                               paring against the performance observed in next day’s beacon mea-
clients switch front-ends, it is to a nearby front-end. This makes                                             surements. We compare 50th and 75th anycast performance for the
sense given the CDN front-end density in North America and Eu-                                                 group to 50th and 75th performance for the predicted front-end.
rope. The median change in distance from front-end switches is                                                 The Bing team routinely uses 75% percentile latency as an inter-
483 km while 83% are within 2000 km.                                                                           nal benchmarks for a variety of comparisons. Next, we evaluate
   We saw in this section that most clients show high front-end-                                               prediction using both ECS and LDNS client grouping.
affinity, that is, they continue going to the same front-end over time.
For the clients that do switch front-ends, there is a long tail of                                             2 We cannot make predictions at finer timescales, as our sampling rate was limited due
distance between a client and switched pairs of front-ends.                                                    to engineering issues.




                                                                                                         535
                                    1
                                                                                                tralized route controller. Unlike our work, they do not examine
                                   0.9                                                          the end-to-end application performance comparison between DNS
                                   0.8                                                          redirection and anycast. Follow up work focuses on handling any-
            CDF of Weighted /24s
                                   0.7                                                          cast TCP session disruption due to BGP path changes [7]. Our work
                                   0.6   EDNS-0 Median
                                           EDNS-0 75th
                                                                                                is also closely related to FastRoute [23], a system for load balanc-
                                   0.5
                                           LDNS Median
                                             LDNS 75th
                                                                                                ing within an anycast CDN, but it does not address performance
                                   0.4
                                   0.3
                                                                                                issues around redirection. There has been a good deal of work on
                                   0.2
                                                                                                improving and evaluating general CDN performance [37, 24, 36,
                                   0.1                                                          6, 35, 25]. The majority of previous work on anycast performance
                                    0                                                           has focused on DNS. There has been significant attention to anycast
                                    -400 -300 -200 -100     0    100    200   300   400
                                                     Improvement (ms)
                                                                                                DNS from the network operations community [13, 15, 14, 28, 19,
                                                                                                12, 20] but less so for TCP and anycast [31]. Sarat et al. examined
Figure 9: Improvement over anycast from making LDNS or ECS-based
decisions with prediction using 25th percentile prediction metric. Neg-
                                                                                                the performance impact of anycast on DNS across different anycast
ative x-axis values show where anycast was better than our prediction.                          configurations [38]. Fan et al. [22] present new methods to identify
Values at 0 show when we predicted anycast was the best performing.                             and characterize anycast nodes. There are several pieces of work
Positive x-axis values show our improvement.                                                    describing deployment of anycast services [30, 10, 11, 26].
                                                                                                   Akamai recently published a study on DNS-based redirec-
Prediction using EDNS client-subnet-prefix: The ECS exten-
                                                                                                tion [17]. The authors showed that the majority of clients are nearby
sion [21] enables precise client redirection by including the client’s
                                                                                                their LDNS, enabling DNS-based redirection to perform well. How-
prefix in a DNS request. Our prediction scheme is straightforward:
                                                                                                ever, they also show that a significant number of clients are far from
we consider all beacon measurements for a /24 client network and
                                                                                                their LDNS, and that some LDNS serve clients spread over large
choose the front-end according to the prediction metrics.
                                                                                                geographic regions. The paper describes Akamai’s adoption of
   The “EDNS-0” lines in Figure 9 depict, as a distribution across
                                                                                                ECS-based redirection for clients of public DNS resolvers, show-
clients weighted by query volume, the difference between perfor-
                                                                                                ing impressive performance improvements for these clients versus
mance to the predicted front-end (at the 50th and 75th percentile)
                                                                                                LDNS-based redirection. However, public resolvers only make up a
and the performance to the anycast-routed front-end (at the same
                                                                                                small fraction of global DNS traffic. Clients using their ISPs’ LDNS
percentiles). Most clients see no difference in performance, in most
                                                                                                cannot benefit unless the ISPs enable ECS and the CDN supports
cases because prediction selected the anycast address. For the nearly
                                                                                                ECS requests from the LDNS. Since anycast works well for many
40% of queries-weighted prefixes we predict to see improvement
                                                                                                clients, we see benefit in a hybrid approach that chooses whether
over anycast, only 30% see a performance improvement over any-
                                                                                                to use DNS redirection or anycast based on measurements of which
cast, while 10% of weighted prefixes see worse performance than
                                                                                                works better for the LDNS and whether the LDNS supports ECS.
they would with anycast.
LDNS-based prediction: Traditionally, DNS-based redirection
can only make decisions based on a client’s LDNS. In this sec-                                  8.    CONCLUSION
tion, we estimate to what degree LDNS granularity can achieve                                      In this paper we studied the performance of a large anycast-
optimal performance when anycast routing sends clients to subop-                                based CDN, and evaluated whether it could be improved by using
timal servers. We construct a latency mapping from LDNS to each                                 a centralized, DNS-based solution. We found that anycast usually
measured edge by assigning each front-end measurement made by                                   performs well despite the lack of precise control, but that it directs
a client to the client’s LDNS, which we can identify by joining our                             ≈ 20% of clients to a suboptimal front-end. We demonstrated
DNS and HTTP logs based on the unique hostname for the mea-                                     that a simple prediction scheme may allow DNS redirection to
surement. We then consider all beacon measurements assigned to                                  improve performance for some of the clients that see poor anycast
an LDNS and select the LDNS’s best front-end using the prediction                               performance.
metrics. In the page loads in our experiment, public DNS resolvers
made up a negligible fraction of total LDNS traffic so their wide
user base have an insignificant impact on results.                                              Acknowledgements
   The “LDNS” lines in Figure 9 show the fraction of /24 client                                 We gratefully acknowledge Nick Holt and Daniel Gicklhorn for
networks that can be improved from using prediction of performance                              their support of this work. Matt Calder and Ethan Katz-Bassett
based on an LDNS-based mapping. While we see improvement for                                    were partially supported by the U.S. National Science Foundation
around 27% of weighted /24s, we also pay a penalty where our                                    grant numbers CNS-1351100 and CNS-1413978.
prediction did poorly for around 17% of /24s.
   Our results demonstrate that traditional and recent DNS tech-
niques can improve performance for many of the clients who expe-                                9.    REFERENCES
rience suboptimal anycast routing. We are also considering a hybrid
                                                                                                 [1] CloudFlare. https://www.cloudflare.com/.
approach that combines anycast with DNS-based redirection. The
                                                                                                 [2] RIPE Atlas. https://atlas.ripe.net/.
key idea is to use DNS-based redirection for a small subset of poor
performing clients, while leaving others to anycast. Such a hy-                                  [3] USC CDN Coverage.
brid approach may outperform DNS redirection for clients not well                                    http://usc-nsl.github.io/cdn-coverage.
represented by their LDNS, and it may be more scalable.                                          [4] V. K. Adhikari, Y. Guo, F. Hao, V. Hilt, and Z.-L. Zhang.
                                                                                                     Tale of Three CDNs: An Active Measurement Study of Hulu
                                                                                                     and its CDNs. In IEEE Global Internet Symposium ’12.
7.    RELATED WORK                                                                               [5] B. Ager, W. Mühlbauer, G. Smaragdakis, and S. Uhlig.
  Most closely related to our work is from Alzoubi et al. [9, 8].                                    Comparing DNS Resolvers in the Wild. In IMC ’10.
They describe a load-aware anycast CDN architecture where ingress                                [6] B. Ager, W. Mühlbauer, G. Smaragdakis, and S. Uhlig. Web
routes from a CDN to a large ISP are managed by an ISP’s cen-                                        Content Cartography. In IMC ’11.




                                                                                          536
 [7] Z. Al-Qudah, S. Lee, M. Rabinovich, O. Spatscheck, and                [24] B. Frank, I. Poese, Y. Lin, G. Smaragdakis, A. Feldmann,
     J. Van der Merwe. Anycast-aware Transport for Content                      B. Maggs, J. Rake, S. Uhlig, and R. Weber. Pushing
     Delivery Networks. In WWW ’09.                                             CDN-ISP Collaboration to the Limit. SIGCOMM CCR ’14.
 [8] H. A. Alzoubi, S. Lee, M. Rabinovich, O. Spatscheck, and              [25] M. J. Freedman, E. Freudenthal, and D. Mazieres.
     J. Van Der Merwe. A Practical Architecture for an Anycast                  Democratizing Content Publication with Coral. In NSDI ’04.
     CDN. ACM Transactions on the Web (TWEB) ’11.                          [26] M. J. Freedman, K. Lakshminarayanan, and D. Mazières.
 [9] H. A. Alzoubi, S. Lee, M. Rabinovich, O. Spatscheck, and                   OASIS: Anycast for Any Service. In NSDI ’06.
     J. Van der Merwe. Anycast CDNs Revisited. In WWW ’08.                 [27] M. J. Freedman, M. Vutukuru, N. Feamster, and
[10] H. Ballani and P. Francis. Towards a Global IP Anycast                     H. Balakrishnan. Geographic Locality of IP Prefixes. In IMC
     Service. In SIGCOMM ’05.                                                   ’05.
[11] H. Ballani, P. Francis, and S. Ratnasamy. A                           [28] J. Hiebert, P. Boothe, R. Bush, and L. Lynch. Determining
     Measurement-based Deployment Proposal for IP Anycast. In                   the Cause and Frequency of Routing Instability with Anycast.
     IMC ’06.                                                                   In AINTEC ’06.
[12] P. Barber, M. Larson, and M. Kosters. Traffic Source Analysis         [29] A. Jain, J. Mann, Z. Wang, and A. Quach. W3C Resource
     of the J Root Anycast Instances. NANOG 39. February, ’07.                  Timing Working Draft.
[13] P. Barber, M. Larson, M. Kosters, and P. Toscano. Life and                 http://www.w3.org/TR/resource-timing/, July 2015.
     Times of J-ROOT. NANOG 32. October, ’04.                              [30] D. Katabi and J. Wroclawski. A Framework For Scalable
[14] P. Boothe and R. Bush. Anycast Measurements Used To                        Global IP-anycast (GIA). SIGCOMM CCR ’00.
     Highlight Routing Instabilities. NANOG 35. October, ’05.              [31] M. Levine, B. Lyon, and T. Underwood. Operation
[15] P. Boothe and R. Bush. DNS Anycast Stability. 19th APNIC,                  Experience with TCP and Anycast. NANOG 37. June, ’06.
     ’05.                                                                  [32] W. Li, R. K. Mok, R. K. Chang, and W. W. Fok. Appraising
[16] M. Calder, X. Fan, Z. Hu, E. Katz-Bassett, J. Heidemann,                   the Delay Accuracy In Browser-based Network
     and R. Govindan. Mapping the Expansion of Google’s                         Measurement. In IMC ’13.
     Serving Infrastructure. In IMC ’13.                                   [33] Z. Liu, B. Huffaker, M. Fomenkov, N. Brownlee, et al. Two
[17] F. Cheng, R. K. Sitaraman, and M. Torres. End-user                         Days in the Life of the DNS Anycast Root Servers. In PAM
     mapping: Next Generation Request Routing for Content                       ’07.
     Delivery. In SIGCOMM ’15.                                             [34] Z. M. Mao, C. D. Cranor, F. Douglis, M. Rabinovich,
[18] Y. Chiu, B. Schlinker, A. B. Radhakrishnan, E. Katz-Bassett,               O. Spatscheck, and J. Wang. A Precise and Efficient
     and R. Govindan. Are We One Hop Away from a Better                         Evaluation of the Proximity Between Web Clients and Their
     Internet? In IMC ’15.                                                      Local DNS Servers. In USENIX ATC ’02.
[19] L. Coletti. Effects of Anycast on K-root Performance.                 [35] E. Nygren, R. K. Sitaraman, and J. Sun. The Akamai
     NANOG 37. June, ’06.                                                       Network: A Platform for High-performance Internet
[20] L. Colitti, E. Romijn, H. Uijterwaal, and A. Robachevsky.                  Applications. SIGOPS ’10.
     Evaluating the Effects of Anycast on DNS Root Name                    [36] J. S. Otto, M. A. Sánchez, J. P. Rula, and F. E. Bustamante.
     Servers. RIPE document RIPE-393, ’06.                                      Content Delivery and the Natural Evolution of DNS: Remote
[21] C. Contavalli, W. van der Gaast, D. Lawrence, and                          DNS Trends, Performance Issues and Alternative Solutions.
     W. Kumari. Client Subnet in DNS Requests. IETF Draft                       In IMC ’12.
     draft-vandergaast-edns-client-subnet-02, July 2015.                   [37] I. Poese, B. Frank, B. Ager, G. Smaragdakis, S. Uhlig, and
[22] X. Fan, J. Heidemann, and R. Govindan. Evaluating Anycast                  A. Feldmann. Improving Content Delivery with PaDIS.
     in the Domain Name System. In INFOCOM ’13.                                 Internet Computing, IEEE ’12.
[23] A. Flavel, P. Mani, D. Maltz, N. Holt, J. Liu, Y. Chen, and           [38] S. Sarat, V. Pappas, and A. Terzis. On the Use of Anycast in
     O. Surmachev. FastRoute: A Scalable Load-Aware Anycast                     DNS. In ICCCN ’06.
     Routing Architecture for Modern CDNs. In NSDI ’15.                    [39] N. Spring, R. Mahajan, and T. Anderson. The Causes of Path
                                                                                Inflation. In SIGCOMM ’03.




                                                                     537
