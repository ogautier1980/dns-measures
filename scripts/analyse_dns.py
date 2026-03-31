#!/usr/bin/env python3
"""
Étape 5 du pipeline — Analyse quantitative répondant à Q1–Q4.

Q1 : Quelle proportion des domaines retourne des réponses géographiquement
     différenciées, et quels mécanismes l'expliquent ?
Q2 : Stabilité temporelle des réponses DNS (jour, semaine, mois).
Q3 : Les biais géographiques de RIPE Atlas limitent-ils l'observation de
     la variation DNS géographique ?
Q4 : Impact du type de résolveur (ISP local vs DNS public) sur les réponses.

Sorties :
  reports/q1_geo_diversity.csv / .json
  reports/q2_temporal_stability.csv / .json
  reports/q3_probe_bias.csv / .json
  reports/q4_resolver_impact.csv / .json
  reports/summary_stats.json
  latex/figures/fig_q*.png  (figures prêtes pour le LaTeX)

Usage :
  python analyse_dns.py [--data data/processed/dns_results.parquet]
                        [--output reports/]
                        [--figures latex/figures/]
                        [--questions q1,q2,q3,q4]
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from scipy import stats

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Helpers communs
# ──────────────────────────────────────────────────────────────────────────────

FIGURE_DPI    = 150
FIGURE_WIDTH  = 7.0
FIGURE_HEIGHT = 4.5

CONTINENT_LABELS = {
    "EU": "Europe", "NA": "Amér. Nord", "SA": "Amér. Sud",
    "AF": "Afrique", "AP": "Asie-Pacifique", "OC": "Océanie",
}

def save_fig(fig: plt.Figure, path: Path, tight: bool = True) -> None:
    if tight:
        fig.tight_layout()
    fig.savefig(path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    log.info("Figure sauvegardée : %s", path)


def load_data(parquet_path: Path) -> pd.DataFrame:
    log.info("Chargement des données : %s", parquet_path)
    df = pd.read_parquet(parquet_path)
    log.info("  %d lignes  %d colonnes", len(df), len(df.columns))
    log.info("  Dates : %s → %s", df["date"].min(), df["date"].max())
    log.info("  Domaines uniques : %d", df["query_domain"].nunique())
    log.info("  Sondes uniques   : %d", df["prb_id"].nunique())
    return df


# ──────────────────────────────────────────────────────────────────────────────
# Q1 — Diversité géographique des réponses
# ──────────────────────────────────────────────────────────────────────────────

def analyse_q1(df: pd.DataFrame, out_dir: Path, fig_dir: Path) -> dict:
    """
    Pour chaque domaine et chaque jour, calcule si les réponses DNS varient
    selon la région géographique de la sonde.

    Un domaine est classé "géo-différencié" si au moins deux continents
    reçoivent des ensembles d'IPs de réponse distincts.
    """
    log.info("=== Q1 : Diversité géographique ===")

    # Filtrer les réponses valides (RCODE=0, au moins une IP)
    valid = df[(df["rcode"] == 0) & (df["answer_count"] > 0)].copy()

    results = []
    for (domain, date), group in valid.groupby(["query_domain", "date"]):
        # Ensemble d'IPs par continent
        ips_by_cont = (
            group.groupby("continent")["answer_ips"]
            .apply(lambda s: frozenset("|".join(s).split("|")))
        )

        # Nombre d'ensembles d'IPs distincts entre continents
        unique_ip_sets  = len(set(ips_by_cont))
        n_continents    = len(ips_by_cont)
        is_geo_diverse  = unique_ip_sets > 1

        # Présence de NSID (indique anycast instanceable)
        has_nsid = group["nsid_str"].str.len().gt(0).any()

        results.append({
            "domain":          domain,
            "date":            date,
            "n_continents":    n_continents,
            "unique_ip_sets":  unique_ip_sets,
            "is_geo_diverse":  is_geo_diverse,
            "has_nsid":        has_nsid,
            "n_probes":        len(group),
        })

    q1_df = pd.DataFrame(results)

    # Agrégation par domaine (sur toute la période)
    by_domain = q1_df.groupby("domain").agg(
        days_measured       = ("date", "count"),
        days_geo_diverse    = ("is_geo_diverse", "sum"),
        avg_unique_ip_sets  = ("unique_ip_sets", "mean"),
        has_nsid            = ("has_nsid", "any"),
    ).reset_index()
    by_domain["pct_geo_diverse"] = (
        100 * by_domain["days_geo_diverse"] / by_domain["days_measured"]
    )

    geo_div_count = (by_domain["days_geo_diverse"] > 0).sum()
    total_domains = len(by_domain)

    summary = {
        "total_domains_analysed":  total_domains,
        "geo_diverse_domains":     int(geo_div_count),
        "pct_geo_diverse":         round(100 * geo_div_count / total_domains, 1) if total_domains else 0,
        "domains_with_nsid":       int(by_domain["has_nsid"].sum()),
        "pct_domains_with_nsid":   round(100 * by_domain["has_nsid"].mean(), 1),
        "avg_unique_ip_sets":      round(float(by_domain["avg_unique_ip_sets"].mean()), 2),
    }
    log.info("Q1 : %d/%d domaines géo-différenciés (%.1f%%)",
             geo_div_count, total_domains, summary["pct_geo_diverse"])

    # Export
    by_domain.to_csv(out_dir / "q1_geo_diversity.csv", index=False)

    # ── Figure Q1a : distribution du nombre d'ensembles d'IPs distincts ──────
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    counts = by_domain["avg_unique_ip_sets"].round().value_counts().sort_index()
    ax.bar(counts.index.astype(int), counts.values, color="#2563EB", edgecolor="white")
    ax.set_xlabel("Nombre d'ensembles d'IPs distincts (entre continents)", fontsize=11)
    ax.set_ylabel("Nombre de domaines", fontsize=11)
    ax.set_title("Q1 — Distribution de la diversité géographique des réponses DNS", fontsize=12)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    save_fig(fig, fig_dir / "fig_q1a_ip_set_diversity.png")

    # ── Figure Q1b : top 20 domaines les plus géo-diversifiés ────────────────
    top20 = by_domain.nlargest(20, "avg_unique_ip_sets")[["domain", "avg_unique_ip_sets"]]
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 5.5))
    ax.barh(top20["domain"][::-1], top20["avg_unique_ip_sets"][::-1], color="#7C3AED")
    ax.set_xlabel("Moyenne d'ensembles d'IPs distincts", fontsize=11)
    ax.set_title("Q1 — Top 20 domaines géo-différenciés", fontsize=12)
    save_fig(fig, fig_dir / "fig_q1b_top20_geo_diverse.png")

    return summary


# ──────────────────────────────────────────────────────────────────────────────
# Q2 — Stabilité temporelle
# ──────────────────────────────────────────────────────────────────────────────

def analyse_q2(df: pd.DataFrame, out_dir: Path, fig_dir: Path) -> dict:
    """
    Mesure la stabilité temporelle : pour chaque domaine et chaque sonde,
    calcule le taux de changement des IPs de réponse entre jours consécutifs.
    """
    log.info("=== Q2 : Stabilité temporelle ===")

    valid = df[(df["rcode"] == 0) & (df["answer_count"] > 0)].copy()
    valid["date"] = pd.to_datetime(valid["date"])
    valid = valid.sort_values(["query_domain", "prb_id", "date"])

    # Pour chaque (domaine, sonde), calculer si l'IP a changé d'un jour à l'autre
    changes = []
    for (domain, prb), group in valid.groupby(["query_domain", "prb_id"]):
        group = group.sort_values("date")
        ips   = group["answer_ips"].tolist()
        dates = group["date"].tolist()

        for i in range(1, len(ips)):
            delta_days = (dates[i] - dates[i-1]).days
            changed    = (ips[i] != ips[i-1])
            changes.append({
                "domain":     domain,
                "prb_id":     prb,
                "date":       dates[i].strftime("%Y-%m-%d"),
                "delta_days": delta_days,
                "changed":    changed,
            })

    if not changes:
        log.warning("Q2 : pas assez de données temporelles (au moins 2 jours nécessaires)")
        return {"error": "insufficient_data"}

    ch_df = pd.DataFrame(changes)

    # Taux de changement par delta_days (1j, 7j, 30j)
    stability = {}
    for window, label in [(1, "jour"), (7, "semaine"), (30, "mois")]:
        subset = ch_df[ch_df["delta_days"] <= window]
        if len(subset):
            rate = subset["changed"].mean()
            stability[label] = round(100 * rate, 2)

    log.info("Q2 taux de changement : %s", stability)

    # Taux par domaine
    by_domain = ch_df.groupby("domain")["changed"].mean().reset_index()
    by_domain.columns = ["domain", "change_rate"]
    by_domain["change_rate_pct"] = (100 * by_domain["change_rate"]).round(2)

    by_domain.to_csv(out_dir / "q2_temporal_stability.csv", index=False)

    summary = {
        "stability_by_window":    stability,
        "domains_fully_stable":   int((by_domain["change_rate"] == 0).sum()),
        "pct_domains_fully_stable": round(
            100 * (by_domain["change_rate"] == 0).mean(), 1
        ),
        "median_change_rate_pct": round(float(by_domain["change_rate_pct"].median()), 2),
    }

    # ── Figure Q2 : distribution du taux de changement ────────────────────────
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    ax.hist(by_domain["change_rate_pct"], bins=50, color="#059669", edgecolor="white")
    ax.set_xlabel("Taux de changement de réponse DNS (%)", fontsize=11)
    ax.set_ylabel("Nombre de domaines", fontsize=11)
    ax.set_title("Q2 — Distribution de la stabilité temporelle des réponses DNS", fontsize=12)
    ax.axvline(by_domain["change_rate_pct"].median(), color="red", linestyle="--",
               label=f"Médiane : {by_domain['change_rate_pct'].median():.1f}%")
    ax.legend()
    save_fig(fig, fig_dir / "fig_q2_temporal_stability.png")

    return summary


# ──────────────────────────────────────────────────────────────────────────────
# Q3 — Biais géographique des sondes RIPE Atlas
# ──────────────────────────────────────────────────────────────────────────────

def analyse_q3(df: pd.DataFrame, out_dir: Path, fig_dir: Path) -> dict:
    """
    Évalue si le biais géographique de RIPE Atlas (surreprésentation EU/NA)
    limite la capacité à observer la variation DNS géographique.

    Approche :
      - Distribution effective des sondes par continent
      - Taux de couverture par continent (% de domaines observés par ≥1 sonde)
      - Test de Mann-Whitney : variation DNS observée EU+NA vs autres régions
    """
    log.info("=== Q3 : Biais géographique des sondes ===")

    # Distribution des sondes par continent
    probe_dist = (
        df.drop_duplicates("prb_id")
        .groupby("continent")["prb_id"].count()
        .reset_index()
    )
    probe_dist.columns = ["continent", "n_probes"]
    probe_dist["pct"] = (100 * probe_dist["n_probes"] / probe_dist["n_probes"].sum()).round(1)

    log.info("Distribution sondes : %s", probe_dist.set_index("continent")["n_probes"].to_dict())

    # Couverture des domaines par continent
    coverage = (
        df[df["rcode"] == 0]
        .groupby("continent")["query_domain"]
        .nunique()
        .reset_index()
    )
    coverage.columns = ["continent", "domains_covered"]

    total_domains = df["query_domain"].nunique()
    coverage["coverage_pct"] = (100 * coverage["domains_covered"] / total_domains).round(1)

    # Variation DNS (nombre d'IPs uniques par domaine) par continent
    valid = df[(df["rcode"] == 0) & (df["answer_count"] > 0)]
    ip_diversity = (
        valid.groupby(["continent", "query_domain"])["answer_ips"]
        .apply(lambda s: len(set("|".join(s).split("|"))))
        .reset_index()
    )
    ip_diversity.columns = ["continent", "domain", "n_unique_ips"]

    diversity_by_cont = (
        ip_diversity.groupby("continent")["n_unique_ips"]
        .agg(["mean", "median", "std"])
        .reset_index()
    )

    # Test Mann-Whitney EU+NA vs autres
    eu_na   = ip_diversity[ip_diversity["continent"].isin(["EU", "NA"])]["n_unique_ips"]
    others  = ip_diversity[~ip_diversity["continent"].isin(["EU", "NA"])]["n_unique_ips"]
    if len(eu_na) > 5 and len(others) > 5:
        stat, pvalue = stats.mannwhitneyu(eu_na, others, alternative="two-sided")
        mw_result = {"statistic": float(stat), "pvalue": float(pvalue),
                     "significant": bool(pvalue < 0.05)}
    else:
        mw_result = {"statistic": None, "pvalue": None, "significant": None}

    log.info("Q3 Mann-Whitney EU+NA vs autres : %s", mw_result)

    probe_dist.to_csv(out_dir / "q3_probe_distribution.csv", index=False)
    diversity_by_cont.to_csv(out_dir / "q3_probe_bias.csv", index=False)

    summary = {
        "probe_distribution":  probe_dist.to_dict(orient="records"),
        "coverage_by_continent": coverage.to_dict(orient="records"),
        "diversity_by_continent": diversity_by_cont.round(3).to_dict(orient="records"),
        "mannwhitney_euna_vs_others": mw_result,
    }

    # ── Figure Q3a : distribution des sondes par continent ────────────────────
    conts  = [CONTINENT_LABELS.get(c, c) for c in probe_dist["continent"]]
    fig, axes = plt.subplots(1, 2, figsize=(FIGURE_WIDTH * 1.4, FIGURE_HEIGHT))

    axes[0].bar(conts, probe_dist["n_probes"], color="#DC2626", edgecolor="white")
    axes[0].set_title("Sondes RIPE Atlas par continent", fontsize=11)
    axes[0].set_ylabel("Nombre de sondes")
    axes[0].tick_params(axis="x", rotation=30)

    conts2 = [CONTINENT_LABELS.get(c, c) for c in diversity_by_cont["continent"]]
    axes[1].bar(conts2, diversity_by_cont["mean"], color="#D97706", edgecolor="white",
                yerr=diversity_by_cont["std"], capsize=4)
    axes[1].set_title("IPs uniques observées par continent", fontsize=11)
    axes[1].set_ylabel("Moy. IPs uniques / domaine")
    axes[1].tick_params(axis="x", rotation=30)

    save_fig(fig, fig_dir / "fig_q3_probe_bias.png")

    return summary


# ──────────────────────────────────────────────────────────────────────────────
# Q4 — Impact du type de résolveur
# ──────────────────────────────────────────────────────────────────────────────

def analyse_q4(df: pd.DataFrame, out_dir: Path, fig_dir: Path) -> dict:
    """
    Compare les réponses DNS obtenues via :
      - Résolveur ISP local (use_probe_resolver=True)
      - Google Public DNS (8.8.8.8)
      - Cloudflare DNS (1.1.1.1)
      - Quad9 (9.9.9.9)

    Métriques : taux de divergence d'IPs, RTT, taux d'erreur.
    """
    log.info("=== Q4 : Impact du type de résolveur ===")

    PUBLIC_IPS = {"8.8.8.8", "1.1.1.1", "9.9.9.9"}

    # Identifier la nature du résolveur
    def resolver_label(row) -> str:
        if row.get("use_probe_resolver"):
            return "ISP local"
        ip = str(row.get("resolver_ip", ""))
        if ip == "8.8.8.8":   return "Google (8.8.8.8)"
        if ip == "1.1.1.1":   return "Cloudflare (1.1.1.1)"
        if ip == "9.9.9.9":   return "Quad9 (9.9.9.9)"
        return "Autre"

    q4_df = df[
        df["use_probe_resolver"].fillna(False) |
        df["resolver_ip"].isin(PUBLIC_IPS)
    ].copy()

    if q4_df.empty:
        log.warning("Q4 : aucune donnée de campagne résolveur — vérifier measurements.json")
        return {"error": "no_q4_data"}

    q4_df["resolver_label"] = q4_df.apply(resolver_label, axis=1)

    # Statistiques par résolveur
    stats_df = q4_df.groupby("resolver_label").agg(
        n_measurements  = ("msm_id", "count"),
        error_rate      = ("rcode", lambda x: (x != 0).mean()),
        avg_rt_ms       = ("rt_ms", "mean"),
        median_rt_ms    = ("rt_ms", "median"),
        avg_answers     = ("answer_count", "mean"),
    ).reset_index()
    stats_df = stats_df.round(3)

    log.info("Q4 statistiques résolveurs :\n%s", stats_df.to_string())

    # Divergence : pour chaque (domaine, sonde, date), comparer ISP vs public
    pivot = q4_df.pivot_table(
        index=["query_domain", "prb_id", "date"],
        columns="resolver_label",
        values="answer_ips",
        aggfunc="first",
    )

    divergence_rates = {}
    for col in pivot.columns:
        if col == "ISP local":
            continue
        if "ISP local" not in pivot.columns:
            break
        both = pivot[["ISP local", col]].dropna()
        if len(both):
            rate = (both["ISP local"] != both[col]).mean()
            divergence_rates[f"ISP_vs_{col}"] = round(float(rate) * 100, 2)

    log.info("Q4 taux de divergence : %s", divergence_rates)

    stats_df.to_csv(out_dir / "q4_resolver_impact.csv", index=False)

    summary = {
        "resolver_stats":   stats_df.to_dict(orient="records"),
        "divergence_rates": divergence_rates,
    }

    # ── Figure Q4a : RTT médian par résolveur ─────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(FIGURE_WIDTH * 1.4, FIGURE_HEIGHT))

    resolvers = stats_df["resolver_label"].tolist()
    colors    = ["#3B82F6", "#EF4444", "#F59E0B", "#10B981"][:len(resolvers)]

    axes[0].bar(resolvers, stats_df["median_rt_ms"], color=colors, edgecolor="white")
    axes[0].set_title("RTT médian par résolveur (ms)", fontsize=11)
    axes[0].set_ylabel("RTT médian (ms)")
    axes[0].tick_params(axis="x", rotation=25)

    axes[1].bar(resolvers, 100 * stats_df["error_rate"], color=colors, edgecolor="white")
    axes[1].set_title("Taux d'erreur DNS par résolveur (%)", fontsize=11)
    axes[1].set_ylabel("Taux d'erreur (%)")
    axes[1].tick_params(axis="x", rotation=25)

    save_fig(fig, fig_dir / "fig_q4_resolver_comparison.png")

    # ── Figure Q4b : taux de divergence ──────────────────────────────────────
    if divergence_rates:
        fig, ax = plt.subplots(figsize=(FIGURE_WIDTH * 0.8, FIGURE_HEIGHT * 0.8))
        labels = [k.replace("ISP_vs_", "ISP vs\n") for k in divergence_rates]
        values = list(divergence_rates.values())
        ax.bar(labels, values, color="#6366F1", edgecolor="white")
        ax.set_ylabel("Taux de divergence (%)")
        ax.set_title("Q4 — Divergence ISP local vs résolveurs publics", fontsize=11)
        save_fig(fig, fig_dir / "fig_q4b_divergence.png")

    return summary


# ──────────────────────────────────────────────────────────────────────────────
# Statistiques générales
# ──────────────────────────────────────────────────────────────────────────────

def compute_summary_stats(df: pd.DataFrame) -> dict:
    return {
        "total_measurements":  len(df),
        "unique_domains":      int(df["query_domain"].nunique()),
        "unique_probes":       int(df["prb_id"].nunique()),
        "unique_countries":    int(df["country_code"].nunique()),
        "date_range":          {"min": df["date"].min(), "max": df["date"].max()},
        "rcode_distribution":  df["rcode"].value_counts().to_dict(),
        "avg_rt_ms":           round(float(df["rt_ms"].mean()), 2) if "rt_ms" in df else None,
        "pct_with_nsid":       round(100 * df["nsid_str"].str.len().gt(0).mean(), 1),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Point d'entrée
# ──────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyse quantitative DNS — Q1 à Q4"
    )
    parser.add_argument(
        "--data", type=str, default="data/processed/dns_results.parquet",
        help="Fichier Parquet des résultats (sortie de parse_dns_results.py)"
    )
    parser.add_argument(
        "--output", type=str, default="reports",
        help="Répertoire pour les CSV/JSON de résultats"
    )
    parser.add_argument(
        "--figures", type=str, default="latex/figures",
        help="Répertoire pour les figures PNG"
    )
    parser.add_argument(
        "--questions", type=str, default="q1,q2,q3,q4",
        help="Questions à analyser, séparées par virgule (défaut: q1,q2,q3,q4)"
    )
    args = parser.parse_args()

    data_path = Path(args.data)
    out_dir   = Path(args.output)
    fig_dir   = Path(args.figures)

    if not data_path.exists():
        log.error("Données introuvables : %s — lancez d'abord parse_dns_results.py", data_path)
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    df = load_data(data_path)
    questions = [q.strip().lower() for q in args.questions.split(",")]

    all_results = {}

    # Statistiques générales
    all_results["summary"] = compute_summary_stats(df)
    log.info("Stats générales : %s", all_results["summary"])

    if "q1" in questions:
        all_results["q1"] = analyse_q1(df, out_dir, fig_dir)

    if "q2" in questions:
        all_results["q2"] = analyse_q2(df, out_dir, fig_dir)

    if "q3" in questions:
        all_results["q3"] = analyse_q3(df, out_dir, fig_dir)

    if "q4" in questions:
        all_results["q4"] = analyse_q4(df, out_dir, fig_dir)

    # Sauvegarder le résumé global
    summary_path = out_dir / "summary_stats.json"
    summary_path.write_text(json.dumps(all_results, indent=2, default=str))
    log.info("Résumé global : %s", summary_path)

    log.info("Étape 5 terminée — analyses Q%s complètes",
             "+Q".join(q.upper()[1:] for q in questions))
    return 0


if __name__ == "__main__":
    sys.exit(main())
