# Analyse comparative — Mémoires Master 60 UNamur (2022–2024)

## 1. Données brutes — longueur des mémoires

| Auteur | Année | Pages | Mots |
|--------|-------|-------|------|
| Delvaux G. | 2022 | 73 | 27 022 |
| Verjans M. | 2023 | 69 | 23 133 |
| Bauwens J. | 2023 | 97 | 34 333 |
| Blauwaert M. | 2023 | 95 | 24 015 |
| DeKinder/Peytier | 2023 | 116 | 21 962 |
| DeRop C. | 2023 | 48 | 23 146 |
| Duivier B. | 2023 | 154 | 50 923 |
| Coppin J. | 2024 | 70 | 21 370 |
| DeGrove G. | 2024 | 52 | 17 331 |
| Gaillard M. | 2024 | 79 | 33 919 |
| Galloy M. | 2024 | 58 | 31 171 |
| Henne C. | 2024 | 116 | 47 780 |
| Six T. | 2024 | 89 | 41 506 |
| Sosson T. | 2024 | 55 | 18 848 |
| Hensmans O. | 2024 | 66 | 20 051 |
| Zenobi J. | 2024 | 83 | 39 852 |

**Médiane : 79 pages — Moyenne : 86 pages — Fourchette typique (excl. outliers) : 52–95 pages**

> Les outliers (154p, 116p) existent mais sont des cas particuliers (binôme, projet très long).
> **Master 60 individuel typique : 55–80 pages.**

---

## 2. Structure type observée

### Budget pages par chapitre (Master 60, ~70 pages)

| Section | Pages typiques | Fourchette | Notre actuel |
|---------|---------------|------------|--------------|
| Pages préliminaires (couv, rem, résumé, TdM, acronymes) | 8 | 6–10 | **16** ❌ |
| Ch1 — Introduction | 5 | 2–7 | **16** ❌ |
| Ch2 — État de l'art | 12 | 7–18 | **32** ❌ |
| Ch3 — Méthodologie / Développement | 15 | 9–25 | 18 ✅ |
| Ch4 — Résultats | 12 | 5–16 | 12 ✅ (squelette) |
| Ch5 — Discussion + Conclusion | 10 | 5–16 | 16 ⚠️ |
| Bibliographie | 4 | 2–6 | 4 ✅ |
| Annexes | 8 | 0–16 | 2 ✅ |
| **TOTAL** | **~74** | 55–95 | **117** ❌ |

### Structure des chapitres dans les exemples

**Chapitres d'introduction (2–5 pages) — modèle observé :**
- 1 section contextualisant le problème (~1p)
- 1 section question de recherche + objectifs (~1p)
- 1 section structure du mémoire (~0.5p)
- *Pas de sections séparées pour "challenges", "contributions expected", "work organisation", etc.*

**État de l'art (8–18 pages) — modèle observé :**
- 3 à 6 sous-sections thématiques denses
- Citations en fin de phrase, pas de paragraphe entier par article
- Chaque concept en 2–4 paragraphes, pas de chapitres entiers
- Termine par une synthèse/gap analysis (1–2 pages)

**Méthodologie (9–18 pages) — modèle observé :**
- Description directe des choix faits
- Pas de justification exhaustive de chaque paramètre
- Diagrammes et tableaux utilisés pour compresser l'information

---

## 3. Style d'écriture

### Densité
- **~400–580 mots/page** dans les mémoires exemples
- Notre document : ~350 mots/page (trop peu dense = trop d'espace blanc et de padding)

### Ton et niveau de détail
- Les exemples **vont droit au but** : une phrase = une idée, pas de développements narratifs sur plusieurs paragraphes pour un seul concept
- Les citations sont intégrées dans le texte (`[12]` ou `(Dupont, 2020)`) sans reformuler entièrement l'article cité
- L'état de l'art présente les **résultats clés** des articles, pas leur méthodologie complète
- **Pas de redondances** entre introduction, état de l'art et méthodologie

### Ce que font les bons exemples que nous ne faisons pas
1. Une section introductive → directement le contexte + problème (pas 8 sous-sections)
2. L'état de l'art cite un article en 2–3 lignes, extrait les 1–2 résultats pertinents
3. La méthodologie est descriptive, pas justificative à l'excès
4. Les résultats présentent les données, la discussion les interprète — pas de chevauchement

---

## 4. Diagnostic de notre mémoire

### Problème principal : Ch1 et Ch2 font 3× la norme

**Ch1 Introduction (16 pages → devrait être 5–7 pages)**

Sections actuelles vs ce qui devrait exister :
- Sec 1.1 Context and Motivation (4p) → garder, compresser à 2p
- Sec 1.2 Research Problem (2p) → garder, 1p suffit
- Sec 1.3 Thesis Objectives (1p) → fusionner avec 1.2
- Sec 1.4 Challenges and Constraints (2p) → **supprimer** (résidu de padding)
- Sec 1.5 Methodological Approach (2p) → **supprimer** (répète la méthodologie)
- Sec 1.6 Thesis Structure (1p) → garder mais 0.5p
- Sec 1.7 Expected Contributions and Impact (1p) → **supprimer** (spéculatif)
- Sec 1.8 Work Organisation — Gantt (2p) → **déplacer en annexe** ou supprimer

**Ch2 État de l'art (32 pages → devrait être 12–15 pages)**

Problème : tripling en session précédente = beaucoup de padding
- Sec 2.1 DNS Background (4p) → 2p max (notions de base, pas tutorial complet)
- Sec 2.2 DNS Measurements (3p) → 2p (aller à l'essentiel)
- Sec 2.3 OpenINTEL (3p) → **fusionner avec 2.2** (1.5p)
- Sec 2.4 RIPE Atlas (5p) → 2p (chiffres clés + biais géographique)
- Sec 2.5 Anycast (3p) → 2p
- Sec 2.6 CDN/ECS (3p) → 2p
- Sec 2.7 Domain lists/Tranco (5p) → 1.5p (tableau comparatif + justification Tranco)
- Sec 2.8–2.10 Centralisation + Sécurité + Synthèse (6p) → **sec 2.8 uniquement** : gap analysis (2p)

---

## 5. Plan de réduction recommandé

### Cible : 70–75 pages (≈ -35%)

| Chapitre | Actuel | Cible | Action |
|---------|--------|-------|--------|
| Préliminaires | 16p | 8p | Réduire les pages blanches redondantes |
| Ch1 Introduction | 16p | 6p | Supprimer sec 1.4, 1.5, 1.7 ; compresser 1.1–1.3 ; déplacer Gantt en annexe |
| Ch2 État de l'art | 32p | 14p | Couper ~55% ; aller à l'essentiel ; supprimer développements encyclopédiques |
| Ch3 Méthodologie | 18p | 16p | OK, légère compression possible |
| Ch4 Résultats | 12p | 18p | À remplir avec vraies données |
| Ch5 Discussion+Ccl | 16p | 12p | Compresser les squelettes redondants |
| Bibliographie | 4p | 4p | OK |
| Annexes | 2p | 6p | Déplacer Gantt + config RIPE Atlas détaillée ici |
| **TOTAL** | **117p** | **~84p** | *(deviendra ~70p une fois ch4 rempli avec données réelles)* |

### Priorités de coupes

1. **Ch1** : Supprimer sections 1.4, 1.5, 1.7, 1.8 (≈ -8 pages)
2. **Ch2** : Couper 50% des développements — chaque sous-section max 1.5–2 pages (≈ -16 pages)
3. **Préliminaires** : Supprimer les pages blanches intermédiaires superflues (≈ -4 pages)

### Ce qu'il ne faut PAS couper
- La rigueur des citations et références → c'est un atout
- Les figures et tableaux (bien faits)
- La méthodologie détaillée (ch3) — c'est le cœur du travail
- Les questions de recherche Q1–Q4 — claires et bien formulées

---

## 6. Observations de style à adopter

D'après les exemples analysés :

1. **Une sous-section = 0.5–1.5 pages maximum** (pas 3–4 pages)
2. **Citer un article = 1–3 lignes** : auteur, résultat clé, pertinence pour notre travail
3. **Pas de "In this section, we will..."** ni de redites entre résumé de section et contenu
4. **Les figures et tableaux remplacent du texte** (pas en plus du texte)
5. **L'intro ne répète pas l'état de l'art** — elle pose juste le problème
6. **La conclusion ne répète pas les résultats** — elle les interprète

---

*Analyse générée le 23 mars 2026 à partir de 25 mémoires Master 60 UNamur (2022–2024).*
