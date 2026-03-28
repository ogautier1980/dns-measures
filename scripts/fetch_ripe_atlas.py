#!/usr/bin/env python3
"""
Récupération des résultats de mesures RIPE Atlas.
Usage : python fetch_ripe_atlas.py --msm-id <id> --output data/raw/
"""
import os
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
import requests

API_BASE = "https://atlas.ripe.net/api/v2"
API_KEY  = os.getenv("RIPE_ATLAS_API_KEY", "")


def fetch_measurement_results(msm_id: int, start: datetime, stop: datetime,
                               output_dir: Path) -> Path:
    """Télécharge les résultats d'une mesure RIPE Atlas et les sauvegarde en JSON."""
    params = {
        "start":  int(start.timestamp()),
        "stop":   int(stop.timestamp()),
        "format": "json",
    }
    headers = {"Authorization": f"Key {API_KEY}"} if API_KEY else {}

    url = f"{API_BASE}/measurements/{msm_id}/results/"
    print(f"Fetching msm {msm_id} from {start.date()} to {stop.date()}...")

    results = []
    while url:
        r = requests.get(url, params=params, headers=headers, timeout=60)
        r.raise_for_status()
        data = r.json()
        results.extend(data.get("results", data) if isinstance(data, dict) else data)
        url = data.get("next") if isinstance(data, dict) else None
        params = {}  # next URL already contains params

    output_dir.mkdir(parents=True, exist_ok=True)
    date_str = start.strftime("%Y-%m-%d")
    out_file = output_dir / f"msm_{msm_id}_{date_str}.json"
    out_file.write_text(json.dumps(results, indent=2))
    print(f"  → {len(results)} résultats sauvegardés dans {out_file}")
    return out_file


def main():
    parser = argparse.ArgumentParser(description="Fetch RIPE Atlas measurement results")
    parser.add_argument("--msm-id",  type=int, required=True, help="Measurement ID")
    parser.add_argument("--start",   type=str, required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--stop",    type=str, required=True, help="Stop date YYYY-MM-DD")
    parser.add_argument("--output",  type=str, default="data/raw", help="Output directory")
    args = parser.parse_args()

    start = datetime.fromisoformat(args.start).replace(tzinfo=timezone.utc)
    stop  = datetime.fromisoformat(args.stop).replace(tzinfo=timezone.utc)
    fetch_measurement_results(args.msm_id, start, stop, Path(args.output))


if __name__ == "__main__":
    main()
