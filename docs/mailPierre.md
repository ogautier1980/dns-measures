# Notes et références - Réunion avec Pierre

**Date** : Jeudi (date non spécifiée)

---

## Récapitulatif des références

### Conférences orientées sécurité

- **IEEE Symposium on Security and Privacy (IEEE S&P)**
- **IEEE European Symposium on Security and Privacy (IEEE European S&P)**
- **Network and Distributed System Security (NDSS)**
- **USENIX Security**
- **Proceedings on Privacy Enhancing Technologies (PoPETS)**
- **ACM Computing Classification System (ACM CCS)**

> Pierre a commencé à éplucher les deux premières.

### Conférences orientées réseaux

- **ACM Special Interest Group on Data Communication (SIGCOMM)**

---

## Requêtes Scopus

Requêtes utilisées sur Scopus pour identifier les papiers qui citent **TRANCO** ou **OpenINTEL** :

**URL de recherche avancée :**
https://www.scopus.com/search/form.uri?display=advanced&zone=header&origin=searchadvanced

**Requêtes :**

```
REFEID(2-s2.0-85170646912) AND (CONFNAME(IEEE Symposium on Security and Privacy) OR CONFNAME(IEEE European Symposium on Security and Privacy))

REFEID(2-s2.0-84976412290) AND (CONFNAME(IEEE Symposium on Security and Privacy) OR CONFNAME(IEEE European Symposium on Security and Privacy))
```

---

## Ressources et outils

### Base de données Geo-IP

**MaxMind Geo-IP Demo :**
https://www.maxmind.com/en/geoip-web-services-demo

> Il existe d'autres bases de données, potentiellement certaines en libre accès.

### Liste de résolveurs DNS

**Repository GitHub - Trickest Resolvers :**
https://github.com/trickest/resolvers/tree/main

### Issue GitHub - Prof. Rochet

**Problématique liée au projet :**
https://github.com/shadow/shadow-plugin-tor/issues/63

---

## Échange de mails avec Stéphane Bortzmeyer

### Sujet : Mesures DNS distribuées dans l'espace et le temps

---

## Premier message - Jules Dejaeghere

**FROM:** jules.dejaeghere@unamur.be
**TO:** stephane+blog@bortzmeyer.org
**DATE:** Mercredi 1er octobre 2025, 16:06:37 GMT+02:00

### Contexte

Bonjour Stéphane Bortzmeyer,

Je suis chercheur à l'Université de Namur et certaines de mes recherches portent sur le DNS. Après discussion avec mes collègues (en copie), certains m'ont dirigé vers votre blog. Au vu de votre expertise en matière de DNS, je vous contacte pour avoir votre avis et éventuelles remarques à propos d'un projet de recherche.

### Objectif de recherche

Je suis à la recherche de **données DNS distribuées dans le temps et l'espace**. Certains projets en cours impliquent des simulations d'Internet, mais les données concernant la résolution d'un nom de domaine en particulier, dans le passé et à un endroit donné, est un élément manquant que nous devons approximer.

**Problème actuel :**
Généralement, nous résolvons le domaine en son adresse IP au moment de l'exécution de l'expérience en utilisant un serveur local. Cela ne représente pas forcément la réponse qui aurait été reçue si un client avait fait la même requête il y a plusieurs années et ne tient pas non plus compte de la localisation du client qui peut influencer la réponse DNS pour des raisons de performance.

### Approche envisagée

N'ayant pas trouvé de données publiquement disponibles pour la résolution de noms de domaines dans le temps et l'espace, nous envisageons de construire cette base de données et de la rendre accessible.

**Méthodologie proposée :**

1. **Scanner Internet IPv4** à la recherche de résolveurs DNS publics
2. **Filtrer les résolveurs identifiés** pour ne garder que ceux qui ne mentent pas dans leurs réponses et qui peuvent éthiquement être utilisés pour nos mesures
3. **Localiser les résolveurs retenus** (geo-IP et ASN)
4. **Utiliser ces résolveurs** pour résoudre régulièrement des noms de domaines (issus de sources à identifier, mais sûrement la Tranco list [1] et les logs du système de certificate transparency)
5. **Rendre ces données accessibles** pour d'autres chercheurs (modalités encore à définir)

**Note :** La liste de résolveurs utilisés serait mise à jour à l'aide de scans IPv4 réguliers. Les scans seront publiquement documentés et un mécanisme d'opt-out sera prévu pour les administrateurs qui ne veulent plus que leurs adresses soient scannées.

Si la couverture géographique ou au niveau des AS n'est pas satisfaisante en utilisant les résolveurs publics identifiés, nous pensons utiliser les **sondes de RIPE Atlas** en complément [2].

### Questions

1. **Avez-vous connaissance de travaux similaires ?**
   - La recherche la plus proche identifiée jusqu'à présent est celle de Roland van Rijswijk-Deij et al. [3] (https://www.openintel.nl/)
   - Leurs mesures ne sont pas géographiquement distribuées
   - Les données sont accessibles uniquement sur demande car les chercheurs ont des accords privilégiés avec les gestionnaires de certains TLDs pour obtenir une liste complète des domaines de second niveau

2. **Hypothèse de localisation :**
   - Nous partons de l'hypothèse qu'un serveur DNS localisé par exemple à Tokyo nous donnera une vue similaire à ce que les internautes de Tokyo pourraient observer, même si nous envoyons notre requête depuis la Belgique
   - Cependant, certains résolveurs pourraient répondre différemment sur base de la localisation du client
   - **Auriez-vous des ressources qui permettent de quantifier ce phénomène ?**

3. **Avez-vous des remarques ou ressources pertinentes** qui pourraient nous aider dans ce projet de recherche ?

D'avance merci pour votre réponse.

Cordialement,

**Jules Dejaeghere**
PhD Student · Researcher
Computer Science Faculty
Université de Namur
jules.dejaeghere@unamur.be
https://directory.unamur.be/staff/jdejaegh

### Références

**[1]** Le Pochat, V., Van Goethem, T., Tajalizadehkhoob, S., Korczynski, M., & Joosen, W. (2019). *Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation*. Proceedings 2019 Network and Distributed System Security Symposium. https://doi.org/10.14722/ndss.2019.23386

**[2]** RIPE Atlas Documentation. Retrieved April 9, 2025, from https://atlas.ripe.net/docs/

**[3]** van Rijswijk-Deij, R., Jonker, M., Sperotto, A., & Pras, A. (2016). *A High-Performance, Scalable Infrastructure for Large-Scale Active DNS Measurements*. IEEE Journal on Selected Areas in Communications, 34(6), 1877–1888. https://doi.org/10.1109/JSAC.2016.2558918

---

## Réponse 1 - Stéphane Bortzmeyer

**FROM:** stephane+blog@bortzmeyer.org
**TO:** jules.dejaeghere@unamur.be
**DATE:** Mercredi 1er octobre 2025, 19:02:39 GMT+02:00

### Résumé

Pour résumer la problématique :

- **Distribution dans l'espace** : les sondes Atlas
- **Distribution dans le temps** : utiliser (ou monter soi-même) une base de "passive DNS"

### Détails et remarques

#### 1. Scanner Internet IPv4 à la recherche de résolveurs DNS publics

> Je ne vois pas bien ce que les résolveurs publics apporteraient, par rapport aux sondes Atlas. Et je vois leurs inconvénients : **ils sont très inégalement répartis**.

#### 2. Filtrer les résolveurs identifiés

**Point de vue éthique :**

Article pertinent : [Ethics of RIPE Atlas Measurements](https://labs.ripe.net/author/kistel/ethics-of-ripe-atlas-measurements/)

Il faut bien différencier :

- **Résolveurs publics** (Google Public DNS, Quad9, dns.sb, DNS4ALL, etc.) : Le sont volontairement → pas de problèmes éthiques majeurs
- **Résolveurs ouverts** : Le sont par oubli ou négligence → pas forcément éthique de les utiliser

**Clarification :**
Quand vous parliez de "scanner Internet IPv4 à la recherche de résolveurs DNS publics", je suppose que vous parliez en fait de **résolveurs ouverts**. Pour les publics, pas besoin de scan, ils sont connus et documentés. Et ce scan soulève en effet des questions éthiques.

#### 5. Rendre ces données accessibles

Les bases de "passive DNS" existantes sont des sacrés morceaux, vu la **quantité de données**, et leur accessibilité par un assez large public est donc un **beau défi technique**.

#### Si la couverture géographique n'est pas satisfaisante

> **Pourquoi ne pas utiliser que les sondes Atlas, qui sont faites pour cela ?**

#### 2. Hypothèse de localisation et ECS

**Oui, par exemple si le résolveur utilise ECS (RFC 7871).**

Test avec les sondes Atlas en Belgique :

```bash
% blaeu-resolve --requested 100 --country BE --type TXT ecs.dyn.bortzmeyer.fr
[""] : 87 occurrences
… [j'ai omis les réponses avec ECS mais elles sont très peu nombreuses]
```

**Conclusion :** Très peu de sondes Atlas en Belgique utilisent un résolveur qui fait de l'ECS (c'est bon pour la vie privée, et aussi pour votre recherche).

**Solution :** Envoyer au résolveur une option ECS qui coupe ce service (en espérant que le résolveur obéisse ; Google Public DNS le fait).

```bash
% dig +short @dns.google ecs.dyn.bortzmeyer.fr TXT
"2a01:e34:ec43:e100::/56"

% dig +short +subnet=0/0 @dns.google ecs.dyn.bortzmeyer.fr TXT
""
```

#### 3. Remarques et ressources

Prendre contact avec les gestionnaires de bases de "passive DNS" existantes :
- Leur demander s'ils sont prêts à vous faire un prix (ces services sont typiquement coûteux)
- Ou regarder lesquels ont documenté leur configuration technique, pour pouvoir la reproduire

---

## Réponse 2 - Jules Dejaeghere

**FROM:** jules.dejaeghere@unamur.be
**TO:** stephane+blog@bortzmeyer.org
**DATE:** Jeudi 9 octobre 2025, 13:54:44 GMT+02:00

Bonjour,

Merci pour la réponse détaillée. Je réponds dans le corps ci-dessous.

### Sondes Atlas - Limitations

Les sondes Atlas ont cet avantage, mais les **quotas annoncés par RIPE** [1] semblent limitants.

**Options :**
- Nous pourrions contacter RIPE pour proposer nos mesures et obtenir une exception
- Je ne sais pas à quel point RIPE accorde ces exceptions

Le **nombre de crédits RIPE** dont nous disposons est aussi une limite pour le moment.

### Résolveurs publics vs ouverts

Je suis effectivement à la recherche de **résolveurs ouverts** avec ce scan.

**Objectif :**
Les résolveurs publics peuvent aider mais ne fourniront sans doute pas une vue globale. L'objectif du scan pour trouver des résolveurs ouverts est de combler ces trous dans notre couverture.

**Idéal :**
Obtenir une liste de résolveurs **volontairement ouverts** mais qui ne sont pas forcément annoncés publiquement : je pense par exemple à :
- Résolveurs fournis par des FAI pour leurs clients
- Résolveurs d'universités ou similaires

**Question :** Auriez-vous une liste de résolveurs publics ou une source fiable à ce sujet ?

### ECS (EDNS Client Subnet)

Merci pour la piste concernant RFC 7871 et les tests avec les sondes Atlas.

### Données passives DNS et coûts

Les fournisseurs affichent des prix fort onéreux et ces données pourraient nous aider seulement pour **un des deux objectifs** de la recherche.

**Deux objectifs :**

1. **Évaluer l'impact des données DNS dans nos simulations d'Internet**
   - Possible avec les données payantes de passive DNS

2. **Rendre ces données disponibles pour d'autres chercheurs**
   - Plus difficile à concevoir si nous achetons les données auprès d'un fournisseur commercial qui limitera sûrement l'utilisation que nous pouvons faire des données

**[1]** https://atlas.ripe.net/docs/getting-started/user-defined-measurements#quotas

Cordialement,

Jules Dejaeghere

---

## Réponse 3 - Stéphane Bortzmeyer

**FROM:** stephane+blog@bortzmeyer.org
**TO:** jules.dejaeghere@unamur.be
**DATE:** Jeudi 9 octobre 2025

### Quotas et crédits RIPE Atlas

> Les quotas annoncés par RIPE [1] semblent limitants. Nous pourrions contacter RIPE pour proposer nos mesures et obtenir une exception. Je ne sais pas à quel point RIPE accorde ces exceptions.

**Réponse :** Je ne sais pas non plus mais l'**équipe Atlas est composée de gens sympas et qui répondent**, il ne faut pas hésiter à leur demander.

> Le nombre de crédits RIPE dont nous disposons est aussi une limite pour le moment.

**Réponse :** **Ça, ce n'est pas un problème.** C'est toutes les semaines que, sur la liste, un étudiant ou une chercheuse demande des crédits, en décrivant sa recherche en deux paragraphes, et ielle a tout de suite des **millions de crédits**.

### Résolveurs publics

> Les résolveurs publics peuvent aider mais ne fourniront sans doute pas une vue globale. L'objectif du scan pour trouver des résolveurs ouverts est de combler ces trous dans notre couverture. L'idéal serait d'obtenir une liste de résolveurs volontairement ouverts mais qui ne sont pas forcément annoncés publiquement : je pense par exemple à des résolveurs fournis par des FAI pour leurs clients, des résolveurs d'universités ou similaires.

**Réponse :** Ceux-ci ne sont **quasiment jamais ouverts**.

> Auriez-vous une liste de résolveurs publics ou une source fiable à ce sujet ?

**Réponse :** https://www.chaz6.com/files/resolv.conf

### Données pour d'autres chercheurs

> Nous voulons également que ces données puissent être disponibles pour d'autres chercheurs. Cela semble plus difficile à concevoir si nous achetons les données auprès d'un fournisseur commercial qui limitera sûrement l'utilisation que nous pouvons faire des données.

**Réponse :** Je comprends très bien. Mais monter une base comme celle que vous envisagez, avec accès public, est un **travail non négligeable**.

---

## Points clés à retenir

### ✅ Recommandations de Stéphane Bortzmeyer

1. **Utiliser principalement les sondes RIPE Atlas**
   - Bien distribuées géographiquement
   - Équipe réactive et disposée à aider
   - Crédits facilement obtenables pour la recherche

2. **Éviter le scan de résolveurs ouverts**
   - Questions éthiques importantes
   - Résolveurs universitaires/FAI rarement ouverts volontairement
   - Résolveurs publics connus suffisent probablement

3. **Problème ECS (EDNS Client Subnet)**
   - Peu utilisé en pratique (bon pour la vie privée)
   - Solution : envoyer option ECS +subnet=0/0 pour le désactiver

4. **Passive DNS**
   - Bases existantes volumineuses et coûteuses
   - Monter sa propre base = défi technique important
   - Licences commerciales limitent le partage

### 📌 Ressources identifiées

- **Liste de résolveurs publics** : https://www.chaz6.com/files/resolv.conf
- **Liste de résolveurs (GitHub)** : https://github.com/trickest/resolvers/tree/main
- **Article éthique RIPE Atlas** : https://labs.ripe.net/author/kistel/ethics-of-ripe-atlas-measurements/
- **Base Geo-IP** : https://www.maxmind.com/en/geoip-web-services-demo

### 🎯 Actions à considérer

1. Contacter l'équipe RIPE Atlas pour :
   - Demander des crédits supplémentaires
   - Discuter d'exceptions aux quotas
   - Présenter le projet de recherche

2. Se concentrer sur RIPE Atlas plutôt que sur le scan de résolveurs

3. Évaluer la faisabilité technique d'une base passive DNS publique
