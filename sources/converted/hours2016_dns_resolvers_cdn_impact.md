                                                                     Computer Networks 109 (2016) 200–210



                                                                 Contents lists available at ScienceDirect


                                                                     Computer Networks
                                                         journal homepage: www.elsevier.com/locate/comnet




A study of the impact of DNS resolvers on CDN performance using a
causal approach
Hadrien Hours a,b,∗, Ernst Biersack c, Patrick Loiseau a, Alessandro Finamore d,e,
Marco Mellia d
a
  Eurecom, Campus SophiaTech, 450 Route des Chappes, 06410 Biot, France
b
  Ecole Normale Superieure de Lyon - Site monod, 46 Alle d’Italie - 69007 Lyon, France
c
  CAIPY, 06560 Valbonne, Fance
d
  Torre Telefonica Diagonal 00, Plaza de Ernest Lluch i Martin, 5, 08019 - Barcelona, Spain
e
  Politecnico di Torino - Corso Duca degli Abruzzi, 24 - 10129 Torino, Italy




a r t i c l e          i n f o                           a b s t r a c t

Article history:                                         Resources such as Web pages or videos that are published in the Internet are referred to by their Uniform
Received 30 September 2015                               Resource Locator (URL). If a user accesses a resource via its URL, the host name part of the URL needs
Revised 9 June 2016
                                                         to be translated into a routable IP address. This translation is performed by the Domain Name System
Accepted 17 June 2016
                                                         service (DNS). DNS also plays an important role when Content Distribution Networks (CDNs) are used to
Available online 23 June 2016
                                                         host replicas of popular objects on multiple servers that are located in geographically different areas. A
Keywords:                                                CDN makes use of the DNS service to infer client location and direct the client request to the optimal
Causality                                                server. While most Internet Service Providers (ISPs) offer a DNS service to their customers, clients may
CDN                                                      instead use a public DNS service. The choice of the DNS service can impact the performance of clients
DNS                                                      when retrieving a resource from a given CDN. In this paper we study the impact on download perfor-
Traﬃc performance                                        mance for clients using either the DNS service of their ISP or the public DNS service provided by Google
Bayesian networks
                                                         DNS. We adopt a causal approach that exposes the structural dependencies of the different parameters
Optimization
Monitoring
                                                         impacted by the DNS service used and we show how to model these dependencies with a Bayesian net-
Knowledge inference                                      work. The Bayesian network allows us to explain and quantify the performance beneﬁts seen by clients
Computer networks                                        when using the DNS service of their ISP. We also discuss how the further improve client performance.
                                                                                                                              © 2016 Elsevier B.V. All rights reserved.




1. Introduction                                                                               client is requesting. Based on the origin of the request, the author-
                                                                                              itative CDN DNS redirects the client to the optimal server. Most
    Each time an Internet user wants to access a resource, he uses a                          of the ISPs provide a DNS service, but it is now common to see
human readable name called Uniform Resource Locator (URL), con-                               customers using a public DNS service instead [10]. Clients using
taining the domain name of the administrative entity hosting this                             the DNS service of their ISP are served by a local DNS server that
resource. However, a domain name is not routable and needs to                                 often provides a more accurate location information to the CDN
be translated into the IP address of a server hosting the resource                            compared to the information communicated by a public DNS ser-
the client wants to access. This is taken care of by the DNS ser-                             vice such as the Google DNS service. Indeed, public DNS servers
vice. At the same time, many popular services such as YouTube,                                are usually further away from the clients of a given ISP than the
iTunes, Facebook or Twitter, rely on CDNs, where objects are repli-                           default ISP DNS server. There have been several studies suggest-
cated on different servers, and in different geographical locations                           ing that public DNS services do not perform as well as local DNS
to optimize the performance experienced by their users. When a                                services provided by ISPs, mainly because of the impossibility of
client accesses an object hosted by a CDN, its default DNS server                             public DNS to correctly communicate the location of the clients
contacts the DNS server of the CDN that hosts the resource the                                originating the request [1,7]. This problem is addressed with ECS
                                                                                              (edns-client-subnet) [16] but Akamai does not support it currently.
    ∗                                                                                             Studying the performance of the users accessing resources in
     Corresponding author.
     E-mail addresses: hadrien.hours@eurecom.fr, hadrien.hours@ens-lyon.fr                    the Internet is a complex task. Many parameters inﬂuence the end
 (H. Hours), erbi@e-biersack.eu (E. Biersack), patrick.loiseau@eurecom.fr (P. Loiseau),       user experience and the relationships between these parameters
alessandro.ﬁnamore@telefonica.com, alessandro.ﬁnamore@polito.it (A. Finamore),                is not always observable or intuitive. It is therefore necessary to
marco.mellia@telefonica.com (M. Mellia).

http://dx.doi.org/10.1016/j.comnet.2016.06.023
1389-1286/© 2016 Elsevier B.V. All rights reserved.
                                                H. Hours et al. / Computer Networks 109 (2016) 200–210                                          201


use a simple, yet formal model that allows us to understand the              The Appendix is available with the online version of this paper.1
role of a given parameter and its dependencies with other param-             We give references to these studies in the paper.
eters. Bayesian networks offer a simple and concise way to repre-
sent complex systems [2]. In this paper, we use a Bayesian network           2. Causal model: Deﬁnitions and usage
to represent the causal model that captures the impact of the DNS
service on the throughput performance experienced by clients ac-                 To model a complex system such as a communication network
cessing resources hosted by the Akamai CDN. Bayesian networks                and to organize the knowledge obtained from its passive observa-
capture the dependencies between the different parameters im-                tion is very challenging. Existing work typically looks for the pres-
pacting the throughput of the clients. One very interesting prop-            ence of correlation between different events observed simultane-
erty of causal models is their stability under intervention. Causal          ously (see [9] and references therein). However, correlation is not
models can be used to predict how the throughput of CDN users                causation and the detection of correlation between two parameters
would evolve if we would intervene on the different parameters in-           A and B does not inform us on how they are related. A can impact
ﬂuencing the performance of CDN users. Here an intervention con-             B, or the other way around, or an unobserved parameter can im-
sists in isolating a given parameter of the system being studied,            pact both A and B simultaneously. The difference between corre-
removing all its direct and remote causes and ﬁxing its variations           lation and causation plays an important role if we want to ﬁnd
to a pre deﬁned value or distribution. Being able to predict the ef-         out how to improve our system by partly modifying its behavior. A
fect of interventions, we can use causal models to understand the            causal approach uncovers the structural dependencies between the
observed performance of a given system and to design strategies to           parameters of the system under study. The ability to predict the
improve its performance. In this work, we infer and use the causal           effects of a manipulation of the parameters of a system is a major
model of CDN performance to understand the impact of choosing                strength of causal models as they are stable under intervention. Sta-
one DNS service instead of another. From such a model we are able            bility under intervention means that a causal model, inferred from
to explain why clients using the DNS service of their ISP experi-            the observations of a system in a given situation, is still valid if we
ence better download performance than clients using the Google               manually change the system mechanisms, redeﬁning the systems
DNS service. We are also able to indicate how to further improve             laws. The manual modiﬁcation of the system parameters is called
the performance of the clients using the DNS service of their ISP.           an intervention. Interventions consist in modifying the behavior of
    Our work differs from previous studies of DNS services in sev-           a component of the system, removing the inﬂuence of its direct
eral important points:                                                       and remote causes and manually setting its variations. The infer-
                                                                             ence of a causal model and of a causal effect [11,15] is made using
                                                                             passive observations only. The causal theory allows us to predict
                                                                             the behavior of the various parameters of the inferred model after
 • We use a causal approach that formally models the struc-
                                                                             an intervention without the need of additional observations.
   tural dependencies of the different parameters inﬂuencing the
                                                                                 In this section we present the PC algorithm [14] that is used to
   throughput obtained.
                                                                             infer the causal model of our system. We also describe the differ-
 • Observing that the clients using the DNS service of their ISP
                                                                             ent properties of a causal model as described in [11,15].
   (referred to as local DNS) experience higher throughput than
   the clients using the public DNS service (referred to as Google
                                                                             2.1. Causal model: Inference
   DNS), we can show that this performance difference is due to
   the fact that clients using the DNS service of their ISP are redi-
                                                                                For our work, we use the PC algorithm [14] to build the
   rected to closer servers. We are also able to precisely quantify
                                                                             Bayesian graph representing the causal model of our system. This
   this performance improvement.
                                                                             algorithm takes as input the observations of the different param-
 • The causal model of our system also reveals that the parame-
                                                                             eters that characterize our system and infers the corresponding
   terization of TCP (initial congestion window) of the servers ac-
                                                                             causal model. In our representation of a causal model as a Bayesian
   cessed by the users of the Google DNS plays a key role in their
                                                                             network, each node represents one parameter of our system and
   throughput performance. Besides fully explaining the observed
                                                                             the presence of an edge from a node X to a node Y (X → Y) rep-
   performance, this result also indicates how to further improve
                                                                             resents the existence of a causal dependence of parameter Y on
   the performance of the clients using the local DNS.
                                                                             parameter X.
                                                                                The PC algorithm starts with a fully connected and unoriented
                                                                             graph, called skeleton, where each parameter is represented by a
    Overall, the main contribution of our work resides in the                node and connected to every other parameter. The PC algorithm
methodology adopted and in its use of counterfactuals to under-              then trims the skeleton by checking for independencies between
stand the causal dependencies of a complex system.                           adjacent nodes:
    In Section 2, we introduce causal models and their use to
                                                                               • First, the unconditional independencies (X  Y ) are tested for all
predict interventions, summarizing some of the main concepts
                                                                                 pairs of parameters and the edges between two nodes whose
from [11,15]. We then present, in Section 3, the environment of
                                                                                 corresponding parameters are found to be independent are re-
our study and the description of the parameters constituting our
                                                                                 moved.
system. Section 4 presents our study of the DNS impact on the
                                                                               • For the parameters whose nodes are still adjacent, the PC algo-
throughput. In particular we present the causal model of our sys-
                                                                                 rithm then checks if there exists a conditioning set of size one
tem where we can observe the impact of the choice of the DNS
                                                                                 that makes two adjacent nodes independent. If this is the case,
service on the throughput. Our approach also allows us to predict
                                                                                 it removes the edge connecting the corresponding two nodes,
the improvement that could be achieved by modifying the param-
                                                                                 otherwise the edge is kept.
eterization of the servers accessed by the users of the local DNS
                                                                               • The previous step is repeated, increasing the conditioning set
service. Section 5 compares our approach to the related work and
                                                                                 size by one at each step, until the size of the conditioning
Section 6 summarizes our work and proposes directions to further
                                                                                 set reaches the maximum degree of the current skeleton (the
extend our work.
    Several methods mentioned in this paper were designed and
validated with parallel studies that are presented in an Appendix.             1
                                                                                   http://dx.doi.org/10.1016/j.comnet.2016.06.023
202                                                  H. Hours et al. / Computer Networks 109 (2016) 200–210


      maximum number of adjacent nodes for any node in the cur-                        Rule 2 (Action/observation exchange):
      rent graph), which means that no more independencies can be
                                                                                  P (y|do(x ), do(z ), w ) = P (y|do(x ), z, w ) if (Y  Z | X, W )GX Z                        (2)
      found.
                                                                                       Rule 3 (Insertion/deletion of intervention):
    The ﬁnal step of the PC algorithm consists in orienting the
edges. First, the PC algorithm orients all the V-structures, i.e. sub-            P (y|do(x ), do(z ), w ) = P (y|do(x ), w ) if (Y  Z | X, W )GX Z (W ) ,                    (3)
graphs X − Z − Y where X and Y are not adjacent, and then orients
                                                                                  where Z(W) is the set of Z-nodes that are not ancestor of any W-nodes
as many edges as possible without creating new colliders or cy-
                                                                                  in GX .
cles [11]. A node Z is a collider if it is part of an oriented subgraph
X → Z ← Y where X and Y are not adjacent. An illustration of the
                                                                                  2.2.2. Enforcing intervention with a given probability
different steps of the PC algorithm is presented in the Appendix
                                                                                      To study the impact of the DNS service on the performance
A.1.
                                                                                  seen by the clients (c.f. Section 4) we must estimate the effect of
2.2. Causal model: Properties and theorems                                        interventions on the parameters inﬂuenced by the DNS service and
                                                                                  on the parameters inﬂuencing the throughput. To do so, we cannot
    In this section we assume that we have the causal model of                    use atomic interventions since we intervene on a given parameter
our system that is represented by a Bayesian network. We focus                    by changing its distribution. If we want to predict how an inter-
on two parameters X and Y, where Y represents the performance                     vention on X affects Y, where the intervention on X is enforced
of our system and we are interested in the global effect on Y when                with the conditional probability distribution f∗ (X|Z), we obtain
intervening on X, including the effects mediated by external pa-                  [11, Section 4.2]:
                                                                                                                    
rameters also impacted by this intervention. We call this causal
                                                                                   f ( y )| f ∗ ( x|z ) =                     fY |do(X ),Z (y, x, z ) f ∗ (x|z ) f (z )dxdz.   (4)
effect the total causal effect. Details of the implementation of the                                            DX       DZ
methods presented in this section can be found in the Appendix B.
                                                                                  2.3. D-separation
2.2.1. Atomic interventions
    We denote by do(X = x ) (or do(x)) the intervention that con-                     The d-separation criterion is a graphical criterion to decide,
sists in intervening on the parameter X by ﬁxing its value to be                  by looking at the graph, if two parameters, represented by their
x. An intervention that simply assigns to X a ﬁxed value is called                nodes, are independent. D-separation associates the notion of con-
an atomic intervention. The diﬃculty of predicting the effect of an               nectedness with dependence. If there exists a directed path be-
intervention comes from the possible presence of spurious associa-                tween two nodes, the nodes are said to be d-connected and their
tions between the intervention variable and the response variable.                corresponding parameters are dependent. On the other hand, if we
A spurious association between X and Y is an association between                  condition on one of the nodes in the path from X to Y, then this
X and Y due to external parameters (∈ {X, Y }). To obtain an unbi-               node is said to block the path and X and Y are conditionally inde-
ased estimation of the effect of an intervention, we need to remove               pendent relative to this path. For X and Y to be independent, one
the effect of spurious associations. As an intervention is equivalent             must block all the paths d-connecting X and Y. When studying d-
to isolating a given parameter from its direct and remote causes                  separation, an important notion is the one of collider. The presence
and to assigning it a ﬁxed value, we need to remove the effects                   of a collider on a undirected path blocks this path. While condition-
of direct and remote causes in our estimations. Such estimation                   ing on a collider unblocks the path which can be explained by the
is complex if one needs to consider all the possible inter depen-                 fact that two independent causes become dependent if one condi-
dencies between the different parameters inﬂuencing the perfor-                   tions on their common consequence.
mance of the system being studied. However, the use of a graphical
causal model, where the different dependencies are present, makes                 2.4. Density estimation
it easy to estimate the outcome of interventions. Different criteria
(c.f. [11]) can be used to identify the minimum set of parameters                     The theory of causality [11] makes no assumption on the distri-
that block the effects of direct and remote causes when estimating                bution of the parameters. We estimate the multidimensional prob-
the effect of a given intervention.                                               ability density functions via Copulae [8], using the Sklar theorem.
    If G denotes the Bayesian graph that represents the causal re-                    The Sklar theorem stipulates that, if F a is multivariate cumu-
lationships between the parameters of our system, we use GX to                    lative distribution function with marginals (F1 , . . . , Fi , . . . , Fn ), there
denote the sub-graph of G where all the edges entering X are re-                  exists a copula C such that
moved and GX the sub-graph of G where all the edges exiting X are
                                                                                  F (x1 , . . . , xi , . . . , xn ) = C (F1 (x1 ), . . . , Fi (xi ), . . . , Fn (xn )).        (5)
removed. We can use the rules of do-calculus [11] to estimate the
distributions of the parameters of our system after an intervention                  There are different types of copulae, in our work we focus on
based on their distributions prior to this intervention. Note that                T-copulae [3] and G-copulae [13]. T-copulae present the advantage
these rules do not make any assumption regarding the distribu-                    that, by tuning the different parameters of the T-copula, one can
tions or functional dependencies of the parameters.                               better capture the tail dependencies between the different com-
    We brieﬂy recall the Rules of do calculus that will be used in                ponents of the multi-variate distribution that is modeled. This is
Section 4.2 to predict the interventions we are interested in this                highly useful in our case where the performance (e.g. the through-
work. Let P denote a (possibly multivariate) probability distribution             put of a Web user) can be strongly affected by changes to the char-
speciﬁed by the probability mass function or probability density                  acteristics of the network such as packet loss or delay. Unfortu-
function, depending on the nature of the parameters.                              nately, T-copulae are complex to parameterize, which implies that
                                                                                  more data is needed to ﬁt such model to our problem. In this pa-
Theorem 1 (3.4.1 from [11]). (Rules of do calculus) Let G be the di-
                                                                                  per, we are interested in counterfactuals such as “How would the
rected acyclic graph associated with a causal model [... ] and let P(·)
                                                                                  system behave under the condition C1 if one of its parameter was to
stand for the probability distribution induced by that model. For any
                                                                                  behave as it has done under the condition C2, knowing that C1 and
disjoint subsets of variables X, Y and Z we have the following rules.
                                                                                  C2 are exclusive ?”. Counterfactuals correspond to the predictions of
    Rule 1 (Insertion/deletion of observation):
                                                                                  complex interventions, each of which requires conditioning on sev-
P (y|do(x ), z, w ) = P (y|do(x ), w ) if (Y  Z | X, W )GX              (1)      eral variables in order to block the different spurious associations.
                                                        H. Hours et al. / Computer Networks 109 (2016) 200–210                                                 203


   We decided to use Gaussian copulae [13], which are known to                                Table 1
                                                                                              Summary of the different parameters.
be less sensitive if the amount of data available is limited (see Ap-
pendix C).                                                                                      Parameter         μ       min        max        σ       CoV
   In the bivariate case, the Gaussian copula is deﬁned as:
                                                                                                dstip             N.A.    1300       340 0 0    N.A.    N.A
Cρ (u, v ) = ρ (−1 (u ), −1 (v )),                                       (6)                 dns               N.A     1          3          N.A.    N.A.
                                                                                                dow               N.A.    4          7          N.A.    N.A.
where ρ represents the correlation matrix and  the CDF of the                                  tod (s)           7100    52,0 0 0   78,0 0 0   4400    0.1
standard normal distribution. The marginals, Fi (xi ), are estimated                            isprttavg (ms)    76      0          19,0 0 0   460     6.1
using normal kernels.                                                                           isprttstd (ms)    100     0          37,0 0 0   960     9.2
                                                                                                ispnbhops         1.8     1          3          0.51    0.3
   The choice of Gaussian copulae as well as the methods and                                    inetrttavg(ms)    26      0.48       660        27      1.0
their implementation to compute the conditional PDFs have been                                  inetrttstd (ms)   8.2     0          4700       61      7.5
designed and validated based on studies made on artiﬁcial data                                  inetnbhops        9.4     2          21         2.8     0.3
sets that are presented in the Appendix C.                                                      rwin0             0.83    0          360        11      13
                                                                                                rwinmin (kB)      31.3    0.004      65         22.5    0.9
                                                                                                rwinmax (kB)      213     17.5       2625       150     0.7
3. Experimental set up                                                                          cwinmax (kB)      150     7.3        1625       103     0.7
                                                                                                cwinmin (kB)      0.9     0.001      1.5        0.6     0.7
    In this section, we present how we do the data collection and                               retrscore         0.005   0          0.19       0.009   1.9
how we extract the parameters of interest. We deﬁne our system                                  rto (bool)        0.11    0          1          0.32    2.8
                                                                                                nbbytes (MB)      23.8    2.1        3875       138     5.7
as the set of parameters (see Section 2.1) and observe these pa-
                                                                                                tput (Mbps)       3.2     0.006      35         2.6     0.8
rameters in different situations to capture their dependencies and
infer the corresponding graphical causal model.

3.1. Experiment design                                                               nections where the LDNS is being used and for the connections
                                                                                     where the GDNS is being used.
    We collect IP packet traces at a Point of Presence (PoP) of a                       We use the following notations:
large European ISP and extract all the traﬃc directed to or com-
ing from the Akamai CDN. To model the impact of the choice of                          • Parameters with the preﬁx isp represent the isp network statis-
DNS service on the client throughput, we make three choices: i)                          tics, while the ones with the preﬁx inet represent the inet net-
We only focus on the traﬃc carried by the TCP protocol. ii) To                           work statistics.
eliminate the impact of TCP slowstart, we only consider large TCP                      • The suﬃx avg represents the average value of a given parame-
connections that carry at least 2MBytes of data. iii) As more than                       ter for a single connection (for example the average Round Trip
90% of the observed connections use either Google DNS (GDNS) or                          Time between the client and the probe is denoted isprttavg).
the DNS of the local ISP (LDNS) we consider only these two DNS                         • The suﬃx std represents the standard deviation of a given pa-
services.                                                                                rameter for a single connection (for example the standard de-
    The probe capturing the traﬃc is placed between the client and                       viation of the Round Trip Time between the probe and a server
the server. We call internal network, denoted as isp network, the                        is denoted inetrttstd).
part of the network between the client and the probe. We call ex-                      • The rto parameter is set to true if there was at least one packet
ternal network the part of the network between the probe and the                         retransmission due to a time out and to false otherwise
server, assimilated to the Internet network and denoted as inet net-                   • The retrscore parameter represents the fraction of retransmitted
work. The traﬃc was captured on two different days, a Thursday                           packets for a single connection (= retransmissions ).
                                                                                                                              total transmissions
and a Sunday, from 5.30 pm to 9.30 pm.                                                 • The parameters rwin∗ and cwin∗ represent receiver window and
                                                                                         congestion window metrics respectively.
3.2. Parameters of our model                                                           • The day of the week and time of the day are captured by the
                                                                                         variables dow and tod respectively.
    We use the Tstat software [4] to extract from the packet traces
relevant information on a per connection basis. We have about                           Destination IP (dstip), DNS (dns) and days (dow) are categorical
70 0 0 connections. We use domain knowledge to select a subset                       data for which the average value, standard deviation or coeﬃcient
of the information obtained from Tstat that represents the param-                    of variation do not exist.
eters known to impact the throughput. In addition to the infor-                         Without discussing in detail the values of the different param-
mation obtained from Tstat we collect for each connection addi-                      eters in Table 1, we would like to draw the attention to the dif-
tional information such as the DNS service used, the number of                       ference in the RTT values observed inside the ISP network and the
hops between the client and the server and the server address.2                      RTT values observed in the Internet: the average RTT value isprt-
The packet traces used for this study are conﬁdential and cannot                     tavg is almost three times as high as the average RTT value inetrt-
be shared publicly.                                                                  tavg. The use of an ADSL on the access link and the large buffers
                                                                                     used in ADSL networks not only increase the RTT but also result
3.3. Summary of our data                                                             in high variations of the RTT values observed that correspond to a
                                                                                     standard deviation of the isprttstd being more than ten times big-
    Each connection is described by 19 parameters. In Table 1, we                    ger than the inetrttstd.
present the average (μ), minimum (min), maximum (max), stan-
dard deviation (σ ) and coeﬃcient of variation (CoV = μ σ ) of each
                                                                                     4. Causal study of the impact of the DNS service used on
of the 19 parameters.                                                                throughput
    Since we are interested in comparing the performance of LDNS
users and GDNS users, Table 2 presents the statistics for the con-                   4.1. Modeling causal relationships

 2
   Since the addresses were anonymized we represented the server address by the         We use the PC algorithm [14] and the kernel based indepen-
Autonomous System (AS) number of the AS the server is located in.                    dence test from [19] to obtain the Bayesian network showing the
204                                                           H. Hours et al. / Computer Networks 109 (2016) 200–210


                               Table 2
                               Summary of the different metrics for the two DNS: Local DNS (LD) and Google DNS (GD) (dow and tod are
                               similar and provide no insight, so they were removed).

                                  Par                μ                   min               max                   σ             CoV

                                                     LD        GD        LD        GD      LD         GD         LD     GD     LD     GD

                                  isprttavg (ms)     80        61        0         0       19,0 0 0   15,0 0 0   470    440     5.9    7.2
                                  isprttstd (ms)     1100      76        0         0       32,0 0 0   37,0 0 0   920    1100    8.3   14.0
                                  ispnbhops          1.8       1.9       1         1       3          3          0.53   0.4     0.3    0.2
                                  inetrttavg (ms)    20        48        0.48      11      510        660        20     38      1.0    0.8
                                  inetrttstd (ms)    8.6       6.5       0         0       4700       1400       65     44      7.6    6.8
                                  inetnbhops         8.7       12        2         5       17         21         2.4    2.7     0.3    0.22
                                  rwin0              0.97      0.29      0         0       330        360        12     9.2    12.0   32.0
                                  rwinmin (kB)       35        12        0.004     0.03    65         65         28     14      0.8    1.1
                                  rwinmax (kB)       213       213       18        18      2625       20 0 0     150    138     0.3    0.7
                                  cwinmax (kB)       163       118       7.3       7.8     1625       738        108    72      0.7    0.6
                                  cwinmin (kB)       0.9       1.2       0.001     0.001   1.5        1.5        0.6    0.5     0.7    0.4
                                  retrscore          0.005     0.004     0         0       0.19       0.06       0.01   0.01    1.9    1.8
                                  rto (bool)         0.11      0.11      0         0       1          1          0.32   0.31    2.8    2.9
                                  nbbytes (MB)       29        7         2.1       2.1     3875       1375       150    44      5.3    6.5
                                  tput (Mbps)        3.2       3         0.006     0.007   35         29         2.7    2       0.9    0.7




                                                                                           use the LDNS service against 28% using the GDNS service, while on
                                                                                           Sunday 93% of the connections use the LDNS service against 7% us-
                                                                                           ing the GDNS service. It would be interesting to identify the clients
                                                                                           using one DNS service and compare their locations with the ones
                                                                                           of the clients using the other DNS service to better understand this
                                                                                           dependence. The day of the week may capture the difference in the
                                                                                           Internet usage and the devices used at home and at work. How-
                                                                                           ever, for privacy reasons, the IP addresses of the clients are obfus-
                                                                                           cated, which prevents us from investigating this hypothesis.
                                                                                               One of the most interesting dependencies, which motivated this
                                                                                           work, is the one between the DNS service (dns) and the external
                                                                                           RTT (inetrttavg). Our data show that most of the time, clients using
                                                                                           the DNS of their ISP are redirected to an Akamai server located in
                                                                                           the same AS. On the other hand, the clients using the Google DNS
                                                                                           service are often redirected to servers located outside the client AS
Fig. 1. Bayesian network representing the causal model of Web performance using            and even, in some cases, to a server outside of Europe.
two different DNS: the public Google DNS and the DNS of the local ISP with the
following parameters: Day of the Week (dow), Number of bytes exchanged during
                                                                                               It has been previously shown [7] that clients using the lo-
the connection (Nbbytes), ﬁrst advertised receiver window (rwin0), minimum adver-          cal DNS service beneﬁt from a redirection to servers closer than
tised receiver window (rwinmin), maximum advertised receiver window (rwinmax),             the ones of the clients using a public DNS service. Our data (see
minimum server congestion window (cwinmin), maximum server congestion win-                 Table 2) corroborate this observation since the average external
dow (cwinmax), time of the day (tod), retransmission score (retrscore), presence of
                                                                                           RTT for the LDNS service users is of 20 ms, while the users of the
time outs (rto), server IP address (dstip), number of hops between client and probe
(ispnbhops), number of hops between probe and server (inetnbhops), average exter-          GDNS service experience an average external RTT of 48 ms.
nal delay (inetrttavg), standard deviation external delay (inetrttstd), average internal       We can also see that congestion window metrics (cwinmin,
delay (isprttavg) and standard deviation internal delay (isprttstd).                       cwinmax) have a direct impact on the throughput (tput). Addition-
                                                                                           ally, the minimum congestion window (cwinmin) has the DNS (dns)
                                                                                           as direct parent. Its average value for clients using GDNS is 1.2kB
causal model of our system (c.f. Fig. 1). We brieﬂy discuss some of                        against 0.9kB for users served by the LDNS, see Table 2.
the most interesting dependencies exhibited by this model.                                     A parameter present in a causal model represents also the
    The day of the week (dow) and the time of the day (tod) are                            mechanisms captured by such parameter. This is the case of the
two nodes that have no parents, which is not surprising. The time                          cwinmin that also captures the tuning of the TCP parameters at
of the day (tod) inﬂuences the RTT between the probe and the                               the server side. Clients using the LDNS often access their objects
server (inetrttavg), which captures the peak hour effect in the In-                        from servers that are located inside the ISP network. These servers
ternet.                                                                                    could have a conﬁguration different from the servers accessed by
    In Table 1 we saw that that the variance of the internal RTT (is-                      the users of the GDNS. This hypothesis could also explain the fact
prttstd ) was much higher than the one of the Inet RTT (inetrttstd)                        that both DNS services result in a similar throughput performance
. This may lead one to expect that isprttstd has a stronger impact                         despite the difference in the RTTs observed. Other reasons could be
on the throughput than the inetrttstd. However, the causal model                           the impact of losses on the congestion window or the load of the
shows something different: we have a direct dependence between                             servers being accessed by the clients. To capture the server load,
(inetrttstd) and the throughput (tput) but not between the stan-                           we estimate the server processing time deﬁned from the time at
dard deviation of the internal RTT (isprttstd) and the throughput.                         which a server sends the acknowledgment of the client HTTP/GET
This example illustrates the ability of causal model to exhibit non                        message and the time at which it sends the ﬁrst data packet. How-
intuitive dependencies.                                                                    ever, the server processing time shows an expected value of 43 ms
    We observe that the day of the week (dow) inﬂuences the DNS                            for the LDNS users against 64 ms for the GDNS users. A higher
service used by the clients (dns). As our observations are made on                         processing time for the servers accessed by the GDNS users sug-
two days (a Thursday and a Sunday), our conclusions are a bit lim-                         gests that they are more loaded. On the other hand, the congestion
ited. However, it appears that on Thursday 72% of the connections
                                                    H. Hours et al. / Computer Networks 109 (2016) 200–210                                                                 205




                                 Fig. 2. Comparison of the throughput with the quantity of data a client can handle (rwin∗ ).



window is impacted by the loss. However in our data set, very few                4.2. Asking what-if questions
losses actually happen and no dependence is found between the
loss (retrscore) and the DNS service (dns).                                          We have seen that the Bayesian network reveals a rich set of
    It is to be expected that the internal RTT (isprttavg) is a parent           causal relationships that indicate how the different parameters im-
of the throughput. Also, the absence of a dependence between the                 pact the throughput. We will now use this model to answer what-
time of the day (tod) and the internal RTT can be explained by the               if questions using only the already collected data, i.e. without the
fact that all the observed users are using the same “internal” path              need to collect more data or perform additional experiments.
(the path from the users to the probe).                                              This reasoning used to answer what-if questions is referred to
    We see that the maximum receiver window advertised by the                    as counterfactual thinking. By asking “What would be the perfor-
client (rwinmax) has the time of the day as one of its parents                   mance of a user of theLDNSservice if one of her parameter was to
(tod). This could be due to the TCP buffer auto tuning mecha-                    behave as it does when theGDNSis used, knowing that the use of
nism [5] that adjusts the receiver window according to the quan-                 theLDNSand theGDNSare exclusive ?”, we can estimate the impact of
tity and frequency of data received by the client, which is inﬂu-                the choice of a DNS service on user performance. Such an approach
enced by the time of the day.                                                    allows to estimate the impact of choosing one DNS service instead
    There is no edge between the DNS (dns) and the destination IP                of another and, even more interesting, allows us to estimate the
address (dstip) and the object size (nbbbytes) is not connected at               impact of this choice on a given parameter that, in turn, impacts
all. This may be explained by the fact that the number of users of               the user performance. In our work, we focus on the impact of the
the LDNS service (80%) is much higher than the number of users of                choice of a DNS service on the user throughput via the impact of
the GDNS service (20%). The same percentages are observed for the                the DNS service on the CDN server location (c.f. Section 4.2.1), and
number of servers accessed by the users of the LDNS service (80%)                via the impact of the DNS service on the CDN server conﬁguration
and the number of servers accessed by the users of the GDNS ser-                 (c.f. Section 4.2.2).
vice. The difference between these percentages weakens the de-                       Since we deal with probabilities, we will compare the expected
pendence between dns and dstip. A solution to detect weaker de-                  values of the throughput3 instead of its average values4 as we did
pendencies is to increase the acceptance rate in the independence                in the previous section.
tests. However, increasing the acceptance rate implies a higher risk
of failing to reject weak independencies and should be used with
                                                                                 4.2.1. Distance and delay
caution. The independence of the object size from other parame-
                                                                                     To investigate the impact of the RTT on download performance
ters inﬂuencing the throughput is not necessarily surprising as we
                                                                                 we investigate the question: “What would have been the perfor-
consider long connections.
                                                                                 mance of a user served by the local DNS if it would have been redi-
    The two loss parameters (retrscore and rto) and the two RTT pa-
                                                                                 rected to a server whose inetrtt corresponds to the one the Google
rameters (inetrttstd and isprttavg) are four of the six direct parents
                                                                                 DNS service would have redirected him to ?”.
of the throughput, which is in line with our domain knowledge of
                                                                                     To answer this question is equivalent to predicting the effect
TCP. The additional parents are the congestion window parameters
                                                                                 of an intervention where the external delay (RTT) experienced by
of the server (cwinmin and cwinmax).
                                                                                 clients served by the LDNS is modeled by the distribution of the
    The fact that none of the receiver window metrics (rwin∗ ) is a
                                                                                 delay experienced by clients served by the GDNS; the distribution
direct parent of the throughput (tput) is not surprising. By compar-
                                                                                 of the rest of the parameters being kept identical for the LDNS ser-
ing the throughput of a given connection with the minimum and
                                                                                 vice users.
the maximum quantity of information that the client can handle
(see Fig. 2), it appears that the receiver window advertised by the
client is never limiting the throughput.                                                         
                                                                                   3
                                                                                     E[T PUT ] = DT PUT f T PUT (t put ) · t put · dt put , with DTPUT the throughput domain.
                                                                                                 
                                                                                                 N
                                                                                   4
                                                                                     μT PUT = N throughputi , with N the total number of observations.
                                                                                               1
                                                                                                 i=1
206                                                                  H. Hours et al. / Computer Networks 109 (2016) 200–210




                   Fig. 3. Evolution of the throughput distribution before and after intervening on the external delay experienced by Local DNS (LDNS) clients.



   More formally, if RTT denotes the inetrttavg parameter, LD the                                 a user performance if she would have chosen the GDNS service,
local DNS and GD the Google DNS, we need to estimate the fol-                                     knowing that in reality the LDNS was used.
lowing distribution:                                                                                  Fig. 4 shows the distribution of the external RTT for GDNS users
                                                                                                and LDNS users. Both conditional probability distributions present
f T PUT = t put |DNS = LD, do(RT T ∼ fRT T |do(DNS ) (·, GD ))                           (7)
                                                                                                  a long tail and very few values are actually observed for a RTT >
   The causal graph in Fig. 1 (cf the explanation of d-separation in                              200 ms. It is important to mention that RTT values are observed
Section 2.3) tells us that (RT T  DNS )GDNS , which implies (Rule 2                              for the LDNS users for the range [0.5ms,200ms] and for GDNS
from Theorem 1):                                                                                  users for the range [10ms,200ms]. This condition is necessary to
                                                                                                  perform the prediction preformed in this section, which is a limi-
fRT T |do(DNS ) (rt t , GD ) = fRT T |DNS (rt t , GD ).                                  (8)
                                                                                                  tation of the method used: The prediction formulated in Eq. (7) is
   To predict how an intervention on X affects Y, where the in-                                   only possible since the range of the external RTT values observed
tervention on X is enforced with the conditional probability distri-                              for GDNS users represents a subset of the range of values observed
bution f∗ (X|Z) we use Eq. (4). The causal graph in Fig. 1 (cf the                                for the LDNS users.
explanation of d-separation in Section 2.3) tells us that (RT T                                      If one wants to study the opposite intervention, where the
T PUT |DNS, T OD )GRT T . It follows, from Rule 2 of Theorem 1 that                               users of the GDNS service would be given access to servers placed
                                                                                                  at the locations of the servers the LDNS service users are redi-
fT PUT |do(RT T ),T OD,DNS (t put , rt t , tod, dns ) =
                                                                                                  rected to, the prediction would be more complex. We do not have
          fT PUT |RT T,T OD,DNS (t put , rt t , tod, dns ).                              (9)      samples to estimate f(tput|rtt, GD, tod) for some of the smallest RTT
      As a consequence, we can rewrite Eq. (7) as:                                                values (RTT < 10 ms) for which we have f(RTT|LDNS) > 0. However,
                                                                                                  this limitation should not surprise us, since it is common to many
  f (t put |LD ) f (rt t |do(GD ))                                                                machine learning problems where the amount of available infor-
            
                                                                                                  mation determines the predictions we can make. The reason why
     =                 f (t put |do(rt t ), LD, t od ) f (t od ) f (rt t |do(GD ))P (GD )
           D       D                                                                              we cannot predict the opposite intervention is due to the use of
           RT T  T OD                                                                           kernels to estimate distributions, which requires the presence of
      =                    f (t put |rt t , LD, t od ) f (t od ) f (rt t |GD )P (GD )   (10)      samples in a given region to estimate the value of the distribution
           DRT T   DT OD
                                                                                                  in this region. One possible way to overcome this problem would
using Eqs. (8) and (9).                                                                           be to develop a parametric model that allows to extrapolate the
   The result of the intervention is presented in Fig. 3. The CDF                                 different PDFs beyond the value range where the variables of our
of the throughput for the LDNS before intervention is plotted as                                  system are observed.
blue solid line and the CDF of the throughput for the LDNS service                                    It is important to note that our model considers the impact of
users after an intervention setting their external delays distribu-                               the change in the delay distribution but also the impact of the
tion to the delay distribution seen by the GDNS users is plotted as                               servers themselves, captured by the minimum congestion window
red dotted line. The throughput after invention is degraded due to                                and parameters such as the loss (retrscore) that are different be-
the higher RTTs experienced by the clients’: The expected through-                                tween the two DNS services. In fact, the inﬂuence of these param-
put for clients using the local DNS service prior to intervention is                              eters may explain that the throughput experienced, in the original
3.5 Mbps and 3.0 Mbps after intervention (14% decrease). This                                     dataset, by the users of the GDNS service is only 7% smaller than
result quantiﬁes the gain in performance that the redirection to                                  for the users of the local DNS service. To evaluate the impact of
closer CDN servers, provided by the use of the local DNS service,                                 the servers on download performance we focus on the impact of
represents.                                                                                       the minimum congestion window since cwinmin is a direct par-
   This result also illustrates the use of counterfactual thinking. We                            ent of the throughput (tput) and is inﬂuenced by the DNS service
can deduce the gain in performance for a user who chose the                                       choice (dns). Also, other parameters such as the loss parameters
LDNS service by estimating the change in performance if the GDNS                                  (retrscore and rto), the delay parameters (isprttavg and isprttstd) or
would have been chosen instead.                                                                   the maximum congestion window (cwinmax) are not inﬂuenced by
   The results obtained cannot be validated in practice as this                                   the choice of the DNS service (dns) (c.f. Fig. 1).
would require the modiﬁcation of the behavior of the local DNS
servers. In fact, this diﬃculty nicely illustrates the beneﬁt of the                              4.2.2. Minimum congestion window
causal approach: it offers the possibility to predict the effect of in-                               The minimum congestion window (cwinmin) is a direct parent
terventions that are impossible to perform experimentally. Our ap-                                of the throughput (tput), see Fig. 1. Its average value is higher for
proach allows us to estimate what would have been the effect on                                   the clients using the GDNS service than for the clients using the
                                                             H. Hours et al. / Computer Networks 109 (2016) 200–210                                        207




                                            Fig. 4. Histogram of the external RTT for the local DNS (LDNS) and Google DNS (GDNS).



LDNS service (1.2kB and 0.9kB respectively). The difference in the                        the fact that the servers GDNS service users are redirected to use
expected value of the throughput of LDNS users (3.5 Mbps) and                             higher values for their minimum congestion window.
GDNS users (3.3 Mbps) is 6%, smaller than the gain for the LDNS                               The study of the opposite intervention, where GDNS service
users being redirected to closer server, that is estimated to be 14%.                     users are redirected to servers with a minimum congestion win-
Our hypothesis is that the minimum congestion window repre-                               dow following the distribution of the minimum congestion win-
sents a difference in the conﬁguration of the servers accessed by                         dow seen by the LDNS service users, in the original dataset, is
the LDNS users and the conﬁguration of the servers accessed by                            not possible. The reason is the same as the one mentioned in
the GDNS users. To evaluate this hypothesis we estimate the causal                        Section 4.2.1. If we compare the distribution of the minimum con-
effect of the minimum congestion window on the throughput, me-                            gestion windows for LDNS service users and GDNS service users,
diated by the choice of the DNS service. This is equivalent to asking                     Fig. 6, we can notice the absence of cmin values for GDNS users to
the question: “What would be the throughput for the clients using                         estimate f(tput|cmin, GD, σ rtt ) for values of cmin where f(cmin|LD)
the local DNS if the servers they are redirected to would present the                     > 0.
same minimum congestion window as the ones Google DNS users are                               If we summarize the ﬁndings of the last two sections, we can
redirected to ?”.                                                                         say that by using a causal model and its graphical representation
    We observe from the causal graph of Fig. 1 (cf the explanation                        we were able to quantify that it is not only the proximity of the
of d-separation in Section 2.3):                                                          server that has an important impact on the throughput but also
                                                                                          the conﬁguration of the server hosting the content a client wants
 • (CW INMIN  DNS )GDNS                                                                  to access.
 • (CW INMIN  T PUT |DNS, INET RT T ST D )GCW INMIN                                          In a causal model such as the one presented in Fig. 1, a given
                                                                                          node X also represents the inﬂuence that external factors im-
    For space reasons, and because the approach is the same as in
                                                                                          pacting only this parameter have on the rest of the system. This
Section 4.2.1 for the external delay (inetrttavg), we only present the
                                                                                          means that the difference in behavior of Akamai servers that the
ﬁnal equation.
                                                                                          Google DNS redirects the clients to compared to the behavior of
    Let denote cmin the minimum congestion window (called cwin-
                                                                                          the servers the LDNS redirects the clients to may not be solely the
min in our model) and σ rtt the standard deviation of the external
                                                                                          effect of the minimum congestion window but may also be the
rtt (called inetrttstd in our model). As before LD refers to the local
                                                                                          effect of other un-observed parameters of TCP such as the addi-
DNS and GD to the Google DNS. We obtain the following equa-
                                                                                          tive increase value for each acknowledged packet. Unfortunately, we
tion:
                                                                                          have no means to validate this hypothesis.
  f (t put | LD ) f (cmin|do(GD ))
                                                                                        5. Related work
     =                f (t put |do(cmin ), LD, ts ) f (σrtt ) f (cmin|do(GD ))
         DCMIN   DσRT T
                                                                                              The two works closest to ours are WISE [18] and Nano [17].
        ×P (GD )                                                                              WISE uses, as does our work, the PC algorithm [14] to infer
            
                                                                                          a graphical causal model from which interventions are then pre-
    =                     f (t put |cmin, LD, σrtt ) f (σrtt ) f (cmin|GD )P (GD )
         DCMIN   DσRT T                                                                   dicted. However, WISE requires a lot of domain knowledge in its
                                                                                          feature selection and in the deﬁnition of external causes that guide
                                                                                (11)
                                                                                          the inference of the causal model. Also, WISE uses the Z-Fisher in-
   Eq. (11) allows the prediction of the distribution of the through-                     dependence, which assumes linear dependencies. We have tested
put for the LDNS users after an intervention when we use for                              the Z-Fisher independence criterion in our work and obtained very
the minimum congestion window the distribution seen by GDNS                               poor results as the test fails to detect parameter independencies
users. The CDFs of the pre-intervention throughput (solid line) and                       resulting in incorrect models [6]. In addition, WISE considers much
post-intervention throughput (dotted line) are presented in Fig. 5.                       simpler scenarios of intervention and requires a much larger data
We can see the gain in throughput due to the intervention on                              set. Our approach takes full advantage of the causal theory devel-
the minimum congestion windows of the LDNS servers. The ex-                               oped by Pearl [11,15] to predict interventions and counterfactuals.
pected throughput for LDNS service users after the intervention is                        Counterfactuals are very useful to understand the role of the differ-
4.6 Mbps (compared to 3.5 Mbps prior to intervention), which                              ent parameters of a system and, to our knowledge, scenarios such
represents an increase of more than 30%. This increase is due to                          as the ones presented in Section 4.2 have not been treated so far.
208                                                     H. Hours et al. / Computer Networks 109 (2016) 200–210




       Fig. 5. Evolution of the throughput distribution before and after intervening on the minimum congestion window of servers of the users of the local DNS.




                               Fig. 6. Histogram of the minimum congestion window for the local DNS (LDNS) and Google DNS (GDNS).



    Nano tries to detect network neutrality violation by assessing                   similar throughput for connections experiencing a different RTT).
the direct causal effect between the quality of experience of a user                 Second, the major contribution of the work presented in this pa-
from a given ISP and the type of content being accessed. A perfor-                   per is due to the use of counterfactuals and counterfactual thinking,
mance baseline is deﬁned based on observations made for differ-                      Section 4.2. The use of counterfactuals gives us access to a deeper
ent ISPs sharing similar conﬁgurations and then compared to the                      understanding of the causal mechanisms ruling the performance of
one observed for a particular scenario. Again, this approach uses                    the system and it allows us to quantify the impact of each of these
domain knowledge to deﬁne the possible confounders and to con-                       mechanisms on the performance of this system.
dition on these variables to remove spurious associations. Since
Nano has not derived a formal causal model, its approach has se-                     6. Concluding remarks
rious limitations since one of the confounders could be a collider
in the corresponding causal graphical model. Also, conditioning on                      The main contribution of our paper resides in the methodol-
a common effect induces a dependence between two independent                         ogy based on the inference and in the usage of a causal model
causes whose inﬂuence tries to be canceled, questioning the ob-                      that allows us to estimate the causal effect of the DNS service on
tained results.                                                                      user performance. Using a causal approach and inferring the causal
    Several papers study how the choice of the DNS service impacts                   model, which is then represented as a Bayesian graph, we are able
client performance [1,7,10]. These works rely on active measure-                     to study the causal effect of a DNS service on the TCP throughput.
ments and differ greatly in their approach and objectives from our                   We compare the performance of clients using their ISP local DNS
work.                                                                                service to the performance of clients using the Google DNS ser-
    In our previous work [6] we presented solutions to the prob-                     vice. The causal model allows to unveil dependencies that would
lem of causal model inference and to the prediction of atomic in-                    be very diﬃcult, if not impossible, to extract otherwise from the
terventions for cases where the assumptions of normality and lin-                    data. We showed that the choice of the DNS service has a strong
earity do not hold. We also validated our approach and showed for                    impact on the location of the servers the clients are redirected to,
simple systems and scenarios that it was possible to use a causal                    which in turn impacts not only the distance from clients to servers
approach to study communication network performance.                                 but also the type of conﬁguration of the servers. Distance and con-
    The work presented in this paper goes much further. First, we                    ﬁguration are captured by the dependence between the DNS and
study a more complex system with more parameters and diverse                         the RTT and the dependence between the DNS and the server min-
categories of data (including categorical data). We use the causal                   imum congestion window.
model obtained to explain non intuitive observations (namely a                          A very interesting property of causal models is their “stability
                                                                                     under intervention”. The model inferred from data following a given
                                                 H. Hours et al. / Computer Networks 109 (2016) 200–210                                                          209


distribution is still valid when we predict the effect of modifying               dence in the presence or absence of any edge in the graph we
this distribution. When comparing the performance of the users of                 obtain to give us a conﬁdence in the model. This approach be-
the local DNS and the users of the Google DNS, we can observe                     comes complex due to the number of tests to consider for a
that the performance difference cannot simply be explained by the                 given pair of nodes and no general criterion has been designed
redirection of Google DNS users to more distant Akamai servers.                   as this stage of our work.
Based on the causal graph obtained, we can formulate the hy-                    • We had to design several solutions to build a reliable frame-
pothesis that the conﬁgurations of the Akamai servers Google DNS                  work for causal knowledge inference [6] that implied an in-
users are redirected to allow them to experience a performance                    crease in complexity and resource requirements. While we have
close to the one of the local DNS service users. This hypothesis                  used very small data sets to validate our approach and to
is conﬁrmed by our prediction where we give to Akamai servers                     show its beneﬁts, there are many directions to explore to make
serving the local DNS users a minimum congestion window equiv-                    Causal reasoning work more eﬃciently on large quantities of
alent to the one of the Akamai servers serving Google DNS users.                  data thanks to the use of distributed computing. The paral-
We estimate the gain in throughput corresponding to this inter-                   lelization of the independence testing for causal model infer-
vention to be 32%. By comparison, the gain in terms of throughput                 ence [6] and the parallelization of the estimation of interven-
corresponding to the redirection of the local DNS users to closer                 tions (see Appendix B.2) ﬁt very well a Big Data approach.
servers is estimated to be only 14%.                                              Working with a bigger and partitioned data set on which paral-
    We demonstrated the potential of adopting a causal approach                   lel computing could be done, would improve the performance
using counterfactuals. Counterfactuals are one of the possible way                of the Causal knowledge inference framework we presented in
to approach Causality and we use this technique to evaluate the                   this work.
effect of a parameter on the system performance by predicting the
effect that changing its parent would have with the rest of the sys-          Acknowledgment
tem parameters left unchanged. We manage to answer questions
such as “How would the system behave under the condition C1 if one                We would like to thank Elias Bareinboim from UCLA for his ad-
of its parameter was to behave as it has done under the condition             vice and support in developing the methodology to predict coun-
C2, knowing that C1 and C2 are exclusive ?”. The ability to make              terfactuals. We also would like to thank the reviewers for their
predictions for such scenarios illustrates the power of the inherent          constructive remarks. The research leading to these results has re-
mechanisms underlying the development of Causality. Counterfac-               ceived fundings from the European Union under the FP7 Grant
tuals are relatively complex to study, explain and even more so               Agreement n. 318627 (Integrated Project “mPlane”).
to predict. However, thanks to the Bayesian network as a repre-
sentation of the causal model of our system, using counterfactuals            Supplementary material
becomes easier.
    Complex interventions, where many parameters are modi-                       Supplementary material associated with this article can be
ﬁed simultaneously, require important resources in terms of the               found, in the online version, at 10.1016/j.comnet.2016.06.023
amount of data and computational power. The results presented
in this paper document a ﬁrst successful attempt. Based on this               References
work, we are conﬁdent that the underlying tools and methods can
                                                                               [1] B. Ager, W. Mühlbauer, G. Smaragdakis, S. Uhlig, Comparing DNS resolvers in
be improved to reduce the required resources and increase both,                    the wild, in: IMC, ACM, 2010, pp. 15–21.
the accuracy of such predictions and the range and complexity of               [2] A. Darwiche, Modeling and Reasoning with Bayesian Networks, ﬁrst, Cam-
the interventions that one can consider.                                           bridge University Press, Cambridge, 2009.
                                                                               [3] S. Demarta, A. McNeil, The T-copula and related copulas, Int. Stat. Rev. 73 (1)
    We see the following directions for future work:                               (2005) 111–129.
                                                                               [4] A. Finamore, et al., Experiences of internet traﬃc monitoring with tstat, IEEE
 • By ﬁtting a parametric model we could extend the prediction                     Netw. Mag. 25 (3) (2011) 8–14.
   of counterfactuals for cases where the two conditional proba-               [5] P. Ford, A. Shelest, N. Srinivas, Method for automatic tuning of TCP receive win-
   bilities have only partial overlap.                                             dow, 2002, US Patent App. 09/736,988.
                                                                               [6] H. Hours, E. Biersack, P. Loiseau, A causal approach to the study of TCP perfor-
 • The weight of an edge, X → Y, corresponds to what is known                      mance, ACM Trans. Intell. Syst. Technol. 7 (2) (2015) 25:1–25:25.
   as the direct effect of one parameter, X on another, Y. However,            [7] C. Huang, D.A. Maltz, J. Li, A.G. Greenberg, Public DNS system and global traﬃc
   in the absence of linearity, the estimation of the direct effect of             management., in: INFOCOM, IEEE, 2011, pp. 2615–2623.
                                                                               [8] P. Jaworski, F. Durante, W. Härdle, T. Rychlik, Copula theory and its applica-
   X on Y is complex and requires predicting the effects of several
                                                                                   tions, Lecture Notes in Statistics, Springer, Berlin, Heidelberg, 2010.
   interventions [12] for each direct effect, which requires a lot of          [9] V. Mayer-Schönberger, Big Data: A Revolution That Will Transform How We
   computational resources.                                                        Live, Work and Think., John Murray Publishers, UK, 2013.
                                                                              [10] J.S. Otto, M.A. Sánchez, J.P. Rula, F.E. Bustamante, Content Delivery and the Nat-
 • Regarding a selection criterion, the absence of any assumption
                                                                                   ural Evolution of DNS: Remote DNS trends, performance issues and alternative
   regarding the distribution of the parameters and the nature of                  solutions, in: IMC, ACM, 2012, pp. 523–536.
   their dependencies prevents us from using a classical selec-               [11] J. Pearl, Causality: Models, Reasoning and Inference, Cambridge University
   tion criterion such as maximum likelihood. Two possibilities                    Press, New York, NY, USA, 2009.
                                                                              [12] J. Pearl, Direct and indirect effects, CoRR abs/1301.2300 (2013).
   could be used instead: (i) A Bootstrap approach, where, by re-             [13] M. Pitt, D. Chan, R. Kohn, Eﬃcient Bayesian inference for gaussian copula re-
   sampling the original data set to create new data sets, we could                gression models, Biometrika 93 (3) (2006) 537–554.
   infer one causal model for each data set and, by comparison,               [14] P. Spirtes, C. Glymour, An Algorithm for Fast Recovery of Sparse Causal Graphs,
                                                                                   Soc. Sci. Comput. Rev. 9 (1991) 62–72.
   derive a conﬁdence level for our model. This approach is sim-              [15] P. Spirtes, C. Glymour, R. Scheines, Causation, Prediction, and Search, second,
   ple to implement. However, the inference of the causal model                    The MIT Press, Cambridge MA 02142-1209, 2001.
   presented in this paper took up to one week running on a clus-             [16] F. Streibelt, J. Böttger, N. Chatzis, G. Smaragdakis, A. Feldmann, Exploring edns–
                                                                                   client-subnet adopters in your free time, in: IMC, ACM, 2013, pp. 305–312.
   ter of 30 machines. Therefore, a bootstrap approach requires im-           [17] M. Tariq, M. Motiwala, N. Feamster, M. Ammar, Detecting network neutrality
   portant resources in terms of computation time. On the other                    violations with causal inference., in: CoNEXT, ACM, 2009, pp. 289–300.
   hand, when creating sub-data sets, we work with smaller data               [18] M. Tariq, et al., Answering what-if deployment and conﬁguration questions
                                                                                   with WISE, in: SIGCOMM, ACM, 2008, pp. 99–110.
   sets, which has an impact on the accuracy of the results. (ii)
                                                                              [19] K. Zhang, J. Peters, D. Janzing, S. B., Kernel-based conditional independence test
   We could use the independence test p-values to obtain a conﬁ-                   and application in causal discovery, CoRR abs/1202.3775 (2012).
210                                   H. Hours et al. / Computer Networks 109 (2016) 200–210


      Hadrien Hours was born in 1986 in Aix-en-Provence, France. From September 2004 to July 2006, he did Engineering Science and Mathematics and
      Physics at the Ecole Preparatoire of Lycée Thiers, Marseille, France. He joined Télécom Bretagne in September 2006 and did one Erasmus semester
      in the Facultad de Informatica de Madrid (Spain). From 2008 to 2009, he worked for Bouygues Télécom (Aix en Provence, France) as an intern
      with Performances and Optimizations missions, along with Dimensioning and Architecture. In March 2010 he attended the Networking Track in
      EURECOM. He got his engineering diploma from Télécom Bretagne in 2011 for Engineer in Telecommunication in Networking Track. He made his
      master thesis in Technicolor Paris Research Lab on House Automation: Energy Monitoring under the supervision of the Professor Ernst Biersack
      from EURECOM and Laurent Massoulié from Technicolor. He started his PhD under the supervision of Professor Ernst Biersack and Professor Patrick
      Loiseau on the subject of A Causal Approach to the Study of Communication network performance in November 2011. He obtained his Ph.D. in
      September 2015. Since November 2016 he is a post-doc in the Dante team at ENS Lyon, France.
