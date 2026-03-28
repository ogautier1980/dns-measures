# Données — Mesures DNS

Ce répertoire est persisté via le volume Docker `dns-data`.
Il n'est **pas versionné** (voir `.gitignore`).

## Structure attendue

```
data/
├── raw/                        # Données brutes RIPE Atlas (JSON)
│   ├── YYYY-MM-DD/
│   │   ├── msm_<id>_<domain>.json
│   │   └── ...
│   └── ...
├── processed/                  # Données traitées (Parquet/Avro)
│   ├── dns_results.parquet     # Table principale des mesures
│   ├── probes_metadata.parquet # Métadonnées des sondes RIPE Atlas
│   └── tranco_top10k.csv       # Liste Tranco (téléchargée hebdomadairement)
└── README.md                   # Ce fichier
```

## Volumes estimés

| Source | Volume estimé |
|--------|--------------|
| Résultats RIPE Atlas (JSON brut, 90 jours) | ~5–15 Go |
| Parquet traité | ~500 Mo–2 Go |
| Liste Tranco | ~1 Mo |

## Régénérer les données converties

```bash
# Convertir les PDFs sources en texte (pour analyse)
cd /workspace/sources
for pdf in *.pdf; do
    pdftotext "$pdf" "converted/${pdf%.pdf}.md"
done
```

## Notes

- Les données brutes RIPE Atlas sont téléchargées via l'API (`scripts/`)
- La liste Tranco : https://tranco-list.eu/
- Clé API RIPE Atlas requise dans `.env` (`RIPE_ATLAS_API_KEY`)
