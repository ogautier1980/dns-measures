# Fiche de lecture - Impact DNS Resolvers sur Performance CDN

**Référence bibliographique** :
Hours, H., Biersack, E., & Loiseau, P. (2016). *A study of the impact of DNS resolvers on CDN performance using a causal approach*. Computer Networks, 109, 200-210. https://doi.org/10.1016/j.comnet.2016.05.011

**Thème** :
Impact du choix de service DNS (ISP local DNS vs Google Public DNS) sur performance CDN via approche causale (réseaux bayésiens)

**Intérêt pour le mémoire** :
Quantifie avec approche causale pourquoi le choix de resolver DNS impacte la performance CDN : redirection géographique (20 ms vs 48 ms RTT) + paramétrage serveurs TCP (congestion window). Démontre que local DNS offre meilleur débit (+14% distance, +30% config serveur) malgré adoption croissante DNS publics. Pertinent pour comprendre impact diversité géographique queries DNS.

---

## Contexte de lecture

**Date de lecture** : 21 mars 2026
**Section du mémoire** :
- Section 2.6 (CDN, DNS resolvers, performance géographique)

---

## Contenu de l'article

### Objectif(s) / Question(s) de recherche

**Problème** : Impact du choix de service DNS sur performance web/CDN largement discuté mais **difficile à quantifier causalement** :
- DNS local ISP → clients redirigés vers serveurs proches (ECS, geolocation)
- DNS publics (Google DNS, OpenDNS) → adoption croissante mais redirection potentiellement suboptimale
- Question ouverte : Quelle **part de l'impact** due à distance serveurs vs configuration serveurs ?

**Questions de recherche** :
1. Quel impact **causal** du choix DNS (LDNS vs GDNS) sur throughput client ?
2. Impact via **distance/latency** (RTT externe) ?
3. Impact via **configuration serveurs** (paramètres TCP, congestion window) ?

**Approche innovante** : **Causal inference** via réseaux bayésiens (Bayesian networks) pour dépasser limitations corrélation statistique et permettre **what-if questions** (interventions contrefactuelles).

### Méthodologie

- **Type d'étude** : Mesures passives (packet traces) + modélisation causale (Bayesian networks)
- **Infrastructure** :
  - **PoP European ISP** (Point of Presence, grand ISP européen)
  - **Trafic CDN Akamai** extrait (>90% trafic DNS = LDNS ou GDNS)
  - **Probe** placée entre clients et serveurs
  - **Internal network (isp)** : client ↔ probe
  - **External network (inet)** : probe ↔ server (Internet)

- **Échelle** :
  - **~7,000 TCP connections** (>2MB chaque, éliminer slowstart)
  - **2 jours** : jeudi + dimanche, 17h30-21h30 (peak hours)
  - **19 paramètres** par connexion

- **Outils** :
  - **Tstat** : extraction metrics packet traces (RTT, windows, loss, retransmissions)
  - **PC algorithm** : construction Bayesian network (structure learning)
  - **Kernel-based independence tests** : validation dépendances
  - **Gaussian copulae** : estimation densités probabilité multidimensionnelles

- **Protocole causal** :
  1. **Collecte données** : traces IP, extraction 19 paramètres
  2. **Modèle causal** : PC algorithm → Bayesian network (Fig. 1)
  3. **Validation** : d-separation, conditional independencies
  4. **Interventions** : counterfactual predictions (do-calculus)
     - "What if LDNS users had RTT distribution of GDNS users?"
     - "What if LDNS servers had cwinmin config of GDNS servers?"

**Paramètres (19 variables)** :
- **Temps** : dow (day of week), tod (time of day)
- **DNS** : dns (LDNS=local ISP, GDNS=Google DNS)
- **Serveur** : dstip (destination AS number)
- **Volume** : nbbytes (Mbytes)
- **RTT** :
  - **isp** : isprttavg, isprttstd, ispnbhops
  - **inet** : inetrttavg, inetrttstd, inetnbhops
- **Receiver window** : rwin0, rwinmin, rwinmax
- **Congestion window** : cwinmin, cwinmax
- **Loss** : retrscore (fraction retransmissions), rto (timeouts boolean)
- **Performance** : tput (throughput Mbps)

### Résultats principaux

#### 1. Statistiques descriptives LDNS vs GDNS

**Table 2 - Comparaison moyenne (μ)** :

| Paramètre | LDNS | GDNS | Ratio |
|-----------|------|------|-------|
| **isprttavg** (ms) | 80 | 61 | GDNS 24% meilleur |
| **isprttstd** (ms) | 1100 | 76 | GDNS 93% moins variable |
| **inetrttavg** (ms) | **20** | **48** | **LDNS 2.4× meilleur** |
| **inetrttstd** (ms) | 8.6 | 6.5 | LDNS 32% plus variable |
| **inetnbhops** | 8.7 | 12 | LDNS 38% moins hops |
| **cwinmin** (kB) | **0.9** | **1.2** | **GDNS 33% meilleur** |
| **cwinmax** (kB) | 163 | 118 | LDNS 38% meilleur |
| **tput** (Mbps) | 3.2 | 3.0 | LDNS 7% meilleur |

**Observations clés** :
- **RTT externe (inetrttavg)** : LDNS = **20 ms** vs GDNS = **48 ms** (2.4×)
  - LDNS → serveurs **proches** (même AS souvent)
  - GDNS → serveurs **éloignés** (parfois hors Europe)

- **Congestion window min (cwinmin)** : LDNS = 0.9 kB vs GDNS = 1.2 kB (33% supérieur)
  - Configuration serveurs différente
  - GDNS servers = paramétrage TCP plus agressif

- **Throughput final** : LDNS = 3.2 Mbps vs GDNS = 3.0 Mbps (**7% seulement**)
  - Petit écart malgré RTT 2.4× différent
  - Suggère **compensation** par configuration serveurs

- **RTT interne (isprttavg)** : 80 ms (LDNS) vs 61 ms (GDNS)
  - Variance énorme (isprttstd = 1100 ms LDNS, 76 ms GDNS)
  - Explication : ADSL access + large buffers (bufferbloat)

#### 2. Modèle causal (Bayesian network, Figure 1)

**Dépendances clés identifiées** :

**DNS → inetrttavg** (direct parent) :
- Confirmation causale : choix DNS **cause** changement RTT externe
- Mécanisme : DNS local → redirection AS local (proche)
- GDNS → redirection serveurs globaux (éloignés)

**DNS → cwinmin** (direct parent) :
- Choix DNS **cause** changement configuration TCP serveurs
- Serveurs proches (LDNS) vs serveurs éloignés (GDNS) = paramétrages différents

**tput parents directs** (6 facteurs) :
1. **inetrttstd** (variance RTT externe)
2. **isprttavg** (RTT interne moyen)
3. **retrscore** (loss)
4. **rto** (timeouts)
5. **cwinmin** (congestion window min)
6. **cwinmax** (congestion window max)

**Absences notables** :
- **rwin*** (receiver window) ≠ parent direct tput
  - Raison (Fig. 2) : receiver window jamais limitant (clients peuvent toujours absorber débit)
- **dns** ≠ parent direct **tput**
  - Impact **indirect** via inetrttavg + cwinmin
  - Confirme : DNS impacte performance via mécanismes intermédiaires

**Insights contre-intuitifs** :
- **isprttstd** (variance RTT interne) ≠ parent tput
  - Malgré variance énorme (σ=1100 ms)
  - Mais **inetrttstd** (variance RTT externe) = parent direct
  - Causal model révèle : variance externe plus impactante que variance interne

- **dow** (day of week) → **dns** (choice DNS)
  - Jeudi : 72% LDNS, 28% GDNS
  - Dimanche : 93% LDNS, 7% GDNS
  - Hypothèse : devices différents (travail vs maison), localisation clients

#### 3. Interventions causales (counterfactuals)

**Intervention 1 : Distance/Latency** (Section 4.2.1)

**Question** : "Quel serait le throughput des clients LDNS si redirects vers serveurs avec RTT distribution de GDNS ?"

**Equation contrefactuelle** (Eq. 7-10) :
- Intervention : do(RTT ∼ f_{RTT|GDNS})
- Prédiction : f(tput | LDNS, do(RTT ~ GDNS))

**Résultats (Figure 3)** :
- **Avant intervention** : E[tput|LDNS] = **3.5 Mbps**
- **Après intervention** : E[tput|LDNS, do(RTT~GDNS)] = **3.0 Mbps**
- **Impact** : **-14% throughput** (perte 0.5 Mbps)

**Interprétation** :
- Redirection vers serveurs proches (LDNS) = **gain 14% performance**
- Quantification causale : distance serveurs = facteur significatif
- Validation : LDNS supérieur car clients plus proches géographiquement

**Intervention 2 : Configuration serveurs** (Section 4.2.2)

**Question** : "Quel serait throughput clients LDNS si serveurs avaient cwinmin distribution de GDNS ?"

**Equation contrefactuelle** (Eq. 11) :
- Intervention : do(cwinmin ∼ f_{cwinmin|GDNS})
- Prédiction : f(tput | LDNS, do(cwinmin ~ GDNS))

**Résultats (Figure 5)** :
- **Avant intervention** : E[tput|LDNS] = **3.5 Mbps**
- **Après intervention** : E[tput|LDNS, do(cwinmin~GDNS)] = **4.6 Mbps**
- **Impact** : **+30% throughput** (gain 1.1 Mbps)

**Interprétation** :
- Configuration TCP serveurs GDNS (cwinmin = 1.2 kB) **meilleure** que LDNS (0.9 kB)
- Impact **plus fort que distance** (30% vs 14%)
- Explication : Initial TCP congestion window = critical pour performance
- Serveurs GDNS = mieux paramétrés (aggressive start)

#### 4. Trade-offs et synthèse

**Facteurs antagonistes** :

| Facteur | LDNS avantage | GDNS avantage | Impact |
|---------|---------------|---------------|--------|
| **Distance serveurs** (RTT) | ✅ 20 ms | ❌ 48 ms | **+14% LDNS** |
| **Config TCP** (cwinmin) | ❌ 0.9 kB | ✅ 1.2 kB | **+30% GDNS** |
| **Throughput réel** | 3.2 Mbps | 3.0 Mbps | +7% LDNS |

**Bilan** :
- LDNS gagne sur **distance** (+14%)
- GDNS gagne sur **configuration** (+30% potentiel)
- Mais configuration GDNS **pas suffisante** pour compenser distance → LDNS **meilleur au final** (+7%)

**Optimal théorique** : LDNS distance + GDNS config = **+44% potential** (3.5 × 1.14 × 1.30 ≈ 5.2 Mbps)

### Conclusion des auteurs

**Contributions** :
1. ✅ **First causal study** DNS service impact on CDN performance
2. ✅ **Quantification séparée** : distance (14%) vs config (30%)
3. ✅ **Bayesian networks** : reveal non-intuitive dependencies
4. ✅ **Counterfactual predictions** : what-if without new experiments
5. ✅ **Practical insights** : LDNS better despite public DNS adoption

**Implications** :

**For users** :
- Local ISP DNS = **better throughput** (+7-14%) si CDN utilise geolocation
- Public DNS (Google) = **suboptimal redirection** (servers farther)
- Trade-off : privacy (GDNS) vs performance (LDNS)

**For CDN operators** :
- Server **location** matters (14% impact)
- Server **configuration** matters **MORE** (30% impact)
- Initial congestion window (cwinmin) = **critical parameter**
- Optimize both geography + TCP tuning

**For DNS providers** :
- ECS (EDNS Client Subnet) = partial solution (2016 adoption limited)
- Need balance : global infrastructure vs local redirection

**Limitations** :
- **Single CDN** : Akamai only (largest but specific)
- **2 days snapshot** : Thursday + Sunday (no longitudinal)
- **Europe only** : single ISP PoP, geographic bias
- **2 DNS services** : LDNS + GDNS (90%+ traffic but excludes OpenDNS, Quad9, etc.)
- **Kernel estimation** : requires data overlap (cannot predict all interventions)
- **Confidentiel data** : packet traces not shareable

---

## Analyse personnelle

### Que garder pour le mémoire

**Concepts clés** :
- **Causal inference** DNS → CDN performance (not just correlation)
- **Geographic redirection** : local DNS = closer servers (20 ms vs 48 ms)
- **TCP configuration** : initial congestion window = critical (30% impact)
- **Counterfactual reasoning** : what-if predictions without experiments
- **Trade-off** distance vs config : antagonistic factors

**Chiffres essentiels** :
- **RTT externe** : LDNS = 20 ms, GDNS = 48 ms (2.4×)
- **Congestion window min** : LDNS = 0.9 kB, GDNS = 1.2 kB (1.33×)
- **Impact distance** : -14% throughput if LDNS users had GDNS RTT
- **Impact config** : +30% throughput if LDNS servers had GDNS cwinmin
- **Throughput réel** : LDNS = 3.2 Mbps, GDNS = 3.0 Mbps (+7%)
- **~7,000 connections** analysées, 19 paramètres

**Méthodes applicables** :
- Bayesian networks pour modèles causaux (PC algorithm)
- Gaussian copulae pour densités multidimensionnelles
- Counterfactual predictions via do-calculus
- Passive traces + active feature extraction (Tstat)
- Geographic AS mapping (destination servers)

**Limites pour nous** :
- Étude 2016 (10 ans) → évolution ECS, public DNS adoption ?
- 1 CDN (Akamai) → généralisation autres CDNs ?
- Pas de mesures actives distribuées (1 PoP passive)
- Focus TCP/throughput (pas availability, DNS resolution time)

### Critique personnelle

**Forces** :
- ✅ **Novel causal approach** : dépasse corrélation, permet interventions
- ✅ **Quantification séparée** : 14% distance, 30% config (insights clairs)
- ✅ **Real traffic** : ~7K connections production (not synthetic)
- ✅ **Rigorous methodology** : Bayesian nets, copulae, kernel tests
- ✅ **Practical insights** : actionable pour CDN operators
- ✅ **Honest limitations** : authors acknowledge data constraints

**Faiblesses** :
- ⚠️ **Limited scope** : 1 CDN, 1 ISP, 2 days, Europe only
- ⚠️ **No temporal analysis** : snapshot, pas évolution
- ⚠️ **ECS discussion light** : mentions client subnet but no empirical test
- ⚠️ **Binary DNS choice** : LDNS vs GDNS (excludes OpenDNS, Quad9, etc.)
- ⚠️ **Kernel estimation limits** : cannot predict all interventions (data overlap required)
- ⚠️ **TCP focus** : ignore UDP, DNS query time, cache effects
- ⚠️ **Privacy prevent deeper analysis** : IP obfuscation → cannot analyze client locations

**Lien avec autres articles** :

- **Calder 2015 (Anycast CDN)** :
  - Calder : anycast routing = 20% clients suboptimal (BGP)
  - Hours : DNS choice = 7% impact final, 14% distance seule
  - Complémentarité : routing (BGP) + redirection (DNS) = double impact

- **Xu 2023 (Centralization)** :
  - Xu : DNS infrastructure centralisée (oligopole)
  - Hours : choix DNS impact redirection géographique
  - Paradoxe : centralization backend vs geographic redirection frontend

- **Koch 2021 (Anycast context)** :
  - Koch : context matters (Microsoft CDN = extensive peering)
  - Hours : CDN server config matters (30% > 14% distance)
  - Cohérence : infrastructure complexity beyond simple distance

- **Nosyk 2024 (RIPE Atlas)** :
  - Nosyk : RIPE Atlas = 12.9K vantage points distribués
  - Hours : 1 PoP passif (limited geography)
  - Notre mémoire : RIPE Atlas peut mesurer variations DNS/CDN globalement

**Questions ouvertes** :
1. **Évolution 2016-2024** : ECS adoption impact ? Public DNS gains ?
2. **Autres CDNs** : Cloudflare, Fastly, AWS CloudFront = mêmes patterns ?
3. **IPv6** : Redirection DNS différente IPv6 vs IPv4 ?
4. **Temporal dynamics** : Variations heure/jour/saison ?
5. **Client diversity** : Mobile vs desktop, residential vs datacenter ?
6. **Optimal config** : Quelle valeur cwinmin optimale selon RTT ?

### Citations importantes

> "We use a causal model to capture the way the different parameters of the system impact the throughput, which allows us to evaluate the impact of choosing one DNS service instead of another without requiring the modiﬁcation of the DNS services themselves." (Abstract)

> "Our data show that most of the time, clients using the DNS of their ISP are redirected to an Akamai server located in the same AS. On the other hand, the clients using the Google DNS service are often redirected to servers located outside the client AS and even, in some cases, to a server outside of Europe." (Section 4.1)

> "The expected throughput for clients using the local DNS service prior to intervention is 3.5 Mbps and 3.0 Mbps after intervention (14% decrease). This result quantiﬁes the gain in performance that the redirection to closer CDN servers, provided by the use of the local DNS service, represents." (Section 4.2.1)

> "The expected throughput for LDNS service users after the intervention is 4.6 Mbps (compared to 3.5 Mbps prior to intervention), which represents an increase of more than 30%. This increase is due to the fact that the servers GDNS service users are redirected to use higher values for their minimum congestion window." (Section 4.2.2)

**Sur méthode causale** :
> "This reasoning used to answer what-if questions is referred to as counterfactual thinking. By asking 'What would be the performance of a user of the LDNS service if one of her parameter was to behave as it does when the GDNS is used, knowing that the use of the LDNS and the GDNS are exclusive ?', we can estimate the impact of the choice of a DNS service on user performance." (Section 4.2)

**Sur limites** :
> "The prediction formulated in Eq. (7) is only possible since the range of the external RTT values observed for GDNS users represents a subset of the range of values observed for the LDNS users." (Section 4.2.1)

---

## Utilisation dans le mémoire

**Sections concernées** :
- **Section 2.6 (CDN, DNS resolvers)** : Impact choix DNS sur redirection géographique
- **Section 7 (Discussion)** : Geographic diversity RIPE Atlas vs single vantage point

**Points à développer** :

**État de l'art** :
- DNS local ISP ≠ DNS public Google : redirection géographique différente
- Impact **double** : distance serveurs (14%) + configuration TCP (30%)
- Choix DNS = trade-off privacy (public) vs performance (local)
- ECS (EDNS Client Subnet) = partial solution (adoption 2016 limitée)

**Notre contribution** :
- Hours 2016 : 1 PoP passif Europe, 2 jours
- Notre approche : RIPE Atlas 12.9K sondes, 178 pays, longitudinal
- Capacité mesurer variations DNS/CDN **globalement** (geographic diversity)
- Identifier si patterns Hours (LDNS meilleur) généralisent mondialement

**Discussion** :
- Hours montre **why** geographic diversity matters (14% impact distance)
- 1 vantage point (Hours) = cannot observe geographic variations DNS redirection
- RIPE Atlas (distributed) = révèle variations redirection selon probe location
- Complémentarité : causal study (Hours) + distributed measurements (nous)

**Méthodologie** :
- Inspiration causal thinking : séparer facteurs (distance vs config)
- Mais RIPE Atlas = active measurements (pas passive traces)
- Possible : mesurer RTT towards resolvers, analyse responses géographiques

**Limitations** :
- RIPE Atlas = probes fixes (not all client populations)
- Mais 178 countries → better coverage than single ISP PoP

---

**Tags** : #dns #cdn #performance #causality #bayesian-networks #akamai #google-dns #local-dns #throughput #tcp #congestion-window #geographic-redirection #counterfactuals

**Statut** : [X] Lu (PDF via MD) / [X] Fiché / [ ] Intégré mémoire

**Date fiche** : 21 mars 2026
