#!/usr/bin/env python3
"""Propagated bar for Packomania-style record tables (standard library only, Python 3.9+).

A packing table lists one best known value per N. Some cells can be beaten with no search at all:
- equal balls (radius, larger is better): deleting balls from the posted packing of any larger N' keeps its radius, so
  the honest bar for N is B(N) = max over listed N' >= N of r(N');
- sum of radii (csqv, larger is better): adding arbitrarily small circles to the packing of any smaller N' keeps its sum,
  so B(N) = max over listed N' <= N of S(N').
A cell is FREE when B(N) exceeds the row for N by at least the margin: a value between the row and B(N) beats the row but is
not a record. Values are compared exactly (fractions of the decimal strings), never as floats.

Usage:
  python3 kit/propagated_bar.py TABLE [--direction down|up] [--margin 1e-10] [--n N] [--list]
TABLE is a local file or an https:// URL of a two-column text table (N, value), for example
https://packomania.com/scu/txt/radius.txt (direction down) or https://packomania.com/csqv/txt/sumradii.txt (direction up).
"""
import argparse
import sys
import urllib.request
from fractions import Fraction


def parse_table(text):
    """Return {N: (Fraction value, original string)} from lines 'N value ...'; other lines are ignored."""
    rows = {}
    for line in text.splitlines():
        parts = line.replace(",", " ").split()
        if len(parts) < 2 or not parts[0].isdigit():
            continue
        try:
            value = Fraction(parts[1])
        except (ValueError, ZeroDivisionError):
            continue
        rows[int(parts[0])] = (value, parts[1])
    return rows


def propagated(rows, direction="down"):
    """Return {N: (bar value, N' that attains it)} for every listed N."""
    if direction not in ("down", "up"):
        raise ValueError("direction must be 'down' or 'up'")
    order = sorted(rows, reverse=(direction == "down"))
    bars, best, best_n = {}, None, None
    for n in order:
        v = rows[n][0]
        if best is None or v > best:
            best, best_n = v, n
        bars[n] = (best, best_n)
    return bars


def free_cells(rows, direction="down", margin="1e-10"):
    """Return [(N, N', gap)] for cells whose bar exceeds the row by at least margin (gap as Fraction)."""
    m = Fraction(margin)
    bars = propagated(rows, direction)
    out = []
    for n in sorted(rows):
        bar, src = bars[n]
        gap = bar - rows[n][0]
        if src != n and gap >= m:
            out.append((n, src, gap))
    return out


def read_source(src):
    if src.startswith(("https://", "http://")):
        with urllib.request.urlopen(src, timeout=60) as resp:
            return resp.read().decode("latin-1")
    with open(src, encoding="latin-1") as f:
        return f.read()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Propagated bar and free cells of a record table.")
    ap.add_argument("table")
    ap.add_argument("--direction", default="down", choices=("down", "up"),
                    help="down: larger N' can be reduced to N (equal balls); up: smaller N' can be extended (sum of radii)")
    ap.add_argument("--margin", default="1e-10", help="the margin of the target's criterion (exact decimal)")
    ap.add_argument("--n", type=int, help="report the bar for this N")
    ap.add_argument("--list", action="store_true", help="list every free cell")
    a = ap.parse_args(argv)
    rows = parse_table(read_source(a.table))
    if not rows:
        print("no rows parsed", file=sys.stderr)
        return 2
    fc = free_cells(rows, a.direction, a.margin)
    print(f"rows {len(rows)} (N {min(rows)}..{max(rows)}); free cells at margin {a.margin}: {len(fc)}")
    if a.n is not None:
        if a.n not in rows:
            print(f"N = {a.n} is not listed")
            return 2
        bar, src = propagated(rows, a.direction)[a.n]
        print(f"N = {a.n}: row {rows[a.n][1]}; bar {rows[src][1]} from N' = {src}; "
              f"{'FREE (the row is beaten by the bar)' if src != a.n and bar - rows[a.n][0] >= Fraction(a.margin) else 'not free'}")
    if a.list:
        for n, src, gap in fc:
            print(f"{n}\t{rows[n][1]}\tbar {rows[src][1]} from {src}\tgap {float(gap):.3e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
