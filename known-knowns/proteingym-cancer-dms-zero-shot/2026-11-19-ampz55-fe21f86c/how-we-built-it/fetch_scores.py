#!/usr/bin/env python3
"""Fetch selected assay score files from the ProteinGym Zenodo zip by HTTP
range request (no 1.9 GB full download).

Provenance: Zenodo record 15293562,
https://zenodo.org/records/15293562/files/zero_shot_substitutions_scores.zip
(total 1,911,045,703 bytes). The zip holds ONE FILE PER ASSAY (217 entries,
central directory parsed from the zip tail during scouting). Each entry is
fetched as [local-header offset, offset + compressed size + 4096) and
raw-deflate decompressed; the local header is parsed for name/extra lengths
to locate the data start. One honest GET per range (User-Agent names
V3R1T4S); no retries on 4xx/5xx.
"""
import hashlib
import struct
import urllib.request
import zlib
from pathlib import Path

URL = "https://zenodo.org/records/15293562/files/zero_shot_substitutions_scores.zip"
UA = "V3R1T4S (scheduled run)"
OUT = Path(__file__).resolve().parents[3] / "data"

# name -> (local-header offset, compressed size) from the central directory
# parsed during scouting (runs/2026-11-15-0953/scout.md).
ENTRIES = {
    "PTEN_HUMAN_Matreyek_2021.csv": (1142491914, 3910103),
    "PTEN_HUMAN_Mighell_2018.csv": (1146402103, 5558497),
}


def fetch_range(start: int, end: int) -> bytes:
    req = urllib.request.Request(
        URL, headers={"User-Agent": UA, "Range": f"bytes={start}-{end}"}
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        assert r.status == 206, f"range fetch HTTP {r.status}"
        return r.read()


def fetch_entry(name: str, offset: int, csize: int) -> bytes:
    blob = fetch_range(offset, offset + csize + 4096)
    assert blob[:4] == b"PK\x03\x04", f"{name}: bad local header signature"
    (ver, flag, method, mtime, mdate, crc, cs, us, nlen, elen) = struct.unpack(
        "<HHHHHIIIHH", blob[4:30]
    )
    assert method == 8, f"{name}: method {method} is not deflate"
    assert cs == csize, f"{name}: local compressed size {cs} != central {csize}"
    data_start = 30 + nlen + elen
    raw = blob[data_start : data_start + csize]
    assert len(raw) == csize, f"{name}: short read {len(raw)} != {csize}"
    out = zlib.decompress(raw, -15)
    assert len(out) == us, f"{name}: decompressed {len(out)} != {us}"
    assert zlib.crc32(out) & 0xFFFFFFFF == crc, f"{name}: CRC mismatch"
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (offset, csize) in ENTRIES.items():
        data = fetch_entry(name, offset, csize)
        path = OUT / name
        path.write_bytes(data)
        sha = hashlib.sha256(data).hexdigest()
        print(f"{name}: {len(data)} bytes, sha256 {sha}")
        print(f"  saved to {path}")


if __name__ == "__main__":
    main()
