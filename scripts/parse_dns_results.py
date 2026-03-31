#!/usr/bin/env python3
"""
Étape 4 du pipeline — Parsing des résultats JSON RIPE Atlas → Parquet.

Extrait pour chaque résultat :
  - Identifiants : msm_id, prb_id, timestamp
  - Sonde         : country_code, asn_v4, continent
  - DNS réponse   : rcode, answer_count, answer_ips (A/AAAA), ttl_min
  - RTT           : rt_ms
  - NSID          : nsid_hex, nsid_str (pour identifier l'instance anycast)
  - ABUF          : taille du paquet de réponse (bytes)
  - Résolveur Q4  : resolver_ip (si mesure via résolveur récursif)

Sortie : data/processed/dns_results.parquet (cumul journalier)
         data/processed/dns_results_<date>.parquet (archive par jour)

Usage :
  python parse_dns_results.py [--input data/raw/] [--output data/processed/]
                              [--date 2026-03-31]
"""

import argparse
import base64
import json
import logging
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# Colonnes du schéma Parquet final
SCHEMA = pa.schema([
    pa.field("msm_id",        pa.int64()),
    pa.field("prb_id",        pa.int32()),
    pa.field("timestamp",     pa.int64()),
    pa.field("date",          pa.string()),
    pa.field("country_code",  pa.string()),
    pa.field("asn_v4",        pa.int32()),
    pa.field("continent",     pa.string()),
    pa.field("query_domain",  pa.string()),
    pa.field("rcode",         pa.int16()),
    pa.field("answer_count",  pa.int16()),
    pa.field("answer_ips",    pa.string()),     # séparés par "|"
    pa.field("ttl_min",       pa.int32()),
    pa.field("rt_ms",         pa.float32()),
    pa.field("nsid_str",      pa.string()),
    pa.field("nsid_hex",      pa.string()),
    pa.field("abuf_size",     pa.int32()),
    pa.field("resolver_ip",   pa.string()),     # vide pour campagne principale
    pa.field("use_probe_resolver", pa.bool_()),
])


# ──────────────────────────────────────────────────────────────────────────────
# Décodage NSID
# ──────────────────────────────────────────────────────────────────────────────

def decode_nsid(abuf_b64: str | None) -> tuple[str, str]:
    """
    Extrait le NSID depuis le champ 'abuf' (réponse DNS encodée en base64).
    Retourne (nsid_str, nsid_hex) ou ("", "") si absent / illisible.

    L'ABUF est un paquet DNS binaire. L'option NSID est dans la section
    Additional / OPT record (type 41), option code 3 (RFC 5001).
    """
    if not abuf_b64:
        return "", ""
    try:
        raw = base64.b64decode(abuf_b64)
    except Exception:
        return "", ""

    # Parcourir le paquet DNS à la recherche du record OPT
    # Structure DNS header = 12 octets
    if len(raw) < 12:
        return "", ""

    offset = 12
    # Sauter question section
    try:
        offset = _skip_questions(raw, offset)
        # Sauter answer + authority sections
        ancount = struct.unpack("!H", raw[6:8])[0]
        nscount = struct.unpack("!H", raw[8:10])[0]
        arcount = struct.unpack("!H", raw[10:12])[0]

        for _ in range(ancount + nscount):
            offset = _skip_rr(raw, offset)

        # Chercher OPT dans additional
        for _ in range(arcount):
            rr_start = offset
            name_end = _skip_name(raw, offset)
            if name_end + 10 > len(raw):
                break
            rtype = struct.unpack("!H", raw[name_end:name_end + 2])[0]
            rdlen = struct.unpack("!H", raw[name_end + 8:name_end + 10])[0]
            rdata_start = name_end + 10

            if rtype == 41:  # OPT record
                nsid_str, nsid_hex = _parse_opt_nsid(raw, rdata_start, rdlen)
                if nsid_str or nsid_hex:
                    return nsid_str, nsid_hex

            offset = rdata_start + rdlen

    except (struct.error, IndexError):
        pass

    return "", ""


def _skip_name(data: bytes, offset: int) -> int:
    """Saute un nom DNS compressé, retourne l'offset après le nom."""
    while offset < len(data):
        length = data[offset]
        if length == 0:
            return offset + 1
        if (length & 0xC0) == 0xC0:   # pointeur de compression
            return offset + 2
        offset += length + 1
    return offset


def _skip_questions(data: bytes, offset: int) -> int:
    qdcount = struct.unpack("!H", data[4:6])[0]
    for _ in range(qdcount):
        offset = _skip_name(data, offset)
        offset += 4   # qtype + qclass
    return offset


def _skip_rr(data: bytes, offset: int) -> int:
    offset  = _skip_name(data, offset)
    rdlen   = struct.unpack("!H", data[offset + 8:offset + 10])[0]
    return offset + 10 + rdlen


def _parse_opt_nsid(data: bytes, rdata_start: int, rdlen: int) -> tuple[str, str]:
    """Parcourt les options EDNS0 d'un OPT record et retourne le NSID."""
    offset = rdata_start
    end    = rdata_start + rdlen
    while offset + 4 <= end:
        opt_code = struct.unpack("!H", data[offset:offset + 2])[0]
        opt_len  = struct.unpack("!H", data[offset + 2:offset + 4])[0]
        opt_data = data[offset + 4:offset + 4 + opt_len]
        if opt_code == 3:   # NSID option code
            nsid_hex = opt_data.hex()
            try:
                nsid_str = opt_data.decode("ascii")
            except Exception:
                nsid_str = opt_data.decode("latin-1", errors="replace")
            return nsid_str, nsid_hex
        offset += 4 + opt_len
    return "", ""


# ──────────────────────────────────────────────────────────────────────────────
# Continent mapping (réutilise la même logique que create_ripe_measurements.py)
# ──────────────────────────────────────────────────────────────────────────────

_EU = {"AL","AD","AT","BY","BE","BA","BG","HR","CY","CZ","DK","EE","FI","FR",
       "DE","GR","HU","IS","IE","IT","XK","LV","LI","LT","LU","MT","MD","MC",
       "ME","NL","MK","NO","PL","PT","RO","RU","SM","RS","SK","SI","ES","SE",
       "CH","UA","GB","VA"}
_NA = {"AG","BS","BB","BZ","CA","CR","CU","DM","DO","SV","GD","GT","HT","HN",
       "JM","MX","NI","PA","KN","LC","VC","TT","US"}
_SA = {"AR","BO","BR","CL","CO","EC","GY","PY","PE","SR","UY","VE"}
_AF = {"DZ","AO","BJ","BW","BF","BI","CV","CM","CF","TD","KM","CG","CD","CI",
       "DJ","EG","GQ","ER","SZ","ET","GA","GM","GH","GN","GW","KE","LS","LR",
       "LY","MG","MW","ML","MR","MU","MA","MZ","NA","NE","NG","RW","ST","SN",
       "SL","SO","ZA","SS","SD","TZ","TG","TN","UG","ZM","ZW"}
_OC = {"AU","FJ","KI","MH","FM","NR","NZ","PW","PG","WS","SB","TO","TV","VU"}

def _cc_to_continent(cc: str) -> str:
    cc = (cc or "").upper()
    if cc in _EU: return "EU"
    if cc in _NA: return "NA"
    if cc in _SA: return "SA"
    if cc in _AF: return "AF"
    if cc in _OC: return "OC"
    return "AP"


# ──────────────────────────────────────────────────────────────────────────────
# Parsing d'un résultat RIPE Atlas
# ──────────────────────────────────────────────────────────────────────────────

# Mapping RIPE Atlas rcode string → int
_RCODE_MAP = {
    "NOERROR": 0, "FORMERR": 1, "SERVFAIL": 2, "NXDOMAIN": 3,
    "NOTIMP": 4, "REFUSED": 5, "YXDOMAIN": 6, "YXRRSET": 7,
    "NXRRSET": 8, "NOTAUTH": 9, "NOTZONE": 10,
}

def parse_result(r: dict) -> dict | None:
    """
    Extrait tous les champs utiles d'un résultat DNS RIPE Atlas.
    Retourne None si le résultat est invalide / incomplet.
    """
    try:
        result_block = r.get("result", {})
        answers      = result_block.get("answers", []) or []

        # IPs de réponse (A et AAAA)
        answer_ips = []
        ttls       = []
        for a in answers:
            if a.get("type") in ("A", "AAAA"):
                ip = a.get("data", "").strip()
                if ip:
                    answer_ips.append(ip)
                ttl = a.get("TTL")
                if ttl is not None:
                    ttls.append(int(ttl))

        # RCODE : peut être string ou int selon l'API
        rcode_raw = result_block.get("ANCOUNT", result_block.get("rcode", -1))
        if isinstance(rcode_raw, str):
            rcode = _RCODE_MAP.get(rcode_raw.upper(), -1)
        else:
            rcode = int(rcode_raw) if rcode_raw is not None else -1

        # NSID depuis l'ABUF
        abuf     = result_block.get("abuf", "")
        nsid_str, nsid_hex = decode_nsid(abuf)

        # Taille ABUF
        abuf_size = len(base64.b64decode(abuf)) if abuf else 0

        # Métadonnées sonde
        probe_meta   = r.get("probe", {}) or {}
        country_code = (probe_meta.get("country_code") or r.get("country_code") or "").upper()
        asn_v4       = probe_meta.get("asn_v4") or r.get("from_asn")

        ts    = r.get("timestamp", 0)
        date  = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d") if ts else ""

        return {
            "msm_id":             r.get("msm_id"),
            "prb_id":             r.get("prb_id"),
            "timestamp":          ts,
            "date":               date,
            "country_code":       country_code,
            "asn_v4":             int(asn_v4) if asn_v4 else None,
            "continent":          _cc_to_continent(country_code),
            "query_domain":       result_block.get("qname", r.get("qname", "")),
            "rcode":              rcode,
            "answer_count":       len(answer_ips),
            "answer_ips":         "|".join(answer_ips),
            "ttl_min":            min(ttls) if ttls else None,
            "rt_ms":              result_block.get("rt"),
            "nsid_str":           nsid_str,
            "nsid_hex":           nsid_hex,
            "abuf_size":          abuf_size,
            "resolver_ip":        str(r.get("dst_addr", "") or ""),
            "use_probe_resolver": bool(r.get("use_probe_resolver", False)),
        }

    except Exception as exc:
        log.debug("Erreur parsing résultat prb=%s msm=%s : %s",
                  r.get("prb_id"), r.get("msm_id"), exc)
        return None


# ──────────────────────────────────────────────────────────────────────────────
# Traitement d'un fichier JSON
# ──────────────────────────────────────────────────────────────────────────────

def process_file(json_file: Path) -> pd.DataFrame:
    """Charge un fichier JSON RIPE Atlas et retourne un DataFrame."""
    raw  = json.loads(json_file.read_text())
    rows = [parse_result(r) for r in raw]
    rows = [r for r in rows if r]
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)


# ──────────────────────────────────────────────────────────────────────────────
# Point d'entrée
# ──────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Parse les résultats JSON RIPE Atlas en Parquet"
    )
    parser.add_argument(
        "--input", type=str, default="data/raw",
        help="Répertoire contenant les JSON bruts (défaut: data/raw)"
    )
    parser.add_argument(
        "--output", type=str, default="data/processed",
        help="Répertoire de sortie Parquet (défaut: data/processed)"
    )
    parser.add_argument(
        "--date", type=str, default=None,
        help="Ne traiter que les fichiers de cette date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Écraser le fichier Parquet existant plutôt que d'appender"
    )
    args = parser.parse_args()

    in_dir  = Path(args.input)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Sélection des fichiers à traiter
    if args.date:
        json_files = sorted(in_dir.glob(f"*{args.date}*.json"))
        date_suffix = f"_{args.date}"
    else:
        json_files = sorted(in_dir.glob("*.json"))
        date_suffix = ""

    # Exclure les fichiers d'erreurs
    json_files = [f for f in json_files if "fetch_errors" not in f.name]

    log.info("Traitement de %d fichiers JSON…", len(json_files))
    if not json_files:
        log.warning("Aucun fichier à traiter dans %s", in_dir)
        return 0

    frames = []
    errors = 0
    for i, f in enumerate(json_files, 1):
        try:
            df = process_file(f)
            if not df.empty:
                frames.append(df)
        except Exception as exc:
            log.error("  Erreur fichier %s : %s", f.name, exc)
            errors += 1
        if i % 100 == 0:
            log.info("  %d/%d  erreurs=%d", i, len(json_files), errors)

    if not frames:
        log.error("Aucun résultat parsé.")
        return 1

    df = pd.concat(frames, ignore_index=True)

    # Cast des types pour correspondre au schéma Parquet
    df["msm_id"]       = df["msm_id"].astype("Int64")
    df["prb_id"]       = df["prb_id"].astype("Int32")
    df["timestamp"]    = df["timestamp"].astype("Int64")
    df["asn_v4"]       = df["asn_v4"].astype("Int32")
    df["rcode"]        = df["rcode"].astype("Int16")
    df["answer_count"] = df["answer_count"].astype("Int16")
    df["ttl_min"]      = df["ttl_min"].astype("Int32")
    df["abuf_size"]    = df["abuf_size"].astype("Int32")
    df["rt_ms"]        = pd.to_numeric(df["rt_ms"], errors="coerce").astype("float32")

    for col in ("country_code", "continent", "query_domain",
                "answer_ips", "nsid_str", "nsid_hex", "resolver_ip", "date"):
        df[col] = df[col].fillna("").astype(str)

    # Fichier Parquet daté (archive)
    if args.date:
        dated_path = out_dir / f"dns_results_{args.date}.parquet"
        df.to_parquet(dated_path, index=False, schema=SCHEMA)
        log.info("Parquet daté : %s  (%d lignes)", dated_path, len(df))

    # Fichier Parquet cumulatif
    cumul_path = out_dir / "dns_results.parquet"
    if cumul_path.exists() and not args.overwrite:
        existing = pd.read_parquet(cumul_path)
        df = pd.concat([existing, df], ignore_index=True)
        # Dédupliquer sur (msm_id, prb_id, timestamp)
        before = len(df)
        df = df.drop_duplicates(subset=["msm_id", "prb_id", "timestamp"])
        log.info("Déduplication : %d → %d lignes", before, len(df))

    df.to_parquet(cumul_path, index=False)
    log.info("Parquet cumulatif : %s  (%d lignes total)", cumul_path, len(df))
    log.info("Étape 4 terminée — %d erreurs fichiers", errors)

    return 0


if __name__ == "__main__":
    sys.exit(main())
