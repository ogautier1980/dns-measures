   T RANCO: A Research-Oriented Top Sites Ranking
           Hardened Against Manipulation

     Victor Le Pochat∗ , Tom Van Goethem∗ , Samaneh Tajalizadehkhoob† , Maciej Korczyński‡ , Wouter Joosen∗
          ∗ imec-DistriNet, KU Leuven              † Delft University of Technology              ‡ Grenoble Alps University
     {firstname.lastname}@cs.kuleuven.be           S.T.Tajalizadehkhoob@tudelft.nl        maciej.korczynski@univ-grenoble-alpes.fr

     Abstract—In order to evaluate the prevalence of security             Even though most providers declare that the data is processed
and privacy practices on a representative sample of the Web,              to remove such statistical biases, the lack of exact details
researchers rely on website popularity rankings such as the Alexa         makes it impossible for researchers to assess the potential
list. While the validity and representativeness of these rankings         impact of these lists on their results and conclusions.
are rarely questioned, our findings show the contrary: we show
for four main rankings how their inherent properties (similarity,              In this paper, we show that the four main popularity rank-
stability, representativeness, responsiveness and benignness) affect      ings (Alexa, Cisco Umbrella, Majestic and Quantcast) exhibit
their composition and therefore potentially skew the conclusions          significant problems for usage in research. The rankings hardly
made in studies. Moreover, we find that it is trivial for an
                                                                          agree on the popularity of any domain, and the Umbrella and
adversary to manipulate the composition of these lists. We are
the first to empirically validate that the ranks of domains in each       especially the Alexa lists see a significant turnover even on con-
of the lists are easily altered, in the case of Alexa through as little   secutive days; for Alexa, this is the result of an unannounced
as a single HTTP request. This allows adversaries to manipulate           and previously unknown change in averaging approach. All
rankings on a large scale and insert malicious domains into               lists include non-representative and even malicious sites, which
whitelists or bend the outcome of research studies to their               is especially dangerous considering the widespread use of these
will. To overcome the limitations of such rankings, we propose            rankings as whitelists. Overall, these flaws can cause the choice
improvements to reduce the fluctuations in list composition and           for a particular ranking to severely skew measurements of
guarantee better defenses against manipulation. To allow the              vulnerabilities or secure practices.
research community to work with reliable and reproducible
rankings, we provide T RANCO, an improved ranking that we                     Moreover, we are the first to empirically prove that pitfalls
offer through an online service available at https://tranco-list.eu.      in these rankings leave them vulnerable to one of our newly
                                                                          introduced manipulation techniques. These techniques have a
                                                                          surprisingly low cost, starting from a single HTTP request for
                       I.   I NTRODUCTION                                 Alexa, and can therefore be used to affect the rank of thousands
    Researchers and security analysts frequently study a selec-           of domains at once on a substantial level: we estimate that the
tion of popular sites, such as for measuring the prevalence               top 10 000 can easily be reached. The incentives of adversaries
of security issues or as an evaluation set of available and               to alter the composition of these lists, both for single domains
often used domain names, as these are purported to reflect                due to the practice of whitelisting popular domains, and on
real-world usage. The most well known and widely used list                a larger scale to influence research and its impact outside
in research studies is that of Alexa, with researchers’ reliance          academia, make this manipulation particularly valuable.
on this commercial list being accentuated by their concern
when it was momentarily taken offline in November 2016 [11].                  Finally, there is still a need for researchers to study popular
However, several companies provide alternative rankings based             domains, so they would therefore benefit from a list that
on Internet usage data collected through various channels [54]:           avoids biases in its inherent properties and is more resilient to
a panel of users whose visits are logged, tracking code placed            manipulation, and that is easily retrieved for future reference.
on websites and traffic captured by intermediaries such as ISPs.          To this extent, we propose improvements to current rankings in
                                                                          terms of stability over time, representativeness and hardening
    We found that 133 top-tier studies over the past four years           against manipulation. We create T RANCO, a new ranking
based their experiments and conclusions on the data from these            that is made available and archived through an accompanying
rankings. Their validity and by extension that of the research            online service at https://tranco-list.eu, in order to enhance the
that relies on them, should however be questioned: the methods            reproducibility of studies that rely on them. The community
behind the rankings are not fully disclosed, and commercial               can therefore continue to study the security of popular domains
interests may prevail in their composition. Moreover, the                 while ensuring valid and verifiable research.
providers only have access to a limited userbase that may be
skewed towards e.g. certain user groups or geographic regions.
                                                                          In summary, we make the following contributions:

                                                                            • We describe how the main rankings can negatively affect
Network and Distributed Systems Security (NDSS) Symposium 2019                security research, e.g. half of the Alexa list changes every
24-27 February 2019, San Diego, CA, USA
ISBN 1-891562-55-X                                                            day and the Umbrella list only has 49% real sites, as well
https://dx.doi.org/10.14722/ndss.2019.23386                                   as security implementations, e.g. the Majestic list contains
www.ndss-symposium.org                                                        2 162 malicious domains despite being used as a whitelist.
   • We classify how 133 recent security studies rely on these                           The panel is claimed to consist of millions of users,
     rankings, in particular Alexa, and show how adversaries                         who have installed one of “many different” browser exten-
     could exploit the rankings to bias these studies.                               sions that include Alexa’s measurement code [9]. However,
   • We show that for each list there exists at least one                            through a crawl of all available extensions for Google Chrome
     technique to manipulate it on a large scale, as e.g. only                       and Firefox, we found only Alexa’s own extension (“Alexa
     one HTTP request suffices to enter the widely used Alexa                        Traffic Rank”) to report traffic data. Moreover, this exten-
     top million. We empirically validate that reaching a rank                       sion is only available for the desktop version of these two
     as good as 28 798 is easily achieved.                                           browsers. Chrome’s extension is reported to have around
   • Motivated by the discovered limitations of the widely-                          570 000 users [1]; no user statistics are known for Firefox, but
     used lists, we propose T RANCO, an alternative list that is                     extrapolation based on browser usage suggests at most one
     more appropriate for research, as it varies only by 0.6%                        million users for two extensions, far less than Alexa’s claim.
     daily and requires at least the quadrupled manipulation
                                                                                         In addition, sites can install an ‘Alexa Certify’ tracking
     effort to achieve the same rank as in existing lists.
                                                                                     script that collects traffic data for all visitors; the rank can then
                                                                                     be based on these actual traffic counts instead of on estimates
     II.    M ETHODOLOGY OF TOP WEBSITES RANKINGS
                                                                                     from the extension [8]. This service is estimated to be used by
    Multiple commercial providers publish rankings of popular                        1.06% of the top one million and 4% of the top 10 000 [19].
domains that they compose using a variety of methods. For
                                                                                          The rank shown in a domain’s profile on Alexa’s website is
Alexa, Cisco Umbrella, Majestic and Quantcast, the four lists
                                                                                     based on data over three months, while in 2016 they stated that
that are available for free in an easily parsed format and
                                                                                     the downloadable list was based on data over one month [6].
that are regularly updated, we discuss what is known on how
                                                                                     This statement was removed after the brief takedown of this
they obtain their data, what metric they use to rank domains
                                                                                     list [7], but the same period was seemingly retained. However,
and which potential biases or shortcomings are present. We
                                                                                     as we derive in Section III-B, since January 30, 2018 the list is
base our discussion mainly on the documentation available
                                                                                     based on data for one day; this was confirmed to us by Alexa
from these providers; many components of their rankings are
                                                                                     but was otherwise unannounced.
proprietary and could therefore not be included.
                                                                                         Alexa’s data collection method leads to a focus on sites
   We do not consider any lists that require payment, such as
                                                                                     that are visited in the top-level browsing context of a web
SimilarWeb1 , as their cost (especially for longitudinal studies)
                                                                                     browser (i.e. HTTP traffic). They also indicate that ranks worse
and potential usage restrictions make them less likely to be
                                                                                     than 100 000 are not statistically meaningful, and that for these
used in a research context. We also disregard lists that would
                                                                                     sites small changes in measured traffic may cause large rank
require scraping, such as Netcraft2 , as these do not carry the
                                                                                     changes [8], negatively affecting the stability of the list.
same consent of their provider implied by making the list
available in a machine-readable format. Finally, Statvoo’s list3
seemingly meets our criteria. However, we found it to be a                           B. Cisco Umbrella
copy of Alexa’s list of November 23, 2016, having never been                             Cisco Umbrella publishes a daily updated list6 consisting
updated since; we therefore do not consider it in our analysis.                      of one million entries since December 2016 [37]. Any domain
                                                                                     name may be included, with it being ranked on the aggregated
A. Alexa                                                                             traffic counts of itself and all its subdomains.
     Alexa, a subsidiary of Amazon, publishes a daily up-                                The ranks calculated by Cisco Umbrella are based on
dated list4 consisting of one million websites since December                        DNS traffic to its two DNS resolvers (marketed as OpenDNS),
2008 [5]. Usually only pay-level domains5 are ranked, except                         claimed to amount to over 100 billion daily requests from
for subdomains of certain sites that provide ‘personal home                          65 million users [37]. Domains are ranked on the number
pages or blogs’ [8] (e.g. tmall.com, wordpress.com). In Novem-                       of unique IPs issuing DNS queries for them [37]. Not all
ber 2016, Alexa briefly took down the free CSV file with the                         traffic is said to be used: instead the DNS data is sampled and
list [11]. The file has since been available again [10] and is still                 ‘data normalization methodologies’ are applied to reduce bi-
updated daily; however, it is no longer linked to from Alexa’s                       ases [21], taking the distribution of client IPs into account [47].
main website, instead referring users to the paid ‘Alexa Top                         Umbrella’s data collection method means that non-browser-
Sites’ service on Amazon Web Services [12].                                          based traffic is also accounted for. A side-effect is that invalid
   The ranks calculated by Alexa are based on traffic data                           domains are also included (e.g. internal domains such as
from a “global data panel”, with domains being ranked on a                           *.ec2.internal for Amazon EC2 instances, or typos such as
proprietary measure of unique visitors and page views, where                         google.conm).
one visitor can have at most one page view count towards the
page views of a URL [73]. Alexa states that it applies “data                         C. Majestic
normalization” to account for biases in their user panel [8].                           Majestic publishes the daily updated ‘Majestic Million’ list
  1 https://www.similarweb.com/top-websites                                          consisting of one million websites7 since October 2012 [39].
  2 https://toolbar.netcraft.com/stats/topsites                                      The list comprises mostly pay-level domains, but includes sub-
  3 https://statvoo.com/dl/top-1million-sites.csv.zip                                domains for certain very popular sites (e.g. plus.google.com,
  4 https://s3.amazonaws.com/alexa-static/top-1m.csv.zip                             en.wikipedia.org).
  5 A pay-level domain (PLD) refers to a domain name that a consumer or
                                                                                       6 https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip
business can directly register, and consists of a subdomain of a public suffix
or effective top-level domain (e.g. .com but also .co.uk).                             7 http://downloads.majestic.com/majestic_million.csv




                                                                                 2
                                                                                              Umbrella                  Quantcast
    The ranks calculated by Majestic are based on backlinks                  Alexa                                                          Majestic
to websites, obtained by a crawl of around 450 billion URLs                                    29.5%                     7.72%
                                                                                            0.892%            0.319%        2.56%
over 120 days, changed from 90 days on April 12, 2018 [48],
                                                                                 23.7%               0.516%            0.417%           23.7%
[49]. Sites are ranked on the number of class C (IPv4 /24)
                                                                                                        2.48%
subnets that refer to the site at least once [39]. Majestic’s                                2.07% 1.89%     0.725%
                                                                                                                    0.472%
data collection method means only domains linked to from                                                3.03%
other websites are considered, implying a bias towards browser-
based traffic, however without counting actual page visits.
Similarly to search engines, the completeness of their data is           Fig. 1. The average daily intersections between the lists of the four providers
                                                                         from January 30, 2018 to November 13, 2018.
affected by how their crawler discovers websites.

D. Quantcast                                                             used by the provider to compile the list may be older. In
                                                                         addition, we crawled the sites on the four lists as downloaded
    Quantcast publishes a list8 of the websites visited the most         on May 11, 2018 at 13:00 UTC from a distributed crawler
in the United States since mid 2007 [60]. The size of the list           setup of 10 machines with 4 CPU cores and 8 GB RAM in
varies daily, but usually was around 520,000 mostly pay-level            our European university network, using Ubuntu 16.04 with
domains; subdomains reflect sites that publish user content              Chromium version 66.0.3359.181 in headless mode.
(e.g. blogspot.com, github.io). The list also includes ‘hidden
profiles’, where sites are ranked but the domain is hidden.              A. Similarity
    The ranks calculated by Quantcast are based on the number                Figure 1 shows the average number of sites that the
of people visiting a site within the previous month, and                 rankings agree upon per day; there is little variance over
comprises ‘quantified’ sites where Quantcast directly measures           time. The four lists combined contain around 2.82 million
traffic through a tracking script as well as sites where Quant-          sites, but agree only on around 70 000 sites. Using the rank-
cast estimates traffic based on data from ‘ISPs and toolbar              biased overlap (RBO) [72], a similarity measure that can be
providers’ [64]. These estimates are only calculated for traffic         parameterized to give a higher weight to better ranks, we see
in the United States, with only quantified sites being ranked            that the lists of Alexa, Majestic and Quantcast are the most
in other countries; the list of top sites also only considers US         similar to each other. However, even when heavily weighting
traffic. Moreover, while quantified sites see their visit count          the top 100, the RBO remains low between 24% and 33%.
updated daily, estimated counts are only updated monthly [65],           Umbrella’s full list is most dissimilar to the others, with an
which may inflate the stability of the list. Before November 14,         RBO of between 4.5% and 15.5%. However, this is to be
2018, quantified sites made up around 10% of the full (US) list.         expected as Umbrella includes subdomains: when ranking only
However, since then Quantcast seems to have stopped ranking              pay-level domains, the RBO with the other lists reaches around
almost any estimated domains, therefore reducing the list size           30% as well. Finally, Quantcast’s removal of non-quantified
to around 40 000.                                                        sites after November 14, 2018 causes a significant drop in
                                                                         RBO to less than 5.5%, with no overlap of the top 10: many
                III.    Q UANTITATIVE COMPARISON                         very popular domains are not quantified and are therefore now
                                                                         missing from Quantcast’s list.
    Ideally, the domain rankings would perfectly reflect the
popularity of websites, free from any biases. However, the                    The small overlaps signify that there is no agreement on
providers of domain rankings do not have access to complete              which sites are the most popular. This means that switching
Internet usage data and use a variety of largely undisclosed             lists yields a significantly different set of domains that can e.g.
data collection and processing methods to determine the metric           change how prevalent certain web trackers seem to be [26].
on which they rank websites. This may lead to differences
between the lists and potential ‘hidden’ factors influencing             B. Stability
the rankings: the choice of list can then critically affect e.g.             From the intersections between each provider’s lists for two
studies that measure the prevalence of security practices or             consecutive days, shown in Figure 2, we see that Majestic’s and
vulnerabilities. We compare the four main lists over time in             Quantcast’s lists are the most stable, usually changing at most
order to assess the breadth and impact of these differences.             1% per day, while for Umbrella’s list this climbs to on average
    Certain properties may reflect how accurately Internet               10%. Until January 30, 2018, Alexa’s list was almost as stable
usage is measured and may be (more or less) desired when                 as Majestic’s or Quantcast’s. However, since then stability has
using the lists for security research. We consider five properties       dropped sharply, with around half of the top million changing
in our comparison: 1) similarity or the agreement on the set             every day, due to Alexa’s change to a one day average. There
of popular domains, 2) stability or the rank changes over time,          exists a trade-off in the desired level of stability: a very stable
3) representativeness or the reflection of popularity across the         list provides a reusable set of domains, but may therefore
web, 4) responsiveness or the availability of the listed websites,       incorrectly represent sites that suddenly gain or lose popularity.
and 5) benignness or the lack of malicious domains.                      A volatile list however may introduce large variations in the
                                                                         results of longitudinal studies.
   To quantitatively assess these properties, we use the lists
obtained between January 1 and November 30, 2018, referring              C. Representativeness
to the date when the list would be downloaded; the data
                                                                            Sites are mainly distributed over a few top-level domains,
  8 https://ak.quantcast.com/quantcast-top-sites.zip                     with Figure 3 showing that 10 TLDs capture more than 73% of

                                                                     3
                       100
                        90
% daily change


                        80
                        70                                             Alexa              Majestic
                        60                                             Umbrella           Quantcast
                        50
                        45                                                                                  Fig. 4.       The responsiveness and reported HTTP status code across the lists.
                                      Feb        Apr         Jun        Aug         Oct          Dec
                                                                                                                TABLE I.   P RESENCE OF DOMAINS IN THE FOUR RANKINGS ON
       Fig. 2. The intersection percentage between each provider’s lists for two                                     G OOGLE ’ S S AFE B ROWSING LIST ON M AY 31, 2018.
       consecutive days.
                                                                                                                                                                                         Potentially
                       100                                                                                                    Malware         Social Engineering    Unwanted software     harmful
                                                                                                                                                                                         application
                                                                                                                                                                                                        Total
% of domains covered




                        90                                                                                                  100K     Full    10K    100K     Full   10K   100K    Full   100K    Full

                        80                                                                                    Alexa          32      98       4      85      345     0     15     104     0        0    547

                                                                                            Alexa
                                                                                                              Umbrella       11     326       0       3      393     0     23     232     4       60    1011
                        70                                                                                    Majestic      130    1676       0      23      359     1      9     79      9       48    2162
                                                                                            Umbrella          Quantcast      3       76       0       4      105     0      4     41      0        2    224
                        60                                                                  Majestic
                        50                                                                  Quantcast
                        45
                             0              5           10           15           20              25        sites and those without content do not represent real sites and
                                                          Number of TLDs
                                                                                                            may therefore skew e.g. averages of third-party script inclusion
       Fig. 3.                   The cumulative distribution function of TLD usage across the lists.        counts [55], as these sites will be counted as having zero
                                                                                                            inclusions.

       every list. The .com TLD is by far the most popular, at almost                                       E. Benignness
       half of Alexa’s and Majestic’s list and 71% of Quantcast’s
       list; .net, .org and .ru are used most often by other sites. One                                         Malicious campaigns may target popular domains to extend
       notable outlier is the .jobs TLD: while for the other lists it                                       the reach of their attack, or use a common domain as a point of
       does not figure in the top 10 TLDs, it is the fourth most                                            contact, leading to it being picked up as ‘popular’. While it is
       popular TLD for Quantcast. Most of these sites can be traced                                         not the responsibility of ranking providers to remove malicious
       to DirectEmployers, with thousands of lowly ranked domains.                                          domains, popular sites are often assumed to be trustworthy, as
       This serves as an example of one entity controlling a large                                          evidenced by the practice of whitelisting them [29] or, as we
       part of a ranking, potentially giving them a large influence in                                      show in Section IV-A, their usage in security research as the
       research results.                                                                                    benign test set for classifiers.
            We use the autonomous system to determine the entities                                              Table I lists the number of domains flagged on May
       that host the ranked domains. Google hosts the most websites                                         31, 2018 by Google Safe Browsing, used among others by
       within the top 10 and 100 sites, at between 15% and 40%                                              Chrome and Firefox to automatically warn users when they
       except for Quantcast at 4%: for Alexa these are the localized                                        visit dangerous sites [33]. At 0.22% of its list, Majestic has
       versions, for the other lists these are subdomains. For the full                                     the most sites that are flagged as potentially harmful (in
       lists, large content delivery networks dominate, with Cloudflare                                     particular as malware sites), but all lists rank at least some
       being the top network hosting up to 10% of sites across all lists.                                   malicious domains. In Alexa’s top 10 000, 4 sites are flagged
       This shows that one or a few entities may be predominantly                                           as performing social engineering (e.g. phishing), while 1 site in
       represented in the set of domains used in a study and that                                           Majestic’s top 10 000 serves unwanted software. The presence
       therefore care should be taken when considering the wider                                            of these sites in Alexa’s and Quantcast’s list is particularly
       implications of its results.                                                                         striking, as users would have to actively ignore the browser
                                                                                                            warning in order to trigger data reporting for Alexa’s extension
       D. Responsiveness                                                                                    or the tracking scripts.

           Figure 4 shows the HTTP status code reported for the                                                  Given the presence of malicious domains on these lists,
       root pages of the domains in the four lists. 5% of Alexa’s                                           the practice of whitelisting popular domains is particularly
       and Quantcast’s list and 11% of Majestic’s list could not be                                         dangerous. Some security analysis tools whitelist sites on
       reached. For Umbrella, this jumps to 28%; moreover only 49%                                          Alexa’s list [36], [50]. Moreover, Quad9’s DNS-based blocking
       responded with status code 200, and 30% reported a server                                            service whitelists all domains on Majestic’s list [29], exposing
       error. Most errors were due to name resolution failure, as                                           its users to ranked malicious domains. As Quad9’s users expect
       invalid or unconfigured (sub)domains are not filtered out.                                           harmful domains to be blocked, they will be even more under
                                                                                                            the impression that the site is safe to browse; this makes the
           Of the reachable sites, 3% for Alexa and Quantcast, 8.7%                                         manipulation of the list very interesting to attackers.
       for Majestic and 26% for Umbrella serve a page smaller than
       512 bytes on their root page, based on its download size as                                                             IV.          U SAGE IN SECURITY RESEARCH
       reported by the browser instance. As such pages often appear
       empty to the user or only produce an error, this indicates that                                          Whenever security issues are being investigated, re-
       they may not contain any useful content, even though they                                            searchers may want to evaluate their impact on real-world
       are claimed to be regularly visited by real users. Unavailable                                       domains. For these purposes, security studies often use and

                                                                                                        4
 TABLE II.   C ATEGORIZATION OF RECENT SECURITY STUDIES USING
    THE A LEXA RANKING . O NE STUDY MAY APPEAR IN MULTIPLE
                                                                                 B. Influence on security studies
                          CATEGORIES .
                                                                                      1) Incentives: Given the increasing interest in cybersecurity
                                Subset studied                                   within our society, the results of security research have an
  Purpose      10   100   500   1K    10K        100K   1M   Other   Total
                                                                                 impact beyond academia. News outlets increasingly report on
                                                                                 security vulnerabilities, often mentioning their prevalence or af-
  Prevalence   1     6     8     9     16         7     32    13      63
  Evaluation   7    16    14    10      9         3     14    28      71         fected high-profile entities [30]–[32], [70]. Meanwhile, policy-
  Whitelist    0     2     1     4      3         2     11     6      19         makers and governments rely on these studies to evaluate
  Ranking      0     1     3     3      2         4     15     7      28
                                                                                 secure practices and implement appropriate policies [15], [25];
  Total        8    20    18    18     23         9     45    36     133         e.g. Mozilla in part decided to delay distrusting Symantec cer-
                                                                                 tificates based on a measurement across Umbrella’s list [68].
                                                                                      Malicious actors may therefore risk exposure to a wider
reference the top sites rankings. The validity and representa-                   audience, while their practices may trigger policy changes,
tiveness of these rankings therefore directly affects their results,             yielding them an incentive to directly influence security studies.
and any biases may prohibit correct conclusions being made.                      Invernizzi et al. [38] discovered that blacklists sold on under-
Moreover, if forged domains could be entered into these lists,                   ground markets contain IP addresses of academic institutions
an adversary can control research findings in order to advance                   as well as security companies and researchers, illustrating
their own goals and interests.                                                   that adversaries already actively try to prevent detection by
                                                                                 researchers. As we showed, security studies often rely on
                                                                                 popularity rankings, so pitfalls in the methods of these rankings
A. Survey and classification of list usage                                       that expose them to targeted manipulation open up another
                                                                                 opportunity for adversaries to affect security research. The way
    To assess how security studies use these top sites rankings,                 in which an adversary may want to influence rankings, and
we surveyed the papers from the main tracks of the four main                     therefore the research dependent upon them, varies according
academic security conferences (CCS, NDSS, S&P, USENIX                            to their incentives. They may want to promote domains into the
Security) from 2015 to 2018; we select these venues as they                      lists, making them be perceived as benign and then execute ma-
are considered top-tier and cover general security topics. We                    licious practices through them. Alternatively, they can promote
classify these papers according to four purposes for the lists:                  other domains to hide their own malicious domains from the
prevalence if the rankings are used to declare the proportion                    lists. Finally, they can intelligently combine both techniques
of sites affected by an issue; evaluation if a set of popular                    to alter comparisons of security properties for websites of
domains serves to test an attack or defense, e.g. for evaluating                 different entities.
Tor fingerprinting [61]; whitelist if the lists are seen as a source
of benign websites, e.g. for use in a classifier [71]; ranking if                    2) Case study: The issue of online tracking and fingerprint-
the exact ranks of sites are mentioned or used (e.g. to estimate                 ing has been studied on multiple occasions for Alexa’s top one
website traffic [26]) or if sites are divided into bins according                million [26], [42], [44], [45], [55]. Users may want to avoid
to their rank.                                                                   organizations that perform widespread or invasive tracking, and
                                                                                 therefore have an interest in new tracking mechanisms and/or
    Alexa is by far the most popular list used in recent security                specific trackers being found or named by these studies, e.g.
studies, with 133 papers using the list for at least one purpose.                to include them in blocklists. The trackers therefore have an
Table II shows the number of papers per category and per                         incentive to avoid detection by not figuring among the domains
subset of the list that was used. The Alexa list is mostly used                  being studied, e.g. by pushing these out of the popularity
for measuring the prevalence of issues or as an evaluation set                   ranking used to provide the set of investigated domains.
of popular domains. For the former purpose as well as for
                                                                                     We quantify the effort required to manipulate a ranking
whitelisting and ranking or binning, the full list is usually used,
                                                                                 and therefore alter findings for the measurements of finger-
while for evaluation sets, the subset size varies more widely.
                                                                                 printing prevalence by Acar et al. [3] and Englehardt and
Three papers from these conferences also used another ranking,
                                                                                 Narayanan [26] on Alexa’s top 100 000 and top one million
always in tandem with the Alexa list [17], [74], [75].
                                                                                 respectively. These studies published data on which domains
    Most studies lack any comment on when the list was                           included which scripts, including the Alexa rank. We calculate
downloaded, when the websites on the lists were visited                          how many domains minimally need to be moved up in order
and what proportion was actually reachable. This hampers                         to push out the websites using a particular tracking provider.
reproducibility of these studies, especially given the daily                         Figure 5 shows how many fingerprinting providers would
changes in list compositions and ranks.                                          fully disappear from the Alexa list if a given number of
                                                                                 domains are manipulated. We consider removal for different
    Two papers commented on the methods of the rankings.
                                                                                 subsets, as commonly used by the studies that we surveyed in
Juba et al. [40] mention the rankings being “representative of
                                                                                 Section IV-A. The smallest number of manipulated domains
true traffic numbers in a coarse grained sense”. Felt et al. [27]
                                                                                 required is 7 032, 1 652, 74 and 24 for the top 1M, 100K,
mention the “substantial churn” of Alexa’s list and the unavail-
                                                                                 10K and 1K respectively; 15 providers need less than 100 000
ability of sites, and express caution in characterizing all its sites
                                                                                 manipulated domains to disappear from the top 1M.
as popular. However, in general the studies do not question the
validity of the rankings, even though they have properties that                      As we will show, the cost of such large-scale manipulation
can significantly affect their conclusions, and as we will show                  is very low and well within reach of larger providers, espe-
are vulnerable to manipulation.                                                  cially given the incentive of being able to stealthily continue

                                                                             5
                         100
% of providers removed
                                                                                           TABLE III.         S UMMARY OF MANIPULATION TECHNIQUES AND THEIR
                                 top 1M                                                                                ESTIMATED COST.
                         75      top 100K
                                 top 10K                                                                                                     Cost
                         50      top 1K
                                                                                                  Provider      Technique         Monetary   Effort    Time
                         25
                                                                                                  Alexa         Extension          none      medium    low
                          0                                                                                     Certify           medium     medium    high
                                    102      103             104      105     106                 Umbrella      Cloud providers    low       medium    low
                                                   Domains to boost                               Majestic      Backlinks          high       high     high
                                                                                                                Reflected URLs     none       high    medium
                                                                                                  Quantcast     Quantified         low       medium    high
        Fig. 5. The percentage of fingerprinting script providers that would not be
        detected if a given number of domains were pushed above all fingerprinting
        domains for different subsets of Alexa’s ranking.
                                                                                              These techniques can be applied to both new domains and
                                                                                          domains already present in the lists, e.g. when those domains
        tracking. Moreover, this is an upper bound needed to remove                       bear the properties that could skew certain studies; a domain
        all instances of a tracker domain from the list; reducing the                     that has been ranked for a longer period of time may enjoy a
        prevalence of a script requires only hiding the worst-ranked                      higher trust or importance. In our work, we focus on techniques
        domains. Finally, it is not required to insert new domains:                       that directly influence the rankings’ data at a modest cost. An
        forging a few requests to boost sites already in the list is                      alternative approach could be to buy expired or parked domains
        sufficient, further reducing the cost and even making the                         already in the list [53]. However, expired domains are usually
        manipulation harder to detect.                                                    bought up very quickly by “drop-catchers” [43], leaving a
                                                                                          limited number of ranked domains open for registration [63].
           Englehardt and Narayanan highlighted how “the long tail of                     Meanwhile, popular parked domains can command prices
       fingerprinting scripts are largely unblocked by current privacy                    upwards of 1 000 USD [63]. This approach therefore incurs
       tools,” reinforcing the potential impact of exposing these                         a prohibitive cost, especially at a large scale.
       scripts. A malicious party can therefore gain an advantage by
       actively manipulating the rankings of popular domains. As we
       will show in the next section, such manipulation is actually                       A. Alexa
       feasible across all four lists, usually even on a sufficiently large                   Alexa ranks domains based on traffic data from two
       scale without the need for significant resources.                                  sources: their “Traffic Rank” browser extension that reports
                                                                                          all page visits, and the “Certify” analytics service that uses a
                           V.   F EASIBILITY OF LARGE - SCALE MANIPULATION                tracking script to count all visits on subscribing websites. We
                                                                                          forge traffic data to both and observe the achieved ranks.
           The data collection processes of popularity rankings rely
                                                                                              1) Extension: The “Alexa Traffic Rank” extension collects
       on a limited view of the Internet, either by focusing on one
                                                                                          data on all pages that its users visit. The extension also shows
       specific metric or because they obtain information from a small
                                                                                          users information on the rank and traffic of the visited site,
       population. This implies that targeted small amounts of traffic
                                                                                          which may serve as an incentive to install the extension.
       can be deemed significant on the scale of the entire Internet and
       yield good rankings. Moreover, the ranking providers generally                         We submitted page visits for both registered and nonexis-
       do not filter out automated or fake traffic, or domains that                       tent test domains previously unseen by Alexa. We generated
       do not represent real websites, further reducing the share of                      profiles with all 1 152 possible configurations, i.e. the demo-
       domains with real traffic in their lists.                                          graphic details that are requested when installing the extension,
                                                                                          and this within a short timeframe from the same IP address;
            Consequently, attacks that exploit these limitations are                      Alexa did not impose any limits on the number of profiles
        especially effective at allowing arbitrary modifications of the                   that could be created. We submitted visits to one domain per
        rankings at a large scale. We showed how adversaries may                          profile; as visits to the same page by the same profile are only
        have incentives to skew the conclusions of security studies, and                  counted once [8], we generated exactly one visit per page to
        that security researchers and practitioners often use popularity                  the homepage and randomly generated subpages. The number
        rankings to drive the evaluation of these studies. Manipulating                   of page views for one test domain ranges from 1 to 30.
        these rankings therefore becomes a prime vector for influenc-
        ing security research, and as we will show, the small costs and                       We installed the extension in a real Chrome browser
        low technical requirements associated with this manipulation                      instance and then generated page visits to our test domain,
        make this approach even more attractive.                                          simulating a realistic usage pattern by spacing out page visits
                                                                                          between 30 and 45 seconds, and interspersing them with
           For each of the four studied popularity rankings, we                           as many visits to domains in Alexa’s top 1000. Through
       describe techniques that manipulate the data collection process                    inspection of the extension’s source code and traffic, we found
       through the injection of forged data. To prove their feasibility,                  that upon page load, a GET request with the full URL of
       we execute those techniques that conform to our ethical frame-                     the visited page9 is sent alongside the user’s profile ID and
       work and that have a reasonable cost, and show which ranks                         browser properties to an endpoint on data.alexa.com. This
       can be achieved. In Table III, we summarize the techniques and                     means these requests can also be generated directly without the
       the cost they incur on three aspects: money, effort and time                       need to use an actual browser, greatly reducing the overhead
       required. Through this cost assessment, we identify how these                      in manipulating many domains on a large scale.
       manipulations could be applied at scale and affect a significant
       portion of these lists.                                                              9 For pages loaded over HTTPS, the path is obfuscated.




                                                                                      6
       350000                                           0                                                                107                                         107.5 * r 1.125




                                                                                                    Estimated requests
       400000
                                                    50000                                                                105
       450000
       500000                                       100000                                                               103
Rank




       550000




                                             Rank
                                                    150000                                                               101
       600000
                                                    200000                                                                     1   10   100    1000      10000     100000       1000000
       650000                                                                                                                                  Rank
       700000                                       250000
                                                                                                          Fig. 7. The estimated relation between requests and rank for Alexa. The gray
       750000                                       300000                                                areas show data as retrieved from the Alexa Web Information Service.
                1 4 7 10 13 16 19 22 25 28                   0   5000 10000 15000 20000 25000
                        Requests                                       Requests
                (a) Extension.                                   (b) Certify.                             in the ranking: these point towards the same number of visits
Fig. 6. Ranks obtained in the Alexa list. Ranks on the same day are connected.                            being counted for these domains. We use these blocks as well
                                                                                                          as the processed visitor and view metrics retrieved from the
                                                                                                          Alexa Web Information Service [13] to estimate the required
    From May 10, 2018 onward, Alexa appears to block data                                                 visit count for better ranks.
reporting from countries in the European Union (EU) and
European Economic Area (EEA), as the response changed                                                         Figure 7 shows the number of requests needed to achieve a
from the visited site’s rank data shown to the user to the                                                certain rank; we consider this an upper bound as Alexa ranks
string “Okay”. This is likely due to the new General Data                                                 domains that see more unique visitors better than those with
Protection Regulation coming into force. While we were able                                               more page views, meaning that manipulation with multiple
to circumvent this block through a VPN service, Alexa may                                                 profiles would require less requests. This analysis shows that
be ignoring traffic in EU and EEA countries, introducing a                                                even for very good ranks, the amount of requests required and
further bias towards traffic from other countries.                                                        accompanying cost remains low, e.g. only requiring 1 000 page
                                                                                                          views for rank 10 000. This model of Alexa’s page visits also
    For 20% of our profiles/domains, we were successful in                                                corresponds with previous observations of Zipf’s law in web
seeing our page views counted and obtaining rankings within                                               traffic [4], [22].
the top million. Alexa indicates that it applies statistical
processing to its data [73], and we suspect that some of our                                                   Alexa’s list is also susceptible to injection of nonexistent
requests and generated profiles were pruned or not considered                                             domains; we were able to enter one such domain. Furthermore,
sufficient to be ranked, either because of the profile’s properties                                       we confirmed in our server logs that none of our test domains
(e.g. a common browser configuration or an overrepresented                                                were checked by Alexa as we forged page visit requests. The
demographic) or because only a subset of traffic data is (ran-                                            ability to use fake domains reduces the cost to manipulate the
domly) selected. To increase the probability of getting domains                                           list at scale even further: an attacker is not required to actually
ranked, an adversary can select only the successful profiles, or                                          purchase domain names and set up websites for them.
generate page views to the same site with different profiles in                                              Even though Alexa’s statistical postprocessing may prune
parallel, improving the efficiency of their manipulation.                                                 some visits, the low number of required visits, the ability to
     Figure 6(a) lists our 224 successful rankings grouped per                                            quickly generate new profiles and the lack of filtering of fake
day, showing the relation between ranks and number of visits.                                             domains allows an attacker to still easily achieve significant
We performed our experiments between July 25 and August                                                   manipulation of Alexa’s list.
5, 2018. As during this period Alexa averaged traffic over one                                               2) Certify: Alexa’s ‘Certify’ service offers site owners an
day, there was only a delay of one day between our requests                                               analytics platform, using a tracking script installed on the
and the domains being ranked; they disappeared again from the                                             website to directly measure traffic. The service requires a
list the following day. This means that it is not necessary to                                            subscription to Alexa’s services, which start at USD 19.99 per
forge requests over a longer period of time when the malicious                                            month for one website.
campaign is short-lived.
                                                                                                             As Alexa verifies installation of its scripts before tracking
    What is most striking, is the very small number of page                                              visits, we installed them on a test website. From the JavaScript
visits needed to obtain a ranking: as little as one request                                              part of this code, we extracted its reporting algorithm and
yielded a rank within the top million, and we achieved a rank                                            repeatedly forged GET requests that made us appear as a new
as high as 370 461 with 12 requests (albeit in the week-end,                                             user visiting the website, therefore avoiding the need to retain
when the same number of requests yields a better rank). This                                             the response cookies for continued tracking. To diversify the
means that the cost to manipulate the rankings is minimal,                                               set of IP addresses sending this forged traffic, we sent these
allowing adversaries to arbitrarily alter the lists at large scale                                       requests over the Tor network, which has a pool of around
for an extended period of time. This ensures continued ranking                                           1 000 IP addresses [69]. We sent at most 16 000 requests per
and increases the likelihood of a list containing manipulated                                            24 hours, of which half were for the root page of our domain,
domains being used for research purposes, despite the large                                              and the other half for a randomly generated path.
daily change.
                                                                                                             Figure 6(b) lists the ranks of our test domain and the
   The low number of required requests is further confirmed                                               number of visits that were logged by Alexa across 52 days.
by large blocks of alphabetically ordered domains appearing                                               For 48 days, we reached the top 100 000 (purported to more

                                                                                                7
accurately reflect popularity), getting up to rank 28 798. Not                    200000
all our requests were seen by Alexa, but we suspect this is                       400000
rather due to our setup (e.g. by timeouts incurred while sending




                                                                           Rank
                                                                                  600000
requests over Tor). Alexa’s metrics report that our site received
"100.0% real traffic" and that no traffic was excluded, so we                     800000
suspect that Alexa was not able to detect the automated nature                    1000000
of our requests.                                                                            0   250   500   750   1000   1250    1500   1750   2000
                                                                                                                   IPs
    After subscription to the service, Alexa will only calculate
(and offer to display) the ‘Certified’ rank of a website after              Fig. 8. Ranks obtained in the Umbrella list. Ranks on the same day are
                                                                            connected; ranks over two days for one set of requests use the same line
21 days. Since no visits to our site were being reported                    style.
through Alexa’s extension, no ‘normal’ rank was achieved in
the meantime, and therefore there was a large delay between
the start of the manipulation and the ranking of the domain.                (i.e. addresses permanently assigned to a user) yields higher
                                                                            throughput, at 10 seconds per IP. However, AWS and other
    The disadvantage of this technique is that the cost of ma-
                                                                            providers such as Microsoft Azure discourage this practice by
nipulation at scale quickly becomes prohibitive, as for each site
                                                                            attaching a cost to this ‘remap’ operation: for AWS, a remap
that needs to be inserted into the list, a separate subscription
                                                                            costs USD 0.10, so a set of 10 000 IPs incurs a prohibitive
is required. Given Alexa’s verification of the tracking script
                                                                            cost of USD 1 000.
being installed, the domain needs to be registered and a real
website needs to be set up, further reducing the scalability                    Figure 8 shows the relation between the number of issued
of the technique. However, we were able to achieve better                   DNS requests and the obtained rank; all of our attempts
ranks with a more consistent acceptance of our forged requests.             were successful. We were able to obtain ranks as high as
Depending on the attacker’s goal, it is of course still possible            200 000 with only a thousand unique IP addresses, albeit in
to artificially increase the ranking of specific websites who               the weekend, when OpenDNS processes around 30% less DNS
already purchased and installed the Alexa Certify service.                  traffic [57]. We only sustained DNS traffic for one day at
                                                                            a time, but it appears that Umbrella counts this traffic (and
    We obtained a rank even though we did not simulate
                                                                            therefore ranks the domain) for two days, reducing the number
traffic to this test domain through the Alexa extension, which
                                                                            of requests needed per day to either obtain a good rank for one
strongly suggests that Alexa does not verify whether ‘Certified’
                                                                            domain or rank many domains.
domains show similar (credible) traffic in both data sources.
Based on this observation, we found one top 100 ‘Certified’                     Given the relatively high cost per IP, inserting multiple
site where Alexa reports its extension recording barely any or              domains actually is more economical as several DNS requests
even no traffic: while in this case it is a side-effect of its usage        can be sent for each IP instantiation. As the name requested in
pattern (predominantly mobile), it implies that manipulation                the DNS query can be chosen freely, inserting fake domains
conducted solely through the tracking script is feasible.                   is also possible; the high number of invalid entries already
                                                                            present shows that Umbrella does not apply any filtering.
B. Cisco Umbrella                                                           This further improves scalability of this technique, as no real
                                                                            websites need to be set up in order to manipulate the list.
    Umbrella ranks websites on the number of unique client
                                                                                The effort to generate many ranked entries is further
IPs issuing DNS requests for them. Obtaining a rank therefore
                                                                            reduced by the inclusion of subdomains, as all subdomains at
involves getting access to a large variety of IP addresses and
                                                                            lower depths are automatically ranked: we were able to rank
sending (at least) one DNS request from those IPs to the two
                                                                            12 subdomains simultaneously with one set of requests. Fur-
open DNS resolvers provided by Umbrella.
                                                                            thermore, the number of requests is aggregated per subdomain,
    1) Cloud providers: Cloud providers have obtained large                 so a low number of requests to many subdomains can result
pools of IP addresses for distribution across their server                  in both many ranked subdomains and a good rank for the pay-
instances; e.g. Amazon Web Services (AWS) owns over 64                      level domain.
million IPv4 addresses [14]. These can be used to procure the                   Combining the ability to insert fake domains with the low
unique IP addresses required for performing DNS requests, but               overhead of requests to additional domains, the inclusion of
due to their scarcity, providers restrict access to IPv4 addresses          subdomains and the lack of any filtering or manipulation detec-
either in number or by introducing a cost.                                  tion means that the scale at which an attacker can manipulate
    In the case of AWS, there are two options for rapidly                   Umbrella’s list can be very large.
obtaining new IPv4 addresses. Continuously starting and stop-                      2) Alternatives:
ping instances is an economical method, as even 10 000
different IPs can be obtained for less than USD 1 (using                        • Tor. The Tor service provides anonymous communica-
the cheapest instance type), but the overhead of relaunching                tion between a user and the service they use. Traffic is relayed
instances reduces throughput: on the cheapest t2.nano in-                   across multiple nodes before being sent to the destination from
stance, we were able to obtain a new IP on average every                    an exit node, meaning that the destination observes traffic
minute. Moreover, the number of concurrent running instances                originating from that node’s IP address. This set of exit nodes
is limited, but by using instances in multiple regions or even              provide a pool of IP addresses, and by switching the routing
multiple accounts, more instances are accessible. Keeping one               over the Tor network, DNS requests can be altered to appear
instance and allocating and deallocating Elastic IP addresses               to originate from multiple IP addresses in this pool. However,

                                                                       8
                                                                                     0
as there are less than 1 000 exit nodes at any given point in
time [69], it will be possible to inject domains in the list, but               250000
infeasible to obtain a high rank solely through this technique.




                                                                         Rank
                                                                                500000
    • IP spoofing. IP packets contain the IP address of its
sender, that can however be arbitrarily set in a technique known                750000                                               Backlinks
                                                                                                                                     Reflected URLs
as IP spoofing. We could leverage this technique to set the                     1000000
source IP of our DNS packets to many different addresses,                                     103               104                105
in order for our requests to appear for Umbrella to originate                                                   Subnets
from many unique IPs. As IP spoofing is often used during                 Fig. 9. The relation between subnets and rank in the Majestic list for May
denial-of-service attacks, many ISPs block outgoing packets               31, 2018, with our obtained ranks highlighted.
with source IPs outside their network. Leveraging IP spoofing
for sending DNS requests therefore requires finding a network
that supports it. Karami et al. [41] found that certain VPS                   The cheapest type of backlink costs USD 0.25 a month,
providers allow IP spoofing; as such these could be used for              but since there was not a sufficient amount of such pages to
our experiment.                                                           cover the necessary number of subnets, more expensive back-
    Due to the ethical concerns that are raised by leveraging             links were also required. The backlinks were partially found
IP spoofing (the responses of our DNS requests would arrive               organically by Majestic; in this case there is no additional cost.
at the users of the forged source IPs, and the associated traffic         Through a subscription on Majestic’s services, backlinks can
may cause the VPS provider to be flagged as malicious), we                also be submitted explicitly for crawling: the minimum cost is
did not further explore this technique. It is important to note           USD 49.99 for one month.
however that an adversary only needs to find a single provider
or network that does not prevent IP spoofing in order to send                 We bought backlinks for our test domain and curated them
a very large number of DNS requests to Umbrella’s resolvers               for two and a half months, in order to capture as many subnets
and thus manipulate the list at a very large scale.                       as possible while managing the monetary cost. Our total cost
                                                                          was USD 500. We successfully inserted our domain, with
C. Majestic                                                               Figure 9 showing the achieved rankings on top of the relation
                                                                          between the rank and the number of found subnets for all
   Majestic’s ranking is based on the number of subnets                   ranked sites as published by Majestic.
hosting a website that links to the ranked domain. Therefore,
we cannot construct data reporting requests sent directly to                  There exists a trade-off between the cost and the time
Majestic, but must use techniques where website owners                    required to enter the rank: if the monetary cost should be kept
knowingly or unknowingly serve a page that contains a link to             low, more time is needed as the set of eligible backlink pages
our domain and that is then crawled independently by Majestic.            is smaller and backlinks will need to be deleted. Alternatively,
                                                                          a higher number of possibly more expensive backlinks would
    1) Backlinks: Backlink providers offer a paid service where           allow to achieve the necessary number of subnets more quickly,
they place incoming links for a requested website (‘backlinks’)           but at a higher monetary cost. Conversely, because Majestic
on various sites. The goal of this service is usually to achieve          considers links for at least 120 days, the cost for long-term
a higher position in search engine rankings, as part of search            manipulation is relatively limited: even though we stopped
engine optimization (SEO) strategies; the deceptive nature of             buying backlinks and these subsequently disappeared, our
this technique makes that this is considered ‘black-hat’ SEO.             ranking was still maintained for more than two months as
    Backlinks are priced differently according to the reputation          previously found backlinks were still counted.
of the linking site. While we need a sufficiently diverse set
of websites hosted on different subnets, Majestic does not                    2) Reflected URLs: An alternative technique that we dis-
take the quality of our backlinks into account when ranking               covered, for which it is not required to purchase services from
domains. This means that we can reduce our cost by choosing               external parties, is to leverage websites that reflect a GET
the cheapest type of backlink. Moreover, we have the choice               parameter into a link. Note that for our purpose, reflected cross-
of removing backlinks after they have been found, as these                site scripting (XSS) attacks could also be used; however, this
are no longer billed but still count towards the subnets for a            technique is more intrusive as it will inject HTML elements,
period of at most 120 days, reducing monetary cost.                       so we did not evaluate it out of ethical considerations. To
                                                                          discover web pages that reflect a URL passed as a parameter,
    We use the services of BackLinks.com, as they operate                 we started crawling the 2.8 million domains from the four lists,
only on sites under their control, therefore avoiding impact of           finding additional pages by following links from the homepage
our experiment on unaware site owners. The choice for this                of these domains. If GET parameters were found on the page,
particular backlink provider brings about certain constraints             we replaced each one with a URL and tested whether this URL
(such as the pool of available backlink sites, or a limit on daily        was then included in the href of an a tag on the page.
backlink deletions), but these can be alleviated by using other
and/or multiple backlink providers. We buy backlinks if they                  Through this crawl, we found that certain MediaWiki sites
are located in a subnet not covered by any already purchased              were particularly susceptible to reflecting URLs on each page,
site, but have to use OCR as the URLs on which links would                depending on the configuration of the site. We therefore tested
be placed are only available as a warped image. We therefore              this reflection on the wikis from a number of data sources:
curated the set of backlinks through manual verification to               the root domains as well as the subdomains containing wiki
compensate for any errors, increasing our required effort.                of the four top lists, the set of wikis found by Pavlo and

                                                                     9
Shi in 2011 [59] and the wikis found by WikiTeam10 . As                     manual effort, as well as in monetary cost, as for each hosting
the reflection is purely achieved through altering the GET                  provider a subscription needs to be bought.
parameters, we do not permanently alter the wiki.                               • Pingbacks. Content management systems such as Word-
                                                                            Press provide a pingback mechanism for automatically report-
    Given the special construction of their URLs, the pages
                                                                            ing URLs that link to one of the pages hosted on that system.
reflecting our domain will not be found organically by Majestic.
                                                                            Many sites will then insert a link back to the reported URL on
The list of affected URLs can be submitted directly to Majestic,
                                                                            that page. By finding a set of domains supporting pingbacks
but this requires a subscription. The links can also be placed
                                                                            (similar to finding wikis) and reporting a URL on the domain
on one aggregating web page: by verifying ownership of
                                                                            we want to see ranked, we could again have links to our domain
the hosting domain with Majestic, a crawl of this page and
                                                                            on a large set of domains and therefore subnets. However, this
subsequently of the links placed on it can be triggered for
                                                                            permanently changes pages on other websites, and although
free; alternatively, using Majestic’s site to request the freely
                                                                            enabling the pingback feature implies some consent, we opted
available subset of backlinks data for this special web page
                                                                            to not explore this technique for ethical reasons.
also seems to trigger this crawl.
    Through our crawls, we found 1 041 pages that reflected                 D. Quantcast
the URL of our test domain when passed in a GET param-
                                                                                1) Quantified: Quantcast mainly obtains traffic data
eter. Through submitting these reflecting URLs to Majestic’s
                                                                            through its tracking script that webmasters install on their
crawler, we successfully ranked our domain, with Figure 9
                                                                            website. We extracted the reporting algorithm from the tracking
showing the achieved rankings over time. Through this tech-
                                                                            script, and automatically sent requests to Quantcast from a set
nique, we also successfully had one backlink to a non-existing
                                                                            of 479 VPN servers located in the United States, as Quantcast’s
domain crawled and counted as a referring subnet. By scaling
                                                                            ranking only takes US traffic into account. We sent requests
this up to the number of subnets required to be ranked, this
                                                                            for 400 generated users per day, presenting ourselves as a new
implies that Majestic’s list ranking is also susceptible to fake
                                                                            user on the first request and subsequently reusing the generated
entries; as there are unavailable sites in the list, Majestic likely
                                                                            token and received cookie in four more requests. As opposed
does not actively check whether entries in the list are real.
                                                                            to Alexa’s tracking script, reporting page views for only new
    This technique allows to construct backlinks at no monetary             users did not result in any visits being counted.
cost, but requires a high effort to find appropriate pages. We                  Our forged requests were acknowledged by Quantcast and
found only small subsets of wikis and domains in general to                 its analytics dashboard reports that on May 30, 2018, "the
reflect our URL, so the number of pages and subnets that can                destination reaches over 6,697 people, of which 6,696 (100%)
be discovered using this technique may not be sufficient to                 are in the U.S." The latter metric is used to determine the rank.
achieve very high rankings. Given a deeper crawl of pages,                  However, our test domain has not appeared in the ranking.
more sites that reflect URLs passed through a GET parameters                This is likely due to the short age of our domain; although we
may be found, more subnets can be covered and a higher                      have sent requests for more than a month, Quantcast’s slow
ranking can be achieved. Moreover, an attacker can resort                   update frequency means its ranking algorithm may not take
to more ‘aggressive’ techniques where URLs are permanently                  our domain into account yet.
stored on pages or XSS vulnerabilities are exploited.
                                                                                As Quantcast publishes the number of visits counted for
    Once found however, a reflecting URL will be counted                    each ranked domain, the relation between the desired rank and
indefinitely: a site would effectively have to be reconfigured or           required effort is known as shown in Figure 10. Up to around
taken offline in order for the backlink to disappear. This means            5 000 visits, the achieved rank remains relatively low; this tail
maintaining a rank comes at no additional cost. Furthermore,                contains primarily quantified sites that are ranked even with
every website that is susceptible to URL reflection can be                  almost no visits. Above 5 000 visits, Quantcast’s list includes
leveraged to promote any number of attacker-chosen (fake)                   many more domains for which a rank is estimated; especially at
domains, at the cost of submitting more (crafted) URLs to                   worse ranks, large blocks of estimated domains are interspersed
Majestic. This means that manipulation of Majestic’s list is                with quantified domains, so increasing the number of visits to
also possible on a large scale.                                             jump across such a block gives a large improvement in rank.
   3) Alternatives:                                                         If a rank were to be assigned to our domain, we can determine
                                                                            that we would theoretically be given a rank around 367 000.
    • Hosting own sites. Using domains seen in passive DNS                  Achieving higher ranks only requires submitting more forged
measurements, Tajalizadehkhoob et al. [67] identified 45 434                requests, so the increased cost in time and effort is minimal.
hosting providers in 2016, and determined their median address
space to contain 1 517 IP addresses. Based on these figures,                    Quantcast will only start processing traffic data once it has
we can assume that the number of subnets available through                  verified (through crawling) that its tracking pixel is present on
hosting providers is well above the threshold to be ranked by               the domain. It is therefore required to register the domain and
Majestic. An attacker could therefore set up websites on a                  set up a real website to manipulate the rankings, so scaling to
sufficient number of these providers, all with a link back to               multiple domains incurs a higher cost; Quantcast’s analytics
the domain to be ranked. By making all the websites link to                 platform itself is free however, limiting the additional cost. As
each other, a larger set of domains could easily be ranked. This            Quantcast performs the check only once, the domain and the
technique incurs a high cost however: in effort, as setting up              website also do not need to be sustained. Merely registering for
accounts with these providers is very likely to require a lot of            tracking may even suffice to be ranked: over 2 000 domains are
                                                                            ranked but reported to have 0 visits, with over half registered
  10 https://github.com/WikiTeam/wikiteam                                   by DirectEmployers as discussed in Section III-C.

                                                                       10
            0
                                                                                     that in general many more ranked domains are unavailable
       100000
                                                                                     or unrepresentative. Our sites only hosted benign content, so
       200000                                                                        whitelists using rankings are unaffected.
Rank



       300000
       400000                                                                               VI.    A N IMPROVED TOP WEBSITES RANKING
       500000
                100   101   102    103    104     105    106     107     108             As we showed, the different methods used to generate
                                         Visits                                      popularity rankings cause undesirable effects on their prop-
                                                                                     erties that can potentially sway the results and conclusions of
 Fig. 10. The relation between measured visits and rank in the Quantcast list        studies. In addition, we showed that researchers are prone to
 for May 31, 2018, with the theoretical rank for our visit count highlighted.
                                                                                     ignore or be unaware of these effects. We also proved that
                                                                                     these rankings show several pitfalls that leave them vulnerable
     2) Alternatives: Quantcast states that it also uses traffic                     to large-scale manipulation, further reducing their reliability
 data from ‘ISPs and toolbar providers’ [64]. ISPs sell traffic                      and suitability to research. Nevertheless, popularity rankings
 data to third parties [18], and Quantcast may be buying these                       remain essential for large-scale empirical evaluations, so we
 services to generate the number of page visits and therefore                        propose improvements to existing rankings as well as a new
 the rank for non-quantified websites. However, we cannot                            ranking that has characteristics geared towards research.
 determine which ISPs may be used. As for extensions, we
 were unable to discover any extensions reporting to a URL                           A. Defending existing rankings against manipulation
 that was obviously related to Quantcast.                                                Even though the methods for data collection and processing
        Ethical considerations: Because our experiments may                          of the existing lists are usually unknown, our experiments
 have a large impact on the reputation of the rankings as well as                    suggest that their providers employ little defense against large-
 potentially affect third parties, we conduct an ethical review of                   scale manipulation. We outline techniques that the providers
 our experimental methods. Such reviews have been advocated                          could use to make these lists more resilient to attacks.
 for by the academic community [58] and ensure that the                                  Detecting and deterring singular instances of fraud ensures
 potential damage inflicted is minimized. We base this review                        that all data used in ranking domains is deemed valid. Alexa
 on the ethical principles outlined in the Menlo Report [24],                        and Quantcast rely on the reporting of page visits; within the
 which serves as a guideline within the field of ICT research;                       realm of online advertising, techniques have been designed to
 we apply the principle of beneficence in particular: identifying                    subvert click inflation [2], [16], [51]. As we saw that not all
 potential benefits and harms, weighing them against each other                      attempts at manipulating Alexa’s ranking were successful, this
 and minimizing the risk of inflicting harm.                                         may imply that Alexa already employs some of these tactics.
     Because of their commercial nature, the providers of popu-                          To deter large-scale manipulation, ranking providers could
 larity rankings have an economic interest in these being accu-                      employ tactics that increase the effort and resources required
 rate. We show that these lists can be manipulated, negatively                       to affect many domains to prohibitive levels. This therefore
 affecting their perceived reputability. Our findings are however                    avoids significant influence on research results, even if these
 of value to the providers: by evaluating the various techniques                     tactics may not be sufficient to stop small-scale manipulation.
 and reporting our findings, the providers become aware of the
 potential threats, may take actions to thwart attackers and can                         For a traffic reporting extension, the profile setup could
 improve the correctness of their rankings.                                          be tied to an account at an online service; while a normal
                                                                                     user can easily create one account, creating many accounts
     We have disclosed our findings and proposals for potential                      in an automated way can be countered by techniques that try
 remedies to the four providers, alongside a list of manipulated                     to detect fake accounts [20]. In the case of Alexa, given its
 domains for them to remove from their datasets and past                             ownership by Amazon, a natural choice would be to require
 and present rankings. Alexa and Majestic provided statements                        an Amazon account; in fact, a field for such an account ID is
 regarding the value of their rankings and the (in)feasibility                       available when registering the extension, but is not required.
 of manipulation, but commercial considerations prevent them                         This technique is not useful for tracking scripts, since no user
 from elaborating on their methods. Cisco Umbrella closed our                        interaction can be requested, and fraud detection as discussed
 issue without any statement, and we received no response                            earlier may be required. For providers that use both, the two
 from Quantcast. None of our test domains were (retroactively)                       metrics can be compared to detect anomalies where only one
 removed from any rankings after our notification.                                   source reports significant traffic numbers, as we suspect such
                                                                                     manipulation is already happening for Alexa Certify.
     We minimize the impact of our experiments on third parties
 by only significantly manipulating the ranking of our own,                              Data could be filtered on the IP address from which it
 purposefully registered domains and refraining from intrusive                       originates. Ignoring requests from ranges belonging to cloud
 or questionable techniques. Our sites also contained an ex-                         providers or conversely requiring requests to come from ranges
 planation of our experiment and contact details for affected                        known to belong to Internet service providers (e.g. through
 parties. Our low number of test domains means that only                             its autonomous system) does not block a single user from
 few domains will see negligible shifts in ranking due to our                        reporting their traffic. However, using many IP addresses
 experiments; e.g. the volatility of Alexa’s list has a significantly                concurrently is prevented as these cannot be easily obtained
 larger impact. Moreover, we minimized the duration of our                           within the permitted ranges. This technique is particularly
 experiments and of our domains being ranked. The impact on                          useful for Umbrella’s list; for the other lists, using many IP
 other research using these lists is also minimal; we showed                         addresses is not strictly necessary for large-scale manipulation.

                                                                                11
    The relative difficulty of maliciously inserting links into                 To improve the stability of our combined lists, we allow
pages on many IP subnets already reduces the vulnerability                 to average ranks over the lists of several days; our standard
of link-based rankings to large-scale manipulation. Specific               list uses the lists of the past 30 days. Again, we allow to
attacks where the page reflects a URL passed as a parameter                filter out domains that appear only for one or a few days, to
could be detected, although this can be made more difficult by             avoid briefly popular (or manipulated) domains. Conversely, if
obfuscation and attacks that alter a page more permanently.                capturing these short-term effects is desired, lists based on one
The link-based rankings could be refined with reputation                   day’s data are available. When combining lists, we also provide
scores, e.g. the age of a linked page or Majestic’s “Flow                  the option to only consider a certain subset of the input lists,
Metrics” [48], to devalue domains that are likely to be part               to select domains that are more likely to actually be popular.
of a manipulation campaign.
                                                                               Differences in list composition complicate the combination
    Finally, requiring ranked domains to be available and to               of the lists. Umbrella’s list includes subdomains; we include
host real content increases the cost of large-scale manipulation,          an option to use a recalculated ranking that only includes pay-
as domain names need to be bought and servers and web pages                level domains. Quantcast’s list contains less than one million
need to be set up. For Umbrella, not ranking domains where                 domains; we proportionally rescale the scores used in the two
name resolution fails can significantly reduce unavailable (and            combination methods to the same range as the other lists.
therefore possibly fake) domains in the list. The other providers
                                                                               We add filters to create a list that represents a certain
can perform similar availability checks in the DNS or by
                                                                           desired subset of popular domains. A researcher can either
crawling the domain.
                                                                           only keep domains with certain TLDs to select sites more
                                                                           likely to be associated with particular countries or sectors, or
B. Creating rankings suitable for research                                 exclude (overly represented) TLDs. To avoid the dominance of
    As we cannot ensure that providers will (want to) imple-               particular organizations in the list, a filter can be applied where
ment changes that discourage (large-scale) manipulation, we                only one domain is ranked for each set of pay-level domains
look at combining all currently available ranking data with                that differ only in TLD. Finally, only certain subdomains can
the goal of improving the properties of popularity rankings                be retained, e.g. to heuristically obtain a list of authentication
for research, canceling out the respective deficiencies of the             services by selecting login.* subdomains.
existing rankings. To this extent, we introduce T RANCO, a                      To allow researchers to work with a set of domains that
service that researchers can use to obtain lists with such more            is actually reachable and representative of real websites, we
desirable and appropriate properties. We provide standard lists            provide options to filter the domains on their responsiveness,
that can be readily used in research, but also allow these lists to        status code and content length. We base these filters on a
be highly configurable, as depending on the use case, different            regular crawl of the union of all domains on the four existing
traffic sources or varying degrees of stability may be beneficial.         lists. This ensures that the sample of domains used in a study
                                                                           yields results that accurately reflect practices on the web.
     Moreover, we provide a permanent record to these new
lists, their configuration and their construction methods. This                To further refine on real and popular websites, we include
makes historical lists more easily accessible to reduce the                a filter on the set of around 3 million distinct domains in
effort in replicating studies based upon them, and ensures that            Google’s Chrome User Experience Report, said to be ‘popular
researchers can be aware of the influences on the resulting list           destinations on the web’ [34]. Its userbase can be expected
by its component lists and configuration.                                  to be (much) larger than e.g. Alexa’s panel; however, Google
                                                                           themselves indicate that it may not fully represent the broader
     Our service is available at https://tranco-list.eu. The
                                                                           Chrome userbase [34]. Moreover, the list is only updated
source code is also openly published at https://github.com/
                                                                           monthly and does not rank the domains, so it cannot be used
DistriNet/tranco-list to provide full transparency of how our
                                                                           as a replacement for the existing rankings.
lists are processed.
                                                                               To reduce the potential effects of malicious domains on
    1) Combination options and filters: We support creating                research results (e.g. in classifier accuracy), we allow to
new lists where the ranks are averaged across a chosen period              remove domains on the Google Safe Browsing list [33] from
of time and set of providers, and introduce additional filters,            our generated lists.
with the goal of enhancing the research-oriented properties of
our new lists.                                                                 2) Evaluation: We evaluate the standard options chosen
                                                                           for our combined lists on their improvements to similarity and
    In order to improve the rank of the domains that the lists             stability; the representativeness, responsiveness and benignness
agree upon, we allow to average ranks over the lists of some               of the included domains can be improved by applying the
or all providers. We provide two combination methods: the                  appropriate filters. We generate our combined lists from March
Borda count where, for a list of length N , items are scored with          1, 2018 to November 14, 2018, to avoid distortions due to
N, N −1, ..., 1, 0 points; and the Dowdall rule where items are            Alexa’s and Quantcast’s method changes, and truncate them to
scored with 1, 1/2, ..., 1/(N − 1), 1/N points [28]. The latter            one million domains, as this is the standard for current lists.
reflects the Zipf’s law distribution that website traffic has been
modeled on [4], [22]. Our standard list applies the Dowdall                        a) Similarity: To determine the weight of the four ex-
rule to all four lists. We also allow to filter out domains that           isting lists, we calculate the rank-biased overlap with our com-
appear only on one or a few lists, to avoid domains that are               bined lists. Across different weightings, the RBO with Alexa’s
only marked as popular by one provider: these may point to                 and Majestic’s lists is highest at 46.5–53.5% and 46.5–52%
isolated manipulation.                                                     respectively, while the RBO with Quantcast’s and Umbrella’s

                                                                      12
lists is 31.5–40% and 33.5–40.5% respectively. These results                                     VII.     R ELATED WORK
are affected by the differences in list composition: subdomains
                                                                                 The work that is most recent and most closely related to
for Umbrella and the shorter list for Quantcast mean that these
                                                                            ours is that of Scheitle et al. [62], who compared Alexa’s,
two lists have less entries potentially in common with Alexa
                                                                            Majestic’s and Umbrella’s lists on their structure and stability
and Majestic, reducing their weight. Overall, there is no list
                                                                            over time, discussed their usage in (Internet measurement)
with a disproportionate influence on the combined list.
                                                                            research through a survey of recent studies, calculated the
        b) Stability: Averaging the rankings over 30 days is                potential impact on their results, and drafted guidelines for
beneficial for stability: for the list combining all four providers,        using the rankings. We focus on the implications of these
on average less than 0.6% changes daily, even for smaller                   lists for security research, expanding the analysis to include
subsets. For the volatile Alexa and Umbrella lists, the improve-            representativeness, responsiveness and benignness. Moreover,
ment is even more profound: the daily change is reduced to                  we are the first to empirically demonstrate the possibility of
1.8% and 0.65% respectively. This means that the data from                  malicious large-scale manipulation, and propose a concrete
these providers can be used even in longitudinal settings, as               solution to these shortcomings by providing researchers with
the set of domains does not change significantly.                           improved and publicly available rankings.
   3) Reproducibility: Studies rarely mention the date on                       In 2006, Lo and Sedhain [46] studied the reliability of
which a ranking was retrieved, when the websites on that list               website rankings in terms of agreement, from the standpoint of
were visited and whether they were reachable. Moreover, it is               advertisers and consumers looking for the most relevant sites.
hard to obtain the list of a previous date: only Cisco Umbrella             They discussed three ranking methods (traffic data, incoming
maintains a public archive of historical lists [21]. These two              links and opinion polls) and analyzed the top 100 websites
aspects negatively affect the reproducibility of studies, as the            for six providers, all of which are still online but, except for
exact composition of a list cannot be retrieved afterwards.                 Alexa, have since stopped updating their rankings.
    In order to enhance the reproducibility of studies that use                 Meusel et al. [52] published one-time rankings of web-
one of our lists, we include several features that are designed             sites11 , based on four centrality indices calculated on the
to create a permanent record that can easily be referenced.                 Common Crawl web graph [23]. Depending on the index, these
Once a list has been created, a permanent short link and a                  ranks vary widely even for very popular sites. Moreover, such
preformatted citation template are generated for inclusion in               centrality indices can be affected by manipulation [35], [56].
a paper. Alongside the ability to download the exact set of
domains that the list comprises, the page available through this                In his analysis of DNS traffic from a Tor exit node,
link provides a detailed overview of the configuration used to              Sonntag [66] finds that popularity according to Alexa does
create that particular list and of the methods of the existing              not imply regular traffic over Tor, listing several domains
rankings, such that the potential influences of the selected                with a good Alexa rank but that are barely seen in the DNS
method can be assessed. This increases the probability that                 traffic. These conclusions confirm that different sources show
researchers use the rankings in a more well founded manner.                 a different view of popularity, and that the Alexa list may not
                                                                            be the most appropriate for all types of research (e.g. into Tor).
    4) Manipulation: Given that our combined lists still rely on
the data from the four existing lists, they remain susceptible                                    VIII.    C ONCLUSION
to manipulation. As domains that appear on all lists simultane-
ously are favored, successful insertion in all lists at once will               We find that 133 studies in recent main security confer-
yield an artificially inflated rank in our combined list.                   ences base their experiments on domains from commercial
                                                                            rankings of the ‘top’ websites. However, the data sources
    However, the additional combinations and filters that we                and methods used to compile these rankings vary widely and
propose increase the effort required to have manipulated do-                their details are unknown, and we find that hidden properties
mains appear in our combined lists. Averaging ranks over a                  and biases can skew research results. In particular, through
longer period of time means that manipulation of the lists needs            an extensive evaluation of these rankings, we detect a recent
to be maintained for a longer time; it also takes longer for the            unannounced change in the way Alexa composes its list: their
manipulated domains to obtain a (significant) aggregated rank.              data is only averaged over a single day, causing half of the list
Moreover, intelligently applying filters can further reduce the             to change every day. Most probably, this unknowingly affected
impact of manipulation: e.g. removing unavailable domains                   research results, and may continue to do so. However, other
thwarts the ability to use fake domains.                                    rankings exhibit similar problems: e.g. only 49% of domains
     As each ranking provider has their own traffic data source,            in Umbrella’s list respond with HTTP status code 200, and
the effects of manipulating one list are isolated. As none of the           Majestic’s list, which Quad9 uses as a whitelist, has more than
lists have a particularly high influence in the combined list, all          2 000 domains marked as malicious by Google Safe Browsing.
four lists need to manipulated to the same extent to achieve                     The reputational or commercial incentives in biasing the
a comparable ranking in the combined list, quadrupling the                  results of security studies, as well as the large trust placed in
required effort. For the combined list generated for October 31,            the validity of these rankings by researchers, as evidenced by
2018, achieving a rank within the top million would require                 only two studies putting their methods into question, makes
boosting a domain in one list to at least rank 11 091 for one day           these rankings an interesting target for adversarial manipula-
or rank 332 778 for 30 days; for a rank within the top 100 000,             tion. We develop techniques that exploit the pitfalls in every
ranks 982 and 29 479 would be necessary respectively. This                  list by forging the data upon which domain rankings are based.
shows that massive or prolonged manipulation is required to
appear in our combined list.                                                  11 http://wwwranking.webdatacommons.org/




                                                                       13
Moreover, many of these methods bear an exceptionally low                             [9] ——. (2018, May) What exactly is the Alexa Traffic Panel? [Online].
cost, both technically and in resources: we only needed to craft                          Available: https://support.alexa.com/hc/en-us/articles/200080859
a single HTTP request to appear in Alexa’s top million sites.                        [10] Alexa Support (@AlexaSupport). (2016, Nov.) Thanks to customer
This provides an avenue for manipulation at a very large scale,                           feedback, the top 1M sites is temporarily available again. We’ll provide
                                                                                          notice before updating the file in the future. [Online]. Available:
both in the rank that can be achieved and in the number of                                https://twitter.com/Alexa_Support/status/801167423726489600
domains artificially inserted into the list. Adversaries can there-
                                                                                     [11] ——. (2016, Nov.) Yes, the top 1m sites file has been
fore sustain massive manipulation campaigns over time to have                             retired. [Online]. Available: https://twitter.com/Alexa_Support/status/
a significant impact on the rankings, and, as a consequence, on                           800755671784308736
research and the society at large.                                                   [12] Amazon Web Services, Inc. (2018, Mar.) Alexa Top Sites. [Online].
                                                                                          Available: https://aws.amazon.com/alexa-top-sites/
    Ranking providers carry out few checks on their traffic data,
                                                                                     [13] ——. (2018, Aug.) Alexa Web Information Service. [Online]. Available:
as is apparent from our ability to insert nonexistent domains,                            https://aws.amazon.com/awis/
further simplifying manipulation at scale. We outline several                        [14] ——. (2018, Apr.) AWS IP address ranges. [Online]. Available:
mitigation strategies, but cannot be assured that these will                              https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html/
be implemented. Therefore, we introduce T RANCO, a new                               [15] Y. Aydin, “Étude nationale portant sur la sécurité de lespace
ranking based on combining the four existing lists, along-                                numérique français 2017,” pp. 4–14, Oct. 2017, available in
side the ability to filter out undesirable (e.g. unavailable or                           English at https://www.economie.gouv.fr/files/2017_National_Study_
malicious) domains. These combined lists show much better                                 Cybersecurity.pdf. [Online]. Available: https://www.economie.gouv.fr/
                                                                                          files/2017_Etude_nationale_securite_numerique.pdf
stability over time, only changing by at most 0.6% per day,
and are much more resilient against manipulation, where even                         [16] C. Blundo, S. Cimato, and B. Masucci, Secure Metering Schemes.
                                                                                          Springer US, 2010, pp. 1–32.
manipulating one list to reach the top 1 000 only yields a rank
                                                                                     [17] K. Borgolte, C. Kruegel, and G. Vigna, “Meerkat: Detecting website
of 100 000 in our combined list. We offer an online service at                            defacements through image-based object recognition,” in Proc. USENIX
https://tranco-list.eu to access these rankings in a reproducible                         Security, 2015, pp. 595–610.
manner, so that researchers can continue their evaluation with                       [18] J. Brodkin. (2017, Mar.) How ISPs can sell your
a more reliable and suitable set of domains. This helps them in                           Web history — and how to stop them. Ars Technica.
assuring the validity, verifiability and reproducibility of their                         [Online]. Available: https://arstechnica.com/information-technology/
studies, making their conclusions about security on the Internet                          2017/03/how-isps-can-sell-your-web-history-and-how-to-stop-them/
more accurate and well founded.                                                      [19] BuiltWith Pty Ltd. (2018, Sep.) Alexa Certified site metrics usage
                                                                                          statistics. [Online]. Available: https://trends.builtwith.com/analytics/
                                                                                          Alexa-Certified-Site-Metrics
                        ACKNOWLEDGMENT                                               [20] Q. Cao, M. Sirivianos, X. Yang, and T. Pregueiro, “Aiding the detection
                                                                                          of fake accounts in large scale social online services,” in Proc. NSDI,
    The authors would like to thank Vera Rimmer, Davy                                     2012, pp. 197–210.
Preuveneers and Quirin Scheitle for their valuable input. This                       [21] Cisco Umbrella. (2016) Umbrella popularity list. [Online]. Available:
research is partially funded by the Research Fund KU Leuven.                              https://s3-us-west-1.amazonaws.com/umbrella-static/index.html
Victor Le Pochat holds a PhD Fellowship of the Research                              [22] A. Clauset, C. R. Shalizi, and M. E. J. Newman, “Power-law distri-
Foundation - Flanders (FWO).                                                              butions in empirical data,” SIAM Review, vol. 51, no. 4, pp. 661–703,
                                                                                          2009.
                                                                                     [23] Common Crawl Foundation. Common Crawl. [Online]. Available:
                             R EFERENCES                                                  https://commoncrawl.org/
 [1] (2018, Nov.) Alexa Traffic Rank - Chrome Web Store. [Online].                   [24] D. Dittrich and E. Kenneally, “The Menlo Report: Ethical principles
     Available: https://chrome.google.com/webstore/detail/alexa-traffic-rank/             guiding information and communication technology research,” U.S.
     cknebhggccemgcnbidipinkifmmegdel                                                     Department of Homeland Security, Tech. Rep., Aug. 2012.
 [2] M. Abu Rajab, F. Monrose, A. Terzis, and N. Provos, “Peeking through            [25] N. Doty, “Mitigating browser fingerprinting in web specifications,”
     the cloud: DNS-based estimation and its applications,” in Proc. ACNS,                W3C, W3C Editor’s Draft, Jul. 2018. [Online]. Available: https:
     2008, pp. 21–38.                                                                     //w3c.github.io/fingerprinting-guidance/
 [3] G. Acar, C. Eubank, S. Englehardt, M. Juarez, A. Narayanan, and                 [26] S. Englehardt and A. Narayanan, “Online tracking: A 1-million-site
     C. Diaz, “The web never forgets: Persistent tracking mechanisms in                   measurement and analysis,” in Proc. CCS, 2016, pp. 1388–1401.
     the wild,” in Proc. CCS, 2014, pp. 674–689.                                     [27] A. P. Felt, R. Barnes, A. King, C. Palmer, C. Bentzel, and P. Tabriz,
 [4] L. A. Adamic and B. A. Huberman, “Zipf’s law and the Internet,”                      “Measuring HTTPS adoption on the web,” in Proc. USENIX Security,
     Glottometrics, vol. 3, pp. 143–150, 2002.                                            2017, pp. 1323–1338.
 [5] Alexa Internet, Inc. (2008, Dec.) Global top sites. [On-                        [28] J. Fraenkel and B. Grofman, “The Borda count and its real-world al-
     line]. Available: https://web.archive.org/web/20081216072512/http:                   ternatives: Comparing scoring rules in Nauru and Slovenia,” Australian
     //www.alexa.com:80/site/ds/top_sites                                                 Journal of Political Science, vol. 49, no. 2, pp. 186–205, 2014.
 [6] ——. (2016, Jan.) Does Alexa have a list of its top-                             [29] S. Gallagher. (2017, Nov.) New Quad9 DNS service
     ranked websites? Archived on April 4, 2016. [Online].                                blocks malicious domains for everyone. Ars Technica. [On-
     Available:            https://web.archive.org/web/20160404003433/https:              line]. Available: https://arstechnica.com/information-technology/2017/
     //support.alexa.com/hc/en-us/articles/200449834-Does-Alexa-have-                     11/new-quad9-dns-service-blocks-malicious-domains-for-everyone/
     a-list-of-its-top-ranked-websites-                                              [30] D. Goodin. (2015, Oct.) Don’t count on STARTTLS to automatically
 [7] ——. (2017, Jan.) Does Alexa have a list of its top-                                  encrypt your sensitive e-mails. Ars Technica. [Online]. Avail-
     ranked websites? Archived on March 11, 2017. [Online].                               able:    https://arstechnica.com/information-technology/2015/10/dont-
     Available:            https://web.archive.org/web/20170311160137/https:              count-on-starttls-to-automatically-encrypt-your-sensitive-e-mails/
     //support.alexa.com/hc/en-us/articles/200449834-Does-Alexa-have-                [31] ——. (2015, May) HTTPS-crippling attack threatens tens of
     a-list-of-its-top-ranked-websites-                                                   thousands of Web and mail servers. Ars Technica. [Online]. Avail-
 [8] ——. (2017, Nov.) How are Alexa’s traffic rankings determined? [On-                   able:     https://arstechnica.com/information-technology/2015/05/https-
     line]. Available: https://support.alexa.com/hc/en-us/articles/200449744              crippling-attack-threatens-tens-of-thousands-of-web-and-mail-servers/


                                                                                14
[32]   ——. (2016, Mar.) More than 11 million HTTPS websites                            [54] P. M. Napoli, P. J. Lavrakas, and M. Callegaro, “Internet and mobile
       imperiled by new decryption attack. Ars Technica. [Online]. Avail-                   ratings panels,” in Online Panel Research: A Data Quality Perspective.
       able:      https://arstechnica.com/information-technology/2016/03/more-              Wiley-Blackwell, 2014, ch. 17, pp. 387–407.
       than-13-million-https-websites-imperiled-by-new-decryption-attack/              [55] N. Nikiforakis, L. Invernizzi, A. Kapravelos, S. Van Acker, W. Joosen,
[33]   Google Inc. Safe browsing. [Online]. Available: https://safebrowsing.                C. Kruegel, F. Piessens, and G. Vigna, “You are what you include:
       google.com/                                                                          Large-scale evaluation of remote JavaScript inclusions,” in Proc. CCS,
[34]   Google, Inc. (2018, Jan.) Chrome User Experience Report.                             2012, pp. 736–747.
       [Online]. Available: https://developers.google.com/web/tools/chrome-            [56] Q. Niu, A. Zeng, Y. Fan, and Z. Di, “Robustness of centrality measures
       user-experience-report/                                                              against network manipulation,” Physica A: Statistical Mechanics and
[35]   Z. Gyöngyi, P. Berkhin, H. Garcia-Molina, and J. Pedersen, “Link spam                its Applications, vol. 438, pp. 124–131, 2015.
       detection based on mass estimation,” in Proc. VLDB, 2006, pp. 439–              [57] OpenDNS. OpenDNS System. [Online]. Available: https://system.
       450.                                                                                 opendns.com/
[36]   E.     Hjelmvik.        (2017,   Apr.)    Domain      whitelist   bench-        [58] C. Partridge and M. Allman, “Ethical considerations in network mea-
       mark: Alexa vs Umbrella. NETRESEC. [Online]. Avail-                                  surement papers,” Communications of the ACM, vol. 59, no. 10, pp.
       able: https://www.netresec.com/?page=Blog&month=2017-04&post=                        58–64, Sep. 2016.
       Domain-Whitelist-Benchmark%3A-Alexa-vs-Umbrella                                 [59] A. Pavlo and N. Shi, “Graffiti networks: A subversive, Internet-
[37]   D. Hubbard. (2016, Dec.) Cisco Umbrella 1 million. [Online]. Available:              scale file sharing model,” ArXiv e-prints, 2011. [Online]. Available:
       https://umbrella.cisco.com/blog/2016/12/14/cisco-umbrella-1-million/                 http://arxiv.org/abs/1101.0350
[38]   L. Invernizzi, K. Thomas, A. Kapravelos, O. Comanescu, J. Picod, and            [60] Quantcast. (2007, Jul.) Open internet ratings service. [On-
       E. Bursztein, “Cloak of visibility: Detecting when machines browse a                 line]. Available: https://web.archive.org/web/20070705200342/http:
       different web,” in Proc. SP, 2016, pp. 743–758.                                      //www.quantcast.com/
[39]   D. Jones. (2012, Oct.) Majestic Million CSV now free for                        [61] V. Rimmer, D. Preuveneers, M. Juarez, T. Van Goethem, and W. Joosen,
       all, daily. [Online]. Available: https://blog.majestic.com/development/              “Automated website fingerprinting through deep learning,” in Proc.
       majestic-million-csv-daily/                                                          NDSS, 2018.
[40]   B. Juba, C. Musco, F. Long, S. Sidiroglou-Douskos, and M. Rinard,               [62] Q. Scheitle, O. Hohlfeld, J. Gamba, J. Jelten, T. Zimmermann, S. D.
       “Principled sampling for anomaly detection,” in Proc. NDSS, 2015.                    Strowes, and N. Vallina-Rodriguez, “A long way to the top: Significance,
                                                                                            structure, and stability of Internet top lists,” in Proc. IMC, 2018, pp.
[41]   M. Karami, Y. Park, and D. McCoy, “Stress testing the booters:                       478–493.
       Understanding and undermining the business of DDoS services,” in
       Proc. WWW, 2016, pp. 1033–1043.                                                 [63] M. Schmidt. (2018, Aug.) Expired domains. [Online]. Available:
                                                                                            https://www.expireddomains.net
[42]   D. Kumar, Z. Ma, Z. Durumeric, A. Mirian, J. Mason, J. A. Halderman,
                                                                                       [64] S. Simpson. (2018, Jan.) For sites that are not Quantified, it
       and M. Bailey, “Security challenges in an increasingly tangled web,” in
                                                                                            says “data is estimated.” What does this mean? [Online]. Available:
       Proc. WWW, 2017, pp. 677–684.
                                                                                            https://quantcast.zendesk.com/hc/en-us/articles/115013961667
[43]   C. Lever, R. Walls, Y. Nadji, D. Dagon, P. McDaniel, and M. Anton-
                                                                                       [65] ——. (2018, Jan.) What is the date range for the traffic numbers
       akakis, “Domain-Z: 28 registrations later. Measuring the exploitation of
                                                                                            on your site? [Online]. Available: https://quantcast.zendesk.com/hc/en-
       residual trust in domains,” in Proc. SP, 2016, pp. 691–706.
                                                                                            us/articles/115013961687
[44]   T. Libert, “Exposing the hidden web: An analysis of third-party HTTP            [66] M. Sonntag, “DNS traffic of a Tor exit node - an analysis,” in Proc.
       requests on 1 million websites,” International Journal of Communica-                 SpaCCS, 2018, pp. 33–45.
       tion, vol. 9, pp. 3544–3561, Oct. 2015.
                                                                                       [67] S. Tajalizadehkhoob, M. Korczyński, A. Noroozian, C. Gañán, and
[45]   ——, “An automated approach to auditing disclosure of third-party data                M. van Eeten, “Apples, oranges and hosting providers: Heterogeneity
       collection in website privacy policies,” in Proc. WWW, 2018, pp. 207–                and security in the hosting market,” in Proc. NOMS, 2016, pp. 289–297.
       216.
                                                                                       [68] W. Thayer. (2018, Oct.) Delaying further Symantec TLS certificate dis-
[46]   B. W. N. Lo and R. S. Sedhain, “How reliable are website rankings?                   trust. Mozilla Foundation. [Online]. Available: https://blog.mozilla.org/
       Implications for e-business advertising and Internet search,” Issues in              security/2018/10/10/delaying-further-symantec-tls-certificate-distrust/
       Information Systems, vol. VII, no. 2, pp. 233–238, 2006.
                                                                                       [69] The Tor Project. (2018, Apr.) Number or relays with relay flags
[47]   O. Lystrup. (2016, Dec.) Cisco Umbrella releases free top 1 million                  assigned. [Online]. Available: https://metrics.torproject.org/relayflags.
       sites list. [Online]. Available: https://medium.com/cisco-shifted/cisco-             html?start=2017-01-01&end=2018-04-26&flag=Exit
       umbrella-releases-free-top-1-million-sites-list-8497fba58efe
                                                                                       [70] J. Valentino-DeVries. (2015, May) New computer bug exposes
[48]   Majestic-12 Ltd. Frequently asked questions. [Online]. Available:                    broad security flaws. The Wall Street Journal. [Online]. Avail-
       https://majestic.com/support/faq                                                     able: https://www.wsj.com/articles/new-computer-bug-exposes-broad-
[49]   ——. (2018, Apr.) Majestic launch a bigger fresh index. [On-                          security-flaws-1432076565
       line]. Available: https://blog.majestic.com/company/majestic-launch-a-          [71] T. Vissers, W. Joosen, and N. Nikiforakis, “Parking sensors: Analyzing
       bigger-fresh-index/                                                                  and detecting parked domains,” in Proc. NDSS, 2015.
[50]   X. Mertens. (2017, Apr.) Whitelists: The holy grail of attackers. SANS          [72] W. Webber, A. Moffat, and J. Zobel, “A similarity measure for indefinite
       Internet Storm Center. [Online]. Available: https://isc.sans.edu/forums/             rankings,” ACM Transactions on Information Systems, vol. 28, no. 4, pp.
       diary/Whitelists+The+Holy+Grail+of+Attackers/22262/                                  1–38, Nov. 2010.
[51]   A. Metwally, D. Agrawal, A. E. Abbad, and Q. Zheng, “On hit inflation           [73] J. Yesbeck. (2014, Oct.) Your top questions about Alexa data
       techniques and detection in streams of web advertising networks,” in                 and ranks, answered. [Online]. Available: https://blog.alexa.com/top-
       Proc. ICDCS, 2007, pp. 52–52.                                                        questions-about-alexa-answered/
[52]   R. Meusel, S. Vigna, O. Lehmberg, and C. Bizer, “The graph structure            [74] X. Zhang, X. Wang, X. Bai, Y. Zhang, and X. Wang, “OS-level side
       in the Web – analyzed on different aggregation levels,” The Journal of               channels without procfs: Exploring cross-app information leakage on
       Web Science, vol. 1, no. 1, pp. 33–47, 2015.                                         iOS,” in Proc. NDSS, 2018.
[53]   G. C. M. Moura, M. Müller, M. Davids, M. Wullink, and C. Hesselman,             [75] S. Zimmeck, J. S. Li, H. Kim, S. M. Bellovin, and T. Jebara, “A privacy
       “Domain names abuse and TLDs: From monetization towards mitiga-                      analysis of cross-device tracking,” in Proc. USENIX Security, 2017, pp.
       tion,” in Proc. IM, May 2017, pp. 1077–1082.                                         1391–1408.




                                                                                  15
