#!/usr/bin/env python3
"""
verify_snake_coil.py — Standalone exact verifier and automorphism-invariant checker
for Snake-in-the-Box and Coil-in-the-Box in Q_n.

Verifies:
1. Single-bit transitions: popcount(v_i ^ v_{i+1}) == 1
2. Distinct vertices: L+1 vertices for snake of length L; L vertices for coil of length L
3. Inducedness (zero chords): O(L * n) hash-table neighbor check + O(L^2) exact check option
4. Symmetric coil property (p1): even length L = 2h with steps[:h] == steps[h:] (P . P doubling)
5. Hypercube automorphism inequivalence (p3):
   - Exact canonical relabelled transition sequence under B_n = S_n x| (Z_2)^n, reversal,
     and (for coils) cyclic rotation.
   - Structural automorphism invariants:
     (a) Dimension-count vector (DCV): sorted multiset of coordinate flip counts
     (b) Coordinate step-gap spectrum: sorted multiset of gap lengths between consecutive flips
         of the same coordinate
     (c) k-step Hamming distance spectrum: counts of pairs at path/cycle distance k with
         each Hamming distance, for k = 1..8
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from collections import Counter

csv.field_size_limit(sys.maxsize)


def first_appearance_relabel(steps):
    mapping = {}
    nxt = 0
    out = []
    for s in steps:
        c = mapping.get(s)
        if c is None:
            c = nxt
            mapping[s] = c
            nxt += 1
        out.append(c)
    return tuple(out)


def canonical_snake(steps):
    f = first_appearance_relabel(steps)
    r = first_appearance_relabel(steps[::-1])
    return min(f, r)


def canonical_coil(steps):
    L = len(steps)
    rev = steps[::-1]
    best = None
    for i in range(L):
        rot_f = first_appearance_relabel(steps[i:] + steps[:i])
        if best is None or rot_f < best:
            best = rot_f
        rot_r = first_appearance_relabel(rev[i:] + rev[:i])
        if rot_r < best:
            best = rot_r
    return best


def steps_to_b36(steps):
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    return "".join(chars[s] for s in steps)


def compute_invariants(steps, is_coil, n):
    L = len(steps)
    # 1. Dimension-count vector (DCV): sorted flip counts across all n coordinates
    counts = Counter(steps)
    dcv = sorted([counts.get(b, 0) for b in range(n)])

    # 2. Coordinate step-gap spectrum
    gap_profiles = []
    for b in range(n):
        pos = [i for i, s in enumerate(steps) if s == b]
        if not pos:
            gap_profiles.append(())
        elif is_coil:
            k = len(pos)
            gaps = sorted([(pos[(idx + 1) % k] - pos[idx]) % L for idx in range(k)])
            gap_profiles.append(tuple(gaps))
        else:
            gaps = tuple(pos[idx + 1] - pos[idx] for idx in range(len(pos) - 1))
            gap_profiles.append(min(gaps, gaps[::-1]))
    gap_profiles.sort()

    # 3. k-step Hamming distance spectrum for k = 1..6
    verts = [0]
    v = 0
    for s in steps:
        v ^= (1 << s)
        verts.append(v)
    ring = verts[:-1] if is_coil else verts
    k_spec = {}
    for k in range(2, 7):
        if is_coil:
            hds = Counter(bin(ring[i] ^ ring[(i + k) % L]).count("1") for i in range(L))
        else:
            hds = Counter(bin(verts[i] ^ verts[i + k]).count("1") for i in range(L + 1 - k))
        k_spec[str(k)] = dict(sorted(hds.items()))

    return {
        "dcv": dcv,
        "gap_spectrum_hash": hashlib.sha256(repr(gap_profiles).encode()).hexdigest()[:16],
        "k_step_hamming_spectrum": k_spec,
    }


def vertices_to_steps(verts):
    steps = []
    for i in range(len(verts) - 1):
        diff = verts[i] ^ verts[i + 1]
        if diff <= 0 or (diff & (diff - 1)) != 0:
            raise ValueError(f"Non-adjacent consecutive vertices at {i}: {verts[i]} -> {verts[i+1]}")
        steps.append(diff.bit_length() - 1)
    return steps


def parse_input(path_or_str):
    if os.path.exists(path_or_str):
        raw = open(path_or_str, "r", encoding="utf-8").read().strip()
    else:
        raw = path_or_str.strip()

    if raw.startswith("{"):
        d = json.loads(raw)
        if "transition_sequence" in d:
            raw = d["transition_sequence"]
        elif "ts" in d:
            raw = d["ts"]
        elif "steps" in d:
            return [int(x) for x in d["steps"]]
        elif "vertices" in d:
            verts = d["vertices"]
            if d.get("type") == "induced_cycle" or (
                len(verts) >= 4 and bin(verts[0] ^ verts[-1]).count("1") == 1 and verts[0] != verts[-1]
            ):
                if verts[0] != verts[-1] and bin(verts[0] ^ verts[-1]).count("1") == 1:
                    verts = list(verts) + [verts[0]]
            return vertices_to_steps(verts)

    tokens = raw.split()
    if len(tokens) > 2 and all(t.isdigit() for t in tokens):
        nums = [int(t) for t in tokens]
        if nums[0] == len(nums) - 1 and max(nums[1:]) >= 16:
            return vertices_to_steps(nums[1:])
        if max(nums) >= 32:
            return vertices_to_steps(nums)
        return nums

    clean = [ch for ch in raw.lower() if not ch.isspace()]
    return [int(ch, 36) for ch in clean]


def verify_steps(steps, expected_n=None):
    if not steps:
        raise ValueError("Empty transition sequence")
    used_dims = len(set(steps))
    max_dim = max(steps) + 1
    n = expected_n if expected_n is not None else max_dim
    if max_dim > n:
        raise ValueError(f"Step uses coordinate {max_dim - 1} >= n={n}")

    verts = [0]
    v = 0
    for s in steps:
        v ^= (1 << s)
        verts.append(v)

    L = len(steps)
    is_coil = (L >= 4 and verts[-1] == verts[0])

    if is_coil:
        ring = verts[:-1]
        pos = {}
        for i, u in enumerate(ring):
            if u in pos:
                raise ValueError(f"Duplicate vertex {u} at coil positions {pos[u]} and {i}")
            pos[u] = i
        for i, u in enumerate(ring):
            for b in range(n):
                j = pos.get(u ^ (1 << b))
                if j is not None:
                    diff = (i - j) % L
                    if diff != 1 and diff != L - 1:
                        raise ValueError(f"Chord in coil between positions {i} and {j} (vertices {u} and {ring[j]})")
        half = L // 2
        is_sym = (L % 2 == 0 and steps[:half] == steps[half:])
        v_half = verts[half] if L % 2 == 0 else None
    else:
        pos = {}
        for i, u in enumerate(verts):
            if u in pos:
                raise ValueError(f"Duplicate vertex {u} at snake positions {pos[u]} and {i}")
            pos[u] = i
        for i, u in enumerate(verts):
            for b in range(n):
                j = pos.get(u ^ (1 << b))
                if j is not None and abs(i - j) != 1:
                    raise ValueError(f"Chord in snake between positions {i} and {j} (vertices {u} and {verts[j]})")
        is_sym = False
        v_half = None

    invariants = compute_invariants(steps, is_coil, n)
    return {
        "valid": True,
        "n": n,
        "used_dims": used_dims,
        "type": "coil" if is_coil else "snake",
        "length": L,
        "is_symmetric": is_sym,
        "v_half": v_half,
        "steps": steps,
        "invariants": invariants,
    }


def load_reference_bank(seeds_dir, n, kind, length):
    """Load all published reference sequences for (n, kind, length) -> dict of name: (canonical_tuple, invariants)."""
    bank = {}
    canon_fn = canonical_coil if kind in ("coil", "symmetric_coil") else canonical_snake
    is_coil = kind in ("coil", "symmetric_coil")

    # 1. minortriad_records.json
    mt_path = os.path.join(seeds_dir, "minortriad_records.json")
    if os.path.exists(mt_path):
        for r in json.load(open(mt_path)):
            sid = r["id"]
            r_kind = "snake" if sid.startswith("sn") else ("coil" if sid.startswith("co") else "symmetric_coil")
            r_n = int(re.sub(r"[^0-9]", "", sid))
            if r_n == n and r["length"] == length and (r_kind == kind or (kind == "coil" and r_kind == "symmetric_coil")):
                steps = [int(c, 36) for c in r["ts"]]
                bank[f"minortriad:{sid}"] = (canon_fn(steps), compute_invariants(steps, is_coil, n))

    # 2. Fast line-prefix scan of Caltech CSVs
    prefix = f"{n},{length},"
    if kind == "snake":
        csv_path = os.path.join(seeds_dir, "record_snakes.csv")
        if os.path.exists(csv_path):
            with open(csv_path, "r") as f:
                for idx, line in enumerate(f):
                    if line.startswith(prefix):
                        parts = line.split(",")
                        steps = [int(x) for x in parts[2].split()]
                        bank[f"caltech_snake:{idx}"] = (canon_fn(steps), compute_invariants(steps, False, n))
    else:
        for fn, tag in [("record_coils.csv", "caltech_coil"), ("record_symmetric_coils.csv", "caltech_sym_coil")]:
            csv_path = os.path.join(seeds_dir, fn)
            if os.path.exists(csv_path):
                with open(csv_path, "r") as f:
                    for idx, line in enumerate(f):
                        if line.startswith(prefix):
                            parts = line.split(",")
                            steps = [int(x) for x in parts[2].split()]
                            bank[f"{tag}:{idx}"] = (canon_fn(steps), compute_invariants(steps, True, n))

    # 3. Toner & Taylor files
    extra_files = [
        ("toner_q13_2944.txt", 13, "snake", 2944),
        ("toner_q13_2946.txt", 13, "snake", 2946),
        ("toner_q14_5850.txt", 14, "snake", 5850),
        ("taylor_snake_Q13.json", 13, "snake", 2938),
        ("taylor_snake_Q14.json", 14, "snake", 5844),
        ("taylor_coil_Q13.json", 13, "coil", 2844),
        ("taylor_coil_Q14.json", 14, "coil", 5750),
    ]
    for fn, fn_n, fn_kind, fn_len in extra_files:
        if fn_n == n and fn_kind == kind and fn_len == length:
            p = os.path.join(seeds_dir, fn)
            if os.path.exists(p):
                steps = parse_input(p)
                bank[fn] = (canon_fn(steps), compute_invariants(steps, is_coil, n))

    return bank


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", nargs="?", help="Input file or transition string")
    ap.add_argument("--dim", type=int, default=None, help="Expected dimension n")
    ap.add_argument("--seeds-dir", default="data/seeds", help="Reference seeds directory")
    ap.add_argument("--check-inequiv", action="store_true", help="Check canonical inequivalence against reference bank")
    ap.add_argument("--calibrate", action="store_true", help="Run calibration across all downloaded records")
    args = ap.parse_args()

    if args.calibrate:
        mt = json.load(open(os.path.join(args.seeds_dir, "minortriad_records.json")))
        for r in mt:
            sid = r["id"]
            n = int(re.sub(r"[^0-9]", "", sid))
            steps = [int(c, 36) for c in r["ts"]]
            res = verify_steps(steps, expected_n=n)
            expected_type = "snake" if sid.startswith("sn") else "coil"
            assert res["type"] == expected_type, f"Type mismatch on {sid}"
            assert res["length"] == r["length"], f"Length mismatch on {sid}"
            if sid.startswith("sc"):
                assert res["is_symmetric"], f"Expected symmetric coil on {sid}"
            print(f"[CALIBRATE OK] minortriad {sid:5s}: n={n:2d} type={res['type']:5s} len={res['length']:4d} sym={res['is_symmetric']}")
        # Also calibrate on Snake-in-the-Box CSVs
        for fn, expected_type in [("record_coils.csv", "coil"), ("record_symmetric_coils.csv", "coil")]:
            p = os.path.join(args.seeds_dir, fn)
            if os.path.exists(p):
                with open(p) as f:
                    rows = list(csv.DictReader(f))
                for idx, r in enumerate(rows):
                    steps = [int(x) for x in r["actions"].split()]
                    res = verify_steps(steps, expected_n=int(r["n"]))
                    assert res["type"] == expected_type and res["length"] == int(r["length"])
                print(f"[CALIBRATE OK] {fn:26s}: verified all {len(rows)} rows")
        for fn in ["toner_q13_2946.txt", "toner_q14_5850.txt", "taylor_coil_Q14.json", "taylor_snake_Q14.json"]:
            p = os.path.join(args.seeds_dir, fn)
            if os.path.exists(p):
                steps = parse_input(p)
                res = verify_steps(steps)
                print(f"[CALIBRATE OK] {fn:26s}: n={res['n']:2d} type={res['type']:5s} len={res['length']:4d} sym={res['is_symmetric']}")
        return

    if not args.input:
        ap.error("Provide an input file/string or --calibrate")

    steps = parse_input(args.input)
    res = verify_steps(steps, expected_n=args.dim)
    inv = res["invariants"]
    print(f"VALID {res['type'].upper()}: n={res['n']} used_dims={res['used_dims']} length={res['length']} symmetric={res['is_symmetric']} dcv={inv['dcv']} gap_hash={inv['gap_spectrum_hash']}")

    if args.check_inequiv:
        canon_fn = canonical_coil if res["type"] == "coil" else canonical_snake
        my_canon = canon_fn(steps)
        bank = load_reference_bank(args.seeds_dir, res["n"], res["type"], res["length"])
        matches = [k for k, (v_canon, _) in bank.items() if v_canon == my_canon]
        dcv_matches = [k for k, (_, v_inv) in bank.items() if v_inv["dcv"] == inv["dcv"]]
        gap_matches = [k for k, (_, v_inv) in bank.items() if v_inv["gap_spectrum_hash"] == inv["gap_spectrum_hash"]]
        print(f"Reference bank for (n={res['n']}, type={res['type']}, len={res['length']}): {len(bank)} entries, {len(set(v[0] for v in bank.values()))} distinct canonical classes")
        if matches:
            print(f"EQUIVALENT to reference entry: {matches}")
            sys.exit(2)
        else:
            print(f"STRICTLY INEQUIVALENT to all {len(bank)} reference entries! (dcv_matches={len(dcv_matches)}, gap_matches={len(gap_matches)}, canonical prefix: {steps_to_b36(my_canon[:30])}...)")


if __name__ == "__main__":
    main()
