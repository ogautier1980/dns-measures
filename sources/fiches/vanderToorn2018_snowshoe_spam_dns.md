# Fiche de lecture - Snowshoe Spam Detection via Active DNS

**Référence bibliographique** :
van der Toorn, O., van Rijswijk-Deij, R., Geesink, B., & Sperotto, A. (2018). *Melting the Snow: Using Active DNS Measurements to Detect Snowshoe Spam Domains*. NOMS 2018 - IEEE/IFIP Network Operations and Management Symposium. DOI: 10.1109/NOMS.2018.8406264

**Thème** :
Détection de domaines spam via mesures DNS actives + machine learning

**Intérêt pour le mémoire** :
Démontre l'utilisation concrète de mesures DNS actives à grande échelle (OpenINTEL, 60% namespace) combinées avec ML pour détection proactive. Illustre la valeur ajoutée des mesures actives vs passives et le potentiel d'anticipation (détection 100 jours avant blacklists).

---

## Contexte de lecture

**Date de lecture** : 21 mars 2026
**Section du mémoire** :
- Section 2.2 (Mesures DNS actives vs passives)
- Section 2.6 (Sécurité DNS - cas d'usage)

---

## Contenu de l'article

### Objectif(s) / Question(s) de recherche

**Problème** : Le snowshoe spam représente 15% du spam global et est difficile à détecter car :
- Charge distribuée sur de nombreux hôtes (évite les blacklists basées sur réputation)
- Adoption de best practices email (SPF) pour paraître légitime
- Détection traditionnelle = passive DNS → limitée aux domaines déjà utilisés

**Question** : Peut-on détecter les domaines crafted pour snowshoe spam **avant leur utilisation** via mesures DNS actives + ML ?

**Hypothèse clé** : Les domaines snowshoe spam ont des caractéristiques DNS distinctives :
- Grand nombre d'enregistrements A ou MX (nombreux hôtes)
- Enregistrements TXT larges (SPF avec nombreuses IP)
- Patterns détectables dans la "long tail" de la distribution DNS

### Cadre global d'explication

**Contexte économique** :
- Coût envoi 1M spam : $250 pour spammer
- Coût réception 1M spam : $2,800 en temps perdu (Pfleeger & Bloom)

**Snowshoe spam (caractéristiques)** :
1. Distribution charge sur **nombreux hôtes** (évite concentration = détection)
2. Adoption **SPF** (Sender Policy Framework) → requiert DNS légitimes
3. **Crafting** : création domaines avec large nombre de records DNS

**Gap littérature** :
- Passive DNS = bias d'usage, détection post-facto
- Études actives précédentes = zones limitées ou petits datasets
- Peu de travaux spécifiques snowshoe spam

### Méthodologie

- **Type d'étude** : Expérimentale - mesures actives + supervised ML
- **Outils utilisés** :
  - **OpenINTEL platform** : mesures DNS actives quotidiennes
  - **Scikit-learn** (Python) : 13 classifiers testés
  - **Blacklists publiques** : validation (SURBL, Spamhaus, etc.)
- **Échelle** :
  - **60% du namespace DNS global** (.com, .net, .org, .info, .mobi, nouveaux gTLDs, ccTLDs)
  - **Millions de domaines** analysés quotidiennement
  - **Déploiement production** : 3 mois chez opérateur réseau néerlandais
- **Protocole de mesure** :
  1. **Collecte DNS** (A) : snapshots quotidiens OpenINTEL (types A, AAAA, MX, TXT, etc.)
  2. **Long Tail Analysis** (B) : extraction domaines outliers (seuils 99.9%, 99%, 98%, 97%)
  3. **Classification ML** (C) : prédiction binaire spam/non-spam (35 features)
  4. **RBL** (D) : Real-time Blackhole List mise à jour quotidiennement
- **Données collectées** :
  - **Features (35 total)** : nombre records (A, AAAA, MX, TXT, NS, SOA, CNAME, etc.), longueur TXT, patterns SPF, etc.
  - **Features clés** (Gini index) : `response_name_matches`, `ip4_count`, `mx_count`
  - **Training dataset** : positives (blacklists) + negatives (Alexa Top 1M)

**Classifiers testés (13)** :
- Naive Bayes (BernoulliNB, GaussianNB, MultinomialNB)
- Decision Tree (DecisionTreeClassifier, RandomForestClassifier)
- Nearest Neighbor (KNeighborsClassifier, RadiusNeighborsClassifier)
- Gradient Descent (GradientBoostingClassifier, SGDClassifier)
- Autres : SVC, MLPClassifier, AdaBoostClassifier

**Sélection "best classifier"** : 2 étapes
1. Optimisation hyperparamètres (GridSearchCV)
2. Évaluation performance sur test set

### Résultats principaux

1. **Précision détection : >93%** avec classifier optimal
2. **Détection précoce : jusqu'à 100 jours avant blacklists publiques**
   - Fraction significative détectée bien avant apparition sur blacklists
   - Avantage temporel crucial pour blocage proactif
3. **Validation production (3 mois)** :
   - Déploiement réel chez opérateur réseau néerlandais (SURFnet)
   - Système mail filter opérationnel
   - **Décision déploiement production basée sur résultats**
4. **Couverture : 60% namespace DNS** (vs études précédentes < quelques zones)
5. **Long tail analysis efficace** :
   - Seuils 97-99.9% capturent domaines snowshoe
   - Majorité domaines = peu records, snowshoe = outliers (queue distribution)

**Comparaison active vs passive DNS** :
- Passive DNS = limité aux domaines **déjà utilisés** et observés
- Active DNS = détection **globale** et **indépendante de l'usage**
- Permet détection **avant utilisation malveillante**

### Conclusion des auteurs

**Contributions principales** :
1. Première détection snowshoe spam via mesures DNS actives à grande échelle
2. Méthode identifie domaines **avant** blacklists existantes (time advantage)
3. RBL publiquement disponible pour chercheurs et opérateurs
4. **Validation pratique : déploiement production confirmé**

**Implications** :
- Mesures actives DNS = outil puissant détection proactive malware/spam
- Machine learning + DNS features = approche généralisable
- Indépendance du contenu email = détection upstream

---

## Analyse personnelle

### Que garder pour le mémoire

**Concepts clés à réutiliser** :
- **Distinction active vs passive DNS** : active = coverage complète, passive = usage-biased
- **Long tail analysis** : outliers statistiques révèlent comportements anormaux
- **Détection proactive** : identifier menaces avant usage effectif
- **Validation production** : importance déploiement réel (pas seulement lab)

**Méthodes applicables** :
- OpenINTEL comme infrastructure référence mesures actives large échelle
- Features extraction depuis records DNS standard (A, MX, TXT, etc.)
- Combinaison mesures quantitatives (nombre records) + qualitatives (patterns SPF)
- Validation via comparaison blacklists publiques

**Chiffres/statistiques importantes** :
- **60% namespace DNS global** mesuré quotidiennement (OpenINTEL)
- **15% spam = snowshoe** (Cisco 2014)
- **>93% précision** détection
- **100 jours avance** sur blacklists (temps de réaction)
- **35 features** extraites des DNS records
- **13 classifiers** testés (exhaustivité approche ML)

**Limites identifiées (gaps à combler)** :
- Focalisation snowshoe spam uniquement (généralisation autres abus DNS ?)
- Dépendance à OpenINTEL (infrastructure centralisée, 1 point mesure)
- Pas de diversité géographique mesures → **lien direct avec notre mémoire**
- Training data = blacklists + Alexa (potentiels faux négatifs Alexa)
- Classifiers = features numériques uniquement (pas raw strings)

### Critique personnelle

**Forces de l'article** :
- ✅ **Validation pratique exceptionnelle** : déploiement production 3 mois + adoption réelle
- ✅ **Échelle impressionnante** : 60% namespace (vs études précédentes limitées)
- ✅ **Comparaison rigoureuse** : 13 classifiers testés, grid search hyperparams
- ✅ **Méthodologie claire** : pipeline reproductible (A-B-C-D-E)
- ✅ **Impact mesurable** : time advantage quantifié (100 jours)
- ✅ **Open science** : RBL publiquement disponible
- ✅ **Auteurs crédibles** : équipe OpenINTEL (van Rijswijk-Deij, Sperotto)

**Faiblesses identifiées** :
- ⚠️ **Centralisation mesures** : 1 seul vantage point (Pays-Bas) → pas de validation géographique
- ⚠️ **Ground truth limitée** : dépendance aux blacklists (qui sont elles-mêmes imparfaites)
- ⚠️ **Features engineering** : choix 35 features pas fully justified (pourquoi ces features ?)
- ⚠️ **Concept drift** : évolution spam tactics → besoin re-training régulier (mention mais pas testé long-terme)
- ⚠️ **Ethical considerations** (Section VII) : mentionnées mais peu développées
- ⚠️ **Faux positifs** : 93% précision = 7% erreur → impact sur domaines légitimes ?

**Lien avec autres articles lus** :
- **van Rijswijk-Deij 2016 (OpenINTEL)** : Même infrastructure, confirme applicabilité à use cases sécurité
- **Tranco (Le Pochat 2019)** : Contraste avec Alexa (utilisé ici comme baseline) - Tranco serait meilleur choix négatives
- **RIPE Atlas (Nosyk 2024)** : Complémentarité potentielle - diversité géographique manquante ici

**Questions ouvertes** :
- Résultats seraient-ils différents avec mesures depuis vantage points multiples (géo-diversité) ?
- Peut-on détecter autres types abus DNS (DGA, phishing, C&C) avec approche similaire ?
- Impact ECS (EDNS Client Subnet) sur détection ? (pas mentionné)
- Combien de faux positifs sur domaines légitimes ? (non quantifié)
- Évolution performance classifier sur 1-2 ans sans re-training ?

### Citations importantes

> "Snowshoe spammers distribute sending of spam over many hosts, in order to evade detection by spam reputation systems (blacklists)." (p. 1)

> "We make use of active DNS measurements, covering more than 60% of the global DNS namespace, in combination with machine learning to identify malicious domains crafted for snowshoe spam." (Abstract)

> "We are able to detect a significant fraction of the malicious domains up to 100 days earlier than existing blacklists, which suggests our method can give us a time advantage in the fight against spam." (Abstract)

> "Passive DNS is in general usage-biased and [...] only anomalous behavior in the monitored network can be detected. [...] We use actively collected DNS data, which allow us to detect anomalous domains at a global scale and independently from their being accessed by users." (p. 2)

> "Not only did this demonstrate that our approach works in practice, the operator has actually decided to deploy our method in production, based on the results obtained." (Abstract)

---

## Utilisation dans le mémoire

**Sections concernées** :
- **2.2 (Mesures actives vs passives)** : Argument fort pour mesures actives (détection proactive, pas usage-biased)
- **2.3 (OpenINTEL)** : Cas d'usage concret infrastructure, validation applicabilité sécurité
- **2.6 (Sécurité DNS)** : État de l'art détection spam/abus via DNS
- **5.X (Discussion limites)** : Argumenter besoin diversité géographique (limitation OpenINTEL 1 point)

**Points à développer** :
- **Active vs Passive** : contraste clair avec long tail analysis impossible en passive
- **Scalabilité** : 60% namespace = faisable avec infra centralisée (OpenINTEL) mais quid distribution ?
- **Complémentarité RIPE Atlas** : notre approche apporte diversité géo manquante ici
- **Généralisation méthode** : ML + DNS features applicable à d'autres contextes (pas que spam)

**Références croisées** :
- van Rijswijk-Deij 2016 : Infrastructure sous-jacente
- Nosyk 2024 : Diversité géographique (complémentaire)
- Tranco 2019 : Alternative Alexa pour négatives training

---

**Tags** : #dns #active-measurement #machine-learning #spam-detection #openintel #security #snowshoe-spam #rbl
**Statut** : [X] Lu / [X] Fiché

**Date fiche** : 21 mars 2026
