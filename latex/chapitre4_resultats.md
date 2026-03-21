# Chapitre 4 - Résultats

## 4.1 Vue d'ensemble du dataset collecté

### 4.1.1 Statistiques générales de collecte

**Période de collecte** : [DATE_DEBUT] - [DATE_FIN] (X jours)

**Domaines mesurés** :
- Nombre total de domaines Tranco : 10,000
- Domaines après filtrage (responsiveness + safe browsing) : X,XXX
- Domaines avec ≥85% résultats valides : X,XXX

**Mesures effectuées** :
- Nombre total de mesures lancées : X,XXX,XXX
- Nombre total de résultats collectés : XX,XXX,XXX
- Taux de succès global : XX.X%

**Distribution temporelle** :
- Mesures quotidiennes réussies : XX/XX jours
- Interruptions : [Aucune / X jours avec collecte partielle]
- Décalage scheduling moyen : ±XX minutes

**Sondes RIPE Atlas utilisées** :
- Nombre de sondes uniques : XXX
- Distribution géographique :
  - Europe : XX sondes (XX%)
  - Amérique du Nord : XX sondes (XX%)
  - Asie : XX sondes (XX%)
  - Amérique du Sud : XX sondes (XX%)
  - Afrique : XX sondes (XX%)
  - Océanie : XX sondes (XX%)

### 4.1.2 Qualité des données

**Filtrage et validation** :

| Filtre appliqué | Résultats exclus | Pourcentage | Raison |
|-----------------|------------------|-------------|--------|
| Pas de résultat | XXX,XXX | X.X% | Sonde offline, network issue |
| RCODE ≠ NOERROR | XXX,XXX | X.X% | NXDOMAIN, SERVFAIL |
| Lying resolvers | XXX,XXX | X.X% | Réponses anormales |
| Timing >4h | XXX,XXX | X.X% | Scheduling interference extrême |
| **Total exclusions** | **XXX,XXX** | **XX.X%** | - |
| **Résultats valides** | **XX,XXX,XXX** | **XX.X%** | Utilisés dans analyses |

**Distribution des codes de réponse DNS** :

```
NOERROR (0):     XX.X%
NXDOMAIN (3):    X.X%
SERVFAIL (2):    X.X%
REFUSED (5):     X.X%
Autres:          X.X%
```

### 4.1.3 Volume de données stockées

**Stockage** :

| Format | Taille brute | Taille compressée | Ratio compression |
|--------|--------------|-------------------|-------------------|
| JSON (raw RIPE Atlas) | XXX GB | - | - |
| Apache Avro | XXX GB | XX GB | 1:X.X |
| Apache Parquet | XXX GB | XX GB | 1:X.X |
| **Total** | **XXX GB** | **XX GB** | **1:X.X** |

---

## 4.2 Résultats Question Q1 : Diversité géographique

### 4.2.1 Distribution globale de la diversité

**Question** : Quelle proportion de domaines Tranco Top 10K retourne des réponses DNS différentes selon la localisation géographique ?

**Méthode** : Classification de chaque domaine selon le nombre d'adresses IP uniques observées à travers tous les vantage points.

**Résultats** :

| Catégorie | Nombre domaines | Pourcentage | Nombre IPs moyen |
|-----------|-----------------|-------------|------------------|
| SINGLE_IP (1 IP unique) | X,XXX | XX.X% | 1.0 |
| LOW_DIVERSITY (2-5 IPs) | X,XXX | XX.X% | X.X |
| MEDIUM_DIVERSITY (6-20 IPs) | X,XXX | XX.X% | XX.X |
| HIGH_DIVERSITY (>20 IPs) | X,XXX | XX.X% | XX.X |
| **TOTAL** | **X,XXX** | **100%** | **X.X** |

**Figure 4.1** : Distribution de la diversité géographique DNS
[TODO: Graphique en barres - Catégories vs Nombre de domaines]

**Interprétation** :
- XX.X% des domaines populaires présentent une diversité géographique (≥2 IPs)
- XX.X% utilisent CDN ou infrastructure distribuée (MEDIUM + HIGH)
- XX.X% n'ont aucune diversité géographique observable

### 4.2.2 Corrélation géographie ↔ IP retournée

**Méthode** : Pour chaque domaine HIGH_DIVERSITY, calcul du ratio de corrélation géographique (inter-country diversity / intra-country diversity).

**Résultats** :

**Figure 4.2** : Distribution ratio corrélation géographique
[TODO: Histogramme - Ratio géo-corrélation (0-10)]

| Catégorie | Nombre domaines | Interprétation |
|-----------|-----------------|----------------|
| Ratio <2 (faible) | XXX | Anycast ou round-robin global |
| Ratio 2-5 (moyen) | XXX | CDN partiel ou régional |
| Ratio >5 (élevé) | XXX | CDN géo-distribué complet |

**Cas d'étude - Domaines HIGH_DIVERSITY** :

**Exemple 1 : [domaine-cdn.com]**
- Nombre IPs uniques : XX
- Ratio géo-corrélation : X.X
- Provider CDN : [Cloudflare / Akamai / AWS / etc.]
- Interprétation : [CDN géo-distribué classique]

**Exemple 2 : [domaine-anycast.com]**
- Nombre IPs uniques : XX
- Ratio géo-corrélation : X.X
- Provider : [...]
- Interprétation : [Anycast avec inflation géographique]

### 4.2.3 Providers CDN et infrastructure

**Distribution des providers** :

| Provider | Domaines | Pourcentage | IPs moyennes |
|----------|----------|-------------|--------------|
| Cloudflare | XXX | XX.X% | XX.X |
| Akamai | XXX | XX.X% | XX.X |
| Amazon CloudFront | XXX | XX.X% | XX.X |
| Google Cloud CDN | XXX | XX.X% | XX.X |
| Fastly | XXX | XX.X% | XX.X |
| Autres | XXX | XX.X% | XX.X |
| Non-identifié | XXX | XX.X% | X.X |

**Figure 4.3** : Part de marché CDN (domaines Tranco Top 10K)
[TODO: Camembert - Distribution providers]

**Observation** : [Les X providers dominants capturent XX% des domaines avec diversité géographique]

---

## 4.3 Résultats Question Q2 : Stabilité temporelle

### 4.3.1 Taux de changement par échelle temporelle

**Question** : Quelle est la stabilité temporelle des enregistrements DNS pour les domaines Tranco Top 10K ?

**Méthode** : Calcul du taux de changement (1 - similarité Jaccard) entre périodes consécutives (jour, semaine, mois).

**Résultats globaux** :

| Échelle temporelle | Taux changement moyen | Écart-type | Médiane |
|--------------------|----------------------|------------|---------|
| Quotidienne (J → J+1) | X.X% | X.X% | X.X% |
| Hebdomadaire (S → S+1) | XX.X% | XX.X% | X.X% |
| Mensuelle (M → M+1) | XX.X% | XX.X% | XX.X% |

**Figure 4.4** : Distribution taux de changement quotidien
[TODO: Histogramme - Taux changement (0-100%)]

### 4.3.2 Classification stabilité des domaines

**Distribution par catégorie de stabilité** :

| Stabilité | Taux changement | Nombre domaines | Pourcentage |
|-----------|----------------|-----------------|-------------|
| VERY_STABLE | <5% | X,XXX | XX.X% |
| STABLE | 5-20% | X,XXX | XX.X% |
| MODERATE | 20-50% | X,XXX | XX.X% |
| VOLATILE | >50% | XXX | X.X% |

**Figure 4.5** : Stabilité temporelle des domaines
[TODO: Barres empilées - Catégories stabilité par échelle temporelle]

**Observations** :
- XX.X% des domaines sont (very) stable (changements <20%)
- X.X% des domaines sont volatiles (changements >50%)
- La stabilité [augmente / diminue] avec l'échelle temporelle

### 4.3.3 Corrélation TTL ↔ changement

**Hypothèse** : Les domaines avec TTL court changent plus fréquemment.

**Méthode** : Corrélation Spearman entre TTL médian et taux de changement quotidien.

**Résultats** :

```
Corrélation Spearman (TTL ↔ Taux changement quotidien):
  ρ = -X.XXX
  p-value = X.XXe-XX
  Interprétation: [Corrélation négative significative / non-significative]
```

**Figure 4.6** : Scatter plot TTL vs Taux de changement
[TODO: Nuage de points - TTL (log scale) vs Taux changement]

**Interprétation** : [Les domaines avec TTL court (<300s) changent effectivement plus fréquemment, confirmant l'hypothèse / Pas de corrélation significative]

### 4.3.4 Top 10 domaines les plus volatiles

| Rang | Domaine | Taux changement | TTL moyen | Catégorie |
|------|---------|----------------|-----------|-----------|
| 1 | [exemple1.com] | XX.X% | XXXs | [Gaming / Streaming / etc.] |
| 2 | [exemple2.com] | XX.X% | XXXs | [...] |
| ... | ... | ... | ... | ... |
| 10 | [exemple10.com] | XX.X% | XXXs | [...] |

**Analyse qualitative** : [Les domaines les plus volatiles sont principalement des services de streaming, gaming ou infrastructures CDN avec load balancing dynamique]

---

## 4.4 Résultats Question Q3 : Impact biais géographiques

### 4.4.1 Comparaison stratégies de sampling

**Question** : Le biais géographique RIPE Atlas (91% Europe+NA) impacte-t-il significativement l'observation de la diversité ?

**Méthode** : Sous-échantillonnage contrôlé selon 3 stratégies, comparaison diversité observée.

**Résultats - Nombre IPs uniques moyen par domaine** :

| Stratégie | IPs uniques moyen | Écart-type | Médiane |
|-----------|-------------------|------------|---------|
| ACTUAL (baseline) | XX.X | XX.X | X |
| UNIFORM (équilibré) | XX.X | XX.X | X |
| EUROPE_NA_ONLY (91%) | XX.X | XX.X | X |

**Figure 4.7** : Comparaison distributions diversité (3 stratégies)
[TODO: Box plots - Nombre IPs uniques par stratégie]

### 4.4.2 Test statistique

**Test Wilcoxon (données appariées)** :

**ACTUAL vs UNIFORM** :
```
Statistic: XXXXX
p-value: X.XXXe-XX
Conclusion: [Différence significative / non-significative] (α=0.05)
```

**ACTUAL vs EUROPE_NA_ONLY** :
```
Statistic: XXXXX
p-value: X.XXXe-XX
Conclusion: [Différence significative / non-significative] (α=0.05)
```

**Interprétation** : [Le biais géographique RIPE Atlas impacte / n'impacte pas significativement la diversité observée]

### 4.4.3 Contribution unique par région

**Méthode** : Pour chaque région, calcul des IPs uniques non observées depuis autres régions.

**Résultats** :

| Région | Sondes (%) | IPs uniques apportées | Contribution (%) |
|--------|------------|----------------------|------------------|
| Europe | XX% | XXX,XXX | XX.X% |
| Amérique du Nord | XX% | XXX,XXX | XX.X% |
| Asie | XX% | XXX,XXX | XX.X% |
| Amérique du Sud | X% | XX,XXX | XX.X% |
| Afrique | X% | XX,XXX | XX.X% |
| Océanie | X% | XX,XXX | XX.X% |

**Figure 4.8** : Contribution unique par région
[TODO: Barres - Contribution IPs uniques vs % sondes disponibles]

**Observations clés** :
- [Asie / Afrique / Am. Sud] apportent XX.X% d'IPs uniques malgré seulement XX% des sondes
- Ratio contribution/disponibilité le plus élevé : [Région]
- [Interprétation impact biais]

### 4.4.4 Domaines affectés par le biais

**Nombre de domaines changeant de catégorie** :

| Changement catégorie | ACTUAL → UNIFORM | ACTUAL → EUROPE_NA |
|---------------------|------------------|---------------------|
| SINGLE → LOW/MEDIUM | XXX | XXX |
| LOW → MEDIUM/HIGH | XXX | XXX |
| MEDIUM → HIGH | XXX | XXX |
| **Total domaines affectés** | **XXX (X.X%)** | **XXX (X.X%)** |

**Interprétation** : [Le biais affecte la classification de X.X% des domaines, ce qui est acceptable / significatif]

---

## 4.5 Résultats Question Q4 : Impact du choix de resolver

### 4.5.1 Classification des resolvers observés

**Question** : Quel est l'impact du choix de resolver (ISP local vs DNS public) sur les adresses IP observées ?

**Distribution des types de resolvers** :

| Type resolver | Sondes | Pourcentage | Providers principaux |
|---------------|--------|-------------|----------------------|
| ISP local | XXX | XX.X% | [Divers] |
| DNS public | XXX | XX.X% | Google (XX%), Cloudflare (XX%), Quad9 (XX%) |

**Figure 4.9** : Distribution types de resolvers
[TODO: Camembert - ISP local vs DNS publics]

### 4.5.2 Similarité IPs retournées (Public vs ISP)

**Méthode** : Pour chaque domaine, calcul similarité Jaccard entre IPs retournées par resolvers publics vs ISP locaux.

**Résultats globaux** :

| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| Jaccard moyen | X.XXX | [Similarité élevée / moyenne / faible] |
| Médiane | X.XXX | [...] |
| Écart-type | X.XXX | [...] |

**Figure 4.10** : Distribution similarité Public vs ISP
[TODO: Histogramme - Jaccard similarity (0-1)]

**Distribution par seuil** :

| Similarité Jaccard | Nombre domaines | Pourcentage | Interprétation |
|-------------------|-----------------|-------------|----------------|
| >0.8 (très similaire) | X,XXX | XX.X% | Pas de divergence |
| 0.5-0.8 (similaire) | X,XXX | XX.X% | Divergence modérée |
| <0.5 (divergent) | XXX | X.X% | Divergence significative |

### 4.5.3 Impact EDNS Client Subnet (ECS)

**Hypothèse** : Resolvers supportant ECS (Google, Cloudflare) retournent IPs similaires aux ISP locaux.

**Méthode** : Comparaison similarité Jaccard selon support ECS du resolver.

**Résultats** :

| Resolver | Support ECS | Jaccard moyen (vs ISP) | p-value (vs non-ECS) |
|----------|-------------|------------------------|----------------------|
| Google DNS | Oui | X.XXX | X.XXXe-XX |
| Cloudflare DNS | Oui | X.XXX | X.XXXe-XX |
| Quad9 | Non | X.XXX | - |
| Autres publics | Variable | X.XXX | - |

**Figure 4.11** : Similarité selon support ECS
[TODO: Box plots - Jaccard similarity (ECS-enabled vs non-ECS)]

**Test Mann-Whitney U** :
```
ECS-enabled vs non-ECS (similarité avec ISP):
  Statistic: XXXXX
  p-value: X.XXXe-XX
  Conclusion: [ECS améliore / n'améliore pas] significativement la similarité
```

**Interprétation** : [L'hypothèse selon laquelle ECS permet aux DNS publics de retourner des IPs similaires aux ISP locaux est validée / invalidée]

### 4.5.4 Comparaison RTT (temps de réponse)

**Méthode** : Comparaison RTT (response time) DNS selon type de resolver.

**Résultats** :

| Resolver type | RTT moyen (ms) | Médiane (ms) | P95 (ms) | Écart-type |
|---------------|---------------|--------------|----------|------------|
| ISP local | XX.X | XX.X | XXX.X | XX.X |
| DNS public | XX.X | XX.X | XXX.X | XX.X |

**Figure 4.12** : Distribution RTT selon type resolver
[TODO: Violin plots - RTT (ms) ISP vs Public]

**Test Mann-Whitney U** :
```
ISP local vs DNS public (RTT):
  Statistic: XXXXX
  p-value: X.XXXe-XX
  Conclusion: [Différence significative / non-significative]
  Effet: Les DNS publics sont [plus rapides / plus lents] de XX.X ms en moyenne
```

### 4.5.5 Providers CDN affectés

**Domaines avec divergence significative (Jaccard <0.5) par provider** :

| Provider CDN | Domaines divergents | % du total provider | IPs moyennes (ISP) | IPs moyennes (Public) |
|--------------|---------------------|---------------------|-------------------|----------------------|
| Cloudflare | XXX | XX.X% | XX.X | XX.X |
| Akamai | XXX | XX.X% | XX.X | XX.X |
| Amazon CloudFront | XXX | XX.X% | XX.X | XX.X |
| Google Cloud CDN | XXX | XX.X% | XX.X | XX.X |

**Interprétation** : [Certains providers CDN sont plus sensibles au choix de resolver que d'autres, suggérant des stratégies de redirection DNS différentes]

---

## 4.6 Synthèse des résultats

### 4.6.1 Réponses aux questions de recherche

**Q1 : Diversité géographique**
- **Résultat** : XX.X% des domaines Tranco Top 10K présentent une diversité géographique
- **Détail** : XX.X% utilisent CDN géo-distribué, XX.X% anycast, XX.X% pas de diversité
- **Implication** : [Mesurer DNS depuis un point unique perd XX% de l'information]

**Q2 : Stabilité temporelle**
- **Résultat** : Taux de changement moyen quotidien = X.X%
- **Détail** : XX.X% domaines (very) stable, X.X% volatiles
- **Implication** : [Mesures quotidiennes suffisantes / nécessaires pour la majorité des domaines]

**Q3 : Biais géographiques**
- **Résultat** : [Biais RIPE Atlas impacte / n'impacte pas significativement] (p=X.XXe-XX)
- **Détail** : XX.X% domaines changent de catégorie avec sampling uniforme
- **Implication** : [Résultats généralisables / nécessitent prudence interprétation]

**Q4 : Impact resolver**
- **Résultat** : Similarité moyenne Public vs ISP = X.XXX
- **Détail** : ECS [améliore / n'améliore pas] significativement similarité (p=X.XXe-XX)
- **Implication** : [Choix resolver impacte modérément / fortement les observations]

### 4.6.2 Résultats inattendus

[À compléter après analyse des données réelles]

**Résultat inattendu 1** : [Description]
- **Observation** : [...]
- **Interprétation** : [...]

**Résultat inattendu 2** : [Description]
- **Observation** : [...]
- **Interprétation** : [...]

### 4.6.3 Limitations des résultats

**Limitations méthodologiques** :
- Période de collecte limitée (X mois) vs tendances long-terme
- Biais géographique RIPE Atlas (91% Europe+NA)
- Couverture limitée (Top 10K vs millions de domaines)

**Limitations techniques** :
- Interférence mesures RIPE Atlas (désynchronisation ±1h possible)
- Filtrage lying resolvers peut exclure comportements légitimes
- Granularité temporelle quotidienne (pas horaire)

**Limitations d'interprétation** :
- Corrélation ≠ causalité (TTL vs changement)
- Providers CDN non tous identifiés
- Effet ECS difficile à isoler complètement

---

**Fin du Chapitre 4 - Résultats**
