#!/usr/bin/env python3
"""Standalone exhaustive verifier for the (94,13,5) covering design with 125,184 blocks.
Runs built-in positive and negative self-tests on the Fano plane C(7,3,2)=7 first, then
verifies the SHA-256 of each part object/design_94_13_5_part1.txt .. part5.txt,
reassembles the full design, and exhaustively checks all C(94,5) = 54,891,018 5-subsets of {0..93}.
Last output line is PASS or FAIL."""
import glob, hashlib, itertools, math, os, sys

EXPECTED_PART_SHA256 = {
    "object/design_94_13_5_part1.txt": "23293563435089495905a9e566a4e7967cc8ee2680d18d1c371c62dc259e0e84",
    "object/design_94_13_5_part2.txt": "dba09719caebbf3a02311053e961c7b4d322b8ca6459867078667cd7e552406a",
    "object/design_94_13_5_part3.txt": "17fa58d424b84ce7046f8afca8ac28d4fa43606850046ca0796aeac1cd3ae2de",
    "object/design_94_13_5_part4.txt": "689115faa84af43d3c2d7fc411f272b02df5f9830ec8b02e72b26fba8861dc52",
    "object/design_94_13_5_part5.txt": "0b43890442d627c987cf27f184512b0fd3288c035ca61dae22f308ab91e095fc",
}
EXPECTED_FULL_SHA256 = "e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908"

def schonheim(v, k, t):
    b = 1
    for i in range(t - 1, -1, -1):
        b = (b * (v - i) + (k - i) - 1) // (k - i)
    return b

def check_design_bytes(v, k, t, raw_bytes, require_strict_inc=True):
    lines = [l.strip() for l in raw_bytes.decode("utf-8", "replace").splitlines() if l.strip()]
    b = len(lines)
    L = schonheim(v, k, t)
    blocks = []
    for idx, line in enumerate(lines):
        toks = line.split()
        if len(toks) != k:
            return False, f"line {idx}: expected {k} ints, got {len(toks)}"
        try:
            pts = [int(x) for x in toks]
        except ValueError:
            return False, f"line {idx}: non-integer token"
        if require_strict_inc:
            for j in range(k - 1):
                if pts[j] >= pts[j + 1]:
                    return False, f"line {idx}: points not strictly increasing: {pts}"
        if min(pts) < 0 or max(pts) >= v or len(set(pts)) != k:
            return False, f"line {idx}: invalid or repeated points in 0..{v-1}: {pts}"
        blocks.append(tuple(sorted(pts)))
    distinct = len(set(blocks))
    if distinct != b:
        return False, f"duplicate blocks: distinct={distinct} != b={b}"
    if b < L:
        return False, f"b={b} < Schonheim bound L={L}"

    N = math.comb(v, t)
    try:
        import numpy as np
        A = np.array(blocks, dtype=np.int64)
        C = np.zeros((v + 1, t + 1), dtype=np.int64)
        for n in range(v + 1):
            C[n, 0] = 1
            for r in range(1, min(n, t) + 1):
                C[n, r] = C[n - 1, r - 1] + C[n - 1, r]
        pos = np.array(list(itertools.combinations(range(k), t)), dtype=np.int64)
        cov = np.zeros(N, dtype=np.uint8)
        step = 2000
        for s in range(0, b, step):
            sub = A[s:s + step][:, pos]
            rk = np.zeros(sub.shape[:2], dtype=np.int64)
            for j in range(t):
                rk += C[sub[:, :, j], j + 1]
            cov[rk.ravel()] = 1
        uncovered = int(N - int(cov.sum()))
    except ImportError:
        C = [[math.comb(n, r) for r in range(t + 1)] for n in range(v + 1)]
        pos = list(itertools.combinations(range(k), t))
        cov = bytearray(N)
        for blk in blocks:
            for p in pos:
                rk = 0
                for j in range(t):
                    rk += C[blk[p[j]]][j + 1]
                cov[rk] = 1
        uncovered = N - sum(cov)

    if uncovered != 0:
        return False, f"uncovered={uncovered} of {N}"
    return True, f"b={b} distinct={distinct} L={L} C({v},{t})={N} uncovered=0"

def main():
    # 1. Self-tests on Fano plane C(7,3,2)=7
    fano = b"0 1 3\n1 2 4\n2 3 5\n3 4 6\n0 4 5\n1 5 6\n0 2 6\n"
    ok, msg = check_design_bytes(7, 3, 2, fano)
    if not ok:
        print("SELF-TEST fano positive failed:", msg)
        print("FAIL")
        return 1
    fano_bad1 = b"0 1 3\n1 2 4\n2 3 5\n3 4 6\n0 4 5\n1 5 6\n"
    ok, _ = check_design_bytes(7, 3, 2, fano_bad1)
    if ok:
        print("SELF-TEST fano 6-block negative failed")
        print("FAIL")
        return 1
    fano_bad2 = b"0 1 3\n1 2 4\n2 3 5\n3 4 6\n0 4 5\n1 5 6\n0 2 2\n"
    ok, _ = check_design_bytes(7, 3, 2, fano_bad2)
    if ok:
        print("SELF-TEST fano repeated-point negative failed")
        print("FAIL")
        return 1
    print("self_tests: PASS (positive Fano C(7,3,2)=7 and negative controls)")

    # 2. Verify each part's individual SHA-256 and reassemble object/design_94_13_5_part1.txt .. part5.txt
    parts = sorted(glob.glob("object/design_94_13_5_part*.txt"))
    if len(parts) != 5:
        print(f"expected 5 part files in object/, found {len(parts)}")
        print("FAIL")
        return 1
    chunks = []
    for p in parts:
        b_part = open(p, "rb").read()
        sha_part = hashlib.sha256(b_part).hexdigest()
        if sha_part != EXPECTED_PART_SHA256.get(p):
            print(f"part sha256 mismatch on {p}: {sha_part}")
            print("FAIL")
            return 1
        chunks.append(b_part)
    raw = b"".join(chunks)
    sha = hashlib.sha256(raw).hexdigest()
    print(f"parts_verified=5 reassembled_bytes={len(raw)} sha256={sha}")

    ok, msg = check_design_bytes(94, 13, 5, raw, require_strict_inc=True)
    print("check_94_13_5:", msg)
    if not ok:
        print("FAIL")
        return 1
    if not msg.startswith("b=125184 "):
        print("unexpected block count")
        print("FAIL")
        return 1
    if sha != EXPECTED_FULL_SHA256:
        print("sha256 mismatch against claimed design")
        print("FAIL")
        return 1
    print("comparison: 125184 < 125236 (47+47 LJCR combining baseline, -52) < 129203 (CR 2026-10-18, -4019) < 129337 (LJCR 2026-10-18, -4153)")
    print("PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
