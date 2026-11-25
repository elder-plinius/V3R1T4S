"""Worker: solve a list of pairs, append JSONL results, skip done."""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from py.solve_pair import solve_pair  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True, help="JSON list of 'A-B' strings")
    ap.add_argument("--table", default="unrestricted")
    ap.add_argument("--k-min", type=int, default=2)
    ap.add_argument("--k-max", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--out", required=True, help="JSONL results path")
    ap.add_argument("--work", required=True, help="work directory")
    args = ap.parse_args()

    pairs = json.loads(Path(args.pairs).read_text())
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            if not line.strip():
                continue
            try:
                done.add(json.loads(line)["pair"])
            except Exception:
                pass

    stop = Path(args.work) / "STOP"
    with out.open("a") as f:
        for pr in pairs:
            if stop.exists():
                break
            if pr in done:
                continue
            a, b = pr.split("-")
            wd = Path(args.work) / pr
            try:
                summary = solve_pair(
                    a, b,
                    k_min=args.k_min,
                    k_max=args.k_max,
                    table=args.table,
                    work_dir=wd,
                    timeout_per_k=args.timeout,
                )
                rec = {
                    "pair": pr,
                    "table": args.table,
                    "found": summary["found"],
                    "k": (summary["solution"] or {}).get("k"),
                    "summary": str(wd / "summary.json"),
                    "checker_ok": (summary["solution"] or {}).get("checker", {}).get("ok"),
                }
            except Exception as e:
                rec = {"pair": pr, "table": args.table, "found": False, "error": str(e)}
            f.write(json.dumps(rec) + "\n")
            f.flush()
            done.add(pr)


if __name__ == "__main__":
    main()
