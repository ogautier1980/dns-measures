#!/usr/bin/env python3
"""
Parse les résultats JSON RIPE Atlas en DataFrame Parquet.
Usage : python parse_dns_results.py --input data/raw/ --output data/processed/
"""
import json
import argparse
from pathlib import Path
import pandas as pd


def parse_result(r: dict) -> dict | None:
    """Extrait les champs pertinents d'un résultat DNS RIPE Atlas."""
    try:
        answers = r.get("result", {}).get("answers", [])
        answer_ips = [a.get("data", "") for a in answers if a.get("type") in ("A", "AAAA")]
        return {
            "msm_id":       r.get("msm_id"),
            "prb_id":       r.get("prb_id"),
            "timestamp":    r.get("timestamp"),
            "probe_country": r.get("probe", {}).get("country_code", ""),
            "probe_asn":    r.get("probe", {}).get("asn_v4"),
            "rcode":        r.get("result", {}).get("ANCOUNT", -1),
            "answer_ips":   ",".join(answer_ips),
            "rt_ms":        r.get("result", {}).get("rt"),
        }
    except Exception:
        return None


def process_file(json_file: Path) -> pd.DataFrame:
    data = json.loads(json_file.read_text())
    rows = [parse_result(r) for r in data]
    return pd.DataFrame([r for r in rows if r])


def main():
    parser = argparse.ArgumentParser(description="Parse RIPE Atlas DNS results to Parquet")
    parser.add_argument("--input",  type=str, default="data/raw",       help="Input directory")
    parser.add_argument("--output", type=str, default="data/processed", help="Output directory")
    args = parser.parse_args()

    in_dir  = Path(args.input)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    json_files = sorted(in_dir.glob("*.json"))
    print(f"Processing {len(json_files)} JSON files...")

    frames = [process_file(f) for f in json_files]
    if not frames:
        print("No data found.")
        return

    df = pd.concat(frames, ignore_index=True)
    out_file = out_dir / "dns_results.parquet"
    df.to_parquet(out_file, index=False)
    print(f"→ {len(df):,} résultats → {out_file}")


if __name__ == "__main__":
    main()
