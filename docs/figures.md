# Figures, schémas et tableaux — Plan d'illustration

Ce document liste les figures, schémas et tableaux pour les chapitres 1, 2 et 3 du mémoire.

**Légende statut** : ✅ Générée et intégrée au LaTeX | ⏳ À faire après mesures | ❌ À faire

---

## Chapitre 1 — Introduction

**Figure 1 — Processus de résolution DNS itérative** *(Section 1.1.1)* ✅
Le chemin client → resolver récursif → root → TLD → authoritative, avec les messages échangés et le TTL.
- Fichier : `latex/figures/fig1_dns_resolution.png`
- Script : PlantUML — `latex/figures/fig1_dns_resolution.puml`
- Label LaTeX : `\ref{fig:dns_resolution}`

**Figure 2 — Les trois mécanismes de variation géographique** *(Section 1.1.3)* ✅
Trois sous-figures côte à côte : CDN routing, anycast BGP basins, ECS.
- Fichier : `latex/figures/fig2_geographic_mechanisms.png`
- Script : `scripts/gen_fig2_geographic_mechanisms.py` (Matplotlib)
- Label LaTeX : `\ref{fig:geographic_mechanisms}`

**Figure 3 — Triangle des contraintes du budget RIPE Atlas** *(Section 3.3.6)* ✅
Le compromis domaines / géographie / fréquence, borné par le budget crédits RIPE Atlas.
- Fichier : `latex/figures/fig3_constraints_triangle.png`
- Script : `scripts/gen_fig3_constraints_triangle.py` (Matplotlib)
- Label LaTeX : `\ref{fig:constraints_triangle}`

**Tableau 1 — Calendrier des phases du projet** *(Section 1.8.1)* ❌
Gantt simplifié à 5 lignes (phases 1–5) sur 30 semaines.
→ À créer en LaTeX (tableau booktabs avec cellules colorées).

---

## Chapitre 2 — État de l'art

**Figure 4 — Distribution géographique des probes RIPE Atlas** *(Section 2.4.4)* ✅
Carte mondiale choroplèthe, biais Europe/Amérique du Nord (91%), données Nosyk 2024 / Bajpai 2017.
- Fichier : `latex/figures/fig4_ripe_atlas_distribution.png`
- Script : `scripts/gen_fig4_ripe_atlas_distribution.py` (Cartopy + naturalearth)
- Label LaTeX : `\ref{fig:ripe_atlas_distribution}`

**Figure 5 — Schéma ECS (EDNS Client Subnet)** *(Section 2.6.3)* ✅
Trois scénarios : sans ECS, avec ECS /24, opt-out subnet=0/0.
- Fichier : `latex/figures/fig5_ecs_schema.png`
- Script : PlantUML — `latex/figures/fig5_ecs_schema.puml`
- Label LaTeX : `\ref{fig:ecs_schema}`

**Figure 6 — Routing anycast et BGP attraction basins** *(Section 2.5.3)* ✅
Comparaison routage attendu vs réel pour d.nic.fr (Bortzmeyer 2013) : NA → Paris à 55%.
- Fichier : `latex/figures/fig6_bgp_attraction_basins.png`
- Script : `scripts/gen_fig6_bgp_attraction_basins.py` (Matplotlib)
- Label LaTeX : `\ref{fig:bgp_attraction_basins}`

**Tableau 2 — Comparaison des plateformes de mesure distribuée** *(Section 2.4.1)* ❌
RIPE Atlas vs CAIDA Archipelago vs SamKnows vs PlanetLab.
→ À construire en LaTeX depuis le texte du chapitre 2 + Bajpai 2017 + Cicalese 2015.

**Tableau 3 — Comparaison des listes de domaines** *(Section 2.7)* ❌
Alexa vs Cisco Umbrella vs Majestic vs Tranco.
→ Données dans Le Pochat et al. (2019).

**Tableau 4 — Types de Resource Records pertinents** *(Section 2.1.2)* ❌
A, AAAA, NS, CNAME, SOA, MX, TXT avec usage et pertinence pour les mesures.
→ Référence RFC 1035.

---

## Chapitre 3 — Méthodologie

**Figure 7 — Architecture du pipeline de collecte** *(Section 3.1.2)* ✅
5 stages : Tranco API → corpus → RIPE Atlas → JSON → Avro/Parquet → analyse.
- Fichier : `latex/figures/fig7_pipeline_collecte.png`
- Script : PlantUML — `latex/figures/fig7_pipeline_collecte.puml`
- Label LaTeX : `\ref{fig:pipeline_collecte}`

**Figure 8 — Pipeline de validation des mesures** *(Section 3.4.3)* ✅
Flowchart des 4 filtres successifs : TIMEOUT → SCHED_REJECTED → DNS_ERROR → PROXY_SUSPECT → VALID.
- Fichier : `latex/figures/fig8_pipeline_validation.png`
- Script : PlantUML — `latex/figures/fig8_pipeline_validation.puml`
- Label LaTeX : `\ref{fig:pipeline_validation}`

**Tableau 5 — Schéma des champs Avro** *(Section 3.4.5)* ❌
Champs msm_id, prb_id, timestamp, domain, rcode, answer_ips, ttl, nsid, rt…
→ Déjà partiellement présent sous forme de tableau LaTeX dans 03-methodologie.tex §3.4.5. À compléter avec colonne "exemple de valeur".

**Figure 9 — Carte des probes sélectionnés** *(Section 3.3.1)* ⏳
Carte des ~100 probes retenus après stratification, colorés par continent.
- Script prévu : Cartopy + données RIPE Atlas API (probe metadata)
- **Dépend des mesures réelles** — à générer une fois la campagne lancée.

---

## Récapitulatif

| N° | Titre court | Chapitre | Statut | Fichier |
|---|---|---|---|---|
| Fig. 1 | Résolution DNS itérative | 1 | ✅ | `fig1_dns_resolution.png` |
| Fig. 2 | Trois mécanismes géographiques | 1 | ✅ | `fig2_geographic_mechanisms.png` |
| Fig. 3 | Triangle des contraintes | 3 | ✅ | `fig3_constraints_triangle.png` |
| Tab. 1 | Gantt des phases | 1 | ❌ | — |
| Fig. 4 | Distribution probes RIPE Atlas | 2 | ✅ | `fig4_ripe_atlas_distribution.png` |
| Fig. 5 | Schéma ECS | 2 | ✅ | `fig5_ecs_schema.png` |
| Fig. 6 | BGP attraction basins | 2 | ✅ | `fig6_bgp_attraction_basins.png` |
| Tab. 2 | Comparaison plateformes mesure | 2 | ❌ | — |
| Tab. 3 | Comparaison listes domaines | 2 | ❌ | — |
| Tab. 4 | Types RR DNS | 2 | ❌ | — |
| Fig. 7 | Architecture pipeline collecte | 3 | ✅ | `fig7_pipeline_collecte.png` |
| Fig. 8 | Pipeline validation données | 3 | ✅ | `fig8_pipeline_validation.png` |
| Tab. 5 | Schéma champs Avro | 3 | ❌ | — |
| Fig. 9 | Carte probes sélectionnés | 3 | ⏳ | après mesures |

**Progression figures** : 8/9 générées (89%) — Fig. 9 bloquée sur données réelles.
**Progression tableaux** : 0/5 intégrés — à faire en LaTeX.

---

## Notes

- Tous les PNG sont dans `latex/figures/` à 200 DPI.
- Scripts Python dans `scripts/gen_fig*.py` — régénération : `python3 scripts/gen_figX_*.py`.
- Scripts PlantUML dans `latex/figures/*.puml` — régénération : `plantuml -Sdpi=200 -tpng latex/figures/*.puml`.
- Fig. 9 : utiliser l'API RIPE Atlas (`/api/v2/probes/?id__in=...`) pour récupérer lat/lon des probes sélectionnés, puis `scripts/gen_fig4_ripe_atlas_distribution.py` comme base.
