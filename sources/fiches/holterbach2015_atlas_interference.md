# Fiche de lecture - Quantifying Interference between Measurements on RIPE Atlas

**Référence bibliographique** :
Holterbach, T., Pelsser, C., Bush, R., & Vanbever, L. (2015). Quantifying Interference between Measurements on the RIPE Atlas Platform. *Proceedings of the 2015 Internet Measurement Conference (IMC '15)*, 437–443. https://doi.org/10.1145/2815675.2815710

**Thème** : Interférence entre mesures simultanées sur RIPE Atlas

**Intérêt pour le mémoire** :
Article critique pour comprendre les limitations des mesures RIPE Atlas lorsque plusieurs utilisateurs lancent des mesures en parallèle. Impact direct sur la fiabilité des résultats DNS que nous allons collecter et sur la conception de notre stratégie de mesure.

---

## Contexte de lecture

**Date de lecture** : 21 janvier 2026
**Section du mémoire** : 2.5 (État de l'art - RIPE Atlas et mesures distribuées)

---

## Contenu de l'article

### Objectif(s) / Question(s) de recherche

**Question principale** : "Do measurements launched by others impact my results?"

**Objectif** : Mesurer l'impact des mesures concurrentes lancées par différents utilisateurs sur la précision et la synchronisation des résultats RIPE Atlas.

**Motivation** :
- Plateformes de mesures publiques (RIPE Atlas) = hardware low-end
- Permettent mesures concurrentes entre utilisateurs (scalabilité)
- Besoin de quantifier l'interférence pour évaluer fiabilité résultats
- Impact sur recherche académique utilisant ces plateformes

### Cadre global d'explication

**Context RIPE Atlas** :
- Plateforme de mesures Internet distribuée
- Sondes = dispositifs hardware limités (CPU, mémoire)
- Multiples utilisateurs lancent mesures simultanément
- Modèle communautaire = partage des ressources

**Types d'interférence potentiels** :
1. **Timing interference** : Augmentation des latences mesurées
2. **Scheduling interference** : Désynchronisation des campagnes de mesure

**Hardware sondes** (à l'époque) :
- Premières générations : CPU très limité
- Générations récentes : meilleur CPU mais toujours contraint

### Méthodologie

**Type d'étude** : Expérimentale avec mesures contrôlées

**Configuration expérimentale** :
- Mesures vers/depuis sondes RIPE Atlas
- Campagnes de mesures avec charges variables
- Monitoring impact sur timing et scheduling

**Paramètres étudiés** :
1. **Timing measurements** :
   - Mesure RTT (Round-Trip Time)
   - Impact charge CPU sur précision timing
   - Comparaison hardware générations différentes

2. **Scheduling synchronization** :
   - Campagnes mesures récurrentes
   - Décalage horaire par rapport au planning prévu
   - Impact charge concurrente

**Échelle** :
- Sondes RIPE Atlas (nombre non spécifié dans résumé)
- Mesures concurrentes contrôlées
- Durée : tests multiples avec charges variables

**Outils utilisés** :
- API RIPE Atlas
- Mesures ping, traceroute
- Monitoring charge CPU sondes
- Code disponible : https://github.com/nsg-ethz/atlas_interference

### Résultats principaux

#### 1. Timing interference (précision mesures)

**Impact sur RTT** :
- ✅ **Mesures concurrentes augmentent significativement les timings**
- Augmentation latences rapportées par les sondes
- Impact variable selon charge CPU

**Influence hardware** :
- ✅ **CPU plus puissant réduit interférence timing**
- Sondes anciennes (low CPU) : forte dégradation
- Sondes récentes (better CPU) : interférence limitée
- **Recommandation** : préférer sondes hardware récent

#### 2. Scheduling interference (synchronisation)

**Désynchronisation campagnes** :
- ✅ **Campagnes peuvent se décaler jusqu'à 1 heure**
- Décalage dû à charge concurrente sur sondes
- Impact sur mesures récurrentes programmées

**Influence hardware** :
- ❌ **Meilleur hardware N'aide PAS pour synchronisation**
- Problème architectural de la plateforme
- Persiste même avec sondes récentes
- Limitation fondamentale du scheduling RIPE Atlas

#### 3. Implications pour utilisateurs

**Timing** :
- Sélectionner sondes hardware récent (v3+)
- Éviter périodes haute charge si précision critique
- Considérer variance timing dans analyses

**Scheduling** :
- Ne pas se fier strictement aux horaires programmés
- Accepter décalages jusqu'à 1h pour mesures récurrentes
- Vérifier timestamps réels dans résultats (pas juste scheduling)

### Conclusion des auteurs

**Contributions principales** :
1. ✅ **Première quantification interférence RIPE Atlas**
2. ✅ Identification 2 types interférence (timing + scheduling)
3. ✅ Impact hardware documenté (CPU améliore timing, pas scheduling)
4. ✅ Recommandations pour utilisateurs plateforme

**Limitations reconnues** :
- Étude sur génération hardware de 2015 (peut avoir changé)
- Pas d'analyse impact sur types mesures spécifiques (DNS focus)
- Pas de solution proposée pour scheduling interference

**Implications recherche** :
- ⚠️ Résultats RIPE Atlas = potentiellement biaisés par interférence
- ✅ Quantification permet ajuster interprétation résultats
- ✅ Sélection sondes = critère important (hardware version)

---

## Analyse personnelle

### Que garder pour le mémoire

**Concepts clés à réutiliser** :
- ✅ Interférence timing = timing measurements biaisés
- ✅ Interférence scheduling = désynchronisation campagnes
- ✅ Hardware sonde = critère sélection important
- ✅ Timestamps réels ≠ timestamps programmés
- ✅ Charge concurrente = facteur à considérer

**Méthodes applicables** :
- Filtrer sondes par version hardware (v3+)
- Vérifier timestamps réels dans résultats
- Accepter variance timing dans analyses
- Ne pas se fier strictement au scheduling prévu
- Considérer périodes haute/basse charge

**Chiffres/statistiques importantes** :
- Désynchronisation jusqu'à **1 heure** possible
- Impact timing **significatif** (non quantifié précisément dans résumé)
- Hardware récent **réduit** mais **n'élimine pas** interférence
- Code open source disponible (GitHub)

**Limites identifiées (pertinentes pour nous)** :
- ⚠️ **Impact sur mesures DNS non documenté spécifiquement**
- ⚠️ Étude 2015 = hardware peut avoir évolué depuis
- ⚠️ Pas de recommandation pour minimiser scheduling interference
- ⚠️ Pas de guidelines charge optimale par sonde

### Critique personnelle

**Forces de l'article** :
- ✅ Première étude systématique interférence RIPE Atlas
- ✅ Méthodologie expérimentale rigoureuse
- ✅ Identification claire 2 types interférence
- ✅ Recommandations pratiques utilisateurs
- ✅ Code open source (reproductibilité)
- ✅ Publication IMC (conférence prestigieuse)
- ✅ Affiliation institutions reconnues (ETH Zürich, IIJ)

**Faiblesses identifiées** :
- ⚠️ Résumé manque chiffres précis (amplitude interférence)
- ⚠️ Pas d'analyse par type de mesure (ping vs DNS vs traceroute)
- ⚠️ Hardware 2015 = possiblement obsolète (v5 sondes maintenant)
- ⚠️ Pas de solution proposée pour scheduling problem
- ⚠️ Pas d'analyse impact selon charge réseau (vs CPU)
- ⚠️ Pas de guidelines fréquence mesures optimale

**Lien avec autres articles lus** :
- **Nosyk et al. (2024) - RIPE Atlas DITL** :
  - Nosyk mentionne 88K mesures DNS quotidiennes
  - Holterbach montre que charge affecte timing + scheduling
  - Implique : 88K mesures = potentiellement forte interférence
  - Notre étude : besoin considérer ce biais

- **OpenINTEL (van Rijswijk-Deij 2016)** :
  - OpenINTEL = infrastructure dédiée (pas d'interférence)
  - RIPE Atlas = partagée (interférence documentée ici)
  - Trade-off : contrôle (OpenINTEL) vs diversité géo (RIPE)

- **Tranco (Le Pochat 2019)** :
  - Tranco fournit liste stable pour mesures
  - Holterbach : timing variance affecte fiabilité
  - Combinaison : liste stable + variance timing à gérer

**Questions ouvertes** :
1. **Impact interférence spécifiquement sur mesures DNS ?**
   → DNS = queries rapides, timing moins critique que traceroute ?
2. **Hardware v5 (2024) a-t-il résolu ces problèmes ?**
   → Comparer avec Nosyk 2024 (hardware récent)
3. **Comment détecter interférence dans nos propres mesures ?**
   → Monitoring charge sondes ? Analyse variance timing ?
4. **Fréquence mesures optimale pour minimiser interférence ?**
   → Quotidien vs hebdomadaire : impact charge ?
5. **Scheduling interference affecte-t-il analyses temporelles ?**
   → Notre étude = dimension temporelle importante
6. **Peut-on compenser interférence algorithmiquement ?**
   → Filtrage, pondération, calibration ?

### Citations importantes

> "Public measurement platforms composed of low-end hardware devices such as RIPE Atlas have gained significant traction in the research community."

> "This paper answers a fundamental question for any platform user: Do measurements launched by others impact my results?"

> "We found that overlapping measurements do interfere with each other in at least two ways."

**Sur timing interference** :
> "First, we show that measurements performed from and towards the platform can significantly increase timings reported by the probe. We found that increasing hardware CPU greatly helped in limiting interference on the measured timings."

**Sur scheduling interference** :
> "Second, we show that measurement campaigns can end up completely out-of-synch (by up to one hour), due to concurrent loads. In contrast to precision, we found that better hardware does not help."

---

## Utilisation dans le mémoire

### Sections concernées

- **Section 2.5** : RIPE Atlas et mesures distribuées
  Décrire limitations plateforme (interférence timing + scheduling)
  Impact sur fiabilité résultats

- **Section 4** : Méthodologie
  Justifier choix sondes hardware récent
  Expliquer stratégie gestion interférence
  Utilisation timestamps réels (pas programmés)
  Considération variance timing dans analyses

- **Section 5** : Résultats
  Discuter variance observée (potentielle interférence)
  Analyse robustesse résultats face à interférence

- **Section 7** : Discussion
  Limitations RIPE Atlas vs OpenINTEL
  Trade-off diversité géographique vs contrôle infrastructure
  Recommandations futurs travaux

### Points à développer

**Dans état de l'art** :
- Deux types interférence RIPE Atlas :
  1. **Timing** : augmentation latences mesurées (réduit par meilleur CPU)
  2. **Scheduling** : désynchronisation jusqu'à 1h (non résolu par hardware)
- Impact charge concurrente sur précision mesures
- Hardware sonde = critère sélection important

**Pour notre méthodologie** :
- **Sélection sondes** :
  - Filtrer par version hardware (v3+ minimum, v5 préféré)
  - Vérifier disponibilité CPU via API ?
  - Éviter sondes avec charge excessive
- **Gestion timing** :
  - Utiliser timestamps réels (pas timestamps programmés)
  - Accepter variance timing dans analyses
  - Possiblement : mesures multiples pour moyenner variance
- **Gestion scheduling** :
  - Ne pas se fier strictement aux horaires programmés
  - Fenêtre temporelle flexible (tolérer décalages)
  - Vérifier distribution temporelle résultats a posteriori
- **Stratégie optimisation** :
  - Lancer mesures périodes basse charge si possible ?
  - Fréquence mesures : balance précision vs charge
  - Monitoring impact interférence (analyse variance)

**Pour discussion/limitations** :
- ⚠️ Résultats potentiellement affectés par interférence
- ⚠️ Variance timing non due uniquement au réseau
- ⚠️ Désynchronisation limite précision analyses temporelles
- ✅ Trade-off accepté pour bénéficier diversité géographique
- ✅ Sélection sondes hardware récent minimise impact

**Tableau comparatif (à ajouter)** :

| Critère | OpenINTEL | RIPE Atlas (notre approche) |
|---------|-----------|------------------------------|
| Contrôle infrastructure | ✅ Total | ❌ Partagée |
| Interférence mesures | ❌ Aucune | ⚠️ Timing + scheduling |
| Précision timing | ✅ Haute | ⚠️ Variable (CPU-dependent) |
| Synchronisation | ✅ Précise | ⚠️ ±1h désync possible |
| Mitigation | N/A | ✅ Hardware récent (partiel) |
| Trade-off accepté | N/A | ✅ Pour diversité géo |

### Références croisées

**Articles à lire ensuite** :
- [ ] Articles citant Holterbach 2015 (évolution depuis)
- [ ] Études RIPE Atlas post-2015 (hardware v4, v5)
- [ ] Comparaisons timing précision RIPE vs autres plateformes
- [ ] Analyses impact interférence sur types mesures spécifiques (DNS)

**Auteurs à suivre** :
- Thomas Holterbach (ETH Zürich) - network measurements
- Laurent Vanbever (ETH Zürich) - Internet measurement platforms
- Cristel Pelsser (IIJ) - routing, measurements
- Randy Bush (IIJ) - Internet infrastructure

**Ressources complémentaires** :
- Code GitHub : https://github.com/nsg-ethz/atlas_interference
- Présentation RAIM 2015 : https://www.irtf.org/raim-2015-papers/raim-2015-paper23.pdf
- HAL archive : https://hal.science/hal-01306027

---

**Tags** : #ripe-atlas #interference #timing #scheduling #measurement-quality #hardware #limitations

**Statut** : [X] Lu (résumé) / [ ] Relu / [X] Fiché / [ ] PDF complet lu / [ ] Intégré mémoire

**Prochaines étapes** :
1. ✅ Fiche complétée (basée sur résumé)
2. ⏭️ Télécharger PDF complet via ACM DL (accès UNamur)
3. ⏭️ Lire section résultats détaillés (chiffres précis)
4. ⏭️ Analyser code GitHub (méthodologie expérimentale)
5. ⏭️ Vérifier évolution hardware RIPE Atlas 2015-2024
6. ⏭️ Chercher articles citant Holterbach (solutions proposées ?)
