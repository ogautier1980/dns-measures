                                                                  Digital Communications and Networks 4 (2018) 235–243



                                                                      Contents lists available at ScienceDirect


                                                    Digital Communications and Networks
                              journal homepage: www.keaipublishing.com/en/journals/digital-communications-and-networks/




Evolution and challenges of DNS-based CDNs
Zheng Wang a, *, Jun Huang b, Scott Rose a
a
    Advanced Network Technologies Division, National Institute of Standards and Technology, USA
b
    School of Computer Science, Chongqing University of Posts and Telecommunications, China




A R T I C L E I N F O                                        A B S T R A C T

Index terms:                                                 DNS-based server redirecting is considered the most popular means of deploying CDNs. However, with the
Content delivery network                                     increasing use of remote DNS, DNS-based CDNs face a great challenge in performance degradation. To address
DNS-Based server redirecting                                 this issue, encouraging progress has been made in both industry and research communities. In this article, state-of-
Remote DNS                                                   art solutions for the remote DNS problem are discussed at ﬁrst. Next, privacy concerns about DNS-based CDNs,
DNS privacy                                                  including client location as well as redirection privacy, are identiﬁed and a representative solution is summarized.
                                                             Finally, the solution is compared to those in prior works under different measures, and a discussion on DNS-based
                                                             CDN applications is provided. A model is also established to deepen the understanding of CDN performance. We
                                                             believe that this survey will shed light on the application of DNS-based CDNs, and it is expected to provide design
                                                             guidelines to CDN service providers.




1. Introduction                                                                                   latency, network distance, and surrogate server load. Because the nearest
                                                                                                  surrogate server is commonly considered to best serve end users, end user
    Over the past three decades, the world has witnessed the rapid growth                         location is typically used as the decisive parameter in request routing
of the internet and the enormously enriched content delivered over it.                            [5–7]. In practice, most CDN servers simply obtain the end user location
The ever-increasing demands from users place a heavy burden on the                                from the source IP address of the incoming CDN request.
limited networking and computing resources of content providers. Thus,                                 Server redirecting mechanism. The mechanism informs the end
new approaches or paradigms are needed to address the emerging                                    user about the optimal surrogate server selected by the server selection
challenges in delivering content. For example, popular web services are                           mechanism. Among all server redirecting mechanisms, DNS-based server
often vulnerable to the so-called ﬂash crowing problem [1,2]. When                                redirecting is the most popular. It makes full use of the existing DNS
many users simultaneously access the same web site, the request load                              infrastructure and thus enables quick and easy deployment. Despite its
may overwhelm the web servers. Flash crowd may cause slowed                                       merits, DNS-based server redirecting is increasingly challenged by the
responsiveness, diminished availability, or even website crashes.                                 remote DNS issue and privacy concerns.
    Content Delivery Networks (CDNs) were proposed to solve content                                   The remote DNS issue arises from the false assumption that a DNS
delivery bottlenecks, such as scalability, reliability, and performance. In                       recursive server is in proximity to its clients. When a client queries a
CDNs, content is replicated from the original server to surrogate servers                         remote DNS recursive server, the DNS recursive server contacts the DNS
distributed over the internet [3,4]. Surrogate servers are placed at                              authoritative server for an answer. In determining the optimal response,
optimal sites, e.g., the edge of the internet infrastructure [39], providing                      the DNS authoritative server infers the client location from incoming
improved connectivity to the nearby end users. In this manner, contents                           requests, and therefore uses the source IP address of the DNS recursive
are transparently, rapidly, and reliably delivered to end users.                                  server rather than that of the client. Given the location mismatch be-
    Request routing is a critical issue in CDNs. It directs end users to                          tween the client and the remote DNS recursive server, the DNS recursive
optimal surrogate servers per speciﬁc metrics or policies. Typically, the                         server tends to misrepresent the client location to the DNS authoritative
design of CDN request routing involves:                                                           server. Thus, the server selection result is likely to deviate from the
     Server selection mechanism. The mechanism determines the                                    optimal. Recently, various solutions have been proposed to overcome the
optimal surrogate server for an end user. A server selection algorithm                            remote DNS problem; the most recognized of these is known as a EDNS-
may use a set of metrics, such as network utilization, user perceived                             Client-Subnet(ECS) DNS extension [21]. ECS explicitly indicates client


    * Corresponding author. 100 Bureau Dr., Stop 1070, Gaithersburg, MD 20899-1070, USA.
      E-mail addresses: zhengwang98@gmail.com (Z. Wang), xiaoniuadmin@gmail.com (J. Huang), scott.rose@nist.gov (S. Rose).


https://doi.org/10.1016/j.dcan.2017.07.005
Received 16 February 2017; Received in revised form 11 May 2017; Accepted 7 July 2017
Available online 27 July 2017
2352-8648/© 2018 Chongqing University of Posts and Telecommunications. Production and hosting by Elsevier B.V. on behalf of KeAi. This is an open access article under the CC BY-NC-
ND license (http://creativecommons.org/licenses/by-nc-nd/4.0/).
Z. Wang et al.                                                                                                  Digital Communications and Networks 4 (2018) 235–243


location information in an option of the DNS message. By inspecting the             by sacriﬁcing precise redirection. The measurement showed that the
ECS option rather than the source IP address of the arriving DNS request,           anycast CDN directed roughly 20% of clients to suboptimal front ends. A
the DNS authoritative server can identify the client location.                      load-aware anycast CDN architecture [13,14] was proposed as a solution
    The cost incurred by adopting ECS is loss of privacy. ECS makes client          to the problem. However, its efﬁcacy is limited by session disruptions
location information visible to the DNS authoritative server and on-path            that plague anycast. Another work addressed the session disruption issue
eavesdroppers. Thus, client location privacy, which is well protected by            by dedicating a transport level mechanism [15]. However, both the so-
remote DNS, is almost invalidated by ECS. The other problem with ECS is             phisticated routing control and the innovated transport protocol are too
the vulnerability of redirection enumeration. If ECS is adopted, potential          radical to deploy rapidly and efﬁciently.
adversaries may enumerate CDN mapping at an affordable cost. As a
result, CDN mapping policy, which is often assumed to be private to the             2.4. DNS-based server redirecting
CDN provider, is actually exposed to the public.
    In this work, we survey the state-of-the-art DNS-based CDN technol-                 This mechanism piggybacks redirection in responses to DNS queries.
ogies, and provide insights into the emerging challenges and solutions.             It is a ﬂexible and lightweight solution and fully compatible with the
We expect this work to be the ﬁrst to systematically discuss DNS-based              existing DNS infrastructure. Thus, it has gained signiﬁcant popularity in
CDNs and provide design guidelines to CDN service providers. The                    major CDN networks such as Akamai [16], Limelight Networks [17], and
remainder of this paper is structured as follows. Section 2 overviews the           Mirror Image [18].
existing approaches for CDN server directing with a focus on DNS-based                  As an indispensable substrate of today's Internet, the DNS functions as
server redirecting. Section 3 discusses the remote DNS problem and                  a globally distributed directory. Its primary role is to map domain names
presents the state-of-art solutions to it. Section 4 discusses privacy con-         to the corresponding IP addresses. In a typical DNS session, the client ﬁrst
cerns and analyzes possible responses. Based on the discussions above,              sends a request to its designated recursive DNS server. A recursive DNS
Section 5 surveys DNS-based server redirecting solutions via compari-               server is either operated by ISPs (Internet Service Providers) or provided
sons. Section 6 summarizes and concludes the work.                                  as a public service for any users around the globe (e.g., the Google DNS
                                                                                    service hosted at 8.8.8.8 and 8.8.4.4). The recursive DNS server resolves
2. Existing approaches                                                              the request on behalf of the client. It iteratively traverses relevant
                                                                                    authoritative DNS servers following the DNS tree until the ﬁnal answer is
  Existing approaches for server directing include HTTP redirection,                obtained. The recursive DNS server not only delivers the answer to the
URL rewriting, anycast, and DNS-based server redirecting.                           client but also caches it for future queries. In the DNS, a name-to-address
                                                                                    mapping is represented by a DNS record. Each DNS record contains a
2.1. HTTP redirection                                                               Time-To-Live (TTL) ﬁeld that speciﬁes how long the recursive DNS server
                                                                                    caches it.
    HTTP redirection allows a web server to propagate the server selec-                 In DNS-based server redirecting, a domain name associated with the
tion result to the end user via HTTP headers [8,9]. Hence, the end user             content (e.g., the web pages available at a web site) offered by the con-
can be redirected to the optimal server by following the response                   tent provider is hosted on the authoritative servers. Currently, it is
generated from the Web server. The weakness of HTTP redirection lies in             common practice to outsource the task of content delivery a CDN pro-
its reliance on support from the server side to the client side. Moreover,          vider. A CDN provider, which disseminates the content on behalf of the
HTTP redirection is not a lightweight solution because an extra round-              content provider, is likely to operate the authoritative servers as an in-
trip delay is introduced in every HTTP session, and the processing                  tegral part of its content delivery service.
overheads of HTTP are non-trivial.                                                      Many content providers prefer to take care of their brand valued
                                                                                    domain names themselves, and a commercial CDN provider tends to
2.2. URL rewriting                                                                  manage its CDN authoritative servers for its customers below one domain
                                                                                    or several domains owned by itself. Here we call a domain name owned
    This technique mainly targets content delivery with embedded ob-                by a content provider a “content domain name” and a domain name
jects in response to client requests [10,11]. In URL rewriting, the origin          owned by a CDN provider a “CDN domain name.” The separation be-
server rewrites the generated pages' URL links in order to indicate the             tween a content domain name and a CDN domain name in some ways
best surrogate server. Following the rewritten responses, the client can be         decouples the DNS management between a content provider and a CDN
optimally redirected. The major cost of URL rewriting is the delay for              provider, and therefore facilitates independent and stable
URL-parsing. Worse yet, the cost is likely to increase because the                  CDN operation.
rewritten URL is non-cacheable for the end user.                                        To associate a content domain name with a CDN domain name, a
                                                                                    CNAME-type DNS record can be registered at the content provider to
2.3. Anycast                                                                        point an alias name, namely a content domain name, to a canonical
                                                                                    name, namely a CDN domain name. When a client sends a request for a
    Anycast is a network layer technology for transparent server selection          content domain name, the content providers DNS authoritative server
and redirecting. In this approach, the same IP address is assigned to               answers with the CNAME record referring to the CDN domain name. The
multiple surrogate servers located distributively. When the client sends            client is then redirected to the CDN provider's DNS authoritative server
requests to the IP address, the requests will be routed to the nearest              which resolves the CDN domain name.
surrogate server deﬁned by the routing policy. Note that the server                     In DNS-based server redirecting, the server selection result is deliv-
redirecting enabled by anycast is technically not controllable for content          ered to the end user by resolving the domain name to the IP address of the
providers; therefore, anycast usage is controversial. On the one hand, its          selected surrogate server. To do this, the CDN authoritative server
transparency to both content providers and end users may be a beneﬁt, as            dynamically updates its DNS record via the server selection algorithm,
content providers are liberated from request-routing overhead. On the               always pointing to the optimal surrogate servers. The dynamic name
other hand, content providers may lose some server selection ﬂexibility.            resolution is usually conducted according to the sources of incoming
Consider a scenario in which anycast forwards requests to the nearest               requests. Owing to the caching effects, a small TTL value is usually
(yet overloaded) server, by simply respecting a distance-based routing              preferable for the DNS record, to ensure server redirecting prompt-
policy. Additionally, internet routing ﬂuctuations may negatively impact            ness [29].
the stability of IP anycast. In a measurement study [12] on the perfor-                 Fig. 1 shows an example of DNS-based server redirecting. First, the
mance of anycast CDN, the simplicity of anycast was found to be gained              client requests the DNS recursive server for the IP address of zoo.com

                                                                              236
Z. Wang et al.                                                                                                   Digital Communications and Networks 4 (2018) 235–243


(Step (1)). The DNS recursive server is informed by the content provider's           recent years. Among the servers, some are public DNS servers offered by
authoritative server that zoo.com is an alias of cdn.com (Step (2)). The             major internet enterprises such as Google, OpenDNS, Norton, etc. Many
DNS recursive server then obtains the result from the CDN provider's                 users have switched to those public DNS services because of their better
authoritative server, it shows that cdn.com is hosted at an optimal sur-             DNS performance in terms of availability, stability, and security. Ac-
rogate server whose IP address is 1.1.1.1 (Step (3)). When the DNS                   cording to a 2012 study [28], the public DNS user base grew by 27%
recursive server forwards the answer to the client (Step (4)), the client            annually, and 8.6% of users in the sample relied on a public DNS service.
accesses the content delivered from the surrogate server at 1.1.1.1 (Step                DNS-based server redirecting is likely to perform poorly when the
(5)). All surrogate servers connected by the CDN backbone are syn-                   client uses a remote DNS recursive server. For example, an end user
chronized from the original server at the content provider.                          located in the US can experience slow responses when accessing the CDN
    DNS-based server redirecting has several advantages over other                   website, if choosing a DNS recursive server located in Europe. The
server redirecting methods:                                                          problem is caused by the selected CDN server in Europe. The server se-
                                                                                     lection is optimized based on the location of the DNS recursive server but
● Transparency. It is fully transparent to the end users. The CDN ser-               is essentially suboptimized for the location of the end user. A recent study
  vice hosted on different servers is accessible from one domain name.               [19] on Africa's internet infrastructure reveals that the use of distant DNS
  Moreover, the dynamic mapping between the domain name and                          servers contributed to in excess of 100 ms of DNS resolution delay for
  different servers is invisible to end users.                                       approximately 50% of the measurement probes. In another study, Otto
● Simplicity. It can be seamlessly incorporated into the DNS resolution              et al. [28] assessed the end-to-end impact of using remote DNS services
  process. In particular, the DNS infrastructure is so universally avail-            on CDN performance. To compare performance, server redirections
  able that both content providers and end users are saved from heavy                performed by clients, ISP DNS, and public DNS were measured at a set of
  investment.                                                                        locations. ISP DNS was shown to have some similarity with clients in at
● Flexibility. Server redirecting can be ﬂexibly managed by adjusting                least 80% of locations, and there was no similarity between public DNS
  the TTL value of the DNS record. A large TTL value is favorable for                and client for 90% of locations. The differences in similarity were
  more static server redirecting and lowered authoritative server load.              explained by the increased distance to the client using public DNS. For
  Small TTL values allow for more dynamic server redirecting. In an                  HTTP performance, public DNS was found to yield doubled latencies
  extreme case, a zero TTL allows up-to-date direction for every indi-               compared with clients and ISP DNS. As one natural explanation, the
  vidual DNS request.                                                                degraded HTTP performance was correlated with sub-optimal server
                                                                                     redirections by remote DNS. Those results showed that remote DNS
3. Remote DNS problem and solutions                                                  signiﬁcantly impacts the client's perceived CDN performance.
                                                                                         Hidden behind local DNS servers, clusters of hosts are inaccessible to
3.1. Remote DNS problem                                                              content providers in terms of features such as size and geographical
                                                                                     compactness. Thus, without knowledge about the local clusters' proper-
    The major limitation of DNS-based server redirecting is a false                  ties, content delivery using local DNS servers is likely to be sub-
assumption regarding the recursive DNS server's proximity to the client.             optimized [20].
The CDN provider typically determines the optimal server selection
based on the source IP address of the DNS request (probably combined
with other information). However, the source IP address conveyed to the              3.2. Solutions
CDN provider is that of the DNS recursive server, rather than that of the
client. This is because the CDN authoritative server is queried by the DNS           3.2.1. ECS
recursive server, not by the client. The server selection result may be only             A recent solution to the remote DNS problem is the EDNS-Client-
slightly problematic when the DNS recursive server and client are sufﬁ-              Subnet DNS extension (ECS) [21]. It was proposed by Google and agreed
ciently proximate. However, the result may be sub-optimal if the prox-               to by IETF. The proposed extension allows a recursive server to deliver
imity assumption does not hold.                                                      client location information to an authoritative server.
    The use of remote DNS recursive servers has increased signiﬁcantly in                ECS is based on an EDNS0 DNS extension [22], which is introduced to
                                                                                     include optional data in a DNS message. In ECS, an OPT record in the




                                                              Fig. 1. DNS-based server redirecting.


                                                                               237
Z. Wang et al.                                                                                                   Digital Communications and Networks 4 (2018) 235–243


DNS message is used to convey the client's IP address preﬁx and the                 [24]. The so-called Direct Resolution approach allows a recursive DNS
scope. An ECS-enabled client includes that ECS OPT record in its request.           server to translate content domain names to CDN names and then obtain
Additionally, an ECS-aware DNS recursive server copies the ECS OPT                  the authoritative CDN server. The ﬁnal CDN redirection result is then
record from the client's request when sending out its request. The                  fetched by the client itself rather than by the recursive server. Because
ECS-aware DNS authoritative server can determine the CDN server se-                 redirection by Direct Resolution is based on the client location, it is better
lection using the client location indicated by the ECS OPT record.                  optimized compared to using a remote DNS recursive server or even a
    ECS demands substantial deployment costs. It calls for joint efforts by         local DNS recursive server. However, the client-side resolver's job is
all parties involved in DNS transactions, including the following:                  complicated in two ways: one is the increased number of queries involved
                                                                                    in resolving a CDN name; the other is the caching overheads. Another
● End users should upgrade their stub resolvers (often embedded in                  cost of Direct Resolution is reduced privacy. More private information
  web browsers), email clients, and other applications to support ECS.              about the client location is expected to be exposed by Direct Resolution,
  This should be serviced by software vendors and awareness of end                  because the client's full IP address is visible in a DNS request. In contrast,
  users.                                                                            only the client's IP address preﬁx is leaked by the ECS extension.
● DNS recursive servers should provide ECS support for their clients.
  Considering the fact that ECS-capable DNS server implementation is                4. Privacy concerns and solution
  barely available, this is a non-trivial task.
● DNS authoritative servers should be compatible with ECS in support                4.1. Location privacy
  of content delivery. Even for non-CDN authoritative servers, ECS
  payloads should not be identiﬁed as format errors or malicious data.                  While ECS improves CDN performance by exposing client location
● Intermediate systems and DNS middle-boxes should be compatible                    information, it raises concerns over privacy. In the conventional DNS
  with ECS and at least forward ECS payloads unmodiﬁed.                             model, the client is well hidden from the DNS authoritative server by the
                                                                                    DNS recursive server. For example, DNS authoritative servers for popular
    Cache efﬁciency is another concern with ECS. In the conventional                domains such as google.com, facebook.com, and amazon.com. have no
DNS caching model, one DNS question is basically mapped to one cor-                 information regarding which end users actually query them. Addition-
responding DNS record in cache. This simple caching mechanism has                   ally, DNS authoritative server operators are unlikely to associate an
proven to be effective and efﬁcient in DNS practice from the 1980's                 incoming DNS request to its originating end user. Thus, the end user's
through today [30]. ECS expands the one-to-one caching model by                     behavior is largely kept private from the DNS authoritative server. In the
introducing another dimension, namely, the ECS scope. In ECS, a set of              context of increased DNS privacy concerns in recent years [32–34,36],
items in cache are allowed to share one DNS record yet differ in the ECS            the conventional DNS model protects end users from being directly
scope. A diversity of ECS scopes is often needed to ensure good content             monitored, recorded, and analyzed by DNS authoritative servers. How-
delivery performance for global end users. Hence, by adopting ECS, the              ever, ECS does reveal private information, as client location information
DNS cache will be expanded and complicated by a factor of the number of             is hardly private. While using an IP address preﬁx rather than an exact IP
ECS scopes. The vulnerability may be exploited in DoS attacks, which aim            address is recommended in the ECS option, a long IP address preﬁx is
at bypassing caching and ﬂooding authoritative servers [37,38]. A DNS               generally preferred to ensure optimal CDN server selection. Here a
privacy study [32] pinpointed the limitation, which applies to any                  tradeoff exists in that longer IP addresses, and allow better CDN perfor-
end-to-end DNS proposal. This limitation is a prohibitive trafﬁc overhead           mance, but reduce user privacy. Thus, the end user must trade privacy for
on the name servers, caused by non-interoperability with the caches.                CDN performance.
    The transition to ECS will be challenging in terms of handling co-
existing ECS compliance and ECS non-compliance. In the current ECS
extension, an upstream party has no means of signaling its ECS support to           4.2. Redirection privacy
a downstream party. For example, ECS compliant clients tend to send ECS
queries by default to DNS recursive server that are non-ECS-compliant,                  To optimize user-perceived latency, some major content providers
causing an unnecessary waste of ECS payload. Even worse an ECS-                     such as Google invest heavily in building content delivery networks and
compliant DNS recursive server contacts an ECS non-compliance DNS                   developing sophisticated CDN mapping algorithms. Individual or small
authoritative server with ECS payload. In that case, the client's private           sets of redirection mappings are commonly considered readily available
data is unnecessarily leaked in the path between the recursive server and           and open to the public. However, mapping out entire content delivery
the authoritative server, because the latter does not support ECS at all.           networks by enumerating redirection mapping is likely to infringe on the
                                                                                    content provider's privacy. Complete redirection mapping information
3.2.2. Name extension                                                               may be utilized in orchestrated DDoS attacks against the CDN infra-
     To bypass the overhead and complexity of handling ECS, an alter-               structure, as well as for other offensive purposes. Therefore, the risks of
native proposal is to encode the client's location information in the DNS           redirection privacy are either undesired or unexpected by con-
query name [23]. In the proposal, the client sends a request for a speciﬁc          tent providers.
query name, which is constructed by preﬁxing the original query name                    Generally, traversing a 32-bit IPv4 address space (excluding private
onto the client's location information. The DNS recursive server handles            IP addresses) is almost impossible for most attackers, given the enormous
that modiﬁed query name just as it would handle an unmodiﬁed one, and               number of queries. However, like any other cluster based redirection
it is thus kept transparent. If it supports extended query names, the DNS           mechanism, ECS may make this possible because it greatly reduces the
authoritative server retrieves the client's location information from that          number of queries. Calder et al. [26] used ECS-enabled queries to mea-
query and thereby returns the CDN server selection. As an end-to-end                sure the redirection mapping of the Google web service. Based on the
extension between the client and the DNS authoritative server, the                  enumeration and geolocation results, they demonstrated the growth of
approach does not require support from all intermediate devices and                 Google's serving infrastructure and acquired its content serving strategy.
servers. Thus, the obstacles impeding its adoption are greatly reduced              By using routable/24 client preﬁxes, queries against Google were re-
compared with ECS.                                                                  ported as taking about a day to enumerate. The efﬁciency of ECS-based
                                                                                    redirection enumeration highlights the privacy issue with any IP
3.2.3. Direct resolution                                                            block-based redirection mechanism. Similarly, Streibelt et al. [27]
    Considering the low adoption level of ECS, another solution is to use a         showed measurement opportunities to uncover details about CDN pro-
client-side resolver that directly contacts the CDN authoritative server            viders' operational practices with the support of ECS.

                                                                              238
Z. Wang et al.                                                                                                  Digital Communications and Networks 4 (2018) 235–243


4.3. Solution                                                                       operations, as well as those proposed in recent years. A total of seven
                                                                                    solutions are identiﬁed. For each solution, we identify its merits and
     As a response to the privacy concerns incurred by ECS, a client                demerits using the following ﬁve measures. The comparison is shown
pseudononymizing scheme was proposed in Ref. [25]. In the proposal,                 in Table 1.
the client does not use its IP address preﬁx as location information in its
DNS requests. Instead, it uses its pseudononymizing identiﬁer to protect            5.1. Metrics
its location privacy. The mapping between the IP address and the pseu-
dononymizing identiﬁer is registered, maintained, and resolved at the               5.1.1. Client complexity
pseduonymizing registry of a trustworthy third party. Note that all                     The implementation of the DNS client that accesses the DNS recursive
on-path parties, including DNS authoritative servers, have no access to             server is usually referred to as the stub resolver. Stub resolvers are
client location (through translating the client's pseudononymizing iden-            installed by default on platforms such as Windows, Linux, and Unix. Stub
tiﬁer) unless they are authorized. A trustworthy third party is tasked with         resolvers are assumed to be simpliﬁed enough to be affordable for
CDN server selection on behalf of the authoritative servers in its pse-             lightweight and cost-constrained devices or systems such as emerging IoT
duonymizing optimizer. When accessing the pseudononymizing service,                 (Internet of Things) gadgets and mobile devices. Because they rely
a client ﬁrst registers the mapping between its IP address and its pseu-            heavily on recursive servers, stub resolvers' tasks are limited to sending
dononymizing identiﬁer to the pseduonymizing registry in a secure                   queries, interpreting responses, and resending them if unanswered. In
manner (Step (1) in Fig. 2). It can then send DNS requests using the                accordance with the simplicity principle, any design attempting to place
pseudononymizing identiﬁer (Step (2) in Fig. 2). Note that all on-path              complex burdens on stub resolvers may limit their deployment.
parties, including DNS authoritative servers, have no access to client
location (through translating the client's pseudononymizing identiﬁer)              5.1.2. Intermediate transparency
unless they are authorized. The authoritative server forwards the pse-                 To support a CDN solution, any intermediate component located in
duonymizd requests to the third party (Step (3) in Fig. 2), which looks up          the path between the querier, namely the DNS client, and the responder,
the mapping to the IP address in a secure manner (Step (4) in Fig. 2) and           namely the DNS authoritative server, should be able to interpret, process,
returns the CDN server selection (Step (5) in Fig. 2). Finally, the                 and forward the messages compliantly whenever necessary. If some
authoritative server delivers the CDN server selection to the client (Step          middle-box (e.g., a DNS recursive server) must be substantially upgraded
(6) in Fig. 2).                                                                     or redesigned, the solution's adoption would be costly. In contrast, a
     Despite its privacy-preserving advantages, client pseudononymizing             solution with transparency to any intermediate component has the
may suffer from the bottleneck of CDN redirection delay. Compared with              advantage of easy deployment and excellent compatibility.
common DNS operations, an extra delay is introduced to DNS authori-
tative servers' response latency because they ask an external trustworthy           5.1.3. CDN performance
third party for the redirection results. Clouding the trustworthy third                 For location-based CDN server selection, CDN performance is largely
party's infrastructure may be an effective way of minimizing the extra              determined by the accuracy of the client location information conveyed
DNS lookup delay. Besides investing in the network infrastructure, pro-             to the DNS authoritative servers. For simplicity, we merely consider best-
tocol level optimizations also help. For example, some extra redirection            effort location exposure for each solution, without factoring in privacy
results may be piggybacked on the response if those results are intelli-            concerns. In particular, ECS and Name Extension are both supposed to
gently predicted to be queries that will be used shortly thereafter; the            use full client IP addresses in our comparison.
trustworthy third party may set a validity time for each redirection
mapping so that the authoritative server can immediately respond                    5.1.4. Client location privacy
without an external request. Additionally, the authoritative server may                 For this privacy concern, we consider the client location information
attach a validity time to its response, leaving the response cacheable by           leaked in the path between the DNS recursive server and the authorita-
the recursive server and client.                                                    tive server. Ideally, any in-path eavesdropper or authoritative server can
                                                                                    learn a client's location from DNS messages. Thus, the extent of a client
5. Comparison of existing solutions                                                 location privacy leak depends on the distance between the exposed client
                                                                                    location and the actual client location.
    In this section, we compare all DNS-based solutions in CDN
                                                                                    5.1.5. Redirection privacy
                                                                                       This privacy concern is about uncovering a full snapshot of CDN
                                                                                    location-to-server mappings. That snapshot reveals private data about
                                                                                    the CDN infrastructure and the clustering clients. Compared with con-
                                                                                    ventional DNS, any scope-or preﬁx-based aggregated redirection mech-
                                                                                    anism enables easy and fast enumeration opportunities to observe the
                                                                                    operational practices of content providers.

                                                                                    5.2. Existing solutions in comparison

                                                                                       First, we identify three solutions that still use conventional DNS but
                                                                                    vary in the placement of DNS recursive servers.

                                                                                    5.2.1. Local server
                                                                                       One common practice is that the client uses a local DNS recursive
                                                                                    server to access a CDN service. Such local servers are either provided by
                                                                                    ISPs (Internet Service Providers) as default DNS servers or manually
                                                                                    conﬁgured by users for reliable and fast name resolution service. The
                                                                                    local server complies with existing clients and intermediate components.
                                                                                    Hence, the simplicity of client and intermediate transparency is retained.
                        Fig. 2. Client pseduonymizing.                                 In comparison with remote servers, local servers are believed to

                                                                              239
Z. Wang et al.                                                                                                        Digital Communications and Networks 4 (2018) 235–243

Table 1
Comparison of existing solutions.

  Solution                          Metric

                                    Client complexity   Intermediate transparency           CDN performance           Client location privacy        Redirection privacy

  Local sever                       Low                 Good                                Medium                    Medium                         Good
  Remote server                     Low                 Good                                Bad                       Good                           Good
  Client server                     High                Good                                Good                      Bad                            Good
  ECS                               Low                 Bad                                 Good                      Bad                            Bad
  Direct Resolution                 Medium              Good                                Good                      Bad                            Good
  Name Extension                    Low                 Good                                Good                      Bad                            Bad
  Client pseudononymizing           Low                 Bad                                 Good                      Good                           Good



provide better content delivery performance by maintaining the vicinity              client complexity is low. Because the client location information is coded
of the end-user and its DNS resolver. In a study of DNS performance, the             in the canonical domain name, Name Extension can be transparent to the
deployments of 50 commercial ISPs are DNS deployment is compared                     DNS recursive server. Similar to ECS, Name Extension exposes client
against widely used third-party DNS resolvers, namely GoogleDNS and                  location information and implements scope-based redirection. Hence, it
OpenDNS [31]. It was observed that third-party DNS resolvers did not                 has poor client location privacy and redirection privacy.
redirect users toward content available within the ISP, contrary to the
local DNS resolvers.                                                                 5.2.7. Client pseudononymizing
    However, the proximity between local servers and clients is not al-                  Client pseudononymizing maintains low client complexity because
ways ensured. For example, in the context of cellular networks, cellular             the pseudononymizing process at the client is lightweight. However,
DNS was found to be unsuitable for client localization [35]. As shown by             intermediate transparency is violated because the DNS recursive server
the measurement, even public DNS outperformed cellular DNS in terms                  requires modiﬁcations to accommodate client pseudononymizing. It en-
of CDN replica performance during 75% of the measurement time. Thus,                 sures CDN performance, client location privacy, and redirection privacy.
CDN performance and client location privacy levels in local servers are
both medium, in comparison with other solutions.                                     5.3. Modeling CDN performance
    As a one-to-one mapping based solution, local servers protect redi-
rection privacy well.                                                                    To better illustrate CDN performance, we develop a conceptual model
                                                                                     to evaluate the impact of location mismatches between clients and DNS
5.2.2. Remote server                                                                 recursive servers.
   Remote DNS recursive servers have been increasingly used in recent                    For optimal CDN performance, the provisioning of CDN surrogate
years. They are mostly utilized as public DNS services. Remote servers               servers often utilizes CDN replicas located in proximity to the requestors.
provide advantages in client complexity and intermediate transparency.               Without loss of generality, we can assume that the distribution of dis-
Owing to the location mismatches between clients and remote servers,                 tance between a DNS recursive server and a CDN surrogate server, which
CDN performance is often considered poor. However, the location mis-                 is denoted by f(x), follows the following conditions:
matches also protect client location privacy. Similar to local server,
remote servers ensure redirection privacy.                                           ● The probability that a DNS recursive server and a CDN surrogate
                                                                                       server are co-located is very close to zero. That is
5.2.3. Client server
   Hosting DNS recursive servers at clients is rare in practice, partly              limf ðxÞ ¼ 0                                                                     (1)
                                                                                     x→0
because it is uneconomical in resource constrained circumstances. The
pros include intermediate transparency, improved CDN performance                     ● The probability that a DNS recursive server and a CDN surrogate
given by the co-location of client and server, and good redirection pri-               server are inﬁnitely far away from each other is very close to zero.
vacy. The cons are high client complexity and poor client location privacy             That is
caused by the co-located server.
   Next, we compare existing proposals that more or less modify the                  limf ðxÞ ¼ 0                                                                     (2)
                                                                                     x→∞
conventional DNS.
                                                                                     ● The probability increases with the distance between a DNS recursive
5.2.4. ECS                                                                             server and a CDN surrogate server, if the distance falls below a point
    ECS introduces minor extra overhead to clients by adding the ECS                   with the highest probability, xmax. That is
option. It violates intermediate transparency by claiming the modiﬁed
recursive server. It succeeds in optimizing CDN performance but per-                 df ðxÞ
forms poorly in preserving client location privacy and redirec-                             >0         0 < x < xmax                                                   (3)
                                                                                      dx
tion privacy.
                                                                                     ● The probability decreases with the distance between the DNS recur-
5.2.5. Direct resolution                                                               sive server and the CDN surrogate server, if the distance is above a
   Direct Resolution still relies on DNS recursive servers to ﬁnd                      point with the highest probability, xmax. That is
authoritative servers, but makes clients solicit the answers on their own.
Thus, Direct Resolution has medium client complexity in comparison                   df ðxÞ
                                                                                            <0         x > xmax                                                       (4)
with local servers and client servers. It gains good intermediate trans-              dx
parency and CDN performance by sacriﬁcing its location privacy.
Because it essentially bases redirection on a single IP, it effectively re-          ● There is a point with the highest probability, xmax, satisfying
spects redirection privacy.
                                                                                     df ðxÞ
                                                                                            ¼0          x ¼ xmax                                                      (5)
5.2.6. Name extension                                                                 dx
   Name Extension makes relatively trivial changes to clients; thus, its                   In the following discussion, we use two distributions satisfying Eqs.

                                                                               240
Z. Wang et al.                                                                                                          Digital Communications and Networks 4 (2018) 235–243


(1)–(5) to investigate the expected distance between the client and the
CDN surrogate server, which is usually negatively correlated with the
user-perceived CDN performance.
    A Weibull distribution has the ability to assume the characteristics of
many different types of distributions. This has made it popular among
engineers. The Probability Density Function (PDF) of the Weibull dis-
tribution is given by

          k xk1 ðt=λÞk
f ðxÞ ¼           e        e       x0                                       (6)
          λ λ

where λ and k are the scale and shape parameters, respectively. Here, we
let λ ¼ 1.09 and k ¼ 5, to ensure that the mean will be 1. Fig. 3 shows the
PDF of the Weibull distribution.
    Fig. 4 shows the expected distance between a client and a CDN sur-
rogate server, given the distance between a DNS recursive server and a
CDN surrogate server according to the Weibull distribution in Fig. 3. We
can see that CDN performance degrades slowly when the location
mismatch is small. E.g., the expected distance between a client and a CDN
surrogate server increases by less than 5% when the DNS recursive server
is 0.2 units away from the client. The CDN performance penalty grows
rapidly with the increase in location mismatch. E.g., the expected dis-                             Fig. 4. CDN performance under Weibull distribution in Fig. 3.
tance between the client and the CDN surrogate server increases by 113%
when the DNS recursive server is 2 units away from the client. The results
explain the performance issue with the remote server services as well as
the medium latency costs of the local server services. They also fully meet
previous measurements [24,28,31].
    The PDF of a Lognormal distribution is given by

           1
f ðxÞ ¼ pﬃﬃﬃﬃﬃﬃﬃﬃﬃﬃe½lnðxÞμ =ð2σ Þ
                              2    2
                                          x0                                (7)
         2πσx
    We use a lognormal distribution with parameters μ and σ as 0.5493
and 1.0481, respectively, to ensure that the mean and variance will be 1
and 2, respectively. Fig. 5 shows the PDF of that Lognormal distribution.
    Fig. 6 shows the expected distance between a client and a CDN sur-
rogate server, given the distance between the DNS recursive server and
the CDN surrogate server according to the Lognormal distribution in
Fig. 5. The curve in Fig. 6 is somewhat similar to the curve in Fig. 4,
except that Fig. 6 exhibits a steeper slope than Fig. 4. This is due to the
“near-ﬁeld” effects of the Lognormal distribution, which are not exhibi-
ted in the Weibull distribution despite the distribution equal
mean values.


                                                                                                Fig. 5. PDF of Lognormal distribution (μ ¼ 0.5493 and σ ¼ 1.0481).


                                                                                         5.4. Existing solutions in applications

                                                                                             According to previous measurements [28], the three most popular
                                                                                         public DNS services (Google, OpenDNS, and Level3) had been adopted by
                                                                                         8.6% of sampled users in December 2011. Also, a 27% annual growth
                                                                                         rate in public DNS adoption was found in the survey. In particular,
                                                                                         Google's DNS service claimed a 74% annual increase, which made it the
                                                                                         most-used public DNS service. Because remote public DNS services may
                                                                                         be greatly penalized in CDN performance, there are growing concerns
                                                                                         over it.
                                                                                             By now, it can be inferred that a majority of internet users still use
                                                                                         local DNS recursive severs, although there are virtually not direct mea-
                                                                                         surements or surveys on this usage pattern. This is because all other so-
                                                                                         lutions listed in Table 1 are either rarely implemented or seldom
                                                                                         deployed, except for the remote server solution.
                                                                                             In the following, we exemplify the usage of each solution in Table 1
                                                                                         using appropriate scenarios:

                                                                                         5.4.1. Local server
                 Fig. 3. PDF of Weibull distribution (λ ¼ 1.09 and k ¼ 5).                  For most common internet users, a local server may be their default

                                                                                   241
Z. Wang et al.                                                                                                          Digital Communications and Networks 4 (2018) 235–243


                                                                                      also be neutralized based on our analysis above.

                                                                                      5.4.6. Name extension
                                                                                           Name Extension is a good choice if 1) the authoritative side supports
                                                                                      it; 2) both client location and redirection are non-conﬁdential.

                                                                                      5.4.7. Client pseudononymizing
                                                                                          Client pseudononymizing is best suited to those users who desire the
                                                                                      strongest protection of client location privacy and redirection privacy at
                                                                                      almost no cost of CDN performance. It is expected to grow into differ-
                                                                                      entiated services, because it places heavy demands on the DNS
                                                                                      infrastructure.

                                                                                      6. Conclusions and outlook

                                                                                          This paper has presented a comprehensive survey of DNS-based
                                                                                      CDNs. While DNS-based server redirecting demonstrates its merits
                                                                                      compared with other approaches, remote DNS poses critical issues in
                                                                                      terms of CDN performance. ECS, Name Extension, and Direct Resolution
                                                                                      are three promising proposals to address the remote DNS problem. As an
                                                                                      increasingly concerned yet probably mostly overlooked issue, privacy is
           Fig. 6. CDN performance under Lognormal distribution in Fig. 5.
                                                                                      highlighted in the design of DNS-based CDN. Unlike in most prior works,
                                                                                      client location privacy concerns and redirection privacy concerns are
and probably simplest solution. They do not have to rely on installations             identiﬁed and addressed. A recently proposed client pseudononymizing
on their machines, or external DNS infrastructure upgrades by CDN                     scheme is the most effective method of addressing both privacy concerns.
service providers or network service providers. Moreover, they would not              A comparative study of all exiting DNS-based CDN solutions shows that
suffer from the probably signiﬁcant CDN performance costs of remote
                                                                                      each model has advantages and disadvantages. In particular, ECS is found
servers. If the exposure of their locations to the operator of local DNS              to lack intermediate transparency and privacy protection despite its good
server is not a signiﬁcant concern, a local server is often the ﬁrst choice
                                                                                      CDN performance, and Direct Resolution is shown to respect redirection
for most DNS non-professionals.                                                       privacy at the expense of increased client complexity.
                                                                                          As a fundamental substrate of today's internet, DNS has been
5.4.2. Remote server                                                                  constantly yet cautiously improved in adapting to emerging technologies
    Remote DNS recursive servers may be preferred when local DNS
                                                                                      and services. It is always risky to roll out a new DNS solution on an
servers are not available, stable, or secure. Often it is recommended that            Internet scale without fully testing and validating it. Therefore, extensive
remote servers be conﬁgured as secondary or backup servers, because
                                                                                      implementation, experiments, and performance modeling and evaluation
that increases the diversity of DNS servers. Another reason for using                 of emerging DNS-based CDN solutions will be top prionties for the DNS
remote servers is that the privacy of the client location is considered a
                                                                                      and CDN community in the next few years.
priority. Note that the biggest risk with remote servers is the increased
latency experienced by CDN users.
                                                                                      References

5.4.3. Client server                                                                   [1] H. Yin, X. Liu, F. Qiu, N. Xia, C. Lin, H. Zhang, V. Sekar, G. Min, Inside the bird's
    Installing a DNS server on a local machine is not a difﬁcult task for                  nest: measurements of large-scale live VoD from the 2008 olympics, in: Proc. of the
                                                                                           9th ACM SIGCOMM Conference on Internet Measurement Conference (IMC '09),
common internet users. However, the greatest issue of that conﬁguration
                                                                                           2009, pp. 442–455.
is the diminished cache sharing effects, which beneﬁt shared DNS                       [2] P. Wendell, M.J. Freedman, Going viral: ﬂash crowds in an open CDN, in: Proc. of
servers. Cache sharing ensures that a query from one user may be                           the 2011 ACM SIGCOMM Conference on Internet Measurement Conference (IMC
promptly responded to cache if that query was recently issued from                         '11), 2011, pp. 549–558.
                                                                                       [3] A. Vakali, G. Pallis, Content delivery networks: status and trends, IEEE Internet
another user. In the mechanism, the cache hit rate may be greatly                          Comput. 7 (no. 6) (2003) 68–74.
enhanced by a large set of users. However, when a cache is unilaterally                [4] J. Dilley, B. Maggs, J. Parikh, H. Prokop, R. Sitaraman, B. Weihi, Globally
used by one user, the cache miss rate will be increased along with the                     distributed content delivery, IEEE Internet Comput. 6 (no. 5) (2002) 50–58.
                                                                                       [5] E. Nygren, R.K. Sitaraman, J. Sun, The akamai network: a platform for high-
prolonged response latency. Another negative impact is the augmented                       performance internet applications, ACM SIGOPS Oper. Syst. Rev. 44 (no. 3) (2010)
load on DNS authoritative servers.                                                         2–19.
                                                                                       [6] L. Wang, V. Pai, L. Peterson, The effectiveness of request redirection on cdn
                                                                                           robustness, ACM SIGOPS Oper. Syst. Rev. 36 (no. SI) (2002) 345–360.
5.4.4. ECS                                                                             [7] V.K. Adhikari, Y. Guo, F. Hao, V. Hilt, Z.-L. Zhang, A tale of three cdns: an active
    The adoption of ECS has different meanings for different stake-                        measurement study of hulu and its cdns, in: Computer Communications Workshops
holders. For the CDN service provider, ECS is preferred if all the                         (INFOCOM WKSHPS), 2012 IEEE Conference, 2012, pp. 7–12.
                                                                                       [8] S. Manfredi, F. Oliviero, S.P. Romano, Optimized balancing algorithm for content
following are met: 1) a large portion of its users rely on remote servers; 2)              delivery networks, IET Commun. 6 (no. 7) (2012) 733–739.
its CDN mapping is not private; 3) ECS gains support from a large portion              [9] A. Alsum, M.L. Nelson, R. Sanderson, H.V. Sompel, Archival HTTP redirection
of recursive servers. For the end user, ECS is the best choice if all the                  retrieval policies, in: Proc. of the 22nd International Conference on World Wide
                                                                                           Web (WWW '13), 2013, pp. 1051–1058.
following are met: 1) the CDN service provider supports ECS; 2) the user
                                                                                      [10] B. Krishnamurthy, C. Willis, Y. Zhang, On the use and performance of content
uses a remote server; 3) ECS gains support from the user's recur-                          distribution network, in: Proc. of 1st International Internet Measurement Workshop
sive server.                                                                               (IMC '01), 2001, pp. 169–182.
                                                                                      [11] T. Yoshimura, Y. Yonemoto, T. Ohya, M. Etoh, S. Wee, Mobile streaming media
                                                                                           CDN enabled by dynamic SMIL, in: Pro. of the 11th International Conference on
5.4.5. Direct resolution                                                                   World Wide Web (WWW '02), 2002, pp. 651–661.
    Direct Resolution is able to strike a balance between client servers and          [12] M. Calder, A. Flavel, E. Katz-Bassett, R. Mahajan, J. Padhye, Analyzing the
external servers (which include remote servers and local servers) in terms                 performance of an anycast CDN, in: Proc. of the 2015 ACM Conference on Internet
                                                                                           Measurement Conference (IMC '15), 2015, pp. 531–537.
of client complexity and CDN performance. Thus, its applications should


                                                                                242
Z. Wang et al.                                                                                                                       Digital Communications and Networks 4 (2018) 235–243

[13] H.A. Alzoubi, S. Lee, M. Rabinovich, O. Spatscheck, J.V. Merwe, Anycast CDNS                  [27] F. Streibelt, J. B€
                                                                                                                          ottger, N. Chatzis, G. Smaragdakis, A. Feldmann, Exploring EDNS-
     revisited, in: Proc. of the 17th International Conference on World Wide Web (WWW                   client-subnet adopters in your free time, in: Proc. of the 2013 ACM SIGCOMM
     '08), 2008, pp. 277–286.                                                                           Conference on Internet Measurement Conference (IMC '13), 2013, pp. 305–312.
[14] H.A. Alzoubi, S. Lee, M. Rabinovich, O. Spatscheck, J.V. Merwe, A practical                   [28] J.S. Otto, M.A. Sanchez, J.P. Rula, F.E. Bustamante, Content delivery and the
     architecture for an anycast CDN, ACM Trans. Web 5 (no. 4) (2011). Article 17, 29                   natural evolution of DNS: remote dns trends, performance issues and alternative
     pages.                                                                                             solutions, in: Proc. of the 2012 ACM Conference on Internet Measurement
[15] Z.A. Qudah, S. Lee, M. Rabinovich, O. Spatscheck, J.V. Merwe, Anycast-aware                        Conference (IMC '12), 2012, pp. 523–536.
     transport for content delivery networks, in: Proc. of the 18th International                  [29] W. Benchaita, S.G. Doudane, S. Tixeuil, Stability and optimization of DNS-based
     Conference on World Wide Web (WWW '09), 2009, pp. 301–310.                                         request redirection in CDNs, in: Proc. of the 17th International Conference on
[16] Akamai, www.akamai.com.                                                                            Distributed Computing and Networking (ICDCN '16), Article 11, 2016, 10 pages.
[17] Limelight Networks, www.limelight.com.                                                        [30] J. Jung, E. Sit, H. Balakrishnan, R. Morris, DNS performance and the effectiveness of
[18] Mirror Image, www.mirror-image.com.                                                                caching, IEEE/ACM Trans. Netw. 10 (no. 5) (2002) 589–603.
[19] R. Fanou, G. Tyson, P. Francois, A. Sathiaseelan, Pushing the frontier: exploring the         [31] B. Ager, W. Mühlbauer, G. Smaragdakis, S. Uhlig, Comparing DNS resolvers in the
     african web ecosystem, in: Proc of the 25th International Conference on World                      wild, in: Proc. of the 10th ACM SIGCOMM Conference on Internet Measurement
     Wide Web (WWW '16), 2016, pp. 435–445.                                                             (IMC '10), 2010, pp. 15–21.
[20] H.A. Alzoubi, M. Rabinovich, O. Spatscheck, The anatomy of LDNS clusters:                     [32] H. Shulman, Pretty bad privacy: pitfalls of DNS encryption, in: Proc. of the 13th
     ﬁndings and implications for web content delivery, in: Proc. of the 22nd                           Workshop on Privacy in the Electronic Society (WPES '14), 2014, pp. 191–200.
     International Conference on World Wide Web (WWW '13), 2013, pp. 83–94.                        [33] S.H. Jeong, A.R. Kang, J. Kim, H.K. Kim, A. Mohaisen, A longitudinal analysis of.i2p
[21] C. Contavalli, W. Gaast, D. Lawrence, W. Kumari, Client subnet in DNS queries, in:                 leakage in the public DNS infrastructure, in: Proc. of the ACM SIGCOMM
     IETF RFC 7871, 2016, pp. 1–29.                                                                     Conference (SIGCOMM '16), 2016, pp. 557–558.
[22] J. Damas, M. Graff, P. Vixie, Extension mechanism for DNS (EDNS(0)), in: IETF RFC             [34] L. Zhu, Z. Hu, J. Heidemann, D. Wessels, A. Mankin, N. Somaiya, T-DNS:
     6891, 2013, pp. 1–16.                                                                              connection-oriented DNS to improve privacy and security (poster abstract),
[23] Z. Wang, A.L. Hu, A lightweight solution to remote DNS, in: Proc of the IEEE 32nd                  SIGCOMM Comput. Commun. Rev. 44 (no. 4) (2014) 379–380.
     International Performance Computing and Communications (IPCCC '13), 2013,                     [35] J.P. Rula, F.E. Bustamante, Behind the curtain: cellular DNS and content replica
     pp. 1–3.                                                                                           selection, in: Proc. of the 2014 Conference on Internet Measurement Conference
[24] J.S. Otto, M.A. Sanchez, J.P. Rula, T. Stein, F.E. Bustamante, Namehelp: intelligent               (IMC '14), 2014, pp. 59–72.
     client-side DNS resolution, in: Pro. of the ACM SIGCOMM Conference on                         [36] S. Bortzmeyer, DNS privacy considerations, in: IETF RFC 7626, 2015, pp. 1–17.
     Applications, Technologies, Architectures, and Protocols for Computer                         [37] Z. Wang, Analysis of ﬂooding DoS attacks utilizing DNS name error queries, KSII
     Communication (SIGCOMM '12), 2012, pp. 287–288.                                                    Trans. Internet & Inf. Syst. 6 (no. 10) (2012) 2750–2763.
[25] Z. Wang, POSTER: pseudonymizing client as a privacy-preserving service: a case                [38] Z. Wang, S.S. Tseng, Impact evaluation of DDoS attacks on DNS cache server using
     study of CDN, in: Proc of the 22nd ACM SIGSAC Conference on Computer and                           queuing model, KSII Trans. Internet & Inf. Syst. 7 (no. 4) (2013) 859–909.
     Communications Security (CCS '15), 2015, pp. 1–3.                                             [39] X. Chang, J. Li, G. Wang, Z. Zhang, L. Li, Y. Niu, Software deﬁned backpressure
[26] M. Calder, X. Fan, Z. Hu, E. Katz-Bassett, J. Heidemann, R. Govindan, Mapping the                  mechanism for edge router, in: Proc. of the 2015 IEEE 23rd International
     expansion of Google's serving infrastructure, in: Proc. of the 2013 ACM SIGCOMM                    Symposium on Quality of Service (IWQoS), 2015, pp. 171–176.
     Conference on Internet Measurement Conference (IMC '13), 2013, pp. 313–326.




                                                                                             243
