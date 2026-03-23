                                                                                                                                     PDF Download
                                                                                                                                     2716281.2836101.pdf
                                                                                                                                     21 March 2026
                                                                                                                                     Total Citations: 29
                                                                                                                                     Total Downloads: 333
    .
    .
        Latest updates: hps://dl.acm.org/doi/10.1145/2716281.2836101




                                                                                                                                     .
                                                                                                                                     .
                                                                                                                           Published: 01 December 2015
        .
        .
                                                                                                                           .
    RESEARCH-ARTICLE




                                                                                                                           .
                                                                                                                           Citation in BibTeX format
    Characterizing IPv4 anycast adoption and deployment




                                                                                                                           .
                                                                                                                           .
                                                                                                                           CoNEXT '15: Conference on emerging
                                                                                                                           Networking Experiments and
    DANILO CICALESE, Telecom Paris, Palaiseau, Ile-de-France, France                                                       Technologies
    .
                                                                                                                           December 1 - 4, 2015
    JORDAN AUGÉ, Telecom Paris, Palaiseau, Ile-de-France, France                                                           Heidelberg, Germany
    .
                                                                                                                           .
    DIANA JOUMBLATT, Telecom Paris, Palaiseau, Ile-de-France, France




                                                                                                                           .
                                                                                                                           Conference Sponsors:
                                                                                                                           SIGCOMM
    .
    TIMUR FRIEDMAN
    .
    DARIO ROSSI, Telecom Paris, Palaiseau, Ile-de-France, France
    .
    .
    .
    Open Access Support provided by:
    .
    Telecom Paris
    .
                                         CoNEXT '15: Proceedings of the 11th ACM Conference on Emerging Networking Experiments and Technologies (December 2015)
                                                                                                                          hps://doi.org/10.1145/2716281.2836101
                                                                                                                                             ISBN: 9781450334129
.
                                        Characterizing IPv4 Anycast
                                         Adoption and Deployment

                     Danilo Cicalese                                      Jordan Augé                      Diana Joumblatt
                   Telecom ParisTech                                  Telecom ParisTech                   Telecom ParisTech
              danilo.cicalese@enst.fr                              jordan.auge@enst.fr                    joumblat@enst.fr
                                              Timur Friedman                                Dario Rossi
                                              UPMC Sorbonne                             Telecom ParisTech
                                                Universités                            dario.rossi@enst.fr
                                        timur.friedman@lip6.fr

ABSTRACT                                                                             1. INTRODUCTION
This paper provides a comprehensive picture of IP-layer                                 Modern content-delivery networks (CDNs) employ L7-
anycast adoption in the current Internet. We carry on                                anycast, exploiting DNS and HTTP redirection tech-
multiple IPv4 anycast censuses, relying on latency mea-                              niques to direct traffic from a client to any server in a
surement from PlanetLab. Next, we leverage our novel                                 group of geographically dispersed but otherwise equiv-
technique for anycast detection, enumeration, and ge-                                alent servers. Such redirection techniques perform load
olocation [17] to quantify anycast adoption in the In-                               balancing among nearby replicas and map users to the
ternet. Our technique is scalable and, unlike previous                               closest replica, reducing user-perceived latency.
efforts that are bound to exploiting DNS, is protocol-                                  Network-level (IP) anycast [4] is another instantia-
agnostic. Our results show that major Internet com-                                  tion of the same principle, where a set of replicas spread
panies (including tier-1 ISPs, over-the-top operators,                               across a number of locations around the world share a
Cloud providers and equipment vendors) use anycast:                                  standard unicast IP address. BGP policies route pack-
we find that a broad range of TCP services are offered                               ets sent to this address to the nearest replica according
over anycast, the most popular of which include HTTP                                 to BGP metrics, notably (though not only) the number
and HTTPS by anycast CDNs that serve websites from                                   of autonomous system (AS) hops.
the top-100k Alexa list. Additionally, we complement                                    L7 anycast and IP anycast are complementary. On
our characterization of IPv4 anycast with a description                              one hand, L7 anycast allows for very dense server de-
of the challenges we faced to collect and analyze large-                             ployments with customized user-server mapping algo-
scale delay measurements, and the lessons learned.                                   rithms and complex operations to shuffle content among
                                                                                     servers. Although this allows a fine grain control of the
CCS Concepts                                                                         server selection, it also increases the management com-
                                                                                     plexity [36]. On the other hand, IP anycast offers a
•Networks → Network measurement; Network                                             loose control over user-server mapping, which limits the
structure; •General and reference → Measurement;                                     deployment density but considerably simplifies manage-
                                                                                     ment by delegating replica selection to IP routing.
Keywords                                                                                In recent years, the scientific community has made
Anycast; Census; Network monitoring; Network mea-                                    significant contributions to understand L7 anycast, e.g.,
surement; IPv4; BGP                                                                  to uncover deployments and geolocate points of pres-
                                                                                     ence (PoPs) with active measurements [15, 45–47], and
Permission to make digital or hard copies of all or part of this work for personal   characterize the performance of L7 anycast via passive
or classroom use is granted without fee provided that copies are not made or
distributed for profit or commercial advantage and that copies bear this notice      measurements [5, 12]. Yet, with few exceptions [45] as
and the full citation on the first page. Copyrights for components of this work      these application-level deployments are diverse, and as
owned by others than ACM must be honored. Abstracting with credit is per-            PoPs are pervasive, such efforts generally focus on a
mitted. To copy otherwise, or republish, to post on servers or to redistribute to
lists, requires prior specific permission and/or a fee. Request permissions from     single application/player such as Akamai [46], YouTube
permissions@acm.org.                                                                 [5, 47], Amazon [12] and Google [15]. A recent trend in
CoNEXT ’15 December 01-04, 2015, Heidelberg, Germany                                 the area of Internet infrastructure mapping is to exploit
c 2015 ACM. ISBN ISBN 978-1-4503-3412-9/15/12. . . $15.00                            the edns-client-subnet DNS extension (ECS) [20] to un-
DOI: http://dx.doi.org/10.1145/2716281.2836101
cover the geographical footprints of major CDNs [15,                        Measurement                  Analysis [16] Ground truth
                                                                IPv4
                                                                              PlanetLab                    Detec�on
45]. Still, given the wide design space and flexibility         hitlist
                                                                              (ICMP,TCP,UDP                Enumera�on
                                                                                                                        Anycast     Valida�on
                                                                Blacklist                     Greylist
in L7 anycast implementations, it is hard to generalize                        RTT Latency)
                                                                                                           Geoloca�on             Characteriza�on

results of L7 anycast usage, performance, and geograph-                                                    Unicast       nmap portscan
ical deployments across CDNs.
   Conversely, most IP anycast studies [9,34,43] are lim-      Figure 1: Overall workflow of the anycast census
ited to DNS, which has historically been the killer appli-
cation of IP anycast [3,7,29,37]. This paper shows that
the usage of IP anycast has significantly changed in re-
cent years. In particular, major players of the Internet
ecosystem including Internet service providers (ISPs),
OTTs, and manufacturers provide a diversity of ser-
vices with IP anycast (e.g., content distribution, cloud
services, web hosting, web acceleration, DDoS protec-
tion). Yet, missing an Internet-scale study of IP anycast
deployment, the scientific community is not up-to-date
with such changes, and knowledge related to non-DNS
anycast (e.g., anycast IP address ranges, the number           Figure 2: Analysis technique: anycast detection
of replicas behind each address, services provided) is         (figure adapted from [17])
anecdotal at best, which motivates our current work.
   Indeed, while valuable research efforts (Sec. 2), started
with seminal work such as [30] and culminated with [1,
                                                               efforts (Sec. 2.2). For the sake of readability, we describe
22] more recently, focus on unicast censuses, this paper
                                                               our complete workflow with the help of Fig. 1.
presents the first census of the use of IPv4 anycast in
the Internet. First, we describe the challenges faced in       2.1          Workflow
designing a system able to collect and analyze Internet-
scale delay measurements [17] in a short time frame            Measurements. We use a distributed software run-
(Sec. 3). Next, we discuss the results of a thorough ex-       ning over PlanetLab (PL) to conduct IPv4 anycast cen-
perimental campaign, analyzing anycast adoption over           suses with ICMP latency measurements. Each of the
multiple anycast IPv4 censuses (Sec. 4). To summarize          O(102 ) PL vantage points (VP) receives a set of O(107 )
our main contributions:                                        IP/32 targets (namely, the IPv4 hitlist provided by [31]).
                                                               We consider that each IP/32 in this hitlist is repre-
   • We conduct and combine delay measurements from            sentative of the corresponding IP/24 subnet, and thus
     four full censuses, based on which we find about          cover the entire IPv4 address space (we validate this
     O(103 ) IP/24 subnets to be anycasted.                    assumption in Sec. 3.1). Later on, we thoroughly jus-
                                                               tify our choices of the measurement platform (e.g. PL
   • We characterize the geographical footprint of IP
                                                               over RIPE, MLab, Archipelago, etc. in Sec. 3.2), soft-
     anycast deployments, that we (conservatively) find
                                                               ware (e.g., fastping/TDMI over Zmap in Sec. 3.3), and
     on average to have O(10) replicas.
                                                               protocols (e.g., ICMP over TCP or UDP in Sec. 3.4).
   • We provide empirical evidence that IP anycast is
     used by ASes in the CAIDA top-10 rank and by              Analysis. The dataset collected from the census is
     ASes serving content over HTTP and HTTPS for              uploaded to a central repository. We run an iterative
     websites in the Alexa top-100 rank.                       algorithm that we recently proposed [17] to detect, enu-
                                                               merate, and geolocate anycast replicas over the dataset.
   • We show that anycast is used to serve a large di-
                                                               For the sake of completeness we provide an overview of
     versity of stateful services (a complementary port-
                                                               the technique, which is based on detection of speed-of-
     scan finds 10,000 open port, about 500 of which
                                                               light violations [35]: as depicted in Fig. 2, the main idea
     are well known) running on top of TCP.
                                                               is that in case latency measurements from two vantage
   • We describe our distributed system design, able to        points toward the same target exhibit geo-inconsistency,
     perform and analyze one census in under 5 hours.          then it is safe to assume the target to be anycast.
                                                                  We illustrate an execution of the technique in Fig. 3.
   • We make our census results browsable at [21].             Briefly, given a specific target IP, (a) we first map each
                                                               RTT latency measurement to a disk centered around the
2. METHODOLOGY OVERVIEW                                        VP, that by definition contains the target contacted;(b)
  In this section, we present an overview of our work          if two such disks do not intersect, as just discussed, we
(Sec. 2.1) and put it in perspective with prior research       can infer that VPs are contacting two different replicas,
(a)     Measure- (b) Detect: Non- (c) Enumerate: Solving a Maxi- (d)               Geolocate: (e) Iterate: Col-
ment: Map RTT overlapping disks mum Independent Set (MIS) prob- Maximum likeli- lapse disks around
samples to disks imply      speed-of- lem yields non-overlapping disk, each hood classification geolocated repli-
centered  around light violation      containing a different replica (two problem         (city- cas until conver-
VPs                                   steps shown)                          level)               gence

         Figure 3: Illustration of the Analysis technique: enumeration and geolocation steps)


as is the case for the green discs in Fig. 3(b). While ob-
servation of inconsistency among any pair lead to any-
cast detection, leveraging multiple observations it is pos-
sible to further enumerate such replicas. Enumeration
is described in step (c): to provide a conservative esti-
mation of the minimum number of anycast replicas, we
solve a Maximum Independent Set (MIS) problem. MIS
outputs a set of non-overlapping disks which contain a
different replica of the same target: while MIS prob-         Figure 4: Anycast census at a glance: typical
lem is NP-Hard, we solve it using a 5-approximation           census magnitude
algorithm that greedily operates on disks of increasing
radius size as in Fig. 3(c), and that in practice yield
results that are very close to the optimum provided           anycast IPs obtained from the census, to reveal open
by a prohibitively more costly brute force solution [17].     ports and the software their run. Given that an exhaus-
Geolocation happens in step (d): in the smallest disk,        tive portscan (i.e., of the 216 TCP and UDP portspaces,
we geolocate the replica at city-level granularity with a     over all replicas of all anycast deployments) still incurs
maximum likelihood estimator biased toward city pop-          a prohibitive measurement cost, we restrict the mea-
ulation; actually, we find that the city population has       surements to TCP services (i.e., the most unexpected
sufficient discriminative power alone (about 75% accu-        ones) and interesting deployments (i.e., deployments
racy [18]), so that our geolocation criterion boils down      with large geographical footprints). We discuss any-
into picking the largest city in that disk. Finally, (e)      cast services in Sec. 4.3, finding over 10,000 open ports,
we coalesce the disk to the classified city, which reduces    that map to about 500 well-known services, and finger-
disk overlap and allows iteration of the algorithm until      printing some 30 software applications.
convergence, thus increasing the recall (i.e., number of
replicas discovered) along each iteration.                    Scale, Completeness, and Accuracy. Although we
   The analysis technique [17] is of course not an original   described the anycast geolocation technique in [17], we
contribution of this work, whose main aims are instead        had to overcome several challenges to run it at Internet-
to scale up its application to an Internet-wide census on     scale and within a short timespan, for which we went
the one hand (Sec. 3), and to analyse and publish the         through multiple re-engineering phases. We believe that
gathered dataset on the other hand (Sec. 4).                  a number of lesson learned (e.g., as the counter-intuitive
                                                              need to slow-down the sending rate to complete a cen-
Characterization and Validation. In addition to               sus) are worth sharing, and discuss them in Sec. 3.
anycast detection, the previous steps allow to geolocate        Notice that a large number of vantage points is re-
the replicas behind each anycast IP/24. As outlined in        quired to provide an accurate picture of anycast de-
Fig 1, we validate the output of the geolocation step         ployment, especially in terms of the number of repli-
whenever a ground truth is available (as in Sec. 3.4 for      cas discovered around the world. Related work that fo-
CDNs such as CloudFlare and Edgecast, complemen-              cuses on O(1) targets (i.e., DNS root-servers) indeed run
tary to the validation limited to DNS in [17]).               measurement campaigns involving from O(104 ) [10] to
  Finally, we provide a fine-grained characterization of      O(105 ) [25] vantage points to achieve ≈90% recall [25].
IP/24 anycast services. While our detection method-           In our case, given the sheer size O(107 ) of our target set,
ology is service-agnostic, we use nmap [38] on a list of      we tradeoff completeness for scale, and possibly under-
estimate the number of IP-anycast replicas, as we use a       only few hours, constitutes an achievement per se.
mere O(102 ) vantage points.
  Still, our results provide a broad, conservative, yet       Geolocation and infrastructure mapping. Uni-
accurate picture of Internet anycast usage: for targets       cast geolocation is a well investigated research topic.
for which we have the ground truth, our city-level ge-        Numerous techniques based on latency measurements
olocation is accurate in about 75% of the cases with a        [23, 24, 28] and databases [41, 44] have been proposed.
median error of 350 Km otherwise (Sec. 3.4).                  Yet, database techniques are not only unreliable with
                                                              unicast [41], but also with anycast, since they adver-
Typical census. In this work, we perform four IPv4            tise a single geolocation per IP. Similarly, latency-based
censuses and analyse the results obtained from their          techniques [23, 24, 28] use triangulation, and geolocate
combination. For each of the O(102 ) VPs the magnitude        unicast addresses at the intersection of multiple latency
of a typical census is illustrated in Fig. 4: starting from   measurements from geographically dispersed vantage points.
a hitlist of O(107 ) targets, less than half send a reply     However, this assumption no longer necessarily holds for
(Sec. 3.1). ICMP replies include O(105 ) errors, some of      anycast as depicted in Fig. 3.
which relates to administratively prohibited communi-            L7-anycast infrastructure mapping studies [15,45] lever-
cation: senders of these ICMP error messages are added        age ECS requests to geolocate servers: (millions of) re-
to a greylist, to avoid probing them again in future cen-     quests are sent with different client IPs from one VP to
suses (Sec. 3.3). Finally, running the anycast geoloca-       unveil (thousands of) unicast IP addresses correspond-
tion technique over the O(106 ) targets that generate         ing to PoPs of major OTTs. However, ECS support
valid ICMP echo reply messages, we discover roughly           is becoming widespread to enhance the user online ex-
O(103 ) IP/24 anycast deployments, corresponding to           perience, but is not yet pervasive. Finally, the tech-
approximately 0.1h of the whole IPv4 address space –          nique fails with alternative L7-anycast design relying
the proverbial needle in the IPv4 haystack.                   on HTTP redirection.
                                                                 To the best of our knowledge, no IP-anycast geolo-
2.2    State of the art                                       cation technique exists other than our own: as such
                                                              no other study, apart from this work, deals with any-
Anycast vs Unicast. In standard IP unicast censuses,          cast infrastucture mapping. With respect to ECS-based
the set of targets can be split among VPs for scalability     technique for L7 anycast, our technique allows to re-
reasons. In contrast, in the anycast case, all targets        duce the cardinality of the problem without sacrificing
should be probed by all VPs to provide an accurate            geolocation accuracy (a qualitative comparison is pro-
map of geographical footprints. Given that the number         vided in [17]). Additionally, since BGP provides a uni-
of active VPs in PL is around 300, and that only one          fied redirection technique, IP-anycast offers an unprece-
IP/32 target for each IP/24 subnet needs to be probed         dented opportunity to broadly assess all deployments at
in a given anycast census, it follows that the raw amount     once.
of probe traffic is only slightly larger than that of an
unicast censuses.                                             Anycast discovery and characterization. Prior
   In the unicast case, the relative location of VPs with     work investigates different aspects related to anycast,
respect to targets is irrelevant. Therefore, census strate-   with a focus on discovery and enumeration [25, 35] or
gies cover extremes such as a single centralized high-end     on characterization [9–11, 19, 32, 34, 43], but to the best
server capable of O(106 ) probes-per-second on a well         of our knowledge, not on anycast census. Closest to
provisioned 1 Gbps Ethernet connection as in Zmap [22],       ours [17] is the work of [25, 35]. Specifically, [17] is
or a highly decentralized system that exploits O(105 )        a service-agnostic technique for detection, enumeration
low-resource gateways as in the illegal Carna Botnet          and geolocation. Similarly to [17], speed of light vio-
census [1]. Our system design sits halfway between            lation is used in [35] (however limited to detection and
these two extremes: in particular, it uses an efficient       not capable of enumeration/geolocation). Conversely,
application-level multi-threaded scanner capable of O(104 )   [25] exploits DNS-specificities (i.e., CHAOS requests)
probes/sec, distributed over O(102 ) PlanetLab nodes.         to enumerate DNS replicas (but unlike [17] is neither
   It is also worth pointing out that an independent          capable of geolocation, nor applicable beyond DNS).
analysis [33] of the Carna Botnet dataset found multiple         Other studies assess the performance of current IP
campaigns, covering a cumulative number of probes ex-         anycast deployments, with a focus on metrics such as
ceeding a full IPv4 census, over a duration of 8 months.      proximity [9,10,19,34,43], affinity [9–11,13,34,43], avail-
Additionally, [33] suggests that due to an overlap in the     ability [10,32,43], and load-balancing [10,11]. Yet, these
target set, not all hosts were probed, neither during the     studies focus on DNS, which is just a piece of the cur-
two fast scan campaign identified, nor during the whole       rent anycast puzzle.
measurement period. As such, our measurement cam-                Finally, some work study IP-anycast CDN, such as [16,
paign comprising multiple anycast censuses each lasting
27]. However these focused studies add yet other useful
pieces to the puzzle, that remained so far incomplete,
lacking the broad perspective given by a Internet-wide
coverage over all prefixes and services.

3. SYSTEM DESIGN
   Anycast detection relies on measuring round trip de-
lays between a set of vantage points and a target IP ad-
dress to uncover geo-inconsistencies. Running an Inter-
net census thus requires measurements towards millions
of destinations, ideally in a short timeframe: we now
describe and justify system design choices that allow us
                                                               Figure 5: Microsoft deployment as seen from
to perform multiple censuses, that we analyze later in
                                                               PlanetLab (21 replicas) vs RIPE (54 replicas).
Sec. 4. Items discussed in this section concern the se-
                                                               Notice that PlanetLab results (white markers)
lection of targets (Sec. 3.1), the measurement platform
                                                               are a subset of RIPE (white and black markers)
(Sec. 3.2) and software (Sec. 3.3), as well as the network
protocol used (Sec. 3.4). Finally, we report considera-
tions about the scalability of our workflow (Sec. 3.5).        them to reduce the target size to 6.6 · 106 per VP.

3.1    Census targets                                          Coverage. Given our census aim, we verify how well
Census granularity. Unlike multicast, anycast ad-              this hitlist covers all routed /24 prefixes. We therefore
dresses need no reservation into the IP space: as any IP       obtain from CAIDA a dump of routing tables originat-
address can be a candidate, this makes deployment easy,        ing from both RIPE RIS and RouteViews collectors.
but the detection of anycast addresses hard. Luckily, to       To compare the hitlist vs the advertised prefixes, we
avoid a significant increase in the size of routing tables,    split the latter in /24, obtaining 10,616,435 /24 pre-
BGP standard practice [4] is to ignore or block prefixes       fixes, of which 10,615,563 have a representative in the
shorter that /24. Thus, /24 is the minimum granular-           hitlist (over 99.99% coverage). We additionally cross-
ity for anycasted services, which is a good granularity        check our observed target responsiveness with the ex-
for our census. We validate this assumption with (spot)        pected recall: specifically, recent ICMP scans [48] ob-
verifications for all IP addresses on some IP/24 (belong-      serve 4.9·106 used /24 subnets and our campaigns simi-
ing to EdgeCast), confirming any IP in the /24 to be           larly capture 4.4 · 106 responsive subnets (90% coverage
equivalent for anycast detection purposes. Additionally,       with respect to [48]).
a /24 granularity implies that announced BGP prefixes
that are smaller than /24 are tested multiple times, one       3.2   Measurement dataset vs platform
per each /24 they contain: the mapping between /24             Dataset. One option to avoid running a large scale
and announced prefixes is still possible a posteriori, as      measurement campaign is to exploit readily available
we do in this work. This choice is reinforced by [35],         datasets from public measurement infrastructures – yet
which found 88% of announced prefixes to be /24, stated        we could not find any fitting our purpose. For instance,
that “anycast prefixes are dominated by /24” and sug-          despite probing all /24 every 2-3 days, Archipelago [6]
gested that larger prefixes may be anycast only in part        clusters its vantage points into three independent groups,
due to BGP prefix aggregation. We therefore fix the            each using random IPs selected in each /24 prefix: it
census granularity to a single target IP per /24.              follows that at most 3 monitors target each /24, with
                                                               generally different IP addresses, and a hit rate of about
Target liveness. As previously argued, any alive IP            6%. Given the low hit-rate and low-parallelism, such
belonging to a /24 is equivalent in telling whether the        dataset is not appropriate for our purpose, as it would
whole /24 is anycast (or unicast). To identify a respon-       not lead to a complete census, nor to an accurate geolo-
sive IP address in every /24-prefix, we rely on the hitlist    cation footprint even in case of hits.
periodically published by [31]. The hitlist consists in
generally one representative IP address for O(107 ) pre-       Platforms. There are a number of available measure-
fixes, along with a score indicative of the host liveliness,   ment platforms in the community, each with its own
computed over several measurement campaigns. When              advantages and limitations. Except for illustration pur-
no alive IP has been observed in a /24, the hitlist con-       poses, in this paper we relied on PlanetLab (PL). While
tains an arbitrary address from that /24 (score ≤−2).          RIPE Atlas (RIPE for short) is more interesting for ge-
After covering the full hitlist with the first census, we      ographical diversity due to its scale, it has a limited
confirm these hosts not being reachable and remove             control on the rate and type (cf. Sec. 3.4) of measure-
ments, as well as their instantiation for such a large                           OpenDNS                 Edgecast         Cloudflare     Microsoft
scale campaign (i.e., upload of the hitlist, probing bud-                                         L3                L4                  L7
get). Additionally, the larger number of vantage points                                 100




                                                                   Response ratio [%]
would mechanically increase about 20-fold the amount                                    80
of probes per census with respect to PL (in case all                                    60
VPs are used). Conversely, measurement in PL are lim-                                   40
ited by node availability (generally around 300 vantage                                 20
points), but offer full flexibility for deploying custom                                 0
software and run it at high speed (cf. Sec. 3.3).                                                 ICMP     TCP-53        TCP-80   DNS/UDP DNS/TCP
   While in this work we limitedly use PL, we depict
for illustration purposes an application of our technique    Figure 6: Response rates seen by heterogeneous
from measurements collected from PlanetLab vs RIPE           protocols across different targets.
in Fig. 5: as PL results are a subset of RIPE results,
white markers indicate replicas found from both plat-
forms, while black markers pinpoint replicas that are                                          CloudFlare                   EdgeCast




                                                                                                                                                     Median error [Km]
                                                             GT/PAI and TPR
only found with RIPE measurements. While this ex-                                             1                                               1000
ample has anecdotal relevance, it suggests that an in-                                  0.75                                                  750
triguing direction is to combine both platforms, e.g., by
                                                                                         0.5                                                  500
refining via RIPE the geolocation of anycast /24 de-
tected via PL.                                                                          0.25                                                  250
                                                                                              0                                               0
                                                                                                   GT/PAI            TPR          Error[Km]
3.3    Measurement software
Fastping. An efficient measurement tool is needed to
maximize the probing capacity of our VPs. While at           Figure 7: Validation with CloudFlare and Edge-
first sight Zmap [22] could seem the perfect tool for        Cast ASes. Bars represent standard deviation
such large-scale campaign, it however exhibits a major       among IP/24 of the AS.
blocking point in our setup: namely, Zmap generates
raw Ethernet frames, which are very efficient in a local
setup, but are not supported by the PlanetLab virtu-         maining in reason of communications administratively
alization layer. We therefore resort to Fastping [26], a     prohibited at network or host levels (respectively 1.3%,
tool specialized, as the name implies, in ICMP scan-         code 10 [14] and 0.2%, code 9 [14]).
ning which is deployed on each PL node. Fastping is
able to send about O(104 ) probes per second – about
two orders of magnitude slower than Zmap, but faster
than the fastest nmap scripting engine scanner. As we        3.4                          Network protocol
will point out later concerning scalability (Sec. 3.5), in   Recall. ICMP has often been used (and misused) in
order to gather complete censuses in few hours, we had       measurement studies: especially given recent work show-
to undergo several rounds of re-engineering – including      ing that ICMP latency measurements are often not re-
purposely slowing down Fastping sending-rate.                liable [40], we thus need to confirm the validity of our
                                                             protocol selection. A major motivation for ICMP mea-
Greylist. Additionally, Fastping adopts the usual tech-      surement is given by the high recall it offers [48]. Con-
niques to be a good Internet measurement citizen – i.e.,     sider indeed that TCP and UDP measurements would
a signature in the payload points to its homepage, Fast-     need an a priori knowledge (or guess) of services run-
ping probes the target list in a randomized order to         ning on the target under test. We therefore perform a
reduce intrusiveness, and implements a greylist mecha-       test on a reduced set of targets, performing 100 mea-
nism to honor requests to stop probing administratively      surements with different protocols: specifically, we con-
prohibited hosts/networks inferred from ICMP return          sider network L3 (ICMP) and transport L4 (TCP SYN-
codes. Before running a census from O(102 ) VP we ini-       SYN/ACK pair in the three-way handshake to port
tially run a census from a single VP in order to build       53 or 80) measurements, as well as L7 (DNS/UDP vs
an initial blacklist. During any census, we then collect     DNS/TCP using dig) measurements. Fig. 6 shows that
addresses generating ICMP return codes (other than           protocols other than ICMP have a binary recall: in
echo reply) in a temporary greylist, that we later in-       other words, they work well only if the service is known
crementally merge with the the blacklist. This list has      a priori. Conversely, ICMP is the only reliable alterna-
approximately O(105 ) hosts, with 98.5% added due to         tive, yielding high recall across all deployments, and is
administrative filtering [8] (type 3 code 13) and the re-    thus well suited for censuses.
Accuracy. While our technique relies on latency mea-              Table 1: Textual (0) vs binary (1-4) censuses
                                                                    Census ID   Format    Size (host,total)   Analysis
surements, it leverages the discriminative power of side
                                                                    0           csv       (270M, 79G)         >3 days
channel information (i.e., cities population within disks),         1-4         binary    (21M, 6G)           3 hr
to cope with latency measurement noise. While we vali-
date the accuracy of the methodology for DNS in [17], a               1

validation for stateful TCP connections is still missing.            0.8

To do so, we build a ground truth (GT) for CloudFlare                0.6




                                                              CDF
and EdgeCast by performing HTTP measurements with                    0.4
                                                                     0.2
curl from PL: note that HTTP measurements are not
                                                                      0
available from RIPE, highlighting once more the com-                       1       2         4          8         16
plementarity of these platforms.                                                Completion time per VP [Hr]
   By inspection of the HTTP headers, we find that
CloudFlare (EdgeCast) encode geolocation of the replica       Figure 8: CDF of per-vantage point completion
in the custom CF-RAY: (standard Server:) header field.        time, over all censuses
Notice that the measured GT constitutes the upper-
bound of what can be possibly achieved from PL mea-
                                                              via a Linear Feedback Shift Register (LFSR) with Ga-
surements, while the publicly available information (PAI)
                                                              lois configuration. Still, while the LFSR solves rate lim-
displayed on the CloudFlare and EdgeCast websites con-
                                                              iting at the target, it does not solve problems at the
tains a super-set of locations with respect to those mea-
                                                              source (or in the network): indeed, while requests are
sured from PL. We contrast true positive (TPR) clas-
                                                              well spread, replies do aggregate close to the VP, that
sification of our census vs HTTP GT in Fig. 7: in 77%
                                                              receives an aggregate rate equal to the probing rate of
of the IP/24 for CloudFlare (65% for EdgeCast) there
                                                              Fastping (in excess of 10,000 hosts per second). In our
is agreement at city level, with a median error of 434
                                                              preliminary (and incomplete) censuses, we noted het-
Km (287 Km for EdgeCast) in the (relatively few) mis-
                                                              erogeneous (and possibly very high) drop rates for some
classification cases. As expected, the low number of PL
                                                              VPs (likely tied to rate limiting spatially close to the
nodes possibly limits the portion of discoverable repli-
                                                              VP). Given that the networks where PL machines are
cas (GT/PAI is fairly high for CloufFlare, but fairly low
                                                              hosted are independently administered, we opted for a
for EdgeCast), making our footprint estimates conser-
                                                              simple solution and slowed down Fastping by one order
vative and confirming the interest for alternative plat-
                                                              of magnitude1 , that we verified empirically not trigger-
forms such as RIPE.
                                                              ing the above problems. Consequently, probing 6.6 · 106
                                                              targets at 103 targets per second takes less than two
Consistency. Additionally, in the case of openDNS,
                                                              hours: as shown in Fig.8 about 40% of PL nodes com-
we verify consistency across multiple RTT latency mea-
                                                              plete within this timeframe, and 95% in under 5 hours
surement techniques used early in Fig. 6. In this case we
                                                              (longer duration likely due to load on the PL host).
rely on public information that maps 24 locations [39].
For all protocols, applying [17] on the dataset yields
                                                              Output size and analysis duration. A second scal-
between 15 and 17 instances. Notice that all cities re-
                                                              ability issue concerns the output format. We initially
turned by the analysis are correct except Philadelphia
                                                              overlooked this issue and logged, in textual format, a
(while the server is located in Ashburn at 260km or
                                                              wealth of information amounting to 270M per node and
2.6ms worth of propagation delay away): this misclas-
                                                              80GB overall per census (cf. Tab.1). We therefore opted
sification is due to the bias enforced in [17] toward city
                                                              for a radical reduction of the output size, dumping a
population (Philadelphia is 33 times more populated
                                                              stripped-down binary format containing a timestamp,
than Ashburn), but as observed in [15] this is not prob-
                                                              delay and ICMP flag (encoding greylist return codes 9,
lematic as the “physical” Ashburn location is actually
                                                              10, or 13 as a negative sign) for a total of about 20MB
serving the “logical” Philadelphia population.
                                                              per node and 6GB overall per census.
                                                                 A third challenge lies in the analysis of the data. For
3.5    Scalability                                            a single target, the running time of [17] is O(10−1 ) sec,
Probing rate. When designing census experiments,              which compares very favorably to the O(103 ) sec of the
we take care of avoiding obvious pitfalls. For instance,      brute force optimal solution: at the same time, pro-
while we target a single host per /24, nevertheless we        cessing a census would still take days (we indeed have
perform measurements from all PL nodes. It follows            1
                                                               While it is possible to more finely tune the probing
that each node must desynchronize to avoid hitting ICMP       rate per VP, however coverage may benefit from samples
rate limiting (or raising alert) at the destination. We do    coming from the slowest VP, especially if it resides in a
so by randomized permutation for target nodes, achieved       geographical area which is not well covered by PL.
stopped processing the complete Census-0 after 3 days                            IP/24    ASes    Cities   CC    Replicas
                                                               All                1,696    346     77      38     13,802
of CPU time, where textual format additionally led to          ≥ 5 Replicas        897     100     71      36     11,598
slow processing due to disk fragmentation). Moreover,          ∩ CAIDA-100          19      8      30      18      138
due to LFSR, the order of the target IPs in all files          ∩ Alexa-100k        242     15      45      29     4,038
is not the same, meaning that an on-the-fly sorting of
about 300 lists (one per VP) containing millions targets
is needed. We therefore optimized our implementation,
which currently runs in under three hours, i.e., about
the same timescale of the census duration, so that in
principle we could perform a continuous analysis. While
this is not interesting for the anycast characterization
use-case, it may become relevant for other applications
of this technique (e.g. BGP hijacking inference men-
tioned in Sec. 5).

4. ANYCAST /0 CENSUSES
  This section presents results of the first Internet-wide    Figure 10: Anycast censuses results, at a glance.
anycast study. We start by aggregated statistics (Sec. 4.1)
and then incrementally refine the picture by providing
a bird’s-eye view of the most interesting deployments         ing IP-anycast: here again, we find 242 IP/24 of 15
(Sec. 4.2) over which we perform an additional portscan       ASes that are among the major players of the Web.
campaign to reveal their running services (Sec. 4.3).
4.1      At a glance                                          4.2    Top-100 Anycast ASes
Details about the of our censuses are reported in Fig. 10.       Albeit the amount of anycast IP/24 may seem de-
Overall, 1696 IP/24 belonging to 346 ASes appear to           ceiving at first in reason of its exiguous footprint, it is
have more than one anycast replica, while we were able        nevertheless very rich – revealing silver needles in the
to find only 897 IP/24 belonging to 100 ASes having           haystack. From the very coarse cross-check of CAIDA
at least 5 replicas with our technique. The plot also         and Alexa ranks, we already expect that anycast usage
shows a geographical density map of anycast replicas:         is not only restricted to DNS, but rather covers impor-
results of our censuses are available for browsing at [21],   tant ISPs and OTTs. Fig. 9 presents a bird’s-eye view
offering per-deployment (as in Fig. 5) or aggregated (as      of anycast adoption, depicting several information for
in Fig. 10) visualizations. Notice that results reported      the 100 ASes for which we detected at least 5 replicas,
in this paper correspond to censuses performed during         identified by their WHOIS name reported in the x-axis
March 2015: with later censuses, we observed small but        (capped to 12 characters). Geographical and IP/24 foot-
interesting changes in the anycast landscape. While we        print are reported in the bottom: ASes are arranged left
plan to run a continuous service, please be advised that      to right, in decreasing number of replicas (bottom bar-
(at time of writing) results at [21] refer to the censuses    plot, with standard deviation across IP/24 belonging
described in this paper.                                      to the same AS), additionally reporting the number of
   Several remarks from Fig. 10 are in order. First, no-      anycast IP/24 for that AS (middle bar-plot). Service
tice that our results are conservative since (i) in regions   footprint is correlated to the open TCP ports in the AS
with low presence of PlanetLab VPs, we may miss some          (middle scatter-plot). Next, the relative importance of
anycast replicas, e.g., when the BGP prefix is only lo-       the AS in the Internet and for the Web are expressed
cally advertised; (ii) the analysis technique provides a      in terms of the CAIDA and Alexa ranks respectively
lower bound on the number of replicas, since overlap-         (top scatter-plots). Finally, a label reported on the top
ping disks may correspond to different anycast replicas       x-axis categorize the main activity of the ASes from a
but they will not be considered in the solution of the        business perspective (category is informal and in case of
MIS problem (recall Fig. 3). Second, we investigate the       ASes with multiple services, only the most prominent is
CAIDA AS rank list, to cross check how many ASes us-          selected).
ing IP-anycast figure in the top-100: results tabulated
in Fig. 10, show that 19 IP/24 of 8 ASes that play a          Big fishes. Major players of the Internet ecosystem
central role in the Internet belong to the list. Similarly,   are easy to spot in Fig. 9. The list includes not only
we investigate the Alexa rank, to cross check how many        tier-1 and other ISPs (such as AT&T Services, Tinet,
webpages in the top-100k rank are hosted2 by ASes us-
                                                              of the frontpage found in Alexa to an IP, and disregard
2
    For the sake of simplicity, we resolve the domain name    content that is referenced in the frontpage.
                                                                                                                                                                                                                                       #Replicas           #IPs/24 Open ports Alexa rank Caida rank




                                                                                                                                                                                                                                       0
                                                                                                                                                                                                                                           10
                                                                                                                                                                                                                                                20
                                                                                                                                                                                                                                                           1
                                                                                                                                                                                                                                                               10
                                                                                                                                                                                                                                                                    100
                                                                                                                                                                                                                                                                                 53
                                                                                                                                                                                                                                                                                 80
                                                                                                                                                                                                                                                                                443
                                                                                                                                                                                                                                                                                      8080
                                                                                                                                                                                                                                                                                                   100
                                                                                                                                                                                                                                                                                                         1k
                                                                                                                                                                                                                                                                                                              10k
                                                                                                                                                                                                                                                                                                                    100k
                                                                                                                                                                                                                                                                                                                                1
                                                                                                                                                                                                                                                                                                                               10
                                                                                                                                                                                                                                                                                                                              100
                                                                                                                                                                                                                                                                                                                               1k
                                                                                                                                                                                                                                                                                                                              10k
                                                                                                                                                                                                                                                                                                                             100k
                                                                                                                                                                                                                         1 CLOUDFLARENET               1                    1                  1                             1      CDN
                                                                                                                                                                                                                         2 ISC-AS,US                   2                    2                  2                             2      DNS
                                                                                                                                                                                                                         3 HURRICANE,US                3                    3                  3                             3      ISP
                                                                                                                                                                                                                         4 CDNETWORKSUS-               4                    4                  4                             4      CDN
                                                                                                                                                                                                                         5 FACEBOOK,US                 5                    5                  5                             5      Social Network
                                                                                                                                                                                                                         6 COMMUNITYDNS,               6                    6                  6                             6      DNS
                                                                                                                                                                                                                         7 XGTLD,US                    7                    7                  7                             7      DNS
                                                                                                                                                                                                                         8 L-ROOT,US                   8                    8                  8                             8      DNS
                                                                                                                                                                                                                         9 MICROSOFT,US                9                    9                  9                             9      Cloud
                                                                                                                                                                                                                         10 I-ROOT,SE                 10                   10                 10                            10      DNS
                                                                                                                                                                                                                         11 VERISIGN-INC              11                   11                 11                            11      DNS
                                                                                                                                                                                                                         12 LLNW,US                   12                   12                 12                            12      CDN
                                                                                                                                                                                                                         13 ARYAKA-ARIN,              13                   13                 13                            13      Cloud
                                                                                                                                                                                                                         14 APPLE-ENGINE              14                   14                 14                            14      CDN
                                                                                                                                                                                                                         15 CEDEXIS,US                15                   15                 15                            15      Security
                                                                                                                                                                                                                         16 HIGHWINDS3,U              16                   16                 16                            16      CDN
                                                                                                                                                                                                                         17 NETNOD-IX,SE              17                   17                 17                            17      DNS
                                                                                                                                                                                                                         18 OPENDNS,US                18                   18                 18                            18      Security/DNS
                                                                                                                                                                                                                         19 WOODYNET-1,U              19                   19                 19                            19      DNS
                                                                                                                                                                                                                         20 LGTLD,US                  20                   20                 20                            20      DNS
                                                                                                                                                                                                                         21 LIECHTENSTEI              21                   21                 21                            21      unknown
                                                                                                                                                                                                                         22 FASTLY,US                 22                   22                 22                            22      CDN
                                                                                                                                                                                                                         23 CACHENETWORK              23                   23                 23                            23      CDN
                                                                                                                                                                                                                         24 INSTART,US                24                   24                 24                            24      CDN
                                                                                                                                                                                                                         25 DNSCAST-AS,U              25                   25                 25                            25      DNS
                                                                                                                                                                                                                         26 GOOGLE,US                 26                   26                 26                            26      Cloud/DNS
                                                                                                                                                                                                                         27 EDGECAST-IR,              27                   27                 27                            27      CDN
                                                                                                                                                                                                                         28 UMDNET,US                 28                   28                 28                            28      unknown
                                                                                                                                                                                                                         29 DYNDNS,US                 29                   29                 29                            29      DNS
                                                                                                                                                                                                                         30 NSONE,US                  30                   30                 30                            30      DNS
                                                                                                                                                                                                                         31 EASYLINK4,US              31                   31                 31                            31      Cloud messaging
                                                                                                                                                                                                                         32 YAHOO-AN2,US              32                   32                 32                            32      Web Portal
                                                                                                                                                                                                                         33 ULTRADNS,US               33                   33                 33                            33      DNS
                                                                                                                                                                                                                         34 OVH,FR                    34                   34                 34                            34




DNS, OpenDNS) also emerge in the census.
                                                                                                                                                                                                                                                                                                                                    Cloud
                                                                                                                                                                                                                         35 LIECHTENSTEI              35                   35                 35                            35      unknown
                                                                                                                                                                                                                         36 AS-AFILIAS1,              36                   36                 36                            36      DNS
                                                                                                                                                                                                                         37 AUTOMATTIC,U              37                   37                 37                            37      Blogging
                                                                                                                                                                                                                         38 TINET-BACKBO              38                   38                 38                            38      ISP-tier1
                                                                                                                                                                                                                         39 ABOVENET-CUS              39                   39                 39                            39      ISP
                                                                                                                                                                                                                         40 AMAZON-02,US              40                   40                 40                            40      Cloud
                                                                                                                                                                                                                         41 CW,GB                     41                   41                 41                            41      ISP
                                                                                                                                                                                                                         42 LEVEL3,US                 42                   42                 42                            42      ISP-tier1
                                                                                                                                                                                                                         43 EDGECAST,US               43                   43                 43                            43      CDN
                                                                                                                                                                                                                         44 TWITTER-NETW              44                   44                 44                            44      Social Network




messaging (EASYLINK2 owned by AT&T Services),




Fig. 11, crisply showing that DNS now represents about
Diversity. We report a breakdown of AS classes in
CommunityDNS), DNS service management (e.g., Ul-
as root and top-level domain servers (e.g., ISC/F-root,
tems). Of course, DNS-related service providers such
Amazon Web Services), social networks (e.g., Twitter,
Sprint, TATA Communications, Qwest, Level 3, Hur-




one third of IP anycast activities. Plots in Fig. 9 clearly
and web analytics (OMNITURE owned by Adobe Sys-
nic.at), virtual roaming and virtual meeting services
ers (e.g., Apple, RIM), Web registrars (e.g., Verisign,
lexic, OpenDNS). The list also includes manufactur-
Facebook, LinkedIn), and security companies that pro-
ricane Electrics), but also a rather large spectrum of

ing (e.g., OVH) and cloud providers (e.g., Microsoft,
OTTs such as CDNs (e.g., CloudFlare, EdgeCast), host-



vide mitigation services against DDoS attacks (e.g., Pro-
                                                                                                                                                                                                                         45 INCAPSULA,US              45                   45                 45                            45




tic, a publishing company hosting wordPress.com), cloud
                                                                                                                                                                                                                                                                                                                                    CDN




(Media Network Services), blogging platforms (Automat-
                                                                                                                                                                                                                         46 AGTLD,US                  46                   46                 46                            46      DNS




traDNS, DynDNS), and public DNS resolvers (e.g., Google
                                                                                                                                                                                                                         47 AUSREGISTRY-              47                   47                 47                            47      DNS
                                                                                                                                                                                                                         48 CENTRALNIC-A              48                   48                 48                            48      DNS
                                                                                                                                                                                                                         49 COGENT-2149,              49                   49                 49                            49      ISP
                                                                                                                                                                                                                         50 HGTLD,US                  50                   50                 50                            50      DNS
                                                                                                                                                                                                                         51 HIGHWINDS4,U              51                   51                 51                            51      CDN
                                                                                                                                                                                                                         52 K-ROOT-SERVE              52                   52                 52                            52      DNS
                                                                                                                                                                                                                         53 NETRIPLEX01,              53                   53                 53                            53      DNS
                                                                                                                                                                                                                         54 OMNITURE,US               54                   54                 54                            54      Online Marketing
                                                                                                                                                                                                                         55 SOFTLAYER,US              55                   55                 55                            55      Cloud
                                                                                                                                                                                                                         56 WANGSU-US,US              56                   56                 56                            56      CDN
                                                                                                                                                                                                                         57 YAHOO-FC,US               57                   57                 57                            57      Web Portal
                                                                                                                                                                                                                         58 BITGRAVITY,U              58                   58                 58                            58      CDN
                                                                                                                                                                                                                         59 ABILENE,US                59                   59                 59                            59      Backbone Network
                                                                                                                                                                                                                         60 ADVAN-CAST,U              60                   60                 60                            60      unknown
                                                                                                                                                                                                                         61 ASATTLDSE                 61                   61                 61                            61      DNS
                                                                                                                                                                                                                         62 AS-QUADRANET              62                   62                 62                            62      Cloud
                                                                                                                                                                                                                         63 AS6453,US                 63                   63                 63                            63      ISP-tier1
                                                                                                                                                                                                                         64 ATT,EU                    64                   64                 64                            64      ISP
                                                                                                                                                                                                                         65 CENTRALNIC-A              65                   65                 65                            65      DNS
                                                                                                                                                                                                                         66 CENTURYLINK-              66                   66                 66                            66      ISP-tier1
                                                                                                                                                                                                                         67 CONEXIM-AS-A              67                   67                 67                            67      Cloud
                                                                                                                                                                                                                         68 EGTLD,US                  68                   68                 68                            68      DNS
                                                                                                                                                                                                                         69 KGTLD,US                  69                   69                 69                            69      DNS
                                                                                                                                                                                                                         70 MNS-AS,NO                 70                   70                 70                            70      Video Conferencing
                                                                                                                                                                                                                         71 NICAT,AT                  71                   71                 71                            71      DNS
                                                                                                                                                                                                                         72 VITAL-DNS,US              72                   72                 72                            72      DNS
                                                                                                                                                                                                                         73 WHS-ANYCAST-              73                   73                 73                            73      Security
                                                                                                                                                                                                                         74 ZGTLD,US                  74                   74                 74                            74      DNS
                                                                                                                                                                                                                         75 INTERNAP-BLK              75                   75                 75                            75      Cloud
                                                                                                                                                                                                                         76 NETAPP-ANYCA              76                   76                 76                            76      Web Analytics
                                                                                                                                                                                                                         77 SPRINTLINK,U              77                   77                 77                            77      ISP-tier1
                                                                                                                                                                                                                         78 AUSREGISTRY-              78                   78                 78                            78      DNS
                                                                                                                                                                                                                         79 CENTURYLINK-              79                   79                 79                            79      ISP
                                                                                                                                                                                                                         80 DNSIMPLE,US               80                   80                 80                            80      DNS
                                                                                                                                                                                                                         81 DYN-HC,US                 81                   81                 81                            81      DNS
                                                                                                                                                                                                                         82 EASYLINK2,US              82                   82                 82                            82      Cloud messaging
                                                                                                                                                                                                                         83 EDNS,CA                   83                   83                 83                            83      DNS
                                                                                                                                                                                                                         84 ESGOB-ANYCAS              84                   84                 84                            84      DNS
                                                                                                                                                                                                                         85 HOMEPL-AS,PL              85                   85                 85                            85      Cloud
                                                                                                                                                                                                                         86 LINKEDIN,US               86                   86                 86                            86      Social Network
                                                                                                                                                                                                                         87 MASERGY,US                87                   87                 87                            87      Cloud
                                                                                                                                                                                                                         88 MEDIAMATH-IN              88                   88                 88                            88      AD technology
                                                                                                                                                                                                                         89 MII-2,GB                  89                   89                 89                            89      CDN
                                                                                                                                                                                                                         90 MII-XPC,US                90                   90                 90                            90      CDN
                                                                                                                                                                                                                         91 PEER1,US                  91                   91                 91                            91      Cloud
                                                                                                                                                                                                                         92 PHH-AS,DE                 92                   92                 92                            92      CDN
                                                                                                                                                                                                                         93 PRETECS,CA                93                   93                 93                            93      CDN
                                                                                                                                                                                                                         94 PROLEXIC,US               94                   94                 94                            94      Security
                                                                                                                                                                                                                         95 QUANTCAST,US              95                   95                 95                            95      Web Analytics
                                                                                                                                                                                                                         96 RIMBLACKBERR              96                   96                 96                            96      Telecom Vendor
                                                                                                                                                                                                                         97 SUPERNETWORK              97                   97                 97                            97      Cloud
                                                                                                                                                                                                                         98 UNOVA-1,CA                98                   98                 98                            98      DNS
                                                                                                                                                                                                                         99 VOXILITY,RO               99                   99                 99                            99
                                                                                                                        Figure 9: Bird’s eye view of Top-100 anycast ASes (ranked according to geographical footprint)




                                                                                                                                                                                                                                                                                                                                    Cloud
                                                                                                                                                                                                                         100 ZVONKOVA-AS             100                  100                100                           100      unknown




                                                           with CloudFlare using 4× more ports than EdgeCast).




smaller with respect to L7-anycast deployments that
mean number of geographical replicas per AS (bottom
Geographical footprint. We specifically study the
                                                           port for DNS to O(104 ) open ports for OVH) but also




Notice that these orders of magnitude are, significantly
                                                           and 443 over the set of 22 open ports they are using,
                                                           and EdgeCast CDNs have in common only port 53, 80
                                                           between deployments of the same kind (e.g., CloudFlare
                                                           model, (e.g., we observe from a minimum of 1 open
                                                           across deployments having an heterogeneous business
                                                           metrics. Indeed, no correlation appear between any two




have at least 10 replicas distributed around the globe.
our measurement. Overall, we observe that 25 ASes
                                                           open ports, and the specific port values, vary not only
                                                           lation coefficient of 0.35). Additionally, the number of
                                                           IP/24 footprints are largely unrelated (Pearson corre-
                                                           ployments: for instance, the geographical footprint and
                                                           metrics, illustrating the degree of freedom in anycast de-
                                                           illustrate the large diversity of anycast usage, under all




plot in Fig. 9) championed by the CDN CloudFlare in
                                                                          CDF of number of IPs/24
AS breakdown [%]   35                                                                                 1
                   30                                                                               0.9
                                                                                                    0.8
                   25
                                                                                                    0.7
                   20                                                                               0.6
                   15                                                                               0.5
                   10                                                                               0.4                   (27/02/15) Census 1-261VPs
                    5                                                                               0.3                   (02/03/15) Census 2-255VPs
                                                                                                    0.2                   (04/03/15) Census 3-269VPs
                    0                                                                                                     (13/03/15) Census 4-240VPs
                                                                                                    0.1               Combination of censuses-308VPs
                        DNS         Cloud      Unknown     Social                                     0
                              CDN           ISP     Security     Other                                    2       5            10       15          20        25
                                                                                                                              Number of replicas


Figure 11: Breakdown of AS category (only first
category is considered).                                                 Figure 12: CDF of geographically distinct repli-
                                                                         cas per IP/24 (individual censuses and overall)

                                                                                                      1




                                                                           CDF of number of ASes
can exceed O(103 ) for the large providers, which is in                                                        APPLE,US (6)
                                                                                                    0.9                                  CLOUDFLARENET,US (328)
part due to the low number of vantage points in Plan-                                               0.8                          EDGECAST,US (37)
etLab (see Sec.3.2). Among those ASes, we observe                                                   0.7                                       GOOGLE,US (102)
                                                                                                                           PROLEXIC,US (21)
10 DNS service providers (including ISC, DNScast, and                                               0.6
                                                                                                    0.5                 TWITTER,US (3)
DynDNS) and 7 major CDNs (e.g., CloudeFlare, Lime-
                                                                                                    0.4
light, Highwinds, Fastly, CacheNetworks, Instart Logic,                                             0.3           LEVEL3,US (2)
CDNetworks). We also discover two cloud providers                                                   0.2       LINKEDIN,US (1)
(e.g., Microsoft and Aryaka Networks), one tier-1 ISP                                               0.1                                  >= 5 Replicas
                                                                                                      0
(Hurricane Electric which has 15% of ASes in its cus-                                                     1                    10            100             1000
tomer cone according to CAIDA), a security company                                                                             Number of IPs/24
(OpenDNS, also popular for its public DNS service), a
social network (Facebook) and a manufacturer (Apple).
   Fig. 12 further reports the cumulative number of repli-                                            Figure 13: Number of IPs/24 per AS
cas per IP/24, depicting both results coming from the
combination of censuses, as well as individual result
from each census alone. Specifically, the MIS solver                     IP/24 footprint. In terms of the number of anycast
orders circles by increasing radius size: intuitively, the               IPs/24 per AS (middle plot in Fig. 9), we find that
smaller the latency, the lower the number of overlaps,                   the CDN CloudFlare is by far the largest in terms of
the better the recall of our method. This is confirmed                   IP address ranges. Overall, we find 10 ASes that have
in Fig. 12, where censuses are combined by computing                     at least 10 anycast IPs/24: 3 are CDNs (CloudFlare,
the minimum among multiple latency measurements                          EdgeCast, BitGravity), 3 are DNS providers (DNScast,
between the same VP and target pair, to get an es-                       WoodyNet, UltraDNS), and the remaining ASes rep-
timate of the RTT latency that is as close as possible                   resent multiple services (Automattic, Google, Amazon
to the propagation delay. Additionally, combining mea-                   Web Services, and Prolexic). The distribution of the
surement increases recall: about 200 more IP/24 are                      number of IPs/24 per AS depicted in Fig. 13 shows that
found to be anycast in the combination with respect to                   about half have exactly one IP/24 (e.g., LinkedIn and
the average individual census.                                           AT&T Services). Yet, about 10% of the ASes employ
   In this paper, we limitedly consider results from the                 at least 10 subnets: for instance Prolexic, EdgeCast,
combination, but remark that results are quite con-                      Google, and CloudFlare employ 21, 37, 102, and 328
sistent across censuses (notice that curves overlap in                   anycast IP/24 respectively.
Fig. 12). A last comment is worth making about de-                          While in this work we do not provide a systematic
ployments where we observe only 2 geographically dis-                    investigation of the deployment density (i.e., how many
tributed replicas – which is possibly due to the low den-                IP/32 are alive in each IP/24), from the above discus-
sity of our VPs, but could also be tied to the wrong                     sion about diversity is not surprising that we were able
geolocation of some VP raising false positive replicas.                  to identify both very sparse (e.g., Google 8.8.8.8 is the
While we have anecdotal evidence of some of these ex-                    only address alive in the 8.8.8.0/24) and very dense de-
iguous deployments being anycast, we prefer to defer a                   ployments (e.g., well over 99% of IPs are alive in most
more detailed analysis for future work (see Sec. 5).                     CloudFlare subnets).
Importance. The presence of ASes ranking among                                                    nmap portscan statistics
                                                                            IPs/32             ASes  Ports (SSL)     Well                                                                Software
the top-100 in the CAIDA list, as well as CDNs serving                                                              known
content in the top-100k Alexa list are good indicators                               812        81    10,499 (185)    457                                                                       30
that anycast is used for popular and important services.




                                                                   AS frequency
Considering CDNs that are, after DNS, the most popu-




                                                                                                                                 tcpwrapped




                                                                                                                                                               tcpwrapped

                                                                                                                                                                            tcpwrapped
                                                                                     60




                                                                                                                                                                                                movaz-ssc
lar anycast service according to Fig. 11, we observe that                            40




                                                                                                                      http-ssl
                                                                                              domain
8 CDNs serve Alexa-100k websites: this set includes




                                                                                                         http




                                                                                                                                                       http
                                                                                     20




                                                                                                                                               ssh




                                                                                                                                                                                         sip
CloudFlare, EdgeCast, and Fastly with 188, 10, and                                    0




                                                                                              53

                                                                                                         80

                                                                                                                      443

                                                                                                                                 179

                                                                                                                                               22

                                                                                                                                                       8080

                                                                                                                                                               8083

                                                                                                                                                                            3306

                                                                                                                                                                                         1935

                                                                                                                                                                                                5252
5 websites respectively (in addition, Highwinds, Cach-
eNetworks, Instart, Incapsula, and BitGravity host one




                                                                   IP/24 frequency
popular site each). In addition, 11 of the websites listed
by Alexa are hosted by Google anycast IPs. Finally,                                  400




                                                                                                           http ssl




                                                                                                                                      domain
10 websites are hosted on IPs that belong to Prolexic                                200




                                                                                                  http




                                                                                                                          http




                                                                                                                                                http

                                                                                                                                                        http

                                                                                                                                                                 http

                                                                                                                                                                             http

                                                                                                                                                                                         http

                                                                                                                                                                                                http
(now part of Akamai), which operates a DDoS mitiga-                                       0
tion service that receives the traffic on behalf of its client




                                                                                                  80

                                                                                                           443

                                                                                                                          8080

                                                                                                                                     53

                                                                                                                                                2052

                                                                                                                                                        2053

                                                                                                                                                                 2082

                                                                                                                                                                             2083

                                                                                                                                                                                         8443

                                                                                                                                                                                                2087
networks, redirecting only legitimate traffic to them.

4.3    Anycast Services                                          Figure 14: Overall nmap portscan statistics and
Portscan campaign. In reason of the historical use of            Top-10 open TCP ports (per AS and per /24).
anycast for DNS services, we believe it to be important
to provide an up-to-date longitudinal view across ser-
vices offered via IP-anycast, especially focusing on TCP.        We make the following observations: (i) roughly half of
We provide a summary of the nmap probing in the top              the ASes have at least one open TCP port, (ii) about
of Fig. 14. We test all anycast /24 of the top-100 ASes:         10% of the ASes have at least 5 open TCP ports and
picking a single IP representative per /24 we scan, at           (iii) the largest service footprint is represented by Incap-
low rates, all 216 TCP ports. Our results are conser-            sula and especially OVH with 313 and 10148 open ports
vative in that different IPs in the same /24 may have            respectively. In the latter case, while we did not inves-
different open ports (which happens, e.g., for Cloud-            tigate thoroughly, we suspect the large number of ports
Flare and EdgeCast), and since an under-estimation of            being due to the fact that OVH, the largest hosting ser-
the number of open TCP ports can also be the result of           vice in Europe and the 3rd in the world, is significantly
probe filtering by firewalls and routers along the path          popular in the BitTorrent seedbox ecosystem [42]. Pre-
to the targets. Out of the 897 IP of the top-100 ASes,           dominant services (beyond DNS) include fairly popu-
we find that 816 of 81 ASes have at least one open TCP           lar HTTP and HTTPS, used by over 20% of the ASes.
port. The total number of distinct open TCP ports                Even excluding the OVH case, the list of interesting
across is 10485, providing 449 well-known services (i.e.,        services is large. In terms of business diversity, 22 ASes
as indicated by TCP port classification), 170 of which           have at least 4 different TCP ports open: 8 CDNs, 4
over SSL. Additionally, nmap fingerprinting discovers            DNS, 4 ISPs including a tier-1 ISP (Tinet SpA) and
30 different software implementations running on the             Google with 9 open TCP ports. Finally, interesting
anycast replicas, that we also detail next.                      (though unpopular) services worth listing include multi-
                                                                 media services (RTMP, Simplify Media, MythTV), and
Class imbalance. Given the heterogeneity of the IP/24            gaming (Minecraft).
footprint, we argue being necessary to consider only per-
AS statistics to avoid presenting results that are biased        Software diversity. Fig. 16 lists 30 different soft-
due to class imbalance. We illustrate the problem by             ware that we group into three main categories: Web,
depicting in Fig. 14 the frequency count of the top-10           Mail, and DNS. Interestingly, the list includes open
open TCP ports by number of ASes (top) and IPs/24                source software such as popular web and DNS daemons
(bottom). Notice that only port 80, 443 and 53 appear            (e.g., nginx, ISC BIND) and proprietary software (e.g.,
to be common to both top and bottom plots: especially,           ECAcc/ECS/ECD which are web servers developed by
all ports in the hatched area are due to the large pre-          EdgeCast). Starting with DNS software, notice that for
dominance of IP/24 owned by the CloudFlare AS, which             44 ASes using port 53 (out of 67), nmap could not iden-
also affect the order of common ports in the top-10. We          tify the software version running on the remote server.
thus focus on per AS statistics in the following.                Unsurprisingly, we find that ISC BIND is by far the
                                                                 most adopted protocol to handle DNS requests over
Stateful services. Fig. 15 presents the complemen-               anycast. Yet, we also detect the use by 3 ASes (Apple,
tary CDF of the number of open TCP ports per AS.                 K-ROOT, L-ROOT) of the NLnet Labs NSD implemen-
                                                                                            DNS                   Web            Mail            Other




                                                                       AS frequency
           1                                                                          20
                    EDGECAST,US (5)            ASes
                         GOOGLE,US (9)                                                10
   CCDF


                         CLOUDFLARENET,US (20)
          0.1                                                                         0




                                                                                                  ISC BIND
                                                                                           NLnet Labs NSD
                                                                                            Microsoft DNS
                                                                                                 OpenDNS

                                                                                                                         nginx
                                                                                                                      lighttpd
                                                                                                                Apache httpd
                                                                                                                          ECD
                                                                                                                 Microsoft IIS
                                                                                                                      Varnish
                                                                                                              Apache Tomcat
                                                                                                                     bitasicv2
                                                                                                                    CFS 0213
                                                                                                             cloudflare-nginx
                                                                                                                 cPanel httpd
                                                                                                                        thttpd
                                                                                                                  ECAcc/ECS
                                                                                                                Google httpd
                                                                                                                   instart/160
                                                                                                                                  Gmail imapd
                                                                                                                                  Gmail pop3d
                                                                                                                                 Google gsmtp

                                                                                                                                                     OpenSSH
                                                                                                                                                       MySQL
                                                                                                                                                       sslstrip

                                                                                                                                                Microsoft RPC
                                                                                                             Microsoft HTTP




                                                                                                                                                Microsoft SQL
                                         INCAPSULA,US (330)

                                                OVH,FR (10,148)

      0.01
                1    10    100      1000   10000              100000
                      Number of open TCP ports

                                                                       Figure 16: Breakdown of software running on
                                                                       anycast replicas.
Figure 15: Complementary CDF of the number
of open TCP ports per AS.
                                                                       IP-level CDN: Refining the active methodology by
                                                                       mapping content object (and not only frontpage) from
tation, which is specifically designed to add resilience               the Alexa-100k would be needed to gather a better un-
against software failures of DNS root servers.                         derstanding of IP-level CDN.
   Among web servers, the most popular are nginx (7                    Longitudinal view: Taking periodic censuses and an-
ASes), Apache httpd and lighttpd (ex æquo with 4                       alyzing the time evolution over longer timescales would
ASes). We observe the use of proprietary web servers                   allow to track evolution of IP anycast deployments.
by some CDNs (e.g., cloudflare-nginx and Panel httpd).                 Traffic volume: A missing information concerns the
Though our dataset has a limited size, we attempt a                    traffic volume served by IP anycast, that can be gath-
comparison with the relative popularity of webservers                  ered via passive measurement, and annotated with re-
in the unicast world: the Spearman correlation of popu-                sults of our census (i.e., binary flag per anycast IP/24).
larity rank in our dataset with webserver ranks [2] in the             Combine measurement platforms: As we have seen,
Alexa-10M is low (0.38). As for the DNS case, difference               it would be interesting to exploit multiple platforms in
may arise in some peculiar features that are especially                addition to PlanetLab, such as RIPE Atlas: this would
valuable in the anycast context. Finally, we detect the                both lead to a better characterization of large deploy-
presence of running daemons that serve mail on anycast                 ments (e.g., increase the recall), as well as possibly assist
IPs from Google (Gmail imapd, Gmail pop3d, gsmtp)                      in confirming/discarding suspicious deployments (i.e.,
as well as of RPC (ssh, MicrosoftRPC) and databases                    those for which we detected 2 replicas from PL).
(MySQL/Microsoft SQL).                                                 BGP hijacking: Detecting geo-inconsistencies for know-
                                                                       ingly unicast prefixes is symptomatic of BGP hijack-
5. DISCUSSION                                                          ing attacks: being able to periodically and quickly scan
                                                                       the network to raise alarms and cross-check them with
   We present the first census(es) of IPv4 anycast de-
                                                                       other types of data (e.g., BGP feeds, traceroute mea-
ployment, gathered through an original and robust tech-
                                                                       surements) is a relevant extension of this work.
nique implemented with an efficient and scalable system
design. In spirit with the open source and data move-
ment, results of our census are available at [21].                     Acknowledgements
   Our characterization show that a tiny fraction of the               We thank our shepherd, Matteo Varvello, and the anony-
IPv4 space is anycasted, yet among the anycasters we                   mous CoNEXT reviewers for their valuable feedback.
recognize major players of the Internet ecosystem in-                  This work has been carried out at LINCS (http://www.
cluding top-ranking ISPs, popular Cloud, OTT and es-                   lincs.fr). The research leading to these results was sup-
pecially CDN operators. We additionally show great                     ported by the European Union under the FP7 Grant
heterogeneity along multiple directions, and especially                Agreement n. 318627 (Integrated Project ”mPlane”)
in terms of the offered services. Particularly, our portscan           and by a Google Faculty Research Award.
campaign of anycasted subnets reveals over 450 well-
known services from over 10, 000 unique open ports.                    6. REFERENCES
Additionally, we uncover 30 software implementations,                   [1] http://internetcensus2012.bitbucket.org/paper.html.
with a relative breakdown that differs from software                    [2] http://w3techs.com/technologies/overview/web server/all.
ranking in the unicast IP world.                                        [3] J. Abley. A software approach to distributing requests
   Yet, this work only scratches the surface, and opens                     for DNS service using GNU Zebra, ISC BIND 9
more questions than it is able to answer, as for instance:                  FreeBSD. In Proc. USENIX ATEC, 2004.
 [4] J. Abley and K. Lindqvist. Operation of Anycast            [28] B. Gueye, A. Ziviani, M. Crovella, and S. Fdida.
     Services. RFC 4786 (Best Current Practice), 2006.               Constraint-based geolocation of internet hosts. In
 [5] V. K. Adhikari, S. Jain, and Z. li Zhang. Youtube               ACM IMC, 2004.
     traffic dynamics and its interplay with a tier-1 isp: An   [29] T. Hardie. Distributing Authoritative Name Servers
     isp perspective. In ACM IMC, 2010.                              via Shared Unicast Addresses. IETF RFC 3258, 2002.
 [6] http://www.caida.org/projects/ark/.                        [30] J. Heidemann, Y. Pradkin, R. Govindan,
 [7] http://www.root-servers.org.                                    C. Papadopoulos, G. Bartlett, and J. Bannister.
 [8] F. Baker. Requirements for IP Version 4 Routers.                Census and survey of the visible internet. In ACM
     IETF RFC 1812, 1995.                                            IMC, 2008.
 [9] H. Ballani and P. Francis. Towards a global IP anycast     [31] Internet addresses hitlist dataset (20140829/rev4338).
     service. In Proc. ACM SIGCOMM, 2005.                            Provided by the USC/LANDER project
[10] H. Ballani, P. Francis, and S. Ratnasamy. A                     (http://www.isi.edu/ant/lander).
     measurement-based deployment proposal for IP               [32] D. Karrenberg. Anycast and BGP stability: A closer
     anycast. In ACM IMC, 2006.                                      look at DNSMON data. Nanog, 2005.
[11] B. Barber, M. Larson, and M. Kosters. Traffic source       [33] T. Krenc, O. Hohlfeld, and A. Feldmann. An internet
     analysis of the J root anycast instances. Nanog, 2006.          census taken by an illegal botnet: A qualitative
[12] I. Bermudez, S. Traverso, M. Mellia, and M. Munafo.             assessment of published measurements. ACM CCR,
     Exploring the cloud from passive measurements: The              44(3), 2014.
     Amazon AWS case. In Proc. IEEE INFOCOM, 2013.              [34] Z. Liu, B. Huffaker, M. Fomenkov, N. Brownlee, and
[13] P. Boothe and R. Bush. DNS Anycast Stability: Some              K. C. Claffy. Two days in the life of the DNS anycast
     Early Results. CAIDA, 2005.                                     root servers. In PAM, 2007.
[14] R. Braden. Requirements for Internet Hosts -               [35] D. Madory, C. Cook, and K. Miao. Who are the
     Communication Layers. IETF RFC 1122, 1989.                      anycasters. Nanog, 2013.
[15] M. Calder, X. Fan, Z. Hu, E. Katz-Bassett,                 [36] B. M. Maggs and R. K. Sitaraman. Algorithmic
     J. Heidemann, and R. Govindan. Mapping the                      nuggets in content delivery. SIGCOMM Comput.
     expansion of google’s serving infrastructure. In ACM            Commun. Rev., 45(3), Jul 2015.
     IMC, 2013.                                                 [37] K. Miller. Deploying IP anycast. Nanog, 2003.
[16] M. Calder, A. Flavel, E. Katz-Bassett, R. Mahajan,         [38] https://nmap.org.
     and J. Padhye. Analyzing the performance of an             [39] https://www.opendns.com/data-center-locations.
     anycast cdn. In ACM IMC, 2015.                             [40] C. Pelsser, L. Cittadini, S. Vissicchio, and R. Bush.
[17] D. Cicalese, D. Joumblatt, D. Rossi, M.-O. Buob,                From paris to tokyo: On the suitability of ping to
     J. Augé, and T. Friedman. A fistful of pings: Accurate         measure latency. In ACM IMC, 2013.
     and lightweight anycast enumeration and geolocation.       [41] I. Poese, S. Uhlig, M. A. Kaafar, B. Donnet, and
     In Proc. IEEE INFOCOM, 2015.                                    B. Gueye. IP geolocation databases: Unreliable? ACM
[18] D. Cicalese, D. Joumblatt, D. Rossi, M.-O. Buob,                CCR, 41(2), 2011.
     J. Augé, and T. Friedman. Latency-based anycast           [42] D. Rossi, G. Pujol, X. Wang, and F. Mathieu. Peeking
     geolocalization: Algorithms, software and datasets. In          through the BitTorrent seedbox hosting ecosystem. In
     Tech. Rep., 2015.                                               Proc. Traffic Monitoring and Analysis (TMA), 2014.
[19] L. Colitti. Measuring anycast server performance: The      [43] S. Sarat, V. Pappas, and A. Terzis. On the use of
     case of K-root. Nanog, 2006.                                    anycast in DNS. In Proc. ACM SIGMETRICS, 2005.
[20] C. Contavalli, W. van der Gaast, S. Leach, and             [44] Y. Shavitt and N. Zilberman. A geolocation databases
     E. Lewis. Client Subnet in DNS Queries. https://tools.          study. IEEE J-SAC, 29(10), 2011.
     ietf.org/html/draft-ietf-dnsop-edns-client-subnet-04.      [45] F. Streibelt, J. Böttger, N. Chatzis, G. Smaragdakis,
[21] http://www.enst.fr/˜drossi/anycast.                             and A. Feldmann. Exploring edns-client-subnet
[22] Z. Durumeric, E. Wustrow, and J. A. Halderman.                  adopters in your free time. In ACM IMC, 2013.
     Zmap: Fast internet-wide scanning and its security         [46] A. Su, D. R. Choffnes, A. Kuzmanovic, and
     applications. In USENIX Security Symposium, 2013.               F. Bustamante. Drafting behind akamai
[23] B. Eriksson, P. Barford, J. Sommers, and R. Nowak.              (travelocity-based detouring). In Proc. ACM
     A learning-based approach for IP geolocation. In                SIGCOMM, 2006.
     PAM, 2010.                                                 [47] R. Torres, A. Finamore, J. R. Kim, M. Mellia, M. M.
[24] B. Eriksson and M. Crovella. Understanding                      Munafo, and S. Rao. Dissecting video server selection
     geolocation accuracy using network geometry. In Proc.           strategies in the YouTube CDN. In Proc. of IEEE
     IEEE INFOCOM, 2013.                                             ICDCS, 2011.
[25] X. Fan, J. S. Heidemann, and R. Govindan.                  [48] S. Zander, L. L. Andrew, and G. Armitage. Capturing
     Evaluating anycast in the domain name system. In                ghosts: Predicting the used ipv4 space by inferring
     Proc. IEEE INFOCOM, 2013.                                       unobserved addresses. In ACM IMC, 2014.
[26] http://www.ict-mplane.eu/public/fastping.
[27] A. Flavel, P. Mani, D. A. Maltz, N. Holt, J. Liu,
     Y. Chen, and O. Surmachev. Fastroute: A scalable
     load-aware anycast routing architecture for modern
     cdns. In Proc. USENIX NSDI, 2015.
