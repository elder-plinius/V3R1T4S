#!/usr/bin/env python3
"""
Stage 0: Download Zenodo 23159774 archives, verify MD5 & compute SHA-256 manifest,
and extract into DREVAL_CAMPAIGN/data/.
Strictly respects the Air-Gap Rule: does NOT read any response values from
BeatAML2, PDX_Bruna, GDSC2, GDSC1, CCLE, or CTRPv1.
"""
import hashlib
import json
import os
import time
import zipfile
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ZIPS_DIR = DATA_DIR / "zenodo_zips"
ZIPS_DIR.mkdir(parents=True, exist_ok=True)

RECORD_ID = "23159774"
FILES_TO_FETCH = [
    "meta.zip",
    "splits.zip",
    "CTRPv2.zip",
    "BeatAML2.zip",
    "PDX_Bruna.zip",
    "GDSC2.zip",
]


def compute_hashes(path: Path) -> tuple[str, str]:
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            md5.update(chunk)
            sha256.update(chunk)
    return md5.hexdigest(), sha256.hexdigest()


def main():
    t0 = time.time()
    r = requests.get(f"https://zenodo.org/api/records/{RECORD_ID}", timeout=60)
    r.raise_for_status()
    rec = r.json()
    file_map = {f["key"]: f for f in rec.get("files", [])}

    manifest = {
        "zenodo_record_id": RECORD_ID,
        "zenodo_doi": rec.get("doi"),
        "drevalpy_version": "1.6.0",
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "air_gap_rule": (
            "STRICT AIR-GAP: BeatAML2, PDX_Bruna, and GDSC2 response values are never read "
            "during feature engineering, model design, or hyperparameter selection."
        ),
        "archives": {},
    }

    for fname in FILES_TO_FETCH:
        finfo = file_map[fname]
        url = finfo["links"]["self"]
        expected_size = finfo["size"]
        expected_md5 = finfo["checksum"].replace("md5:", "")
        zip_path = ZIPS_DIR / fname

        if not zip_path.exists() or zip_path.stat().st_size != expected_size:
            print(f"[Download] {fname} ({expected_size / 1e6:.1f} MB) from {url} ...", flush=True)
            t_dl = time.time()
            with requests.get(url, stream=True, timeout=300) as resp:
                resp.raise_for_status()
                with open(zip_path, "wb") as out_f:
                    for chunk in resp.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            out_f.write(chunk)
            print(f"  Downloaded {fname} in {time.time() - t_dl:.1f}s", flush=True)

        md5_hex, sha256_hex = compute_hashes(zip_path)
        assert md5_hex == expected_md5, f"MD5 mismatch for {fname}: {md5_hex} != {expected_md5}"
        print(f"  [Verified] {fname}: MD5={md5_hex} | SHA256={sha256_hex}", flush=True)

        manifest["archives"][fname] = {
            "size_bytes": expected_size,
            "zenodo_md5": expected_md5,
            "verified_md5": md5_hex,
            "sha256": sha256_hex,
            "url": url,
        }

        target_name = fname.replace(".zip", "")
        target_dir = DATA_DIR / target_name
        if not target_dir.exists():
            print(f"  [Extract] Extracting {fname} into {DATA_DIR} ...", flush=True)
            with zipfile.ZipFile(zip_path, "r") as zf:
                for member in zf.infolist():
                    if not member.filename.startswith("__MACOSX/"):
                        zf.extract(member, DATA_DIR)

    manifest_path = BASE_DIR / "manifest_sha256.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"\nSaved verified SHA-256 manifest to {manifest_path} (total time {time.time() - t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
