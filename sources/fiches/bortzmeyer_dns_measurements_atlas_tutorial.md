# Fiche de lecture - DNS Measurements with RIPE Atlas (Tutorial)

**Référence bibliographique** :
Bortzmeyer, S. (n.d.). DNS measurements with RIPE Atlas. *AFNIC Presentation*. Retrieved from https://www.ripe.net/media/documents/DNS-Measurements-with-RIPE-Atlas.pdf

**Thème** : Tutorial pratique mesures DNS avec RIPE Atlas

**Intérêt pour le mémoire** :
Tutorial pratique essentiel par un expert DNS français (AFNIC). Guide opérationnel pour utiliser RIPE Atlas pour mesures DNS : interfaces (web, API, CLI), options de configuration, pièges à éviter. Application directe pour implémentation de notre projet.

---

## Contexte de lecture

**Date de lecture** : 21 janvier 2026
**Section du mémoire** : 2.5 (État de l'art - RIPE Atlas), 4 (Méthodologie - Implémentation pratique)

---

## Contenu du tutorial

### Objectif(s) / Question(s) de recherche

**Objectif principal** : Fournir un guide pratique pour effectuer des mesures DNS avec RIPE Atlas.

**Public cible** : Chercheurs et opérateurs réseaux souhaitant utiliser RIPE Atlas pour mesures DNS.

**Motivation** :
- DNS = infrastructure critique mais souvent oubliée dans études résilience/QoS
- RIPE Atlas permet mesures DNS distribuées géographiquement
- Besoin de documentation pratique pour utilisation effective

### Cadre global d'explication

**DNS rappel** :
- Partie infrastructure Internet
- Aussi nécessaire qu'IP
- **Souvent oublié dans études résilience/QoS** ← Point important

**RIPE Atlas capabilities** :
- Sondes peuvent faire mesures DNS
- Nombreuses options disponibles via API
- Plusieurs interfaces d'accès

### Méthodologie (Tutorial pratique)

**Type de document** : Tutorial / Guide opérationnel

#### 1. Interface Web

**Étape 1 - Définitions** :
- **Address Family** : IPv4 ou IPv6
- **Query Class** : IN (Internet) ou CHAOS
- **Query Type** : A, AAAA, NS, MX, TXT, etc.
- **Query Argument** : Nom de domaine à résoudre
- **Use the Probe's Resolver(s)** : Utiliser resolver local de la sonde
- **Resolve on Probe** : Forcer résolution sur la sonde
- **Set NSID bit** : Nameserver Identifier (RFC5001)
- **Use Macros** : Variables dynamiques ($p=probe ID, $r=random, $t=timestamp)

**Options avancées disponibles** (non détaillées dans slides).

**Étape 2 - Sélection sondes** :
- Sélection par critères géographiques, AS, tags
- Tags disponibles : `system-resolves-a-correctly`, `system-r...` (tronqué)

**Résultats interface web** :
- Tableau avec Probe ID, ASN (IPv4/IPv6), Time, Answer, NSID, Response Time
- Visualisation graphique temps de réponse (code couleur)
- Statuts DNS : NOERROR, FORMERR, etc.
- Drapeaux pays pour localisation géographique

#### 2. Interface API

**Format JSON** :
```json
{
  'definitions': [{
    'protocol': 'UDP',
    'description': 'DNS resolution of ns.eu.org',
    'af': 4,
    'query_argument': 'ns.eu.org',
    'query_type': 'AAAA',
    'query_class': 'IN',
    'set_rd_bit': True,
    'type': 'dns',
    'use_probe_resolver': True
  }],
  'is_oneoff': True,
  'probes': [{
    'requested': 10,
    'type': 'area',
    'value': 'WW',
    'tags': {
      'include': ['system-resolves-a-correctly', 'system-r...']
    }
  }]
}
```

**Paramètres clés** :
- `protocol` : UDP ou TCP
- `af` : 4 (IPv4) ou 6 (IPv6)
- `query_type` : Type d'enregistrement DNS
- `set_rd_bit` : Recursion Desired flag
- `use_probe_resolver` : Utiliser resolver de la sonde
- `is_oneoff` : Mesure ponctuelle (True) ou récurrente (False)
- `type: 'area', value: 'WW'` : Sélection mondiale

#### 3. Options DNS nombreuses (détaillées slide 8)

**Options UDP/TCP** :
- `[dns] udp_payload_size (integer)` : Taille payload UDP (512-4096, défaut 512)
- `[dns] protocol (string)` : ['UDP' or 'TCP'], défaut UDP

**Options resolver** :
- `[dns] use_probe_resolver (boolean)` : Envoyer query au resolver local sonde
- `[dns] set_rd_bit (boolean)` : Flag Recursion Desired

**Options query** :
- `[dns] query_class (string)` : ['IN' or 'CHAOS']
- `[dns] query_argument (string)` : L'argument (nom de domaine) de la query
- `[dns] prepend_probe_id (boolean)` : Ajouter probe ID + timestamp pour unicité

**Options retries et raw data** :
- `[dns] retry (integer)` : Nombre de tentatives retry
- `[dns] include_qbuf (boolean)` : Inclure raw DNS query data (défaut false)
- `[dns] include_abuf (boolean)` : Inclure raw DNS answer data (défaut true)

**Options DNSSEC** :
- `[dns] set_nsid_bit (boolean)` : Flag NSID (RFC5001)

#### 4. Outil CLI : Magellan

**Exemple utilisation** :
```bash
% ripe-atlas measure dns --query-argument=lqdn.net
```

**Output format dig** :
```
Probe #29198
; <<>> RIPE Atlas Tools <<>> lqdn.net.
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 47134
;; flags: qr ra rd; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 10

;; QUESTION SECTION:
;lqdn.net.                     IN      A

;; ANSWER SECTION:
lqdn.net.              600     IN      A       204.12.240.154

;; Query time: 386.869 msec
;; SERVER: 172.20.7.1#53(172.20.7.1)
;; WHEN: Mon Oct 02 17:43:55 CEST 2017
;; MSG SIZE  rcvd: 253
```

**Avantage** : Format familier pour utilisateurs `dig`.

#### 5. Outil custom de Bortzmeyer

**Exemple** :
```bash
% atlas-resolve --nsid --type AAAA --requested 10 \
  --country FR mamot.fr
[2a00:99a0:0:1000::7] : 9 occurrences
Test #9407903 done at 2017-10-02T15:47:28Z
```

**Features** :
- Sélection par pays (`--country FR`)
- Type de query (`--type AAAA`)
- Nombre de sondes (`--requested 10`)
- NSID option (`--nsid`)
- Output agrégé (occurrences d'adresses IP)
- Test ID et timestamp

#### 6. Résultats en JSON

**Structure** :
```json
{
  "from": "89.142.236.92",
  "msm_id": 9668778,
  "msm_name": "Tdig",
  "prb_id": 16336,
  "resultset": [
    {
      "dst_addr": "192.168.1.1",
      "result": {
        "ANCOUNT": 3,
        "ARCOUNT": 1,
        "ID": 10350,
        "abuf": "KG6BgAABAAMA..."
      }
    }
  ]
}
```

**Champs importants** :
- `from` : Adresse IP source (sonde)
- `msm_id` : ID de la mesure
- `prb_id` : ID de la sonde
- `dst_addr` : Adresse du resolver interrogé
- `ANCOUNT`, `ARCOUNT` : Compteurs sections DNS
- `abuf` : Raw DNS answer (base64)

### Pièges à éviter (Traps)

**Problème 1 - Resolvers étranges** :
- Certaines sondes utilisent **resolvers alternatifs** (alternative roots)
- **Lying resolvers** : Resolvers menteurs (filtrage, redirection)
- Impact : Résultats DNS incorrects ou biaisés

**Problème 2 - Interception réseau** :
- Certains réseaux **interceptent et réécrivent trafic DNS**
- **Proxies transparents** DNS
- Impact : Mesures ne reflètent pas vraie résolution DNS

**Mitigation suggérée** :
- Filtrer sondes avec tags `system-resolves-a-correctly`
- Vérifier cohérence résultats entre sondes
- Détecter outliers (réponses anormales)

### Cas d'usage (Examples of use)

**1. Mesurer la censure** :
- Sélectionner sondes par pays
- Comparer réponses DNS entre pays
- **⚠️ WARNING : May raise ethical issues**
- Exemple : Nosyk 2024 montre 69% sondes chinoises bloquées (Meta)

**2. Vérifier instances anycast** :
- Mesurer depuis multiples localisations
- Identifier instances serveur anycast
- Cartographier distribution géographique

**3. Tester résolution globale domaine** :
- Vérifier que domaine résout partout
- Détecter problèmes configuration zones
- Citation : "Many zones have all eggs in the same basket"

---

## Analyse personnelle

### Que garder pour le mémoire

**Concepts clés à réutiliser** :
- ✅ 3 interfaces disponibles : Web, API, CLI
- ✅ Options DNS nombreuses (UDP/TCP, RD bit, NSID, etc.)
- ✅ Format résultats : JSON structuré + raw DNS (abuf)
- ✅ Sélection sondes par : pays, AS, area, tags
- ✅ Tags filtrage : `system-resolves-a-correctly` (essentiel!)
- ✅ Mesures one-off vs récurrentes
- ✅ Macros variables ($p, $r, $t)

**Méthodes applicables** :
- Utiliser API programmatique (Python)
- Filtrer sondes par tags (éviter resolvers problématiques)
- Parser résultats JSON (msm_id, prb_id, dst_addr, abuf)
- Vérifier cohérence résultats (détecter lying resolvers)
- Sélection géographique ciblée (pays, area:WW)
- Option NSID pour identifier serveurs
- Mesures récurrentes pour dimension temporelle

**Options DNS critiques pour notre projet** :
- `use_probe_resolver: True` : Utiliser resolver local (diversité géographique)
- `set_rd_bit: True` : Recursion Desired
- `include_abuf: True` : Raw DNS answer (analyse détaillée)
- `query_type: 'A'` ou `'AAAA'` : Selon besoins
- `protocol: 'UDP'` : Standard (TCP si truncation)
- `is_oneoff: False` : Mesures récurrentes (dimension temporelle)

**Pièges critiques à éviter** :
- ⚠️ **Resolvers alternatifs/menteurs** → Filtrer avec tags
- ⚠️ **Interception DNS réseau** → Détecter via analyse résultats
- ⚠️ **Proxies transparents** → Comparer dst_addr attendu vs réel
- ⚠️ **Ethical issues censure** → Considérations éthiques

### Critique personnelle

**Forces du tutorial** :
- ✅ Exemples concrets et pratiques
- ✅ Couverture 3 interfaces (Web, API, CLI)
- ✅ Screenshots interface web (très utile)
- ✅ Format JSON détaillé
- ✅ **Section "Traps" cruciale** (pièges à éviter)
- ✅ Cas d'usage réalistes
- ✅ Warning éthique (censure)
- ✅ Par expert reconnu (AFNIC/Bortzmeyer)

**Faiblesses identifiées** :
- ⚠️ Pas de date (document non daté)
- ⚠️ Exemples 2017 (possiblement obsolètes)
- ⚠️ Options avancées non détaillées (slide 5)
- ⚠️ Pas de discussion système crédits
- ⚠️ Pas d'exemples mesures récurrentes
- ⚠️ Pas d'exemples traitement données volumineuses
- ⚠️ Pas de stratégies optimisation (nombre sondes vs précision)
- ⚠️ Tool custom Bortzmeyer non open source (?)

**Lien avec autres articles lus** :
- **Nosyk et al. (2024) - RIPE Atlas DITL** :
  - Nosyk analyse infrastructure, Bortzmeyer montre utilisation pratique
  - Complémentaires : théorie (Nosyk) vs pratique (Bortzmeyer)
  - Traps Bortzmeyer = limitations Nosyk (resolvers, interception)

- **Holterbach (2015) - Interference** :
  - Bortzmeyer ne mentionne pas interférence (limitation!)
  - Besoin combiner : tutorial Bortzmeyer + warnings Holterbach
  - Ajouter : sélection hardware récent, timestamps réels

- **OpenINTEL (van Rijswijk-Deij 2016)** :
  - OpenINTEL = infrastructure dédiée (pas de traps resolvers)
  - RIPE Atlas = infrastructure partagée (traps Bortzmeyer)
  - Trade-off : contrôle vs diversité géographique

**Questions ouvertes** :
1. **Outil atlas-resolve de Bortzmeyer est-il open source ?**
   → Chercher sur GitHub Bortzmeyer
2. **Comment détecter automatiquement lying resolvers ?**
   → Comparaison réponses multiples sondes ? Baseline OpenINTEL ?
3. **Quelle proportion sondes ont resolvers problématiques ?**
   → Statistiques RIPE Atlas sur tags ?
4. **Comment gérer interception DNS réseau ?**
   → Mesures directes vers autoritatifs (pas via resolver) ?
5. **Ethical considerations pour mesures censure ?**
   → Consulter guidelines RIPE Atlas éthique
6. **Format abuf (base64) : comment parser efficacement ?**
   → Librairie Python dnspython ?
7. **Macros ($p, $r, $t) : cas d'usage pratiques ?**
   → Quand utiliser pour notre projet ?

### Citations importantes

> "Domain Name System: A part of the Internet infrastructure, As necessary as IP, **Often forgotten in studies about resilience or quality of service.**" (p. 3)

**Sur les pièges** :
> "Some probes use strange resolvers (alternative roots, lying resolvers. . . )" (p. 12)

> "Some networks intercept and rewrite DNS traffic, some have transparent proxies." (p. 12)

**Sur cas d'usage censure** :
> "Measuring censorship (selecting probes by country). **Warning: may raise ethical issues.**" (p. 13)

**Sur anycast** :
> "Check the different instances of an anycast server." (p. 13)

**Sur résilience** :
> "Test that your domain name resolves from everywhere. **(Many zones have all eggs in the same basket.)**" (p. 13)

---

## Utilisation dans le mémoire

### Sections concernées

- **Section 2.5** : RIPE Atlas et mesures distribuées
  Description interfaces disponibles (Web, API, CLI)
  Options DNS measurement
  Pièges à éviter (resolvers, interception)

- **Section 4** : Méthodologie - Implémentation
  Choix interface : API programmatique (Python)
  Configuration mesures DNS :
  - `use_probe_resolver: True`
  - Tags filtrage : `system-resolves-a-correctly`
  - Mesures récurrentes (`is_oneoff: False`)
  - Options NSID, RD bit, abuf
  Sélection sondes (pays, area, AS)
  Parsing résultats JSON

- **Section 5** : Résultats
  Format résultats JSON (msm_id, prb_id, abuf)
  Traitement données brutes (abuf parsing)
  Détection anomalies (lying resolvers, interception)

- **Section 6** : Validation
  Filtrage résultats suspects (tags, cohérence)
  Comparaison avec baseline (OpenINTEL?)

- **Section 7** : Discussion
  Limitations : resolvers alternatifs, interception réseau
  Considérations éthiques (si mesures censure)
  Mitigation pièges (filtrage, validation)

### Points à développer

**Dans état de l'art** :
- Interfaces RIPE Atlas disponibles :
  - Web : Accessible, mais pas scalable
  - API : Programmatique, scalable, format JSON
  - CLI (Magellan) : Format dig, interactif
  - Custom tools (atlas-resolve Bortzmeyer)
- Options DNS measurement exhaustives (tableau)
- Format résultats JSON structuré

**Pour notre méthodologie** :
- **Choix interface** : API REST programmatique (Python)
- **Configuration mesures** :
  ```json
  {
    'protocol': 'UDP',
    'af': 4,  // IPv4 priorité, IPv6 si dual-stack
    'query_type': 'A',  // ou AAAA selon analyse
    'query_class': 'IN',
    'set_rd_bit': True,
    'use_probe_resolver': True,  // CRUCIAL pour diversité géo
    'set_nsid_bit': True,  // Identifier serveurs
    'include_abuf': True,  // Raw data pour analyse
    'is_oneoff': False  // Mesures récurrentes
  }
  ```
- **Sélection sondes** :
  ```json
  {
    'requested': N,  // À définir selon crédits
    'type': 'area',
    'value': 'WW',  // Mondial
    'tags': {
      'include': ['system-resolves-a-correctly'],  // CRUCIAL
      // Possiblement: hardware version >= 3
    }
  }
  ```
- **Parsing résultats** :
  - Extraire : msm_id, prb_id, dst_addr, timestamp
  - Décoder abuf (base64 → DNS answer)
  - Parser réponses DNS (dnspython)
  - Enrichir métadonnées (GeoIP, ASN)
- **Détection anomalies** :
  - Identifier lying resolvers (réponses incohérentes)
  - Détecter interception (dst_addr unexpected)
  - Filtrer outliers (response time, errors)

**Pour validation/filtrage** :
- **Tags obligatoires** : `system-resolves-a-correctly`
- **Vérification cohérence** :
  - Comparer réponses multiples sondes même région
  - Baseline avec OpenINTEL (si même domaines)
  - Détecter réponses DNS anormales (alternative roots)
- **Seuils de filtrage** :
  - Response time > X ms (interférence?)
  - Taux erreurs > Y% par sonde
  - Réponses uniques (1 sonde ≠ toutes autres)

**Pour discussion éthique** :
- Si mesures incluent censure → Guidelines RIPE Ethics
- Consulter : https://labs.ripe.net/author/kistel/ethics-of-ripe-atlas-measurements/ (voir recherche.md)
- Anonymisation données si publication

### Tableau des options DNS (pour méthodologie)

| Option | Type | Défaut | Notre choix | Raison |
|--------|------|--------|-------------|--------|
| `protocol` | UDP/TCP | UDP | **UDP** | Standard, suffisant |
| `af` | 4/6 | - | **4** | IPv4 priorité |
| `query_type` | A/AAAA/NS/... | - | **A** | Adresses IPv4 |
| `query_class` | IN/CHAOS | IN | **IN** | Internet class |
| `set_rd_bit` | boolean | - | **True** | Recursion désirée |
| `use_probe_resolver` | boolean | False | **True** | **Diversité géo!** |
| `set_nsid_bit` | boolean | False | **True** | Identifier serveurs |
| `include_abuf` | boolean | True | **True** | Raw data analyse |
| `include_qbuf` | boolean | False | **False** | Pas nécessaire |
| `udp_payload_size` | 512-4096 | 512 | **512** | Standard |
| `is_oneoff` | boolean | - | **False** | **Récurrent!** |
| `retry` | integer | - | **2** | Balance fiabilité/charge |

### Références croisées

**Outils à explorer** :
- [X] Magellan (ripe-atlas CLI) - mentionné dans tutorial
- [ ] atlas-resolve (tool Bortzmeyer) - chercher GitHub
- [ ] Cousteau (Python library RIPE Atlas API)
- [ ] Sagan (Python library parsing résultats)
- [ ] dnspython (parsing abuf)

**Documentation à consulter** :
- [X] API Reference : https://atlas.ripe.net/docs/api/v2/reference/#/measurements (mentionné slide 4)
- [ ] Guide best practices : https://atlas.ripe.net/docs/howtos/best-practices/
- [ ] Ethics guidelines : https://labs.ripe.net/author/kistel/ethics-of-ripe-atlas-measurements/

**Articles connexes à lire** :
- [ ] Bortzmeyer blog posts sur RIPE Atlas (https://www.bortzmeyer.org/)
- [ ] RIPE Labs articles par Bortzmeyer
- [ ] RFC 5001 (NSID - Nameserver Identifier)

---

**Tags** : #ripe-atlas #dns #tutorial #practical-guide #api #measurement #traps #ethics #bortzmeyer #afnic

**Statut** : [X] Lu / [ ] Relu / [X] Fiché / [ ] Intégré mémoire

**Prochaines étapes** :
1. ✅ Fiche complétée
2. ⏭️ Chercher tool atlas-resolve (GitHub Bortzmeyer)
3. ⏭️ Lire documentation Cousteau + Sagan (Python libs)
4. ⏭️ Consulter ethics guidelines RIPE Atlas
5. ⏭️ Tester exemples API (créer mesure test)
6. ⏭️ Analyser format abuf (parser avec dnspython)
7. ⏭️ Identifier stratégie filtrage lying resolvers
