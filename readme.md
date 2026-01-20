# Mesures DNS dans l'espace et le temps

**Projet de mémoire - Numéro 9**
**Promoteurs** : Fl. Rochet - J. Dejaeghere

---

## Contexte

Le DNS est un service distribué initialement prévu pour associer des noms d'hôtes à leur adresse IP. L'information contenue dans le DNS donne un aperçu de la manière dont Internet est structuré et comment les domaines sont administrés.

Cependant, l'information fournie par le DNS est **éphémère** : les administrateurs de zones DNS peuvent modifier l'information liée à leur zone sans qu'un historique des changements ne soit disponible.

## Problématique

Dans certains domaines de recherche, il est intéressant de pouvoir obtenir les informations fournies par le système DNS à une période donnée. Ces informations permettent par exemple de **simuler Internet dans un état comparable à celui d'il y a quelques mois ou quelques années**.

Certains chercheurs ont déjà envisagé d'archiver une partie des données du service DNS à des fins de recherche [1]. Cependant, la démarche présentée dans [1] mesure l'information DNS depuis un seul point sur Internet.

Or, les informations retournées par le DNS peuvent **varier en fonction de la localisation du client** (par exemple pour minimiser la latence, pour fournir une version locale du service). Il semble dès lors intéressant de capturer la **diversité géographique** des réponses DNS dans le temps.

## Objectifs du projet

Le projet de mémoire proposé vise à **enregistrer une partie de l'information fournie par le système DNS en capturant la diversité des réponses dans le temps et dans l'espace**.

Ces données pourront ensuite être rendues disponibles à des fins de recherche, pour de la simulation réseau notamment.

Comme l'information fournie par le système DNS est volumineuse, le projet se concentrera sur un nombre réduit d'entrées intéressantes (sur base de la **Tranco list** [2], par exemple).

## Travail attendu

Il sera attendu ce qui suit de l'étudiant :

1. **Familiarisation** avec le sujet de recherche et les résultats existants les plus pertinents

2. **Conception d'un outil d'archivage** des informations DNS, en utilisant :
   - La **Tranco list** comme source de noms de domaines
   - **RIPE Atlas** [3] pour lancer des requêtes DNS depuis différents lieux sur Terre

3. **Conception d'une stratégie** pour optimiser les informations archivées par rapport au nombre de requêtes autorisées par RIPE Atlas

4. **Conception d'une structure de données** qui facilite le partage des données récoltées

## Ressources

Pour aider l'étudiant dans sa tâche, un nombre de **crédits RIPE Atlas** lui sera alloué pour lancer les mesures DNS.

D'autres options que RIPE Atlas peuvent être envisagées si elles répondent au besoin.

Il est conseillé à l'étudiant de lire les références [1] et [3] avant de choisir ce projet.

---

## Références

### [1] Infrastructure de mesure DNS à grande échelle

**van Rijswijk-Deij, R., Jonker, M., Sperotto, A., & Pras, A. (2016)**
*A High-Performance, Scalable Infrastructure for Large-Scale Active DNS Measurements*
IEEE Journal on Selected Areas in Communications, 34(6), 1877–1888
https://doi.org/10.1109/JSAC.2016.2558918

📄 Document disponible : [sources/A High-Performance, Scalable Infrastructure for Large-Scale Active DNS Measurements.pdf](sources/A%20High-Performance,%20Scalable%20Infrastructure%20for%20Large-Scale%20Active%20DNS%20Measurements.pdf)

### [2] Tranco - Classement robuste de sites web

**Le Pochat, V., Van Goethem, T., Tajalizadehkhoob, S., Korczynski, M., & Joosen, W. (2019)**
*Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation*
Proceedings 2019 Network and Distributed System Security Symposium
Network and Distributed System Security Symposium, San Diego, CA
https://doi.org/10.14722/ndss.2019.23386

📄 Document disponible : [sources/TRANCO A Research-Oriented Top Sites Ranking Hardened Against Manipulation.pdf](sources/TRANCO%20A%20Research-Oriented%20Top%20Sites%20Ranking%20Hardened%20Against%20Manipulation.pdf)

### [3] RIPE Atlas Documentation

RIPE Atlas Documentation
Retrieved April 9, 2025
https://atlas.ripe.net/docs/

---

## Documentation du projet

Pour la documentation complète de l'environnement de travail, des outils et des bonnes pratiques, consulter :

📚 **[docs/documentation.md](docs/documentation.md)** - Documentation complète (Markdown)
📄 **[docs/documentation.pdf](docs/documentation.pdf)** - Documentation complète (PDF)

## Structure du projet

```
dns-measures/
├── docs/                 # Documentation complète
├── sources/              # Articles académiques et références
├── data/                 # Données de mesures DNS
├── notebooks/            # Analyses exploratoires Jupyter
├── scripts/              # Scripts Python d'analyse
├── reports/              # Rapports générés
├── latex/                # Mémoire LaTeX
└── output/               # Résultats et visualisations
```

## Quick Start

### Avec VSCode Dev Container (recommandé)

1. Ouvrir le projet dans VSCode
2. `F1` → "Dev Containers: Reopen in Container"
3. L'environnement complet sera configuré automatiquement

### Avec Docker Compose

```bash
# Démarrer le container
docker-compose up -d dns-measures

# Se connecter
docker-compose exec dns-measures bash
```

Pour plus d'informations, consulter la [documentation complète](docs/documentation.md).
