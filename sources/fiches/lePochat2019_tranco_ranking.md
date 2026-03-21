# Fiche de lecture - Tranco

**Référence bibliographique** :
Le Pochat, V., Van Goethem, T., Tajalizadehkhoob, S., Korczynski, M., & Joosen, W. (2019). Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation. *Network and Distributed Systems Security (NDSS) Symposium 2019*. https://doi.org/10.14722/ndss.2019.23386

**Thème** : Problèmes des listes de popularité et proposition de solution (Tranco)

**Intérêt pour le mémoire** :
Article FONDAMENTAL qui démontre les limitations et vulnérabilités des listes de popularité (Alexa, Umbrella, Majestic, Quantcast). Justifie notre choix de Tranco pour la sélection des domaines. Démontre qu'Alexa peut être manipulé avec UNE SEULE requête HTTP. Critique directe des approches existantes.

---

## Contexte de lecture

**Date de lecture** : 20 janvier 2026
**Section du mémoire** : 2.4 (État de l'art - Liste Tranco)

---

## Contenu de l'article

### Objectif(s) / Question(s) de recherche

**Question principale** : Les listes de popularité commerciales (Alexa, Umbrella, Majestic, Quantcast) sont-elles fiables pour la recherche en sécurité ? Peuvent-elles être manipulées ?

**Objectifs** :
1. Analyser les propriétés des 4 principales listes de popularité
2. Démontrer empiriquement leur vulnérabilité à la manipulation
3. Proposer Tranco : une liste améliorée pour la recherche

**Motivation** :
- 133 études top-tier (CCS, NDSS, S&P, USENIX Security 2015-2018) utilisent ces listes
- Validité rarement questionnée
- Méthodes opaques, intérêts commerciaux
- Vulnérabilité potentielle à la manipulation

### Cadre global d'explication

**Contexte recherche sécurité** :
- Chercheurs s'appuient sur listes de "sites populaires" pour :
  - Mesurer prévalence de vulnérabilités
  - Ensembles d'évaluation (evaluation sets)
  - Whitelists (domaines "bénins" pour classifiers)
  - Ranking/binning selon popularité
- **Impact** : Résultats recherche influencent médias, politiques publiques

**4 listes analysées** :

1. **Alexa** (Amazon)
   - Source : Extension navigateur (~570K users Chrome) + script tracking "Certify"
   - Métrique : Unique visitors + page views (propriétaire)
   - Taille : 1M domaines
   - Période : 3 mois (site) vs **1 jour** (CSV depuis jan 2018 - NON ANNONCÉ)

2. **Cisco Umbrella** (ex-OpenDNS)
   - Source : 2 résolveurs DNS (100B requêtes/jour, 65M users)
   - Métrique : Nombre d'IPs uniques faisant requêtes DNS
   - Taille : 1M entrées (inclut sous-domaines)
   - Période : Sampling + normalisation

3. **Majestic**
   - Source : Crawl web 450B URLs sur 120 jours (depuis avril 2018)
   - Métrique : Nombre de subnets /24 avec backlinks
   - Taille : 1M domaines
   - Période : 120 jours

4. **Quantcast**
   - Source : Script tracking (sites "quantified") + estimations ISP/toolbar
   - Métrique : Nombre de visiteurs US sur 1 mois
   - Taille : ~520K domaines (réduit à ~40K nov 2018)
   - Focus : US seulement

### Méthodologie

**Type d'étude** : Analyse quantitative + expérimentation manipulation

**Période données** : Janvier 1 - Novembre 30, 2018 (335 jours)

**5 propriétés évaluées** :

1. **Similarity** : Accord entre listes sur domaines populaires
2. **Stability** : Changements de rang dans le temps
3. **Representativeness** : Reflet fidèle de la popularité web
4. **Responsiveness** : Disponibilité des sites listés
5. **Benignness** : Absence de domaines malicieux

**Crawl validation** :
- 11 mai 2018, 13:00 UTC
- 10 machines (4 CPU, 8GB RAM)
- Chromium 66 headless
- Réseau universitaire européen

**Expériences manipulation** :
- Domaines de test enregistrés
- Trafic forgé selon méthode de chaque liste
- Mesure rang atteint vs effort requis

### Résultats principaux

#### 1. Propriétés des listes (Section III)

**Similarity - Accord très faible** :
- Intersection 4 listes : **~70K domaines** (sur 2.82M total)
- RBO (Rank-Biased Overlap) entre listes :
  - Alexa-Majestic-Quantcast : 24-33% seulement
  - Umbrella vs autres : 4.5-15.5% (30% si PLDs seulement)
  - **Conclusion** : Pas de consensus sur "sites populaires"

**Stability - Volatilité problématique** :

| Liste | Changement quotidien moyen |
|-------|----------------------------|
| **Majestic** | <1% |
| **Quantcast** | <1% |
| **Umbrella** | ~10% |
| **Alexa (avant 30 jan 2018)** | <1% |
| **Alexa (après 30 jan 2018)** | **~50% !!!** |

- **DÉCOUVERTE MAJEURE** : Alexa a changé de moyenne 30 jours → **1 jour** (30 jan 2018)
  - NON ANNONCÉ publiquement
  - Confirmé par Alexa après contact des auteurs
  - **50% de la liste change chaque jour** depuis

**Representativeness** :
- 10 TLDs capturent >73% de chaque liste
- .com domine : 50% (Alexa, Majestic), 71% (Quantcast)
- Cloudflare héberge jusqu'à 10% des sites
- Google : 15-40% du top 10-100 (sauf Quantcast 4%)
- **Problème** : Concentration sur quelques entités

**Responsiveness - Sites non accessibles** :

| Liste | Non-accessibles | Status 200 | Page <512 bytes |
|-------|-----------------|------------|-----------------|
| Alexa | 5% | 89% | 3% |
| Quantcast | 5% | 89% | 3% |
| Majestic | 11% | 78% | 8.7% |
| **Umbrella** | **28%** | **49% !!!** | **26%** |

- Umbrella : **51% NE SONT PAS des vrais sites** !
- Beaucoup de domaines invalides, non-configurés

**Benignness - Domaines malicieux présents** :

Google Safe Browsing (31 mai 2018) :

| Liste | Malware | Social Eng. | Unwanted | Total | % |
|-------|---------|-------------|----------|-------|---|
| Alexa | 98 | 345 | 104 | **547** | 0.05% |
| Umbrella | 326 | 393 | 232+60 | **1011** | 0.10% |
| **Majestic** | **1676** | 359 | 79+48 | **2162** | **0.22%** |
| Quantcast | 76 | 105 | 41+2 | **224** | 0.04% |

- **Majestic le pire** : 2162 domaines malicieux
- Alexa top 10K : 4 sites phishing
- **DANGER** : Quad9 utilise Majestic comme whitelist !

#### 2. Usage en recherche (Section IV)

**133 études de sécurité (2015-2018)** utilisent ces listes :

| Usage | Description | Nombre |
|-------|-------------|--------|
| **Prevalence** | Mesurer prévalence de problèmes | 63 |
| **Evaluation** | Test set pour attaques/défenses | 71 |
| **Whitelist** | Domaines "bénins" pour classifiers | 19 |
| **Ranking** | Utilisation des rangs exacts | 28 |

**Problèmes identifiés** :
- ❌ Rarement de commentaire sur date de download
- ❌ Rarement mention de la proportion accessible
- ❌ **Impact non évalué** du choix de liste sur résultats
- ❌ Validité rarement questionnée

**Case study - Fingerprinting** :
- Études Acar et al., Englehardt & Narayanan sur Alexa top 100K-1M
- **Démonstration** : Attaquant peut manipuler pour cacher scripts tracking
- Exemple : 7032 domaines manipulés → cache 1 provider du top 1M
- **Impact** : Recherche biaisée, tracking non détecté

#### 3. Manipulation à grande échelle (Section V)

**RÉSULTATS CHOQUANTS** :

**ALEXA - Extension** :
- **1 SEULE requête HTTP** → entre dans top 1M !
- 12 requêtes → rang **370,461**
- 20% des tentatives réussies
- Modèle estimé : **10^7.5 × r^(-1.125)** requests pour rang r
- Rang 10,000 : seulement **1000 page views** nécessaires
- **Coût** : GRATUIT
- **Effort** : Faible (automatisable)
- **Temps** : 1 jour (moyenne sur 1 jour)

**ALEXA - Certify** :
- 16,000 requêtes/jour via Tor
- Rang atteint : **28,798** (meilleur résultat validé empiriquement)
- Délai : 21 jours (vérification Alexa)
- **Coût** : USD 19.99/mois/site
- **Effort** : Moyen
- **Temps** : Élevé (21 jours attente)

**UMBRELLA - Cloud providers (AWS)** :
- 1000 IPs uniques → rang **200,000**
- Trafic compté pendant 2 jours
- 12 sous-domaines simultanément rankés
- **Coût** : <USD 1 pour 10,000 IPs (instance start/stop)
- **Effort** : Moyen
- **Temps** : Faible
- **Domaines fake** : Possible (aucun filtrage)

**MAJESTIC - Backlinks** :
- 500 backlinks achetés (USD 500)
- Rang atteint validé
- Alternative : 1041 URLs reflected (GRATUIT mais effort élevé)
- **Coût** : Élevé (USD 0.25-plus par backlink/mois)
- **Effort** : Élevé (curation manuelle)
- **Temps** : Élevé (120 jours comptage)
- **Persistance** : 120 jours après arrêt paiement

**QUANTCAST - Quantified** :
- 479 VPN servers US
- 400 users générés/jour × 5 requests
- Rang théorique : ~367,000
- **Coût** : Faible (VPN)
- **Effort** : Moyen
- **Temps** : Élevé (validation lente)

**Tableau récapitulatif** (Table III) :

| Liste | Technique | Coût $ | Effort | Temps |
|-------|-----------|--------|--------|-------|
| Alexa | Extension | ★☆☆ | ★★☆ | ★☆☆ |
| Alexa | Certify | ★★☆ | ★★☆ | ★★★ |
| Umbrella | Cloud | ★☆☆ | ★★☆ | ★☆☆ |
| Majestic | Backlinks | ★★★ | ★★★ | ★★★ |
| Majestic | Reflected URLs | ★☆☆ | ★★★ | ★★☆ |
| Quantcast | Quantified | ★☆☆ | ★★☆ | ★★★ |

#### 4. Solution : TRANCO (Section VI)

**Design** :
- Combinaison des 4 listes
- Méthode : Dowdall rule (1, 1/2, 1/3, ..., 1/N) - reflète Zipf's law
- Moyenne sur **30 jours** par défaut
- Normalisation Umbrella (PLDs seulement)
- Rescaling Quantcast (<1M)

**Filtres disponibles** :
- TLD filtering
- Responsiveness (HTTP status, content length)
- Google Safe Browsing (malware)
- Chrome UX Report (sites réellement populaires)
- Apparition minimum (ex: présent sur 2+ listes, 2+ jours)

**Résultats Tranco** :
- **Stabilité** : 0.6% changement quotidien (vs 50% Alexa !)
- **RBO avec listes sources** :
  - Alexa/Majestic : 46.5-53.5%
  - Quantcast/Umbrella : 31.5-40.5%
  - Aucune liste ne domine
- **Résilience manipulation** :
  - Effort **quadruplé** pour même rang
  - Rang top 1M : besoin rang 11,091 (1 jour) ou 332,778 (30 jours) dans UNE liste
  - Rang top 100K : besoin rang 982 (1 jour) ou 29,479 (30 jours)

**Service https://tranco-list.eu** :
- Listes archivées quotidiennement
- Permalink + citation pour chaque liste
- Configuration détaillée visible
- Reproductibilité garantie
- Open source : https://github.com/DistriNet/tranco-list

### Conclusion des auteurs

**Contributions** :
1. ✅ Analyse quantitative 4 listes principales (10 mois)
2. ✅ Classification 133 études sécurité utilisant ces listes
3. ✅ **Démonstration empirique** manipulation à grande échelle
4. ✅ Proposition Tranco : liste améliorée pour recherche

**Limitations des listes existantes** :
- ❌ Similarity faible (pas d'accord sur popularité)
- ❌ Instabilité élevée (Alexa 50%/jour, Umbrella 10%/jour)
- ❌ Non-représentativité (51% Umbrella non-réels, concentration entités)
- ❌ Domaines malicieux (2162 sur Majestic)
- ❌ **MANIPULATION TRIVIALE** (1 requête pour Alexa !)

**Recommandations défense** (providers) :
- Détection fraude individuelle (click inflation techniques)
- Augmenter effort/ressources manipulation (comptes en ligne, filtrage IP)
- Vérification disponibilité domaines
- Reputation scores pour backlinks

**Tranco comme solution** :
- Combinaison réduit biais individuels
- Moyenne temporelle améliore stabilité
- Filtres permettent customisation
- Service permanent pour reproductibilité

---

## Analyse personnelle

### Que garder pour le mémoire

**Concepts clés à réutiliser** :
- ✅ **Instabilité Alexa** : 50% changement/jour (justifie choix Tranco)
- ✅ **5 propriétés** : similarity, stability, representativeness, responsiveness, benignness
- ✅ **Méthodologie Tranco** : Dowdall rule, moyenne 30 jours
- ✅ **Vulnérabilité manipulation** : argument pour NE PAS utiliser listes brutes
- ✅ **133 études** utilisent Alexa → usage répandu en recherche

**Méthodes applicables** :
- Dowdall rule pour combinaison rankings (vs Borda count)
- Filtrage domaines non-disponibles
- Filtrage malware (Google Safe Browsing)
- Moyenne temporelle pour stabilité
- Validation crawl pour vérifier accessibilité

**Chiffres/statistiques importantes** :
- **50% Alexa change/jour** (depuis 30 jan 2018)
- 1 requête HTTP → top 1M Alexa
- 51% Umbrella ne sont PAS de vrais sites
- 2162 domaines malicieux sur Majestic
- 133 études top-tier utilisent ces listes (2015-2018)
- Tranco : 0.6% changement/jour (vs 50% Alexa)
- Effort manipulation **×4** avec Tranco

**Limites identifiées (notre contexte)** :
- ⚠️ Tranco combine toutes listes (mais on peut filtrer)
- ⚠️ Domaines populaires ≠ domaines géographiquement distribués
- ⚠️ Aucune liste ne mesure diversité géographique réponses DNS
- ⚠️ Quantcast = US seulement (biais géographique)
- ⚠️ Umbrella inclut sous-domaines (peut fausser mesures)

### Critique personnelle

**Forces de l'article** :
- ✅ **Méthodologie rigoureuse** : 10 mois de données, 133 études analysées
- ✅ **Validation empirique** manipulation (pas juste théorique)
- ✅ **Impact réel** : rang 28,798 atteint (Alexa Certify)
- ✅ **Solution concrète** : Tranco + service en ligne
- ✅ **Open source** : Code + données disponibles
- ✅ **NDSS 2019** : Conférence top-tier
- ✅ **Découverte majeure** : Changement Alexa non-annoncé (jan 2018)
- ✅ **Analyse éthique** : Discussion Menlo Report
- ✅ **Reproductibilité** : Service permanent avec permalinks

**Faiblesses identifiées** :
- ⚠️ Données 2018 (mais principes restent valables)
- ⚠️ Quantcast a drastiquement changé (nov 2018) - impact sur Tranco ?
- ⚠️ Pas de comparaison avec SimilarWeb (payant)
- ⚠️ Pas d'analyse impact changement Alexa sur études publiées 2018+
- ⚠️ Défenses proposées pour providers pas testées empiriquement

**Lien avec autres articles lus** :
- **van Rijswijk-Deij (OpenINTEL)** :
  - OpenINTEL mesure TOUS domaines .com/.net/.org
  - Tranco sélectionne "top" domaines selon popularité
  - **Complémentarité** : OpenINTEL = exhaustivité, Tranco = popularité
  - Les deux peuvent être combinés pour notre approche

**Questions ouvertes** :
1. **Tranco capture-t-il la diversité géographique ?**
   → NON : Tranco agrège listes qui mesurent depuis points centralisés
   → Notre contribution RIPE Atlas reste valable !

2. Quelle taille de liste Tranco utiliser pour notre mémoire ?
   → Top 1K, 10K, 100K, 1M ?

3. Filtres Tranco à appliquer pour notre cas d'usage ?
   → Responsiveness (status 200) ? Safe Browsing ? Chrome UX ?

4. Impact de l'instabilité Alexa sur études DNS 2018-2026 ?

5. Est-ce que les listes de popularité sont pertinentes pour mesures DNS géo-distribuées ?
   → Sites populaires ≠ nécessairement sites avec réponses DNS géo-variées

### Citations importantes

**Sur instabilité Alexa** :
> "Since January 30, 2018 the [Alexa downloadable] list is based on data for one day; this was confirmed to us by Alexa but was otherwise unannounced." (p. 2)

> "Until January 30, 2018, Alexa's list was almost as stable as Majestic's or Quantcast's. However, since then stability has dropped sharply, with around half of the top million changing every day" (p. 3)

**Sur manipulation** :
> "We show that for each list there exists at least one technique to manipulate it on a large scale, as e.g. only one HTTP request suffices to enter the widely used Alexa top million." (p. 2)

> "What is most striking, is the very small number of page visits needed to obtain a ranking: as little as one request yielded a rank within the top million" (p. 7)

**Sur impact recherche** :
> "We found that 133 top-tier studies over the past four years based their experiments and conclusions on the data from these rankings." (p. 1)

> "The validity and representativeness of these rankings are rarely questioned" (p. 1)

**Sur Umbrella** :
> "For Umbrella, this jumps to 28%; moreover only 49% responded with status code 200" (p. 4)

**Sur solution Tranco** :
> "Motivated by the discovered limitations of the widely-used lists, we propose TRANCO, an alternative list that is more appropriate for research, as it varies only by 0.6% daily and requires at least the quadrupled manipulation effort" (p. 2)

**Sur diversité géographique** (limitation pertinente pour NOUS) :
> "Yet, the information returned by DNS can vary depending on the location of the client (for example to minimize latency, to provide a local version of the service)" (p. 1) ← Mentionné mais pas adressé par Tranco !

---

## Utilisation dans le mémoire

### Sections concernées

- **Section 2.4** : Liste Tranco (section dédiée)
  - Critique des listes existantes (Alexa instable, Umbrella 51% invalide)
  - Méthodologie Tranco (Dowdall, moyenne 30j)
  - Justification de notre choix

- **Section 3** : Question de recherche
  - Utiliser limitation "géographique" non adressée par Tranco
  - Justifier besoin de mesures RIPE distribuées

- **Section 4** : Méthodologie
  - Justifier choix Tranco top X (1K, 10K, 100K ?)
  - Expliquer filtres appliqués (responsiveness, malware)
  - Comparaison avec approche OpenINTEL

- **Section 7** : Discussion
  - Comparer stabilité de nos mesures vs volatilité Alexa
  - Discuter représentativité domaines choisis
  - Valider que nos domaines sont accessibles

### Points à développer

**Pour justifier choix Tranco** :
- Tableau comparatif 4 listes (stabilité, accessibilité, malware)
- Graphique instabilité Alexa (50%/jour) vs Tranco (0.6%/jour)
- Argumentation : recherche nécessite stabilité et reproductibilité

**Pour méthodologie** :
- Quelle taille liste ? (discuter trade-off couverture vs faisabilité)
- Quels filtres ? (argumenter selon objectif recherche)
- Validation accessibilité domaines sélectionnés (comme article)

**Pour positionnement contribution** :
- **Gap identifié** : Tranco améliore stabilité/manipulation mais ne résout PAS diversité géographique
- **Notre contribution** : Ajouter dimension géographique via RIPE Atlas
- Complémentarité : Tranco (sélection domaines) + RIPE (diversité géo)

### Références croisées

**Articles à lire ensuite** :
- [X] van Rijswijk-Deij (2016) - OpenINTEL (déjà lu)
- [ ] Scheitle et al. (2018) - "A long way to the top" (IMC 2018) - cité comme travail connexe
- [ ] Englehardt & Narayanan (2016) - Tracking (cas d'usage)
- [ ] Études utilisant RIPE Atlas pour DNS

**Auteurs à suivre** :
- Victor Le Pochat (auteur principal, KU Leuven)
- Wouter Joosen (promoteur, KU Leuven)
- Chercher leurs publications DNS/mesures récentes

---

**Tags** : #tranco #alexa #ranking #manipulation #stability #top-sites #methodology

**Statut** : [X] Lu / [ ] Relu / [X] Fiché / [ ] Intégré mémoire

**Prochaines étapes** :
1. ✅ Fiche complétée
2. ⏭️ Décider quelle taille de liste Tranco utiliser (discuter avec promoteurs)
3. ⏭️ Tester accessibilité domaines Tranco top X
4. ⏭️ Chercher études utilisant Tranco + RIPE Atlas
5. ⏭️ Lire Scheitle et al. (2018) IMC paper
