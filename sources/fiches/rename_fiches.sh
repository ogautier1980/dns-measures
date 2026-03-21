#!/bin/bash
# Renommage des fiches existantes pour cohérence avec convention [auteur][année]_[descriptif].md

rename_if_exists() {
    old="$1"
    new="$2"
    if [ -f "$old" ]; then
        if [ -f "$new" ]; then
            echo "⚠️  SKIP: $new existe déjà"
        else
            mv "$old" "$new"
            echo "✅ $old → $new"
        fi
    else
        echo "❌ NOT FOUND: $old"
    fi
}

echo "=== Renommage des fiches pour cohérence ==="
echo ""

# Déjà bien nommé - garder
echo "✓ vanderToorn2018_snowshoe_spam_dns.md - OK (déjà conforme)"

# À renommer pour cohérence
rename_if_exists "bortzmeyer_dns_measurements_atlas.md" "bortzmeyer_dns_measurements_atlas_tutorial.md"
rename_if_exists "holterbach2015_atlas_interference.md" "holterbach2015_ripeatlas_interference.md"
rename_if_exists "lePochat2019_tranco.md" "lePochat2019_tranco_ranking.md"
rename_if_exists "vanRijswijk2016_openintel.md" "vanRijswijk2016_openintel_infrastructure.md"

# Celui-ci est OK
echo "✓ nosyk2024_ripeatlas_ditl.md - OK (déjà conforme)"

echo ""
echo "=== Renommage terminé ==="
