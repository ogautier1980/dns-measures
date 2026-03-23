      Melting the Snow: Using Active DNS
 Measurements to Detect Snowshoe Spam Domains
                  Olivier van der Toorn∗ , Roland van Rijswijk-Deij∗ , Bart Geesink† , Anna Sperotto∗
                                                       ∗ University of Twente

                                     {o.i.vandertoorn, r.m.vanrijswijk, a.sperotto}@utwente.nl
                                                             † SURFnet

                                                      bart.geesink@surfnet.nl


   Abstract—Snowshoe spam is a type of spam that is notoriously     (blacklists). A second characteristic of snowshoe spam is that
hard to detect. Anti-abuse vendors estimate that 15% of spam        spammers want to appear as legitimate as possible, by adopting
can be classified as snowshoe spam. Differently from regular        email best practices. An example of such a best practice
spam, snowshoe spammers distribute sending of spam over
many hosts, in order to evade detection by spam reputation          is Sender Policy Framework (SPF), a technique to ensure
systems (blacklists). To be successful spammers need to appear      only authorized email servers can send email for specific
as legitimate as possible, for example, by adopting email best      domains. However, SPF requires spammers to also register and
practices, such as the Sender Policy Framework (SPF). This          configure a legitimate Domain Name System (DNS) domain.
requires spammers to register and configure legitimate DNS          Additionally, it requires them to create a DNS record for
domains. Many previous studies have relied on DNS data to detect
spam. However, this often happens based on passive DNS data.        every host that should be able to send email for that domain.
This limits detection to domains that have actually been used       This results in a domain with a large number of records. The
and have been observed on passive DNS sensors. To overcome          creation of such domains is often called crafting. Cisco [2]
this limitation, we take a different approach. We make use          reported that 15% of spam in 2014 was classified as snowshoe
of active DNS measurements, covering more than 60% of the           spam.
global DNS namespace, in combination with machine learning
to identify malicious domains crafted for snowshoe spam. Our           Spam detection has been studied intensely by the security
results show that we are able to detect snowshoe spam domains       research and anti-abuse communities. A number of studies link
with a precision of over 93%. More importantly, we are able         the use of data in the DNS to spam detection. However, this
to detect a significant fraction of the malicious domains up to     usually happens in a passive manner. The goal of this paper,
100 days earlier than existing blacklists, which suggests our
method can give us a time advantage in the fight against spam.
                                                                    on the other hand, is to detect crafted snowshoe spam domains
In addition to testing the efficacy of our approach in comparison   using active DNS measurements. Our approach combines
to existing blacklists, we validated our approach over a 3-month    active DNS measurements with supervised machine learning.
period in an actual mail filter system at a major Dutch network     The active DNS measurements are retrieved from the unique
operator. Not only did this demonstrate that our approach works     OpenINTEL platform1 , which actively queries more than 60%
in practice, the operator has actually decided to deploy our
method in production, based on the results obtained.
                                                                    of all registered domain names worldwide. We verify our
   Index Terms—<Spam Detection, Active DNS Measurements,            results by comparing them to well-known blacklists.
Blacklisting.>                                                         The main contributions of this paper are that we:
                                                                      • perform detection of domains crafted for snowshoe spam,
                       I. I NTRODUCTION                                 using active DNS measurements;
   Spam is a major problem on the Internet. In particular, the        • show that our method can identify domains earlier than
kind of spam containing URLs to malicious content, or viruses,          existing blacklists, which allows us to block spam that
is troublesome. Pfleeger and Bloom [1] have reported that the           would otherwise bypass a mailfilter;
sending of one million spam emails costs around US$250 for            • make the resulting blacklist available for researchers and
the sending party, but that on average, the time spent deleting         spam filter operators, for further study and to improve
them costs the receiving party about US$2,800 in lost wages.            detection of spam.
Spam is a cat-and-mouse game between the spammers and                  The remainder of this paper is structured as follows. Sec-
email providers. Spammers often try to bypass mail filters by       tion II discusses related work. In Section III we present
developing new methods of distributing spam. Snowshoe spam          our methodology. The datasets we use are introduced in
is one of these methods.                                            Section IV. Section V discusses our results. A real-world
   In ‘normal’ types of spam the entire burden of transmitting      deployment of our work is presented in Section VI. We
the spam messages is often put on only a few hosts. In contrast,    analyse the ethical impact of our work in Section VII. Finally,
in the case of snowshoe spam the sending is spread out over         Section VIII details our conclusions.
many hosts, to avoid detection by spam reputation systems
978-1-5386-3416-5/18/$31.00 c 2018 IEEE                              1 https://openintel.nl/
                       II. R ELATED WORK                              There exists very little related work specifically focusing on
A. Passive and active DNS monitoring                                snowshoe spam. Bhowmick et al. [16] mention snowshoe spam
                                                                    as an emerging threat. In this work, we focus on snowshoe
   Many security-related studies have looked at passively mon-
                                                                    spam in particular.
itoring DNS. Especially when done at a large scale, passive
monitoring of DNS can yield important information about the         C. Machine learning
use and security of DNS. A notable approach is passive DNS             Supervised machine learning is a way to build a predictive
(pDNS) [3], a system that monitors DNS queries and responses        model (classifier) based on labeled data. It is often used
issued from a recursive resolver towards authoritative name         to detect malicious activity on networks [17], [18]. Several
servers. pDNS is used to investigate DNS anomalies [4]–[7],         studies combine the subjects of spam detection and machine
such as domains used for spam campaigns and malware.                learning. Youn et al. [19] provide an overview of classifier
Perdisci et al. [8] used passive DNS to measure the growth of       types and their performance. Clustering and decision trees are
IP addresses in order to determine if a domain would be used        techniques frequently used [5]–[8]. Drucker et al. [20] use a
in flux service networks. The biggest advantage of pDNS is          Support Vector Machine (SVM) to classify email, based on
that it reflects live use of the DNS. However, this also means      the content, as spam or ham. In the work of Sakkis et al. [21],
that pDNS is in general usage-biased and that only anomalous        classifiers are used sequentially to increase the accuracy of the
behavior in the monitored network can be detected. In this          classification. Bhowmick et al. [16] look at how spam evolves
paper, we take a different approach. We use actively collected      and what tools emerge, or change, to combat these new types
DNS data, which allow us to detect anomalous domains at a           of spam. All techniques presented focus on the headers of an
global scale and independently from their being accessed by         email and/or the content of the email.
users.                                                                 While we also use a machine learning approach, we differ
   A few studies have already looked at how active DNS              from the state of the art in the fact that our methods is
measurements can be used to identify malicious activities.          independent from the content of an email, but it relies only
Konte et al. [9] monitor changes in DNS records of known            on domain names configurations.
spam domains to investigate at which rate and to which extent
malicious domains change their characteristics, e.g., in relation                         III. M ETHODOLOGY
to fast-flux domains. Hao et al. [10] use zone transfer records        In this section, we present our methodology. Figure 1 shows
to obtain DNS data to characterize, among others, the time          a high-level overview of our approach. From left to right, it
between registration of a malicious domain and its appearance       displays four parts (A)-(D) that together make up our detection
on a spam blacklist and the location of the name servers used       process. In addition to this, a fifth part, (E), is shown in the
for the domain. Felegyhazi et al. [11] investigate the use of       gray rectangle, which represents the training of the machine
DNS in proactive blacklisting of malicious domains. Hao et          learning classifier that our detection relies on.
al. [12] also look at the history of a domain name and the             At a high-level, our method for detection does the following.
details of new registrations to single out malicious domains.       Every day, based on data from the OpenINTEL platform (A),
While these studies share our same intuition, that is that          we perform a filtering step, called the long tail analysis (B),
malicious domains need to be registered and configured before       to extract candidate domains. We then use a machine learning
they can be used, our contribution differs in the following         classifier (C) to perform a binary prediction of domains to
aspects. First, while several other contributions are limited to    blacklist, which are then added to our Real-time Blackhole
analyzing only a handful of zones, our work covers more than        List (RBL) (D).
60% of currently registered domain names. Secondly, most               In the section ‘Building and training a classifier’ (E) we
of the previous studies start from a set of known malicious         explain the parts of Figure 1 with a gray background. These
domains, and use this for inferring general characteristics. We     parts concern the training of the classifier.
focus instead on building a model of malicious behavior using       A. DNS data collection
a machine learning approach.
                                                                       Both our training and detection make extensive use of
B. Spam                                                             data from the OpenINTEL platform. Since February 2015,
   Syed et al. [13] and Moura et al. [14] report that spam          the OpenINTEL1 large scale active DNS measurement plat-
sources can be identified using only network-based character-       form collects daily snapshots of the data in the DNS [22].
istics. Their works are based on the observation that spam          The measurement currently queries 60% of the global DNS
sources tend to be clustered in relative address proximity,         namespace. At the time of writing, the measurement covers the
e.g. in the same subnet or autonomous system. Yamakawa              zones .com, .net, .org, .info, .mobi, the new gTLDs
et al. [15] show that this address clustering also exists geo-      defined by ICANN, and a set of ccTLDs such as .nl, .se,
graphically, since large volumes of spam comes from the same        .ca, .fi, .at, .dk, .nu and .ru. For each domain name,
countries. To be effective these approaches need to observe         the measurement performs a fixed set of queries including A,
large volumes of spam to identify bad neighborhoods (tainted        AAAA, MX, TXT, etc. The result from these queries forms the
address space), and they can only perform just-in-time spam         basis for the features we use. These features are described in
identification, namely at the time spam has already been sent.      Section III-E
                          (E)                                            this list, which are not already present on the RBL, are added
   Alexa                               Training dataset                  to it. For validation purposes, all domains on the RBL are
                                                                         then checked against existing public blacklists (Table I). We
                                                                         mark it as soon as a domain on our RBL also appears on
           Blacklist                                         Blacklist
                                                                         a public blacklist. This allows us to do time analysis of our
                                                                         detections. The blacklists from Table I were selected based on
   DNS                 Long Tail        Classification         RBL       their popularity among operators.
    (A)                   (B)                (C)                (D)
                                                                         E. Building and training a classifier
             Figure 1. High level overview of our approach                  In this section we describe the building of the training
                                                                         dataset and the training of the classifier. Figure 1 shows these
                                                                         steps with a grey background.
B. Long Tail Analysis                                                       1) Dataset: To build a training dataset for our classifier,
   Snowshoe spammers aim at spreading the sending load                   we label the dataset of candidate domains extracted from the
among a large number of hosts. At the same time, they are                long tail of the DNS. We do this by checking the domains
likely to use SPF in order to make their domains appear                  against public blacklists (Table I). Depending on the nature
legitimate. Therefore, we expect that snowshoe spam domains              of the public blacklist, we either check the domain name of a
will have a large number of A or MX records and large (in                candidate domain against the blacklist or an Internet Protocol
terms of number of characters) TXT records. Domains with                 (IP) address from one of the DNS records (A and MX) for
these characteristics will likely show up in a long tail analysis        the domain. If the domain is listed, we label the domain as
of DNS domains. The long tail typically refers to the outliers           a positive, otherwise, it is labeled as a negative. In order to
of a distribution. In our case, the majority of domains will have        increase the accuracy of the training dataset, we filter the
only a few DNS records of a given type, whereas snowshoe                 positives from the dataset and balance them with and equal
spam domains will exhibit many records of the certain types.             number of negatives from the Alexa top one million list. While
Thus, these domains appear far away from the mean, in the                domains on the Alexa list are not guaranteed to be benign,
long tail of the DNS. In this paper we look at two types                 the probability of them being benign is much higher than the
of long tail of the DNS. The first tail holds domains with               negative instances extracted from the long tail.
a large number of records. The second type holds domains                    Additionally, we created an evaluation dataset which does
with exceptionally large TXT records. We have defined four               not perform this extra filtering step. This evaluation dataset is
thresholds for what we consider to be the long tail: 99.9%,              used to compare different classifier types.
99%, 98% and 97%. We have chosen these thresholds to                        Both the training and evaluation dataset consist of 35
range from very conservative to more permissive selections.              features. The features we have used and their sources are
We stopped at 97% to limit the number of domains to we need              listed in Table II. Most of these features measure how many
to analyze, so we can perform daily detections in a timely               records of a certain type a domain contains. Some features
manner.                                                                  are more complex and rely on evaluating regular expressions.
                                                                         For example, the ‘spfv1_ip_count’ feature uses a regular
C. Classification                                                        expression to count the number of IP addresses in an SPF
   To cope with the dynamic nature of spam, we have opted                record. The output of all of the features is numerical, because
to use machine learning to do the detection. The reason for              all the evaluated classifiers are able to make predictions based
this is that a classifier can easily be retrained on new data if         on numeric features and only a few (special) classifiers are
spam trends change. In addition to this, the vast amount of              able to process raw strings [23]. Thus to reach maximum
data makes a manual creation of signatures unfeasible. In this           compatibility we make sure all features are in numeric form.
step, we match the domains selected from the long tail analysis             Not all features are equally important. Following the output
against a machine learning classifier. The classifier has been           from a trained ‘Decision Tree’, the ‘response_name_matches’
chosen as described in Section III-E. The classifier takes into          feature is the most important, since it has the highest Gini
account a set of features derived from the DNS records for the           index. This feature details if the query name in the response
candidate domains (see Table II). The output of the classifier           is the same as in the request. The ‘ip4_count’ and ‘mx_count’
is a binary decision detailing if a domain should be considered          features are, after the ‘response_name_matches’, equally im-
as a snowshoe domain.                                                    portant.
                                                                            2) Classifier: In order to perform optimal detection, we first
D. Realtime Blackhole List (RBL)                                         needed to select a suitable classifier. Below, we explain our
   To make our results easily available and usable, we store             methodology for finding the ‘best’ classifier for our problem.
them in the form of an RBL. In this section, we explain how              We also explain what we mean by ‘best’.
the RBL is kept up to date. As said, every day we run our                   We evaluated classifiers in a number of categories. In
detection process. The classifier outputs a list of domains that         the Naive Bayes category, we looked at the ‘BernoulliNB’,
it considers to be snowshoe spam domains. Domains from                   ‘GaussianNB’ and ‘MultinomialNB’ classifiers. For Decision
Tree-type classifiers, we tested the ‘DecisionTreeClassifier’                                                    TABLE II
and the ‘RandomForestClassifier’. Of the Nearest Neighbor                                        U SED F EATURES AND T HEIR DATA S OURCES
variant, we evaluated the ‘KNeighborsClassifier’ and ‘Radius-                       Data source         Feature
NeighborsClassifier’. From the Gradient Descend type we took                        as                  as_count
the ‘GradientBoostingClassifier’ and ‘SGDClassifier’. Finally                       cname_name          cname_count, cname_in_domain, cname_out_domain
                                                                                    country             country_codes
we also looked at the ‘Support Vector Classifier (SVC)’,                            ip4_address         ip4_count, ip4_prefixes
‘MLPClassifier’ and the meta-classifier ‘AdaBoostClassifier’2 .                     ip6_address         ip6_count, ip6_prefixes
Our selection of classifiers was primarily motivated by the                         mx_address          mx_cloud, mx_count
                                                                                    ns_address          ns_count, ns_domain_count
combination of classifiers used in related work [6]–[8], [13],
                                                                                    query_name          p_numeric
[16], [19]–[21], and the availability of classifiers in the                         query_name &        response_name_matches
‘sklearn’ [24] Python library.                                                      response_name
   Selection of the ‘best’ classifier is done in two steps.                         soa_minimum         soa_minimum
                                                                                    txt_text            p_txt_numeric, spfv1_{a,cidr,include,ip}_count,
First, we establish the optimal parameters for each of the 13                                           spfv1_{a,cidr,include,ip}_ratio,
classifiers selected. This step aims at understanding what the                                          spfv1_{a,cidr,include,ip}_unique_count,
optimal performance of each classifier is, given our training                                           txt_length,verification_{globalsign,google}_count,
                                                                                                        verification_{globalsign,google}_ratio, verifica-
set. This also allows us to compare the classifiers later on. This                                      tion_{globalsign,google}_unique_count
was done as follows. The training set is split in training data
and test data. The classifier is then trained on the training data
                                                                                         k(1)       k(2)        k(3)       k(4)        k(5)
following the K-Fold Cross Validation [25] method, which
is visualized in Figure 2. The training part of the dataset is                                             training data                         test data
split into K folds. A classifier is trained K times on K − 1
folds of the training part, for example, in the figure parts
k(1) through k(4). During the training process the chosen                                       Figure 2. Visualization of split in training dataset
algorithm builds a model of the (labeled) data, in particular the
boundaries between the positive and negative entries. Based
                                                                                                                IV. DATASETS
on such a model predictions can be made on new, unseen,
data. Then the performance of the classifier is validated in                          Based on the approach discussed in Section III, we have
the K-th fold, in our example k(5). This is done K times,                          performed daily detection from May 24, 2017 till September
where the validation fold is a different fold each time. The                       5, 2017. This section discusses the details on the datasets used,
performance of the classifier is the average over each fold.                       either in the training, validation or during the daily detections.
Based on this performance, we select the parameters for each
                                                                                   A. Distinction positives & negatives
classifier that lead to the highest precision, where precision is
expressed as the number of True Positives (TP) relative to the                        Before we dive into the results of our method, we verify
total amount of positives, which also includes False Positives                     that there is a clear difference between the positives (spam)
(FP) (Equation 1). We repeat this procedure for every type of                      and negatives (ham). For this goal we have made a dataset
classifier.                                                                        from April 2017. We have selected domains above the 99
                                                                                   percentile, since this percentile threshold gave a clear distinc-
                                            TP                                     tion between positives and negatives. After labeling the dataset
                       P recision =                                         (1)
                                          TP + FP                                  we filtered this dataset following the same method as for the
                                                                                   training dataset. This resulted in a dataset with both 136441
   The second step consists of comparing the optimal perfor-                       positives and negatives. We do so by plotting the Cumulative
mance of the different classifiers. The performance of each                        Distribution Function (CDF) for two features, these plots are
classifier is measured on the evaluation dataset. The one with                     visible in Figure 3. This analysis indicates that at the 90th
the best precision on this dataset is selected as the classifier                   percentile for the A record distribution, spam domains have on
that will be used for our daily detection.                                         average 16.2 records more than regular domains. Similarly, at
                                                                                   the 98th percentile of the MX record distribution, spam domains
   2 Documentation on these classifiers is available at http://scikit-learn.org/
                                                                                   have 77 records more than regular domains. The fact that not
stable/modules/classes.html                                                        all domains show this clear distinction motivated us to make
                                                                                   use of the many features available to us.
                                TABLE I                                            B. Training and evaluation dataset
               T HE U SED B LACKLISTS AND T HEIR P URPOSE
                                                                                     For the selection of the ‘best’ classifier we have made two
             Name                     Domain         IP address
                                                                                   datasets. The first is the training dataset, the classifier is trained
             multi.uribl.com            3
             dbl.spamhaus.org           3                                          upon this dataset, it consists of data from April 18, 2017 till
             rbl.rbldns.ru                                3                        April 24, 2017. The second dataset, the evaluation dataset,
             zen.spamhaus.org                             3                        consists of data from April 25, 2017. Table III lists how many
         1                                                                                                      TABLE IV
                        16.6                                                                C LASSIFIER P ERFORMANCE ON THE ‘R EAL’ DATA S ET
        0.9
CDF

        0.8         11.2                                                            Classifier Type    TP      FN      FP     TN      Accuracy   Precision
                                                                positives           AdaBoost            6688    7842    110   10741     68.69%     98.38%
        0.7                                                                         Improved
                                                                negatives
        0.6
                                                                                    AdaBoost            5971    8559    164   10687    65.63%     97.32%
              0            10         20           30           40          50      MLP                 7273    7257    707   10144    68.62%     91.14%
                                                                                    DecisionTree        6279    8251    695   10156    64.75%     90.03%
                                  Number of A records                               MultinomialNB      12179    2351   1397    9454    85.23%     89.70%
                                                                                    RandomForest       11156    3374   1488    9363    80.84%     88.23%
                                                                                    KNeighbors          4562    9968    676   10175    58.06%     87.09%
                                                                                    GaussianNB         13330    1200   2075    8776    87.10%     86.53%
       (a) Comparison of the number of A records                                    SVC                13449    1081   2339    8512    86.53%     85.18%
         1                                                                          RadiusNeighbors    13318    1212   2367    8484    85.90%     84.90%
                                                                                    SGD                 3599   10931    674   10177    54.28%     84.22%
                                        77.0                                        BernoulliNB        12995    1535   2507    8344    84.07%     83.82%
       0.98
CDF




                                                                                    GradientBoosting   12645    1885   9605    1246    54.73%     56.83%
       0.96                                                     positives
                                                                negatives
       0.94
              0            20         40           60           80          100
                                                                                     We have decided to look for a classifier with a low number
                                                                                  of FP. This is because is spam detection it is far more costly
                                 Number of MX records                             to make an FP, a ham domain marked as spam, than any other
                                                                                  error. The cost of making a FP outweighs making a correct
      (b) Comparison of the number of MX records                                  classification, a TP. The reasoning can be put in perspective
                                                                                  by an example; the cost of marking an important email as
               Figure 3. CDF of two features in the test data set                 spam, or discarding the email, is much higher than receiving
                                                                                  a spam message. This is the reason we have chosen to rank
                                                                                  our classifiers on their precision metric (Eq 1), since it is more
domains there are in both datasets, along with how many
                                                                                  closely related to the number of FPs made by the classifier than
positives and negatives. As intended the training dataset is
                                                                                  other metrics.
balanced.
                                                                                     The performances from the second step are listed in Ta-
C. Daily detection datasets                                                       ble IV. The ‘AdaBoost’ classifier has the highest precision
   Since May 24, 2017, we have been doing daily detections                        on our evaluation dataset, and it has the lowest number of
of possible snowshoe spam domains. The basis of these detec-                      false positives. However, it does not have the highest number
tions is a dataset of that day containing domains exceeding the                   of true positives. We improve this classifier by taking a
99.9, 99, 98 or 97 percentile. On average there are about 2.7K                    closer look at the parameters of the classifier. We managed
domains in the dataset of the 99.9 percentile. This figure grows                  to increase the number of TPs by 717 and reduce the number
to 57.3K domain names in the dataset of the 97 percentile.                        of FPs by 54. The resulting classifier is labeled as ‘AdaBoost
Table VI shows the average size of each of the daily datasets.                    Improved’ in Table IV. The ‘AdaBoostClassifier’ is a meta-
                                                                                  classifier. “It begins by fitting a classifier on the original
                                V. R ESULTS                                       dataset and then fits additional copies of the classifier on the
   This section has been split into two parts. First, we discuss                  same dataset but where the weights of incorrectly classified
the results from selecting the ‘best’ classifier. Secondly, we                    instances are adjusted such that subsequent classifiers focus
discuss the daily detections made for the RBL.                                    more on difficult cases" [26]. To improve our classifier we
                                                                                  changed the base estimator from the ‘DecisionTreeClassifier’
A. Selecting the ‘best’ classifier                                                to the ‘MultinomialNB’ and set the number of estimators to
   As discussed in Section III-C, the selection of the best clas-                 1. The additional parameters are in Table V.
sifier is a two step process. First, select the optimal parameters                   Table IV makes clear why we rank the classifiers based
for each classifier. Then, we select the ‘best’ classifier, as the                on their precision metric rather than, for example, the accu-
one with the best performance. For brevity sakes we omit the                      racy. If we compare the classifier with the highest accuracy,
results of the first step and directly present a comparison of                    ‘GaussianNB’, with the improved ‘AdaBoostClassifier’, we
the classifiers, in Table IV.                                                     see about double the TPs but there are more than 18 times
                                                                                  as many FPs. The cost of making a FP is much higher than
                                                                                  the gain of a TP, since it may mean important benign email
                                  TABLE III
             S TATISTICS OF T RAINING AND E VALUATION DATASET                     is discarded. Thus, for our goal the ‘AdaBoostClassifier’ is
                                                                                  ‘better’ than the ‘GaussianNB’ classifier.
                         #Domains (total, positive, negative)
      %-tile
                     Training dataset          Evaluation dataset                 B. Detection results
      99.9        2018 (1009 – 1009)        1407      (1261 – 146)
      99          3540   (1770 – 1770)      5453      (5199 – 254)                  In this section we discuss the general detection results.
      98          4806 (2403 – 2403)       20534     (20177 – 357)                During our measurement period, our detection method marked
      97          5526   (2763 – 2763)     25381     (24968 – 413)                35,004 domains as snowshoe spam domains. 32,677 of these
                                                                                                    100000

 (a)




                                                                               Number of detected
                                                                                                     10000
              Δt < 2 days




                                                                                   domains
                                                                                                     1000
 (b)
                                                                                                       100
                                    Δt ≥ 2 days
 (c)
                       domain not on existing blacklist yet
                                                                         ?
                                                                                                        1
                                                                                                             0          20          40         60          80   100


                            detected by our method                                                                           Detection in advance (days)
                            appeared on existing blacklist
                                                                                                                  Figure 5. Early detection of domains

                  Figure 4. Early detection categories
                                                                              (b) domains with a detection difference of at least two days
domains (93.35%) appeared on an existing blacklist at some                         or more.
point during the measurement period. This indicates that                      (c) domains that – on the day of writing – have not (yet)
our method is highly effective at detecting snowshoe spam                          been blacklisted.
domains. The remaining 2,327 domains (6.65%) are either                         Figure 5 shows how many domains have been detected, with
false positives or they have not yet appeared in one of the                  how much of a time difference before being blacklisted. The
existing blacklists. This second case occurs when our detection              y-axis is log-scaled to make the spread more visible.
mechanism reports snowshoe domains (much) earlier than                          In total 35,004 domains have been detected. The majority of
blacklists. We analyze this case in the next section.                        domains by far falls in the first category (a), 30,705 domains
   Table VI lists how many domains per day on average are in                 (87.72%) appear on a blacklist less than two days after
the long tail dataset (per percentile), how many are detected                detection via our method. In the second category (b), where
by the classifier and how many are newly added to the RBL.                   our detection is at least two days in advance, contains 1,972
                                                                             domains (5.63%). Of these 1,972 domains, 1,154 domains
C. Early detection                                                           (3.30%) were detected at least a week in advance, 1,105
   In this section we analyze if our approach has a time ad-                 domains (3.16%) were detected more than two weeks in
vantage over regular, existing blacklists, such as the Spamhaus              advance, and 971 domains (2.77%) were detected at least
blacklist. By time advantage we mean the window between de-                  a month in advance. There are even 949 domains (2.71%)
tection by our method and the time at which the same domains                 which were detected at least 60 days before they appeared on
appears on one of the existing blacklists we considered (see                 a blacklist. The maximum time difference we observed so far
Table I).                                                                    is 104 days. 2,327 domains (6.65%) fall in the last category
   In the context of early detection, we distinguish three                   (c), and have not (yet) been blacklisted. While these numbers
categories of domains. Figure 4 depicts these categories, and                may seem small percentage-wise, it should be noted that this
they are described in more detail below:                                     type of email often makes it past an email filter.
 (a) domains that are already on a blacklist at the time of
      detection, or have only a day difference. There can be a                                                   VI. O PERATIONAL DEPLOYMENT
      one day difference since the daily data is of the previous                To validate our method in a real-world scenario, we de-
      day, while the blacklist query happens in real-time.                   ployed the RBL (Section III-D) in an operational mail fil-
                                                                             tering service. This allows us to measure how effective our
                                                                             detections are. This deployment was done in collaboration
                            TABLE V
        PARAMETERS OF THE I MPROVED A DA B OOST C LASSIFIER                  with SURFnet, the National Research and Education Network
                                                                             in The Netherlands. The email of most of their connected
                Name of parameter       Value
                                                                             universities and colleges is handled by SURFmailfilter. Hence,
                base_estimator          MultinomialNB
                n_estimators            1                                    this is an excellent vantage point for evaluating if the domains
                learning_rate           1.                                   we detect are in use for sending spam. In this section we
                algorithm               SAMME.R                              discuss the results of this case study.

                              TABLE VI                                       A. Method
        P ER - DAY AVERAGES OF THE DATASETS AND D ETECTIONS
                                                                                 First we describe the setup of this case-study. SURFmail-
 Percentile   Avg. domains in     Avg. domains           Avg. added to       filter works, like many mail filters, with a scoring system;
              dataset             detected               the RBL
                                                                             the higher the score, the more likely it is that the email is
 99.9         2728.07             243.96                 18.99
 99           19179.59            3228.75                149.37              spam. The operators of SURFmailfilter have set the defaults
 98           37202.64            5226.31                205.72              for tagging an email as spam to a score of 5, and discard
 97           57250.48            6805.55                239.37              any email with a score higher than 10. While these thresholds
                                                                                                                                                                                                             5.0
                                                                                                                                                                                          Blacklisted
                 daadzgam.com                                                                                                                                                                                4.5
                                                                                                                                                                                          Detected
                                                                                                                                                                                                             4.0
                 realdrippy.com
                                                                                                                                                                                                             3.5
Domain names




                                                                                                                                                                                                             3.0




                                                                                                                                                                                                                   Spam score
               coachspoke.com
                                                                                                                                                                                                             2.5
                stillscratch.com                                                                                                                                                                             2.0
                                                                                                                                                                                                             1.5
                 homerope.com
                                                                                                                                                                                                             1.0

               quittradition.com                                                                                                                                                                             0.5
                                                                                                                                                                                                             0.0
                             2017-05-24   2017-05-31   2017-06-07   2017-06-14   2017-06-21   2017-06-28                 2017-07-05   2017-07-12   2017-07-19   2017-07-26   2017-08-02         2017-08-09
                                                                                                        Observation dates




                                                                                   Figure 6. SURFmailfilter Detections



are configurable, in this paper we follow the thresholds as                                                     in Figure 6 summarizes the various possible cases we face
set by the SURFmailfilter operators. To test our approach, we                                                   when comparing our method with blacklists.
configured our RBL as an extra source for blacklisted domains                                                     In total, 130 domains that appear on our RBL have been
in SURFmailfilter. To not influence the normal spam score                                                       seen by SURFmailfilter in the body of an email. These
an email would get by too much, we have given the RBL a                                                         domains can roughly be categorized in three ways:
minimum score (0.1). This has the effect that the mail filter                                                        1) The first category, where the detection difference is one
will not ignore the RBL, but at the same time our detection                                                             day or less, contains 23 domains (17.69%). Of these, 16
system will not accidentally turn ham into spam in case a                                                               have an average score above five. The other four domains
benign domain happens to be on our RBL.                                                                                 appear in emails scoring both below and above the five
   Then, to assess the effectiveness of our method, we retrieve                                                         point mark, but on average score below five. The reason
the email IDs which have hit the RBL, and we extract the                                                                many domains in this category have a high spam score
domains that have triggered the RBL. Of these emails we                                                                 can be explained by the fact that the blacklist status
record the triggering domain, the spam score, the date the                                                              causes an increase in spam score, and thus it exceeds
domain was detected, if the domain was blacklisted, and if so,                                                          the threshold of five more easily. This also means that in
when.                                                                                                                   this category many of the emails are already marked as
                                                                                                                        spam, because of their high score, and that our approach
B. Results                                                                                                              does not offer much gain for this category.
    We discuss the results from SURFmailfilter in two ways.                                                          2) In the second category, where the detection difference
Firstly, via the domains which have been seen by SURFmail-                                                              is two days or more, there are 38 domains (29.23%). Of
filter. The initial goal was to confirm that the detected domains                                                       these domains, 22 have an average score above five. Four
are in use, but these results can also be used to confirm that                                                          domains have only been seen in an email once, scoring
the domains are actually spam domains. And secondly, via                                                                below five. Two domains have been seen in multiple
the emails themselves which have hit the RBL. With these                                                                emails, all scoring less than five points. The remaining
results we can answer how much extra spam could be tagged                                                               10 domains, appear in emails with scores above and
or blocked by using our approach.                                                                                       below the five point mark, but do not make the five point
    1) Domains: The domains which have been seen by SURF-                                                               average. Percentage wise there are fewer domains with an
mailfilter can, roughly, be categorized into the same three cat-                                                        average score above five compared to the first category,
egories as used in Section V-C. The first category (a) consists                                                         thus our approach may make difference in this category
of domains which have appeared on a blacklist shortly after                                                             of domains.
detection by our method (one day or less of a difference). The                                                       3) The last category, where detected domains have not
second category (b) contains domains which have appeared on                                                             appeared on a blacklist in the measurement interval,
a blacklist some time after detection by our method (two days                                                           contains 69 domains (53.08%). Of these 69 domains,
or more of a difference). Finally, the last category (c) is for                                                         there are 38 with an average spam score above five.
domains which have, during our measurement period, never                                                                12 domains have appeared in emails which have all
appeared on a blacklist.                                                                                                scored below the five point mark. However, seven of
    Figure 6 exemplifies 6 domains from these 3 categories.                                                             these domains have only been seen in a single email. The
This graph is built by looking at each domain separately. The                                                           remaining 19 domains were seen in emails scoring both
upper row displays their maximum score per day. A black                                                                 below and above the five point mark, but with an average
color means no email containing the domain was observed                                                                 score of below five. Our approach is most beneficial in
that day. The score visualization ranges from a low score, in                                                           this category. About half of the domains in this category
blue, to a high score, in red. The score is cut off at five. This                                                       score, on average, below five, this means that emails
means that while emails may have scored higher than five,                                                               containing these domains are able to bypass the mail
these are all displayed in red.                                                                                         filter. However, since the domains do appear on our RBL
    In overlay, we have the status of the domain. A domain is                                                           the score of those emails can be increased by assigning
either detected only by our system (purple) or it is detected                                                           a higher score of hitting the RBL.
and appears in one of the blacklists (green). The visualization                                                        A large portion of detected domains have an average score
                                                                                  Occasionally we were given access to the subject line, in order
  Percentage of emails
    marked as spam       100%                                                     to get a better idea if a message could be spam or not.
                                                                                     Another concern is that the RBL resulting from our method
                         50%                                                      may contain benign entries (false positives). This is true for
                                                                                  all blacklists. While blacklist operators try to ensure that
                          0%
                                                                                  only malicious domains end up on their list, sometimes false
                                0       1         2          3            4   5   positives slip through the cracks. This problem is doubled for
                                            Additional score of the RBL           our RBL since our classifier is only as good as the training set
                                                                                  is. The training set is labeled by looking up the domains on
                            Figure 7. Amount of extra email marked as spam        existing blacklists, if their accuracy is not one hundred percent,
                                                                                  the predictions from the classifier are not going to be perfect.
                                                                                  We therefore caution against treating our RBL as ‘absolute
above five, this gives confidence that our method is effective                    truth’, and instead advocate that it is treated as circumstantial
in detecting domains associated with spam.                                        evidence that supports the suspicion of a message being spam.
   2) Emails: Over our measurement period, SURFmailfilter                                              VIII. C ONCLUSIONS
processed 3,773 emails that triggered the RBL. Of these
                                                                                     In this paper we investigate how domains crafted for sending
emails, 1695 come from the latter two categories presented
                                                                                  snowshoe spam can be detected using active DNS measure-
in Section V-C at the time of receiving the emails. We only
                                                                                  ments. Using the unique large-scale OpenINTEL dataset of
evaluate emails containing domains which are not blacklisted.
                                                                                  the DNS and by applying machine learning techniques, we
560 emails have a score equal to, or above five. While this
                                                                                  are able to detect malicious domains. 93.25% of domains we
means that the email would have been marked as spam with or
                                                                                  have detected have appeared on an existing blacklist at some
without our method, it also gives confidence that our method is
                                                                                  point during the measurement period. Additionally, we have
effective at detecting spam. In the pool of 1,135 emails scoring
                                                                                  shown that our method is able to detect domains from 2 to 104
below five, 77 emails contain domains in the body which have
                                                                                  days in advance, when compared to regular blacklists, such as
not appeared in emails scoring higher than five.
                                                                                  the Spamhaus blacklist.
   This pool of 1,135 emails, which have scored below the
                                                                                     In the operator case-study at SURFnet, we demonstrated
five point mark, has been used to evaluate how many emails
                                                                                  that the time advantage translates into additional emails being
could additionally be blocked, at what assigned score for the
                                                                                  marked as spam. In addition to this, we verified that these
RBL. Figure 7 visualizes the results of this analysis. As a
                                                                                  emails actually contain domains known to be associated with
conservative measure the RBL could be awarded a single
                                                                                  spam. These emails would otherwise bypass the email filter.
point. In our situation this would have marked 19.1% of those
1,135 emails as spam. If the score is increased to two, 52.3%                     A. Future work
of emails would have been marked as spam.                                            This paper has shown the potential of active DNS measure-
   While we have strong reasons to assume that all domains                        ments in the search for snowshoe spam domains. We realise,
on our RBL are linked to spam, this approach lets mail filter                     however, that this is just a starting point. First, the next obvious
operators control how much they trust these results.                              step is to collaborate with spam filter operators in order to
                                                                                  have more measurement points. Since spam is highly targeted
C. Uptake                                                                         it is reasonable to assume that SURFnet, the Internet service
   SURFnet has used our RBL for three months as discussed                         provider for academia in the Netherlands, receives a different
above. At first glance, the amount of additional spam that                        kind of spam than, say, for example, an email provider in the
could potentially be filtered seems small. Typically, spam fil-                   United States. Since SURFnet is planning to add two points
tering systems catch a large percentage of spam messages [2],                     to emails hitting the RBL we will follow up with SURFnet
and very few actually end up in a user’s inbox. SURFnet has                       after some time to learn from their experience. Secondly, the
indicated that the emails detected by our method are actually                     optimal period for obtaining a fresh training set and retraining
those that currently slip through the cracks and end up in                        the classifier needs further investigation.
users’ inboxes. This makes our approach valuable to operators.
                                                                                                      ACKNOWLEDGEMENTS
In fact, SURFnet has decided to start using our method in
production, and will assign a score of two to the RBL.                               Special thanks go to SURFnet for allowing us to test our
                                                                                  method in practice. Their contribution proved invaluable to
                                            VII. E THICS                          testing our approach in an operational environment.
                                                                                     The research leading to the results presented in this pa-
   The SURFmailfilter case study raises obvious privacy con-
                                                                                  per was made possible by OpenINTEL, a joint project of
cerns, as the system processes actual private email. There-
                                                                                  SURFnet, the University of Twente and SIDN. This research
fore, the operators at SURFnet protected the privacy of their
                                                                                  was partly funded by SIDN Fonds.
customers by only giving us enough information to do our
research. We did not have access to the actual body of emails.
                        R EFERENCES                                    Trends,” CoRR, 2016. [Online]. Available: http://arxiv.
 [1]   S. L. Pfleeger and G. Bloom, “Canning Spam: Proposed            org/abs/1606.01042.
       Solutions to Unwanted Email,” IEEE Security Privacy,     [17]   P. Owezarski, “Unsupervised Classification and Charac-
       vol. 3, no. 2, 2005.                                            terization of Honeypot Attacks,” in CNSM 2014, 2014,
 [2]   J. Schultz, Walking in a Winter Wonderland, 2014.               pp. 10–18.
       [Online]. Available: https://blogs.cisco.com/security/   [18]   J. J. Santanna, R. d. O. Schmidt, D. Tuncer, J. de
       walking-in-a-winter-wonderland.                                 Vries, L. Z. Granville, and A. Pras, “Booter Blacklist:
 [3]   F. Weimer, “Passive DNS Replication,” in Proc. of               Unveiling DDoS-for-hire Websites,” in CNSM 2016,
       FIRST 2005, 2005.                                               2016, pp. 144–152.
 [4]   B. Zdrnja, N. Brownlee, and D. Wessels, “Passive         [19]   S. Youn and D. McLeod, “A Comparative Study for
       Monitoring of DNS Anomalies,” in Proc. of DIMVA                 Email Classification,” in Advances and Innovations in
       2007, 2007.                                                     Systems, Computing Sciences and Software Engineer-
 [5]   Bilge, Leyla and Kirda, Engin and Kruegel, Christopher          ing, K. Elleithy, Ed. Springer Netherlands, 2007.
       and Balduzzi, Marco, “EXPOSURE: Finding Malicious        [20]   H. Drucker, D. Wu, and V. N. Vapnik, “Support Vector
       Domains Using Passive DNS Analysis,” in NDSS 2011,              Machines for Spam Categorization,” IEEE Transactions
       2011.                                                           on Neural Networks, vol. 10, no. 5, 1999.
 [6]   M. Antonakakis, R. Perdisci, D. Dagon, W. Lee, and       [21]   G. Sakkis, I. Androutsopoulos, G. Paliouras, V.
       N. Feamster, “Building a Dynamic Reputation System              Karkaletsis, C. D. Spyropoulos, and P. Stamatopoulos,
       for DNS,” in Proc. of the 19th USENIX Security, 2010.           “Stacking classifiers for anti-spam filtering of e-mail,”
 [7]   M. Antonakakis, R. Perdisci, W. Lee, N. Vasiloglou II,          CoRR, 2001. [Online]. Available: http://arxiv.org/abs/cs.
       and D. Dagon, “Detecting Malware Domains at the                 CL/0106040.
       Upper DNS Hierarchy,” in Proc. of the 20th USENIX        [22]   R. van Rijswijk-Deij, M. Jonker, A. Sperotto, and A.
       Security, 2011.                                                 Pras, “A High-Performance, Scalable Infrastructure for
 [8]   R. Perdisci, I. Corona, D. Dagon, and W. Lee, “Detect-          Large-Scale Active DNS Measurements,” IEEE Journal
       ing Malicious Flux Service Networks through Passive             on Selected Areas in Communications, vol. 34, no. 6,
       Analysis of Recursive DNS Traces,” in 2009 Annual               2016.
       Computer Security Applications Conference (ACSAC         [23]   H. Lodhi, C. Saunders, J. Shawe-Taylor, N. Cristian-
       ’09), 2009, pp. 311–320.                                        ini, and C. Watkins, “Text Classification Using String
 [9]   M. Konte, N. Feamster, and J. Jung, “Dynamics of                Kernels,” J. Mach. Learn. Res., 2002.
       Online Scam Hosting Infrastructure,” in Proc. of PAM     [24]   F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel,
       2009. 2009.                                                     B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer,
[10]   S. Hao, N. Feamster, and R. Pandrangi, “Monitoring the          R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D.
       Initial DNS Behavior of Malicious Domains,” in Proc.            Cournapeau, M. Brucher, M. Perrot, and E. Duchesnay,
       of the 2011 ACM IMC, 2011.                                      “Scikit-learn: Machine Learning in Python,” Journal of
[11]   M. Felegyhazi, C. Kreibich, and V. Paxson, “On the              Machine Learning Research, vol. 12, 2011.
       Potential of Proactive Domain Blacklisting,” in LEET     [25]   R. Kohavi, “A Study of Cross-Validation and Bootstrap
       2010, 2010.                                                     for Accuracy Estimation and Model Selection,” in Int.
[12]   S. Hao, A. Kantchelian, B. Miller, V. Paxson, and               Joint Conf. on Artificial Intelligence, 1995.
       N. Feamster, “PREDATOR: Proactive Recognition and        [26]   Scikit-Learn,      sklearn.ensemble.AdaBoostClassifier.
       Elimination of Domain Abuse at Time-Of-Registration,”           [Online].        Available:         http://scikit-learn.org/
       in Proc. of the 2016 ACM CCS, 2016.                             stable/modules/generated/sklearn.ensemble.
[13]   N. A. Syed, A. G. Gray, N. Feamster, and S. Krasser,            AdaBoostClassifier.html.
       “Snare: Spatio-temporal Network-level Automatic Rep-
       utation Engine,” Georgia Institute of Technology - CSE
       Technical Reports - GT-CSE-08-02, Tech. Rep., 2008.
[14]   G. C. M. Moura, A. Sperotto, R. Sadre, and A. Pras,
       “Evaluating third-party Bad Neighborhood blacklists
       for Spam detection,” in 2013 IFIP/IEEE Int. Symp. on
       Integrated Network Management (IM 2013), May 2013.
[15]   D. Yamakawa and N. Yoshiura, “Analysis of spam mail
       sent to Japanese mail addresses in the long term,”
       in 2010 IEEE Network Operations and Management
       Symposium - NOMS 2010, Apr. 2010.
[16]   A. Bhowmick and S. M. Hazarika, “Machine Learning
       for E-mail Spam Filtering: Review, Techniques and
