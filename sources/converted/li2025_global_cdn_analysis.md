                                                                                                                               PDF Download
                                                                                                                               3763400.3763406.pdf
                                                                                                                               21 March 2026
                                                                                                                               Total Citations: 0
                                                                                                                               Total Downloads: 118
    .
    .
        Latest updates: hps://dl.acm.org/doi/10.1145/3763400.3763406




                                                                                                                               .
                                                                                                                               .
                                                                                                                     Published: 24 November 2025
        .
        .
                                                                                                                     .
    RESEARCH-ARTICLE




                                                                                                                     .
                                                                                                                     Citation in BibTeX format
    Measurement and Analysis of a Global-Scale CDN -- Locality, Dynamics,




                                                                                                                     .
                                                                                                                     .
                                                                                                                     AINTEC '25: Asian Internet Engineering
    and Load Balance                                                                                                 Conference
                                                                                                                     November 25 - 27, 2025
    GUO-CHENG LI, National Taiwan University, Taipei, Taiwan                                                         Manila, Philippines




                                                                                                                     .
    .
                                                                                                                     .
    POLLY HUANG, National Taiwan University, Taipei, Taiwan
    .
    .
    .
    Open Access Support provided by:
    .
    National Taiwan University
    .
                                                                 AINTEC '25: Proceedings of the 20th Asian Internet Engineering Conference (November 2025)
                                                                                                                      hps://doi.org/10.1145/3763400.3763406
                                                                                                                                         ISBN: 9798400718465
.
     Measurement and Analysis of a Global-Scale CDN – Locality,
                  Dynamics, and Load Balance
                                 Guo-Cheng Li                                                                       Polly Huang
                                     NTU                                                                               NTU
                                 Taipei, Taiwan                                                                    Taipei, Taiwan
                             r12942085@ntu.edu.tw                                                             pollyhuang@ntu.edu.tw

Abstract                                                                                    CDN and (2) the server selection strategy. There has been a body
Content Delivery network (CDN) is a critical part of the Internet                           of system [1–4] and performance [5–10] studies that co-design the
service design. It functions as a distributed cache of the content to                       CDN and server selection strategy for performance metrics such
deliver. Its scale, distribution and caching scheme concerns the user                       as delay, throughput, load balance, and power efficiency. Here, we
experience that the service providers seek to improve. To facilitate                        take a measurement approach and seek lessons from real world
the design and performance analysis process, we measure and                                 designs, much like how [11–13] unveil the CDN and the server
analyze the CDN of a popular live video service – Twitch. In that,                          selection strategy for global-scale Internet services such as Google,
we conducted a 30-day, global-scale crawl that mapped 2166 edge                             Bing and Akamai. To expand the knowledge base, we report in
servers across major continents. The effort, as far as we know, is                          this work the global CDN and the server selection strategy behind
the most widespread in time-span and geo-diversity in recent years.                         a popular live video service, i.e., Twitch [14]. Discovery of the
From the data collected, we observed a two-level hierarchy in the                           CDN and its server allocation strategy in Twitch could serve as
edge server (i.e., the video cache) selection process, similar to that                      a reference design for emerging live streaming services or CDN
has been reported in[16]. What we see new are 3 salient properties                          providers. The findings provide also as the performance baseline for
on the locality, dynamics, and load distribution of the servers. (1)                        studies that seek optimal balances among user experience, system
The system maintains the viewer-server proximity at the continent                           utilization, and/or energy efficiency.
granularity. (2) There is a slow rotation of the server clusters over                          Our contribution is two-fold. We first employ an open-source
time, and (3) The load distribution is approximately uniform random                         Twitch CDN crawler, i.e., Kukudy [15]. The crawler was designed
at both levels of the hierarchy. The tool, methodology, and the                             to scan as many video channels as possible within Europe [16]. To
findings are important intermediate steps to cost-effective data                            extend its crawling scope from Europe to the globe and to keep
collection and long-term study of CDNs in operation.                                        the probing traffic under control, we revise the default crawling
                                                                                            strategy such that it is capable of daily discovery of the global CDN.
CCS Concepts                                                                                With that, we rotate through 686 VPN nodes and crawl the top 2000
                                                                                            channels daily, from August 15 to September 15 2024. From the 30
• Networks → Network measurement.
                                                                                            daily snapshots, we observe 2166 CDN servers worldwide. In that,
Keywords                                                                                    1022, 363, 537, 216, and 28 servers are located in Europe, Asia, North
                                                                                            America, South America, and Oceania respectively. This crawl is, as
CDN measurement, Server selection, Video cache                                              far as we know, the most widespread in time span and geo-diversity
ACM Reference Format:                                                                       in recent years.
Guo-Cheng Li and Polly Huang. 2025. Measurement and Analysis of a                              Next, we analyze the data collected and discover three salient
Global-Scale CDN – Locality, Dynamics, and Load Balance. In 20th Asian                      properties in Twitch’s CDN server selection strategy. (1) A viewer
Internet Engineering Conference (AINTEC ’25), November 25–27, 2025, Manila,                 is assigned a server from a set of server clusters in proximity, indi-
Philippines. ACM, New York, NY, USA, 9 pages. https://doi.org/10.1145/
                                                                                            cating locality as a factor in Twitch’s server selection strategy. I.e.,
3763400.3763406
                                                                                            the viewer and the server clusters are generally close and within
                                                                                            the same region. The servers are more often called the edge servers
1    Introduction
                                                                                            for being close to the viewers at the edge of the Internet. (2) Over
Content Delivery network (CDN) is key to the user experience of                             a long time, one can observe a super server cluster set per viewer.
Internet services today. By duplicating or caching content on a                             The super set is fixed but the cluster set observed day to day can be
large set of servers worldwide, user requests are responded quickly.                        different, suggesting dynamics in clusters chosen for service. I.e.,
Video content, in particular, is the most sensitive to the delay and                        the server clusters may rotate in and out of service over time. (3)
available bandwidth in the delivery path. This makes CDN design                             Similar to Akamai’s server selection strategy [1], the mechanism in
critical to the quality of video streaming services. Specifically, the                      Twitch works in two levels. A cluster is selected first from the super
service quality depends on two factors: (1) the size/distribution of                        set. Within the cluster, an edge server is selected next. While the
                                                                                            two-level selection process in Twitch has been observed in [16], we
                                                                                            are able to confirm with the new data that the selection is close to
This work is licensed under a Creative Commons Attribution 4.0 International License.       uniform random at both levels, indicating load balance as another
AINTEC ’25, Manila, Philippines
© 2025 Copyright held by the owner/author(s).                                               factor in Twitch’s design. I.e., the CDN operates under a balanced
ACM ISBN 979-8-4007-1846-5/25/11                                                            load.
https://doi.org/10.1145/3763400.3763406




                                                                                        9
AINTEC ’25, November 25–27, 2025, Manila, Philippines                                                                      Guo-Cheng Li and Polly Huang




Figure 1: The number of VPN nodes used in the one-month,                         Figure 2: Coverage ratio versus number of channels crawled.
global-scale crawl by continents.                                                Crawling the top 2,000 channels reveals 100% of servers ob-
                                                                                 served crawling all 50,000 channels.

2     Measurement Methodology
In this study, we employed an enhanced version of Kukudy to                      RO, SK, UA, AE, IN, TH, JP, KR, TW, HK, SG, ID, PH, MY, IL, AU,
explore the global Twitch CDN. This section outlines the strategies              NZ, AR, BR, CL, CO, MX, PE, US, and CA.
for selecting VPN nodes and Twitch channels1 , emphasizing how                      It is worth noting that the distribution of available VPN nodes
these decisions ensure a cost-effective collection of the global CDN.            reflects the infrastructure layout of NordVPN, with a higher den-
                                                                                 sity in Europe and North America, while regions such as Asia,
2.1      Crawler                                                                 South America, and Oceania have relatively fewer nodes, especially
Our crawler was designed to optimize the efficiency of captur-                   in remote or less connected areas. Nevertheless, this geographic
ing global snapshots of Twitch’s CDN. Utilizing APIs released by                 imbalance does not fundamentally impact the validity of our mea-
Twitch, Kukudy is an efficient crawler that leverages APIs released              surements. The primary goal of our experiment is to observe the
by Twitch and the VPN provider. It can be configured to request                  CDN server assignment strategy based on viewer geolocation, and
a specific set of channels, receive the corresponding URLs, and                  our dataset ensures sufficient coverage of major population centers
discover the servers hosting the channels from worldwide loca-                   and regional access points. As a result, the observed CDN behavior
tions, thereby revealing the global server network. Building on                  reflects the practice of server allocation under real-world condi-
Kukudy, we carefully selected VPN nodes and Twitch channels                      tions. Furthermore, as discussed later in Section 3.1.2, we validate
to achieve broad edge server coverage. By targeting a limited yet                that increasing the number of VPN nodes or expanding the set of
representative sample of VPN nodes and channels, we obtained a                   crawled channels in underrepresented regions results in minimal
comprehensive view of the CDN while minimizing the time and                      change to the set of active CDN servers observed.
network resources required.
                                                                                 2.1.2 Channel Selection. The selection of Twitch channels aimed
2.1.1 VPN Node Selection. By using NordVPN [22], we were able                    at minimizing the number of channels crawled while maximizing
to emulate Twitch viewer interactions across different geographical              CDN coverage. To explore this, in April 2024 we conducted an
regions. To accurately represent global viewership, we systemati-                experiment using VPN nodes located in different regions, including
cally traversed each VPN node to determine its IP address, using                 the United Kingdom, United States, Japan, Australia, and Argentina,
the /24 mask to define each unique subnet. In total, 686 unique                  to crawl the top 50,000 Twitch channels worldwide.
subnets were identified by this process as of August 13, 2024. Note                 As shown in Fig. 2, CDN coverage increases rapidly with the
that NordVPN updates its server infrastructure occasionally, so this             number of channels crawled. However, after approximately 2,000
number may change over time. Since nodes within the same subnet                  channels (indicated by the red dotted line), the coverage ratio ap-
typically exhibit similar routing and connectivity characteristics,              proaches 1.0, signifying that most of the edge servers have been
we select only one node in each subnet. Through the mapping of                   reached. Crawling beyond this threshold offers little additional
these subnets, we ensure that our crawling system covers Twitch’s                value in terms of coverage, allowing us to focus on 2,000 channels
global CDN effectively, which improves the representativeness of                 to maximize efficiency.
the data.
   As shown in Fig. 1, these 686 VPN nodes are distributed across                2.2   Crawling Strategy
multiple regions, including 349 from Europe, 44 from Asia, 182                   Our rate control mechanism takes into account Kukudy’s rate lim-
from North America, 15 from South America, and 24 from Oceania.                  itations [16] and ensures uninterrupted data collection. Despite
Specifically, they cover countries including SE, UK(GB), NL, DE, FR,             Twitch’s maximum request rate of 30 channels per second, we
ES, IT, NO, DK, CZ, PL, AT, FI, BE, CH, BG, CY, HU, LT, MD, PT,                  chose to set it slightly lower at 25 channels per second to pre-
                                                                                 vent throttling or interruption during crawling. As for NordVPN’s
1 These channels are live streams, i.e., mass majority content in Twitch.        switching limit of 10 VPN nodes in 4 minutes, we did not need




                                                                            10
Measurement and Analysis of a Global-Scale CDN – Locality, Dynamics, and Load Balance                          AINTEC ’25, November 25–27, 2025, Manila, Philippines




Figure 3: The map of the CDN servers discovered. There are 2166 servers globally, with 1,022 , 537, 363, 216, and 28 servers in
Europe, North America, Asia, South America, and Oceania. Each circle indicates the location of a server cluster. The size of the
circle indicates the number of servers in the cluster in proportion.


to make any adjustments since it takes 80 seconds to crawl 2,000                        crawl, we observed 2166 servers contained in 64 clusters. The server
channels per VPN node far exceeds NordVPN’s switching limit.                            clusters are plotted in Fig. 3. Each circle represents a cluster. The
   For our crawler, crawling 2,000 channels takes 80 seconds, with                      size of the circle reflects the amount of servers in the cluster. Europe
an additional 20 seconds for connecting to the next VPN node                            is the region with the highest concentration, i.e., 23 clusters with
and buffering, resulting in a total crawl time of 100 seconds per                       1,022 servers. North America comes second, hosting 18 clusters
node. The buffering time includes the time acquiring the top 2000                       with 537 servers. Asia, South America are the 3rd and 4th, hosting
channels for the VPN location. Based on 686 VPN nodes, a complete                       13 clusters with 363 servers and 8 clusters with 216 servers. Oceania
global crawl would require 68,600 seconds, or about 19 hours and 3                      hosts only 2 clusters with 28 servers.
minutes. By monitoring the process of handling channel requests,
we avoided detecting other traffic and determined that each channel
request requires about 8KB of download traffic and 2KB of upload                        3.1    Validation
traffic. With 25 channel requests per second, the total traffic is                      To assess the data, we compare the CDN discovered by our crawl
approximately 200KB/s downlink and 50KB/s uplink.                                       to the CDN as registered to the authority by Twitch. To assess
   Since peak and off-peak hours differ across countries, sequen-                       the crawling strategy, we conducted additional experiments to see
tial traversal of VPN nodes could result in some nodes always                           whether the result is affected by different crawler settings.
requesting channels at the same time of day, limiting the diver-
sity of servers discovered. To mitigate this, we applied uniform
random shuffling to the VPN node traversal order prior to each                          3.1.1 rDNS lookup. We performed rDNS lookups over all IP ad-
crawl. A new random permutation of the node list is generated                           dresses under AS46489 (Twitch Interactive Inc.) as recorded in
daily using a pseudo-random number generator with uniform prob-                         IPinfo.io [23]. Only the nodes with a specific hostname pattern are
ability, ensuring equal likelihood of all visiting sequences. This                      selected. "video-edge-c2b5c8.lax03.abs.hls.ttvnw.net" is the pattern
design guarantees that the order varies completely from day to day.                     a video server is named in Twitch [21]. The first part of the prefix
Consequently, each VPN node is probabilistically distributed across                     is the unique host ID and the 2nd part the cluster ID.
different time windows over the month-long experiment, covering                             Table 1 compares the result from the rDNS lookups and the
both peak and off-peak hours.                                                           global crawl. Listed in the table are the specific countries, cities,
                                                                                        CDN clusters, the number of registered CDN servers from the rDNS
                                                                                        lookups, and the number of CDN servers discovered during the
3    CDN Discovered and Validation                                                      global crawl. According to IPInfo.io, Europe has 29 CDN clusters
The global crawl of 686 VPN nodes is conducted daily for a month                        with 1,793 servers, North America has 25 clusters with 1,153 servers,
from August 15 to September 15 2024. The results in Section 3, 4,                       and Asia has 23 clusters with 850 servers. South America includes
and 6 are the union of the 31 daily CDNs. Section 5 is special. In                      14 clusters with 616 servers, and Oceania has 3 clusters with 70
that, we analyze the difference of the daily CDNs. From the global                      servers. As compared with other continents, North America and




                                                                                11
AINTEC ’25, November 25–27, 2025, Manila, Philippines                                                                                   Guo-Cheng Li and Polly Huang


                   Table 1: Comparison of the CDN servers reported by IPinfo.io vs. discovered by the global crawl.

                           Europe                                               Asia                                          North America
  Country        City         Cluster   IPinfo   Kukudy   Country     City       Cluster   IPinfo   Kukudy   Country       City          Cluster   IPinfo   Kukudy
    ES          Madrid        mad01      120       71       IN      Bangalore     blr01     23        21       US         Atlanta         atl01     59        51
                              mad02      31        28                Chennai      maa01     31        30                  Miami           mia05     64        57
    GB          London         lhr03     45        45                 Delhi       del01     23        23                 New York         jfk04     104       72
                               lhr04     36        0                Hyderabad     hyd01     26        26                                  jfk06     72        29
                               lhr08     20        20                Mumbai       bom01     28        26                                  jfk50     19        14
                               lhr05      1        0        TH       Bangkok      bkk01     32        0                Washington         iad03     19        13
    FR           Paris         cdg02     108       29                             bkk02     25        0                                   iad05     69        21
                               cdg10     53        48       ID       Jakarta      jkt01     17        0                  Chicago          ord02     79        0
               Marseille      mrs02      50        50                             jkt02     18        18                                  ord03     87        45
    NL        Amsterdam       ams02      134       19       CN      Hong Kong     hkg01     35        0                                   ord56     23        19
                              ams03      29        20                             hkg06     24        24                  Dallas          dfw02     129       70
    NO           Oslo          osl01     30        25       PH       Manila       mnl01     19        0                                   dfw56     25        19
     IT         Milan          mil02     84        84       SG      Singapore     sin01     54        40                 Houston          hou01     21        0
    DK       Copenhagen       cph01      33        30                             sin04     42        41                                  iah50     17        15
    DE        Dusseldorf       dus01     55        53      TW        Taoyuan      tpe01     49        26                  Denver          den01     18        0
               Frankfurt       fra02     193       75                             tpe03     33        0                                   den52     16        11
                               fra05     164       97       JP        Osaka       osa01     18        14                 Phoenix          phx01     18        0
                               fra06     94        34                 Tokyo       tyo01     17        0                Salt Lake City     slc01     18        0
               Munich         muc01      29        27                             tyo03     41        37                    LA            lax03     98        61
                Berlin         ber01     59        0                              tyo05     50        37                 San Jose         sjc05     36        0
    CZ          Prague         prg02      1        0        KR        Seoul       sel01     15        0                                   sjc06     22        16
                               prg03     20        17                             sel03     157       0                   Seattle         sea01     24        0
    AT          Vienna         vie02     52        50                             sel04     73        0                                   sea02     17        17
    SE        Stockholm        arn03     95        55                                                          CA        Montreal         ymq03     44        40
                               arn04     107       44                                                                    Toronto          yto01     55        42
    PL         Warsaw         waw01      30        0
                              waw02      29        29
     FI        Helsinki        hel01     15        0
                               hel03     76        72
   Sum                                  1793      1022     Sum                              850      363      Sum                                  1153      537


                    South America                                              Oceania
  Country        City         Cluster   IPinfo   Kukudy   Country     City       Cluster   IPinfo   Kukudy
    AR       Buenos Aires     bue01      29        27       AU       Sydney       syd01     29        0
    BR         Fortaleza       for01     28        19                             syd02     25        16
            Rio de Janeiro     rio01     51        0                              syd03     16        12
                               rio03     126       47
                               rio04     27        0
              São Paulo        sao01     98        0
                               sao03     32        23
                               sao05     62        48
    CL         Santiago        scl01     29        21
    CO          Bogotá        bog01      22        16
    MX        Queretaro        qro01     23        0
                               qro02     45        0
                               qro03     18        15
                               qro04     26        0
   Sum                                   616      216      Sum                              70        28




                                                                                12
Measurement and Analysis of a Global-Scale CDN – Locality, Dynamics, and Load Balance                          AINTEC ’25, November 25–27, 2025, Manila, Philippines




Figure 4: The viewer-server heatmap by the continents. One can see that most viewers are mapped to the clusters in the same
continent. There are a few exceptions for the continents that are less resourced.


Europe have a higher number of servers, reflecting greater demand                       more or less. This suggests that our crawling strategy is efficient in
and better infrastructure.                                                              covering the CDN servers that are actively delivering content.
   We see generally a higher number of servers and clusters from
IPInfo.io. The CDN discovered by our crawl is 57-79% lower in
number of clusters and 35-57% lower in number of servers. A similar                     3.2    Discussion
level of discrepancy has been reported in [16] where Kukudy was                         Here we examine further the clusters that we did not find any active
used to crawl the CDN in Europe in 2023. In that work, the authors                      servers. For instance, the lhr04, hkg01, sjc05, rio01, and syd01 cluster
reported seeing 28 clusters and 1755 servers from IPinfo.io and                         in Table 1. Despite their existence in the IPinfo.io database, these
24 clusters and 1045 servers from an EU-wide crawl. I.e., only a                        CDN clusters are not active in the period of our crawl. Most of these
fraction of the servers registered are active. Comparing the result                     clusters are one of several clusters serving a city or country. This
from [16] to the EU part of our data, we see 1 more cluster and 38                      is not surprising as service providers often adjust their CDNs for
more servers registered in 2024. It is not unusual to see an Internet                   maintenance purpose or changes in workload. Less expected are the
service expanding its CDN infrastructure and adding new clusters                        clusters in Korea, Thailand, and the Philippines. We see no servers
to the domain registry. There is however one less cluster and 23                        in these countries at all. In Korea, IPinfo.io shows that cluster sel01,
less servers in the EU part of our crawl. This can be attributed to                     sel03, and sel04 have a total of 245 IP addresses. However, none
the number of channels crawled in [16]. It is 50 times higher than                      of our requests from Korean VPN nodes are assigned to the sel0*
the number requested in this study. Seeing 2% less servers seems                        clusters. A search on the Web revealed that Twitch clusters in Korea
reasonable.                                                                             were shutdown in February 2024 due to high network access fee.
                                                                                        The Korean clusters are off because of a change in operation cost.
                                                                                        Furthermore, compared to other regions, changes in CDN server
3.1.2 Sensitivity of parameter choices. To assess whether crawl-                        allocation is more common in Asia, possibly because Twitch is often
ing only 2,000 channels and selecting specific VPN nodes would                          not the primary choice for video streaming in Asian countries. For
impact the number of clusters and CDN servers discovered, we                            example, Japanese and Korean users prefer the domestic streaming
conducted three experiments targeting countries where significant                       platforms, such as Niconico [24] in Japan and AfreecaTV [25] in
discrepancies were found between IPinfo.io and our global crawl.                        Korea. Similarly, the service demand in Thailand and the Philippines
They are TH, ID, BR, KR, MX, and PH. In these experiments, we                           is likely not substantial or steady enough to justify the cost of
no longer crawled from a subset of VPN nodes but all the VPN                            operating a local server cluster. Instead, Korean viewers are assigned
nodes in those countries. We increased the number of channels to                        to CDN clusters in neighboring countries such as Japan or North
20,000 and ensured that each country was covered during peak and                        America, while Thai and Filipino viewers are assigned to CDN
off-peak hours. The results showed that expanding the range of                          clusters in Singapore.
VPN nodes and increasing the number of channels did not improve                            Unlike Korea, Thailand, and the Philippines, other regions did not
the likelihood of being assigned to the targeted CDN clusters. The                      exhibit such extreme phenomena. The CDN clusters that were not
number of identified CDN servers remained nearly the same as                            identified are likely backup servers, used for emergency allocation
in the original experiments, with variations of one or two servers                      when server load exceeds the capacity, or previously used clusters




                                                                                13
AINTEC ’25, November 25–27, 2025, Manila, Philippines                                                                   Guo-Cheng Li and Polly Huang




                       Figure 5: The total viewer-server heatmap sorted by the rank of the principle component.


that are still registered with IPinfo.io. In terms of active servers,         are grouped and shown using a unique color. One can see that
Europe shows the highest proportion, with approximately 56% of                viewers are typically assigned to a CDN cluster that corresponds
servers active. This higher percentage could be due to Europe’s               to their geographic location, showing that proximity is a factor
complex network infrastructure and geographically distributed                 in the decision. In North America and Europe, viewers are mostly
user base, requiring more active CDN servers to ensure low la-                assigned to local CDN clusters, minimizing data transfer distances
tency and consistent performance across various countries. North              and optimizing service performance. In South America, a few view-
America, Asia, and Oceania have around 40% of their servers active,           ers are directed to North American CDN clusters. This is expected,
which represents a more typical balance between active and backup             as South America is geographically close to North America and
servers. South America shows the lowest activity level, with about            some viewers in South America may be closer to North American
35% of servers active. This lower percentage in South America                 servers.
might be explained by the fact that the users nearby North America               However, in Oceania and Asia, cross-regional assignments are
can be mapped to North American servers, reducing the need for                more common. Oceania has local CDN servers, but most viewers
active servers within South America itself. In the following sections,        are still assigned to North American CDN servers. The system is
we will focus our analysis on these active CDN clusters.                      likely reassigning viewers to servers in other regions because the
                                                                              local servers cannot handle the full load. In Asia, some viewers are
4     Server Cluster Locality                                                 assigned to European servers, particularly in countries like Israel
To show whether the location of the viewers affects server selec-             and parts of the Middle East, which are geographically closer to
tion, we present first for viewers in a particular continent where            Europe. Like Oceania, some Asian viewers can be assigned to North
the selected server clusters are. Towards a structural understand-            American servers in case of excessive load. Overall, proximity de-
ing, we present the viewer-server relationship next as a heatmap              termines largely how the server cluster is selected, but the mapping
and analyze the relationship by the Principal Component Analysis              can be flexible and adapt dynamically for regions that are under
(PCA).                                                                        provisioned.

4.1     Viewer-Server Co-Locality                                             4.2    Heatmap and PCA Analysis
Fig. 4 depicts where the servers are for viewers in 5 continents. In          To show the global viewer-server mapping, we visualize the rela-
each of the 5 plots, the x-axis represents individual viewers (i.e.,          tionship as a heatmap in Fig. 5. The x-axis represents the viewers
VPN nodes) in the continent and the y-axis gives the location of              and the y-axis represents the server clusters. Each grid (x, y) is
the servers (i.e., CDN clusters). The servers in a specific continent         highlighted when viewer x has been assigned a server in cluster




                                                                         14
Measurement and Analysis of a Global-Scale CDN – Locality, Dynamics, and Load Balance                          AINTEC ’25, November 25–27, 2025, Manila, Philippines


y in our data. Next, we reduce the dimensionality of the heatmap
using PCA. This allows us to capture the primary variations within
the dataset. We are able to reveal which viewers behaved similarly
in terms of server cluster allocation by comparing the coefficient of
the principle component. See the green line in Fig. 5. It indicates the
sorted ranking of viewers along the principal component, revealing
groups of viewers with similar viewer-server mapping. A visual-
ization such as this shows how certain viewers are more likely to
connect to specific servers and can be used to identify anomalies or
changes in the server allocation strategy for a long-term analysis of
the server allocation policy in the CDN, i.e., a subject of our future
work.


                                                                                        Figure 6: The average percentage of the server clusters remain
5    Server Cluster Dynamics                                                            the same over days (Δ𝑇 ).
We explore next whether Twitch adjusts the server cluster assign-
ment dynamically. To this end, we conduct another measurement.
The crawling strategy consists of a global crawl once per day. The
VPN nodes are traversed in random order each day to ensure that                         6.1    Inter-cluster Level
each VPN node (i.e., viewers over the world) requests channels                          The ECDF and ACF plot of server selection process at the interclus-
across peak and off-peak hours in a day. We examine the CDN                             ter level are illustrated in Fig. 7. On the left, the ECDF plot compares
clusters assigned day to day per VPN node. For a given day, we                          the empirical distribution (represented by the orange solid line) to
calculate the percentage of CDN clusters reappearing Δ𝑇 days later.                     the ideal uniform distribution (represented by the dashed line). Let
The metric indicates how much the server cluster set remains the                        𝑁𝐶 represent the number of times cluster 𝐶 is selected to serve a
same. Fig. 6 shows the average of such percentage over all VPN                          channel over the 1-month crawling period. The density function
nodes. In that, Δ𝑇 = 1 compares each VPN node’s CDN clusters on                         (DF) is 𝑃𝐶 = 𝑁𝐶 /𝑁 , where 𝑁 is the total number of channel re-
day 𝑁 with 𝑁 + 1. Similarly, Δ𝑇 = 2 compares day 𝑁 with day 𝑁 + 2,                      quests. The cumulative density function (CDF) stacks the density
and so on. As can be seen, the cluster set shows the highest similar-                   up. In case 𝑃𝐶 are equal among all clusters, i.e. a uniform distri-
ity when Δ𝑇 = 1, i.e., compared between two consecutive days. As                        bution, the DF will be flat and the CDF will be diagonal towards
Δ𝑇 increases, the similarity decreases. The decrease in similarity is                   upper right. The cumulative distribution appears to align with the
relatively small, with the difference between Δ𝑇 = 1 and Δ𝑇 = 15                        uniform distribution, indicating that most CDN clusters across dif-
around 10%. Most of the changes occur in regions with many CDN                          ferent regions are utilized fairly evenly. However, in certain regions,
clusters, such as Europe and North America, where more changes                          the ECDF curve shows sharp increases, revealing that some clus-
are observed. In contrast, the server clusters in Asia, South America,                  ters are allocated significantly more than the others. This happens
and Oceania show fewer changes in absolute number. However, if                          mainly in Europe and North America, where the number of VPN
we look at the change in percentage, i.e., the solid blue and red lines                 nodes used in our experiment is higher. On the right, the ACF plot
in Fig. 6, these regions appear relatively more dynamic in assigning                    reveals the temporal autocorrelation of cluster usage frequencies.
server clusters. This suggests that regions with a large number of                      Generally, the autocorrelation values are close to zero, indicating
CDN clusters tend to adjust frequently in absolute terms, while                         minimal temporal dependency. However, a few points show higher
regions with fewer clusters may appear less dynamic overall but                         autocorrelation values, indicating that certain clusters may experi-
are relatively more volatile when viewed proportionally. Overall,                       ence recurring usage patterns. This could be due to the clustering
the server clusters do change but slowly, possibly the result of a                      of VPN nodes or consistent traffic loads in specific regions.Overall,
common practice that rotates the servers in and out of service for                      it shows that Twitch’s CDN cluster allocation at the inter-cluster
maintenance or troubleshooting purpose.                                                 level is largely uniform across regions and independent over time.

                                                                                        6.2    Intra-cluster Level
6    Server Load Distribution                                                           We observe that intra-cluster distributions are generally consistent
We next examine how workload is distributed across servers world-                       across different clusters. Therefore, we select the lhr03 cluster as
wide, specifically how clusters from the super set and servers within                   a representative for discussion. See Fig. 8. Compared to the inter-
each cluster are selected. While prior work [16] revealed the 2-level                   cluster level analysis, the intra-cluster patterns in the ECDF plot are
hierarchy of this process, the exact load distribution remains un-                      more distinct, showing a closer alignment with the ideal uniform
clear. To characterize it, we apply two standard statistical tests: the                 distribution, suggesting that server utilization within the lhr03 clus-
Empirical Cumulative Distribution Function (ECDF) for uniformity                        ter is well-balanced. The ACF plot confirms further that the server
and the Autocorrelation Function (ACF) for randomness. Below                            assignments are generally independent. Overall, Twitch’s server
we analyze distribution at both the inter-cluster and intra-cluster                     load is balanced across and within clusters with minor variation to
levels.                                                                                 adapt to varying traffic loads.




                                                                                15
AINTEC ’25, November 25–27, 2025, Manila, Philippines                                                                  Guo-Cheng Li and Polly Huang




Figure 7: Left: ECDF plot of the server cluster selection process. The server cluster selection process (orange solid line) deviates
from a perfect uniform distribution (green dashed line) but not by much. Right: ACF plot of the server cluster selection process.
There is no clear autocorrelation in server cluster selection, indicating the process is nearly uniform random.




Figure 8: Left: ECDF plot of the server selection process within cluster lhr03. The server selection process (orange solid line)
is a perfect fit to a uniform process (green dashed line). Right: ACF plot of the server selection process. There is no clear
autocorrelation in the server selection process in cluster lhr03, indicating the process is uniform random.


7    Related Work                                                            streams. To cover a significant geographical span, they exploited
Twitch and its CDN are well studied. [17] was the first study unveil-        806 proxy servers sending the stream requests worldwide. They
ing the use of RTMP, HLS, and 3-way redirection along the video              were able to observe the set of video servers allocated to viewers
distribution pipeline and investigating the arrival process of view-         from different regions of the world. Their analysis showed that the
ers and the popularity distribution of the videos. [18] presented            server allocation policy tend to minimize delay and server load.
a dataset by collecting traffic generated from YouTube Live and              More recently, Wung et al. [20] performed a partial scan of Twitch’s
Twitch and inferred the size of the services in respect of bandwidth         CDN by deploying a crawler on a cloud computing platform. Wang
usage and the number of concurrent channels. Deng et al. [19] is the         et al. [21] documented another crawler and their result for de-
first to measure Twitch’s CDN by repeatedly requesting available             ploying it on a VPN platform. Chou et al. [16] devised an efficient




                                                                        16
Measurement and Analysis of a Global-Scale CDN – Locality, Dynamics, and Load Balance                                       AINTEC ’25, November 25–27, 2025, Manila, Philippines


crawler, i.e., Kukudy. The authors scanned Twitch’s CDN in Europe                              [3] Mukerjee, Matthew K. and Naylor, David and Jiang, Junchen and Han, Dongsu
as completely as possible, referred to as a best-effort scan to serve                              and Seshan, Srinivasan and Zhang, Hui: Practical, Real-time Centralized Control
                                                                                                   for CDN-based Live Video Delivery. In Proceedings of the 2015 ACM Conference
as the best-line to understand the trade-off between CDN coverage                                  on Special Interest Group on Data Communication, pp. 311–324. ACM SIGCOMM
and traffic overhead. In this work, we refine the crawling strategy                                ’15, London, United Kingdom (2015)
                                                                                               [4] J. Kangasharju, F. Hartanto, M. Reisslein and K. Ross: Distributing Layered Encoded
from [16] which enables us to measure Twitch’s global CDN and                                      Video through Caches. IEEE Transactions on Computers 51(06), 622–636 (2002)
observe the dynamics of the CDN over a month time.                                             [5] Kara, Burak and Simon, Gwendal: Power Efficient Multi-CDN Communication
                                                                                                   over Content Steering Server. In Proceedingsof the 15th ACM Multimedia Systems
                                                                                                   Conference, pp. 478–484. ACM MMSys ’24, Bari, Italy (2024)
8    Conclusion                                                                                [6] Usama Naseer and Theophilus A. Benson: Configanator: A Data-driven Approach
                                                                                                   to Improving CDN Performance. In Proceedings of the 19th USENIX Symposium
We have achieved a global crawl of Twitch’s CDN and discovered                                     on Networked Systems Design and Implementation, pp. 1135–1158. USENIX NSDI
2166 servers using a lightweight crawling strategy. The crawling                                   ’22, Renton, WA (2022)
strategy facilitates data collection and long-term observation of                              [7] Wang, Huan and Tang, Guoming and Wu, Kui and Fan, Jiamin: Speeding up Multi-
                                                                                                   CDN Content Delivery via Traffic Demand Reshaping. In Proceedings of the 38th
an Internet-scale eco-system. To consolidate the empirical result,                                 IEEE International Conference on Distributed Computing Systems, pp. 422–433.
one can compare to data from alternative rDNS services such as                                     IEEE ICDCS ’18, Vienna, Austria (2018)
Hoiho [26] or data discovered from alternative VPN providers. The                              [8] D’Oro, Salvatore and Galluccio, Laura and Palazzo, Sergio and Schembra, Giovanni:
                                                                                                   A Game Theoretic Approach for Distributed Resource Allocation and Orchestra-
data collected give rise to several observations of Twitch’s server                                tion of Softwarized Networks. IEEE Journal on Selected Areas in Communications
selection strategy. The findings facilitate performance analysis of                                35(3), 721–735 (2017)
                                                                                               [9] Liu, Chang and Sitaraman, Ramesh K. and Towsley, Don: Go-with-the-winner:
the caching schemes towards cost-effective CDN designs. Towards                                    Performance based client-side server selection. In Proceedings of the 2016 IFIP
long-term analysis of large-scale CDNs at work, we seek to explore                                 Networking Conference (IFIP Networking) and Workshops, pp. 404-412. IEEE IFIP
in the future work the feasibility of a metric such as the principle                               Networking ’16, Vienna, Austria (2016)
                                                                                               [10] Li, Chenglin and Frossard, Pascal and Xiong, Hongkai and Zou, Junni: Distributed
component ranking proposed in Section 4.2 as a fingerprint of                                      wireless video caching placement for dynamic adaptive streaming. In Proceedings
viewer-server mapping, with which one may identify anomalies or                                    of the 26th International Workshop on Network and Operating Systems Support
structural changes in a large-scale CDN with ease.                                                 for Digital Audio and Video. ACM NOSSDAV’16, Klagenfurt, Austria (2016)
                                                                                               [11] Calder, Matt and Fan, Xun and Hu, Zi and Katz-Bassett, Ethan and Heidemann,
                                                                                                   John and Govindan, Ramesh: Mapping the Expansion of Google’s Serving In-
A     Appendix: Ethical Consideration                                                              frastructure. In Proceedings of the 2013 Conference on Internet Measurement
                                                                                                   Conference, pp. 313–326. ACM IMC ’13, Barcelona, Spain (2013)
With regard to the channels and streamers. Twitch allows both                                  [12] Calder, Matt and Flavel, Ashley and Katz-Bassett, Ethan and Mahajan, Ratul and
                                                                                                   Padhye, Jitendra: Analyzing the Performance of an Anycast CDN. In Proceedings
streamers and viewers to download video streams and clips, but                                     of the 2015 Internet Measurement Conference, pp. 531–537. ACM IMC ’15, Tokyo,
reuse without the creator’s consent is a copyright violation. Our                                  Japan (2015)
crawler stopped at the master playlist server; no video content                                [13] Chen, Fangfei, Sitaraman, Ramesh K., Torres, Marcelo: End-User Mapping: Next
                                                                                                   Generation Request Routing for Content Delivery. In Proceedings of the 2015
was downloaded or reused. In addition to public information such                                   ACM Conference on Special Interest Group on Data Communication, pp. 167–181.
as channel ID, title, viewer count, started time, language, game,                                  ACM SIGCOMM ’15, London, United Kingdom (2015)
tags, streamer user ID, user login, and user name, the information                             [14] Christine Weber: Twitch State of Engineering 2023 (2023), https://blog.twitch.tv/
                                                                                                   en/2023/09/28/twitch-state-of-engineering-2023/, last accessed 2024/09/14
collected regarding the channels and streamers was limited to the                              [15] Hsuan-Yu Chou: Kukudy, Github (2023), https://github.com/hy-chou/kukudy,
origin of the stream at a subcontinental level. This origin may                                    last accessed 2024/09/14
                                                                                               [16] Chou, Hsuan-Yu and Huang, Yu-Ting and Huang, Polly: Best-Effort Scan of
suggest the ingest server used, and hence the streamer’s approxi-                                  Twitch’s CDN in Europe. In Proceedings of the 18th Asian Internet Engineering
mate location, but it is coarse enough not to constitute personal or                               Conference, pp. 10–18. ACM AINTEC ’23, Hanoi, Vietnam (2023)
sensitive information.                                                                         [17] Zhang, Cong and Liu, Jiangchuan: On Crowdsourced Interactive Live Streaming:
                                                                                                   A Twitch.TV-Based Measurement Study. In Proceedings of the 25th ACM Work-
   With regard to Twitch, NordVPN, and the Internet community.                                     shop on Network and Operating Systems Support for Digital Audio and Video, pp.
Information on active channels was obtained through the official                                   531–537. ACM NOSSDAV ’15, Portland, Oregon (2015)
Twitch API, which is commonly used by Twitch users to support                                  [18] Pires, Karine and Simon, Gwendal: YouTube Live and Twitch: A Tour of User-
                                                                                                   Generated Live Streaming Systems. In Proceedings of the 6th ACM Multimedia
analysis and enhance client–viewer interaction. Our crawler in-                                    Systems Conference, pp. 225–230, ACM MMSys ’15, Portland, Oregon (2015)
teracted only with standard Twitch CDN systems—including the                                   [19] Deng, Jie and Tyson, Gareth and Cuadrado, Félix and Uhlig, Steve: Internet Scale
                                                                                                   User-Generated Live Video Streaming: The Twitch Case. Amann, J. (eds) Passive
GraphQL endpoint, the Usher, the video weavers, and the video                                      and Active Measurement. PAM 2017. Lecture Notes in Computer Science(2017),
edge servers—all of which are part of the normal data path used                                    vol 10176. Springer, Cham.
by regular viewers. At no point did we exceed the request volume                               [20] Wung, Wei-Shiang and Ting, Guan-Ting and Hsu, Ruey-Tzer and Hsu, Cheng
                                                                                                   and Tsai, Yu-Chien and Wang, Caleb and Liu, Yuan-Tai and Chen, Hsi and Huang,
expected of ordinary users: the crawling frequency was kept below                                  Polly: Twitch’s CDN as an Open Population Ecosystem. In Proceedings of the
Twitch’s published rate limits. Likewise, NordVPN imposes con-                                     16th Asian Internet Engineering Conference, pp. 56–63. ACM AINTEC ’21, Virtual
nection limits to prevent abuse, and our measurements respected                                    Event, Japan (2021)
                                                                                               [21] Wang, Caleb and Liu, Yuan-Tai and Huang, Polly: Jujuby: Design and Deployment
these restrictions.                                                                                of a Crawler for Twitch CDN Mapping. In Proceedings of the 17th Asian Internet
                                                                                                   Engineering Conference, pp. 44–52. ACM AINTEC ’22, Hiroshima, Japan (2022)
                                                                                               [22] NordVPN: NordVPN Website, https://nordvpn.com/, last accessed 2024/09/14
References                                                                                     [23] ipinfo.io: AS46489 Twitch Interactive Inc., https://ipinfo.io/AS46489, last accessed
[1] Chen, Jiayi, Sharma, Nihal, Khan, Tarannum, Liu, Shu, Chang, Brian, Akella, Aditya,            2024/09/14
    Shakkottai, Sanjay, Sitaraman, Ramesh K: Darwin: Flexible Learning-based CDN               [24] NicoNico: Japanese Famous Live Streaming Platform, https://www.nicovideo.jp,
    Caching. In Proceedings of the ACM SIGCOMM 2023 Conference, pp. 981-999.                       last accessed 2024/09/25
    ACM SIGCOMM’23, New York, NY, USA (2023)                                                   [25] Afreeca Tv: Korea Famous Live Streaming Platform, https://www.afreecatv.com/,
[2] Zhou, Mengying and Guo, Tiancheng and Chen, Yang and Wan, Junjie and Wang,                     last accessed 2024/09/25
    Xin: Polygon: a QUIC-based CDN server selection system supporting multiple re-             [26] Hoiho: rDNS Lookup Service, https://hoiho.caida.org/, last accessed 2025/08/18
    source demands. In Proceedings of the 22nd International Middleware Conference:
    Industrial Track, pp. 16–22. ACM Middleware ’21, Québec city, Canada (2021)




                                                                                          17
