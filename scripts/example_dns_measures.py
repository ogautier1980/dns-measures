#!/usr/bin/env python3
"""
Exemple de script pour les mesures DNS dans l'espace et le temps.
Ce script illustre les principales fonctionnalites disponibles dans le container.

Auteur: [Votre nom]
Memoire: Mesures DNS dans l'espace et le temps
"""

import asyncio
from datetime import datetime
from pathlib import Path

# === DNS ===
import dns.resolver
import dns.query
import dns.zone
from tldextract import extract as tld_extract

# === RIPE Atlas ===
# from ripe.atlas.cousteau import AtlasCreateRequest, Dns, AtlasSource
# from ripe.atlas.sagan import DnsResult

# === Data Analysis ===
import pandas as pd
import numpy as np

# === Visualization ===
import matplotlib.pyplot as plt
import seaborn as sns

# === HTTP ===
import requests

# === Progress bars ===
from tqdm import tqdm

# === Logging ===
from loguru import logger


def fetch_tranco_list(top_n: int = 1000) -> pd.DataFrame:
    """
    Telecharge la liste Tranco des domaines les plus populaires.

    Args:
        top_n: Nombre de domaines a recuperer

    Returns:
        DataFrame avec les domaines et leur rang
    """
    logger.info(f"Telechargement de la liste Tranco (top {top_n})...")

    # URL de la liste Tranco (derniere version)
    url = "https://tranco-list.eu/top-1m.csv.zip"

    try:
        # Telecharger et lire directement le CSV
        df = pd.read_csv(
            url,
            compression='zip',
            names=['rank', 'domain'],
            nrows=top_n
        )
        logger.success(f"Liste Tranco telechargee: {len(df)} domaines")
        return df
    except Exception as e:
        logger.error(f"Erreur lors du telechargement: {e}")
        # Retourner quelques domaines de test
        return pd.DataFrame({
            'rank': range(1, 11),
            'domain': [
                'google.com', 'facebook.com', 'youtube.com', 'twitter.com',
                'instagram.com', 'linkedin.com', 'wikipedia.org', 'amazon.com',
                'netflix.com', 'microsoft.com'
            ]
        })


def resolve_dns(domain: str, record_type: str = 'A') -> dict:
    """
    Resout un enregistrement DNS pour un domaine.

    Args:
        domain: Nom de domaine
        record_type: Type d'enregistrement (A, AAAA, MX, NS, TXT, etc.)

    Returns:
        Dictionnaire avec les resultats
    """
    result = {
        'domain': domain,
        'record_type': record_type,
        'timestamp': datetime.utcnow().isoformat(),
        'answers': [],
        'error': None
    }

    try:
        answers = dns.resolver.resolve(domain, record_type)
        result['answers'] = [str(rdata) for rdata in answers]
    except dns.resolver.NXDOMAIN:
        result['error'] = 'NXDOMAIN'
    except dns.resolver.NoAnswer:
        result['error'] = 'NoAnswer'
    except dns.resolver.NoNameservers:
        result['error'] = 'NoNameservers'
    except dns.exception.Timeout:
        result['error'] = 'Timeout'
    except Exception as e:
        result['error'] = str(e)

    return result


def measure_domains(domains: list, record_types: list = ['A', 'AAAA', 'MX', 'NS']) -> pd.DataFrame:
    """
    Effectue des mesures DNS sur une liste de domaines.

    Args:
        domains: Liste de domaines
        record_types: Types d'enregistrements a interroger

    Returns:
        DataFrame avec tous les resultats
    """
    results = []

    for domain in tqdm(domains, desc="Mesures DNS"):
        for rtype in record_types:
            result = resolve_dns(domain, rtype)
            results.append(result)

    return pd.DataFrame(results)


def analyze_results(df: pd.DataFrame) -> dict:
    """
    Analyse les resultats des mesures DNS.

    Args:
        df: DataFrame des resultats

    Returns:
        Dictionnaire avec les statistiques
    """
    stats = {
        'total_queries': len(df),
        'successful_queries': len(df[df['error'].isna()]),
        'failed_queries': len(df[df['error'].notna()]),
        'success_rate': len(df[df['error'].isna()]) / len(df) * 100,
        'errors_by_type': df[df['error'].notna()]['error'].value_counts().to_dict(),
        'queries_by_record_type': df['record_type'].value_counts().to_dict()
    }

    return stats


def plot_results(df: pd.DataFrame, output_path: Path = None):
    """
    Visualise les resultats des mesures.

    Args:
        df: DataFrame des resultats
        output_path: Chemin pour sauvegarder le graphique
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Graphique 1: Taux de succes par type d'enregistrement
    success_by_type = df.groupby('record_type').apply(
        lambda x: (x['error'].isna().sum() / len(x)) * 100
    )
    axes[0].bar(success_by_type.index, success_by_type.values, color='steelblue')
    axes[0].set_xlabel('Type d\'enregistrement')
    axes[0].set_ylabel('Taux de succes (%)')
    axes[0].set_title('Taux de succes par type d\'enregistrement DNS')
    axes[0].set_ylim(0, 100)

    # Graphique 2: Distribution des erreurs
    errors = df[df['error'].notna()]['error'].value_counts()
    if len(errors) > 0:
        axes[1].pie(errors.values, labels=errors.index, autopct='%1.1f%%')
        axes[1].set_title('Distribution des erreurs')
    else:
        axes[1].text(0.5, 0.5, 'Aucune erreur', ha='center', va='center')
        axes[1].set_title('Distribution des erreurs')

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        logger.info(f"Graphique sauvegarde: {output_path}")

    plt.show()


def create_ripe_atlas_measurement(domains: list, probe_count: int = 10) -> dict:
    """
    Cree une mesure RIPE Atlas pour les domaines specifies.
    NOTE: Necessite une cle API RIPE Atlas.

    Args:
        domains: Liste de domaines a mesurer
        probe_count: Nombre de sondes a utiliser

    Returns:
        Configuration de la mesure
    """
    # Configuration de base pour une mesure DNS RIPE Atlas
    measurement_config = {
        'definitions': [],
        'probes': {
            'type': 'area',
            'value': 'WW',  # World Wide
            'requested': probe_count
        }
    }

    for domain in domains:
        measurement_config['definitions'].append({
            'type': 'dns',
            'af': 4,  # IPv4
            'description': f'DNS measure for {domain}',
            'query_class': 'IN',
            'query_type': 'A',
            'query_argument': domain,
            'use_probe_resolver': False,
            'protocol': 'UDP'
        })

    logger.info(f"Configuration de mesure RIPE Atlas creee pour {len(domains)} domaines")
    return measurement_config


def main():
    """Fonction principale."""
    logger.info("=== Mesures DNS dans l'espace et le temps ===")

    # 1. Recuperer la liste Tranco
    tranco = fetch_tranco_list(top_n=100)
    logger.info(f"Top 5 domaines: {tranco['domain'].head().tolist()}")

    # 2. Effectuer des mesures DNS (sur un echantillon)
    sample_domains = tranco['domain'].head(10).tolist()
    logger.info(f"Mesures DNS sur {len(sample_domains)} domaines...")

    results = measure_domains(sample_domains, record_types=['A', 'AAAA', 'MX'])

    # 3. Analyser les resultats
    stats = analyze_results(results)
    logger.info(f"Statistiques:")
    logger.info(f"  - Requetes totales: {stats['total_queries']}")
    logger.info(f"  - Taux de succes: {stats['success_rate']:.1f}%")

    # 4. Sauvegarder les resultats
    output_dir = Path('/workspace/output')
    output_dir.mkdir(exist_ok=True)

    results.to_csv(output_dir / 'dns_results.csv', index=False)
    logger.success(f"Resultats sauvegardes: {output_dir / 'dns_results.csv'}")

    # 5. Visualiser
    plot_results(results, output_dir / 'dns_analysis.png')

    # 6. Exemple de configuration RIPE Atlas
    ripe_config = create_ripe_atlas_measurement(sample_domains[:5])
    logger.info(f"Exemple de configuration RIPE Atlas: {len(ripe_config['definitions'])} mesures")

    logger.success("=== Mesures terminees ===")


if __name__ == '__main__':
    main()
