#!/usr/bin/env bash
set -euo pipefail
DIR="${1:?work dir}"
python3 - <<PY
import json, glob, os
from pathlib import Path
d=Path("$DIR")
rows=[]
for jl in d.glob("*.jsonl"):
    for line in jl.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
found=[r for r in rows if r.get("found")]
open_left=[]
print(f"records: {len(rows)}  found: {len(found)}")
for r in found:
    print(" FOUND", r.get("pair"), "k=", (r.get("solution") or r).get("k") if isinstance(r.get("solution"), dict) else r.get("k"))
text=[]
text.append(f"heptiamond-compat results  records={len(rows)} found={len(found)}")
for r in found:
    text.append(f"  {r.get('pair')} k={r.get('k') or (r.get('solution') or {}).get('k')}")
(Path("$DIR")/"send_back.txt").write_text("\n".join(text)+"\n")
print("wrote", Path("$DIR")/"send_back.txt")
PY
