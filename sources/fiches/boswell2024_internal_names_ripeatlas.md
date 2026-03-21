# Fiche de lecture - Internal Domain Names Survey via RIPE Atlas

**Référence bibliographique** :
Boswell, E., & Perkins, C. (2024). *RIPEn at Home – Surveying Internal Domain Names using RIPE Atlas*. TMA 2024 - Network Traffic Measurement and Analysis Conference. 978-3-903176-64-5 ©2024 IFIP

**Thème** :
Mesures actives RIPE Atlas pour détecter noms de domaines internes dans réseaux domestiques

**Intérêt pour le mémoire** :
Méthodologie originale d'utilisation RIPE Atlas pour mesures client-side (pas server-side). Démontre capacité plateforme à détecter configurations locales DNS. Illustre risques sécurité liés aux name collisions et variations géographiques (FRITZ!Box dominant en Europe).

---

## Contexte de lecture

**Date de lecture** : 21 mars 2026
**Section du mémoire** :
- Section 2.5 (RIPE Atlas - méthodologie mesures client-side)
- Section 2.6 (Sécurité DNS - name collisions)

---

## Contenu de l'article

### Objectif(s) / Question(s) de recherche

**Problème** : Noms de domaines internes (resolus localement, pas par DNS global) créent risque **name collision** si :
1. TLD interne est délégué dans DNS global (ex: `.box` délégué août 2023)
2. Queries accidentellement envoyées à résolveur public
3. Attaquant enregistre le domaine → spoof gateway (vol credentials, malware)

**Cas réel - FRITZ!Box** :
- Gateway populaire Allemagne utilise `fritz.box` comme nom interne
- `.box` ajouté DNS root août 2023, annoncé janvier 2024
- AVM n'a pas enregistré `fritz.box` → squatters l'ont récupéré
- Risque sécurité : spoof page config gateway

**Question de recherche** :
1. Quels noms internes sont utilisés par gateways domestiques ?
2. Lesquels sont vulnérables à name collision ?
3. Combien de probes RIPE Atlas utilisent des noms à risque ?

**Originalité** :
- Études précédentes = passive DNS (logs root servers, resolvers)
- Cette étude = **active DNS via RIPE Atlas** (client-side measurements)
- Avantage : capture noms internes qui n'apparaissent pas dans logs (résolus localement)

### Cadre global d'explication

**Name collisions** :
- Nom interne existe aussi dans DNS global
- Résolution accidentelle via DNS global au lieu de local resolver
- Si réponses différentes et entités différentes → spoof local resource

**Contexte ICANN** :
- Introduction nouveaux gTLDs depuis octobre 2013 (1,241 en novembre 2023)
- Risque : TLDs internes couramment utilisés soient délégués
- Exemple : `.home` utilisé si fréquemment qu'ICANN a **indéfiniment repoussé** sa délégation

**RIPE Atlas pour home networks** :
- ~12,000 sondes, beaucoup dans réseaux domestiques
- Vantage points client-side idéaux
- Permettent mesures actives depuis perspective utilisateurs

### Méthodologie

- **Type d'étude** : Mesures actives DNS, fingerprinting gateways
- **Outils utilisés** :
  - RIPE Atlas measurement API
  - Traceroutes IPv4
  - DNS queries (CHAOS TXT, reverse DNS, A records)
  - Gateway profile fingerprinting
- **Échelle** :
  - **Toutes sondes IPv4 disponibles** (début 2024)
  - **~8,500 sondes testées** (chiffre implicite: 7441+6045 détections)
  - **4,305 sondes** utilisent noms internes (50.86% des testées)
- **Protocole de mesure** (Figure 1) :

**Étape 1 : Détecter adresse gateway**
Deux méthodes parallèles :
- a) **Traceroute** : dernière adresse privée dans traceroute IPv4 = gateway (7,441 probes)
- b) **Local resolver** : adresse DNS resolver = gateway si privée non-loopback (6,045 probes)

**Étape 2 : BIND queries**
- Queries CHAOS TXT pour `version.bind` et `hostname.bind`
- Fingerprinting gateway via response codes (NXDOMAIN, SERVFAIL, etc.)
- Gateway profile = mêmes réponses + même adresse locale → même modèle gateway

**Étape 3 : rDNS queries**
- Reverse DNS query pour adresse gateway
- Si réponse = nom interne
- Traceroute gateways : 2,573 réponses / 7,441 (35%)
- Resolver gateways : 3,872 réponses / 6,045 (64%)

**Étape 4 : Gateway profile fingerprinting**
- Si probe sans réponse rDNS : utiliser noms d'autres probes avec même gateway profile
- Query A records pour ces noms
- Si réponse = adresse locale différente du DNS global → nom interne
- +102 probes détectés via cette méthode

**Limitation** : multicast DNS (mDNS) non détectable (RIPE Atlas ne supporte pas mDNS queries)

### Résultats principaux

#### 1. Noms internes découverts

**Nombres clés** :
- **3,092 noms internes uniques** découverts
- **4,305 probes** (50.86% des testées) utilisent noms internes
- **1,146 noms** (37.06%) n'apparaissent qu'une seule fois (uniques au réseau)

**Top 10 full domain names** :
1. fritz.box (dominant)
2. myfritz.box
3. www.fritz.box
4. www.myfritz.box
5. wpad.fritz.box
6. wpad.box
7. fritz.nas
8. fritz-nas.fritz.box
9. www.fritz.nas
10. fritz-nas.box

→ **FRITZ!Box domine** (popularité Europe + multiples noms par rDNS query)

**Top 10 second+top-level domains** :
- fritz.box, myfritz.box, wpad.box (FRITZ!Box)
- fritz.nas, fritz-nas.box (FRITZ!Box NAS)
- pi.hole (PiHole ad blocker)
- router.lan, OpenWrt.lan (routeurs génériques)
- unifi.localdomain (Ubiquiti UniFi)
- livebox.home (Orange Livebox France)

**Top 5 TLDs** :
1. `.box` (dominant, ~700 probes)
2. `.lan` (~400 probes)
3. `.nas` (~200 probes)
4. `.hole` (~150 probes)
5. `.home` (~100 probes)

Autres TLDs publics utilisés : `.com`, `.net`, `.org` (utilisateurs techniques RIPE Atlas)

#### 2. Risque collision actuel

**Noms avec TLD public** : 1,766 / 3,092 (57.12%)

**Vulnérables actuellement** :
- **66 noms** (3.74% des noms TLD public, **2.13% de tous les noms**)
- Subdomain public suffix non-résolvant → enregistrable par attaquant
- Risque immédiat de collision/spoof

**Non-vulnérables actuellement** : 1,687 (95.53% noms TLD public)
- Public suffix subdomain résout → domaine enregistré (propriétaire légitime ?)

**Non-évalués** : 13 noms (couldn't assess)

#### 3. Risque collision futur

**Noms avec TLD non-délégué** : 1,326 / 3,092 (42.88%)

**Vulnérables si TLD délégué** :
- **1,067 noms** (**34.51%** de tous les noms)
- Si ICANN délègue leur TLD → collision potentielle

**TLDs à risque retardé/réservé** :
- `.home` : 96 noms, **délégation indéfiniment reportée** par ICANN (collision risk trop élevé)
- `.internal` : 26 noms, **proposé réservation** pour usage interne (RFC en cours ?)
- `.local` : usage mDNS (special-use name)
- `home.arpa` : 24 probes (special-use alternative à `.home`, peu adopté)

### Conclusion des auteurs

**Contributions** :
1. ✅ **Première survey active (vs passive)** noms internes via RIPE Atlas
2. ✅ **3,092 noms découverts** sur 4,305 probes (50.86%)
3. ✅ **Quantification risque collision** :
   - 2.13% vulnérables actuellement
   - 34.51% vulnérables si TLD délégué
4. ✅ **Update post-gTLD** (10 ans après introduction nouveaux gTLDs)

**Implications sécurité** :
- Name collisions = risque réel (cas FRITZ!Box 2024)
- Delegation TLDs nécessite analyse risque collision
- Special-use TLDs peu adoptés (home.arpa = 24 probes seulement)

**Limitations reconnues** :
- ⚠️ mDNS non détectable (limitation RIPE Atlas)
- ⚠️ Biais population RIPE Atlas (utilisateurs techniques)
- ⚠️ Detection home gateways = heuristique (non fine-grained)
- ⚠️ Pas de vérification que réponse vient effectivement du gateway (source spoofing possible)

---

## Analyse personnelle

### Que garder pour le mémoire

**Concepts clés à réutiliser** :
- **Active vs passive measurements** : active capture noms résolus localement (invisibles dans logs)
- **Client-side measurements** : RIPE Atlas mesure depuis perspective utilisateur final
- **Gateway profile fingerprinting** : inférer modèle équipement via DNS responses patterns
- **Name collisions** : risque sécurité réel, pas juste théorique (FRITZ!Box 2024)
- **Geographic bias** : FRITZ!Box domine car populaire Europe (où RIPE Atlas concentré)

**Méthodes applicables** :
- Utilisation traceroute + DNS queries pour inférer topologie locale
- CHAOS TXT queries pour fingerprinting équipements
- Reverse DNS pour découvrir noms locaux
- Gateway profile clustering pour extrapolation
- Combinaison méthodes multiples (traceroute + resolver) pour robustesse

**Chiffres/statistiques importantes** :
- **50.86%** probes RIPE Atlas utilisent noms internes
- **3,092 noms** uniques découverts
- **37.06%** noms uniques (1× occurrence) → diversity
- **2.13%** vulnérables actuellement (collision immédiate)
- **34.51%** vulnérables si TLD délégué (collision future)
- **FRITZ!Box** = 10/10 top full domain names (dominance Europe)
- **Special-use names** peu adoptés (24 probes home.arpa vs 96 .home)

**Limites identifiées (pertinentes pour nous)** :
- ⚠️ **Geographic bias** : résultats biaisés vers Europe (FRITZ!Box)
- ⚠️ **RIPE Atlas bias** : utilisateurs techniques ≠ population générale
- ⚠️ **Detection heuristics** : assumptions (last private address = gateway) imparfaites
- ⚠️ **Incomplete coverage** : mDNS non détectable, probes IPv6-only non testées

### Critique personnelle

**Forces de l'article** :
- ✅ **Méthodologie originale** : première survey active (vs passive prior studies)
- ✅ **RIPE Atlas usage créatif** : client-side measurements (pas juste server-side)
- ✅ **Dual detection** : traceroute + resolver (robustesse)
- ✅ **Fingerprinting intelligent** : gateway profile pour extrapolation
- ✅ **Timing pertinent** : post-FRITZ!Box incident (2024) = validation risque
- ✅ **Quantification risque** : 2.13% actuel + 34.51% futur (chiffres clairs)
- ✅ **Update longitud** : 10 ans post-gTLD introduction

**Faiblesses identifiées** :
- ⚠️ **Short paper** (TMA poster) → manque détails méthodologiques
- ⚠️ **Geographic analysis manquant** : pas de breakdown par pays/région (pertinent pour notre mémoire!)
- ⚠️ **Temporal aspect absent** : snapshot unique, pas évolution temporelle
- ⚠️ **Validation limitée** : pas de vérification manuelle sample
- ⚠️ **Root cause analysis manquant** : pourquoi certain gateways répondent rDNS, d'autres non ?
- ⚠️ **Security impact non quantifié** : combien d'utilisateurs réellement impactés par collisions ?

**Lien avec autres articles lus** :

- **Nosyk 2024 (RIPE Atlas DITL)** :
  - Nosyk : 12,892 sondes février 2024
  - Boswell : ~8,500 testées (65%)
  - Nosyk : biais Europe/NA (28% DE+US)
  - Boswell : FRITZ!Box domine (populaire Allemagne) → confirme biais géographique

- **Holterbach 2015 (Interference)** :
  - Holterbach : timing/scheduling interference
  - Boswell : mesures DNS simples (peu impact CPU?)
  - Validation : méthodologie RIPE Atlas robuste pour queries DNS simples

- **van Rijswijk-Deij 2016 (OpenINTEL)** :
  - OpenINTEL : server-side, mesures autoritatives
  - Boswell : client-side, mesures résolveurs locaux
  - Complémentarité : server view (OpenINTEL) vs client view (RIPE)

- **Notre mémoire** :
  - Diversité géographique DNS : Boswell montre variations régionales (FRITZ!Box EU)
  - Client-side measurements : méthodologie applicable à nos queries
  - Geographic bias : besoin considérer distribution sondes RIPE Atlas

**Questions ouvertes** :
1. **Breakdown géographique** : Quels pays utilisent quels noms internes ?
2. **Temporal evolution** : Usage noms internes évolue comment (pre/post gTLD delegation) ?
3. **ISP influence** : Box providers (Orange Livebox, etc.) influencent noms locaux ?
4. **IPv6 impact** : Probes IPv6-only ont-elles patterns différents ?
5. **Security incidents** : Combien collisions réelles (pas juste potentielles) ?
6. **Mitigation** : Effectiveness special-use TLDs pour réduire risque ?

### Citations importantes

> "Internal domain names are domain names that are resolved locally and not by the global DNS. Name collisions occur if an internal name is resolved in the global DNS, e.g. if queries are accidentally sent to a public resolver. This can lead to security issues." (Abstract)

> "While previous studies of name collisions used passive measurement data, we use active measurements on RIPE Atlas to survey the use of internal names in home networks." (Abstract)

> "We find 3092 internal names used by 4305 RIPE Atlas probes. Of these, 2.13% are currently vulnerable to collision (e.g. unregistered subdomains of existing TLDs), and 34.51% use an undelegated TLD and could be vulnerable if it is delegated." (Abstract)

**Sur FRITZ!Box incident** :
> "AVM did not appear to register fritz.box and other related names, and for several weeks in January and February 2024, several such names were owned by likely domain speculators. This is a security risk, as queries for fritz.box could accidentally be sent to the public DNS, e.g. when using a public resolver. The public fritz.box domain could spoof the home gateway, e.g. to steal login credentials, misguide users to install malicious software, or otherwise interfere with the home network." (p. 1)

**Sur active vs passive** :
> "We perform active client-side measurements, as they can capture internal names that don't frequently appear in root server logs because the queries are usually answered by the local resolver." (p. 1)

**Sur geographic bias** :
> "All top 10 full domain names appear to be related to the FRITZ!Box. This is likely due to its popularity in Europe (where many RIPE Atlas probes are located), and because a single rDNS query to a FRITZ!Box often returns multiple names." (p. 2)

---

## Utilisation dans le mémoire

**Sections concernées** :
- **Section 2.5 (RIPE Atlas)** : Méthodologie client-side measurements, capacités plateforme
- **Section 2.6 (Sécurité DNS)** : Name collisions, risques réels (FRITZ!Box case study)
- **Section 4 (Méthodologie)** : Inspiration traceroute + DNS queries, fingerprinting

**Points à développer** :

**Dans état de l'art (2.5)** :
- RIPE Atlas = versatile : server-side ET client-side measurements
- Client-side capture phénomènes invisibles à server-side (noms internes)
- Geographic bias plateforme → impact résultats (FRITZ!Box dominance EU)

**Dans état de l'art (2.6)** :
- Name collisions = risque sécurité réel, pas théorique
- FRITZ!Box 2024 : proof of concept attack réel (domain squatting)
- Délégation TLDs nécessite analyse collision risk (ICANN delays .home)

**Pour notre méthodologie** :
- Active measurements révèlent patterns invisibles à passive
- Geographic distribution sondes RIPE → bias résultats (considérer dans analyses)
- Fingerprinting techniques applicables (patterns DNS responses)

**Pour discussion** :
- **Complémentarité approches** :
  - OpenINTEL : server-side, autoritatives, 1 point
  - RIPE Atlas : client-side, resolvers, 12K points
  - Notre focus : variations géographiques réponses autoritatives
- **Geographic bias** :
  - Boswell : FRITZ!Box domine (Europe bias)
  - Nous : besoin équilibrer sélection sondes par région ?
- **Limites active measurements** :
  - Depend on probe distribution
  - Platform capabilities (ex: no mDNS)
  - Ethical considerations (passive = moins intrusif)

**Références croisées** :
- Nosyk 2024 : Contexte RIPE Atlas 2024
- Holterbach 2015 : Limitations plateforme
- OpenINTEL : Approche complémentaire server-side

---

**Tags** : #ripe-atlas #internal-names #name-collisions #security #client-side #home-networks #fritbox #tld-delegation #active-measurement

**Statut** : [X] Lu (PDF via MD) / [X] Fiché / [ ] Intégré mémoire

**Date fiche** : 21 mars 2026
