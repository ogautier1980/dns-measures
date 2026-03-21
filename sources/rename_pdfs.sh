#!/bin/bash
# Script de renommage des PDFs selon convention [auteur][année]_[descriptif].pdf

# Fonction de renommage sécurisée
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

echo "=== Renommage des PDFs - Convention [auteur][année]_[descriptif].pdf ==="
echo ""

# Déjà bien nommés (garder tel quel)
echo "Fichiers déjà bien nommés :"
ls -1 "A High-Performance"* 2>/dev/null && echo "  → Sera renommé"
ls -1 "TRANCO"* 2>/dev/null && echo "  → Sera renommé"
ls -1 "DNS-Measurements"* 2>/dev/null && echo "  → Sera renommé"
echo ""

# Renommages
rename_if_exists "A High-Performance, Scalable Infrastructure for Large-Scale Active DNS Measurements.pdf" "vanRijswijk2016_openintel_infrastructure.pdf"
rename_if_exists "TRANCO A Research-Oriented Top Sites Ranking Hardened Against Manipulation.pdf" "lePochat2019_tranco_ranking.pdf"
rename_if_exists "Holterbach2015.pdf" "holterbach2015_ripeatlas_interference.pdf"
rename_if_exists "DNS-Measurements-with-RIPE-Atlas.pdf" "bortzmeyer_dns_measurements_atlas_tutorial.pdf"
rename_if_exists "Detecting DNS Root Manipulation.pdf" "johnson2016_dns_root_manipulation.pdf"
rename_if_exists "noms2018.pdf" "vanderToorn2018_snowshoe_spam_dns.pdf"
rename_if_exists "tma2024poster-final1.pdf" "boswell2024_internal_names_ripeatlas.pdf"
rename_if_exists "2815675.2815717.pdf" "calder2015_anycast_cdn_performance.pdf"
rename_if_exists "3452296.3472891.pdf" "koch2021_anycast_context.pdf"
rename_if_exists "1-s2.0-S1389128616302006-main.pdf" "hours2016_dns_resolvers_cdn_impact.pdf"
rename_if_exists "1-s2.0-S2352864817300731-main.pdf" "wang2018_dns_cdn_challenges.pdf"
rename_if_exists "applsci-13-05739.pdf" "xu2023_dns_infrastructure_centrality.pdf"
rename_if_exists "3763400.3763406.pdf" "li2025_global_cdn_analysis.pdf"
rename_if_exists "rfc7871.txt.pdf" "rfc7871_edns_client_subnet.pdf"
rename_if_exists "ripeatlas-im-2017.pdf" "bajpai2017_ripeatlas_tags.pdf"
rename_if_exists "2716281.2836101.pdf" "cicalese2015_conext.pdf"

echo ""
echo "=== Renommage terminé ==="
