    Vantage Point Selection for IPv6 Measurements:
     Benefits and Limitations of RIPE Atlas Tags
        Vaibhav Bajpai∗ , Steffie Jacob Eravuchira† , Jürgen Schönwälder‡ , Robert Kisteleki§ , Emile Aben§
                                                    ∗ TU Munich, Germany

                                                   bajpaiv@in.tum.de
                                              † SamKnows Limited, London, UK

                                                 steffie@samknows.com
                                            ‡ Jacobs University Bremen, Germany

                                     j.schoenwaelder@jacobs-university.de
                                            § RIPE NCC, Amsterdam, NL

                                        (robert | emile.aben)@ripe.net


   Abstract—RIPE Atlas consists of ∼9.1K probes (as of Jan                                   RIPE Atlas Probes
2017) connected in core, access and home networks. RIPE Atlas
                                                                  20K




                                                                                                                   STATUS
                                                                                                             API
has recently (Jul 2014) introduced a tagging mechanism for                         NEVER CONNECTED
fine-grained vantage point selection of probes. These tags are    15K              CONNECTED
subdivided into user and system tags. User tags are based                          DISCONNECTED
on a manual process which is largely dependent on proactive       10K              ABANDONED
participation of probe hosts. We show that only ∼2.8% of probe                     REGISTERED
hosts ever update their user tags which may lead to user tags       5K
that tend to become stale over time. System tags on the other
                                                                     0
hand being automatically assigned and frequently updated (every
                                                                         2010    2011    2012     2013     2014        2015   2016    2017
4 hours) are stable and accurate. We show an application of
system tags by performing a vantage point selection of dual-
stacked probes. This exploration reveals that with ∼2.3K (∼26%)       NEVER CONNECTED                      2795                 13.44%
connected dual-stacked probes, RIPE Atlas provides the richest        CONNECTED                            9116                 43.86%
source of vantage points for IPv6 measurement studies. These          DISCONNECTED                         2265                 10.90%
dual-stacked probes span 88 countries and cover 822 ASNs.             ABANDONED                            6609                 31.80%
∼83% of these dual-stacked probes are connected within access
networks with 782 probes deployed at homes with native IPv6           REGISTERED                           20785                100.0%
connectivity. These home dual-stacked probes are evenly split
across DSL, cable and fibre deployments. We show that IPv6        Fig. 1. Evolution of RIPE Atlas probes by their connection status. The plot
latencies from these probes to RIPE Atlas anchors appear          is generated using the probe archive API [1] which provides probe metadata
comparable to IPv4, although IPv4 performs marginally better.     since Mar 2014. The API was updated to also report the status information
                                                                  of each probe starting Sep 2014. ∼9.1K probes are connected out of ∼20.7K
By applying a correlation against APNIC IPv6 user population
                                                                  registered probes as of Jan 2017.
estimate, we further reveal underrepresented countries (such as
BE and JP) which would benefit from deployment of more probes
for IPv6 measurement studies.
                                                                  tags are subdivided into system and user tags. The system
                     I. I NTRODUCTION                             tags are tags automatically applied by RIPE Atlas based on
   RIPE Atlas [2], [3] consists of ∼9.1K (as of Jan 2017)         results collected from built-in (see Table I) measurements. In
hardware probes connected all around the globe as shown           addition to system tags, hosts can also voluntarily tag their
in Fig. 1. These probes perform active measurements (see          own probes using user tags. A capability to filter vantage point
Table I) to ascertain the network performance of the global       selection based on these tags was recently (starting Oct 2014)
Internet. A majority of these probes are running measurements     made available. The system tags being directly derived from
either from the core or from within access networks. A            measurements and being frequently updated (every 4 hours)
discernible number of probes are also hosted by volunteers        are fairly stable and accurate. The accuracy of user tags on the
within their home network. RIPE Atlas provides public APIs        other hand is largely dependent on the proactive participation
[4], [1], [5] (starting Feb 2013) to programmatically provision   of hosts to not only tag, but also update their tags as and when
measurements on these probes. However the probe selection         network environments around the probe change. This may
(until recently) was limited to either geographic-based (using    therefore lead to stale user tags that do not reflect the current
latitude and longitude) or network origin-based (using network    network situation of the probe. In this paper, we provide 4
prefixes) filters. In order to cope with this limitation, RIPE    main contributions −
Atlas has introduced (starting July 2014) a tagging mechanism        − We show that system tags (see Section III) have im-
[6] that allows tags to be applied on individual probes. These         proved the vantage point selection process by exhibiting
                             TABLE I                              with a goal to assess broadband performance of end-users.
    A LIST OF BUILT- IN MEASUREMENTS PERFORMED BY PROBES BY       SamKnows started in 2008 and consists of ∼70K hardware
   DEFAULT AS OF JAN 2017. (*) IN THE TARGET INDICATE MULTIPLE
                   SERVERS WITHIN THE DOMAIN .                    probes. BISmark [10] is an academic initiative by researchers
                                                                  at Georgia Tech. The goal is to build a platform which is
 MEASUREMENT       TARGET                                         similar to that of SamKnows. It started in 2010 and consists
                                                                  of ∼420 hardware probes deployed around the globe. perf-
 ping, ping6       first hop, second hop (derived                 SONAR [3] is a collaborative initiative to build a performance
                   from traceroute measurements),                 monitoring framework that can identify and isolate problems
                   *.root-servers.net,
                   *.atlas.ripe.net                               in network paths that are used for scientific data exchange.
 traceroute,
                                                                  perfSONAR is supported by ESnet, Internet2, GÉANT and
                   *.root-servers.net,
 traceroute6       *.atlas.ripe.net,                              RNP academic networks. Netradar [11] and Portolan [12] are
                   topology4.dyndns.atlas.ripe.net,               emerging mobile measurement platforms. We further refer the
                   topology6.dyndns.atlas.ripe.net,
                   labs.ripe.net
                                                                  reader to surveys [3], [13] that discuss these performance
                                                                  measurement platforms in greater detail.
 dns, dns6         *.root-servers.net: TCP (SOA),
                   UDP (SOA, version.bind,                           RIPE Atlas with ∼9.1K hardware probes (as of Jan 2017)
                   hostname.bind, id.server,                      is the largest open platform today. It plays a critical role
                   version.server)                                in not only providing operational support to network oper-
 sslcert,          www.ripe.net, atlas.ripe.net                   ators but also facilitating measurement-based research. Few
 sslcert6                                                         studies have used RIPE Atlas for measuring IPv6 networks.
 http, http6       www.ripe.net/favicon.ico,                      For instance, Emile Aben in [14] (2013) using a sample of
                   ip-echo.ripe.net                               ∼1K RIPE Atlas probes show that ∼10% of these probes
                                                                  have fragmentation problems in IPv6. Andra Lutu et al. [15]
                                                                  (2014) run traceroute from ∼100 RIPE Atlas probes to
     a case study on selecting ∼2.3K (∼26%) dual-stacked          measure reachability of IPv6 prefixes. They show that IPv6
     probes.                                                      limited visibility prefixes are generally reachable, however
   − Our region-based analysis (see Section IV) reveals that      dark visibility prefixes are largely not. Jen Linkova in [16]
     dual-stacked probes span 88 countries with ∼91% of           use a sample of ∼1K RIPE Atlas probes to show that packets
     probes concentrated in the RIPE and ARIN region. A           with IPv6 extension headers are often dropped in the Internet.
     correlation against APNIC IPv6 user population estimate      Rodérick Fanou et al. in [17] (2015) use RIPE Atlas probes
     reveals underrepresented countries (such as BE and JP)       to study the state of interdomain routing in Africa. They
     which would benefit from deployment of more probes           observed that IPv6 penetration is largely concentrated in South
     for IPv6 measurement studies.                                Africa with all measured continental IPv6 paths traversing
   − Our network-based analysis (see Section V) reveals           ZA. We take this further and profile all dual-stacked RIPE
     that probes span 822 ASNs with ∼83% of dual-stacked          Atlas probes. This helps us to not only identify the possible
     probes connected within access networks. We show             network−based and region−based bias that comes with using
     that 782 dual-stacked probes are connected in home           dual-stacked probes for IPv6 measurement studies but also
     networks with an even split across DSL, cable and fibre      identify underrepresented areas to help remove this bias.
     deployments. IPv6 latencies from these probes to RIPE
     Atlas anchors appear comparable to IPv4, although IPv4                            III. S YSTEM TAGS
     performs marginally better.                                     System tags are automated tags generated by the RIPE
   − Our exploration of user tags reveals that only ∼2.8% of      Atlas system. Fig. 2 shows the timeseries of top ten
     probes hosts ever update their user tags (see Section VI)    system tags sorted by the number of connected probes.
     which may lead to user tags that tend to become stale        These system tags highlight the state of DNS (such as
     over time.                                                   system-resolves-a-correctly et al.) and the state
                                                                  of IP connectivity (such as system-ipv6-works et al.)
          II. BACKGROUND AND R ELATED W ORK                       of the vantage point and are based on insights derived
   We provide a brief survey on performance measurement           from continuous built-in measurements (see Table I) per-
platforms that exist today. Archipelago (Ark) [7] is a platform   formed by the probes. Fig. 3 shows the distribution of
developed by CAIDA that uses monitors in coordination to          all system tags across connected probes as of Jan 2017.
map the topology of the Internet. Ark started in 2007 and         In order to provide increased protection against spoofing
consists of ∼170 hardware monitors as of Jan 2017. DIMES          attacks, special-case tags are applied on probes (such as
[8] (a software agent) and iPlane [9] (an overlay on top          system-resolver-mangles-case) whose resolver im-
of existing infrastructures) are platforms that coexist with      plements case mangling of DNS requests [18]. Similarly,
Ark and have a similar goal of mapping the topology of            system-dns-problem-suspected is set when only IP-
the Internet. SamKnows [3] on the other hand is a platform        level connectivity (with no DNS activity) is observed while
developed in close collaboration with ISPs and regulators         the tag system-firewall-problem-suspected is set
                                                                        RIPE Atlas Probes
10K




                                                                                                      TAGS
  8K                system-ipv4-capable                              system-v3
                    system-ipv4-works                                system-ipv6-capable
  6K
                    system-resolves-a-correctly                      system-ipv6-works
  4K
                    system-resolves-aaaa-correctly                   system-v2
  2K                system-ipv4-rfc1918                              system-v1
   0
          2010                2011                2012                2013                2014                2015                2016                2017

Fig. 2. Time series of top 10 system tags sorted by the number of connected probes. Popular system tags help identify the probe hardware and highlight the
state of DNS and IP connectivity of probes.



             system-ipv4-capable                     9045                                        Connected, Non-Anchored Probes
               system-ipv4-works                    8743
     system-resolves-a-correctly                  8305
                                                                                 10K




                                                                                                                            TAGS
                                                                                                                             API
  system-resolves-aaaa-correctly                  8236                                              all
             system-ipv4-rfc1918               6715
                       system-v3
                                                                                  8K                dual-stacked
                                               6660
             system-ipv6-capable         3640
               system-ipv6-works       3050
                                                                                  6K      10K
                       system-v2    1427
                       system-v1 767
                                                                                           8K
         system-ipv6-doesnt-work 501
                                                                                           6K
                                                                                  4K       4K
                 system-ipv6-ula 433
    system-resolver-mangles-case 407                                                       2K
                   system-anchor 234                                                        0
                                                                                  2K              05 09 01 05 09 01 05 09 01
          system-auto-geoip-city 160
      system-doesnt-resolve-aaaa 142                                                             2014 2015 2016
         system-doesnt-resolve-a 75                                                 0
         system-ipv4-doesnt-work 63
       system-auto-geoip-country 47                                                     2010 2011 2012 2013 2014 2015 2016 2017
        system-flakey-connection 7
   system-resolves-a-incorrectly 1
    system-dns-problem-suspected 1                                              Fig. 4. Evolution of connected dual-stacked probes. The plot is generated
system-resolves-aaaa-incorrectly 1                                              using the probe archive API [1] which provides probe metadata since March
                                0     3K    6K    9K      12K                   2014. The API reports probe tags starting August 2014. Around 25.99% (2301
                                                  # (Probes)                    / 8855) of all connected non-anchored probes are dual-stacked as of Jan 2017.


Fig. 3. Distribution of connected probes based on system tags as of Jan 2017.
                                                                                as probes with the same ASN over IPv4 and IPv6. This
                                                                                condition allows us to filter out hosts that use a 6in4 (such
when only DNS activity is visible. Given RIPE Atlas consists                    as Hurricane Electric) tunnel [22] for IPv6 connectivity. This
of three versions (v1, v2, and v3) of hardware probes and                       is useful to ensure only probes with native IPv4 and IPv6
anchors (which are dedicated servers that are used as sinks of                  connectivity are used for studies such as comparing IPv4
measurement traffic to measure connectivity and reachability                    and IPv6 latencies to services over the Internet. We further
of a region), system tags (such as system-v1 et al.) are also                   only consider probes dual-stacked when they are tagged with
provided to allow hardware-based calibration of the probes.                     system-ipv4-works and system-ipv6-works tags.
Using such a calibration, we were able to discover [19] (2015)                  The system evaluates each probe every 4 hours for all system
that older versions of the probes experience load issues due to                 tags by inspecting results obtained from built-in (see Table
their hardware limitations. This observation has been further                   I) measurements. For instance, Stéphane Bortzmeyer in [23]
confirmed [20] (2015) to show that these delays are more                        (2013) has shown that using a sample of 1K RIPE Atlas
pronounced in situations where older version of probes are                      probes, 10% of the probes believe to have IPv6 connectivity
loaded with concurrent measurements.                                            but fail when IPv6 measurements are provisioned on them.
   John P. Rula et al. in [21] (2015) recently performed a                      He went further in [24] (2014) to show that using a sample of
factor analysis of the stratified sampling process used in the                  500 RIPE Atlas probes, only ∼60% of the probes are behind
SamKnows / FCC Broadband America study. They moti-                              resolvers that can resolve DNS names that are served by IPv6-
vated towards an approach that takes network and region                         only nameservers. These studies were one of the triggers that
based diversity into account to maintain the integrity of the                   resulted in the introduction of system-ipvX-works tags.
sampling process. In this pursuit, using tag assisted vantage                   By using *-works instead of *-capable, such measure-
point selection we explore the region− and network−based                        ments tend to have more useful results. As such, the presence
diversity of connected dual-stacked probes within the RIPE                      of these tags allow us to ensure selected dual-stacked probes
Atlas platform. Fig. 4 shows the evolution of dual-stacked                      are in fact able to reach out to services over both IPv4 and
probes using these system tags. We define dual-stacked probes                   IPv6 on the Internet. As can be seen ∼25.99% (2301 / 8855) of
                                                                                                          Dual-Stacked Probes OTHERS
                                                                                                                                  DE
                                                                                                                                                                      343
                                                                                                                                                                         489
                                                                                                                                                            US       304
                                                                                                    500




                                                           1489
                                                                                                                                                            FR      248




                                                                       1500
                                                                                                                                                            GB    161
                                                                                                                                                            NL    151
                                                                                                    400




                                                                          # (3rREes)
                                                                                                                                                            CH 88




                                                                                       # (Probes)
                                                                                                                                                            BE 65




                                                                       1000
                                                                                                                                                            CZ 53
                                                                                                    300                                                     RU 51
                                                                                                                                                            CA 44
                                                                                                                                                            NO 42




                                                                       500
                                                                                                    200                                                     AT 33




                                                                      303
                                                                                                                                                            FI 32




                                                             A31IC 106
                                                                                                                                                            GR 32
                                                                                                    100




                                                            LAC1IC 30
                                                           A)5I1IC 30
                                                                                                                                                            JP 31
                                                                                                                                                            SE 31




                                                                   0
                                                              5I3(
                                                              A5I1
                                                                                                                                                            IT 31
                                                                                                     0                                                      AU 25
                                                                                                                                                            DK 24
                                                                                                                                                            SI 23
                                                                                                          0      20      40      60      80                    0 200 400 600
Fig. 5. RIR-based distribution of dual-stacked probes. The plot is generated                    Browser market shares.
                                                                                                         Country       January, 2015 to
                                                                                                                    Rank              # May, 2015
                                                                                                                                        (Probes)
using the RIPE Atlas Probe API [4] and RIPE Data API [25]. ∼91% of                                        Click the slices to view versions. Source: netmarketshare.com.
dual-stacked probes are connected within the RIPE and ARIN region.
                                                                                                                                                 IT: 1.3%

                                                                                                                                                            SE: 1.3%
                                                                                                            DE: 21.3%
all connected and non-anchored probes are dual-stacked as of                                                                                                     GR: 1.4%

Jan 2017. To put numbers into perspective, this is more than                                                                                                           FI: 1.4%

the number of CAIDA Ark [7] dual-stacked probes (77 out                                                                                                                  AT: 1.4%

of 170 as of Jan 2017) with native IPv6 connectivity. We use                                                                                                              NO: 1.8%

this definition of dual-stacked probes in the rest of the paper.                                                                                                           CA: 1.9%

                                                                                                                                                                           RU: 2.2%
                  IV. IP V 6 P ROBES BY R EGION
                                                                                       OTHERS: 14.9%                                                                       CZ: 2.3%
   In order to study IPv6 probes by region, we use the RIPE                                                                                                               BE: 2.8%
Data API [25] to map the IP endpoint used by each dual-                                                                                                                CH: 3.8%
stacked probe to the RIR that allocated the encompassing                                                                                                          NL: 6.6%
prefix of the IP endpoint resource. The registration information                                                                                              GB: 7.0%
is derived from each RIR’s WHOIS [26] service. Using                                                             US: 13.2%
                                                                                                                                                   FR: 10.8%
this mapping we cluster the probes by RIR region. Fig. 5                                                                                                                              Highcharts.com

shows this RIR-based distribution of dual-stacked probes.                              Fig. 6. Country-based distribution of dual-stacked probes. The plot is
It can be seen that ∼91% of the dual-stacked probes are                                generated using the RIPE Atlas Probe API [4]. The countries are ranked
                                                                                       by the number of deployed probes. 88 countries are covered by dual-stacked
connected within the RIPE and ARIN region. We further used                             probes. The entire list is made available at: http://goo.gl/UdEe1Q
the RIPE Atlas Probe API [4] to split the RIR region by
country. This country information is provided by probe hosts
during initial registration. The system also uses geolocation                          with a large IPv6 userbase that have a small fraction of dual-
services in case the user does not provide this informa-                               stacked probes. For instance, it can be seen that JP with ∼19%
tion. For instance, the system-auto-geoip-country                                      IPv6 usage ratio and ∼22M IPv6 users serve only ∼1.4%
and system-auto-geoip-city system tags are used                                        (31/2301) dual-stacked probes. We hope this analysis will help
specifically for this purpose. These system tags are overidden                         improve the deployment of probes in such underrepresented
when a user manually geolocates the probe. Fig. 6 shows this                           countries with a large IPv6 userbase.
country-based distribution of dual-stacked probes. As can be
seen, a large number of dual-stacked probes are connected in                                                    V. IP V 6 P ROBES BY N ETWORK
Germany, US, France, Netherlands and UK. However, even                                    We further used the RIPE Atlas Probe API [4] to cluster
though probes span 88 countries, some countries with a large                           the dual-stacked probes by their origin AS. Fig. 8 shows
IPv6 userbase serve only a small fraction of dual-stacked                              this AS-based distribution of dual-stacked probes. Using this
probes. For instance, we know that Belgium with ∼48.5%                                 information with the country-based distribution (see Fig. 6),
penetration is currently leading IPv6 adoption rates (as of                            it can be seen which service providers contribute to the large
Jan 2017) according to Google IPv6 adoption statistics [27].                           fraction of probes within the top countries. For instance, dual-
However, it does not even fall within the top 5 countries                              stacked probes within Germany are largely represented by
with the largest number of dual-stacked probes. As such,                               Deutsche Telekom and Kabel Deutschland. Similarly Comcast
the probe deployment likely does not reflect the dual-stacked                          has high representation within US, Proxad within France and
user population across the globe. Using the APNIC dataset                              XS4ALL within Netherlands.
[28], we performed a correlation (see Fig. 7) of percentage                               Selecting ISPs: Although Fig. 8 shows that top ASes
of dual-stacked probes against the percentage of IPv6 user                             hosting the highest number of probes are ISPs, it must also
population. An associated table shows the top 10 countries                             be noted that not all probes are deployed in service provider
                                                                                                                                                      DTAG (AS3320)         181
         IPv6 Penetration                         USERS        PROBES
                                                                                                   Dual-Stacked Probes                            COMCAST (AS7922)          169
70%                                                                                        200
                                                                                                                                                  PROXAD (AS12322)
                                                                                                                                                   XS4ALL (AS3265)
                                                                                                                                                                         96
                                                                                                                                                                        71
                                                                                                                                                   AS3215 (AS3215)      71
60%                      Probes            BE     57.4%           2.8%                                                                                 LGI (AS6830) 32
                                                                                                                                      KABELDEUTSCHLAND (AS31334) 32
                                           LU     34.2%           0.6%                     150
50%                      Users                                                                                                                   AS20712 (AS20712) 28




                                                                              # (Probes)
                                                                                                                                                    BSKYB (AS5607) 27
                                           GR     33.7%           1.4%
40%                                                                                        100
                                                                                                                                                 BELGACOM (AS5432) 25
                                                                                                                                                 SWISSCOM   (AS3303) 23
                                           CH     34.3%           3.8%                                                                            TELENET (AS6848) 21
30%                                        PT     29.2%           0.7%                                                                                 ATT (AS7018) 19
                                                                                                                                                   INIT7 (AS13030) 14
20%                                        IN     22.0%           0.1%                      50                                                 NETCOLOGNE (AS8422) 13
                                                                                                                                                      ZEN (AS13037) 13
                                                                                                                                                  SEACOM (AS37100) 11
10%                                        US     33.2%          13.2%                                                                                MNET (AS8767) 11
                                                                                             0                                               ROADRUNNER (AS20001) 11
 0%                                        EC     18.8%           0.1%                          Browser market
                                                                                               100      101
                                                                                                                      shares. January, 2015 to May,
                                                                                                                     102
                                                                                                                                                  TELENOR         2015
                                                                                                                                                            (AS2119)  11
                                                                                                                                                                    0     200
       0    20 40 60 80                    DE     39.9%          21.3%                              Click the slices to view versions. Source: netmarketshare.com.
                                                                                                            ASN Rank                                              # (Probes)
            Country Rank                   JP     19.8%           1.4%                                                       ATT: 0.9%

                                                                                                              TELENET: 1.0%

                                                                                                       SWISSCOM: 1.1%
Fig. 7. Correlation (left) of percentage of IPv6 users against dual-stacked
                                                                                                    BELGACOM: 1.1%
RIPE Atlas probes by country. The countries are ranked by the percentage
of IPv6 users as of Jan 2017. The estimation of number of IPv6 users is                                BSKYB: 1.2%

available from APNIC dataset [28]. A delta comparison (right) reveals the                              A&A: 1.3%

top 10 countries with a large IPv6 userbase that would benefit from more       KABELDEUTSCHLAND: 1.5%
deployment of dual-stacked probes.                                                                      LGI: 1.5%
                                                                                                                                                                   OTHERS: 49.6%
                                                                                                   ORANGE: 3.2%

                                                                                                      XS4ALL: 3.2%

                                                                                                       PROXAD: 4.4%
networks. From the perspective of vantage point selection, it
                                                                                                        COMCAST: 7.7%
is essential to be able to select probes deployed in a specific                                                     DTAG: 8.3%
type of a network that spans multiple ASes and countries.
                                                                                                                                                                       Highcharts.com
We therefore, searched the literature for techniques that can
classify ASes by network type. Xenofontas Dimitropoulos                       Fig. 8. AS-based distribution of dual-stacked probes. The plot is generated
                                                                              using the RIPE Atlas Probe API [4]. The ASNs are ranked by the number of
et al. in [29] (2006) apply machine learning techniques to                    deployed probes. A large number (822) of ASNs are covered by dual-stacked
classify ASes into six categories: a) large ISPs, b) small                    probes. The entire list is made available at: http://goo.gl/bR5JEd.
ISPs, c) customer networks, d) universities, e) IXPs, and
f) NICs. They use data from CAIDA Ark [7], RouteViews,
and Internet Routing Registry (IRR). This study however is                    Measurements were performed using the ICMP Paris probing
dated. PeeringDB [30] which is a database holding peering                     method [31] implemented in the evtraceroute busybox
information of participating networks serves as a living, viable              applet within the platform. We define residential probes as
alternative today. Aemen Lodhi et al. in [30] show that the                   probes that are directly wired to the home gateway. In order
information maintained within this database is reasonably                     to achieve this, we searched for probes whose hop1 was in
representative of network operator peering and is also up-                    a private IPv4 address space [32], but hop2 was in a public
to-date. Therefore we used PeeringDB to map ASes hosting                      IPv4 address space. This criteria eliminates the situation where
dual-stacked probes by their network type information. Not                    the service provider uses a private address space within the
all ASes hosting dual-stacked probes could be mapped to a                     access network unless a probe is situated at the edge of last-
network type due to missing AS information encompassing                       mile. This also ensures we do not incorrectly classify a probe
∼19.3% (443 / 2301) dual-stacked probes (as of Jan 2017) in                   connected to business lines (which likely crosses multiple hops
the PeeringDB database. Fig. 9 shows the evolution of dual-                   of private addresses before reaching out through the main
stacked probes by network type. It can be seen that ∼83%                      router) as a residential probe. It is possible that there may
(1540 out of 1858) of the dual-stacked probes are deployed in                 be home probes that are connected to multiple layers of NAT.
service provider networks. As a result, the RIPE Atlas platform               It’s also possible that some (although a smaller fraction) home
is a potential platform for measuring native IPv6 performance                 probes may not be connected to any NAT. The heuristic will
delivered by service provider networks.                                       filter out these situations, however, note that this maybe an
   Selecting Residential Probes: Furthermore, not all dual-                   accepted tradeoff since it will more affect the coverage and
stacked probes that mapped to a service provider network are                  less likely the accuracy of inferred residential probes. Fig. 10
particularly deployed within a home network, but may also be                  shows the fraction (∼60.5%) of residential dual-stacked (782)
hosted deep within access or backbone network of a service                    probes deployed in service provider networks.
provider. In order to identify residential probes, we used the                    Categorizing Residential Probes by Access Technology:
RIPE Atlas measurement creation API [5] to provision one-                     We further classify residential dual-stacked probes into DSL,
off traceroute measurements towards RIPE Atlas anchors.                       cable and fibre service providers. UPnP discovery messages
We created separate measurements for each ISP in order to                     can be used to reveal access technology used on the WAN
cycle through all available target anchors. This allowed us to                interface of a home gateway. Lucas DiCioccio et al. [33] use
evenly distribute the measurement load inside the platform.                   netalyzr [34] to send Universal Plug and Play (UPnP) dis-
                                                  Dual-Stacked Probes                                                                     Anchoring Measurements




                                                                                                           # (Observations)
                          104
                                        ISP/NSP
                                                                                                                              7M
             # (Probes)




                                                                    TAGS
                          103           CONTENT PROVIDERS
                                                                                                                              6M
                                                                                                                              5M
                                        EDUCATIONAL/RESEARCH
                                                                                                                              4M        IPv4 faster            IPv6 faster
                          102           NON-PROFITS
                                                                                                                              3M
                                        ENTERPRISE                                                                            2M
                          101                                                                                                 1M
                                2010   2011   2012    2013   2014          2015    2016    2017                                0
                                                                                                                                   −3    −2    −1    0     1          2       3
                                ISP/NSP                             1540               83.0%
                                                                                                                                              (slow-fast)/fast
                                CONTENT PROVIDERS                   139                 7.5%
                                EDUCATION/RESEARCH                  110                 6.0%
                                                                                                       Fig. 11. 5th percentile comparison of latencies over IPv4 and IPv6 from
                                NON-PROFITS                         45                  2.4%           2941 RIPE Atlas probes to 149 RIPE Atlas anchors using a month-long
                                ENTERPRISE                          21                  1.1%           (Sep-Oct 2015) dataset consisting of 20M data points. The latencies appear
                                                                                                       comparable, although IPv4 tends to show marginally better performance. The
            Fig. 9. Evolution of dual-stacked probes by network type as mapped by                      raw dataset is available at: http://goo.gl/dOJL5Q
     Browser  market
          PeeringDB    share,
                    [30].        January,
                          An associated table 2015    tonumber
                                              shows the  May, (and
                                                               2015fraction) of
            dual-stacked probes within each network type as of Jan 2017. ∼83% of dual-
            stacked probes Source: netmarketshare.com
                           are connected  within service provider networks.
                                                                                                       measurement studies from home networks.
                                                                                                          Example: Measuring IPv6 Performance: A practical ap-
                                                                   DSL: 20.26%                         plication of using these dual-stacked probes is to determine
                                                                                                       performance of IPv6 relative to IPv4. We use these dual-
                                                                                                       stacked probes to measure IPv6 performance towards RIPE
                                                                                                       Atlas anchors. We used a month-long dataset of ping mea-
NKNOWN: 39.52%
                                                                                                       surements provisioned towards 149 anchors. Fig. 11 shows
                                NON-RESIDENTIAL                                                        the 5th percentile latency comparison between IPv4 and IPv6.
                                                                                  CABLE: 11.45%
                                                                                                       The 5th percentile was used to illustrate the best case sce-
                                                     RESIDENTIAL                                       nario. It can be seen that IPv4 and IPv6 latencies between
                                                                                                       RIPE Atlas probes and RIPE Atlas anchors are comparable,
                                                                                                       although relative performance in IPv4 still seems marginally
                                                                                                       better. It should be noted that this measurement carries the
                                                                    FIBRE: 13.84%
                                                                                                       region−based (see Section IV) and network−based (see Sec-
                                                                                                       tion V) bias of deployed probes and may miss observations
                     UNKNOWN: 14.93%                                                                   from some countries (see Fig. 7) with a large IPv6 userbase.
                                                                                          Highcharts.com


            Fig. 10. Distribution of dual-stacked probes deployed in service provider                                                         VI. U SER TAGS
            networks. ∼60.5% (782) of probes are wired to a home gateway. Amongst
            residential probes, ∼20.26% (262) are connected to DSL, ∼11.45% (148) are                     In addition to system tags, RIPE Atlas also allows probe
            connected to cable while ∼13.84% (179) are connected to fibre networks.                    hosts to tag their own probes with additional tags. Given the
                                                                                                       sample space of words that can be used for user tags is large,
                                                                                                       the visibility of user tags is set to private by default. This
            covery messages to home gateways. They show how responses                                  allows the system to not automatically offer the tag words to
            from these queries can reveal access technology used on the                                other users. The RIPE Atlas team periodically checks newly
            WAN interface. The measurements were performed on 120K                                     entered user tags and approves the ones that seem to be of
            homes in 2012, but only 35% of the gateways were found                                     general use. The approved user tags are then made available
            UPnP enabled. 10% of the gateways were connected further to                                to other users. RIPE Atlas also periodically sanitizes the word
            a modem device, while 3% of the homes had more than one                                    space by merging similar tags. For instance, administrators can
            UPnP gateway. Even more, UPnP responses are not always                                     merge v6-tunnel, ipv6-tunnel and tuneled-ipv6
            accurate. In any case, since RIPE Atlas probes currently do                                into one user tag. This ultimately helps achieve sane vantage
            not support a measurement that can perform UPnP queries and                                point selection for the large number of probes supported by
            since this technique has been proven to be unreliable [33],                                the system. Fig. 12 shows the distribution of these user tags
            we instead rely on user tags (see Section VI) to categorize                                across connected probes. It is worth noting that a large number
            residential dual-stacked probes by the access technology used                              of probes did benefit in the beginning when some of these user
            by the home gateway. Fig. 10 shows the split distribution of                               tags (such as nat) were automatically applied to probes to
            residential dual-stacked probes by access technology. It can                               initially seed the system. Fig. 13 shows the timeseries of top
            be seen that this being an even split of dual-stacked probes                               10 user tags sorted by the number of connected probes. As can
            across access technology can serve as a good sample for IPv6                               be seen popular user tags (nat, no-nat, home, dsl,
                        nat                 3934                                                           RIPE Atlas Probes
                                                                            104
                       home           2459




                                                                                                                              TAGS
                                                                                           nat              cable
                       ipv4        1583                                     103
                                                                                           home             ipv6
                     no-nat       1410                                      102            ipv4             dsl
                      fibre      1061                                                      no-nat           native-ipv6
                      cable     865                                         101
                                                                                           fibre            office
                       ipv6     843                                         100
                        dsl     789                                                2010    2011     2012     2013      2014          2015   2016   2017
                native-ipv6    746
                     office    646
                 datacentre    636                                          Fig. 13. Time series of top 10 user tags sorted by the number of connected
                                                                            probes. Popular user tags are centered around home probes.
                native-ipv4   469
                ipv6-tunnel 300
                       core 298
                 multihomed 244                                                                             Probes: 15.8K
                       adsl 222                                                    1.0




                                                                                                                                                   ['14-'17]
                   academic 202                                                    0.8
                       vdsl 166                                                    0.6




                                                                             CDF
                                                                                                                                            sys
                      vdsl2 159                                                    0.4
                        isp 145                                                    0.2                                                      user
                    comcast 111                                                    0.0
iwantbcp38compliancetesting 90
                       dtag 65                                                               0       50   100   150   200  250
               wireless-isp 64                                                                    Frequency of Tag Updates
                         he 60
                        ixp 51
          known-ipv6-issues 48                                              Fig. 14. Frequency of tag changes over time. ∼2.8% of probe hosts ever update
                 double-nat 46                                              their user tags. On the other hand more than half of the probes (∼61.4%)
                        noc 44                                              received at least one update on system tags with ∼13.1% of probes receiving
                        vpn 42                                              atleast 10 updates. Whenever user tags are changed, more tags are added /
                        upc 42                                              deleted (upto 7 tags changed at once) when compared to system tags.
                       6to4 39
                      sixxs 38
                        6rd 30                                              dependent on the proactiveness of the host. Even though this
                        lte 30
                    ds-lite 27                                              is not expected to happen often, the host needs to update probe
                       free 26                                              tags as and when network conditions change. For instance, in
          known-ipv4-issues 26                                              situations where a host forgets to change a tag due to change in
                         4g 25                                              either service subscription or even worse moving the probe to a
                     xs4all 24
                     mobile 24                                              new location, vantage point selection based barely on user tags
                hackerspace 22                                              would lead to entirely different measurement results. Fig. 14
                        twc 21                                              compares the frequency of tag (user and system) changes over
                        cgn 20                                              time. It can be seen that only ∼2.8% of probes received any
                       fios 19
                     orange 13                                              updates on their user tags. As such, we introduce the notion
                         3g 12                                              that user tags tend to become stale over time. In the future we
                  satellite 10                                              plan to associate a tag creation timestamp to allow a predictive
                   freifunk 9                                               weighting of user tag accuracy. Furthermore, we plan to utilise
                      wimax 9
                       dn42 7                                               built-in measurements to identify if a user-tag is plausible and
                       ftth 6                                               contact volunteers in situations where there is suspicion on the
                  internet2 6                                               accuracy of a user tag.
                      nat64 6
                       fttc 5
                      ziggo 5
                                                                                                      VII. C ONCLUSION
                            0      2K      4K                                  We showed that probe hosts do not update their user tags
                                               # (Probes)                   frequently which may lead to user tags that tend to become
                                                                            stale over time. System tags on the other hand refresh every
Fig. 12. Distribution of connected probes based on tags manually assigned   4 hours and are therefore stable and accurate. We showed
by probe hosts as of Jan 2017.
                                                                            the utility of system tags by performing a region−based and
                                                                            network−based vantage point selection of dual-stacked probes.
                                                                            Although some regions and networks with a large number of
cable, fibre) are centered around probes deployed in                        probes can produce a sampling bias, the exploration revealed
residential settings.                                                       that RIPE Atlas provides the richest source of vantage points
   Although system tags being generated directly by the RIPE                (∼2.3K) for IPv6 measurement studies. This exploration also
Atlas platform are stable, the accuracy of user tags is largely             helped us identify underrepresented regions (such as BE and
JP) with a large IPv6 user base that can benefit from increased                 [18] P. Vixie and D. Dagon, “Use of Bit 0x20 in DNS Labels to
deployment of probes.                                                                Improve Transaction Identity,” IETF, Internet-Draft draft-vixie-dnsext-
                                                                                     dns0x20-00, Mar. 2008. [Online]. Available: http://tools.ietf.org/html/
                                                                                     draft-vixie-dnsext-dns0x20-00
                   VIII. ACKNOWLEDGEMENTS                                       [19] V. Bajpai, S. J. Eravuchira, and J. Schönwälder, “Lessons Learned
                                                                                     From Using the RIPE Atlas Platform for Measurement Research,”
  This work was partly funded by Flamingo, a Network of                              ser. Computer Communication Review (CCR) ’15, 2015, pp. 35–42.
                                                                                     [Online]. Available: http://doi.acm.org/10.1145/2805789.2805796
Excellence project (ICT-318488) supported by the European                       [20] T. Holterbach, C. Pelsser, R. Bush, and L. Vanbever, “Quantifying
Commission under its Seventh Framework Programme. We                                 Interference between Measurements on the RIPE Atlas Platform,” ser.
would also like to thank Philip Homburg (RIPE NCC) for                               ACM SIGCOMM Internet Measurement Conference (IMC) ’15, 2015.
                                                                                     [Online]. Available: http://doi.acm.org/10.1145/2815675.2815710
providing us support on the RIPE Atlas mailing list.                            [21] J. P. Rula, Z. S. Bischof, and F. E. Bustamante, “Second Chance:
                                                                                     Understanding diversity in broadband access network performance,”
                             R EFERENCES                                             ser. SIGCOMM Workshop on Crowdsourcing and Crowdsharing
                                                                                     of Big (Internet) Data C2B(I)D ’15, 2015. [Online]. Available:
                                                                                     http://doi.acm.org/10.1145/2787394.2787400
 [1] “RIPE Atlas - Probe Archive API: v2,” https://atlas.ripe.net/api/v2/       [22] S. Steffann, I. van Beijnum, and R. van Rein, “A Comparison
     probes/archive, [Online; accessed 25-Jan-2017].                                 of IPv6-over-IPv4 Tunnel Mechanisms,” RFC 7059 (Informational),
 [2] “RIPE Atlas: A Global Internet Measurement Network,” ser. Internet              Internet Engineering Task Force, Nov. 2013. [Online]. Available:
     Protocol Journal (IPJ) ’15, September 2015, http://ipj.dreamhosters.com/        http://www.ietf.org/rfc/rfc7059.txt
     wp-content/uploads/2015/10/ipj18.3.pdf.                                    [23] “S. Bortzmeyer - How Many RIPE Atlas Probes Believe They Have IPv6
 [3] V. Bajpai and J. Schönwälder, “A Survey on Internet Performance                 (But Are Wrong)?” https://goo.gl/7MoirH, [Accessed: 04-Apr-2016].
     Measurement Platforms and Related Standardization Efforts,” ser. IEEE      [24] “S. Bortzmeyer - How Many RIPE Atlas Probes Can Resolve IPv6-only
     Communications Surveys and Tutorials (COMST) ’15, 2015. [Online].               Domain Names?” https://goo.gl/3D89ha, [Accessed: 04-Apr-2016].
     Available: http://dx.doi.org/10.1109/COMST.2015.2418435                    [25] “RIPE Stat API,” https://stat.ripe.net, [Online; accessed 06-Nov-2015].
 [4] “RIPE Atlas - Probe API: v2,” https://atlas.ripe.net/api/v2/probes, [On-   [26] L. Daigle, “WHOIS Protocol Specification,” RFC 3912 (Draft
     line; accessed 25-Jan-2017].                                                    Standard), Internet Engineering Task Force, Sep. 2004. [Online].
 [5] “RIPE Atlas - Measurement Creation API: v2,” https://atlas.ripe.net/api/        Available: http://www.ietf.org/rfc/rfc3912.txt
     v2/measurements, [Online; accessed 25-Jan-2017].                           [27] “Google - IPv6 Adoption Statistics,” http://goo.gl/kKYXqS, [Online;
 [6] “RIPE Atlas - Update 2014,” https://labs.ripe.net/Members/fatemah_              accessed 22-Jan-2016].
     mafi/ripe-atlas-midsummer-update-2014, [Accessed: 04-Apr-2016].            [28] “APNIC - IPv6 users by country,” http://labs.apnic.net/dists/v6dcc.html,
 [7] kc claffy, “The 7th Workshop on Active Internet Measurements                    [Online; accessed 22-Jan-2016].
     (AIMS7) Report,” ser. Computer Communication Review (CCR) ’16,             [29] X. Dimitropoulos, D. Krioukov, G. Riley, and k. claffy, “Revealing the
     2016. [Online]. Available: http://doi.acm.org/10.1145/2875951.2875960           Autonomous System Taxonomy: The Machine Learning Approach,” ser.
 [8] Y. Shavitt and E. Shir, “DIMES: let the internet measure itself,” ser.          Passive and Active Measurement Conference (PAM) ’06, 2006.
     Computer Communication Review (CCR) ’05, vol. 35, no. 5, 2005.             [30] A. Lodhi, N. Larson, A. Dhamdhere, C. Dovrolis, and kc claffy,
     [Online]. Available: http://doi.acm.org/10.1145/1096536.1096546                 “Using peeringDB to understand the peering ecosystem,” ser. Computer
 [9] H. V. Madhyastha, T. Isdal, M. Piatek, C. Dixon, T. E. Anderson,                Communication Review (CCR) ’14, 2014, pp. 20–27. [Online].
     A. Krishnamurthy, and A. Venkataramani, “iPlane: An Information                 Available: http://doi.acm.org/10.1145/2602204.2602208
     Plane for Distributed Services,” ser. Symposium on Operating Systems       [31] B. Augustin, X. Cuvellier, B. Orgogozo, F. Viger, T. Friedman,
     Design and Implementation (OSDI) ’06, 2006, pp. 367–380. [Online].              M. Latapy, C. Magnien, and R. Teixeira, “Avoiding traceroute anomalies
     Available: http://www.usenix.org/events/osdi06/tech/madhyastha.html             with Paris traceroute,” ser. Internet Measurement Conference (IMC) ’06,
[10] S. Sundaresan, S. Burnett, N. Feamster, and W. de Donato, “BISmark:             2006. [Online]. Available: http://doi.acm.org/10.1145/1177080.1177100
     A Testbed for Deploying Measurements and Applications in Broadband         [32] Y. Rekhter, B. Moskowitz, D. Karrenberg, G. J. de Groot, and
     Access Networks,” ser. USENIX Annual Technical Conference (ATC)                 E. Lear, “Address Allocation for Private Internets,” RFC 1918,
     ’14, 2014, pp. 383–394. [Online]. Available: https://www.usenix.org/            Internet Engineering Task Force, Feb. 1996. [Online]. Available:
     conference/atc14/technical-sessions/presentation/sundaresan                     http://www.ietf.org/rfc/rfc1918.txt
[11] S. Sonntag, J. Manner, and L. Schulte, “Netradar - Measuring               [33] L. DiCioccio, R. Teixeira, M. May, and C. Kreibich, “Probe and
     the wireless world,” ser. International Symposium and Workshops                 Pray: Using UPnP for Home Network Measurements,” ser. Passive
     on Modeling and Optimization in Mobile, Ad Hoc and Wireless                     and Active Measurement Conference (PAM) ’12, 2012, pp. 96–105.
     Networks (WiOpt) ’13, 2013, pp. 29–34. [Online]. Available:                     [Online]. Available: http://dx.doi.org/10.1007/978-3-642-28537-0_10
     http://ieeexplore.ieee.org/xpl/freeabs_all.jsp?arnumber=6576402            [34] C. Kreibich, N. Weaver, B. Nechaev, and V. Paxson, “Netalyzr:
[12] A. Faggiani, E. Gregori, L. Lenzini, V. Luconi, and                             Illuminating the Edge Network,” ser. IMC ’10. [Online]. Available:
     A. Vecchio, “Smartphone-based crowdsourcing for network monitoring:             http://doi.acm.org/10.1145/1879141.1879173
     Opportunities, challenges, and a case study,” ser. IEEE Communications
     Magazine, vol. 52, no. 1, 2014, pp. 106–113. [Online]. Available:
     http://dx.doi.org/10.1109/MCOM.2014.6710071
[13] U. Goel, M. P. Wittie, K. C. Claffy, and A. Le, “Survey of End-
     to-End Mobile Network Measurement Testbeds, Tools, and Services,”
     ser. IEEE Communications Surveys and Tutorials, 2016. [Online].
     Available: http://dx.doi.org/10.1109/COMST.2015.2485979
[14] “Emile Aben - RIPE Atlas - Packet Size Matters,” https://goo.gl/
     CYWsZP, [Accessed: 04-Apr-2016].
[15] A. Lutu, M. Bagnulo, C. Pelsser, and O. Maennel, “Understanding
     the Reachability of IPv6 Limited Visibility Prefixes,” ser. Passive and
     Active Measurement (PAM), 2014, pp. 163–172. [Online]. Available:
     http://dx.doi.org/10.1007/978-3-319-04918-2_16
[16] “Jen Linkova - IPv6 Extension Headers Filtering Measurements with
     RIPE Atlas,” https://goo.gl/K1HozC, [Accessed: 04-Apr-2016].
[17] R. Fanou, P. François, and E. Aben, “On the Diversity of
     Interdomain Routing in Africa,” ser. Passive and Active Measurement
     Conference (PAM), 2015, pp. 41–54. [Online]. Available: http:
     //dx.doi.org/10.1007/978-3-319-15509-8_4
