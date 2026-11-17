#!/usr/bin/env python3
"""Download the La Jolla Covering Repository ingredient designs used by the builder.

Source: Daniel M. Gordon, "La Jolla Covering Repository", Zenodo record 19735294 (version 1.2, 2026-04-24),
https://doi.org/10.5281/zenodo.19735294 , file covers.json (4,191,522,340 bytes, md5 bb59d977afd6724b32dcc187f68a229c),
CC-BY-4.0. That file is a frozen, versioned snapshot, so each ingredient is fetched with one HTTP Range request
for the exact byte span of its "C(v,k,t)" entry; nothing else is downloaded.

Each entry is written to how-we-built-it/ingredients/C_<v>_<k>_<t>.txt (one block per line, 1-based points,
space separated, in the repository's order) and checked against the sha256 listed in INGREDIENTS.tsv
(next to this script) before the builder may use it.

Usage:
  python3 how-we-built-it/fetch_ingredients.py
"""
import csv
import hashlib
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://zenodo.org/api/records/19735294/files/covers.json/content"


def main():
    out_dir = os.path.join(HERE, "ingredients")
    os.makedirs(out_dir, exist_ok=True)
    ok = True
    with open(os.path.join(HERE, "INGREDIENTS.tsv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    for row in rows:
        start, end = int(row["byte_start"]), int(row["byte_end"])
        req = urllib.request.Request(URL, headers={"Range": f"bytes={start}-{end - 1}"})
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
        if len(raw) != end - start:
            sys.exit(f"{row['entry']}: expected {end - start} bytes, got {len(raw)}")
        text = raw.decode("utf-8").strip().rstrip(",")
        key, _, body = text.partition(":")
        if key.strip() != f'"{row["entry"]}"':
            sys.exit(f"{row['entry']}: byte range starts with {key!r}")
        blocks = json.loads(body)
        data = "".join(" ".join(str(x) for x in b) + "\n" for b in blocks).encode()
        digest = hashlib.sha256(data).hexdigest()
        path = os.path.join(out_dir, row["file"])
        with open(path, "wb") as g:
            g.write(data)
        good = digest == row["sha256"] and len(blocks) == int(row["blocks"])
        ok &= good
        print(f"{row['entry']:>12} blocks={len(blocks):>5} sha256={digest} {'OK' if good else 'MISMATCH'} -> ingredients/{row['file']}")
    if not ok:
        sys.exit("FAIL: at least one ingredient does not match INGREDIENTS.tsv")
    print("PASS")


if __name__ == "__main__":
    main()
