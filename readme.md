Mesures DNS dans l'espace et le temps
Numéro : 9 – Promoteurs : Fl. Rochet - J. Dejaeghere

Le DNS est un service distribué initialement prévu pour associer des noms d'hôtes à leur adresse IP. L'information contenue dans le DNS donne un aperçu de la manière dont Internet est structuré et comment les domaines sont administrés. Cependant, l'information fournie par le DNS est éphémère : les administrateurs de zones DNS peuvent modifier l'information liée à leur zone sans qu'un historique des changements ne soit disponible.
Dans certains domaines de recherche, il est intéressant de pouvoir obtenir les informations fournies par le système DNS à une période donnée. Ces informations permettent par exemple de simuler Internet dans un état comparable à celui d'il y a quelques mois ou quelques années. Certains chercheurs ont déjà envisagé d'archiver une partie des données du service DNS à des fins de recherche [1].
La démarche présentée dans [1] mesure l'information DNS depuis un seul point sur Internet. Cependant, les informations retournées par le DNS peuvent varier en fonction de la localisation du client (par exemple pour minimiser la latence, pour fournir une version locale du service). Il semble dès lors intéressant de capturer la diversité géographique des réponses DNS dans le temps.
Le projet de mémoire proposé vise à enregistrer une partie de l'information fournie par le système DNS en capturant la diversité des réponses dans le temps et dans l'espace. Ces données pourront ensuite être rendues disponible à des fins de recherche, pour de la simulation réseau notamment.
Comme l'information fournie par le système DNS est volumineuse, le projet se concentrera sur un nombre réduit d'entrées intéressantes (sur base de la Tranco list [2], par exemple).
Il sera attendu ce qui suit de l'étudiant :
- Familiarisation avec le sujet de recherche et les résultats existants les plus pertinents
- Conception d'un outil d'archivage des informations DNS, en utilisant la Tranco list comme source de noms de domaines et Ripe Atlas [3] pour lancer des requêtes DNS depuis différents lieux sur Terre
- Conception d'une stratégie pour optimiser les informations archivées par rapport au nombre de requêtes autorisées par Ripe Atlas
- Conception d'une structure de données qui facilite le partage des données récoltées
Pour aider l'étudiant dans sa tâche, un nombre de crédits Ripe Atlas lui sera alloué pour lancer les mesures DNS. D'autres options que Ripe Atlas peuvent être envisagées si elles répondent au besoin.
Il est conseillé à l'étudiant de lire les références [1] et [3] avant de choisir ce projet.
Références
[1] van Rijswijk-Deij, R., Jonker, M., Sperotto, A., & Pras, A. (2016). A High-Performance, Scalable Infrastructure for Large-Scale Active DNS Measurements. IEEE Journal on Selected Areas in Communications, 34(6), 1877–1888. IEEE Journal on Selected Areas in Communications. https://doi.org/10.1109/JSAC.2016.2558918
[2] Le Pochat, V., Van Goethem, T., Tajalizadehkhoob, S., Korczynski, M., & Joosen, W. (2019). Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation. Proceedings 2019 Network and Distributed System Security Symposium. Network and Distributed System Security Symposium, San Diego, CA. https://doi.org/10.14722/ndss.2019.23386
[3] RIPE Atlas Documentation. Retrieved April 9, 2025, from https://atlas.ripe.net/docs/