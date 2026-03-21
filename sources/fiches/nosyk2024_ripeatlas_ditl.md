# Fiche de lecture - Day in the Life of RIPE Atlas

**Référence bibliographique** :
Nosyk, Y., Tashiro, M., Lone, Q., Kisteleki, R., Duda, A., & Korczyński, M. (2024). Day in the Life of RIPE Atlas: Operational Insights and Applications in Network Measurements. *arXiv preprint* arXiv:2511.22474v1. https://arxiv.org/html/2511.22474v1

**Thème** : Plateforme de mesures Internet distribuées - RIPE Atlas

**Intérêt pour le mémoire** :
Article récent (2024) analysant l'infrastructure RIPE Atlas que nous utiliserons pour nos mesures DNS géographiquement distribuées. Fournit données opérationnelles, cas d'usage DNS, guidelines best practices, et limitations géographiques à considérer.

---

## Contexte de lecture

**Date de lecture** : 21 janvier 2026
**Section du mémoire** : 2.5 (État de l'art - Plateforme RIPE Atlas)

---

## Contenu de l'article

### Objectif(s) / Question(s) de recherche

**Question principale** : "What operational insights can be gained from analyzing a single day's worth of RIPE Atlas measurements?"

**Objectifs** :
1. Analyser systématiquement les opérations de RIPE Atlas (premier article à le faire)
2. Caractériser types de mesures, distribution géographique, usage réseau
3. Démontrer cas d'usage pratiques avec mesures existantes
4. Fournir guidelines pour utilisation optimale de la plateforme

**Motivation** :
- RIPE Atlas = plateforme majeure de mesures Internet (>12K sondes)
- Littérature existante se concentre sur cas d'usage spécifiques
- Manque d'analyse systématique de l'infrastructure elle-même
- Besoin de guidelines pour utilisation efficace (crédits limités)

### Cadre global d'explication

**Contexte mesures Internet** :
- Internet = infrastructure critique, évolution rapide
- Besoin mesures actives pour cartographie, diagnostic, sécurité
- Plateformes distribuées nécessaires (diversité géographique)
- RIPE Atlas = solution communautaire, ~15 ans d'existence

**RIPE Atlas infrastructure** :
- **Sondes (probes)** : dispositifs légers (~12.9K actifs)
  - Hardware v1-v5 ou software probes
  - Hébergés par volontaires (maisons, organisations)
  - Mesures : ping, traceroute, DNS, TLS, HTTP, NTP
- **Ancres (anchors)** : sondes haute capacité (~810 actifs)
  - Cibles de mesures + sources
  - Hébergées par institutions (ISP, universités, IXP)
  - Mesh complet entre ancres (performance globale)

**Types de mesures** :
1. **User-Defined Measurements (UDM)** : créées par utilisateurs
2. **Anchor Meshes** : mesures automatiques entre toutes les ancres
3. **Built-in Measurements** : DNS root servers, ccTLDs

### Méthodologie

**Type d'étude** : Analyse empirique à grande échelle + case studies

**Période analysée** : 21 février 2024 (24h)
- Choix : métriques dans plage de variance normale
- Snapshot représentatif des opérations typiques

**Données collectées (via API RIPE Atlas)** :
- **Mesures** : 50,885 mesures uniques
- **Résultats** : >1.3 milliards de résultats
- **Infrastructure** : 12,892 sondes + 810 ancres connectées
- **Couverture** : 178 pays

**Métriques analysées** :
- Distribution types de mesures (ping, DNS, traceroute, etc.)
- Distribution géographique (pays, AS, préfixes IP)
- Distribution temporelle (création, scheduling)
- Ratio résultats/mesure
- Support IPv4/IPv6 (dual-stack)

**Outils utilisés** :
- API RIPE Atlas (collecte données)
- MaxMind GeoLite2 (géolocalisation IP)
- Analyses statistiques (Python)

### Résultats principaux

#### 1. Infrastructure et distribution géographique

**Couverture mondiale** :
- 12.9K sondes opérationnelles dans 178 pays
- 810 ancres réparties globalement
- **Biais géographique majeur** :
  - Allemagne + USA = 28% des vantage points
  - 34 pays avec seulement 1 sonde/ancre
  - **Forte concentration Europe + Amérique du Nord**
  - Sous-représentation : Asie, Afrique, Amérique du Sud

**Support IPv6** :
- Sondes publiques : 46.5% dual-stack
- Ancres : 92% dual-stack
- Meilleure adoption ancres (institutions vs particuliers)

**Préfixes IP** :
- 97.84% des préfixes IPv4 = 1 seule ancre
- Concentration faible au niveau préfixe (bonne distribution)

#### 2. Activité de mesure (21 février 2024)

**Distribution par type** :
- Ping : 87.9K mesures (majoritaire)
- DNS : 88K mesures (quasi égalité avec ping)
- Traceroute : fréquent mais pas quantifié exactement
- HTTP, TLS, NTP : minoritaires

**Par catégorie** :
- **User-Defined** : 76.7% des mesures
- **Anchor Meshes** : génère 67.5% des résultats (!)
- **Built-in** : 0.5% des mesures mais 21.1% des résultats

**Ratio efficacité** :
- ~26,000 résultats/mesure en moyenne
- Mesures built-in : très haute densité résultats
- Importance réutiliser mesures existantes (économie crédits)

#### 3. Cas d'usage DNS démontrés

**A) DNS Manipulation Detection**
- Mesures built-in vers root servers
- **Résultat majeur** : Injection réponses DNS
  - **Chine** : 69% des sondes bloquées (services Meta)
  - **Iran** : blocage similaire observé
  - Méthode : DNS response injection (IP incorrectes)
- Démontre utilité mesures géographiquement distribuées

**B) DNSMON**
- 4,435 mesures pour QoS root servers + TLDs
- Utilise réseau de sondes pour diversité géographique
- Surveillance continue disponibilité DNS

#### 4. Autres cas d'usage pertinents

**Traceroute Symmetry** :
- Anchor mesh utilisé pour symétrie chemins
- **Seulement 21%** des traceroutes symétriques (hop count)
- Importance mesures bidirectionnelles

**Reserved Address Space** :
- 1.7M traceroutes contiennent adresses 240/4 non-allouées
- Principalement réseaux Amazon
- Détection via mesures distribuées

**IPv6 RFC Violations** :
- 334K traceroutes (0.35%) avec ::/128 source
- Violation RFC 4291
- Identification automatique via mesures

**Regional Connectivity** :
- Asie Centrale : dépendance forte transit russe/azerbaïdjanais
- Russie : 42.4% à 80.7% du trafic transit (selon pays origine)
- Cartographie dépendances géopolitiques

#### 5. Guidelines et best practices

**Avant de lancer mesures** :
1. ✅ Examiner mesures existantes (API search)
2. ✅ Réutiliser si possible (économie crédits)
3. ✅ Préférer mesures récurrentes vs one-shot multiples
4. ✅ Utiliser tags descriptifs pour retrouvabilité

**Considérations éthiques** :
- ❌ Éviter requêtes domaines sensibles (sans consentement)
- ✅ Respecter Terms & Conditions RIPE Atlas
- ✅ Ne pas surcharger targets
- ✅ Documenter usage recherche

**Reproductibilité** :
- Inclure measurement IDs dans publications
- Utiliser tags systématiques
- Descriptions complètes mesures
- Partager méthodologie sélection sondes

**Optimisation couverture géographique** :
- Identifier régions sous-représentées
- Considérer biais géographique dans interprétation
- Encourager déploiement sondes (régions manquantes)

### Conclusion des auteurs

**Contributions principales** :
1. ✅ **Première analyse systématique** opérations RIPE Atlas
2. ✅ Caractérisation complète infrastructure (12.9K sondes, 178 pays)
3. ✅ Démonstration 5 cas d'usage pratiques (dont DNS manipulation)
4. ✅ Guidelines best practices pour chercheurs
5. ✅ Identification limitations (biais géographique)

**Insights clés** :
- Efficacité mesures existantes (réutilisation > nouvelle mesure)
- Biais géographique Europe/NA à considérer
- Potentiel détection phénomènes sécurité (DNS injection)
- Valeur mesh ancres pour mesures globales

**Limites reconnues** :
- ❌ Analyse limitée à 1 jour (24h)
- ❌ Pas d'analyse longitudinale évolution infrastructure
- ❌ Biais géographique non résolu (limitation structurelle)
- ❌ Pas de comparaison avec autres plateformes (M-Lab, etc.)

**Travaux futurs suggérés** :
- Analyse longitudinale (évolution dans le temps)
- Expansion couverture géographique (Afrique, Asie)
- Comparaison plateformes mesures
- Développement outils détection anomalies automatisée

---

## Analyse personnelle

### Que garder pour le mémoire

**Concepts clés à réutiliser** :
- ✅ Architecture sondes/ancres (distribution charges)
- ✅ Types de mesures disponibles (DNS focus)
- ✅ API RIPE Atlas (utilisation programmatique)
- ✅ Sélection sondes par critères géographiques
- ✅ Concepts dual-stack IPv4/IPv6
- ✅ Mesh measurements (ancres interconnectées)
- ✅ Réutilisation mesures existantes (économie crédits)

**Méthodes applicables** :
- Sélection sondes par pays/AS/préfixe
- Requêtes API systématiques (éviter duplication)
- Tags pour organisation mesures
- Analyse comparative géographique (réponses DNS varient)
- Mesures récurrentes vs one-shot
- Documentation IDs mesures (reproductibilité)

**Chiffres/statistiques importantes** :
- 12.9K sondes actives, 810 ancres (février 2024)
- 178 pays couverts
- Allemagne + USA = 28% des vantage points (biais!)
- 88K mesures DNS quotidiennes (type populaire)
- 69% sondes chinoises bloquées (services Meta)
- 46.5% sondes dual-stack, 92% ancres dual-stack
- ~26,000 résultats par mesure (moyenne)
- 1.3 milliards résultats/jour

**Limites identifiées (à considérer)** :
- ❌ **Biais géographique Europe/NA** ← Impact notre étude!
- ❌ Sous-représentation Asie, Afrique, Am. Sud
- ❌ 34 pays = 1 seule sonde (statistiquement faible)
- ❌ Crédits limités (besoin optimisation)
- ❌ Variabilité sondes (hardware v1-v5, software)

### Critique personnelle

**Forces de l'article** :
- ✅ Premier à analyser systématiquement RIPE Atlas operations
- ✅ Dataset massif (1.3B résultats, 50K mesures)
- ✅ Cas d'usage DNS manipulation très pertinent
- ✅ Guidelines pratiques pour chercheurs
- ✅ Transparence sur limitations (biais géographique)
- ✅ Focus reproductibilité (IDs, tags, descriptions)
- ✅ Publication récente (février 2024 data)
- ✅ Auteurs incluent staff RIPE NCC (expertise directe)

**Faiblesses identifiées** :
- ⚠️ Analyse limitée à 1 jour (pas de tendances temporelles)
- ⚠️ Pas de comparaison avec autres plateformes (M-Lab, CAIDA)
- ⚠️ Pas de discussion coûts crédits RIPE (crucial pour notre projet!)
- ⚠️ Cas DNS manipulation superficiel (manque détails méthodologiques)
- ⚠️ Pas d'analyse impact variabilité hardware sondes
- ⚠️ Biais géographique identifié mais pas de solution proposée
- ⚠️ Pas de discussion représentativité statistique (par région)

**Lien avec autres articles lus** :
- **OpenINTEL (van Rijswijk-Deij 2016)** :
  - OpenINTEL = 1 point de mesure centralisé (Pays-Bas)
  - RIPE Atlas = 12.9K points distribués (178 pays)
  - Complémentarité : OpenINTEL (exhaustivité) vs RIPE Atlas (diversité géographique)
  - Notre contribution : utiliser RIPE Atlas pour ajouter dimension géographique

- **Tranco (Le Pochat 2019)** :
  - Tranco fournit liste domaines stable et non-manipulable
  - RIPE Atlas peut mesurer ces domaines depuis multiples vantages points
  - Combinaison = mesures géographiquement distribuées sur liste fiable
  - Cas d'usage : détecter variations géographiques réponses DNS (CDN, ECS)

**Questions ouvertes** :
1. **Combien de crédits RIPE nécessaires pour notre étude ?**
   → Besoin estimation basée sur nombre domaines Tranco × fréquence × sondes
2. **Comment sélectionner sondes pour maximiser diversité avec crédits limités ?**
   → Stratégie optimisation : pays représentatifs, AS distincts, préfixes variés
3. **Quelle fréquence mesure optimale ?** (quotidien vs hebdo vs mensuel)
4. **Comment gérer biais géographique Europe/NA dans notre analyse ?**
   → Pondération résultats ? Surreprésentation régions sous-représentées ?
5. **Impact variabilité hardware sondes (v1-v5) sur mesures DNS ?**
   → Filtrer anciennes versions ? Accepter hétérogénéité ?
6. **Mesures récurrentes vs one-shot : quel modèle pour nous ?**
   → Dépend durée étude et crédits disponibles
7. **Peut-on réutiliser mesures existantes (DNSMON) ?**
   → Vérifier si domaines Tranco déjà mesurés

### Citations importantes

> "Germany and the United States host substantially more vantage points than any other country, both accounting for 28% of probes and anchors." (Abstract)

> "RIPE Atlas remains underrepresented in other parts of the world." (p. 4)

> "On 2024-02-21, the team examined a single 24 hour period and pulled data from 50,885 measurements from more than 12,000 probes and 810 anchors around the world, generating more than 1.3 billion results." (p. 1)

**Sur DNS measurements** :
> "DNS measurements allow for analysis of how DNS responses vary depending on the geographic area where the probes are located." (Methodology)

> "The great majority of ongoing measurements were user-defined, with most being pings (87.9K) and DNS measurements (88K)." (Results)

**Sur DNS manipulation** :
> "Built-in measurements revealed response injection targeting popular domains in China and Iran, with 69% of probes from China experiencing blocking of Meta services." (Use Cases)

**Sur best practices** :
> "Researchers should examine existing measurements before launching new ones and prefer recurring measurements over multiple one-offs." (Guidelines)

> "Measurement IDs, tags, and comprehensive descriptions should accompany all research publications." (Reproducibility)

**Sur limitations** :
> "34 countries having only one probe or anchor, highlighting a strong bias towards Europe and North America." (Geographic Distribution)

---

## Utilisation dans le mémoire

### Sections concernées

- **Section 2.5** : Plateforme RIPE Atlas (section dédiée)
  Description infrastructure, capabilities, cas d'usage DNS

- **Section 3** : Question de recherche
  Justifier choix RIPE Atlas pour diversité géographique
  Mentionner complémentarité avec OpenINTEL

- **Section 4** : Méthodologie
  Critères sélection sondes (géographie, AS, dual-stack)
  Stratégie optimisation crédits
  API utilization, tags, measurement IDs
  Gestion biais géographique

- **Section 5** : Résultats
  Comparer résultats DNS par région géographique
  Identifier variations géographiques (CDN, ECS, anycast)

- **Section 7** : Discussion
  Limitations biais géographique
  Comparaison OpenINTEL (exhaustivité) vs RIPE Atlas (diversité)
  Guidelines reproductibilité

### Points à développer

**Dans état de l'art** :
- Architecture RIPE Atlas (sondes vs ancres)
- Types de mesures disponibles (focus DNS)
- Couverture géographique (12.9K sondes, 178 pays)
- Biais géographique (28% Europe/NA) → à considérer
- Cas d'usage DNS manipulation (Chine, Iran)
- API capabilities (sélection sondes, tags, scheduling)

**Pour notre méthodologie** :
- **Sélection sondes** :
  - Critères : pays (diversité), AS (indépendance), préfixes IP
  - Équilibrage géographique (compenser biais Europe/NA)
  - Dual-stack préféré (IPv4 + IPv6)
- **Optimisation crédits** :
  - Vérifier mesures existantes (DNSMON, UDM)
  - Mesures récurrentes vs one-shot
  - Nombre sondes vs fréquence (trade-off)
- **Reproductibilité** :
  - Tags systématiques : `thesis-dns-geo`, `tranco-YYYY-MM-DD`
  - Sauvegarder measurement IDs
  - Descriptions détaillées
- **Gestion biais** :
  - Pondération résultats par région
  - Analyse stratifiée (Europe, Asie, Afrique, Am., Océanie)
  - Transparence limitations

**Pour discussion/comparaison** :

| Critère | OpenINTEL | RIPE Atlas | Notre approche |
|---------|-----------|------------|----------------|
| Vantage points | 1 (Pays-Bas) | 12.9K (178 pays) | Multiple (RIPE sondes) |
| Biais géographique | ❌ Aucune diversité | ⚠️ Europe/NA (28%) | ⚠️ Idem (limitation plateforme) |
| Contrôle infra | ✅ Total | ❌ Limité (crédits) | ❌ Limité (crédits alloués) |
| Exhaustivité | ✅ .com complet (123M) | ❌ Échantillon (Tranco) | ❌ Échantillon (Tranco Top 10K?) |
| Diversité géo réponses | ❌ Non | ✅ Oui | ✅ Oui (contribution principale) |
| Fréquence | ✅ Quotidien | ⚠️ Dépend crédits | À définir (hebdo/mensuel?) |
| Reproductibilité | ✅ Data archivées | ✅ IDs permanents | ✅ Via IDs RIPE |
| Coût | Infrastructure dédiée | Crédits RIPE | Crédits alloués |

**Tableau complémentaire - Biais géographique** :

| Région | Représentation RIPE | Impact notre étude |
|--------|---------------------|---------------------|
| Europe | 🟢 Excellent (~40%?) | Statistiques robustes |
| Amérique du Nord | 🟢 Excellent (~28% avec USA) | Statistiques robustes |
| Asie | 🟡 Moyen | Statistiques limitées |
| Afrique | 🔴 Faible | Statistiques faibles |
| Amérique du Sud | 🟡 Moyen | Statistiques limitées |
| Océanie | 🟡 Moyen | Statistiques limitées |

### Références croisées

**Articles à lire ensuite** :
- [X] van Rijswijk-Deij (2016) - OpenINTEL ✅
- [X] Le Pochat (2019) - Tranco ✅
- [ ] Bajpai & Schönwälder (2015) - "A Survey on Internet Performance Measurement Platforms and Related Standardization Efforts" (IEEE)
- [ ] Fontugne et al. (2017) - "Persistent Last-mile Congestion: Not so Uncommon" (IMC)
- [ ] **Rechercher papers combinant Tranco + RIPE Atlas**
- [ ] **Rechercher études DNS avec RIPE Atlas (CDN, anycast, ECS)**
- [ ] RFC 7871 (EDNS Client Subnet)

**Auteurs à suivre** :
- Maciej Korczyński (co-auteur, Grenoble Alpes) - DNS security
- Robert Kisteleki (RIPE NCC staff) - RIPE Atlas expert
- Yevheniya Nosyk (premier auteur) - network measurements
- Chercher leurs publications 2020-2026 sur DNS + RIPE Atlas

**Recherches à effectuer** :
1. IEEE Xplore : `"RIPE Atlas" AND DNS AND (geographic* OR spatial OR CDN)`
2. Google Scholar : `"RIPE Atlas" "DNS measurements" (CDN OR anycast OR ECS)`
3. RIPE Labs blog : articles sur DNS measurements with Atlas
4. arXiv : `"RIPE Atlas" DNS 2020-2026`

---

**Tags** : #ripe-atlas #dns #distributed-measurement #infrastructure #geographic-bias #best-practices #dns-manipulation

**Statut** : [X] Lu / [ ] Relu / [X] Fiché / [ ] Intégré mémoire

**Prochaines étapes** :
1. ✅ Fiche complétée
2. ⏭️ Rechercher articles combinant Tranco + RIPE Atlas
3. ⏭️ Lire documentation officielle RIPE Atlas API
4. ⏭️ Estimer coût crédits pour notre étude (simulation)
5. ⏭️ Chercher études DNS CDN/anycast avec RIPE Atlas
6. ⏭️ Définir stratégie sélection sondes (optimisation géographique)
