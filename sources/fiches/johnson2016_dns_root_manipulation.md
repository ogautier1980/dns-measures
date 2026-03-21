# Fiche de lecture - Detecting DNS Root Manipulation

**Référence bibliographique** :
Jones, B., Feamster, N., Paxson, V., Weaver, N., & Allman, M. (2016). *Detecting DNS Root Manipulation*. International Computer Science Institute (ICIR). Princeton University & UC Berkeley.

**Thème** :
Détection de serveurs DNS root non-autorisés via mesures RIPE Atlas et analyse BGP

**Intérêt pour le mémoire** :
Démontre l'utilisation RIPE Atlas (~8,000 sondes, 2014) pour détecter manipulation infrastructure DNS critique. Combine mesures endpoint (latence, HOSTNAME.BIND) avec analyse BGP. Illustre menace contrôle DNS et techniques détection via mesures distribuées.

---

## Contexte de lecture

**Date de lecture** : 21 mars 2026
**Section du mémoire** :
- Section 2.5 (RIPE Atlas - use case sécurité)
- Section 2.6 (Sécurité DNS - manipulation root servers)

---

## Contenu de l'article

### Objectif(s) / Question(s) de recherche

**Problème** : Entités opérant **serveurs DNS root non-autorisés** peuvent :
- Contrôler complètement namespace Internet pour systèmes sous leur influence
- Bloquer accès sites (disruption name resolution)
- Interposer man-in-the-middle (redirection proxies)

**Menace réelle** : Pays (Chine, Pakistan, Turquie) manipulent déjà DNS pour censure, parfois impact international.

**Question** : Comment détecter serveurs root non-autorisés à grande échelle ?

**Focus** : Attaquants manipulant **tous les 13 DNS root servers** (contrôle total), pas subset.

### Cadre global d'explication

**DNS root infrastructure** :
- 13 adresses serveurs (a-m.root-servers.net)
- Run par 12 organisations
- 12/13 utilisent **anycast** (2-150 replicas par serveur)
- **B root (b.root-servers.net)** = seul **non-anycast** (Los Angeles, USA)
  → Utilisé comme baseline détection

**Threat model - 3 méthodes manipulation** (Figure 1) :
1. **In-path DNS proxy** : middlebox intercepte trafic DNS root
   - Transparent proxy pour cache + contrôle
   - Facile (UDP = connectionless, peu d'état)
2. **DNS injection** : attaquant observe requêtes + injecte réponses avant légitimes
3. **Route hijack** : compromission routing IP → redirige trafic vers fake root replica
   - Analogique à anycast légitime

**Assumption** : Attaquant manipule **13 serveurs** simultanément pour contrôle total + ne sélectionne pas quelles queries manipuler.

### Méthodologie

- **Type d'étude** : Mesures actives + analyse BGP
- **Outils utilisés** :
  - **RIPE Atlas** : ~8,000 sondes, 2,755 AS, 189 pays (juillet 2014)
  - **BGP monitoring** : RouteViews + RIPE RIS
- **Échelle** :
  - 6,546 sondes Atlas avec pings (~2,500 pings/sonde)
  - 6,135 sondes avec HOSTNAME.BIND queries
  - 5,929 sondes fournissant les deux mesures
- **Période** : 6-13 juillet 2014 (1 semaine)
- **Protocole de mesure** :

**Table 1 - Sources de données** :

| Measurement | Dates | Détecte |
|-------------|-------|---------|
| Ping (ICMP) | 6-13 juillet 2014 | Root mirrors |
| HOSTNAME.BIND (DNS) | 22 juillet 2014 | Proxies + mirrors |
| Traceroutes (UDP) | 6 juillet 2014 | Proxies + mirrors |
| RIPE RIS (BGP) | 6-13 juillet 2014 | Root mirrors |
| RouteViews (BGP) | 7 juillet 2014 | Root mirrors |

**Méthodes détection** :

**1. Anomalous Response-Time Latency** :
- Atlas = pings ICMP vers roots chaque 240s (4 minutes)
- Compare RTT ping vs RTT HOSTNAME.BIND query
- Proxy → DNS response beaucoup plus rapide (local vs Los Angeles)
- Latency difference = évidente, difficile masquer
- Validation : pings minimum < speed-of-light propagation delay

**2. Anomalous Server Identity** :

a) **HOSTNAME.BIND Queries** :
- DNS query spéciale demande serveur s'identifier
- B root légitime → pattern `bx` (x=0-9)
- Invalid/null response → suspect
- Proxy difficile à fake (custom per root, non-default software)

b) **Traceroutes** :
- UDP traceroutes vers B + L roots chaque 1800s (30 min)
- Check penultimate hop ASN avant B root
- Compare paths B vs L roots
- Assumption : attaquant difficilement falsifie tous hops

c) **BGP Routing Tables** :
- Analyse RouteViews + RIPE RIS
- Check B root prefix dans RIBs
- Detect AS path modifications ou more-specific prefix announcements
- Détecte route leaks (ex: Pakistan YouTube 2008)

### Résultats principaux

#### 1. DNS Proxies détectés

**HOSTNAME.BIND analysis** :
- **11 réponses** non-conformes au pattern `bx`
- 1 = DNS mirror Chine (voir section 2)
- **10 = DNS proxies**
- 1 seul ISP avec multiple probes (3/4 correctes → config utilisateur, pas ISP)
- 9 autres = décision intentionnelle ISP (nom ISP dans réponse)

**Exemple Wananchi (Kenya)** :
- Réponse : `dns3.wnanchi.com` en 14 ms
- vs ping légitime B root : 318 ms
- **Amélioration performance** (23× plus rapide)

**Validation latency** :
- Geolocate probes, filter Americas (B root = Los Angeles)
- 1,388 probes (22.6%) = location cohérente
- 106 probes (1.7%) = location inconsistente (exclus)
- Technique détecte **mêmes 10 proxies** que HOSTNAME.BIND
- **Confidence élevée** (2 méthodes indépendantes convergent)

**Figure 2** : Afrique representative sample
- Difference (ping - HOSTNAME.BIND) times
- DNS proxy Kenya = outlier clair (DNS response << ping)
- Autres pays : DNS ≈ ping (légitime)

**Comparaison Netalyzr** :
- Weaver et al. : 1.4% clients derrière hidden proxies
- Cette étude : 0.16% (~1/10 taux précédent)
- Possible évolution 2014 vs études antérieures

#### 2. Rogue DNS Root Mirror

**China Education and Research Network (CERNET)** :
- **1 probe Chine** = unauthorized root replica
- Ping B root : 1.2 ms (impossible depuis Los Angeles!)
- HOSTNAME.BIND : réponse invalide, 16 ms
- Geolocation : confirmed Chine (Atlas + MaxMind)
- Traceroute : tous hops = même ASN
- Network issues : 8/2519 pings (0.11%) > 100 ms (Figure 4)
- **Consistency** : 2,519 pings impossibly low, consistently

**Figure 3** : Asia probes B vs L roots
- L root (150 anycast) vs B root (unicast LA)
- DNS mirror = clear outlier (très faible RTT B root)

**Validation** :
- Atlas probe peut contacter directement authoritative DNS sous contrôle auteurs
- → Pas derrière proxy, vraiment root mirror
- Consistance mesures (2,519 pings) → haute confiance

**Outliers analysis** :
- 4 outliers initiaux
- 1 = DNS mirror Chine (confirmé)
- 3 = measurement errors :
  - 1 probe New York geolocated Switzerland (erreur geolocation)
  - 2 probes ICMP error messages mal interprétés (TTL 255 = first hop ICMP error, pas echo reply)

#### 3. Traceroutes analysis

**Penultimate hop verification** (4,333 traceroutes, 1,948 probes) :
- AS 226 (Los Nettos) : 1,647 probes (3,488 tr) ✅ Légitime (BGP neighbor ISI)
- AS 2153/2152 (Cal State Univ) : 295 probes (814 tr) ✅ Légitime (USC location)
- AS 4 (ISI) : 2 probes (22 tr) ✅ Légitime (B root admins)
- AS 8121 (Layer 42) : 1 probe (5 tr) ✅ Légitime (different AS)
- AS 34168 (Rostelecom) : 1 probe (2 tr) ✅ Légitime (230 ms latency)
- AS 2914 (NTT Comm) : 1 probe (1 tr) ✅ Légitime (different AS)

→ **Aucun root mirror détecté via traceroutes**

**B vs L paths comparison** (4,342 pairs, 1,292 probes) :
- Hypothèse : attaquant redirige multiples roots vers 1 instance (éviter duplication)
- Matching hops fraction : max 0.85 (12/14 hops)
- Si manipulation → expect 100% match
- Probes behind DNS proxies : max 0.8 matching (12/15 hops)
- **Conclusion : pas de root manipulation détectée via traceroutes**

#### 4. BGP analysis

**RouteViews + RIPE RIS** :
- Analyse AS paths + prefix announcements pour B root
- **Aucune anomalie détectée**
- Pas de hijack, pas de more-specific prefix, pas de AS path injection

### Conclusion des auteurs

**Contributions** :
1. ✅ **Techniques détection** manipulation DNS root (latency + identity)
2. ✅ **Validation empirique** sur ~8,000 sondes RIPE Atlas
3. ✅ **Discoveries** : 10 DNS proxies + 1 unauthorized root mirror (Chine)
4. ✅ **Confidence** : 2 méthodes indépendantes (latency + HOSTNAME.BIND) convergent

**Implications** :
- DNS root manipulation = **rare mais réelle** (2014)
- Proxies souvent légitimes (performance ISP), pas nécessairement malveillants
- Root mirror Chine = unauthorized, contrôle potentiel namespace
- Techniques détectent **most if not all** mirrors depuis vantage points
- Coverage limité : pas tous AS, potentiellement sous-estime proxies

**Limitations** :
- Attaquant sophistiqué peut masquer latency (transformer replies au lieu répondre)
- Coverage géographique = dépend distribution sondes Atlas
- BGP analysis = only detects leaks to public Internet

---

## Analyse personnelle

### Que garder pour le mémoire

**Concepts clés** :
- **DNS root manipulation** = menace réelle infrastructure critique
- **Multi-method validation** : latency + identity + BGP → robustesse
- **Side-channel detection** : latency anomalies reveal hidden infrastructure
- **RIPE Atlas versatility** : sécurité + performance + infrastructure analysis
- **Geographic distribution** : 189 pays = coverage globale, mais biais

**Méthodes applicables** :
- Comparaison RTT ICMP vs DNS queries (detect proxies)
- HOSTNAME.BIND fingerprinting
- Traceroute AS path validation
- BGP monitoring pour route hijacks
- Geographic filtering (exclude Americas pour B root LA)
- Multi-source geolocation (Atlas + MaxMind)

**Chiffres importants** :
- **~8,000 sondes**, 2,755 AS, 189 pays (2014)
- **10 DNS proxies** détectés (0.16% sondes)
- **1 unauthorized root mirror** (Chine)
- **1.2 ms ping** B root depuis Chine (vs ~300 ms attendu)
- **2,519 pings** consistently low (high confidence mirror)

**Limites pour nous** :
- Étude 2014 (10 ans) → évolution depuis ?
- Focus B root (non-anycast) → méthode moins applicable autres roots
- Assume attaquant manipule tous 13 roots (restrictif)
- Pas de quantification impact utilisateurs (combien affectés ?)

### Critique personnelle

**Forces** :
- ✅ **Multi-method convergence** : latency + HOSTNAME.BIND détectent mêmes proxies
- ✅ **Large scale** : 8,000 sondes, 189 pays (2014 = déjà impressive)
- ✅ **Real threat** : China mirror = unauthorized, pas juste theoretical
- ✅ **Practical validation** : traceroutes + BGP confirm findings
- ✅ **Clear methodology** : reproducible, well-documented

**Faiblesses** :
- ⚠️ **Old study** (2014) → RIPE Atlas now 12.9K sondes (2024)
- ⚠️ **Limited scope** : B root uniquement (non-anycast)
- ⚠️ **No temporal analysis** : snapshot, pas évolution
- ⚠️ **Geographic bias** : dépend distribution sondes
- ⚠️ **Underestimate** : authors acknowledge may miss proxies
- ⚠️ **No impact quantification** : combien users affected ?

**Lien avec autres articles** :

- **Nosyk 2024 (RIPE Atlas DITL)** :
  - 2014 : ~8,000 sondes
  - 2024 : 12,892 sondes (+60%)
  - Coverage improved mais biais géographique persiste

- **Holterbach 2015 (Interference)** :
  - Concurrent measurements → timing interference
  - Jones 2014 : pings + DNS queries OK (simples, peu CPU)
  - Validation : mesures DNS robustes à interference

- **Boswell 2024 (Internal Names)** :
  - Jones : external (root servers)
  - Boswell : internal (home gateways)
  - Complémentarité : threats externes + internes

**Questions ouvertes** :
1. **Évolution 2014-2024** : Plus/moins proxies/mirrors maintenant ?
2. **Anycast roots** : Techniques applicables L root (150 replicas) ?
3. **IPv6** : Manipulation différente IPv6 vs IPv4 ?
4. **Attaque sophistiquée** : Latency masking possible ?
5. **Motivations** : Proxies = performance ou malveillant ?

### Citations importantes

> "Entities operating unauthorized root servers can completely control the entire Internet name space for any systems within their sphere, including blocking access to sites by disrupting their name resolution, or arbitrarily interposing on communication by redirecting through man-in-the-middle proxies." (Introduction)

> "Countries such as China, Pakistan, and Turkey already manipulate DNS to impose censorship, sometimes incidentally affecting DNS resolution for other countries." (Introduction)

> "We found that overlapping measurements do interfere with each other in at least two ways." (Section 3)

**Sur détection proxies** :
> "Using two independent techniques, we identified eleven HOSTNAME.BIND responses that did not match the expected bx pattern [...] ten DNS proxies. The fact that two independent techniques detected the same ten DNS proxies increases our confidence in the result." (Section 4.1)

**Sur China mirror** :
> "We determined that the fourth outlier was an unauthorized root mirror in the China Education and Research Network. The Atlas probe could ping B root in 1.2 ms and a HOSTNAME.BIND query produced an invalid response with a response time of 16 ms." (Section 4.2)

**Sur traceroutes validation** :
> "These methods revealed no evidence of root manipulation. The closest traceroute pair had a matching hop fraction of 0.85 (12/14 hops matched). If manipulation were taking place, we would have expected the traceroutes to match exactly." (Section 4.3)

---

## Utilisation dans le mémoire

**Sections concernées** :
- **Section 2.5 (RIPE Atlas)** : Use case sécurité, détection infrastructure compromise
- **Section 2.6 (Sécurité DNS)** : Manipulation root servers, censure, proxies

**Points à développer** :

**État de l'art** :
- RIPE Atlas = outil sécurité (pas juste performance/monitoring)
- Multi-method validation = robustesse (latency + identity + BGP)
- DNS root manipulation = rare (10 proxies, 1 mirror / 8,000 sondes) mais réel
- Geographic distribution = clé détection (B root LA → filter Americas)

**Méthodologie** :
- Side-channel detection applicable (anomalies reveal infrastructure)
- Latency baseline = geographic distance
- Multiple data sources (Atlas + BGP) = cross-validation

**Discussion** :
- Coverage depends on probe distribution (our study aussi)
- Threat model : assume manipulation visible (sophisticated attacker peut masquer)
- Trade-off : coverage vs attacker capabilities

**Références croisées** :
- Nosyk 2024 : Evolution RIPE Atlas 2014→2024
- Boswell 2024 : Client-side manipulation (internal names)
- Holterbach 2015 : Platform limitations (interference)

---

**Tags** : #dns-root #security #manipulation #ripe-atlas #censorship #proxies #mirrors #china #detection #latency #bgp

**Statut** : [X] Lu (PDF via MD) / [X] Fiché / [ ] Intégré mémoire

**Date fiche** : 21 mars 2026
