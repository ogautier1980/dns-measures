# Chapitre 5 - Discussion et conclusion

## 5.1 Discussion des résultats

### 5.1.1 Interprétation de la diversité géographique (Q1)

**Observation principale** : XX.X% des domaines Tranco Top 10K présentent une diversité géographique des réponses DNS.

**Comparaison avec la littérature** :

Nos résultats [confirment / contredisent / nuancent] les observations de la littérature existante :

- **Calder et al. (2015)** ont montré que 80% des clients anycast CDN sont bien servis géographiquement, 20% suboptimal. Nos mesures révèlent que [XX% des domaines utilisent effectivement anycast, cohérent avec / différent de ces proportions].

- **Koch et al. (2021)** ont démontré que le contexte applicatif détermine l'importance de l'inflation anycast (root DNS >95% inflation acceptable vs CDN 35%). Nos données confirment cette distinction : [les domaines CDN présentent un ratio géo-corrélation moyen de X.X, suggérant...].

- **Wang et al. (2018)** ont quantifié l'impact des DNS publics distants : 2× latency vs ISP local. Notre analyse RTT [confirme / infirme] cet ordre de grandeur avec [XX.X ms ISP vs XX.X ms public].

**Implications pratiques** :

1. **Pour OpenINTEL et infrastructures similaires** : Mesurer depuis un point unique perd [XX%] de la diversité géographique. Une extension multi-points améliorerait significativement la complétude.

2. **Pour les chercheurs en performance réseau** : [XX%] des domaines populaires nécessitent des mesures distribuées pour comprendre leur infrastructure réelle.

3. **Pour les opérateurs CDN** : [Nos observations suggèrent que X providers dominent, avec des stratégies de distribution géographique différentes].

### 5.1.2 Interprétation de la stabilité temporelle (Q2)

**Observation principale** : Taux de changement quotidien moyen = X.X%, avec XX.X% de domaines (very) stable.

**Comparaison avec la littérature** :

- **van Rijswijk-Deij et al. (2016)** ont mesuré OpenINTEL sur plusieurs années, démontrant la valeur des mesures longitudinales. Notre période de X mois révèle [des tendances similaires / des patterns différents à court terme].

- **Le Pochat et al. (2019)** ont observé 0.6% de changement quotidien dans Tranco (liste elle-même), tandis que les enregistrements DNS changent [beaucoup plus / similairement] à X.X%.

**Corrélation TTL ↔ changement** :

Notre hypothèse selon laquelle les domaines avec TTL court changent plus fréquemment est [validée / invalidée] :
- Corrélation Spearman ρ = -X.XXX (p=X.XXe-XX)
- Interprétation : [Les administrateurs DNS configurent effectivement des TTL courts en anticipation de changements fréquents / Le TTL ne reflète pas la volatilité réelle]

**Implications pratiques** :

1. **Fréquence de mesure optimale** : Pour [XX%] des domaines, mesures [quotidiennes / hebdomadaires] suffisent à capturer les changements.

2. **Archivage DNS** : [X jours] de rétention suffiraient pour [XX%] des domaines stables, mais les [X%] volatiles nécessitent archivage quasi-temps-réel.

3. **Simulation réseau** : Les simulateurs peuvent utiliser snapshots [quotidiens / hebdomadaires] pour la majorité des domaines.

### 5.1.3 Interprétation de l'impact du biais (Q3)

**Observation principale** : Le biais géographique RIPE Atlas [impacte / n'impacte pas] significativement la diversité observée (p=X.XXe-XX).

**Analyse de sensibilité** :

Notre test Wilcoxon comparant ACTUAL vs UNIFORM révèle :
- [Différence significative / non-significative] entre distributions
- [XX%] des domaines changent de catégorie de diversité
- Régions sous-représentées (Asie, Afrique) apportent [XX%] d'IPs uniques malgré [X%] des sondes

**Implications méthodologiques** :

1. **Validité externe** : Nos résultats [sont généralisables / doivent être interprétés avec prudence] car [le biais n'affecte pas significativement les tendances globales / certaines régions sont critiquement sous-échantillonnées].

2. **Futures études** : Priorité au déploiement de sondes en [Asie / Afrique / Am. Sud] où ratio contribution/disponibilité est le plus élevé (X.X).

3. **Pondération statistique** : [Nécessaire / Non nécessaire] d'appliquer une pondération inverse pour compenser le biais dans les analyses agrégées.

**Comparaison avec Bajpai et al. (2017)** :

Bajpai et al. avaient identifié le biais 91% RIPE+ARIN en 2017. Notre analyse de 2026 [confirme la persistance / montre une amélioration] de ce biais. Leur recommandation d'utiliser des tags de sélection géographique est [validée / insuffisante] par nos résultats.

### 5.1.4 Interprétation de l'impact du resolver (Q4)

**Observation principale** : Similarité moyenne Public vs ISP = X.XXX, ECS [améliore / n'améliore pas] significativement (p=X.XXe-XX).

**Validation hypothèse ECS** :

Wang et al. (2018) ont proposé qu'ECS résout le problème des DNS publics distants. Nos mesures empiriques [confirment / infirment] cette hypothèse :
- Resolvers ECS-enabled : Jaccard moyen = X.XXX vs ISP local
- Resolvers non-ECS : Jaccard moyen = X.XXX vs ISP local
- Différence [statistiquement significative / non-significative]

**Cas des providers CDN** :

[XX%] des domaines montrent une divergence significative (Jaccard <0.5) selon le resolver. Cette divergence est particulièrement marquée pour :
- [Provider 1] : [XX%] domaines divergents
- [Provider 2] : [XX%] domaines divergents

Suggérant que [certains CDN ne supportent pas bien ECS / implémentent des stratégies de redirection DNS spécifiques au resolver].

**Privacy vs Performance trade-off** :

Hours et al. (2016) ont montré l'impact causal des resolvers sur la performance CDN. Notre analyse RTT [confirme / nuance] leurs résultats :
- Resolvers publics : [XX.X ms] plus [lents / rapides] que ISP local
- Mais avec ECS : [réduction / augmentation] de [X%] de cet écart

Le trade-off privacy (ECS expose préfixe IP client) vs performance (optimisation CDN) reste [pertinent / atténué dans nos observations].

### 5.1.5 Résultats inattendus et implications

[À compléter après analyse des données réelles]

**Résultat inattendu 1** : [Description]
- **Observation** : [...]
- **Hypothèses explicatives** : [...]
- **Implications** : [...]
- **Validation nécessaire** : [...]

**Résultat inattendu 2** : [Description]
- **Observation** : [...]
- **Hypothèses explicatives** : [...]
- **Implications** : [...]
- **Validation nécessaire** : [...]

---

## 5.2 Limitations de l'étude

### 5.2.1 Limitations méthodologiques

**Période de collecte** :
- **Limitation** : X mois de collecte vs plusieurs années pour OpenINTEL
- **Impact** : Tendances saisonnières, événements ponctuels (migrations CDN) potentiellement manqués
- **Mitigation** : Analyse focused sur patterns court-terme, reproductibilité permet extension future

**Couverture domaines** :
- **Limitation** : Top 10K Tranco vs 123M domaines OpenINTEL
- **Impact** : Résultats valides pour domaines populaires, généralisation limitée à long tail
- **Mitigation** : Tranco Top 10K représente les sites critiques (Google, Facebook, Amazon, etc.)

**Biais géographique** :
- **Limitation** : 91% sondes Europe+NA, sous-représentation Asie/Afrique/Am. Sud
- **Impact** : [Modéré / Significatif] selon résultats Q3
- **Mitigation** : Analyse de sensibilité, pondération statistique, transparence sur limitation

### 5.2.2 Limitations techniques

**Interférence RIPE Atlas** :
- **Limitation** : Holterbach et al. (2015) ont montré désynchronisation jusqu'à 1h
- **Impact** : Timing measurements potentiellement biaisés, fenêtre temporelle imprécise
- **Mitigation** : Utilisation timestamps réels, tolérance ±2h, filtrage outliers >4h

**Filtrage lying resolvers** :
- **Limitation** : Méthode heuristique (détection réponses minoritaires)
- **Impact** : Faux positifs possibles (réponses légitimes mais rares)
- **Mitigation** : Seuils conservateurs (5% fréquence minimum), validation manuelle échantillon

**Identification providers CDN** :
- **Limitation** : Inférence basée sur AS mapping et patterns DNS, pas toujours fiable
- **Impact** : [XX%] domaines non-identifiés, classifications possiblement erronées
- **Mitigation** : Validation croisée avec WHOIS, reverse DNS, documentation publique

### 5.2.3 Limitations d'interprétation

**Corrélation vs causalité** :
- **Exemple** : TTL court ↔ changements fréquents
- **Problème** : Corrélation ne prouve pas que TTL court *cause* changements (causalité inverse possible)
- **Mitigation** : Prudence interprétation, proposition hypothèses alternatives

**Effet ECS difficile à isoler** :
- **Problème** : Resolvers ECS-enabled (Google, Cloudflare) ≠ seule différence avec ISP local
- **Confounders** : Infrastructure resolver, peering agreements, géolocalisation resolver
- **Mitigation** : Tests statistiques multivariés, analyse de sensibilité

**Généralisation au-delà de Tranco Top 10K** :
- **Problème** : Domaines populaires ≠ tous domaines (long tail très différente)
- **Impact** : Résultats valides pour 10K sites majeurs, extrapolation risquée
- **Mitigation** : Transparence sur scope, suggestions études complémentaires

---

## 5.3 Contributions de ce travail

### 5.3.1 Contributions scientifiques

**Contribution empirique principale** :

Première quantification systématique de la diversité géographique des réponses DNS pour les domaines populaires, validée sur [X mois] de collecte continue avec ~100 vantage points mondiaux.

**Résultats quantitatifs** :
- XX.X% des domaines Tranco Top 10K présentent diversité géographique
- Taux changement quotidien moyen = X.X%
- Impact biais RIPE Atlas [significatif / modéré / négligeable]
- ECS [améliore / n'améliore pas] significativement similarité Public vs ISP

**Validation empirique** :

Nos résultats [confirment / infirment / nuancent] plusieurs hypothèses de la littérature :
- ✓ Anycast inflation (Koch et al., 2021) : [Confirmé avec...]
- ✓ Impact remote DNS (Wang et al., 2018) : [Confirmé avec...]
- ✓ ECS mitigation (RFC 7871) : [Confirmé partiellement avec...]

### 5.3.2 Contributions méthodologiques

**Méthodologie reproductible** :

Documentation complète permettant reproduction exacte de l'étude :
- Configuration RIPE Atlas détaillée (JSON complet)
- Pipeline de traitement open source (GitHub)
- Schémas de données (Avro, Parquet)
- Analyses statistiques reproductibles (notebooks Jupyter)

**Best practices RIPE Atlas** :

Méthodologie réutilisable pour futures études DNS distribuées :
- Stratégie sélection sondes (4 critères + pondération géographique)
- Gestion interférence (filtrage hardware, tolérance timing)
- Optimisation crédits (4 stratégies documentées)
- Filtrage qualité (3 filtres + taux exclusion attendus)

**Architecture système** :

Adaptation OpenINTEL pour RIPE Atlas :
- Pipeline 5 étapes (Input → Measurement → Collection → Storage → Analysis)
- Stockage 2-tiers (Avro + Parquet)
- Analyses quantitatives Q1-Q4 avec code Python complet

### 5.3.3 Contributions de données

**Dataset public** :

Publication d'un dataset unique combinant :
- [XX millions] de mesures DNS
- Couverture Tranco Top 10K
- Distribution mondiale (~100 vantage points, 6 continents)
- Période longitudinale [X mois]
- Format FAIR (Findable, Accessible, Interoperable, Reusable)

**Accessibilité** :
- DOI Zenodo permanent : [À attribuer]
- Licence CC BY 4.0 (réutilisation libre avec attribution)
- Formats ouverts (Avro, Parquet, CSV)
- Documentation méthodologique complète
- Scripts d'analyse fournis

**Impact attendu** :

Ce dataset permettra :
- Validation/comparaison avec futures études DNS
- Analyses secondaires (questions non explorées ici)
- Enseignement (exemples réels pour cours réseaux/sécurité)
- Benchmark pour nouveaux algorithmes (CDN selection, anycast routing)

---

## 5.4 Perspectives et travaux futurs

### 5.4.1 Extensions immédiates

**Extension temporelle** :

Poursuivre la collecte au-delà de [X mois] pour :
- Capturer tendances saisonnières (été vs hiver, événements commerciaux)
- Identifier migrations CDN long-terme
- Valider stabilité temporelle sur années
- Corréler avec événements géopolitiques/techniques

**Extension spatiale** :

Améliorer couverture géographique :
- Cibler déploiement sondes en Asie, Afrique, Am. Sud (régions sous-représentées)
- Collaborer avec opérateurs locaux (ISP, universités)
- Valider si régions sous-représentées apportent diversité critique

**Extension thématique** :

Étendre types de mesures :
- **IPv6** : Mesures AAAA records (adoption IPv6, diversité géographique IPv6 vs IPv4)
- **Email** : MX records (centralisation infrastructure email)
- **Délégation** : NS records (structure hiérarchique DNS)
- **DNSSEC** : DS, DNSKEY records (adoption sécurité DNS)

### 5.4.2 Nouvelles questions de recherche

**Q5 : Diversité IPv6 vs IPv4** :

Les réponses DNS IPv6 (AAAA) présentent-elles la même diversité géographique que IPv4 (A) ?
- Hypothèse : IPv6 adoption moindre → potentiellement moins de diversité CDN
- Méthode : Mesures dual-stack (A + AAAA) depuis mêmes vantage points
- Impact : Informer migration IPv6

**Q6 : Corrélation avec incidents sécurité** :

Peut-on détecter précocement campagnes malveillantes via anomalies DNS ?
- Approche : Combiner nos données historiques avec feeds malware (URLhaus, Abuse.ch)
- Méthode : Identifier patterns DNS précédant inclusion blacklists
- Impact : Détection proactive phishing/C&C

**Q7 : Centralisation email vs web** :

La centralisation DNS (Xu et al., 2023) affecte-t-elle également l'infrastructure email ?
- Méthode : Analyse MX records Tranco Top 10K
- Comparaison : Providers web (Cloudflare, AWS) vs email (Google Workspace, Microsoft 365)
- Impact : Souveraineté numérique, RGPD

### 5.4.3 Améliorations méthodologiques

**Machine Learning pour CDN classification** :

Notre identification providers CDN est heuristique (AS mapping, patterns). Amélioration :
- **Features** : TTL, nombre IPs, patterns géographiques, AS, réponses NSID
- **Labels** : Validation manuelle échantillon + datasets publics (CDNPlanet)
- **Modèle** : Random Forest ou Gradient Boosting
- **Validation** : Précision >95% sur test set

**Détection automatique lying resolvers** :

Notre filtre lying resolvers utilise seuils fixes (5% fréquence). Amélioration :
- **Approche** : Clustering réponses DNS (DBSCAN, Isolation Forest)
- **Features** : Réponses DNS, RTT, géolocalisation resolver, AS
- **Validation** : Comparaison avec baseline OpenINTEL (ground truth)

**Causalité TTL ↔ changement** :

Notre analyse montre corrélation mais pas causalité. Pour démontrer causalité :
- **Approche** : Réseaux bayésiens (Hours et al., 2016) ou do-calculus
- **Variables** : TTL, fréquence changement, type domaine, provider CDN
- **Impact** : Guider configuration TTL optimale

### 5.4.4 Collaborations et partenariats

**OpenINTEL** :

Collaboration potentielle :
- **Apport mutuel** : OpenINTEL exhaustivité (.com complet) vs notre diversité géo
- **Étude jointe** : Comparer réponses DNS même domaine (OpenINTEL NL vs nos 100 points)
- **Validation** : Identifier domaines où localisation change réponses

**RIPE NCC** :

Contribution communauté RIPE Atlas :
- **Publication RIPE Labs** : Article vulgarisation résultats
- **Présentation RIPE Meeting** : Partager méthodologie, best practices
- **Feedback plateforme** : Suggérer améliorations API, documentation

**Universités partenaires** :

Extension multi-sites avec infrastructures complémentaires :
- **M-Lab** : Plateforme mesures similaire, couverture différente
- **PlanetLab** : Infrastructure académique distribuée
- **Validation croisée** : Comparer résultats RIPE Atlas vs autres plateformes

---

## 5.5 Conclusion générale

### 5.5.1 Synthèse du mémoire

Ce mémoire a abordé la problématique de l'**archivage DNS spatialement et temporellement distribué**, en réponse à une limitation majeure des infrastructures existantes : l'absence de diversité géographique dans les mesures DNS.

**Nos contributions** :

1. **Empirique** : Quantification de la diversité géographique ([XX%] domaines Tranco Top 10K), stabilité temporelle (X.X% changement quotidien), impact biais RIPE Atlas et choix resolver.

2. **Méthodologique** : Conception et validation d'un système de mesures DNS distribuées combinant Tranco + RIPE Atlas, avec pipeline reproductible et best practices documentées.

3. **Données** : Publication dataset public ([XX millions] mesures) conforme FAIR principles, réutilisable par la communauté scientifique.

**Validation hypothèses** :

Nos résultats empiriques [confirment / infirment / nuancent] les hypothèses de la littérature sur CDN, anycast, ECS et centralisation DNS. [Détail selon résultats Q1-Q4].

### 5.5.2 Réponse à la problématique

**Question initiale** : Comment concevoir et déployer un système d'archivage DNS qui capture la diversité géographique des réponses DNS dans le temps ?

**Réponse** : Notre système opérationnel, déployé durant [X mois], démontre qu'il est **techniquement faisable et scientifiquement pertinent** d'archiver DNS de manière distribuée. Les résultats quantitatifs valident que :

1. **La diversité géographique est significative** : [XX%] des domaines populaires varient selon la localisation, justifiant l'approche distribuée.

2. **La stabilité temporelle est hétérogène** : [XX%] domaines stables (mesures hebdomadaires suffisantes) vs [X%] volatiles (quotidien nécessaire).

3. **Les biais sont gérables** : Le biais RIPE Atlas [impacte modérément / significativement] les résultats, mais avec transparence et pondération, les conclusions restent [valides / interprétables].

4. **Le choix de resolver importe** : DNS publics vs ISP locaux [divergent significativement / convergent avec ECS], informant les stratégies de mesure futures.

### 5.5.3 Impact attendu

**Recherche académique** :

- **Performance réseau** : Dataset pour valider modèles CDN, optimisation anycast, protocoles EDNS
- **Sécurité** : Archivage historique pour investigation incidents, détection campagnes malveillantes
- **Mesures Internet** : Méthodologie réutilisable pour autres études RIPE Atlas
- **Enseignement** : Cas d'étude réel pour cours réseaux, DNS, mesures distribuées

**Industrie et opérateurs** :

- **CDN providers** : Insights sur distribution géographique effective, comparaisons compétitives
- **DNS providers** : Validation stratégies ECS, identification domaines à améliorer
- **Régulateurs** : Données objectives sur centralisation infrastructure DNS (souveraineté numérique)

**Politiques publiques** :

- **Souveraineté numérique** : Quantification dépendance providers étrangers (Cloudflare, Google, AWS)
- **RGPD** : Impact ECS sur privacy (exposition préfixe IP clients)
- **Résilience** : Identification single points of failure (centralisation documentée par Xu et al., 2023)

### 5.5.4 Leçons apprises

**Techniques** :

- RIPE Atlas est une plateforme puissante mais nécessite rigueur méthodologique (interférence, biais)
- Stockage 2-tiers (Avro + Parquet) efficace pour gros volumes (ratio compression 1:X.X)
- Filtrage qualité données crucial (XX% résultats exclus mais XX% valides suffisant)

**Scientifiques** :

- Diversité géographique DNS [plus importante / moins importante] qu'anticipé
- TTL ≠ bon prédicteur changements (corrélation [faible / inexistante])
- ECS adoption [résout partiellement / ne résout pas] problème remote DNS

**Méthodologiques** :

- Reproductibilité nécessite versioning complet (code, données, paramètres)
- Trade-offs inévitables (exhaustivité vs faisabilité, précision vs coût)
- Transparence sur limitations essentielle pour validité scientifique

### 5.5.5 Message final

Le DNS, infrastructure invisible et critique d'Internet, évolue constamment. Sa nature éphémère et géographiquement diverse nécessite des approches de mesure **distribuées**, **longitudinales** et **transparentes**.

Ce mémoire démontre qu'avec des outils communautaires (RIPE Atlas), des listes robustes (Tranco) et une méthodologie rigoureuse, il est possible de capturer cette complexité et de la rendre accessible à la communauté scientifique.

Les [XX millions] de mesures DNS collectées, désormais publiques, constituent une **photographie spatio-temporelle** d'Internet en [année 2026]. Elles serviront de référence pour comparer l'évolution future, valider des modèles théoriques, et informer les décisions techniques et politiques sur l'architecture d'Internet.

**Notre espoir** : Que ce travail inspire d'autres chercheurs à étendre ces mesures, combler les lacunes identifiées (couverture géographique, types d'enregistrements, durée longitudinale), et contribuer collectivement à une meilleure compréhension de l'infrastructure DNS mondiale.

Comme l'écrivait Stéphane Bortzmeyer : *"Le DNS est souvent oublié dans les études de résilience et qualité de service d'Internet"*. Ce mémoire est une modeste contribution pour le rendre **visible**, **mesurable** et **compréhensible**.

---

**Fin du Chapitre 5 - Discussion et conclusion**
