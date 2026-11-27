"""Independently written checker for compatibility figures.
Verifies tilings, congruence, cover, connectivity, holeless, tile count.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

# ensure package root on path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from py.grid import connected, holeless, normalize, figure_ascii  # noqa: E402
from py.shapes import aspects_for, dist_sig, piece_cells  # noqa: E402


def _as_cells(obj):
    return [tuple(p) for p in obj]


def check_tiling(figure, placements, letter: str) -> list[str]:
    errs = []
    fig = set(map(tuple, figure))
    aspects = {frozenset(a) for a in aspects_for(letter)}
    target_sig = dist_sig(piece_cells(letter))
    covered = []
    for i, pl in enumerate(placements):
        cells = [tuple(p) for p in pl]
        if len(cells) != 7:
            errs.append(f"placement {i} has {len(cells)} cells")
            continue
        if not set(cells) <= fig:
            errs.append(f"placement {i} outside figure")
        norm = normalize(cells)
        if frozenset(norm) not in aspects:
            # also accept by dist_sig + connected already implied
            if dist_sig(cells) != target_sig:
                errs.append(f"placement {i} not congruent to {letter}")
        covered.extend(cells)
    if len(covered) != len(fig):
        errs.append(f"cover size {len(covered)} != figure {len(fig)}")
    if len(set(covered)) != len(covered):
        errs.append("overlapping placements")
    if set(covered) != fig:
        errs.append("placements do not exactly cover figure")
    return errs


def check_solution(sol: dict, table: str = "unrestricted") -> dict:
    errs = []
    fig = _as_cells(sol["figure"])
    if len(fig) != len(set(fig)):
        errs.append("duplicate cells in figure")
    k = sol.get("k") or (len(fig) // 7)
    if len(fig) != 7 * k:
        errs.append(f"figure area {len(fig)} != 7*{k}")
    if not connected(fig):
        errs.append("figure not connected")
    if table == "holeless" and not holeless(fig):
        errs.append("figure has holes (holeless table)")
    errs += check_tiling(fig, sol["tiling_p"], sol["letter_p"])
    errs += check_tiling(fig, sol["tiling_q"], sol["letter_q"])
    if len(sol["tiling_p"]) != k:
        errs.append(f"tiling_p has {len(sol['tiling_p'])} tiles, expected {k}")
    if len(sol["tiling_q"]) != k:
        errs.append(f"tiling_q has {len(sol['tiling_q'])} tiles, expected {k}")
    return {
        "ok": not errs,
        "errors": errs,
        "k": k,
        "ascii": figure_ascii(fig),
        "table": table,
    }


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("solution_json")
    ap.add_argument("--table", default="unrestricted", choices=["unrestricted", "holeless"])
    args = ap.parse_args()
    sol = json.loads(Path(args.solution_json).read_text())
    r = check_solution(sol, args.table)
    print(json.dumps(r, indent=2))
    sys.exit(0 if r["ok"] else 1)


if __name__ == "__main__":
    main()
