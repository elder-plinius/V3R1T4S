#!/usr/bin/env python3
"""
INDEPENDENT cross-check for OEIS A089980 T(w,m) = number of independent
vertex sets of the grid graph P_w x P_m (w*m vertices; no two chosen
vertices orthogonally adjacent).

Method here (DELIBERATELY DIFFERENT from the main run's hs_mod.py):
  * State = a FULL column pattern: a subset of {0..w-1} naming which of the
    w cells in one column are chosen. A pattern is valid iff it has no two
    vertically-adjacent chosen cells, i.e.  s & (s<<1) == 0.
  * Column-by-column transfer: column c+1 pattern s' may follow column c
    pattern s iff  s & s' == 0  (no horizontally-adjacent chosen cells
    between the two columns).
  * Everything is EXACT Python big integers. NO modular arithmetic, NO CRT,
    NO prime reconstruction. Pure local computation.

This contrasts with a broken-profile (one-cell-at-a-time, w+1 frontier bits)
DP run under several primes + CRT: here the state is a whole column (up to
F(w+2) patterns), the DP step is a full pattern->pattern transfer, and the
counts are carried as arbitrary-precision integers throughout.

Counting convention for m columns:
  dp_1[s] = 1 for every valid pattern s        (one column: each pattern once)
  dp_{c+1}[s'] = sum_{s : s & s' == 0} dp_c[s]
  T(w, m) = sum_s dp_m[s]
Edge cases: T(0, m) = 1 (no vertices -> only the empty set);
            T(w, 0) = 1 (no columns -> only the empty set).
"""
import sys, os, time

BFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b089980.txt")
OUTDIR = os.path.dirname(os.path.abspath(__file__))


def load_bfile(path):
    vals = {}
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            i, v = line.split()
            vals[int(i)] = int(v)
    return vals


def bindex(w, m):
    """Linear b-file index of T(w,m): array read by antidiagonals d=w+m,
    position w within the diagonal (entries T(0,d),T(1,d-1),...,T(d,0))."""
    d = w + m
    return d * (d + 1) // 2 + w


def valid_patterns(w):
    """All s in [0,2^w) with no two vertically-adjacent set bits."""
    return [s for s in range(1 << w) if (s & (s << 1)) == 0]


def column_counts(w, max_m):
    """Return list T[0..max_m] of exact T(w,m) via full-pattern transfer."""
    T = [0] * (max_m + 1)
    T[0] = 1
    if max_m == 0:
        return T
    if w == 0:
        # P_0 x P_m has no vertices: exactly one independent set (empty).
        for m in range(max_m + 1):
            T[m] = 1
        return T

    pats = valid_patterns(w)
    n = len(pats)
    index_of = {s: i for i, s in enumerate(pats)}
    # Precompute, for each target pattern s' (by its list index j), the list of
    # source-pattern indices i with pats[i] & pats[j] == 0.
    compat = [[] for _ in range(n)]
    for j, sp in enumerate(pats):
        cj = compat[j]
        for i, s in enumerate(pats):
            if s & sp == 0:
                cj.append(i)

    dp = [1] * n            # dp_1
    T[1] = n                # T(w,1) = number of valid patterns
    for m in range(2, max_m + 1):
        ndp = [0] * n
        for j in range(n):
            acc = 0
            cj = compat[j]
            for i in cj:
                acc += dp[i]
            ndp[j] = acc
        dp = ndp
        T[m] = sum(dp)
    return T


# ---------------------------------------------------------------------------
# SECOND, structurally different method for small w: a broken-profile DP that
# walks the grid ONE CELL at a time with a w-bit sliding frontier, still exact
# big integers.  Different state encoding entirely (frontier of individual
# cells, not whole-column patterns) -> independent sanity check.
# ---------------------------------------------------------------------------
def brokenprofile_T(w, m):
    if w == 0 or m == 0:
        return 1
    # frontier = w bits. Process cells in column-major order: cell (r,c),
    # c outer, r inner. Bit position r of the frontier currently holds the
    # occupancy of the most recent cell in row r (either (r,c-1) before we
    # process (r,c), or (r,c) after). The cell above, (r-1,c), sits at bit r-1
    # and has already been processed this column.
    from collections import defaultdict
    dp = {0: 1}
    for c in range(m):
        for r in range(w):
            ndp = defaultdict(int)
            bit = 1 << r
            upbit = (1 << (r - 1)) if r > 0 else 0
            for state, cnt in dp.items():
                # option: leave cell (r,c) empty
                ndp[state & ~bit] += cnt
                # option: fill cell (r,c) -- needs left (old state&bit==0)
                # and up (r-1,c) empty.
                if (state & bit) == 0 and (r == 0 or (state & upbit) == 0):
                    ndp[state | bit] += cnt
            dp = ndp
    return sum(dp.values())


def main():
    t0 = time.time()
    vals = load_bfile(BFILE)
    max_published_d = max(w + m for (w, m) in [] ) if False else None
    # Largest fully published antidiagonal:
    max_idx = max(vals)
    # find largest complete diagonal d with bindex(d,0) <= max_idx fully present
    published_d = 0
    d = 0
    while True:
        start = d * (d + 1) // 2
        end = start + d
        if end <= max_idx and all((start + j) in vals for j in range(d + 1)):
            published_d = d
            d += 1
        else:
            break
    print(f"[info] largest fully-published antidiagonal d = {published_d}")

    # ---- VALIDATION: reproduce every published cell for w=1..14 ----
    checked = 0
    mismatches = 0
    mism_list = []
    WVAL = 14
    for w in range(1, WVAL + 1):
        max_m = published_d - w  # published cells have w+m <= published_d
        if max_m < 0:
            continue
        T = column_counts(w, max_m)
        for m in range(0, max_m + 1):
            idx = bindex(w, m)
            if idx in vals:
                checked += 1
                if T[m] != vals[idx]:
                    mismatches += 1
                    mism_list.append((w, m, T[m], vals[idx]))
    print(f"[validate] published cells checked (w=1..{WVAL}): {checked}")
    print(f"[validate] mismatches: {mismatches}")
    if mism_list:
        for (w, m, got, exp) in mism_list[:20]:
            print(f"   MISMATCH T({w},{m}) got {got} expected {exp}")
    if mismatches != 0:
        print("[FATAL] encoding/orientation wrong; aborting before new cells.")
        sys.exit(1)

    # ---- also cross-check column method vs broken-profile for w<=6 over
    #      all published m, plus the new antidiag cell m=79-w ----
    print("[crosscheck] column-transfer vs broken-profile, w=0..6 ...")
    cc_fail = 0
    for w in range(0, 7):
        max_m = max(published_d - w if published_d - w > 0 else 0, 79 - w)
        T = column_counts(w, max_m)
        # check a spread of m values incl. the antidiag cell
        ms = sorted(set([0, 1, 2, 3, min(5, max_m), published_d - w, 79 - w]))
        for m in ms:
            if m < 0 or m > max_m:
                continue
            bp = brokenprofile_T(w, m)
            if bp != T[m]:
                cc_fail += 1
                print(f"   CROSSCHECK FAIL T({w},{m}) col={T[m]} bp={bp}")
    print(f"[crosscheck] mismatches: {cc_fail}")
    if cc_fail != 0:
        print("[FATAL] two independent methods disagree; aborting.")
        sys.exit(1)

    # ---- NEW antidiagonal-79 cells T(w, 79-w) for w=0..16 ----
    print("[new] computing antidiagonal d=79 cells T(w,79-w), w=0..16 ...")
    rows = []
    for w in range(0, 17):
        m = 79 - w
        T = column_counts(w, m)
        val = T[m]
        rows.append((w, m, val, len(str(val))))
        print(f"   T({w},{m}) has {len(str(val))} digits; first20={str(val)[:20]}")

    outtsv = os.path.join(OUTDIR, "antidiag79_indep.tsv")
    with open(outtsv, "w") as fh:
        fh.write("w\tm\tT_w_79mw\tdigits\n")
        for (w, m, val, dig) in rows:
            fh.write(f"{w}\t{m}\t{val}\t{dig}\n")
    print(f"[new] wrote {outtsv}")
    print(f"[done] elapsed {time.time()-t0:.1f}s")

    # expose a few exact values to stdout for the parent run to compare
    for (w, m, val, dig) in rows[:3]:
        print(f"EXACT T({w},{m}) = {val}")


if __name__ == "__main__":
    main()
