# Chapitre 3 - Méthodologie

## 3.1 Vue d'ensemble de l'approche

### 3.1.1 Objectif général

Notre approche vise à concevoir et déployer un système de **mesures DNS distribuées géographiquement** qui capture la diversité spatiale et temporelle des réponses DNS pour les domaines web les plus populaires. Contrairement aux infrastructures existantes comme OpenINTEL qui mesurent depuis un point unique, notre contribution principale consiste à exploiter la distribution géographique de RIPE Atlas pour observer les variations de réponses DNS selon la localisation du client.

**Objectif opérationnel** : Archiver les réponses DNS pour un ensemble représentatif de domaines populaires (Tranco Top 10K), mesurées depuis de multiples vantage points géographiques (sondes RIPE Atlas), sur une période de plusieurs mois, tout en optimisant l'utilisation des crédits RIPE Atlas disponibles.

### 3.1.2 Questions de recherche

Nos travaux visent à répondre aux quatre questions de recherche formulées dans le Chapitre 2 (section 2.7.4) :

**Q1** : Quelle proportion de domaines Tranco Top 10K retourne des réponses DNS différentes selon la localisation géographique ?

**Q2** : Quelle est la stabilité temporelle des enregistrements DNS pour ces domaines (variation jour/semaine/mois) ?

**Q3** : Les biais géographiques RIPE Atlas (91% RIPE+ARIN) impactent-ils significativement l'observation de la diversité ?

**Q4** : Quel est l'impact du choix de resolver (ISP local vs DNS public) sur les adresses IP observées ?

### 3.1.3 Architecture globale du système

Notre système s'articule autour de **quatre composantes principales** inspirées de l'architecture OpenINTEL (van Rijswijk-Deij et al., 2016) mais adaptées aux contraintes de RIPE Atlas :

```
┌─────────────────────────────────────────────────────────────┐
│                   ÉTAPE 1 : INPUT DATA                      │
│  - Téléchargement liste Tranco (hebdomadaire)              │
│  - Sélection domaines (Top 10K + filtres)                  │
│  - Détection domaines ajoutés/supprimés (delta)            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              ÉTAPE 2 : MEASUREMENT SCHEDULING               │
│  - Sélection sondes RIPE Atlas (critères géographiques)    │
│  - Configuration mesures DNS (API RIPE Atlas)              │
│  - Optimisation utilisation crédits                        │
│  - Gestion scheduling (tolérance désynchronisation)        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│               ÉTAPE 3 : DATA COLLECTION                     │
│  - Collecte résultats via API RIPE Atlas                   │
│  - Parsing JSON → extraction champs pertinents             │
│  - Décodage abuf (raw DNS answers)                         │
│  - Enrichissement métadonnées (GeoIP, AS, tags)            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│          ÉTAPE 4 : STORAGE AND PREPROCESSING                │
│  - Stockage brut : Apache Avro (archivage)                 │
│  - Stockage analytics : Apache Parquet (columnar)          │
│  - Filtrage données invalides (lying resolvers, etc.)      │
│  - Indexation temporelle et géographique                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 ÉTAPE 5 : ANALYSIS                          │
│  - Détection variations géographiques (Q1)                 │
│  - Analyse stabilité temporelle (Q2)                       │
│  - Évaluation biais géographiques (Q3)                     │
│  - Impact choix resolver (Q4)                              │
│  - Génération rapports et visualisations                   │
└─────────────────────────────────────────────────────────────┘
```

**Trade-offs assumés** :

| Dimension | Choix | Raison |
|-----------|-------|--------|
| **Couverture domaines** | 10K (vs 123M OpenINTEL) | Contrainte crédits RIPE Atlas |
| **Vantage points** | 12.9K (RIPE Atlas) | Diversité géographique prioritaire |
| **Fréquence mesures** | Quotidienne | Balance précision temporelle vs crédits |
| **Contrôle infrastructure** | Limité (plateforme partagée) | Accepté pour accès diversité géographique |

---

## 3.2 Sélection et gestion des domaines

### 3.2.1 Choix de la liste Tranco

Nous utilisons la **liste Tranco** (Le Pochat et al., 2019) plutôt que les listes commerciales (Alexa, Umbrella, Majestic, Quantcast) pour les raisons suivantes :

**Stabilité** : Tranco présente un changement quotidien de seulement **0.6%** contre **50% pour Alexa** depuis janvier 2018. Cette stabilité est cruciale pour notre analyse longitudinale, car elle permet de suivre les mêmes domaines dans le temps sans bruit dû à l'instabilité de la liste elle-même.

**Résistance à la manipulation** : Tranco requiert un effort de manipulation **4× supérieur** aux listes individuelles (Le Pochat et al., 2019, p. 2). Alexa peut être manipulé avec une seule requête HTTP pour entrer dans le top 1M, tandis que Tranco combine quatre sources et utilise une moyenne sur 30 jours, rendant la manipulation beaucoup plus coûteuse.

**Reproductibilité** : Le service https://tranco-list.eu fournit des **permalinks** pour chaque liste générée, garantissant que nos résultats sont reproductibles. Chaque liste a un identifiant unique (ex: `7DKY`, `8QNZ`) permettant de citer précisément la version utilisée.

**Adoption scientifique** : Tranco est utilisé dans **600+ publications** académiques (état 2024) et est devenu le standard de facto pour la recherche en sécurité réseau.

### 3.2.2 Taille de la liste : Top 10K

Nous avons choisi d'analyser le **Tranco Top 10K** après évaluation de trois options :

| Option | Domaines | Mesures/jour | Coût crédits | Faisabilité |
|--------|----------|--------------|--------------|-------------|
| **Top 1K** | 1,000 | ~1M | Faible | ✅ Facile |
| **Top 10K** | 10,000 | ~10M | Modéré | ✅ **Choisi** |
| **Top 100K** | 100,000 | ~100M | Élevé | ⚠️ Critique |

**Calcul estimatif** (pour Top 10K) :
- **Domaines** : 10,000
- **Sondes par mesure** : 100 (diversité géographique)
- **Types de requêtes** : A (IPv4)
- **Fréquence** : 1×/jour
- **Total** : 10,000 domaines × 100 sondes × 1 query = **1,000,000 résultats/jour**
- **Sur 3 mois** : 1M × 90 jours = **90 millions de résultats**

**Justification du choix Top 10K** :
- **Représentatif** : Capture les sites web majeurs (Google, Facebook, Amazon, etc.)
- **Faisable** : Compatible avec les crédits RIPE Atlas alloués au projet
- **Scientifique** : Utilisé dans de nombreuses études (Calder et al., 2015; Wang et al., 2018)
- **Analysable** : Volume de données gérable (quelques TB compressés sur 3 mois)

### 3.2.3 Configuration Tranco

Nous générons une liste Tranco personnalisée avec la configuration suivante :

```python
# Configuration Tranco via API ou site web
{
  "list_size": 10000,
  "averaging_period": 30,  # 30 jours (par défaut)
  "providers": ["alexa", "umbrella", "majestic", "quantcast"],  # Toutes
  "method": "dowdall",  # Dowdall rule (reflète Zipf's law)
  "filters": {
    "responsiveness": True,  # Domaines accessibles (HTTP 200)
    "safe_browsing": True    # Exclure malware (Google Safe Browsing)
  }
}
```

**Mise à jour de la liste** : Hebdomadaire (chaque lundi), permettant de :
- Capturer l'évolution lente des domaines populaires
- Limiter les changements dus à l'instabilité quotidienne
- Réduire la charge de mise à jour du système

**Gestion des changements** :
- **Domaines ajoutés** (nouveaux dans top 10K) : Ajoutés immédiatement aux mesures
- **Domaines supprimés** (sortis du top 10K) : Continués pendant 2 semaines (capture transition)
- **Delta tracking** : Fichier CSV historisant les changements hebdomadaires

### 3.2.4 Filtrage et validation des domaines

**Étape 1 - Validation technique** :
- Requête A record depuis un point de référence (notre infrastructure locale)
- Vérification : NOERROR status (pas NXDOMAIN, SERVFAIL)
- Exclusion domaines invalides ou parkés (< 512 bytes content)

**Étape 2 - Filtrage sécurité** :
- Vérification Google Safe Browsing API (gratuite)
- Exclusion domaines classés : malware, phishing, unwanted software
- Justification : Éviter mesures fréquentes vers infrastructures malveillantes

**Étape 3 - Filtrage performance** (optionnel) :
- Chrome UX Report (CrUX) : sites réellement visités par utilisateurs Chrome
- Avantage : Garantit que domaines sont activement utilisés (pas juste enregistrés)

**Taux d'exclusion attendu** (basé sur Le Pochat et al., 2019) :
- **Responsiveness** : ~5% domaines Tranco top 10K non-accessibles
- **Safe Browsing** : ~0.05% domaines malveillants
- **Total exclusions** : ~500-600 domaines sur 10K
- **Résultat final** : ~9,400-9,500 domaines mesurés

---

## 3.3 Configuration des mesures RIPE Atlas

### 3.3.1 Sélection des sondes

**Critères de sélection** :

Nous sélectionnons les sondes RIPE Atlas selon **quatre critères prioritaires** :

**Critère 1 - Distribution géographique** :
- Objectif : Maximiser la couverture mondiale
- Approche : Sélection équilibrée par continent
- Méthode : `type: 'area', value: 'WW'` (World-Wide)
- Contrainte : Accepter biais géographique RIPE Atlas (91% Europe+Amérique du Nord)

**Critère 2 - Resolver correctement configuré** :
- Tag obligatoire : `system-resolves-a-correctly`
- Raison : Éviter lying resolvers et alternative roots (Bortzmeyer, tutorial RIPE Atlas)
- Impact : Exclusion ~10-15% sondes (estimation)

**Critère 3 - Hardware récent** :
- Version sonde : v3 minimum, v5 préféré
- Raison : Limiter interférence timing (Holterbach et al., 2015)
- Impact : v1/v2 = +1.10-1.20 ms médiane, +7.30-7.70 ms 95e percentile
- v3/v5 = impact minimal (0.06 ms médiane)

**Critère 4 - Connectivité dual-stack** (optionnel) :
- Tag : `system-ipv4-works` ET `system-ipv6-works`
- Avantage : Permet mesures IPv4 + IPv6 depuis mêmes vantage points
- Taux : 46.5% sondes publiques dual-stack (Nosyk et al., 2024)
- Décision : Privilégier mais pas exiger (maximiser couverture géographique)

**Configuration API RIPE Atlas** :

```json
{
  "probes": [{
    "requested": 100,           // Nombre de sondes par mesure
    "type": "area",
    "value": "WW",               // Sélection mondiale
    "tags": {
      "include": [
        "system-resolves-a-correctly",  // OBLIGATOIRE
        "system-ipv4-works"             // OBLIGATOIRE (mesures IPv4)
      ]
    }
  }]
}
```

**Stratégie de répartition géographique** :

Pour compenser le biais géographique RIPE Atlas, nous appliquons une **pondération inverse** :

| Région | Sondes RIPE | % Total | Sondes allouées | % Allocation |
|--------|-------------|---------|-----------------|--------------|
| **Europe** | ~5,000 | 40% | 30 | 30% |
| **Amérique du Nord** | ~3,500 | 28% | 25 | 25% |
| **Asie** | ~2,000 | 16% | 20 | 20% |
| **Amérique du Sud** | ~1,000 | 8% | 10 | 10% |
| **Afrique** | ~700 | 5% | 10 | 10% |
| **Océanie** | ~400 | 3% | 5 | 5% |
| **TOTAL** | ~12,600 | 100% | **100** | 100% |

**Objectif** : Sur-représenter les régions sous-représentées (Afrique 10% allocation vs 5% disponibilité) pour obtenir des statistiques plus équilibrées géographiquement.

### 3.3.2 Configuration des mesures DNS

**Paramètres de mesure** :

Basé sur le tutorial Bortzmeyer et les best practices RIPE Atlas (Nosyk et al., 2024), nous configurons les mesures DNS comme suit :

```json
{
  "definitions": [{
    "type": "dns",
    "af": 4,                          // IPv4 (priorité)
    "query_type": "A",                // Type A record (adresses IPv4)
    "query_class": "IN",              // Internet class
    "query_argument": "example.com",  // Domaine à résoudre (variable)

    "use_probe_resolver": true,       // *** CRUCIAL : diversité géographique ***
    "set_rd_bit": true,               // Recursion Desired flag
    "set_nsid_bit": true,             // NSID (identifier serveurs)

    "protocol": "UDP",                // UDP standard (TCP si truncation)
    "udp_payload_size": 512,          // Taille standard

    "include_abuf": true,             // Raw DNS answer (analyse détaillée)
    "include_qbuf": false,            // Query buffer non nécessaire

    "retry": 2,                       // 2 tentatives si échec
    "timeout": 5000,                  // 5 secondes timeout

    "description": "Thesis DNS geo-diversity - Tranco YYYY-MM-DD",
    "is_oneoff": false,               // Mesures récurrentes
    "interval": 86400,                // 1×/jour (24h = 86400s)

    "tags": [
      "thesis-dns-geo",
      "tranco-2026-03-21"             // Date de la liste Tranco
    ]
  }]
}
```

**Justification des choix** :

**`use_probe_resolver: true`** : C'est le paramètre le plus critique. En utilisant le resolver local de chaque sonde, nous capturons la diversité géographique réelle des réponses DNS :
- Sondes Europe → Resolvers ISP européens → Réponses CDN optimisées pour Europe
- Sondes Asie → Resolvers ISP asiatiques → Réponses CDN optimisées pour Asie
- Sans ce paramètre, toutes les sondes interrogeraient le même resolver → perte de diversité

**`set_nsid_bit: true`** : Permet d'identifier le serveur DNS autoritaire répondant via l'option NSID (RFC 5001). Utile pour :
- Détecter instances anycast différentes
- Identifier providers DNS (Cloudflare, Route53, etc.)
- Analyser distribution géographique serveurs autoritaires

**`include_abuf: true`** : Le champ `abuf` contient la réponse DNS complète encodée en base64. Essentiel pour :
- Parser tous les records DNS (pas seulement les A)
- Extraire TTL, flags DNS, sections additionnelles
- Analyser réponses DNSSEC si présentes

**`interval: 86400`** : Mesures quotidiennes (24h) permettent de :
- Capturer variations journalières (migrations serveurs, maintenance)
- Détecter tendances hebdomadaires/mensuelles
- Optimiser crédits (vs mesures horaires trop coûteuses)

**`tags`** : Tags systématiques pour :
- Retrouver nos mesures via API (`thesis-dns-geo`)
- Tracer version liste Tranco utilisée (`tranco-2026-03-21`)
- Faciliter reproductibilité scientifique

### 3.3.3 Gestion de l'interférence et du scheduling

**Problème** : Holterbach et al. (2015) ont démontré deux types d'interférence sur RIPE Atlas :
1. **Timing interference** : Augmentation latences (+1-7 ms selon hardware)
2. **Scheduling interference** : Désynchronisation jusqu'à **1 heure**

**Mitigation timing interference** :
- Sélection hardware v3+ (critère déjà appliqué section 3.3.1)
- Accepter variance timing dans analyses (pas critique pour DNS vs traceroute)
- Mesures DNS = rapides (<100ms typique) → moins sensibles que traceroute

**Mitigation scheduling interference** :
- **Ne pas se fier aux timestamps programmés** → Utiliser `timestamp` réels dans résultats
- Tolérance temporelle : Fenêtre de **±2h** autour de l'horaire prévu
- Validation a posteriori : Vérifier distribution temporelle résultats collectés
- Filtrage : Exclure résultats >4h de désynchronisation (outliers extrêmes)

**Exemple gestion scheduling** :

```python
# Horaire programmé : 2026-03-21 00:00:00 UTC
# Tolérance : ±2h (acceptable: 22:00-02:00)
# Filtrage : >4h rejeté (avant 20:00 ou après 04:00)

def validate_timing(result_timestamp, scheduled_timestamp):
    delta = abs(result_timestamp - scheduled_timestamp)
    if delta <= 2 * 3600:  # ±2h
        return "VALID"
    elif delta <= 4 * 3600:  # 2-4h
        return "WARNING"
    else:  # >4h
        return "REJECTED"
```

### 3.3.4 Optimisation de l'utilisation des crédits

**Calcul consommation crédits** :

Les crédits RIPE Atlas sont consommés selon la formule (documentation RIPE Atlas) :

```
Crédits = base_cost × num_probes × num_measurements × duration_days
```

Pour nos mesures DNS récurrentes (1×/jour) :
- **Base cost DNS** : 10 crédits/mesure
- **Nombre de sondes** : 100
- **Durée** : 90 jours (3 mois)
- **Nombre de domaines** : 10,000

**Coût total estimé** :
```
10,000 domaines × 10 crédits × 100 sondes × 90 jours / 10,000 (normalisation API)
= 900,000 crédits pour 3 mois
```

**Stratégies d'optimisation** :

**Stratégie 1 - Vérification mesures existantes** :
- Avant de lancer une mesure, vérifier via API RIPE si mesures similaires existent
- Réutiliser résultats publics si disponibles (économie crédits)
- Justification : Nosyk et al. (2024) recommandent explicitement cette pratique

**Stratégie 2 - Mesures récurrentes vs one-shot** :
- Privilégier mesures récurrentes (1 setup, N jours) vs one-shot quotidiens
- Économie : Setup unique vs 90 setups individuels
- Trade-off : Moins de flexibilité (modification en cours difficile)

**Stratégie 3 - Batching intelligent** :
- Grouper domaines par serveurs DNS autoritaires identiques
- Exemple : `google.com`, `youtube.com`, `gmail.com` → même NS records
- Potentiel : Réduire redondance mesures vers mêmes serveurs

**Stratégie 4 - Adaptation dynamique** :
- Monitoring consommation crédits hebdomadaire
- Si budget serré : réduire fréquence (1×/2 jours) ou nombre sondes (100→50)
- Si budget confortable : étendre à Top 20K ou mesures IPv6

---

## 3.4 Collecte et traitement des données

### 3.4.1 Collecte via API RIPE Atlas

**Workflow de collecte** :

```python
# Pseudo-code simplifié du pipeline de collecte

import requests
from datetime import datetime, timedelta

RIPE_API_BASE = "https://atlas.ripe.net/api/v2/"
API_KEY = "YOUR_API_KEY"

# Étape 1: Récupérer liste des mesures actives
def fetch_measurements():
    """Récupère IDs de toutes nos mesures actives"""
    response = requests.get(
        f"{RIPE_API_BASE}/measurements/",
        params={
            "tags": "thesis-dns-geo",
            "status": "1"  # Ongoing
        },
        headers={"Authorization": f"Key {API_KEY}"}
    )
    return [m["id"] for m in response.json()["results"]]

# Étape 2: Collecter résultats pour chaque mesure
def fetch_results(measurement_id, start_time, end_time):
    """Récupère résultats entre start_time et end_time"""
    response = requests.get(
        f"{RIPE_API_BASE}/measurements/{measurement_id}/results/",
        params={
            "start": int(start_time.timestamp()),
            "stop": int(end_time.timestamp())
        }
    )
    return response.json()

# Étape 3: Collecte quotidienne automatisée
def daily_collection():
    """Collecte quotidienne des résultats J-1"""
    yesterday = datetime.now() - timedelta(days=1)
    start = yesterday.replace(hour=0, minute=0, second=0)
    end = yesterday.replace(hour=23, minute=59, second=59)

    measurements = fetch_measurements()

    for msm_id in measurements:
        results = fetch_results(msm_id, start, end)
        store_raw_results(results, msm_id, yesterday)

# Étape 4: Stockage brut (JSON)
def store_raw_results(results, msm_id, date):
    """Stockage brut JSON avant traitement"""
    filename = f"data/raw/{date.strftime('%Y-%m-%d')}/{msm_id}.json"
    with open(filename, 'w') as f:
        json.dump(results, f)
```

**Fréquence de collecte** : Quotidienne, à J+1 (récupération résultats de la veille).

**Gestion des erreurs** :
- Retry automatique (3 tentatives) si API timeout
- Logging de tous les échecs de collecte
- Alerte email si >10% mesures échouent un jour donné

### 3.4.2 Parsing et extraction des données

**Structure résultat RIPE Atlas (JSON)** :

```json
{
  "msm_id": 123456789,
  "prb_id": 16336,
  "timestamp": 1710979200,
  "from": "89.142.236.92",
  "dst_addr": "192.168.1.1",
  "af": 4,
  "result": {
    "ANCOUNT": 3,
    "ARCOUNT": 1,
    "ID": 10350,
    "NSCOUNT": 0,
    "QDCOUNT": 1,
    "abuf": "KG6BgAABAAMA...",  // Base64 encoded DNS answer
    "rt": 48.5,                  // Response time (ms)
    "size": 253
  }
}
```

**Pipeline de parsing** :

**Étape 1 - Extraction champs directs** :
```python
import base64
import dns.message  # dnspython library

def parse_result(result):
    """Parse un résultat RIPE Atlas"""
    parsed = {
        # Métadonnées mesure
        "msm_id": result["msm_id"],
        "prb_id": result["prb_id"],
        "timestamp": result["timestamp"],

        # Métadonnées sonde
        "probe_ip": result["from"],
        "probe_af": result["af"],

        # Métadonnées resolver
        "resolver_ip": result["dst_addr"],

        # Métriques performance
        "response_time_ms": result["result"].get("rt"),
        "response_size": result["result"].get("size"),

        # Compteurs DNS
        "ancount": result["result"].get("ANCOUNT"),
        "arcount": result["result"].get("ARCOUNT"),
        "nscount": result["result"].get("NSCOUNT"),
    }

    # Étape 2: Décodage abuf (raw DNS)
    if "abuf" in result["result"]:
        parsed.update(parse_abuf(result["result"]["abuf"]))

    return parsed
```

**Étape 2 - Décodage abuf (raw DNS answer)** :

```python
def parse_abuf(abuf_b64):
    """Décode et parse la réponse DNS brute"""
    # Décoder base64
    abuf_bytes = base64.b64decode(abuf_b64)

    # Parser avec dnspython
    dns_msg = dns.message.from_wire(abuf_bytes)

    # Extraire informations
    parsed = {
        "dns_rcode": dns_msg.rcode(),     # NOERROR, NXDOMAIN, etc.
        "dns_flags": dns_msg.flags,       # QR, AA, RD, RA, etc.
        "dns_id": dns_msg.id,

        # Extraire records A
        "a_records": [],
        "ttl": None,
    }

    # Parser section Answer
    for rrset in dns_msg.answer:
        if rrset.rdtype == dns.rdatatype.A:
            for rdata in rrset:
                parsed["a_records"].append(str(rdata))
            parsed["ttl"] = rrset.ttl  # TTL (même pour tous records du rrset)

    return parsed
```

**Étape 3 - Enrichissement métadonnées** :

```python
def enrich_metadata(parsed_result):
    """Ajoute métadonnées géographiques et réseau"""

    # GeoIP (MaxMind GeoLite2)
    geo = geoip2.database.Reader('GeoLite2-City.mmdb')
    probe_geo = geo.city(parsed_result["probe_ip"])

    parsed_result["probe_country"] = probe_geo.country.iso_code
    parsed_result["probe_city"] = probe_geo.city.name
    parsed_result["probe_lat"] = probe_geo.location.latitude
    parsed_result["probe_lon"] = probe_geo.location.longitude

    # AS mapping (pyasn)
    asn_db = pyasn.pyasn('ipasn.dat')
    probe_asn, probe_prefix = asn_db.lookup(parsed_result["probe_ip"])

    parsed_result["probe_asn"] = probe_asn
    parsed_result["probe_prefix"] = probe_prefix

    # Même chose pour resolver_ip
    # ... (similaire)

    return parsed_result
```

### 3.4.3 Filtrage et validation

**Filtres appliqués** :

**Filtre 1 - Résultats DNS valides** :
```python
def is_valid_dns_result(result):
    """Vérifie validité technique résultat DNS"""
    # Doit avoir une réponse
    if "result" not in result:
        return False, "NO_RESULT"

    # Doit avoir abuf (raw DNS)
    if "abuf" not in result["result"]:
        return False, "NO_ABUF"

    # RCODE doit être NOERROR (0)
    parsed = parse_abuf(result["result"]["abuf"])
    if parsed["dns_rcode"] != 0:  # 0 = NOERROR
        return False, f"RCODE_{parsed['dns_rcode']}"

    # Doit avoir au moins 1 A record
    if len(parsed["a_records"]) == 0:
        return False, "NO_A_RECORDS"

    return True, "VALID"
```

**Filtre 2 - Détection lying resolvers** :

Basé sur les recommandations de Bortzmeyer (tutorial RIPE Atlas), nous détectons les resolvers suspects :

```python
def detect_lying_resolver(results_for_domain):
    """Détecte resolvers retournant réponses anormales"""

    # Grouper par resolver IP
    by_resolver = {}
    for r in results_for_domain:
        resolver_ip = r["resolver_ip"]
        if resolver_ip not in by_resolver:
            by_resolver[resolver_ip] = []
        by_resolver[resolver_ip].append(r)

    # Identifier réponses majoritaires
    all_ips = []
    for r in results_for_domain:
        all_ips.extend(r["a_records"])

    ip_counts = Counter(all_ips)
    majority_ips = {ip for ip, count in ip_counts.items()
                    if count / len(all_ips) > 0.05}  # >5% fréquence

    # Flaguer resolvers donnant réponses uniques
    lying_resolvers = set()
    for resolver_ip, results in by_resolver.items():
        resolver_ips = set()
        for r in results:
            resolver_ips.update(r["a_records"])

        # Si aucune IP en commun avec majoritaires → suspect
        if not resolver_ips.intersection(majority_ips):
            lying_resolvers.add(resolver_ip)

    return lying_resolvers
```

**Filtre 3 - Timing et scheduling** :

```python
def validate_timing(result, scheduled_time):
    """Valide timing selon critères Holterbach et al. (2015)"""
    result_time = datetime.fromtimestamp(result["timestamp"])
    delta = abs((result_time - scheduled_time).total_seconds())

    if delta <= 2 * 3600:  # ±2h
        return "VALID"
    elif delta <= 4 * 3600:  # 2-4h
        return "WARNING"
    else:  # >4h
        return "REJECTED"
```

**Taux d'exclusion attendus** :

| Filtre | Taux exclusion | Justification |
|--------|----------------|---------------|
| **Pas de résultat** | ~1-2% | Sondes offline, network issues |
| **RCODE ≠ NOERROR** | ~2-3% | NXDOMAIN, SERVFAIL (DNS errors) |
| **Lying resolvers** | ~5-10% | Resolvers alternatifs, interception |
| **Timing >4h** | ~1% | Scheduling interference extrême |
| **TOTAL** | **~10-15%** | **Résultats exploitables : 85-90%** |

### 3.4.4 Stockage des données

**Architecture de stockage 2-tiers** (inspirée d'OpenINTEL) :

**Tier 1 - Archivage long terme (Apache Avro)** :

```python
# Schéma Avro pour résultats DNS
AVRO_SCHEMA = {
    "type": "record",
    "name": "DNSMeasurement",
    "fields": [
        {"name": "msm_id", "type": "long"},
        {"name": "prb_id", "type": "long"},
        {"name": "timestamp", "type": "long"},
        {"name": "domain", "type": "string"},

        # Probe metadata
        {"name": "probe_ip", "type": "string"},
        {"name": "probe_country", "type": "string"},
        {"name": "probe_asn", "type": ["null", "long"]},
        {"name": "probe_lat", "type": ["null", "double"]},
        {"name": "probe_lon", "type": ["null", "double"]},

        # Resolver metadata
        {"name": "resolver_ip", "type": "string"},

        # DNS response
        {"name": "a_records", "type": {"type": "array", "items": "string"}},
        {"name": "ttl", "type": ["null", "long"]},
        {"name": "rcode", "type": "int"},
        {"name": "response_time_ms", "type": ["null", "double"]},

        # Validation
        {"name": "valid", "type": "boolean"},
        {"name": "validation_reason", "type": "string"}
    ]
}
```

**Avantages Avro** :
- Compression efficace : **Ratio 1:7.4** (van Rijswijk-Deij et al., 2016)
- Schéma intégré au fichier (auto-documentation)
- Évolution schéma compatible (ajout champs futurs)
- Splittable (parallélisation Hadoop/Spark)

**Tier 2 - Analytics (Apache Parquet)** :

```python
import pyarrow.parquet as pq
import pandas as pd

# Conversion Avro → Parquet quotidienne
def avro_to_parquet(avro_file, parquet_file):
    """Convertit Avro vers Parquet pour analytics"""
    # Lire Avro
    records = read_avro(avro_file)

    # Convertir en DataFrame
    df = pd.DataFrame(records)

    # Écrire Parquet (columnar, optimisé requêtes)
    df.to_parquet(
        parquet_file,
        engine='pyarrow',
        compression='snappy',  # Balance compression/vitesse
        index=False
    )
```

**Avantages Parquet** :
- Stockage columnar (lecture colonnes sélectives)
- Compatible SQL (Impala, Presto, Athena)
- Compression par colonne (types homogènes)
- Prédicats pushdown (filtrage efficace)

**Organisation fichiers** :

```
data/
├── raw/                          # JSON bruts RIPE Atlas
│   └── 2026-03-21/
│       └── 123456789.json
│
├── avro/                         # Archives long terme
│   └── 2026-03/
│       └── dns_measurements_2026-03-21.avro
│
├── parquet/                      # Analytics
│   └── year=2026/
│       └── month=03/
│           └── day=21/
│               └── measurements.parquet
│
└── metadata/                     # Métadonnées
    ├── tranco_lists/
    │   └── tranco_2026-03-21_10K.csv
    └── probe_inventory/
        └── probes_2026-03-21.json
```

**Partitionnement** : Parquet partitionné par date (Hive-style) pour :
- Requêtes temporelles efficaces (filtrage par date)
- Gestion incrémentale (ajout journalier)
- Suppression sélective (GDPR, retention policies)

**Estimation volumes** (Top 10K, 100 sondes, 90 jours) :

| Format | Taille/jour | Taille 90j | Compression |
|--------|-------------|------------|-------------|
| **JSON brut** | ~2 GB | ~180 GB | 1:1 (baseline) |
| **Avro** | ~270 MB | ~24 GB | **1:7.4** |
| **Parquet** | ~200 MB | ~18 GB | **1:10** |

**Total stockage requis** : ~220 GB (JSON + Avro + Parquet) pour 3 mois de données.

---

## 3.5 Analyse des données

### 3.5.1 Question Q1 : Diversité géographique des réponses

**Objectif** : Quantifier la proportion de domaines Tranco Top 10K retournant des réponses DNS différentes selon la localisation géographique.

**Méthode d'analyse** :

**Étape 1 - Groupement par domaine et par jour** :

```python
import pandas as pd

# Charger données Parquet
df = pd.read_parquet('data/parquet/year=2026/month=03/')

# Grouper par domaine + jour
daily_diversity = df.groupby(['domain', 'date']).agg({
    'a_records': lambda x: len(set(flatten(x))),  # Nombre IPs uniques
    'probe_country': 'nunique',                    # Nombre pays uniques
    'probe_asn': 'nunique',                        # Nombre AS uniques
    'prb_id': 'count'                              # Nombre sondes
}).reset_index()

daily_diversity.columns = [
    'domain', 'date',
    'unique_ips', 'unique_countries', 'unique_asns', 'num_probes'
]
```

**Étape 2 - Classification domaines** :

```python
def classify_domain_diversity(row):
    """Classifie domaine selon diversité géographique"""
    if row['unique_ips'] == 1:
        return "SINGLE_IP"       # Pas de diversité (1 seule IP globalement)

    elif row['unique_ips'] <= 5:
        return "LOW_DIVERSITY"   # Diversité faible (2-5 IPs)

    elif row['unique_ips'] <= 20:
        return "MEDIUM_DIVERSITY"  # Diversité moyenne (6-20 IPs)

    else:
        return "HIGH_DIVERSITY"  # Diversité élevée (>20 IPs)

daily_diversity['diversity_class'] = daily_diversity.apply(
    classify_domain_diversity, axis=1
)
```

**Étape 3 - Analyse statistique** :

```python
# Distribution par catégorie
diversity_distribution = daily_diversity.groupby('diversity_class').agg({
    'domain': 'nunique'
}).reset_index()

diversity_distribution['percentage'] = (
    diversity_distribution['domain'] / 10000 * 100
)

print(diversity_distribution)
# Résultat attendu (hypothétique) :
# diversity_class     | domain | percentage
# --------------------|--------|------------
# SINGLE_IP           | 3500   | 35%
# LOW_DIVERSITY       | 2500   | 25%
# MEDIUM_DIVERSITY    | 2000   | 20%
# HIGH_DIVERSITY      | 2000   | 20%
```

**Étape 4 - Corrélation géographique** :

Pour chaque domaine classifié "diversité élevée", analyser si les IPs différentes correspondent à des localisations géographiques différentes :

```python
def analyze_geo_correlation(domain_data):
    """Analyse corrélation géographie ↔ IP retournée"""

    # Grouper par pays
    by_country = domain_data.groupby('probe_country')['a_records'].apply(
        lambda x: set(flatten(x))
    )

    # Calculer diversité inter-pays vs intra-pays
    inter_country_diversity = len(set.union(*by_country.values))
    intra_country_diversity = by_country.apply(len).mean()

    # Ratio : élevé = diversité principalement inter-pays (CDN géo-distribué)
    #         faible = diversité même au sein d'un pays (round-robin, anycast)
    ratio = inter_country_diversity / max(intra_country_diversity, 1)

    return {
        'inter_country_ips': inter_country_diversity,
        'avg_intra_country_ips': intra_country_diversity,
        'geo_correlation_ratio': ratio
    }
```

**Hypothèse** : Domaines avec CDN géo-distribués (Akamai, Cloudflare) auront ratio élevé (>5), domaines avec anycast auront ratio faible (<2).

**Métriques finales Q1** :
- **% domaines SINGLE_IP** (pas de diversité géographique)
- **% domaines HIGH_DIVERSITY** (forte diversité géographique)
- **Corrélation géographie ↔ IP** (CDN vs anycast)
- **Providers dominants** (Cloudflare, Akamai, AWS, Google, etc.)

### 3.5.2 Question Q2 : Stabilité temporelle

**Objectif** : Quantifier la stabilité temporelle des enregistrements DNS sur différentes échelles (jour, semaine, mois).

**Méthode d'analyse** :

**Étape 1 - Calcul taux de changement** :

```python
def compute_change_rate(domain_data, timeframe='day'):
    """Calcule taux changement IPs pour un domaine"""

    # Trier par timestamp
    domain_data = domain_data.sort_values('timestamp')

    # Grouper par timeframe
    if timeframe == 'day':
        domain_data['period'] = domain_data['timestamp'].dt.date
    elif timeframe == 'week':
        domain_data['period'] = domain_data['timestamp'].dt.isocalendar().week
    elif timeframe == 'month':
        domain_data['period'] = domain_data['timestamp'].dt.month

    # Pour chaque période, extraire set d'IPs uniques
    period_ips = domain_data.groupby('period')['a_records'].apply(
        lambda x: set(flatten(x))
    )

    # Calculer Jaccard similarity entre périodes consécutives
    similarities = []
    for i in range(len(period_ips) - 1):
        ips_t = period_ips.iloc[i]
        ips_t1 = period_ips.iloc[i + 1]

        jaccard = len(ips_t & ips_t1) / len(ips_t | ips_t1)
        similarities.append(jaccard)

    # Taux changement = 1 - similarité moyenne
    change_rate = 1 - (sum(similarities) / len(similarities))

    return {
        'change_rate': change_rate,
        'avg_jaccard_similarity': 1 - change_rate,
        'num_periods': len(period_ips)
    }
```

**Étape 2 - Classification stabilité** :

```python
def classify_stability(change_rate):
    """Classifie stabilité selon taux de changement"""
    if change_rate < 0.05:
        return "VERY_STABLE"      # <5% changement
    elif change_rate < 0.20:
        return "STABLE"           # 5-20% changement
    elif change_rate < 0.50:
        return "MODERATE"         # 20-50% changement
    else:
        return "VOLATILE"         # >50% changement
```

**Étape 3 - Analyse par échelle temporelle** :

```python
# Analyser chaque domaine sur 3 échelles
results = []

for domain in df['domain'].unique():
    domain_data = df[df['domain'] == domain]

    daily = compute_change_rate(domain_data, timeframe='day')
    weekly = compute_change_rate(domain_data, timeframe='week')
    monthly = compute_change_rate(domain_data, timeframe='month')

    results.append({
        'domain': domain,
        'daily_change_rate': daily['change_rate'],
        'weekly_change_rate': weekly['change_rate'],
        'monthly_change_rate': monthly['change_rate'],
        'daily_stability': classify_stability(daily['change_rate']),
        'weekly_stability': classify_stability(weekly['change_rate']),
        'monthly_stability': classify_stability(monthly['change_rate'])
    })

stability_df = pd.DataFrame(results)
```

**Étape 4 - Corrélation avec TTL** :

Analyser si les domaines avec TTL courts changent plus fréquemment (hypothèse : TTL court = anticipation de changements) :

```python
# Calculer TTL moyen par domaine
ttl_by_domain = df.groupby('domain')['ttl'].median()

# Merger avec taux changement
stability_ttl = stability_df.merge(
    ttl_by_domain,
    left_on='domain',
    right_index=True
)

# Corrélation Spearman (non-paramétrique)
from scipy.stats import spearmanr

corr, pvalue = spearmanr(
    stability_ttl['ttl'],
    stability_ttl['daily_change_rate']
)

print(f"Corrélation TTL ↔ Change Rate: {corr:.3f} (p={pvalue:.3e})")
```

**Hypothèse** : Corrélation négative attendue (TTL court → changements fréquents).

**Métriques finales Q2** :
- **Distribution stabilité** (% domaines very stable, stable, moderate, volatile)
- **Taux de changement moyen** par échelle temporelle (jour, semaine, mois)
- **Corrélation TTL ↔ changement** (coefficient Spearman + p-value)
- **Top 10 domaines les plus volatiles** (cas d'étude)

### 3.5.3 Question Q3 : Impact biais géographiques RIPE Atlas

**Objectif** : Évaluer si le biais géographique RIPE Atlas (91% sondes en Europe + Amérique du Nord) impacte significativement l'observation de la diversité.

**Méthode d'analyse** :

**Étape 1 - Sous-échantillonnage contrôlé** :

```python
def subsample_by_region(df, sampling_strategy):
    """Sous-échantillonne sondes selon stratégie"""

    if sampling_strategy == "ACTUAL":
        # Distribution actuelle RIPE Atlas (baseline)
        return df

    elif sampling_strategy == "UNIFORM":
        # Distribution uniforme entre régions
        regions = df['probe_region'].unique()
        n_per_region = len(df) // len(regions)

        sampled = []
        for region in regions:
            region_data = df[df['probe_region'] == region]
            sampled.append(region_data.sample(n=min(n_per_region, len(region_data))))

        return pd.concat(sampled)

    elif sampling_strategy == "EUROPE_NA_ONLY":
        # Seulement Europe + Amérique du Nord (91%)
        return df[df['probe_region'].isin(['Europe', 'North America'])]
```

**Étape 2 - Comparaison diversité observée** :

```python
# Trois stratégies de sampling
strategies = ["ACTUAL", "UNIFORM", "EUROPE_NA_ONLY"]

comparison_results = []

for strategy in strategies:
    sampled_df = subsample_by_region(df, strategy)

    # Recalculer diversité pour chaque domaine
    diversity = sampled_df.groupby('domain').agg({
        'a_records': lambda x: len(set(flatten(x)))
    }).reset_index()

    diversity.columns = ['domain', 'unique_ips']
    diversity['strategy'] = strategy

    comparison_results.append(diversity)

comparison_df = pd.concat(comparison_results)
```

**Étape 3 - Test statistique** :

```python
from scipy.stats import wilcoxon

# Comparer distributions ACTUAL vs UNIFORM
actual = comparison_df[comparison_df['strategy'] == 'ACTUAL']['unique_ips']
uniform = comparison_df[comparison_df['strategy'] == 'UNIFORM']['unique_ips']

# Test Wilcoxon (données appariées)
statistic, pvalue = wilcoxon(actual, uniform)

print(f"Wilcoxon test ACTUAL vs UNIFORM: p={pvalue:.3e}")
if pvalue < 0.05:
    print("→ Différence SIGNIFICATIVE (biais impact la diversité)")
else:
    print("→ Différence NON significative (biais négligeable)")
```

**Étape 4 - Analyse par région** :

Identifier quelles régions apportent le plus de diversité unique :

```python
def region_contribution(df):
    """Calcule contribution unique de chaque région"""

    results = []

    for domain in df['domain'].unique():
        domain_data = df[df['domain'] == domain]

        # IPs totales
        all_ips = set(flatten(domain_data['a_records']))

        # Pour chaque région
        for region in domain_data['probe_region'].unique():
            region_data = domain_data[domain_data['probe_region'] == region]
            region_ips = set(flatten(region_data['a_records']))

            # IPs uniques à cette région (pas vues ailleurs)
            other_regions = domain_data[domain_data['probe_region'] != region]
            other_ips = set(flatten(other_regions['a_records']))
            unique_ips = region_ips - other_ips

            results.append({
                'domain': domain,
                'region': region,
                'total_ips': len(region_ips),
                'unique_ips': len(unique_ips),
                'contribution_ratio': len(unique_ips) / len(all_ips)
            })

    return pd.DataFrame(results)

region_contrib = region_contribution(df)

# Moyenne par région
region_avg = region_contrib.groupby('region').agg({
    'contribution_ratio': 'mean',
    'unique_ips': 'sum'
}).sort_values('contribution_ratio', ascending=False)

print(region_avg)
```

**Hypothèse** : Si Asie/Afrique/Am. Sud apportent >10% IPs uniques malgré <10% sondes → biais significatif.

**Métriques finales Q3** :
- **Test Wilcoxon p-value** (ACTUAL vs UNIFORM)
- **Contribution unique par région** (% IPs uniques apportées)
- **Domaines affectés** (% domaines où biais change classification diversité)
- **Recommandations** (régions prioritaires pour futures sondes)

### 3.5.4 Question Q4 : Impact du choix de resolver

**Objectif** : Quantifier l'impact du choix de resolver (ISP local vs DNS public) sur les adresses IP observées.

**Méthode d'analyse** :

**Étape 1 - Classification des resolvers** :

```python
# Définir DNS publics connus
PUBLIC_DNS_PROVIDERS = {
    '8.8.8.8': 'Google DNS',
    '8.8.4.4': 'Google DNS',
    '1.1.1.1': 'Cloudflare DNS',
    '1.0.0.1': 'Cloudflare DNS',
    '9.9.9.9': 'Quad9',
    '208.67.222.222': 'OpenDNS',
    # ... (liste complète)
}

def classify_resolver(resolver_ip):
    """Classifie resolver comme public ou ISP local"""
    if resolver_ip in PUBLIC_DNS_PROVIDERS:
        return "PUBLIC", PUBLIC_DNS_PROVIDERS[resolver_ip]
    else:
        return "ISP_LOCAL", None

df['resolver_type'], df['resolver_provider'] = zip(
    *df['resolver_ip'].apply(classify_resolver)
)
```

**Étape 2 - Comparaison IPs retournées** :

```python
def compare_resolver_responses(domain_data):
    """Compare IPs retournées selon type resolver"""

    # Grouper par type resolver
    by_resolver_type = domain_data.groupby('resolver_type')['a_records'].apply(
        lambda x: set(flatten(x))
    )

    if len(by_resolver_type) < 2:
        return None  # Pas assez de types pour comparer

    public_ips = by_resolver_type.get('PUBLIC', set())
    isp_ips = by_resolver_type.get('ISP_LOCAL', set())

    # Métriques
    overlap = len(public_ips & isp_ips)
    public_only = len(public_ips - isp_ips)
    isp_only = len(isp_ips - public_ips)

    jaccard = overlap / len(public_ips | isp_ips) if len(public_ips | isp_ips) > 0 else 0

    return {
        'overlap': overlap,
        'public_only': public_only,
        'isp_only': isp_only,
        'jaccard_similarity': jaccard,
        'total_public_ips': len(public_ips),
        'total_isp_ips': len(isp_ips)
    }

# Analyser chaque domaine
resolver_impact = []

for domain in df['domain'].unique():
    domain_data = df[df['domain'] == domain]
    result = compare_resolver_responses(domain_data)

    if result:
        result['domain'] = domain
        resolver_impact.append(result)

resolver_impact_df = pd.DataFrame(resolver_impact)
```

**Étape 3 - Analyse ECS (EDNS Client Subnet)** :

Les DNS publics supportant ECS (Google, Cloudflare) devraient retourner IPs similaires aux ISP locaux. Vérifier cette hypothèse :

```python
# Classifier resolvers selon support ECS
ECS_PROVIDERS = {'Google DNS', 'Cloudflare DNS', 'OpenDNS'}

df['resolver_supports_ecs'] = df['resolver_provider'].isin(ECS_PROVIDERS)

# Comparer similitude selon support ECS
ecs_analysis = df.groupby(['domain', 'resolver_supports_ecs']).apply(
    lambda x: set(flatten(x['a_records']))
).reset_index()

ecs_analysis.columns = ['domain', 'ecs_support', 'ips']

# Calculer Jaccard entre ECS=True et ISP local
# ...
```

**Hypothèse** : Resolvers ECS devraient avoir Jaccard similarity >0.8 avec ISP local (Wang et al., 2018).

**Étape 4 - Impact performance** :

Comparer RTT (response time) selon type resolver :

```python
# Comparaison RTT
rtt_comparison = df.groupby('resolver_type')['response_time_ms'].agg([
    'mean', 'median', 'std',
    ('p95', lambda x: x.quantile(0.95))
])

print(rtt_comparison)

# Test Mann-Whitney U (non-paramétrique)
from scipy.stats import mannwhitneyu

public_rtt = df[df['resolver_type'] == 'PUBLIC']['response_time_ms']
isp_rtt = df[df['resolver_type'] == 'ISP_LOCAL']['response_time_ms']

statistic, pvalue = mannwhitneyu(public_rtt, isp_rtt)

print(f"Mann-Whitney U test RTT: p={pvalue:.3e}")
```

**Métriques finales Q4** :
- **Jaccard similarity moyenne** (public vs ISP local)
- **% domaines divergence significative** (Jaccard <0.5)
- **Impact ECS** (similitude ECS-enabled vs ISP local)
- **RTT comparison** (public vs ISP local, test statistique)
- **Providers CDN affectés** (Akamai, Cloudflare, AWS, etc.)

---

## 3.6 Éthique et reproductibilité

### 3.6.1 Considérations éthiques

**Conformité RIPE Atlas Ethics Guidelines** :

Nous suivons les recommandations officielles (https://labs.ripe.net/author/kistel/ethics-of-ripe-atlas-measurements/) :

**1. Minimiser l'impact sur les serveurs DNS cibles** :
- Fréquence mesures : 1×/jour maximum (vs horaire ou minute)
- Pas de mesures vers domaines sensibles sans consentement
- Respecter TTL : pas de requêtes plus fréquentes que 1/TTL

**2. Transparence et consentement** :
- Descriptions mesures claires (tags, descriptions)
- Publication méthodologie complète (ce chapitre)
- Measurement IDs inclus dans publications (reproductibilité)

**3. Respect de la vie privée** :
- Anonymisation données si publication publique
- Pas de corrélation sondes ↔ utilisateurs individuels
- Agrégation statistique (pas de données par sonde individuellement)

**4. Utilisation responsable crédits** :
- Vérification mesures existantes avant lancement
- Arrêt mesures si objectif atteint avant terme
- Partage données collectées avec communauté (contribution)

### 3.6.2 Reproductibilité scientifique

**Mesures garantissant la reproductibilité** :

**1. Versioning complet** :
```python
# Métadonnées enregistrées pour chaque collecte
metadata = {
    "project": "thesis-dns-geo-diversity",
    "author": "Olivier Gautier",
    "date_start": "2026-03-21",
    "date_end": "2026-06-21",

    # Paramètres mesures
    "tranco_list_id": "8QNZ",  # Permalink Tranco
    "tranco_size": 10000,
    "num_probes": 100,
    "measurement_frequency": "daily",

    # RIPE Atlas measurement IDs
    "msm_ids": [123456789, 123456790, ...],

    # Software versions
    "python_version": "3.11.5",
    "dnspython_version": "2.4.2",
    "pandas_version": "2.1.3",

    # Code repository
    "github_repo": "https://github.com/ogautier1980/dns-measures",
    "commit_sha": "e879f1d8a4b2..."
}
```

**2. Documentation complète** :
- README.md détaillé (instructions reproduction)
- Notebooks Jupyter annotés (analyses intermédiaires)
- Code commenté (docstrings Python)
- Schémas Avro versionnés

**3. Données archivées** :
- Format Avro (auto-documenté, schéma intégré)
- Métadonnées préservées (provenance, versioning)
- Checksums SHA-256 (intégrité données)

**4. Partage données** :
- Zenodo DOI (archivage permanent)
- Licence Creative Commons BY 4.0
- Formats ouverts (Avro, Parquet, CSV)

### 3.6.3 Conformité FAIR principles

Les données collectées respectent les principes FAIR :

**Findable** :
- DOI Zenodo permanent
- Métadonnées riches (Dublin Core)
- Indexation dans registres scientifiques

**Accessible** :
- Accès public gratuit (après publication mémoire)
- Protocole standard HTTP/HTTPS
- Formats ouverts non-propriétaires

**Interoperable** :
- Vocabulaire standard (RFC DNS)
- Formats standardisés (Avro, Parquet)
- APIs RESTful (documentation OpenAPI)

**Reusable** :
- Licence claire (CC BY 4.0)
- Provenance documentée (métadonnées)
- Qualité garantie (validation, filtres)

---

## 3.7 Timeline et jalons du projet

### 3.7.1 Phases du projet

**Phase 1 : Familiarisation et conception** (4 semaines)
- ✅ Lecture articles fondamentaux (2 semaines)
- ✅ Conception système et méthodologie (2 semaines)
- **Livrable** : Chapitre 2 (État de l'art) + Chapitre 3 (Méthodologie)

**Phase 2 : Développement et tests** (3 semaines)
- Implémentation pipeline collecte (1 semaine)
- Tests pilotes RIPE Atlas (500 domaines, 10 sondes, 7 jours)
- Développement pipeline parsing/stockage (1 semaine)
- Validation qualité données (1 semaine)
- **Livrable** : Code fonctionnel + validation technique

**Phase 3 : Collecte données** (12 semaines = 3 mois)
- Mesures quotidiennes automatisées
- Monitoring consommation crédits
- Ajustements si nécessaire
- **Livrable** : Dataset complet (90M résultats)

**Phase 4 : Analyse et interprétation** (4 semaines)
- Analyses Q1-Q4 (2 semaines)
- Génération visualisations (1 semaine)
- Interprétation résultats (1 semaine)
- **Livrable** : Chapitre 4 (Résultats)

**Phase 5 : Rédaction et finalisation** (3 semaines)
- Discussion et conclusion (1 semaine)
- Révision complète mémoire (1 semaine)
- Préparation défense (1 semaine)
- **Livrable** : Mémoire final + présentation

**Durée totale** : ~26 semaines (6 mois)

### 3.7.2 Critères de succès

**Technique** :
- ✅ Collecte ≥85% résultats valides (filtrage <15%)
- ✅ Couverture ≥95% domaines Tranco Top 10K
- ✅ Distribution géographique ≥4 continents
- ✅ Données conformes FAIR principles

**Scientifique** :
- ✅ Réponses aux 4 questions de recherche (Q1-Q4)
- ✅ Contribution originale (diversité géographique + temporelle)
- ✅ Validation statistique (p-values, tests robustes)
- ✅ Comparaison littérature existante

**Académique** :
- ✅ Mémoire complet (5 chapitres)
- ✅ Reproductibilité garantie (code + données)
- ✅ Respect éthique et déontologie
- ✅ Défense publique réussie

---

**Fin du Chapitre 3 - Méthodologie**
