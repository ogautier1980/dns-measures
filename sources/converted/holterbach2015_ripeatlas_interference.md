                Quantifying Interference between Measurements
                          on the RIPE Atlas Platform

     Thomas Holterbach                                   Cristel Pelsser                                  Randy Bush                  Laurent Vanbever
              ETH Zürich                            Internet Initiative Japan                       Internet Initiative Japan               ETH Zürich
     thomahol@ethz.ch                                   cristel@iij.ad.jp                                randy@psg.com               lvanbever@ethz.ch


ABSTRACT                                                                                            an impact on previous research results? This paper answers
Public measurement platforms composed of low-end hard-                                              these questions empirically for the RIPE Atlas platform.
ware devices such as RIPE Atlas have gained significant                                                By measuring the interference between our own measure-
traction in the research community. Such platforms are in-                                          ments (§3), we show that measurements do indeed interfere
deed particularly interesting as they provide Internet-wide                                         with each other, sometimes significantly. More particularly,
measurement capabilities together with an ever growing set                                          we found that user-induced interferences can impact two as-
of measurement tools. To be scalable though, they allow for                                         pects of measurements: precision and synchrony.
concurrent measurements between users. This paper answers                                              First, the precision of delay measurements (e.g., using
a fundamental question for any platform user: Do measure-                                           ping) performed either from or towards probes can be sig-
ments launched by others impact my results? If so, what can                                         nificantly impacted when other measurements are launched
I do about it?                                                                                      from or toward them (§4).
   We measured the impact of multiple users running exper-                                             Second, user-induced interferences can heavily desynchro-
iments in parallel on the RIPE Atlas platform. We found                                             nize experiments performed on multiple probes, even when
that overlapping measurements do interfere with each other                                          launched at the same time (§5).
in at least two ways. First, we show that measurements per-                                            Our key findings are as follows:
formed from and towards the platform can significantly in-                                          • The precision of measurements performed from and to-
crease timings reported by the probe. We found that increas-                                          wards the probe are impacted when other measurements
ing hardware CPU greatly helped in limiting interference on                                           use the probe at the same time. On older hardware, de-
the measured timings. Second, we show that measurement                                                lays increase by more than 1 ms in the median case and
campaigns can end up completely out-of-synch (by up to one                                            by more than 7 ms for the 95th percentile (Table 2).
hour), due to concurrent loads. In contrast to precision, we
found that better hardware does not help.                                                           • Measurements are very quickly desynchronized when other
                                                                                                      measurements are run in parallel. Under heavy load, com-
                                                                                                      pletion time may be delayed by close to 1 hour (Figure 8).
1.     INTRODUCTION
                                                                                                    • Upgrading the probe hardware significantly improves pre-
  Public measurement platforms composed of many low-end                                               cision levels, but does not help ensuring good synchro-
devices or probes, such as RIPE Atlas [1], are increasingly                                           nization levels (§5).
used by researchers and network operators. In addition to
measure network performance [2, 3, 4], these platforms are                                          • Previous research results, as well as the RIPE Atlas his-
now used to map the Internet [5], detect routing attacks [6],                                         toric dataset, may have been affected by interfering mea-
routing anomalies [7] and censorship [8, 6].                                                          surements. We also highlight two techniques to mitigate
  To scale and be practical, measurement platforms sched-                                             interferences in the future (§6).
ule measurements in parallel, without providing feedback
to the user. When put together with the limited hardware                                              Overall, our results show that measurement interferences
and software capabilities, this raises the question of mea-                                         should be systematically taken into account when analyzing
surement interferences. What is the impact of an increased                                          results from public platforms. To ensure reproducibility, all
load on the precision of measurements performed? Do the                                             our measurement and analysis tools are available online [9].
measurements performed by one participant impact the re-
sults obtained by others? If so, by how much? Can this have                                         2.    THE RIPE ATLAS PLATFORM
                                                                                                      We now describe how Atlas works and highlight its in-
Permission to make digital or hard copies of all or part of this work for personal or               creasing popularity among the academic community.
classroom use is granted without fee provided that copies are not made or distributed
for profit or commercial advantage and that copies bear this notice and the full citation           As of April 2015, RIPE Atlas is composed of over
on the first page. Copyrights for components of this work owned by others than ACM                  6,700 public probes scattered in 197 countries. Three
must be honored. Abstracting with credit is permitted. To copy otherwise, or republish,             versions of the probes exist, differing only by their hardware.
to post on servers or to redistribute to lists, requires prior specific permission and/or a         Version 1 and version 2 are identical except for the amount
fee. Request permissions from Permissions@acm.org.
                                                                                                    of RAM they have. Both are Lantronix XPort Pro with a
IMC’15, October 28–30, 2015, Tokyo, Japan.
 c 2015 ACM. ISBN 978-1-4503-3848-6/15/10 ...$15.00.                                                167MHz CPU, 8MB or 16MB of RAM, respectively and a
DOI: http://dx.doi.org/10.1145/2815675.2815710.                                                     16MB flash. The version 3 probe is a revamped TP-Link TL-




                                                                                              437
                                                                                          v1      v2       v3          Total
                                                                            Total         3.1M    7M       19.7M       29.8M
                                                                            In progress   58K     120K     414K        592K

                                                                      Table 1: Overall, RIPE Atlas has hosted 29.8 million in-
                                                                      dividual measurements. When we collected those results,
                                                                      592,000 concurrent individual measurements were running
                                                                      on the platform.
                                                                      ments2 (Table 1). V3 probes hosted 2/3 of the measure-
Figure 1: RIPE Atlas is composed of more than 6000 low-               ments, while v1 and v2 probes hosted the rest. In March
end probes which differ by their hardware: v1 and v2 probes           2015, the user who used the most credits spent 83.3 million
are not powerful with respect to v3.                                  credits [14]. This is enough to perform more than 2,700,000
                                                                      traceroutes. During the same month, the most used Atlas
                                                                      probe (a v1) provided 608,824 results [14], one every 4 sec-
MR3020 router with a 400MHz CPU, 32MB of RAM and a                    onds. Finally, the number of concurrent measurements is
4MB NAND. The v3 probes are therefore more powerful.                  important. As an illustration, the platform was executing
  Figure 1 depicts the evolution of the number of public              592,000 concurrent individual measurements when we col-
probes per version since the platform inception. The num-             lected the statistics of Table 1.
ber of v3 probes increased rapidly after they started to be              An increasing number of research papers use RIPE Atlas.
distributed in 2013. While the number and proportion of               As an illustration, Machado et al. [15] used it to perform
v1 and v2 probes is decreasing, they remain non-negligible,           more than 3,000 traceroutes between a set of Atlas probes
accounting for 28.2% of the probes in April 2015.                     and a destination in Switzerland to see whether traffic stayed
RIPE Atlas uses credits to regulate the platform                      in the Schengen space. Fanou et al. [16] performed 1,108,709
usage and schedules users’ measurements concur-                       traceroutes from 214 probes located in Africa to measure the
rently. As of 2015, RIPE Atlas offers four1 types of mea-             impact of IXPs on interdomain routing in this region. Fi-
sures to its users: ping, traceroute, DNS and SSL [10]. In            adino et al. [17] perfomed DNS requests for *.whatsapp.net
RIPE Atlas, a measurement is defined by a type, a fre-                from 600 Atlas probes to identify IP addresses hosting this
quency and set of probes. It can therefore refer to an ar-            service. Cicalese et al. [18] performed ping measurements
bitrary number of individual measurements performed from              from over 6000 probes located in 350 ASes in order to enu-
multiple probes. Users can also provide a start date and an           merate and geolocate IP-level anycast replicas.
end date. If none is provided, the measurement will start as          Atlas probes are becoming popular destinations. De-
soon as possible and has to be stopped manually. Measure-             spite being designed for sourcing measurements, Atlas probes
ments can be repeated or run only once (one-off ). One-off            are increasingly used as targets by researchers [19, 20, 21,
measurements are near real-time if no start time is defined:          16]. For example, Aben et al. [19] launched 7140 one-off
users should expect results within 10 seconds [10].                   traceroutes between a set of Atlas probes located in Sweden
   RIPE Atlas regulates users load via a credit system. Users         to infer topological properties. As the IP addresses of the
earn credits by hosting a probe and use them to perform               Atlas probes are publicly available, users can target them
measurements. RIPE’s cost model is based on the resources             from any possible sources (not necessarily from an Atlas
each measurement needs. traceroute is the most expen-                 probe). This enables users to perform hybrid measurement
sive measurement, while ping is the cheapest. One-off mea-            campaigns, with powerful machines as sources, and Atlas
surements are also more expensive (twice more) than their             probes as destinations. Doing so, one can bypass the RIPE
scheduled counterparts as their arrival is not predictable.           Atlas limitations (e.g., frequency, credits cost) while keep-
RIPE Atlas uses basic scheduling strategies on each                   ing some of its interesting characteristics such as the large
probe to handle concurrent load. The source code of                   number of probes.
the RIPE Atlas probes is based on BusyBox [11]. It has                Some Atlas probes are more used than others. Due
been adapted to improve the event management using the                to their geographical position, IPv6 capability or a NAT
libevent library [12]. In addition, probes control the mea-           gateway, some probes are more attractive than others. For
surements frequency with eperd, a cron-like utility that can          instance, the distribution of probes per-country is highly
run measurements at regular intervals. One-off measurements           skewed [22, 23]. While there are more than 1,200 Atlas probes
are managed by the utility eooqd. Probes receive measure-             in Germany, there are 29 countries with only one Atlas
ment requests from their controller with a telnet daemon. As          probe. The recent project sbucket [24] (supported by RIPE)
several users can use a probe at the same time, it is essen-          aims at selecting probes based on spatial distribution rather
tial to somehow schedule and limit users requests. In 2013,           than uniformly. Doing so would then to increase the load on
RIPE made the Atlas source code publicly available [13] but           isolated probes.
not yet the controller’s.
Atlas probes are popular sources of measurements
and are increasingly used in research. Since its incep-
tion, Atlas performed almost 30 million individual measure-
                                                                      2
                                                                       As a measurement may involve a large number of probes,
1
 HTTP measurements are possible but are restricted to re-             the number of individual measurements is more representa-
searchers and other interested users on a case-by-case basis.         tive of the load of the platform.




                                                                438
              Atlas probe                            External
              under test                            Ring nodes


                            Gateway
Reported
             LAN                               Internet
delays


                                External measurements
           Colocated
           Ring node


Figure 2: As opposed to traditional measurements which
pass through the Internet (red arrows), the packets between
the tested Atlas probe and its colocated Ring node (green
arrow) always stay in the local network, thus preventing our             Figure 3: Delays measured from a v2 probe systematically
measurements from being polluted by Internet variations.                 increase when concurrent one-off traceroutes are launched
                                                                         on this probe.

3.    QUANTIFYING INTERFERENCE                                           between them). Because packets between the Atlas probe
                                                                         and its colocated Ring node always stay in the same LAN,
   We describe how we quantify interference between mea-                 we prevent our measurements from being polluted by Inter-
surements performed on a RIPE Atlas probe. We take the                   net variations (Figure 2). We obtained these pairs of colo-
perspective of one user λ and one probe ρ and measure the                cated Atlas probe and Ring node by a traceroute campaign
effects on the results reported by ρ to λ when: i) ρ originates;         between each Ring node and Atlas probes in the same AS.
or ii) is the target of concurrent measurements. In partic-              The results depicted in Table 2 all come from measurements
ular, we look at changes in the delay reported by ρ when                 done between an Atlas probe and its colocated NL Ring
concurrent one-off traceroutes are originated or when ρ is               node.
being used as ping destination. We use NL Ring nodes [25]
as destinations (resp. as sources) of the pings sourced on
(resp. destined to) ρ. We also look at changes in the com-               4.   DECREASED PRECISION
pletion time of one-off traceroute experiments performed on                 We now use our methodology (§3) to measure: i) the de-
ρ.                                                                       crease in precision of delay-based measurements (this sec-
                                                                         tion); and (ii) the decrease in synchrony produced by con-
We measure the delay reported by a probe using
                                                                         current measurements (§5). We performed all our measure-
ping Delay-based measurements are indeed the most sensi-
                                                                         ments on multiple probes (at least two per version) to ensure
tive to concurrent load. In contrast, traceroute, SSL, and
                                                                         conformity. As their number is not negligible and their de-
DNS output is less impacted by extra delay.
                                                                         crease in precision and synchrony is serious, the next figures
We also study the decrease in synchrony by measuring                     only focus on v2 probes.
the completion time of one-off traceroutes performed on the
                                                                         Delays measured from the probe increase when con-
probe.
                                                                         current measurements are launched on it. We launched
. . . when increasing the number of concurrent mea-                      ping measurements from the Atlas probe and towards eight
surements sourced from a probe To generate load on a                     random Ring nodes plus the colocated Ring node. The ping
probe, we launch an increasing number of one-off traceroutes             rate towards each destination is 9 ping/min, averaging 1.4
from it using the REST API [26]. We use traceroute because               ping/s over all destinations. We increase the load on the
it uses the most resources, as indicated by the higher cost.             probe by launching successively 10, 25, 50, 100, 250, and
It is also one of the tools mostly used by researchers.                  500 one-off traceroutes.
                                                                            Figure 3 shows the impact of the concurrent one-off tracer-
. . . when increasing the number of concurrent mea-
                                                                         outes on the delay measured from a v2 probe. The blue
surements targeting a probe The second technique we
                                                                         points are RTTs between the Atlas probe and its colocated
use to load a probe consists in gradually increasing the num-
                                                                         Ring node, while the red points are RTTs between the Atlas
ber of ICMP echo requests (800 bytes) targeted to it. We use
                                                                         probe and another Ring node. The gray areas are the peri-
a set of NL Ring nodes as sources. Each source sends 16 echo
                                                                         ods when one-off traceroutes are running. The number above
requests per second. We start with a single source. Every 2
                                                                         each gray area is the number of one-off traceroutes executed.
minutes, we add a new source. We stop when there are 115
                                                                         To quantify the impact, we compare the median, 95th per-
sources (115 ∗ 16 = 1840 ping/s). While such frequencies are
                                                                         centile, and standard deviation of the ping measurements
not common, experiments that use Atlas probes in a mesh-
                                                                         before the one-off traceroutes (the white area preceding the
like fashion [16, 19, 20, 21] or that ping them from machines
                                                                         gray area) and during the one-off traceroutes execution time
not limited in ping frequency may generate such a load. We
                                                                         (gray area). The difference is reported in Table 2.
use several Ring nodes as sources to mimic real experiments.
                                                                            Delays measured from the probe systematically increase
To perform remote pings on multiple Ring nodes and collect
                                                                         when one-off traceroutes are performed. Starting 100 one-
the results, we built a tool [9] atop Scamper [27].
                                                                         off traceroutes increases the median delay of the concurrent
. . . and while preventing the effects from external                     pings by more than 1 ms. For v1 and v2 Atlas probes, the
factors We want to focus on the behavior of the probe and                standard deviation is seriously impacted: +16.3 ms (v1) and
avoid network interferences. For each experiment, we mea-                +7.4 ms (v2). Atlas probes v3 show less effect, the median is
sure the delay between the tested Atlas probe and a colo-                only increased by 0.06 ms while the standard deviation is not
cated Ring node in the same LAN (i.e. there is no IP hop                 impacted; this is due to v3 probes having more power. Sur-




                                                                   439
        impact on ping delay . . .               sourced on probe                               destined to probe
        when increasing load . . .

        on probe                             50th      95th      stdev                     50th      95th       stdev
                                        (on : 100 traceroutes + 1.4 ping/s)           (on : 100 traceroutes, to : 9 ping/s)
                                        v1 1.10 ms 7.30 ms 16.3 ms                    v1 0.61 ms 0.72 ms 0.04 ms
                                        v2 1.20 ms 7.70 ms 7.40 ms                    v2 0.50 ms 0.62 ms 0.02 ms
                                        v3 0.06 ms 0.10 ms 0.00 ms                    v3 0.06 ms 0.05 ms 0.00 ms

        towards probe                        50th      95th       stdev                   50th      95th      stdev
                                         (on : 9 ping/min, to : 400 ping/s)           (on : 9 ping/min, to : 1000 ping/s)
                                                                                         ∗

                                        v1 0.11 ms 1.90 ms 15.2 ms                    v1 0.20 ms 5.40 ms 33.0 ms
                                        v2 0.22 ms 2.90 ms 3.90 ms                    v2 0.45 ms 2.60 ms 1.10 ms
                                        v3 0.00 ms 0.04 ms 0.00 ms                    v3 0.00 ms 0.00 ms 0.00 ms

Table 2: Quantification of interferences for v1, v2 and v3 probes. At the top, the probe is loaded by sourcing 100 one-off
traceroutes. At the bottom, the load comes from incoming pings. Columns represent benchmarking measurements. On the
left, we look at the impact of a load on the ping delay reported by the probe. On the right, pings are destined to the probe.
With more powerful hardware, v3 probes are less sensitive to load than v1 and v2. ∗ We used these pings to quantify the
impact a load towards the probe produces on ping delay sourced on the probe (bottom-left).




Figure 4: Delays measured towards a v2 probe systematically            Figure 5: Delays measured from a v2 probe increase as the
increase when concurrent one-off traceroutes are launched on           ping frequency targeting the probe increases.
the probe.
                                                                       wards its colocated Ring node with a frequency of 9 ping/min.
prisingly, the number of one-off traceroutes does not change           We then use an increasing set of Ring nodes to target the
the magnitude of the impact but increases its duration: 10             probe with 800 bytes pings, each of them sending 16 ping/s
one-off traceroutes impact as severely as 100 the concurrent           (§3).
ping measurements. As soon as the one-off traceroutes are                 Figure 5 shows the impact on delay measured from the
done, RTTs go back to normal almost immediately.                       probe. Unlike with one-off traceroute measurements, the im-
                                                                       pact now increases with the number of pings directed to-
Delays measured towards the probe increase when
                                                                       wards the probe. When the frequency reaches 400 ping/s,
concurrent measurements are launched on it. We
                                                                       the median delay reported by the probe increases by 0.22 ms,
chose eight random Ring nodes plus the colocated Ring node
                                                                       while the 95th percentile increases by 2.90 ms and the stan-
and ping from them towards the Atlas probe with a fre-
                                                                       dard deviation by 3.90 ms. The probe becomes completely
quency of 1 ping/s, summing up to a load of 9 ping/s. We
                                                                       overloaded when the frequency reaches 1000 ping/s. This
then perform successively 10, 25, 50, 100, 250, and 500 one-
                                                                       leads to very high delays (∼1000 ms). Also, 10% of the pings
off traceroutes from the Atlas probe.
                                                                       are lost when the frequency becomes higher than 1280 ping/s.
   Figure 4 shows the impact of the one-off traceroutes on
                                                                       Here, the probe is the target of the load. Traffic is just sent to
the delay measured towards the Atlas probe. The blue points
                                                                       the probe, without involving the RIPE Atlas controller. We
are the delays reported between the colocated Ring node and
                                                                       believe the inaccuracy increases progressively because the
the Atlas probe while the red points are the delays reported
                                                                       load per unit of time also increases. The controller cannot
between another Ring node and the Atlas probe. Again, gray
                                                                       smooth the load by spreading it in time.
indicates periods when one-off traceroutes are running.
                                                                          Figure 6 illustrates similar effects on the delays measured
   The impact on pings targeting the probe is relatively lower
                                                                       towards the probe. At the bottom of the figure, each box
(Table 2). When 100 one-off traceroutes are executed, the
                                                                       shows the inter-quartile range of RTTs between the colo-
median of RTTs targeting a v2 Atlas probe increases by
                                                                       cated Ring node and the Atlas probe. The line in the box
0.5 ms. Despite the lower impact, we can easily see RTT
                                                                       depicts the median value; the whiskers show the 1st and
shifts.
                                                                       the 99th percentile, respectively. The top figure indicates
Delays measured from and towards a probe increase                      the packet loss percentage. When reaching 1000 ping/s, the
when it is used as a destination by concurrent mea-                    median RTT increases by 0.45 ms and the 95th percentile
surements. We first launch pings from the Atlas probe to-              increases by 2.60 ms. As in Figure 5, when the frequency




                                                                 440
                                                                         Figure 7: Increasing the source and destination load at the
                                                                         same time greatly increases the interference between mea-
                                                                         surements. One-off traceroutes take more time to execute,
Figure 6: Delays measured towards a v2 probe increase as                 and worse, may fail. RTTs measured from the probe become
the pings frequency targeting this probe increases. Packet               higher.
losses may appear if the ping frequency towards the probe
becomes too high.                                                        time to limit the instantaneous load on a probe. When load
                                                                         increases, so does the completion time. We measure the time
becomes even higher, the probe becomes completely over-                  delta between when we request traceroute measurements
loaded. Reported delays skyrocket (∼1000 ms) and some re-                and the time they finish.
quests are lost.
                                                                         Completion time significantly increases with the num-
Interference effects are compounded when combin-                         ber of traceroutes. Figure 8 shows that the completion
ing source and destination load. So far, we have quan-                   time may be 6.7 minutes (resp. 4.5 minutes) when requesting
tified separately the impact of using a probe as source or as            50 one-off traceroutes on a v2 (resp. v3) probe. It takes up to
destination. In reality, a probe may be used both as source              41 minutes with 500 one-off traceroutes on a v3 probes. All
and as destination at the same time. We could expect these               probe versions, including v3, are subject to a significant in-
interference effects to be additive, but our experiments show            crease in completion time. Further experiments have shown
that these effects are compounded.                                       completion times greater than one hour, even for v3 probes.
   To quantify, we first start pings between an Atlas probe
                                                                         Completion time increases with the load towards the
and its colocated Ring node (9 ping/min). We then start
                                                                         probe. In Figure 7, while the completion time for the first
to flood the probe using the set of Ring nodes as described
                                                                         25 one-off traceroutes takes up to 6.2 minutes, it takes up
before. Finally, we start series of 25 one-off traceroutes. Fig-
                                                                         to 11.3 minutes for the second series of one-off traceroutes
ure 7 shows the results. The blue points are the measured de-
                                                                         and up to 20.2 minutes for the third series. Sending 500
lays between the probe and the colocated Ring node. The red
                                                                         ping/s to a probe may then multiply the one-off traceroutes
vertical line indicates when we start to flood the probe with
                                                                         completion time by more than 3. When the ping frequency
pings. The gray areas are the periods when one-off tracer-
                                                                         becomes too high, most of the traceroutes fail.
outes are running. Before starting to flood the probe, we
performed 25 one-off traceroutes in order to be able to com-             Key points Under load, requested measurements may be
pare the interference effects produced by these traceroutes              delayed, rendering the platform unsuitable to synchronized
with and without the ping flood. Each green point on the                 measurements. One could not ensure that pings or tracer-
top indicates a traceroute success. The success rate of each             outes start simultaneously on multiple probes. This is espe-
one-off traceroute series is also mentioned.                             cially a problem when one wants to measure the effect of a
   When compounding source and destination load, delays                  single event from multiple vantage points, or an exogenous
measured from the probe increase even further. During the                event. This problem applies to all probe hardware—including
second series of one-off traceroutes, the standard deviation of          the most powerful v3.
the delay reported by the probe to the colocated Ring node
is 30.8 ms and the 95th percentile is 23.9 ms. These values
are far higher than the addition of the interference effects
                                                                         6.    DISCUSSIONS
produced by a non-combined load on source and destination                  We now describe the impact for researchers working with
(Table 2). Success rate is also effected. 99% of the pings are           the platform (§6.1) as well as two solutions on how to miti-
lost during the last one-off traceroute series.                          gate interference in practice (§6.2).
Key points. We observed significant interferences on delay               6.1   Impact for researchers
measurements for v1 and v2 probes. These probes compose
28% percent of the platform. An important portion (34%)                  On previous works. As described earlier, many research
of the public experiments available result from experiments              papers have used RIPE Atlas. Some of them relied on delay-
on v1 and v2 probes.                                                     based measurements [3, 4, 18, 28, 6, 16] which can be im-
                                                                         pacted by interferences. For instance, Rimondini et al. [3]
                                                                         used PELT [29], a changepoint detection algorithm, to de-
5.   INCREASED ASYNCHRONY                                                tect shifts in RTTs and correlate them with routing changes.
   We now study the impact of concurrent load on comple-                 We mimicked such experiments on the RTTs of Figures 3
tion time. Atlas measurements are indeed scheduled over                  and 4 and detected a changepoint each time a one-off tracer-




                                                                   441
                                                                         provide users with information about the state of these plat-
                                                                         forms and their nodes. In contrast, RIPE Atlas does not use
                                                                         virtualization and relies on a scheduler to share resources
                                                                         among users.
                                                                            Gangam et al. [36] introduced heuristics to schedule a set
                                                                         of measurements between a set of nodes in order to avoid
                                                                         interference effects. However, this does not work when ex-
                                                                         ternal measurements use Atlas probes as destinations.
                                                                            Sanchez [37] et al. proposed a technique to coordinate ex-
                                                                         periments of a large-scale measurements platform in order
Figure 8: One-off traceroutes completion time is also im-                to avoid undesired load on a network or a device. This so-
pacted by concurrent measurements, independent of the                    lution is based on contracts, that give their holder specified
hardware used. Results can be delayed by more than half                  rights over a set of resources for a limited period of time. In
an hour—making it impossible to perform synchronized ex-                 contrast, RIPE Atlas applies static rate limits for users and
periments.                                                               measurements. An user cannot run more than 100 simulta-
                                                                         neous measurements, and the ping frequency is limited to
oute series starts and stops. Cicalese et al. [18] used the min-
                                                                         one ping per minute.
imum value of ten successive RTTs to enumerate and geolo-
                                                                            Dasu [38] is a software-based measurement platform hosted
cate IP-level anycast replicas. As a 1ms difference in latency
                                                                         by voluntary nodes located at the edge of the network. To
measurements corresponds to a 100 km radius in geodesic
                                                                         enable finer-grained synchronization between a set of mea-
distance, such studies may also be polluted by interference
                                                                         surements (on the order of milliseconds), Dasu adopts a re-
effects. An operator can use Atlas probes to measure the
                                                                         mote triggering execution model. In contrast, the one-off
performance of her network. In this case, interference effects
                                                                         measurements provided by RIPE Atlas are launched as soon
highlighted on the Figure 5 and 6 could wrongly trigger con-
                                                                         as possible (best-effort).
gestion alarms. Based on our results, any delay-based mea-
                                                                            In [23], Bajpai et al. showed that RTTs from v1 and v2
surement obtained from v1 and v2 probes should be avoided
                                                                         probes to the first hop router are consistently higher than for
if a precision below 15 ms is required.
                                                                         v3 probes. They do not however study the relation between
On publicly available data. RIPE Atlas makes publicly                    the measured delays and the load of the probes.
available all the results collected with the platform since its             Mok et al. [39] proposed a technique to reduce packet
inception in 2010 [30]. Researchers using these data should              sending time on low-end devices such as Atlas probes. This
consider the impact of interferences. Especially for data col-           technique may be useful to counteract some of the interfer-
lected before 2013—prior to v3 probes. We suggest researchers            ence effects we expose in this paper.
to be very careful when using publicly available delay mea-
surements.                                                               8.   CONCLUSION
6.2    Solutions                                                            We presented the first measurement study of user-induced
                                                                         interferences on the RIPE Atlas platform. We found that
Provide feedback to users with a measurement confi-                      measurements do interfere with each other. Delays reported
dence index. A fundamental problem with Atlas is that the                from the probe increase and vary more when they compete
user has no visibility on the concurrent load of the platform.           with concurrent measurements. Measurement campaigns can
For that, we argue that RIPE can return a “confidence in-                further be arbitrary delayed, making it hard to perform si-
dex” along with each result. The index would be function of              multaneous experiments from multiple probes.
the platform concurrent load. High (resp. low) load would                   Our findings also bring up new, non-trivial research ques-
lead to low (resp. high) confidence. Obviously, computing                tions: how can we design measurement platforms that pro-
this metric should be done based on passive measurements                 vide more isolation between users, while still being efficient
to not stress the platform even more. We are currently work-             (i.e., not requiring a global lock). We plan to explore this
ing on calibrating such a metric using our measurements.                 direction in the future.
Enforce synchronization. While real-time is not a reason-
able objective on shared platforms, more precise scheduling              9.   ACKNOWLEDGMENTS
is achievable by maintaining a lower load on the probes and                We wish to thank both the RIPE Atlas and the NLNOG
delaying upcoming measurements in favor of already sched-                RING support teams for accommodating our measurements
uled events. Upon a measurement request, the user could                  and promptly replying to our questions.
then be informed of the exact timing of her experiment.
Such an approach is however not possible if users do not
all have the same privileges and some experiments can be
preempted.

7.    RELATED WORK
  Other researchers have observed measurement interfer-
ence and its impact on RTT. As an example, the effects
virtualization can produce on measured delays have already
been pointed out [31, 32]. As a number of large-scale plat-
forms use VMs [33, 34, 25], tools such as [35] for PlanetLab,




                                                                   442
10.   REFERENCES                                                     [21] Measuring Countries and IXPs in the SEE Region.
                                                                          [Online]. Available: https://labs.ripe.net/Members/
 [1] RIPE NCC. RIPE Atlas. [Online]. Available: https://                  emileaben/
     atlas.ripe.net                                                       measuring-countries-and-ixps-in-the-see-region
 [2] S. Roy and N. Feamster, “Characterizing correlated              [22] Percentage of connected probes per country. [Online].
     latency anomalies in broadband access networks,” in                  Available: https://atlas.ripe.net/results/maps/
     ACM SIGCOMM 2013 (Poster Session), 2013.                             density/
 [3] M. Rimondini, C. Squarcella, and G. Di Battista,                [23] V. Bajpai, S. J. Eravuchira, and J. Schönwälder,
     “Towards an Automated Investigation of the Impact of                 “Lessons learned from using the ripe atlas platform for
     BGP Routing Changes on Network Delay Variations,”                    measurement research,” SIGCOMM Comput.
     in PAM, 2014.                                                        Commun. Rev., vol. 45, no. 3, pp. 35–42, Jul. 2015.
 [4] G. Da Lozzo, G. Di Battista, and C. Squarcella,                 [24] RIPE-Atlas-sbucket. [Online]. Available: https://
     “Visual discovery of the correlation between bgp                     github.com/cod3monk/RIPE-Atlas-sbucket
     routing and round-trip delay active measurements,”              [25] NLNOG Ring. [Online]. Available: https://ring.nlnog.
     Computing, vol. 96, no. 1, pp. 67–77, 2014.                          net
 [5] A. Faggiani, E. Gregori, A. Improta, L. Lenzini,                [26] Creating Measurements with the RIPE Atlas Restful
     V. Luconi, and L. Sani, “A study on traceroute                       API. [Online]. Available: https://atlas.ripe.net/docs/
     potentiality in revealing the internet as-level                      measurement-creation-api/
     topology,” in IFIP Networking 2014, 2014.
                                                                     [27] M. J. Luckie, “Scamper: a scalable and extensible
 [6] A RIPE Atlas View of Internet Meddling in Turkey .                   packet prober for active measurement of the internet,”
     [Online]. Available: https://labs.ripe.net/Members/                  in IMC, 2010.
     emileaben/
                                                                     [28] RIPE Atlas - Superstorm Sandy. [Online]. Available:
     a-ripe-atlas-view-of-internet-meddling-in-turkey
                                                                          https://labs.ripe.net/Members/emileaben/
 [7] T. Yakimov, “Detecting routing anomalies with ripe                   ripe-atlas-superstorm-sandy
     atlas,” april 2014.
                                                                     [29] R. Killick and I. A. Eckley, “changepoint: An r
 [8] C. Anderson, P. Winter, and Roya, “Global network                    package for changepoint analysis,” Journal of
     interference detection over the ripe atlas network,” in              Statistical Software, vol. 58, no. 3, pp. ??–??, 6 2014.
     4th USENIX Workshop on Free and Open
                                                                     [30] RIPE Atlas - Public measurements. [Online].
     Communications on the Internet, August 2014.
                                                                          Available: https://atlas.ripe.net/measurements/#!
 [9] [Online]. Available: https://github.com/nsg-ethz/                    public
     atlas interference
                                                                     [31] J. Whiteaker, F. Schneider, and R. Teixeira,
[10] RIPE Atlas - User-Defined Measurements. [Online].                    “Explaining packet delays under virtualization,”
     Available: https://atlas.ripe.net/docs/udm/                          SIGCOMM Comput. Commun. Rev., vol. 41, 2009.
[11] N. Wells, “Busybox: A swiss army knife for linux,”              [32] N. Spring, L. Peterson, A. Bavier, and V. Pai, “Using
     Linux J., vol. 2000, no. 78es, Oct. 2000.                            planetlab for network research: Myths, realities, and
[12] libevent - an event notification library. [Online].                  best practices,” SIGOPS Oper. Syst. Rev., 2006.
     Available: http://libevent.org/                                 [33] Planetlab, “Planetlab: An open platform for
[13] Releasing RIPE Atlas Measurements Source Code .                      developing, deploying and accessing planetary-scale
     [Online]. Available: https://labs.ripe.net/Members/                  services,” http://planet-lab.org.
     philip homburg/ripe-atlas-measurements-source-code              [34] M-Lab, “Measurement lab,” http://www.
[14] Community Information, contributions, and hosts that                 measurementlab.net.
     stand out. [Online]. Available: https://atlas.ripe.net/         [35] K. Park and V. S. Pai, “Comon: A mostly-scalable
     get-involved/community/                                              monitoring system for planetlab,” SIGOPS Oper. Syst.
[15] G. Machado, C. Tsiaras, and B. Stiller, “Schengen                    Rev., vol. 40, no. 1, pp. 65–74, Jan. 2006.
     Routing: A Compliance Analysis,” in AIMS, 2015.                 [36] S. Gangam and S. Fahmy, “Mitigating interference in a
[16] R. Fanou, F. Pierre, and E. Aben, “On the Diversity                  network measurement service,” ser. IWQoS ’11, 2011.
     of Interdomain Routing in Africa,” in PAM, 2015.                [37] M. A. Sánchez, F. E. Bustamante, B. Krishnamurthy,
[17] P. Fiadino, M. Schiavone, and P. Casas, “Vivisecting                 and W. Willinger, “Experiment coordination for
     whatsapp in cellular networks: Servers, flows, and                   large-scale measurement platforms,” in ACM
     quality of experience,” in TMA, 2015.                                SIGCOMM Workshop on C2B(I)D, 2015.
[18] D. Cicalese, D. Joumblatt, D. Rossi, M.-O. Buob,                [38] M. A. Sánchez, J. S. Otto, Z. S. Bischof, D. R.
     J. Auge, and T. Friedman, “A fistful of pings:                       Choffnes, F. E. Bustamante, B. Krishnamurthy, and
     Accurate and lightweight anycast enumeration and                     W. Willinger, “Dasu: Pushing experiments to the
     geolocation,” in IEEE INFOCOM, 04/2015 2015.                         internet’s edge,” in NSDI, 2013.
[19] Measuring Countries and IXPs with RIPE Atlas.                   [39] R. K. P. Mok, W. Li, and R. K. C. Chang, “Improving
     [Online]. Available: https://labs.ripe.net/Members/                  the packet send-time accuracy in embedded devices,”
     emileaben/measuring-ixps-with-ripe-atlas                             in PAM 2015.
[20] How does the MENOG Region Measure up? [Online].
     Available: https://labs.ripe.net/Members/mirjam/
     how-does-the-menog-region-measure-up




                                                               443
