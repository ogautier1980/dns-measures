# Guide de recherche bibliographique - État de l'art

**Projet** : Mesures DNS dans l'espace et le temps
**Auteur** : Olivier Gautier
**Date de création** : 20 janvier 2026

---

## Vue d'ensemble

Ce document contient toutes les requêtes et stratégies de recherche pour construire l'état de l'art du mémoire, conformément à la structure définie dans le roadmap (Chapitre 2).

### Structure de l'état de l'art

- **Section 2.1** : Système DNS (rappels techniques)
- **Section 2.2** : Mesures DNS actives vs passives
- **Section 2.3** : Infrastructure OpenINTEL
- **Section 2.4** : Liste Tranco pour classement sites
- **Section 2.5** : RIPE Atlas et mesures distribuées
- **Section 2.6** : Travaux connexes (CDN, géo-localisation, DNSSEC)
- **Section 2.7** : Synthèse et positionnement

---

## Articles clés déjà identifiés

### Articles fondateurs (fiches créées)

1. **OpenINTEL Infrastructure** ✅
   - van Rijswijk-Deij et al. (2016) - IEEE JSAC
   - Fiche : [sources/fiches/vanRijswijk2016_openintel.md](../sources/fiches/vanRijswijk2016_openintel.md)
   - Contribution : Infrastructure centralisée mesures DNS, limitation = 1 point de mesure

2. **Tranco Ranking** ✅
   - Le Pochat et al. (2019) - NDSS
   - Fiche : [sources/fiches/lePochat2019_tranco.md](../sources/fiches/lePochat2019_tranco.md)
   - Contribution : Liste stable domaines, résistante manipulation

3. **RIPE Atlas Day in the Life** ✅
   - Nosyk et al. (2024) - arXiv:2511.22474v1
   - Fiche : [sources/fiches/nosyk2024_ripeatlas_ditl.md](../sources/fiches/nosyk2024_ripeatlas_ditl.md)
   - Contribution : Analyse infrastructure RIPE Atlas, 12.9K sondes, 178 pays, biais géographique

### Articles pertinents trouvés (à lire et ficher)

**RIPE Atlas et DNS** :
- [ ] Bortzmeyer, S. - "DNS Measurements with RIPE Atlas" (RIPE presentation)
  - URL : https://www.ripe.net/media/documents/DNS-Measurements-with-RIPE-Atlas.pdf
  - Intérêt : Tutorial pratique mesures DNS avec Atlas

- [ ] Bajpai & Schönwälder - "Benefits and Limitations of RIPE Atlas Tags" (IM 2017)
  - URL : https://vaibhavbajpai.com/documents/papers/proceedings/ripeatlas-im-2017.pdf
  - Intérêt : Organisation et tags mesures RIPE Atlas

- [ ] "Quantifying Interference between Measurements on the RIPE Atlas Platform" (IMC 2015)
  - URL : https://conferences2.sigcomm.org/imc/2015/papers/p437.pdf
  - Intérêt : Impact mesures simultanées, DNS delays

- [ ] "Detecting DNS Root Manipulation" (ICIR)
  - URL : https://www.icir.org/mallman/pubs/JFP+16/JFP+16.pdf
  - Intérêt : Détection manipulation DNS via RIPE Atlas

**Applications RIPE Atlas** :
- [ ] "RIPEn at Home – Surveying Internal Domain Names using RIPE Atlas" (TMA 2024)
  - URL : https://dl.ifip.org/db/conf/tma/tma2024/tma2024poster-final1.pdf
  - Intérêt : Mesures DNS internes avec Atlas

**OpenINTEL évolution** :
- [ ] "The Ongoing Story of OpenINTEL: Measuring the DNS for Research" (NLnet Labs blog)
  - URL : https://blog.nlnetlabs.nl/the-ongoing-story-of-openintel/
  - Intérêt : Évolution OpenINTEL post-2016, nouveaux TLDs

**Tranco utilisation** :
- [ ] Scott Helme - Security scans on Tranco list
  - URL : https://tranco-list.eu/ (cited applications)
  - Intérêt : Cas d'usage sécurité (HTTPS, DMARC)

- [ ] Why No HTTPS? - Project using Tranco
  - Intérêt : Adoption HTTPS basée sur Tranco

### Ressources documentation

**RIPE Atlas** :
- Documentation officielle : https://atlas.ripe.net/docs/
- RIPE Labs blog DNS : https://labs.ripe.net/author/kistel/dns-measurements-with-ripe-atlas-data/
- Hackathon DNS : https://atlas.ripe.net/hackathon/dns-measurements/
- Best practices : https://atlas.ripe.net/docs/howtos/best-practices/

**OpenINTEL** :
- Site principal : https://www.openintel.nl/
- Accès données : https://openintel.nl/data/
- CAIDA catalog : https://catalog.caida.org/dataset/openintel_active_dns

**Tranco** :
- Site principal : https://tranco-list.eu/
- Python package : https://pypi.org/project/tranco/
- Liste avec SSO : https://sso-monitor.me/list

---

## Requêtes IEEE Xplore

### 1. Infrastructure de mesures DNS distribuées

**Requête principale** :
```
("DNS measurement" OR "DNS monitoring" OR "DNS infrastructure")
AND ("distributed" OR "geographic*" OR "spatial")
```

**Filtres recommandés** :
- Date : 2015-2026 (dernières 10 ans)
- Type : Conference Papers, Journal Articles
- Conférences : INFOCOM, SIGCOMM, IMC, PAM

**Pour** : Sections 2.2, 2.3

---

### 2. RIPE Atlas et mesures actives

**Requête principale** :
```
("RIPE Atlas" OR "active DNS measurement*" OR "active probing")
AND (DNS OR "domain name system")
```

**Requête affinée** :
```
"RIPE Atlas" AND (DNS OR resolver OR authoritative)
```

**Pour** : Sections 2.2, 2.5

---

### 3. Archivage et historique DNS

**Requête principale** :
```
("DNS archive" OR "DNS history" OR "temporal DNS" OR "DNS dataset")
AND (measurement* OR observation*)
```

**Variante passive DNS** :
```
("passive DNS" OR "pDNS") AND (archive OR historical OR dataset)
```

**Pour** : Sections 2.2, 2.3

---

### 4. Diversité géographique DNS (CDN, anycast)

**Requête principale** :
```
(DNS AND (CDN OR "content delivery" OR anycast OR geolocation))
AND (measurement* OR observation* OR study)
```

**Requête affinée** :
```
("geo-location" OR "geographic diversity") AND DNS AND (response* OR resolution)
```

**Pour** : Section 2.6

---

### 5. DNS et sécurité (DNSSEC, cache poisoning)

**Requête principale** :
```
DNS AND (DNSSEC OR security OR attack* OR "cache poisoning" OR abuse)
AND measurement*
```

**Conférences ciblées** : IEEE S&P, NDSS, USENIX Security

**Pour** : Section 2.6

---

### 6. Listes de domaines et classements (Tranco, Alexa)

**Requête principale** :
```
("domain ranking" OR "top sites" OR Tranco OR Alexa OR "domain list")
AND (measurement* OR study OR analysis)
```

**Requête affinée** :
```
("web ranking" OR "popularity list") AND (stability OR manipulation OR methodology)
```

**Pour** : Section 2.4

---

### 7. ECS (EDNS Client Subnet) et optimisation DNS

**Requête principale** :
```
("EDNS Client Subnet" OR ECS OR "RFC 7871")
AND (measurement* OR deployment OR analysis)
```

**Variante** :
```
DNS AND ("client subnet" OR "geographic optimization" OR "latency reduction")
```

**Pour** : Section 2.6

---

### 8. OpenINTEL et infrastructures similaires

**Requête principale** :
```
OpenINTEL OR ("large-scale DNS" AND infrastructure)
OR ("DNS measurement platform" OR "DNS observatory")
```

**Pour** : Section 2.3

---

### 9. Études temporelles DNS (stabilité, évolution)

**Requête principale** :
```
DNS AND (temporal OR evolution OR stability OR "time series" OR longitudinal)
AND (measurement* OR study)
```

**Pour** : Sections 2.2, 2.6

---

### 10. Partage de données et reproductibilité

**Requête principale** :
```
("DNS dataset" OR "DNS data sharing")
AND (research OR reproducib* OR open)
```

**Pour** : Sections 2.3, 2.7

---

## Stratégie de recherche par phase

### Phase 1 : Articles fondamentaux (1-2 jours)

#### Démarrage par citations

1. **Article van Rijswijk-Deij (2016)** - OpenINTEL
   - Chercher "van Rijswijk-Deij" sur IEEE Xplore
   - Consulter "Cited by" (articles qui citent)
   - Consulter "References" (articles cités)
   - Focus : infrastructure DNS à grande échelle

2. **Article Le Pochat (2019)** - Tranco
   - Chercher "Le Pochat" ou "Tranco" sur IEEE Xplore
   - Regarder comparaisons avec Alexa, Umbrella
   - Focus : méthodologie de classement

3. **Documentation RIPE Atlas**
   - Site officiel : https://atlas.ripe.net/docs/
   - Papers utilisant RIPE Atlas
   - Études de cas DNS

#### Auteurs clés à suivre

- **Roland van Rijswijk-Deij** (OpenINTEL, TU Delft)
- **Mattijs Jonker** (DNS measurements, University of Twente)
- **Anna Sperotto** (Network monitoring)
- **Aiko Pras** (Network measurements)
- **Stéphane Bortzmeyer** (AFNIC, expert DNS français)
- **Victor Le Pochat** (Tranco, KU Leuven)
- **Wouter Joosen** (Web security, KU Leuven)

---

### Phase 2 : Revue systématique par section (3-5 jours)

#### Section 2.1 : Système DNS (rappels techniques)

**Sources principales** :
- RFCs officiels IETF :
  - RFC 1034 : Domain Names - Concepts and Facilities
  - RFC 1035 : Domain Names - Implementation and Specification
  - RFC 4033-4035 : DNSSEC (Introduction, Resource Records, Protocol)
  - RFC 7871 : Client Subnet in DNS Queries (ECS)
  - RFC 8499 : DNS Terminology
- Livres de référence :
  - "DNS and BIND" (O'Reilly, 5th edition)
  - "Pro DNS and BIND 10" (Apress)

**Requêtes** : Pas de requête spécifique, se baser sur documentation technique

---

#### Section 2.2 : Mesures DNS actives vs passives

**Requêtes à utiliser** : 1, 2, 3

**Concepts à couvrir** :
- Différence active/passive DNS
- Avantages et inconvénients de chaque approche
- Infrastructures existantes
- Challenges de scalabilité
- Considérations éthiques

**Articles clés à trouver** :
- Comparaisons méthodologiques
- Études de déploiement
- Analyses de performance

---

#### Section 2.3 : Infrastructure OpenINTEL

**Requêtes à utiliser** : 8

**Article fondateur** :
📄 van Rijswijk-Deij, R., Jonker, M., Sperotto, A., & Pras, A. (2016)
*A High-Performance, Scalable Infrastructure for Large-Scale Active DNS Measurements*
IEEE Journal on Selected Areas in Communications, 34(6), 1877–1888

**Aspects à analyser** :
- Architecture en 3 étages (collecte, mesure, stockage)
- Technologies utilisées (LDNS, Apache Avro, Parquet)
- Stratégie de distribution de charge (query pacing)
- Métriques de performance (2 milliards requêtes/jour)
- Impact minimal (0.3-1.6% trafic DNS global)
- Limitations et défis

**Questions critiques** :
- Comment adapter pour mesures géographiquement distribuées ?
- Quelles optimisations possibles avec contraintes crédits RIPE ?
- Comment réduire volume stockage sans perte d'information ?

---

#### Section 2.4 : Liste Tranco pour classement sites

**Requêtes à utiliser** : 6

**Article fondateur** :
📄 Le Pochat, V., Van Goethem, T., Tajalizadehkhoob, S., Korczynski, M., & Joosen, W. (2019)
*Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation*
NDSS 2019

**Aspects à analyser** :
- Problèmes listes commerciales (instabilité, manipulation)
- Méthode d'agrégation (Borda count, Dowdall rule)
- Moyennage temporel (30 jours par défaut)
- Filtres de qualité (réactivité, malveillance)
- Amélioration stabilité : 0.6% vs 50% changement quotidien

**Comparaisons à chercher** :
- Tranco vs Alexa
- Tranco vs Cisco Umbrella
- Tranco vs Majestic Million

**Questions pour le mémoire** :
- Quelle taille de liste utiliser ? (Top 1K, 10K, 100K, 1M ?)
- Filtres supplémentaires nécessaires ?
- Gestion des domaines non-réactifs ?
- Fréquence de mise à jour ?

---

#### Section 2.5 : RIPE Atlas et mesures distribuées

**Requêtes à utiliser** : 2

**Article récent clé** :
📄 Nosyk, Y., et al. (2024) - "Day in the Life of RIPE Atlas" - arXiv:2511.22474v1
✅ **Fiche créée** : [sources/fiches/nosyk2024_ripeatlas_ditl.md](../sources/fiches/nosyk2024_ripeatlas_ditl.md)

**Documentation officielle** :
- https://atlas.ripe.net/docs/
- https://atlas.ripe.net/docs/api/v2/
- https://labs.ripe.net/ (RIPE Labs articles)

**Statistiques clés (février 2024)** :
- **12,892 sondes actives** + **810 ancres**
- **178 pays** couverts
- **88K mesures DNS quotidiennes** (type majoritaire avec ping)
- **1.3 milliards résultats/jour**
- **~26,000 résultats par mesure** (moyenne)
- **Biais géographique** : Allemagne + USA = 28% des vantage points
- **Dual-stack** : 46.5% sondes, 92% ancres

**Aspects à couvrir** :
- Architecture RIPE Atlas (sondes/ancres)
- Types de sondes (hardware v1-v5, software probes)
- Distribution géographique et biais Europe/NA
- Système de crédits et optimisation
- Types de mesures disponibles (DNS, ping, traceroute, HTTP, TLS, NTP)
- API et outils (Cousteau, Sagan)
- Limitations : crédits, quotas, biais géographique
- Best practices (réutilisation mesures, tags, reproductibilité)

**Cas d'usage DNS identifiés** :
- **DNS manipulation detection** : 69% sondes chinoises bloquées (Meta services)
- **DNSMON** : 4,435 mesures QoS root servers + TLDs
- **Geographic diversity** : réponses DNS varient selon localisation sondes

**Études de cas à chercher** :
- Utilisations académiques de RIPE Atlas pour DNS
- Études CDN avec RIPE Atlas
- Études anycast deployment
- Détection censure/manipulation DNS
- Optimisations et bonnes pratiques
- Considérations éthiques

**Éthique des mesures** :
📄 https://labs.ripe.net/author/kistel/ethics-of-ripe-atlas-measurements/

---

#### Section 2.6 : Travaux connexes

**Requêtes à utiliser** : 4, 5, 7, 9

**Thématiques à couvrir** :

1. **CDN et géo-localisation** (Requête 4)
   - Utilisation DNS pour distribution géographique
   - Anycast DNS
   - Mesures de latence
   - GeoDNS et optimisation

2. **Sécurité DNS** (Requête 5)
   - DNSSEC : déploiement et mesures
   - DNS cache poisoning
   - DDoS via DNS
   - DNS tunneling et abus
   - Validation DNSSEC

3. **EDNS Client Subnet (ECS)** (Requête 7)
   - RFC 7871
   - Impact sur vie privée
   - Déploiement et adoption
   - Effets sur géo-localisation
   - Mesures ECS dans la pratique

4. **Études temporelles** (Requête 9)
   - Évolution DNS dans le temps
   - Stabilité enregistrements
   - Patterns temporels
   - Analyses longitudinales
   - Time-to-live (TTL) et impact

---

#### Section 2.7 : Synthèse et positionnement

**Requêtes à utiliser** : 10

**Objectifs** :
- Synthétiser les approches existantes
- Identifier les lacunes (gaps)
- Positionner la contribution du mémoire
- Justifier les choix méthodologiques

**Éléments à inclure** :
- Tableau comparatif des infrastructures
- Forces/faiblesses des approches
- Originalité de votre approche
- Complémentarité avec OpenINTEL
- Valeur ajoutée : diversité géographique + accessibilité

---

### Phase 3 : Articles récents et tendances (2-3 jours)

**Conférences majeures à surveiller** :

| Conférence | Focus | Période | Importance |
|------------|-------|---------|------------|
| **IMC** | Internet Measurement Conference | Novembre | ⭐⭐⭐ Crucial |
| **PAM** | Passive and Active Measurement | Mars | ⭐⭐⭐ Crucial |
| **SIGCOMM** | Réseaux | Août | ⭐⭐⭐ Majeur |
| **NDSS** | Network & Distributed System Security | Février | ⭐⭐ Important |
| **IEEE S&P** | Security and Privacy | Mai | ⭐⭐ Important |
| **USENIX Security** | Security | Août | ⭐⭐ Important |
| **INFOCOM** | Communications | Mai | ⭐ Pertinent |

**Requête générale pour nouveautés 2023-2026** :
```
DNS AND (measurement OR monitoring OR infrastructure)
AND (2023 OR 2024 OR 2025 OR 2026)
```

**Focus spécial** :
- IMC 2023, 2024, 2025 : Parcourir tous les papiers DNS
- PAM 2023, 2024, 2025 : Idem
- SIGCOMM workshops : DNS/routing

---

## Outils et bases de données

### Bases de données académiques

1. **IEEE Xplore** (principale)
   - URL : https://ieeexplore.ieee.org/
   - Accès : Via université UNamur
   - Focus : Conférences IEEE, journaux techniques

2. **ACM Digital Library**
   - URL : https://dl.acm.org/
   - Focus : SIGCOMM, IMC, CCS
   - Accès : Via université

3. **Google Scholar**
   - URL : https://scholar.google.com/
   - Avantage : Couverture la plus large
   - Utiliser pour trouver PDFs gratuits

4. **arXiv.org**
   - URL : https://arxiv.org/
   - Focus : Preprints récents
   - Section : cs.NI (Networking)

5. **DBLP**
   - URL : https://dblp.org/
   - Utilité : Index complet publications informatique
   - Chercher auteurs et conférences

6. **Semantic Scholar**
   - URL : https://www.semanticscholar.org/
   - Avantage : Graphe de citations, recommandations
   - Bon pour découvrir travaux connexes

### Commandes Scopus

```scopus
REFEID(2-s2.0-85170646912) AND CONFNAME(IEEE Symposium on Security and Privacy)
REFEID(2-s2.0-84976412290) AND CONFNAME(IEEE Symposium on Security and Privacy)
```

### Ressources spécialisées

- **RIPE Labs** : https://labs.ripe.net/
- **CAIDA** (DNS data) : https://www.caida.org/
- **DNS-OARC** : https://www.dns-oarc.net/
- **ICANN Research** : https://www.icann.org/resources/pages/research

---

## Critères de sélection des articles

### Priorité haute ⭐⭐⭐

- ✅ Publié dans conférence/journal reconnu (IEEE, ACM, USENIX)
- ✅ Citations > 10 (sauf si très récent < 2024)
- ✅ Méthodologie claire et reproductible
- ✅ Données ou code disponibles (open science)
- ✅ Peer-reviewed (comité de lecture)
- ✅ Contribution originale clairement identifiée

### Priorité moyenne ⭐⭐

- ⚠️ Workshop papers avec peer-review
- ⚠️ Journaux spécialisés (Computer Networks, etc.)
- ⚠️ Articles récents (< 5 citations si 2024-2025)
- ⚠️ Technical reports d'institutions reconnues

### À éviter ❌

- ❌ Articles de workshop sans peer-review solide
- ❌ Méthodologie floue ou non reproductible
- ❌ Pas de validation expérimentale
- ❌ Trop ancien (>10 ans) sauf article fondateur
- ❌ Prédatory journals
- ❌ Preprints non publiés (sauf très récent et pertinent)

---

## Organisation des résultats

### Gestion bibliographique avec Zotero

**Installation** :
```bash
# Dans le container Docker
apt-get update && apt-get install -y zotero-standalone
```

**Workflow recommandé** :
1. Importer automatiquement depuis IEEE Xplore / ACM (plugin navigateur)
2. Tagger par section état de l'art :
   - `etat-art/dns-rappels`
   - `etat-art/actif-passif`
   - `etat-art/openintel`
   - `etat-art/tranco`
   - `etat-art/ripe-atlas`
   - `etat-art/connexe-cdn`
   - `etat-art/connexe-securite`
   - `etat-art/connexe-ecs`
   - `etat-art/connexe-temporel`
3. Export BibTeX régulier vers `latex/bibliography.bib`
4. Synchronisation cloud (compte Zotero gratuit)

**Commande export BibTeX** :
```
File > Export Library > Format: BibTeX
```

---

### Fiches de lecture

**Template de fiche** (cf. Guide mémoire p.21-22) :

```markdown
# Fiche de lecture

**Référence bibliographique** :
[Auteur, Année] Titre. Conférence/Journal. DOI.

**Thème** :
Section état de l'art concernée

**Intérêt pour le mémoire** :
Pourquoi cet article est pertinent (1-2 phrases)

**Objectif(s) / Question(s) de recherche** :
Qu'est-ce que les auteurs cherchent à résoudre ?

**Cadre global d'explication** :
Théorie ou contexte sous-jacent

**Méthodologie** :
- Type d'étude (expérimentale, théorique, mesures, simulation)
- Outils utilisés
- Échelle (nombre de domaines, durée, sondes)
- Protocole de mesure

**Résultats principaux** :
Synthèse des résultats (3-5 points)

**Conclusion des auteurs** :
Que concluent-ils ?

**Que garder pour le mémoire** :
- Concepts clés à réutiliser
- Méthodes applicables
- Chiffres/statistiques importantes
- Limites identifiées (gaps à combler)

**Critique personnelle** :
- Forces de l'article
- Faiblesses identifiées
- Lien avec autres articles lus
- Questions ouvertes

**Citations importantes** :
Phrases clés avec numéro de page

**Tags** :
#dns #measurement #ripe-atlas #openintel (etc.)
```

**Stockage** :
```
sources/fiches/
├── vanRijswijk2016_openintel.md
├── lePochat2019_tranco.md
├── auteur_annee_motcle.md
└── ...
```

---

### Tableau de synthèse

**Créer un tableau récapitulatif** dans `sources/README.md` ou notebook Jupyter :

| Référence | Année | Conférence | Focus | Méthodologie | Limites | Lien avec mémoire |
|-----------|-------|------------|-------|--------------|---------|-------------------|
| van Rijswijk-Deij et al. | 2016 | IEEE JSAC | OpenINTEL | Mesures actives centralisées | Un seul point de mesure | Base pour architecture |
| Le Pochat et al. | 2019 | NDSS | Tranco | Agrégation listes | - | Sélection domaines |
| ... | ... | ... | ... | ... | ... | ... |

---

## Planning de recherche bibliographique

### Semaine 1 (20-26 janvier 2026)

**Lundi-Mardi** : Articles fondamentaux ✅ TERMINÉ
- ✅ Lire van Rijswijk-Deij (2016) - OpenINTEL
- ✅ Lire Le Pochat (2019) - Tranco
- ✅ Lire Nosyk et al. (2024) - RIPE Atlas DITL
- ✅ Créer 3 fiches de lecture détaillées

**Mercredi-Jeudi** : Exploration citations ⏳ EN COURS
- ✅ Recherches web RIPE Atlas + DNS + geographic
- ✅ Identification articles clés (voir liste "Articles pertinents trouvés")
- ⏭️ Télécharger PDFs identifiés
- ⏭️ Lire et ficher 5-8 articles additionnels

**Vendredi** : RFCs et documentation technique
- RFC 1034, 1035 (DNS base)
- RFC 4033-4035 (DNSSEC)
- RFC 7871 (ECS)
- Documentation RIPE Atlas

---

### Semaine 2 (27 janvier - 2 février 2026)

**Lundi** : Section 2.2 - Mesures actives vs passives
- Requêtes IEEE Xplore 1, 2, 3
- Sélectionner 5-8 articles
- Fiches de lecture

**Mardi** : Section 2.3 - OpenINTEL
- Requête IEEE Xplore 8
- Articles connexes infrastructure DNS
- Comparaison avec autres approches

**Mercredi** : Section 2.4 - Tranco
- Requête IEEE Xplore 6
- Comparaisons Alexa, Umbrella
- Méthodologies de ranking

**Jeudi** : Section 2.5 - RIPE Atlas
- Requête IEEE Xplore 2 (focus RIPE)
- Études de cas
- Documentation API

**Vendredi** : Section 2.6 - Travaux connexes (partie 1)
- Requêtes 4, 5 (CDN, sécurité)
- Sélection articles

---

### Semaine 3 (3-9 février 2026)

**Lundi** : Section 2.6 - Travaux connexes (partie 2)
- Requêtes 7, 9 (ECS, temporel)
- Compléter sélection

**Mardi-Mercredi** : Articles récents 2023-2026
- IMC 2023, 2024, 2025 proceedings
- PAM 2023, 2024, 2025 proceedings
- Nouveautés pertinentes

**Jeudi** : Synthèse et positionnement
- Requête 10 (datasets, reproductibilité)
- Identifier gaps dans littérature
- Préparer tableau comparatif

**Vendredi** : Organisation finale
- Compléter Zotero
- Export BibTeX
- Tableau de synthèse complet
- Plan détaillé Chapitre 2

---

## Checklist recherche bibliographique

### Phase préparatoire
- ☐ Installer et configurer Zotero
- ☐ Créer compte Google Scholar
- ☐ Vérifier accès IEEE Xplore via UNamur
- ☐ Vérifier accès ACM Digital Library
- ✅ Créer structure dossiers `sources/fiches/`
- ✅ Créer template fiche de lecture

### Articles fondamentaux
- ✅ van Rijswijk-Deij (2016) - lu et fiché ✅
- ✅ Le Pochat (2019) - lu et fiché ✅
- ✅ Nosyk (2024) - lu et fiché ✅
- ✅ Recherches web RIPE Atlas effectuées (5 articles identifiés)
- ☐ RFCs DNS (1034, 1035, 4033-35, 7871) - à consulter

### Sections état de l'art (Progrès: 3/~40 articles = 7.5%)
- ☐ Section 2.1 - Documentation technique DNS rassemblée (0/1)
- ☐ Section 2.2 - Actif vs passif (0/5-8 articles)
- ⏳ Section 2.3 - OpenINTEL et infrastructures (1/5-8 articles) ✅ van Rijswijk-Deij
- ⏳ Section 2.4 - Tranco et rankings (1/3-5 articles) ✅ Le Pochat
- ⏳ Section 2.5 - RIPE Atlas (1/5-8 articles) ✅ Nosyk + 5 identifiés à lire
- ☐ Section 2.6 - CDN/géo (0/3-5 articles)
- ☐ Section 2.6 - Sécurité DNS (0/3-5 articles)
- ☐ Section 2.6 - ECS (0/2-3 articles)
- ☐ Section 2.6 - Temporel (0/3-5 articles)
- ☐ Section 2.7 - Synthèse et positionnement (0/1)

### Organisation
- ✅ Structure fiches créée (sources/fiches/)
- ✅ 3 fiches de lecture détaillées créées
- ✅ Liste articles pertinents identifiés et documentés
- ✅ Insights clés pour mémoire documentés
- ☐ Zotero à jour avec tags
- ☐ BibTeX exporté vers `latex/bibliography.bib`
- ☐ Tableau de synthèse complété
- ☐ Plan détaillé Chapitre 2 validé avec promoteurs

### Validation
- ☐ Bibliographie présentée aux promoteurs
- ☐ Retour promoteurs intégré
- ☐ Articles manquants identifiés et ajoutés
- ☐ Prêt pour rédaction Chapitre 2

---

## Notes et contacts

### Questions pour promoteurs

**Préparer pour réunion** :
1. Validation sélection d'articles
2. Profondeur attendue pour Section 2.1 (rappels DNS) ?
3. Focus particulier souhaité dans Section 2.6 ?
4. Références manquantes à ajouter ?
5. Validation plan détaillé Chapitre 2

### Contacts chercheurs

**Si questions techniques** :
- Roland van Rijswijk-Deij (OpenINTEL) : consulter via publications
- RIPE Atlas team : atlas@ripe.net
- Stéphane Bortzmeyer (AFNIC) : via blog ou email public

**Protocole contact** :
1. Email court et précis
2. Se présenter (étudiant Master 60 UNamur)
3. Mentionner le mémoire et les promoteurs
4. Question spécifique et concise
5. Remercier pour leur travail

---

## Ressources additionnelles

### Blogs et veille technique

- **RIPE Labs** : https://labs.ripe.net/ (articles techniques RIPE)
- **APNIC Blog** : https://blog.apnic.net/ (DNS, routing)
- **Cloudflare Blog** : https://blog.cloudflare.com/ (DNS, CDN)
- **DNS-OARC** : https://www.dns-oarc.net/ (communauté DNS)
- **Stéphane Bortzmeyer** : https://www.bortzmeyer.org/ (expert DNS français)

### Podcasts et vidéos

- **RIPE NCC YouTube** : Présentations techniques
- **NANOG presentations** : North American Network Operators
- **IETF proceedings** : Groupes de travail DNS

### Outils d'analyse

- **Connected Papers** : https://www.connectedpapers.com/ (graphe citations)
- **Research Rabbit** : https://www.researchrabbit.ai/ (découverte articles)
- **Litmaps** : https://www.litmaps.com/ (carte littérature)

---

## Insights clés pour le mémoire

### Synthèse des articles fondateurs

#### Contribution scientifique

**Gap identifié** (des 3 articles lus) :
1. **OpenINTEL** : Infrastructure exhaustive MAIS **1 seul point de mesure** (Pays-Bas)
2. **Tranco** : Liste stable domaines MAIS **pas de diversité géographique mesures**
3. **RIPE Atlas** : **12.9K vantage points** (178 pays) MAIS **biais géographique** Europe/NA

**Notre contribution** = Combiner Tranco (liste stable) + RIPE Atlas (diversité géo) pour analyser **variations géographiques réponses DNS**.

#### Chiffres clés à retenir

**OpenINTEL** :
- 123M domaines (.com) mesurés quotidiennement
- 1.85 milliards queries/jour
- 0.3-1.6% trafic DNS global (acceptable)
- Limitation majeure : 1 seul vantage point

**Tranco** :
- Alexa : 50% changement quotidien (post-janvier 2018)
- Tranco : 0.6% changement quotidien (stabilité ×83)
- 1 HTTP request suffit entrer Alexa top 1M (vulnérabilité)
- Tranco : 4× effort manipulation requis
- 600+ publications académiques utilisent Tranco

**RIPE Atlas** :
- 12,892 sondes + 810 ancres (février 2024)
- 178 pays couverts
- Allemagne + USA = 28% des vantage points (biais!)
- 88K mesures DNS quotidiennes
- 69% sondes chinoises bloquées (Meta services) → preuve utilité diversité géo
- 1.3 milliards résultats/jour (~26K résultats/mesure)

#### Implications méthodologiques

**Choix domaines (Tranco)** :
- ✅ Utiliser Tranco pour stabilité + résistance manipulation
- ⚠️ Choisir taille liste : Top 1K, 10K, 100K, 1M ?
- ✅ Permalinks Tranco pour reproductibilité
- ✅ Filtrer domaines non-réactifs si nécessaire

**Mesures distribuées (RIPE Atlas)** :
- ✅ Sélection sondes par critères géographiques (pays/AS/préfixe)
- ⚠️ Gérer biais Europe/NA (28% concentration)
- ✅ Privilégier sondes dual-stack (IPv4 + IPv6)
- ✅ Réutiliser mesures existantes (économie crédits)
- ✅ Tags systématiques : `thesis-dns-geo-YYYY-MM-DD`
- ✅ Documenter measurement IDs (reproductibilité)
- ⚠️ Optimiser crédits : nombre sondes × fréquence × domaines

**Complémentarité approches** :

| Critère | OpenINTEL | Notre approche (Tranco + RIPE) |
|---------|-----------|--------------------------------|
| Exhaustivité | ✅ 123M domaines | ❌ Échantillon Tranco |
| Diversité géo | ❌ 1 point (NL) | ✅ 12.9K points (178 pays) |
| Stabilité liste | ✅ Zones TLD complètes | ✅ Tranco (0.6% changement/jour) |
| Contrôle infra | ✅ Total | ❌ Limité (crédits RIPE) |
| Fréquence | ✅ Quotidien | ⚠️ À définir (dépend crédits) |
| Coût | Infrastructure dédiée | Crédits RIPE (alloués) |
| Reproductibilité | ✅ Datasets archivés | ✅ IDs RIPE + permalinks Tranco |

### Questions critiques à résoudre

**Avant conception (Phase 2)** :
1. **Combien de crédits RIPE disponibles ?** (contacter promoteurs)
2. **Quelle taille liste Tranco ?** (Top 10K recommandé pour début)
3. **Fréquence mesures ?** (quotidien vs hebdomadaire vs mensuel)
4. **Durée campagne ?** (3 mois minimum pour tendances temporelles)
5. **Types queries DNS ?** (A, AAAA, NS, MX comme OpenINTEL ?)
6. **Stratégie sélection sondes ?** (équilibrage géographique)

**Pendant conception (Phase 3)** :
7. **Comment gérer biais Europe/NA ?** (pondération, stratification)
8. **Stockage données ?** (format Avro/Parquet comme OpenINTEL ?)
9. **Pipeline traitement ?** (streaming vs batch)
10. **Métadonnées à enrichir ?** (IP-to-AS, GeoIP, anycast detection)

**Pour analyse (Phase 4)** :
11. **Métriques évaluation diversité géo ?** (coefficient variation, distance géographique)
12. **Détection CDN/anycast ?** (patterns réponses multiples)
13. **Impact ECS ?** (EDNS Client Subnet déploiement)
14. **Validation résultats ?** (comparaison OpenINTEL ou autres)

### Prochaines lectures prioritaires

**Très haute priorité** :
1. [ ] Bortzmeyer - "DNS Measurements with RIPE Atlas" (tutorial pratique)
2. [ ] "Quantifying Interference between Measurements" (IMC 2015) - impact mesures
3. [ ] Documentation RIPE Atlas API (implémentation)
4. [ ] RFC 7871 (EDNS Client Subnet) - comprendre ECS impact

**Haute priorité** :
5. [ ] "Detecting DNS Root Manipulation" - méthodologie détection
6. [ ] "Benefits and Limitations of RIPE Atlas Tags" - organisation mesures
7. [ ] Chercher études CDN avec RIPE Atlas (geographic diversity)
8. [ ] Chercher études anycast deployment

**Moyenne priorité** :
9. [ ] "The Ongoing Story of OpenINTEL" - évolution post-2016
10. [ ] Études sécurité utilisant Tranco (HTTPS, DMARC, etc.)
11. [ ] Comparaisons Passive DNS vs Active DNS
12. [ ] M-Lab platform (comparaison RIPE Atlas)

---

**Dernière mise à jour** : 21 janvier 2026
**Prochaine révision** : Après semaine 1 de recherche (27 janvier 2026)
