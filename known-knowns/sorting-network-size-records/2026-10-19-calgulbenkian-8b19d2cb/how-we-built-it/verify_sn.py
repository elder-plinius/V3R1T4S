#!/usr/bin/env python3
"""
Standalone Exhaustive Verifier for Sorting Network Pareto Records (`verify_sn.py`).

Checks:
1. Valid comparator format and orientation (`0 <= i < j < n`).
2. Independent computation of comparator count (`size`) and greedy ASAP layer `depth`.
3. Sanity checks against proven mathematical lower bounds on size and depth.
4. Exhaustive 0-1 Principle verification over all 2^n binary inputs via `./sn_check`
   (exact cluster-merging / prefix output-set propagation, identical to Bert Dobbelaere's
   official verifier `nw_tool.py`).
5. Strict Pareto non-domination against all `(s', d')` pairs listed for `n` in
   `data/sorting_networks_extended.html`.
"""
import os
import re
import sys
import glob
import json
import subprocess

PROVEN_MIN_SIZE = {
    1: 0, 2: 1, 3: 3, 4: 5, 5: 9, 6: 12,
    7: 16, 8: 19, 9: 25, 10: 29, 11: 35, 12: 39
}

def proven_min_depth(n):
    if n <= 1: return 0
    if n == 2: return 1
    if n <= 4: return 3
    if n <= 8: return 6
    if n <= 10: return 7
    if n <= 12: return 8
    if n <= 16: return 9
    return 10

def parse_html_pareto_table(html_path="data/sorting_networks_extended.html"):
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # Extract all network links of the form N<n>L<size>D<depth>
    frontier = {}
    for m in re.finditer(r"N(\d+)L(\d+)D(\d+)", html):
        n, s, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if (s, d) not in frontier.setdefault(n, []):
            frontier[n].append((s, d))
    for n in frontier:
        frontier[n].sort()
    return frontier

def load_network_file(path):
    comparators = []
    n_hdr = None
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
    if not lines:
        raise ValueError(f"Empty file: {path}")
    first_parts = lines[0].split()
    start_idx = 0
    if len(first_parts) == 2 and len(lines) == int(first_parts[1]) + 1:
        n_hdr = int(first_parts[0])
        start_idx = 1
    for idx, line in enumerate(lines[start_idx:], start=start_idx + 1):
        parts = line.replace(",", " ").split()
        if len(parts) < 2:
            raise ValueError(f"{path}:{idx}: invalid comparator line '{line}'")
        i, j = int(parts[0]), int(parts[1])
        comparators.append((i, j))
    if n_hdr is None:
        n_hdr = max(max(i, j) for i, j in comparators) + 1
    return n_hdr, comparators

def compute_greedy_asap_depth(n, comparators):
    wire_layer = [0] * n
    for i, j in comparators:
        if not (0 <= i < j < n):
            raise ValueError(f"Invalid comparator ({i}, {j}) for n={n}: must satisfy 0 <= i < j < n")
        layer = max(wire_layer[i], wire_layer[j]) + 1
        wire_layer[i] = layer
        wire_layer[j] = layer
    return max(wire_layer) if wire_layer else 0

def verify_file(path, frontier):
    n, comparators = load_network_file(path)
    size = len(comparators)
    depth = compute_greedy_asap_depth(n, comparators)

    # Proven lower bound sanity checks
    if n in PROVEN_MIN_SIZE and size < PROVEN_MIN_SIZE[n]:
        return False, f"REJECT: n={n} size={size} < proven lower bound {PROVEN_MIN_SIZE[n]}"
    min_d = proven_min_depth(n)
    if depth < min_d:
        return False, f"REJECT: n={n} depth={depth} < proven lower bound {min_d}"

    # Exhaustive 0-1 verification via ./sn_check
    proc = subprocess.run(["./sn_check", path], capture_output=True, text=True, timeout=120)
    out = proc.stdout.strip()
    if proc.returncode != 0 or "valid=1" not in out:
        return False, f"FAIL 0-1 verification: {out} {proc.stderr.strip()}"

    # Check against HTML Pareto frontier
    listed = frontier.get(n, [])
    dominated_by = [(s, d) for (s, d) in listed if s <= size and d <= depth]
    strictly_dominates = [(s, d) for (s, d) in listed if size <= s and depth <= d and (size < s or depth < d)]

    tier = "FULL_WIN" if 13 <= n <= 32 else ("PARTIAL_WIN_P1" if 33 <= n <= 64 else "OTHER")
    if dominated_by:
        return False, f"DOMINATED: n={n} ({size}, {depth}) dominated by listed {dominated_by}"

    return True, {
        "file": path,
        "n": n,
        "size": size,
        "depth": depth,
        "tier": tier,
        "listed_frontier": listed,
        "strictly_dominates": strictly_dominates,
        "sn_check_output": out,
    }

def main():
    frontier = parse_html_pareto_table()
    paths = sys.argv[1:] if len(sys.argv) > 1 else sorted(glob.glob("results/*.txt"))
    all_ok = True
    for p in paths:
        ok, info = verify_file(p, frontier)
        if ok:
            print(f"[PASS - {info['tier']}] {p}: n={info['n']}, size={info['size']}, depth={info['depth']}")
            print(f"  0-1 Exhaustive Check : {info['sn_check_output']}")
            print(f"  Listed Frontier (n={info['n']}): {info['listed_frontier']}")
            print(f"  Strictly Dominates   : {info['strictly_dominates']}")
        else:
            print(f"[FAIL] {p}: {info}")
            all_ok = False
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
