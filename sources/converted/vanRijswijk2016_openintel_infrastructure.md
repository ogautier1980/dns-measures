IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 34, NO. 6, JUNE 2016                                                                1877




      A High-Performance, Scalable Infrastructure for
         Large-Scale Active DNS Measurements
                            Roland van Rijswijk-Deij, Mattijs Jonker, Anna Sperotto, and Aiko Pras



   Abstract— The domain name system (DNS) is a core                             received from another host is legitimate or should be treated
component of the Internet. It performs the vital task of mapping                as spam. Thus, measuring the DNS provides a wealth of
human readable names into machine readable data (such as IP                     data about the Internet, ranging from operational practices,
addresses, which hosts handle e-mail, and so on). The content of
the DNS reveals a lot about the technical operations of a domain.               to the stability of the infrastructure, to security. Consider,
Thus, studying the state of large parts of the DNS over time                    for example, e-mail handling. In the DNS, the MX record
reveals valuable information about the evolution of the Internet.               type specifies which hosts handle e-mail for a domain. Thus,
We collect a unique long-term data set with daily DNS measure-                  examining which MX records are present can tell us, for
ments for all the domains under the main top-level                              example, if e-mail handling for that domain is outsourced to
domains (TLDs) on the Internet (including .com, .net, and
.org, comprising 50% of the global DNS name space). This                        a cloud provider such as Google, Microsoft or Yahoo. Another
paper discusses the challenges of performing such a large-scale                 example is the monitoring of protocol adoption such as IPv6
active measurement. These challenges include scaling the daily                  and DNSSEC. The analysis of AAAA or DNSKEY resource
measurement to collect data for the largest TLD (.com, with                     records can provide ground truth about the adoption of, and
123M names) and ensuring that a measurement of this scale                       operational practices for these protocols over time. Finally,
does not impose an unacceptable burden on the global DNS
infrastructure. The paper discusses the design choices we have                  DNS data can also play a vital role in security research, for
made to meet these challenges and documents the design of the                   instance for studying botnets, phishing and malware.
measurement system we implemented based on these choices. Two                      The DNS has been the focus of, or used in, past
case studies related to cloud e-mail services illustrate the value of           measurement studies. These studies, however, had a limited
measuring the DNS at this scale. The data this system collects is               scope, in time, coverage of DNS records or number of
valuable to the network research community. Therefore, we end
this paper by discussing how we make the data accessible to                     domains measured. It remains highly challenging to measure
other researchers.                                                              the DNS in a comprehensive, large-scale, and long-term
                                                                                manner. Nonetheless, because this type of measurement can
  Index Terms— DNS, active measurements, cloud, Internet
evolution.                                                                      provide such valuable information about the evolution of the
                                                                                Internet, we challenged ourselves to do precisely this. Our
                                                                                research goal is to perform daily active measurements of all
                          I. I NTRODUCTION                                      domains in the main top-level domains (TLDs) on the Internet

T    HE Domain Name System (DNS), plays a crucial role
     in the day-to-day operation of the Internet. It performs
the vital task of translating human readable names – such as
                                                                                (including .com, .net and .org, together comprising 50%
                                                                                of the global DNS name space) and to collect this data over
                                                                                long periods of time potentially spanning multiple years.
www.example.com – into machine readable information.                               This paper focuses on the challenges of achieving this
Almost all networked services depend on the DNS to store                        goal by answering the following main research question:
information about the service. Often this information is about                  “How can one perform a daily active DNS measurement of
what IP address to contact, but also whether or not e-mail                      a significant proportion of all domains on the Internet?”. The
                                                                                main contributions of the paper are that we show how to:
  Manuscript received September 11, 2015; revised January 20, 2016;
accepted February 15, 2016. Date of publication April 27, 2016; date of            • Scale such a measurement to cope with the largest TLD
current version June 6, 2016. This work was supported in part by the European         (.com with 123M names).
Commission 7th Framework Programme through the FLAMINGO Network                    • Ensure that the traffic such a measurement generates does
of Excellence Project under Grant 318488 and in part by SURF, The
Netherlands, collaborative organisation for ICT in Higher Education and               not adversely affect the global DNS infrastructure.
Research Institutes. (Corresponding author: Roland van Rijswijk-Deij.)             • Efficiently store and analyse the collected data.
  R. van Rijswijk-Deij is with the Design and Analysis of Communication            Our measurements create a novel large-scale dataset of great
System Group, Faculty of Electrical Engineering, Mathematics and Computer
Science, University of Twente, Enschede 7500 AE, The Netherlands, and also      value to the research community as well as in other contexts
with SURFnet bv, National Research and Education Network, Utrecht 3511          (e.g. for security and forensic purposes). Our ultimate goal
EP, The Netherlands (e-mail: r.m.vanrijswijk@utwente.nl).                       therefore is to make the data accessible to others. How we
  M. Jonker, A. Sperotto, and A. Pras are with the Design and Analysis
of Communication System Group, Faculty of Electrical Engineering,               will do this is discussed at the end of the paper.
Mathematics and Computer Science, University of Twente, Enschede 7500              Finally, in order to validate our system in practice and to
AE, The Netherlands.                                                            illustrate potential uses of the data it collects, we performed
  Color versions of one or more of the figures in this paper are available
online at http://ieeexplore.ieee.org.                                           two case studies. Given the growing research interest in
  Digital Object Identifier 10.1109/JSAC.2016.2558918                           cloud services, the case studies focus on the use of cloud
                       0733-8716 © 2016 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.
                            See http://www.ieee.org/publications_standards/publications/rights/index.html for more information.
1878                                                      IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 34, NO. 6, JUNE 2016



e-mail services. Based on ten months of data collected by the                                   TABLE I
measurement system between March 2015 and January 2016,                                 Q UERY T YPES TO P ERFORM
we studied the following questions:
   • Is Google the most popular cloud mail service provider,
      or are others, such as Microsoft or Yahoo, more popular?
   • Which of these three providers sees the fastest growth?
   • Do domains that use these cloud mail services use the
      Sender Policy Framework (SPF) [1] to combat e-mail
      forgery, especially since most providers support SPF?
   Structure of This Paper: Section II introduces our long-term
research goals and the challenges that achieving these goals
pose. Section III discusses and motivates design choices
and the resulting design of the measurement system we
created. Section IV examines operational experiences with
the measurement system, and analyses the impact the system
has on the global DNS infrastructure. Section V presents
two case studies, which serve both to validate the system,
and to illustrate the value of the collected data. Section VI
covers background information and related work. Section VII               TLDs (gTLDs) .com, .net, and .org, as together
describes how we intend to make result data accessible to                 these contain 50% of domain registrations in the
the academic research community. Finally, in Section VIII,                global DNS.
we present our conclusions and discuss future work.
                                                                    B. Challenges
               II. G OALS AND C HALLENGES                              To meet the goals above, a number of challenges will have
                                                                    to be overcome. These challenges are outlined below:
A. Goals                                                              C1 Query volume – as G1 and G4 state, we want to
   Our research goal is to create a large-scale data set covering         be able to measure all domains in the largest TLD
the state of the DNS for a significant proportion of the global           (.com with 123M names) once every 24 hours. For each
name space. The data set should record this state at regular              name, 14 queries are performed (G3). Next to direct
intervals, in order to be able to create time series tracking             queries, the system needs to send additional queries
trends and developments on the Internet. To achieve this                  as part of normal DNS recursion (e.g. to find the
ultimate goal, we define the following sub-goals:                         authoritative name servers for a domain). A conservative
  G1 Measure every single domain in a top-level domain                    estimate is that this requires one additional query per
       (TLD) – this allows us to build a comprehensive picture            domain. Thus, querying every domain in .com requires
       of large parts of the DNS name space.                              at least 1.85B queries per day.
  G2 Be able to measure even the largest TLD (.com) – if              C2 Query pacing – a challenge related to C1 is pacing of
       the system is capable of measuring .com (123M names)               queries. It is important that the queries we send do not
       it can also measure other, smaller TLDs.                           impose an excessive load on authoritative name servers.
  G3 Measure a fixed set of relevant resource records for                 Especially traffic flows to the top-level servers that are
       each domain – the DNS has different resource record                authoritative for the TLDs that are measured need to be
       types that serve specific purposes. In Table I we define           monitored, as queries for individual domains also lead
       the set of queries we want to perform. Queries have been           to queries to these servers due to the hierarchical way
       chosen such that they cover the most common DNS uses               the DNS is organised. Similarly, we have to monitor the
       with the minimum number of queries.                                traffic volume to large hosting providers, since these may
  G4 Measure each domain once per day – to be able                        provide authoritative DNS services for large numbers of
       to create reliable time series, each domain must be                domains.
       measured exactly once every 24 hours.                          C3 Storage – taking the .com TLD as yardstick – and
  G5 Store at least one year’s worth of data – to do                      assuming that each of the 14 queries performed for each
       meaningful research, we should be able to store data               domain returns ±150 bytes of data – more than 240GB
       that covers at least one year, and preferably a longer             of results need to be stored per day for .com alone.
       period.                                                            Considering G5 and G6 this is particularly challenging.
  G6 Analyse data efficiently – we expect to be collecting            C4 Robustness – the measurement must run continuously
       data for tens of millions of domains; this means that              and not suffer from downtime due to maintenance or
       we must explicitly design for efficient analysis through           crashes.
       modern technologies such as the Hadoop ecosystem.              C5 Ease of operation – to meet most of the other
  G7 Scalability – the measurement should scale to both                   challenges outlined above, we foresee a distributed
       handle TLD growth and to measure additional TLDs.                  system of machines that perform the measurement.
       We initially foresee measuring the main generic                    Management and administration of such a distributed
VAN RIJSWIJK-DEIJ et al.: HIGH-PERFORMANCE, SCALABLE INFRASTRUCTURE FOR LARGE-SCALE ACTIVE DNS MEASUREMENTS                    1879



      infrastructure has to be simple. Additionally, scaling the    was that this option would perform sufficiently well to meet
      measurement to incorporate more TLDs should also be           challenge C1. Next to that, the top-speed performance offered
      straightforward.                                              by the first option (bare metal) is not actually a requirement.
                                                                    Rather, to manage the impact of the measurement on
           III. M EASUREMENT S YSTEM D ESIGN                        the global DNS (challenge C2) there must be a trade-off
   We have designed and implemented a measurement system            between speed and impact of the measurement. In order to
to meet the goals and challenges discussed in Section II. This      confirm our intuition that this approach performs sufficiently,
section takes a detailed look at the design of this system. The     a proof-of-concept was implemented, the goal of which was
section is divided into two parts. The first part discusses and     to measure the medium-sized .org top-level domain. Given
motivates the major design decisions taken while creating the       the time taken to measure this TLD, we could extrapolate that
measurement system. The second part describes the resulting         this approach would make meeting challenge C1 (measuring
system design and its implementation.                               very large TLDs such as .com) feasible. Based on these
                                                                    considerations we chose to proceed with the implementation
                                                                    of the second approach. All that remained was to determine
A. Design Choices                                                   the impact of the measurement on the global DNS; this is
   Before setting out to design and implement such                  discussed in Section IV-B.
a large-scale measurement system, we carefully considered key          2) Scalability of the Measurement: The second design
choices to make in order to ensure that the system tackles all      decision focused on how to best scale the measurement system
the challenges and meets all the goals discussed in Section II.     (goal G7 and challenge C5). The first option considered was
This subsection discusses the major design decisions made           to run the measurement software on a single system. Given
while creating the measurement system and motivates our             measurements we performed for an earlier study [3], we knew
choices by discussing the options we explored.                      from experience that this would put high requirements on the
   1) DNS Software: Given the goal of the system, the most          system on which the measurement would run, mainly in terms
important decision to be made concerned the software to             of CPU utilisation. Choosing this option would therefore make
use to perform the actual DNS queries that make up the              it hard to scale the measurement in the future.
measurement. Two options were considered:                              To ensure scalability, we thus chose a distributed approach
      a) A Bare metal approach: in a bare metal approach the        with a central orchestration system and a swarm of worker
focus is on maximum measurement speed. An example of this           nodes. Given the ready availability of cloud computing
approach is the ZMap network scanner [2], which performs            stacks, we focused on an implementation that is amenable
network scans by directly generating Ethernet frames. This          to deployment on cloud platforms, and chose to implement
approach bypasses all intermediate layers in the network stack,     worker nodes as a virtual machine image. While we initially
allowing scans at near line-speed. While a bare metal approach      envisaged a deployment of the measurement system in a single
is a potentially attractive way to tackle the measurement           location, this design choice means that we can scale up
speed challenge we face, there are disadvantages to taking          to commercial cloud platforms if we run out of local
such an approach. Most importantly, resolving DNS queries           resources, and it also means that we can relocate parts of the
is a complex task, much more complex than e.g. the simple           measurement to other geographical regions. The latter may be
port scans ZMap performs. Re-implementing DNS resolution            advantageous for measurements on, for example, country-code
in a bare metal fashion would require significant effort and        top-level domains (ccTLDs) with a strong geographic binding,
runs a high risk of bugs that adversely affect the reliability of   where measuring from a local vantage point relative to the
the measurement system (challenge 4).                               ccTLD can have performance benefits in terms of network
      b) Using off-the-shelf DNS software: this option relies       latency.
on maximum re-use of existing software. The measurement                3) Data Format and Analysis: The final design considera-
software would need to incorporate a simple DNS stub resolver       tions concern storage and analysis of the measurement
that is capable of sending single queries, and the more             results (goals G5 & G6 and challenge C3). The de-facto
complex task of DNS recursion is left to an off-the-shelf           toolchain for analysing big datasets – such as the one our
implementation. The advantage of such an approach is that           measurement system collects – is the Hadoop ecosystem.1
it entails the smallest risk of falling into the pitfalls of        Thus, we designed the system such that the resulting
the complex task of implementing DNS recursion. The                 measurement data is suited to processing in the Hadoop
disadvantage is, of course, that such an approach will be           ecosystem.
slower.                                                                For storage, we decided on a two-tiered approach. In the
   Taking the advantages and disadvantages of these two             first step, results are stored in the Apache Avro file format.2
options into consideration, we chose to explore the second          Avro is a structured, self-describing data serialisation format
option – using standard DNS software as much as possible – in       with built-in support for compression, which is used by the
more detail. Firstly, this approach requires the least complexity   system to reduce the storage size and thus meet C3. We use
in terms of software development. This is important especially      a simple flat schema that encodes a single DNS record as one
because it provides the best guarantees for the robustness of
the system (challenge C4) which is a key requirement for             1 For an in-depth introduction to Hadoop, see [4].
long-term data collection (goal G5). Secondly, our intuition         2 http://avro.apache.org/
1880                                                    IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 34, NO. 6, JUNE 2016



row, with sparse storage. This means that only fields belonging
to the particular DNS record type that is being stored are
filled, other fields are assigned a null value. This approach
was selected over nested structures because it is simple to
map to most database paradigms. As a second step, to further
improve analysis performance, measurement data is converted
to the Parquet3 columnar storage format in situ on a Hadoop
cluster on which data is analysed. Traditional row-oriented
databases are optimised for access to all the data in a single
row. Queries that aggregate data from many rows and that, for
                                                                  Fig. 1.   High-Level Architecture.
instance, accumulate counts based on filters on certain columns
are typically inefficient on this type of database. A columnar
storage system stores all data in a single column sequentially.
This makes aggregation across a single or a few columns much      The domain names in a TLD are stored in a separate database
more efficient. Additionally, because data in a single column     per TLD. Each database has two tables, one for the set of
uses the same data type and is typically made up of similar       active domains (i.e. the current state of the DNS zone), and
values, sequential columnar data can be compressed efficiently    one with all domains seen since the start of the measurement.
using e.g. run-length and delta encoding techniques.              The latter table reflects developments in the zone and stores
    There are two reasons for this two-tiered approach. First,    timestamps for when a domain name was first seen, when it
storing measurement results in the Avro format with the           was last removed from the zone, and when it reappeared in
schema discussed above makes this data suitable for separate      the zone (the latter two are only present if applicable). This
long term archival (see III-B3 below). The row-oriented nature    design decision means that the Stage I database can be used for
of the Avro schema means that the data can easily be converted    stand-alone analysis of changes in the TLD zones. This makes
to future database paradigms. Second, the Avro files are          some forms of analysis more efficient, which contributes to
structured such that they can also be analysed outside of         achieving goal G6.
a Hadoop cluster. All results relating to a single domain name       2) Stage II - Measurement: The second stage has three
are stored sequentially in an Avro file. Knowledge of this        functional components. The first is a cluster manager that
structure allows for development of efficient analysis tools      takes care of dividing work across the second component,
without the help of the Hadoop ecosystem. While performance       a cloud of worker nodes. The third component is a metadata
will be less than on a Hadoop cluster, this makes the data        server. It maintains up-to-date IP address to autonomous
usable to researchers who do not have access to such resources.   system (IP-to-AS) mappings as well as Geo IP data.
    To analyse the data collected by the measurement system,         The cluster manager collects chunks of work from the
we use the Apache Impala4 engine. This allows us to perform       database. A chunk consists of a set of domains that were last
batch-based analyses using SQL queries. The optimal batch         measured before midnight UTC. This ensures that each domain
size depends on the complexity of the query; in general,          is queried exactly once per day (goals G1, G4). Chunks are
processing is done in batches per day or per calendar month.      added to a pool of work to be performed, and the domains
As an example, the analyses we performed for the case studies     in each chunk are marked as checked out in the database.
discussed in Section V took under 2 hours each, processing        As workers process chunks of work, the cluster manager takes
over 511 billion data points. In the future, we will explore      care of administrative tasks, managing the pool of available
additional technologies, such as Apache Spark,5 which allows      work, and updating the database upon job completion by
for streaming processing as the measurement data comes in.        workers. It also monitors measurement progress and will
                                                                  reassign a chunk to a new worker if its current worker takes
B. System Design and Implementation                               too long. This prevents worker crashes from causing parts of
                                                                  the measurement to fail (challenge C4).
   Given the design considerations discussed in the previous         Worker nodes obtain chunks of work from the cluster
subsection and given the goals and challenges outlined in         manager, perform the queries specified in Table I for each
Section II-B we arrived at the design as depicted in Figure 1.    domain in the chunk and collect the results. Workers store all
The figure shows an overview of the entire system and             resource records included in the answer section of the DNS
identifies each of the three stages the system is divided         response, including all DNSSEC signatures, CNAME records
into with a grey rectangle. Each stage is described in detail     and full CNAME expansions. Upon completion of a chunk,
below.                                                            the worker reports back to the cluster manager and obtains
   1) Stage I - Input Data Collection: Stage I collects input     new work. The worker also enriches the collected data based
data, consisting of full DNS zones for the TLDs measured          on available metadata (IP-to-AS and Geo IP) and submits the
(Table II). New zone data is collected once per day, after        measurement results to the storage system in Stage III. Finally,
which a daily delta is computed (domains added and removed).      a worker node will check in with the metadata server to
 3 http://parquet.apache.org/                                     obtain new metadata if available. Worker nodes are generic
 4 http://impala.io/                                              components; this helps meet goal G7 as additional workers
 5 http://spark.apache.org/                                       can be deployed easily to increase measurement throughput.
VAN RIJSWIJK-DEIJ et al.: HIGH-PERFORMANCE, SCALABLE INFRASTRUCTURE FOR LARGE-SCALE ACTIVE DNS MEASUREMENTS                       1881



   The cluster manager and worker software were                                                 TABLE II
custom-developed (in C) for this measurement system.                                 I NPUT Z ONE C HARACTERISTICS
The worker uses LDNS6 for all DNS-specific processing
(issuing queries and parsing query results). To reach goal G2
and challenge C1, workers run multiple query threads. This
prevents workers from prolonged inactivity if queries time out
(which may halt a querying thread for up to 30 seconds). Each
worker node also runs a local DNS resolver for which we
selected Unbound7 as software. Caching by this resolver helps                                  TABLE III
reduce the query load on the global DNS (challenge C2).                            S TAGE II M EASUREMENT D URATION
Caching of infrastructural information, such as the IP addre-
sses of authoritative name servers, is particularly useful,
as large numbers of domains run by a single operator tend
to share the same authoritative servers. To ensure fresh data
is collected each day, the resolver caches are configured to
expire every day. In addition to caching, another important
function of the DNS resolver is distributing queries evenly
over authoritative name servers, which is especially important
to reduce the load on top-level domain servers. Unbound            regulated under contracts9,10 with the registry operators of
strikes a good balance between query round-trip time (RTT)         these TLDs. Table II lists the characteristics of each zone.
and distribution of queries over multiple authoritative name
servers by randomly selecting authoritative name servers with      A. Performance
an RTT below 400ms [5]. As Section IV-B will show, this
results in a good distribution of queries over top-level domain       Stage I retrieves each TLD zone twice a day, extracts the
servers.                                                           list of domain names from each TLD zone, and computes
   Finally, as discussed in Section III-A, Stage II of the         the delta relative to the previous version. It then updates the
measurement system is based on virtual machines. These             databases for each TLD. The rightmost columns of Table II
currently run on top of a private cloud infrastructure based       show the average running times for Stage I over 2015 as well
on OpenStack.8 While we run a large number of worker               as the standard deviation. The variability in running times
nodes, as will be discussed in the next section (IV), these        for .com and .net is caused by intermittent throttling of
consume minimal resources. In the current setup, for each          the zone file download by registry operators. Stage I runs
worker only a single CPU core, 2GB of RAM and 5GB of               are scheduled to complete before the cluster manager starts
disk are allocated.                                                checking out batches of work for Stage II. The two daily runs
   3) Stage III - Storage and Analysis: Stage III takes care       along this schedule guarantee that new domains are part of the
of two tasks. First, data is copied from the aggregation point,    measurement within 24 hours of appearing in a TLD.
where workers deposit data, to long-term storage. This serves         Table III shows the configuration and average measurement
two purposes: safeguarding a backup copy of the data on            times for Stage II over the period March-December 2015. The
reliable storage redundantly distributed over two locations, and   table shows the number of workers per domain, the average
retaining the unmodified source data as measured. Second,          measurement time per batch, and the total duration of a single
data is copied onto a dedicated Hadoop cluster, which we use       day measurement. For the latter two values, the mean as well
for analysis. During the copying process, the data is converted    as the standard deviation is displayed. As shown, the average
to the Parquet format discussed in Section III-A3 above to         measurement time per batch varies significantly between
enable efficient analysis of the data later on.                    TLDs. Closer examination reveals two reasons for this. For
                                                                   .com, the higher average duration is due to certain batches
                                                                   being dominated by domains registered from China. Per query
                IV. O PERATIONAL E XPERIENCES                      network latency causes these batches to have significantly
                                                                   longer measurement times. The average round-trip time (RTT)
  This section discusses operational experiences with the          per query for these batches is up to 7 times higher than average
measurement system. It covers what data we currently collect,      RTT. For .net, the duration per batch is higher because the
provides performance metrics, and discusses the impact of the      RTT for queries is about a third higher than for .org on
measurement on the global DNS infrastructure. Stage I of the       average. There appears to be no discernible cause for this; it
measurement system became operational in July 2014, while          is most likely due to a difference in the infrastructure of the
Stages II & III have been operational since February 2015.         TLD. As Table III shows, the system manages to perform a full
  We obtained access to the zone files of the .com, .net and       measurement well within a 24-hour window, meeting goals
.org generic top-level domains. Access to these zone files is      G1, G2 and G4. The total measurement time per day, however,
 6 https://www.nlnetlabs.nl/projects/ldns/                           9 For .com and .net see http://www.verisigninc.com/en_US/channel-
 7 http://unbound.net/                                             resources/domain-registry-products/zone-file/index.xhtml
 8 http://www.openstack.org/                                         10 For .org see http://pir.org/resources/file-zone-access/
1882                                                       IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 34, NO. 6, JUNE 2016



                            TABLE IV                                 stalling on misconfigured domains. The second metric is the
                   S TAGE II R ESULT S TATISTICS                     average percentage of domains for which no data could be
                                                                     obtained. As shown, only about 0.9% of domains fail to return
                                                                     any results to queries; the name servers for these domains
                                                                     are either misconfigured, or the domains are so-called lame
                                                                     delegations (domains for which none of the delegated name
                                                                     servers respond to queries). There appears to be a downward
                                                                     trend in the number of failures over the current measurement
varies substantially. This can be explained by two effects. First,   period, indicating that more queries succeed. Finally, looking
stage I runs twice per day in order to ensure that new domains       at the amount of data produced per day shows that the data
become part of a measurement within 24 hours. As a result            compression discussed in Section III-A3 works well, achieving
of this, there are occasional measurements for a small number        a stable average compression rate of 1 : 7.4. From the start of
of batches at the end of the day. The total measurement time         the measurement in February 2015, the system has collected
is computed as the time between the first measured domain            over 10TB of compressed data. As our current setup can store
on a day and the last. Thus, these late night batches skew the       up to 50TB of data, goal G5 is also met.
total measurement time. Second, all three TLDs included in
the measurement have grown over the period for which the             B. Impact on the DNS
value was computed, leading to longer overall measurement               As discussed in Section II-B (challenge C2), we have to
times at the end of the period. Nevertheless, even the longest       ensure that the measurement does not impose an unacceptable
measurement (for .com) has ample room to run longer while            burden on the global DNS infrastructure. There are two
still remaining within a 24-hour window. Furthermore, during         reasons for this. First, we consider it ethically unacceptable
the initial tuning of the system, we experimented with the           if the measurement were to put significant load on individual
number of workers per domain to bring down the measurement           DNS servers. This might negatively impact DNS performance
time. There is a strong relation between the number of workers       for ‘real’ users. Second, the contracts under which we gained
and the average duration of the measurement, despite the fact        access to the TLD zone files for .com, .net and .org
that worker VMs share hardware and network infrastructure.           all stipulate that it is not allowed to run “…high volume,
We can thus meet goal G7 and cope with growth in the                 automated, electronic processes that send queries or data to
number of domains by adding additional workers. The average          the systems of [the] Registry Operator … except as reasonably
batch duration and overall measurement time are monitored            necessary…”. While this clause pertains mostly to the registry
continuously so additional workers can be provisioned on time        service itself and is in spirit intended to stop aggressive
to remain within the 24 hour window set in goal G4. CPU              scanning of registry data in order to claim domain names that
utilisation of the workers is also monitored and we aim for an       have also been registered in other TLDs, we nevertheless also
average utilisation between 25% and 50%, to strike a balance         apply it to our measurement and strive to minimise the load
between keeping room for brief bursts of high activity while         on the DNS servers operated by the TLD registries.
not underutilising resources. In general, around a quarter of           An obvious way of limiting the load imposed by the
CPU use on the worker is due to our measurement application          measurement is to actively rate limit queries. We chose not
while the other three quarters are used by Unbound.                  to do this for two reasons. First, to support this form of
   Table IV gives an overview of daily results. The left-hand        throttling, modifications to the standard DNS resolver software
side of the table shows the statistics for December 31, 2015.        we use would be required. Second, the query load is not
The first column shows the total number of results per               distributed evenly over authoritative name servers because of
TLD, followed by the number of domains for which data                the hierarchical nature of the DNS. Servers higher up the DNS
was successfully collected. The next two columns show the            hierarchy, i.e. authoritative name servers for top-level domains,
size of the collected data per TLD. The right-hand side              typically receive many more queries because they have to be
of the table shows two average metrics over the period               consulted to find the specific authoritative name servers for
March-December 2015. These metrics are an indication of              every domain name measured. Conversely, these servers higher
the stability of the measurement. Both metrics vary only             up the DNS hierarchy are designed and configured to handle
slightly over the ten-month period. The first metric is the          many more queries. Thus, we would have to apply a different
average number of results per domain. As the table shows,            rate limiting policy to these servers, making the measurement
this number is lower than the 14 queries performed for each          system much more complex. Instead, our approach is to
domain (Table I). There are two reasons for this. First, only        analyse the impact of the measurement, to show that our
data in the answer section of a DNS response is recorded. If the     system design makes rate limiting unnecessary.
name exists but no record of the queried type exists for this           To gauge the impact of measurements, flow data was
name, the server will return a response with an empty answer         collected for the network from which the measurement
section (a NODATA answer). Second, results for queries that          operates. The infrastructure is hosted by SURFnet,11 which
failed with a response code other than NOERROR (the query            collects sampled flow data from its core routers with
succeeded) or NXDOMAIN (the queried name does not exist)             a sampling rate of 1 : 100. While sampling means some flows
are discarded. If another response code is returned, further
queries for the domain are aborted to prevent workers from            11 The National Research and Education Network in the Netherlands.
VAN RIJSWIJK-DEIJ et al.: HIGH-PERFORMANCE, SCALABLE INFRASTRUCTURE FOR LARGE-SCALE ACTIVE DNS MEASUREMENTS                                 1883



                                                                           from Verisign13 suggest that the actual figure is probably
                                                                           lower. Given that the measurement generates some 2 billion
                                                                           queries per day, this would account for between 0.3%
                                                                           and 1.6% of all queries. Also, in private communication,
                                                                           Verisign has indicated that they see the measurement and that
                                                                           while it is a non-trivial amount of traffic, it is not problematic.
                                                                           The next group of top talkers receives less than 200 queries
                                                                           per second. Closer examination shows all of these belong to
                                                                           companies that practice domain parking.14 While we have no
                                                                           data on the infrastructure of these companies, it is safe to
                                                                           assume that a query rate of less than 200 queries per second
                                                                           can easily be handled by a name server. One thing should be
                                                                           noted: the figures provided are averages over one measurement
Fig. 2.   Measurement flows versus other flows from the SURFnet network.
                                                                           period, meaning there may be peaks during which more traffic
                                                                           is sent. While it is hard to quantify to what extent such peaks
                                                                           occur, they are most likely not extreme as that would have
                                                                           showed up in Figure 2.
                                                                              This analysis demonstrates that the measurement does not
                                                                           impose an excessive burden on the global DNS infrastructure
                                                                           (challenge C2). Nevertheless, the load is significant, which
                                                                           makes it undesirable that large numbers of researchers start
                                                                           running similar measurements. Therefore, we pay specific
                                                                           attention to data sharing in Section VII.

                                                                                                    V. C ASE S TUDIES
                                                                              This section contains two case studies that cover the
                                                                           questions regarding the use of cloud mail service providers
Fig. 3.   CDF showing the distribution of flow rates to individual IPs.    introduced in Section I. These serve to validate the results
                                                                           our measurement system produces and to demonstrate how
                                                                           measuring the DNS can be a valuable instrument that provides
(especially very small ones) will be missed, it provides a good            insight into operational practices on the Internet.
picture of the top talkers. We are interested in these, since they
are the systems on which the highest query burden is imposed.              A. The Growing Use of Cloud e-Mail Service Providers
To get a feeling for the query volume that the measurement
                                                                              E-mail is one of the oldest services on the Internet.
generates, we compared the query volume to that of the entire
                                                                           Where up until the mid 2000s mail was either hosted on
SURFnet network. Figure 2 shows this comparison; the traffic
                                                                           premises or a service provided by the ISP, there is nowadays
volume from the measurement system exceeds the regular
                                                                           a trend to outsource e-mail to cloud service providers. In this
DNS traffic from the SURFnet network. This network has
                                                                           context, we discern three classes of service provider. First,
over 1 million end users in some 180 institutes for higher
                                                                           hosting providers offer domain registration, web hosting,
education and research on it, so the query volume generated
                                                                           (virtual) private servers and e-mail. These providers often
by the measurement system is quite significant.
                                                                           provide basic e-mail services with few user mailboxes or
   To quantify how much traffic individual IP addresses
                                                                           the option to forward mail to an address set by the user.
receive, we examined outgoing flows for 24 hours ordered
                                                                           Second, cloud providers offer fully hosted office ICT services.
by average number of packets per second (pps).12 Figure 3
                                                                           Their service offering in the e-mail space is often rich,
shows the top 1% of a CDF for the flow rate in pps.
                                                                           allowing customers to provision e-mail accounts for all
What is immediately evident is that there are very few flows
                                                                           their users and integrating every day office requirements
with a high pps rate. Second, no flow exceeds 400 pps.
                                                                           like calendaring and document sharing and editing. Third,
Only 35 IPs are true top talkers (more than 100 pps).
                                                                           protection services focus on protecting e-mail against malware,
Unsurprisingly, the top of the list consists exclusively of
                                                                           phishing, spam and other malicious activity. They process
gTLD DNS servers for .com and .net. On average, each of
                                                                           e-mail to filter unwanted content and forward sanitised results
these servers (there are 13) receives ±400 queries per second.
                                                                           to another mail service. This case study focuses on the
A study from 2011 [6] reports that one particular gTLD DNS
                                                                           second category, cloud providers. Based on data collected
server receives over 900 million queries per day (±10,400
                                                                           by our measurement platform over the ten-month period
per second). Under the conservative assumption that the query
                                                                           between March and December of 2015, we study the use of
load did not increase since 2011, our measurement would
                                                                           such services in the .com top-level domain.
add 3.8% to the query load of that server. More recent figures
                                                                            13 http://www.verisign.com/assets/infographic-dnib-Q32015.pdf
  12 The flow rate was adjusted to correct for the 1 : 100 sampling.        14 https://en.wikipedia.org/wiki/Domain_parking
1884                                                              IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 34, NO. 6, JUNE 2016



                                                                             (mentioned above) is an Office 365 reseller since 2014.15
                                                                             A staggering 74% of the growth in number of domains using
                                                                             Office 365 can be directly attributed to domains registered
                                                                             through GoDaddy. Also of interest is the slow decline of
                                                                             Yahoo. While we did not look into this in detail, we note
                                                                             that Yahoo has regularly been in news headlines over the past
                                                                             two years as struggling.
                                                                                The measurement system is not only suited to one-shot
                                                                             analyses and time series, but can also be used to detect
                                                                             significant anomalies in the DNS name space. To illustrate
                                                                             this, we discuss an example anomaly encountered while
                                                                             performing the analysis of MX records above. In the middle
                                                                             of May 2015 a sharp decline occurred for one of the
Fig. 4. Relative growth in use of cloud e-mail providers for the .com TLD.
                                                                             top MX SLDs, from 2.51M domains advertising this record
                                                                             to 1.27M. While the provider the MX SLD belongs to is not
                                                                             a cloud mail provider,16 we investigated the drop nevertheless,
   To identify which e-mail providers handle e-mail for the                  to ensure that this anomaly was not caused by problems
most domains in the .com TLD, we examined the Mail                           with the measurement. Interestingly, it turns out that this
eXchanger (MX) records in the DNS. The first step in the                     MX SLD is associated with a service that appears to be
analysis identified the top MX records used by domains                       targeted at companies specialised in domain parking.14 The
in .com by examining all data points for a single day                        goal of the service is to respond to e-mails sent to parked
(March 1, 2015) in the data set. MX records were grouped                     domains. The assumption behind this appears to be that users
by second-level domain (SLD) to filter out multiple records                  may erroneously send e-mail to parked domains; rather than
that point to hosts within the same service provider. For                    returning a standard error message, the service will return
example, the SLD for Microsoft’s Office 365 cloud service                    a customised error containing advertisements. The sharp drop
offering is outlook.com. We manually classified the results                  in May is caused by a mass change in MX records previously
of this analysis to determine which service provider the                     pointing to this service. We did not analyse the rationale for
MX records belong to and in which of the three classes of                    this change further, but leave this to future study.
service provider they fall. Looking at cloud providers, we find
that on March 1, 2015 the top three consists of what we would
                                                                             B. Sender Policy Framework (SPF) Practices
term the usual suspects: Google (serving 4.09M domains),
Microsoft Office 365 (948k domains) and Yahoo (609k                             A common problem with e-mail is illegitimate sending
domains). Note that, while these are large numbers, cloud                    of e-mails that seemingly originate from a certain domain
providers are not the dominant mail handler. The most                        but are in fact sent by a rogue or compromised mail server
common MX record (±27M) by far for domains in .com                           with no relation to that domain. To combat this, the Sender
points to GoDaddy, a large domain name registrar and hosting                 Policy Framework (SPF, standardised in RFC 7208 [1]) was
provider.                                                                    introduced. SPF allows domain owners to specify which
   In the introduction to this paper we asked the question:                  servers may send e-mails on their behalf, and as such helps
“which cloud e-mail provider sees the fastest growth?”.                      combat forgery. Domain owners publish SPF information17 in
Intuitively one might answer “Google”. Surprisingly, however,                the DNS by means of a TXT record (cf. Table I). This case
that is not the case. Both in absolute numbers as well as in                 study evaluates the use of SPF by domains that use one of
relative growth, Microsoft grows the fastest between March                   the three large cloud e-mail providers from the previous case
and the end of December 2015. In absolute numbers, Microsoft                 study.
went from 948k domains using their service to 1.44M,                            Like the first case study, data was analysed over a ten-month
Google went from 4.09M to 4.57M, and Yahoo dropped                           period to determine the presence of SPF information for
from 609k to 549k. Figure 4 shows the growth relative to                     domains that use either Google, Microsoft, or Yahoo to handle
the starting point of the analysis (March 1, 2015) in the                    their e-mail. Figure 5 shows the result of this analysis. The
number of domains that use one of the three cloud mail                       lines in the figure represent the fraction of domains that use
providers. Again, Microsoft is by far the fastest grower.                    either Google or Microsoft and that publish SPF information in
However, there is a twist to that figure. The blue line shown for            the DNS. Yahoo is not shown in the figure as less than 0.4%
Microsoft is an aggregate of domains that use Windows Live                   of domains that use Yahoo’s mail service publish SPF
(formerly Hotmail) and Office 365. Microsoft has discontinued                information. Significant numbers of both users of Google’s
Windows Live as a brand for mail services and this is                        as well as of Microsoft’s services publish SPF records.
visible in the data. The dashed line shows the decline in
                                                                               15 http://www.computerworld.com/article/2487663/enterprise-applications/
use of Windows Live (hotmail.com). Looking purely at
                                                                             godaddy-touts-simplicity-over-price-as-it-launches-office-365-sales.html
Office 365 (dashed-and-dotted line), Microsoft’s growth is                     16 For ethical reasons, we do not disclose the name of the company as it is
even more noticeable. One explanation for Microsoft’s fast                   not a large publicly traded company.
growth can be that the large registrar and hoster GoDaddy                      17 http://www.openspf.org/SPF_Record_Syntax
VAN RIJSWIJK-DEIJ et al.: HIGH-PERFORMANCE, SCALABLE INFRASTRUCTURE FOR LARGE-SCALE ACTIVE DNS MEASUREMENTS                                     1885



                                                                         the authoritative name servers for the .com and .net TLDs.
                                                                         Pappas et al. [8] study the effect of configuration errors on
                                                                         the DNS; notably, they perform a number of one-shot active
                                                                         measurements that sample around 10% of the domains in the
                                                                         .com TLD.
                                                                            Examples of studies examining the DNS to uncover
                                                                         underlying behaviour of, or on, the Internet can, e.g., be found
                                                                         in the security space. Works by Bilge et al. [9] and
                                                                         Perdisci et al. [10] study malicious domain names and botnets,
                                                                         respectively.

                                                                         B. Passive Versus Active Measurements
Fig. 5.   SPF usage growth for cloud e-mail providers in the .com TLD.      The most well-known method for passive DNS
                                                                         measurements is passive DNS (pDNS) [11]. In most cases,
                                                                         pDNS is used to capture DNS traffic between a recursive
There is, however, a surprising difference between
                                                                         caching name server (resolver) and the authoritative name
the two. As the figure shows, around 31.3% of domains
                                                                         servers it communicates with. This ensures that the privacy
that use Google publish SPF information, growing to 34.4%
                                                                         of users of the resolvers where data is captured is preserved.
at the end of the period. For Microsoft these figures are
                                                                         There are large scale deployments of pDNS that capture
significantly higher, growing from 88.1% to 92.4%. Both
                                                                         data at many vantage points. Notable examples are Farsight
Microsoft and Google provide instructions on how to publish
                                                                         Security’s DNSDB18 and the pDNS infrastructure operated by
SPF information when using their service. We have not
                                                                         CERT.at.19 These large pDNS deployments are often used in
examined in detail why this difference in SPF deployment
                                                                         operational security contexts. They are commonly operated by
occurs. One possible explanation is that the majority of
                                                                         or for Computer Security Incident Response Teams (CSIRTs).
domains that use Microsoft’s Office 365 do so via resellers
                                                                         Research that relies on pDNS often focuses on security (e.g.
that set the appropriate SPF records automatically. For
                                                                         the two papers discussed in the previous subsection [9], [10]).
example, of domains using Office 365 that are registered
                                                                         In addition, pDNS is also used to study operational aspects
through GoDaddy, 98.8% publish SPF information. This is
                                                                         of the DNS. In this case pDNS is often deployed at specific
certainly worthwhile of further study as the use of SPF is an
                                                                         vantage points, for example, [12] and [13] study DNS traffic
important tool in combating e-mail fraud.
                                                                         for the .nl and .it TLDs respectively. Finally, pDNS data
                                                                         can be used to enhance other network measurements. For
            VI. BACKGROUND AND R ELATED W ORK                            example, Bermudez et al. [14] use DNS data to tag network
   Measuring the DNS has a number of dimensions. In partic-              flow data.
ular, we identify the following: the measurement goal, passive              In contrast, active measurements, such as the system we
and active approaches, “one-shot” versus measurements over               introduce in this paper, work by sending targeted queries to the
time and vantage points of the measurement. We note that                 DNS. There are fewer examples of active DNS measurements
these dimensions are not necessarily independent; for instance:          in the literature. Examples include work by Schomp et al. [15]
in most cases passively collecting DNS data only makes                   who use active scans to investigate the client-side DNS
sense if the measurement is distributed, while collecting data           infrastructure. They perform these scans by randomly selecting
at authoritative name servers is probably limited to a few               IPv4 addresses and address blocks to find certain types of
vantage points as it is difficult for researchers to gain access to      DNS servers. Their goal is to characterise the behaviour of
such data sources. In the next subsections we describe these             the DNS servers themselves, not to collect DNS content.
dimensions and discuss past and present research efforts in              Earlier work by the authors of this paper [3], [16] used active
measuring the DNS in the context of these dimensions.                    DNS measurements to study aspects of the DNSSEC protocol.
                                                                         Zhu et al. [17] study the deployment of DNS-based
A. Goal of the Measurement                                               Authentication of Named Entities (DANE) by actively sending
   The DNS can be measured to study the behaviour of the                 DNS queries for all DNSSEC-signed domains in .com
DNS infrastructure itself (e.g. security, resilience, …), or it can      and .net.
be measured because it provides information about operational               When compared to existing work that uses active
practices on the Internet (for example the presence of AAAA              measurements, the approach taken in this paper stands out
records says something about IPv6 deployment). A notable                 in two ways. First, our approach is generic, that is: not
example (on account of scale and running time) of studying the           specifically designed to study a single aspect of the DNS or
DNS itself is the Internet Domain Survey [7]. This automated             the Internet. Second, the scale at which we measure is orders
survey publishes statistics on the number of IP addresses that           of magnitude larger than previous studies that use active DNS
have a name associated with it in reverse DNS and has been               measurements.
running since 1987. Another example is a study by Osterweil               18 https://www.dnsdb.info/
et al. [6] that examines the day-to-day performance of one of             19 The Austrian National CERT team, http://http://www.cert.at/index_en.html
1886                                                     IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 34, NO. 6, JUNE 2016



   Current passive DNS deployments, such as the                    would have a significant and possibly disruptive impact on
aforementioned DNSDB and CERT.at systems, are comparable           the Internet. This means that we feel an obligation to make
in scale to our active measurement approach. Where pDNS            our data accessible to other researchers. We cannot make all
differs from our approach is that pDNS systems collect             our measurement data publicly available due to restrictions
dynamic DNS data that is the result of queries by end clients.     in the contracts under which we gain access to data for the
Thus, pDNS databases will typically contain information on         TLDs currently measured. Nevertheless, we are working on
domain names that are actively queried by clients and will         two ways of making the data accessible:
contain more data if domains are more popular. The spread             1) We have set up a web portal20 on which we will
of TLDs covered by a large scale pDNS setup will typically               publish open access aggregate datasets. For example, all
be very diverse. In contrast, our active measurement covers              aggregate data sets for the case studies in this paper
DNS data for all domains (also domains that are unpopular)               will be released through that portal. Examples of other
in the TLDs we measure, and it has data for each of these                aggregate data sets we intend to publish are daily counts
domains for every day. Thus, our approach is complementary               of IP addresses in a TLD that geolocate to a certain
to pDNS.                                                                 country, counts of IP addresses that are inside a certain
                                                                         autonomous system (AS), the number of domains with
                                                                         at least one AAAA record (indicative of IPv6 use), etc.
C. Time
                                                                      2) We are in the process of setting up a program in which
   For certain research, it is sufficient to perform one or              researchers can visit our group with the specific purpose
perhaps a few single shot DNS measurements. This is                      of using the data we collect using the measurement
the case, for example, for the studies in [3], [13], [16],               infrastructure discussed in this paper. While the program
and [18]–[20]. All of these are based on “one-shot”                      is not ready yet, we already invite fellow researchers
measurements. Other research, however, looks at                          interested in using the data to contact us about visiting.
developments over time and thus needs DNS data collected
over a period of time. For instance, [9] and [10] use                        VIII. C ONCLUSIONS AND F UTURE W ORK
pDNS data collected over longer periods. There are also
examples of active measurements that cover longer periods,            Measuring the DNS is a potent tool for studying the
e.g. [7] and [17]. The intervals at which data is collected        day-to-day evolution of the Internet. For this reason,
varies. For pDNS, data points are scattered over time, as they     we set ourselves the task of actively collecting a long-term,
depend on live queries that arrive at unpredictable times. For     large-scale data set that covers the main top-level domains on
active measurements, this varies from twice per year [7] to        the Internet (including .com, .net and .org). When we
daily in case of the approach taken in this paper, and by [17].    started out, we had many questions about the feasibility of
                                                                   such a measurement. It was uncertain whether a sufficiently
                                                                   scalable infrastructure could be designed and implemented.
D. Vantage Points                                                  Furthermore, if such a measurement were possible, how would
   The final dimension is whether just a single or multiple        it impact the global DNS infrastructure?
vantage points are used to perform the measurement. Whether           In this paper, we discussed the challenges of performing
or not multiple vantage points are necessary depends on            such a measurement and the choices we made while designing
the measurement. For instance, measuring location-sensitive        and implementing a novel active measurement infrastructure
DNS answers from content delivery networks [21] obviously          for this purpose. We have shown that our design scales to
requires multiple vantage points, whereas measuring how            reliably measure even the largest top-level domain (.com
many domains use a certain DNSSEC configuration can be             at 123M names). Careful analysis of the traffic generated
done from a single vantage point [3], [16], [17]. Also the scale   by the measurement system shows that while it generates
of the measurement has an impact on the choice of the location     a significant amount of traffic, the load on the global DNS
and number of vantage points. Osterweil et al. [22], for           infrastructure is at an acceptable level. Measurements started
example, follow the operational status of DNSSEC deployment        in February 2015, and collect daily data for all domains in
since its rollout by means of distributed measurement points.      .com, .net and .org (around 50% of all names on the
Given the size of our daily dataset and the large amounts of       Internet). Since then, the system has collected over 511 billion
queries we produce, we believe that unbridled duplication of       data points, totalling over 74TB of uncompressed data
our infrastructure would add an unwanted burden on the DNS         (10.1TB compressed).
system. We therefore foresee distribution as a future expansion       To validate our measurement system and to illustrate the
aimed at studying specific aspects of the DNS behaviour.           value of the data it collects, two case studies on the use of
                                                                   cloud e-mail services were performed. These studies show
                    VII. DATA S HARING                             that a significant number of domains now use cloud mail
                                                                   services offered by Google, Microsoft and Yahoo. While –
   We realise that the data we collect is highly valuable for      as expected – Google serves the largest number of domains,
other researchers. Also, it is clear that while Section IV-B       surprisingly, the use of Microsoft’s Office 365 grows much
illustrates that the impact our measurement has on the global      faster. An investigation of the use of so-called SPF records
DNS infrastructure is well within reasonable bounds, if lots
of researchers were to set up similar infrastructures this          20 http://www.openintel.nl/
VAN RIJSWIJK-DEIJ et al.: HIGH-PERFORMANCE, SCALABLE INFRASTRUCTURE FOR LARGE-SCALE ACTIVE DNS MEASUREMENTS                                 1887



for combating e-mail forgery also yielded interesting results.                                   R EFERENCES
While both Google and Microsoft have detailed instructions           [1] S. Kitterman, Sender Policy Framework (SPF) for Authorising Use of
on how to configure SPF when using their cloud services, use             Domains in Email, Version 1, document RFC 7208, 2014.
of SPF lags for Google users (at only 34.4%) compared to             [2] Z. Durumeric, E. Wustrow, and J. A. Halderman, “ZMap: Fast
                                                                         Internet-wide scanning and its security applications,” in Proc. 22nd
Microsoft users (over 92.4%).                                            USENIX Security Symp., pp. 605–619, Aug. 2013.
   As the case studies show, the data we collect can provide         [3] R. van Rijswijk-Deij, A. Sperotto, and A. Pras, “DNSSEC and its
valuable insight in developments on the Internet, such as the            potential for DDoS attacks: A comprehensive measurement study,” in
                                                                         Proc. ACM IMC, 2014, pp. 449–460.
use of cloud services. However, traffic analysis has shown           [4] T. White, Hadoop—The Definitive Guide, 4th ed. Canada: O’Reilly,
that while the impact of our measurement on the global DNS               2015.
infrastructure remains within reasonable bounds, it would be         [5] Y. Yu, D. Wessels, M. Larson, and L. Zhang, “Authority server selection
                                                                         in DNS caching resolvers,” ACM Comput. Commun. Rev., vol. 42, no. 2,
inadvisable for large numbers of network researchers to run              pp. 80–86, 2012.
a similar measurement. For this reason we are establishing           [6] E. Osterweil, D. McPherson, S. DiBenedetto, C. Papadopoulos, and
a programme for visiting researchers to use the data we collect          D. Massey, “Behavior of DNS’ top talkers, a .com/.net view,” in Proc.
                                                                         13th Int. Conf. Passive Active Meas. (PAM), 2012, pp. 211–220.
and will publish aggregate statistics on a dedicated web portal.     [7] Internet Domain Survey, Internet Systems Consortium, Redwood City,
   Future Work: While our primary goal is to collect this data           CA, USA, Jul. 2015.
for research purposes, we realise that it has other applications,    [8] V. Pappas, D. Wessels, D. Massey, S. Lu, A. Terzis, and L. Zhang,
                                                                         “Impact of configuration errors on DNS robustness,” IEEE J. Sel. Areas
for instance in the security space. E.g., tracking over time what        Commun., vol. 27, no. 3, pp. 275–290, Apr. 2009.
IP address mapped to which names can be a valuable tool in           [9] L. Bilge, S. Sen, D. Balzarotti, E. Kirda, and C. Kruegel, “Exposure:
forensic investigations. While passive DNS is often used for             A passive DNS analysis service to detect and report malicious domains,”
                                                                         ACM Trans. Inf. Syst. Secur., vol. 16, no. 4, pp. 14:1–14:28, Apr. 2014.
this, we believe it is worthwhile examining if the data we          [10] R. Perdisci, I. Corona, and G. Giacinto, “Early detection of malicious
collect can somehow provide a complementary view on this.                flux networks via large-scale passive DNS traffic analysis,” IEEE Trans.
We plan to work with Computer Security Incident Response                 Dependable Secure Comput., vol. 9, no. 5, pp. 714–726, Sep./Oct. 2012.
                                                                    [11] F. Weimer, “Passive DNS replication,” in Proc. 17th Forum Incident
Teams (CSIRTs) to explore this further.                                  Response Secur. Teams Conf. (FIRST), 2005.
   Of course, we also strive to expand the coverage of              [12] C. Hesselman, J. Jansen, M. Wullink, K. Vink, and M. Simon, “A privacy
our measurements by including additional TLDs. In some                   framework for ‘DNS big data’ applications,” Nov. 2014, pp. 1–13.
                                                                    [13] L. Deri, L. L. Trombacchi, M. Martinelli, and D. Vannozzi, “Towards a
cases, such as the new generic top-level domains, we can                 passive DNS monitoring system,” in Proc. 27th Annu. ACM Symp. Appl.
gain access to the DNS zone files for these TLDs through                 Comput., 2012, pp. 629–630.
ICANN’s Centralized Zone Data Service.21 In other cases,            [14] I. N. Bermudez, M. Mellia, M. M. Munafo, R. Keralapura, and A. Nucci,
                                                                         “DNS to the rescue: Discerning content and services in a tangled Web,”
we need to collaborate with the TLD registry operators. This is          in Proc. ACM IMC, 2012, pp. 413–426.
especially the case for country-code TLDs (ccTLDs). We hope         [15] K. Schomp, T. Callahan, M. Rabinovich, and M. Allman, “On measuring
to convince these operators that collaboration is worthwhile             the client-side DNS infrastructure,” in Proc. ACM IMC, 2013, pp. 77–90.
                                                                    [16] R. van Rijswijk-Deij, A. Sperotto, and A. Pras, “Making the case for
by presenting our measurement infrastructure to them and                 elliptic curves in DNSSEC,” ACM Comput. Commun. Rev., vol. 45, no. 5,
demonstrating the value of the data both to them as well as              pp. 13–19, 2015.
to the wider Internet research community, by means of case          [17] L. Zhu, D. Wessels, A. Mankin, and J. Heidemann, “Measuring
                                                                         DANE TLSA deployment,” in Proc. 7th Int. Workshop Traffic Monitor.
studies.                                                                 Anal. (TMA), 2015, pp. 219–232.
   Finally, we note that our operational experience shows           [18] G. van den Broek, R. van Rijswijk-Deij, A. Sperotto, and A. Pras,
that measuring data for domains that are remote to our                   “DNSSEC meets real world: Dealing with unreachability caused by
                                                                         fragmentation,” IEEE Commun. Mag., vol. 52, no. 4, pp. 154–160,
measurement point (e.g. domains registered from China as                 Apr. 2014.
mentioned in Section IV-A) has a performance impact. The            [19] M. Lentz, D. Levin, J. Castonguay, N. Spring, and B. Bhattacharjee,
distributed design of the measurement system allows for                  “D-mystifying the D-root address change,” in Proc. ACM IMC, 2013,
                                                                         pp. 57–62.
placing worker nodes in different locations. We intend to study     [20] S. Castro, D. Wessels, M. Fomenkov, and K. Claffy, “A day at the root
the potential performance benefit this will give in the near             of the Internet,” ACM Comput. Commun. Rev., vol. 38, no. 5, pp. 41–46,
future.                                                                  Oct. 2008.
                                                                    [21] B. Ager, W. Mühlbauer, G. Smaragdakis, and S. Uhlig, “Web content
                                                                         cartography,” in Proc. ACM IMC, 2011, pp. 585–600.
                         ACKNOWLEDGMENTS                            [22] E. Osterweil, M. Ryan, D. Massey, and L. Zhang, “Quantifying the
                                                                         operational status of the DNSSEC deployment,” in Proc. ACM IMC,
  The authors would like to thank Xander Jansen of SURFnet               2008, pp. 231–242.
for his help in analysing the network flow data for our
measurement infrastructure.
  The research leading to these results was made possible by
OpenINTEL,20 a joint project of SURFnet, the University of                                   Roland      van      Rijswijk-Deij received the
Twente and SIDN.                                                                             M.Sc. degree in computer science from the
                                                                                             University of Twente, The Netherlands, in 2001,
                                                                                             where he is currently pursuing the Ph.D. degree
                                                                                             with the Design and Analysis of Communication
                                                                                             Systems Group. He is also with SURFnet bv,
                                                                                             the National Research and Education Network,
                                                                                             The Netherlands. His research interests include
                                                                                             network security and network measurements, with
 21 https://czds.icann.org/en                                                                a particular interest in DNS and DNSSEC.
1888                                               IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, VOL. 34, NO. 6, JUNE 2016



       Mattijs    Jonker     received the B.Sc. and                                  Aiko Pras is currently a Professor of network
       M.Sc. degrees in computer science from the                                    operations and management with the Design
       University of Twente, The Netherlands, where he is                            and Analysis of Communication Systems Group,
       currently pursuing the Ph.D. degree with the Centre                           University of Twente, The Netherlands. His research
       for Telematics and Information Technology with                                interests include network management, monitoring,
       a focus on the mitigation of DDoS attacks. His                                measurements, and security. He is a Steering
       main research interests include network security,                             Committee Member of several conferences,
       Internet measurements, and big data analytics.                                including IM/NOMS and CNSM, and a Series/
                                                                                     Associate Editor of ComMag, the International
                                                                                     Journal of Network Management, and the IEEE
                                                                                     T RANSACTIONS ON N ETWORK AND S ERVICE
                                                               M ANAGEMENT. He is the Chair of the IFIP Technical Committee on
                                                               Communications Systems and a Coordinator of the European Network of
                                                               Excellence on Management of the Future Internet (FLAMINGO).
       Anna Sperotto received the Ph.D. degree from the
       University of Twente, in 2010, with the thesis titled
       “Flow-Based Intrusion Detection.” She is currently
       an Assistant Professor with the Design and Analysis
       of Communication Systems Group, University of
       Twente, The Netherlands. Her research interests
       include network security, network measurements,
       and traffic monitoring and modeling.
