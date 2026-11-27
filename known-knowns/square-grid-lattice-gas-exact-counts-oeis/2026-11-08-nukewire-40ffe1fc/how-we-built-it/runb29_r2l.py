#!/usr/bin/env python
"""Run B for A210662 row 29: RIGHT-TO-LEFT ROW-SWEEP broken-profile DP.

Independently written for the row-29 arc (night 2 builds and gates it; production
sweeps run only after Run A29's worker exits, per the RAM half-free rule).

Scan: rows j = 0..rows-1 top to bottom, columns c = w-1 .. 0 (RIGHT TO LEFT).
Profile mask m over columns; at scan position (j, c):
  bit b <= c  -> cell (j,   b): 1 = occupied by a domino from (j, b+1) (scanned)
  bit b >  c  -> cell (j+1, b): 1 = occupied by a vertical domino from (j, b)
Per-cell transfer (derived here, mirror image of the left-to-right convention):
  m bit c set  -> pass:      out[m & ~(1<<c)] += v
  m bit c clear:
      monomer:               out[m & ~(1<<c)] += v
      horizontal to (j,c-1): if c > 0 and bit c-1 clear: out[m | (1<<(c-1))] += v
      vertical to (j+1,c):   if not last row:            out[m | (1<<c)]     += v
(the vertical set writes bit c in its NEXT-window meaning, cell (j+1, c); the row
boundary c=0 -> (j+1, w-1) needs no extra shift because bits keep their column).
T(rows, w) = dp[0] after the last cell (no pending dominoes past the bottom).

Prime set B29 (frozen, night-1 PREREG): first 22 proven primes > 2^61 + 103_000_000
(disjoint from set A29, which starts just above 2^61 + 3_000_000).

Modes (all gate modes print PASS/FAIL and exit accordingly):
  primes           print the 22 set-B29 primes
  gate             exact big-int dict DP vs data/b210662.txt, all cells
                   n,k <= 12 (published cell = row max(n,k), col min(n,k))
  gate-mod         first 3 B29 primes: dict DP mod p, residue == published cell
                   mod p for all cells n,k <= 12
  gate-sliced      dense two-half sliced DP == dense plain DP (mod p_B1) at
                   w = 8 and 10, j = 1..12; sliced peaks at 1.5 x 2^(w-1) x 8 B
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', '..', 'data')

B29_START = (1 << 61) + 103_000_000
N_PRIMES = 22
ROWS = 29


def is_probable_prime(n, witnesses=(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)):
    if n < 2:
        return False
    for q in witnesses:
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in witnesses:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def gen_primes(count, start_after):
    out = []
    c = start_after | 1
    while len(out) < count:
        if is_probable_prime(c):
            out.append(c)
        c += 2
    return out


def load_published():
    """b210662.txt: linear index i -> value, triangular row-major
    (i = n(n-1)/2 + k for row n, col k<=n; verified: i=3 -> T(2,2)=7,
    i=6 -> T(3,3)=131, i=8 -> T(4,2)=71). Returns {n: {k: value}}."""
    tab = {}
    for line in open(os.path.join(DATA, 'b210662.txt')):
        parts = line.split()
        if len(parts) == 2 and not line.startswith('#'):
            i, v = int(parts[0]), int(parts[1])
            n = math.isqrt(2 * i)          # n(n-1)/2 < i <= n(n+1)/2
            while n * (n + 1) // 2 < i:
                n += 1
            while n * (n - 1) // 2 >= i:
                n -= 1
            k = i - n * (n - 1) // 2
            tab.setdefault(n, {})[k] = v
    assert sum(len(r) for r in tab.values()) == 378
    assert tab[2][2] == 7 and tab[3][3] == 131 and tab[4][2] == 71
    return tab


def sweep_r2l_dict(w, rows, mod=0):
    """Exact (mod=0) or modular dict broken-profile sweep; returns T(j,w) j=1..rows."""
    dp = {0: 1}
    totals = []
    for j in range(rows):
        last = j == rows - 1
        for c in range(w - 1, -1, -1):          # RIGHT TO LEFT
            out = {}
            bit = 1 << c
            left = 1 << (c - 1) if c > 0 else 0
            for m, v in dp.items():
                if mod:
                    v %= mod
                if m & bit:
                    t = m & ~bit
                    out[t] = out.get(t, 0) + v
                else:
                    out[m] = out.get(m, 0) + v                  # monomer
                    if c > 0 and not m & left:                  # horizontal left
                        t = m | left
                        out[t] = out.get(t, 0) + v
                    if not last:                                # vertical down
                        out[m | bit] = out.get(m | bit, 0) + v
            dp = out
        totals.append(dp.get(0, 0))
    return totals


# ---------------- dense numpy forms (mod p, int64) ----------------
import numpy as np


def step_dense(dp, c, w, last, mod):
    """One cell (column c) on a dense 2^w int64 array, in place via scratch."""
    size = dp.shape[0]
    out = np.zeros(size, dtype=np.int64)
    bit = 1 << c
    sel_set = (np.arange(size, dtype=np.int64) & bit) != 0     # states with bit c set
    m_clear = np.arange(size, dtype=np.int64) & ~np.int64(bit)
    # pass: bit c set -> out[m & ~bit]
    np.add.at(out, m_clear[sel_set], dp[sel_set])
    # monomer: bit c clear -> out[m]  (bit c stays 0 == m & ~bit)
    np.add.at(out, m_clear[~sel_set], dp[~sel_set])
    if c > 0:
        left = 1 << (c - 1)
        can_h = (~sel_set) & ((np.arange(size, dtype=np.int64) & left) == 0)
        np.add.at(out, (np.arange(size) | left)[can_h], dp[can_h])
    if not last:
        np.add.at(out, (np.arange(size) | bit)[~sel_set], dp[~sel_set])
    np.remainder(out, mod, out=out)
    return out


def step_fast(dp, out, c, w, last, mod):
    """Vectorized R->L cell step, pure reshape views (no scatter, no index
    arrays): group states by bit c (reshape(-1, 2, 1<<c)).
      out[bit c = 0] = pass(g1) + monomer(g0) + horiz(g0 with bit c-1 = 0)
      out[bit c = 1] = vertical(g0), zero on the last row
    horiz sets bit c-1 inside the bit-c=0 group: reshape that group by
    bit c-1 (only when c > 0)."""
    gv = dp.reshape(-1, 2, 1 << c)
    ov = out.reshape(-1, 2, 1 << c)
    if c > 0:
        o0 = ov[:, 0, :].reshape(-1, 2, 1 << (c - 1))
        g0 = gv[:, 0, :].reshape(-1, 2, 1 << (c - 1))
        o0[:, 1, :] = g0[:, 1, :]          # monomer identity (bit c-1 = 1)
        o0[:, 1, :] += g0[:, 0, :]         # horiz: bit c-1 0 -> 1
        o0[:, 0, :] = g0[:, 0, :]          # monomer identity (bit c-1 = 0)
    else:
        ov[:, 0, :] = gv[:, 0, :]
    ov[:, 0, :] += gv[:, 1, :]             # pass
    if last:
        ov[:, 1, :] = 0
    else:
        ov[:, 1, :] = gv[:, 0, :]          # vertical
    np.remainder(out, mod, out=out)


def sweep_r2l_fast(w, rows, mod):
    """Fast dense sweep (two arrays: dp + out). Returns T(j,w) j=1..rows."""
    dp = np.zeros(1 << w, dtype=np.int64)
    dp[0] = 1
    out = np.empty_like(dp)
    totals = []
    for j in range(rows):
        last = j == rows - 1
        for c in range(w - 1, -1, -1):
            step_fast(dp, out, c, w, last, mod)
            dp, out = out, dp
        totals.append(int(dp[0]))
    return totals


def sweep_r2l_dense(w, rows, mod):
    dp = np.zeros(1 << w, dtype=np.int64)
    dp[0] = 1
    totals = []
    for j in range(rows):
        last = j == rows - 1
        for c in range(w - 1, -1, -1):
            dp = step_dense(dp, c, w, last, mod)
        totals.append(int(dp[0]))
    return totals


def step_sliced(dp, c, w, last, mod):
    """Two-half step: for c <= w-2 the halves never mix (bit w-1 untouched by
    moves at column c: they touch bits c and c-1 only); c = w-1 is the single
    cross-half case. dp is one 2^w array used as [lo | hi], half = 2^(w-1)."""
    half = 1 << (w - 1)
    if c <= w - 2:
        lo = dp[:half]
        hi = dp[half:]
        dp[:half] = step_dense(lo, c, w, last, mod)
        dp[half:] = step_dense(hi, c, w, last, mod)
        return dp
    # c == w-1: cross-half. hi index z (state z+half): pass -> lo[z].
    # lo index y: monomer -> lo[y]; horiz (bit w-2 clear) -> lo[y|2^(w-2)];
    # vertical -> hi[y].
    out_lo = np.zeros(half, dtype=np.int64)
    out_hi = np.zeros(half, dtype=np.int64)
    lo, hi = dp[:half], dp[half:]
    out_lo += hi                                     # pass (bit w-1 set)
    out_lo += lo                                     # monomer (bit w-1 clear)
    b2 = 1 << (w - 2)
    can_h = (np.arange(half) & b2) == 0
    np.add.at(out_lo, (np.arange(half) | b2)[can_h], lo[can_h])
    if not last:
        out_hi += lo                                 # vertical sets bit w-1
    np.remainder(out_lo, mod, out=out_lo)
    np.remainder(out_hi, mod, out=out_hi)
    dp[:half] = out_lo
    dp[half:] = out_hi
    return dp


def sweep_r2l_sliced(w, rows, mod):
    dp = np.zeros(1 << w, dtype=np.int64)
    dp[0] = 1
    totals = []
    for j in range(rows):
        last = j == rows - 1
        for c in range(w - 1, -1, -1):
            dp = step_sliced(dp, c, w, last, mod)
        totals.append(int(dp[0]))
    return totals


def mode_primes():
    for p in gen_primes(N_PRIMES, B29_START):
        assert 2 * (p - 1) < (1 << 63)
        print(p, flush=True)


def _cells(kmax):
    pub = load_published()
    for n in range(1, kmax + 1):
        for k in range(1, kmax + 1):
            row, col = max(n, k), min(n, k)
            if row in pub and col in pub[row]:
                yield n, k, pub[row][col]


def mode_gate():
    ok = True
    cells = list(_cells(12))
    assert len(cells) == 144, f"vacuous gate: only {len(cells)} cells"
    for n, k, want in cells:
        got = sweep_r2l_dict(k, n)[-1] if n >= 1 else 0
        # T(n,k): sweep a k-wide profile over n rows -> rows=n, width=k
        good = got == want
        if n == k or not good:            # print diagonal always, errors always
            print(f"T({n},{k}): {'OK' if good else 'FAIL'} "
                  f"[dict exact, {len(str(want))} digits]", flush=True)
        ok = ok and good
    print("GATE %s (dict exact vs b210662, all cells n,k <= 12)"
          % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def mode_gate_mod():
    primes = gen_primes(3, B29_START)
    ok = True
    ntested = 0
    for p in primes:
        for n, k, want in _cells(12):
            ntested += 1
            got = sweep_r2l_dict(k, n, mod=p)[-1] % p
            if got != want % p:
                print(f"p={p} T({n},{k}): FAIL residue", flush=True)
                ok = False
        print(f"p={p}: all n,k<=12 residues match published "
              f"({'OK' if ok else 'FAIL'}) [{ntested} cells tested]", flush=True)
    print("GATE %s (modular residues, first 3 set-B29 primes)"
          % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def mode_gate_sliced():
    p = gen_primes(1, B29_START)[0]
    ok = True
    for w in (8, 10):
        a = sweep_r2l_dense(w, 12, p)
        b = sweep_r2l_sliced(w, 12, p)
        good = a == b
        print(f"w={w}: sliced == plain (j=1..12): {'OK' if good else 'FAIL'}",
              flush=True)
        ok = ok and good
        # and the dense form itself against published cells (mod p)
        for n, k, want in _cells(w):
            if k == w and n <= 12:
                good2 = a[n - 1] == want % p
                print(f"  dense T({n},{w}) mod p == published: "
                      f"{'OK' if good2 else 'FAIL'}", flush=True)
                ok = ok and good2
    print("GATE %s (sliced-vs-plain at w=8,10 + dense vs published)"
          % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def step_sliced_fast(dp, c, w, last, mod):
    """Two-half fast step (dp = 2^w as [lo | hi], one half scratch inside):
    c <= w-2: halves are independent (moves touch bits c and c-1 only) — run
    the fast step on each half slice against a scratch half.
    c = w-1 (the single cross-half case): out_lo = pass(hi) + monomer(lo)
    + horiz(lo by bit w-2); out_hi = vertical(lo) or 0."""
    half = 1 << (w - 1)
    if c <= w - 2:
        scratch = np.empty(half, dtype=np.int64)
        lo = dp[:half]
        hi = dp[half:]
        step_fast(lo, scratch, c, w - 1, last, mod)     # width w-1: bit c < w-1
        dp[:half] = scratch
        step_fast(hi, scratch, c, w - 1, last, mod)
        dp[half:] = scratch
        return dp
    lo, hi = dp[:half], dp[half:]
    o_lo = np.empty(half, dtype=np.int64)
    o_hi = np.empty(half, dtype=np.int64)
    b2 = 1 << (w - 2)
    o_lo[:] = hi                     # pass drops bit w-1
    o_lo += lo                       # monomer (identity)
    ov = o_lo.reshape(-1, 2, b2)     # horiz: bit w-2 0 -> 1 inside lo space
    gv = lo.reshape(-1, 2, b2)
    ov[:, 1, :] += gv[:, 0, :]
    if last:
        o_hi[:] = 0
    else:
        o_hi[:] = lo                 # vertical sets bit w-1
    np.remainder(o_lo, mod, out=o_lo)
    np.remainder(o_hi, mod, out=o_hi)
    dp[:half] = o_lo
    dp[half:] = o_hi
    return dp


def sweep_r2l_sliced_fast(w, rows, mod):
    """Sliced fast sweep: dp (2^w) + scratch (2^(w-1)) + the cross-half temps
    (2x 2^(w-1)) ~ 2.5 x 2^(w-1) x 8 B peak."""
    dp = np.zeros(1 << w, dtype=np.int64)
    dp[0] = 1
    totals = []
    for j in range(rows):
        last = j == rows - 1
        for c in range(w - 1, -1, -1):
            dp = step_sliced_fast(dp, c, w, last, mod)
        totals.append(int(dp[0]))
    return totals


def mode_gate_fast():
    """Fast vectorized step vs the scatter step vs published cells, then timing."""
    import time
    p = gen_primes(1, B29_START)[0]
    ok = True
    for w in (8, 10):
        a = sweep_r2l_dense(w, 12, p)
        b = sweep_r2l_fast(w, 12, p)
        good = a == b
        print(f"w={w}: fast == scatter-dense (j=1..12): {'OK' if good else 'FAIL'}",
              flush=True)
        ok &= good
    # published cells at wider widths: residue equality for all published j
    tab = load_published()
    ntest = 0
    for w in (12, 16, 20):
        tot = sweep_r2l_fast(w, 27, p)
        for j in range(1, 28):
            row, col = max(j, w), min(j, w)
            want = tab.get(row, {}).get(col)
            if want is None:
                continue
            ntest += 1
            if tot[j - 1] != want % p:
                print(f"fast T({j},{w}) mod p != published: FAIL", flush=True)
                ok = False
    print(f"fast vs published residues at w=12,16,20 (all published j): "
          f"{ntest} cells {'OK' if ok else 'FAIL'}", flush=True)
    t0 = time.time()
    tot = sweep_r2l_fast(24, 29, p)
    dt = time.time() - t0
    print(f"timing: w=24 full 29-row sweep {dt:.1f}s "
          f"(projected k=1..26 per prime ~{dt/24*55/60:.1f} min)", flush=True)
    for w in (8, 10, 12):
        a = sweep_r2l_fast(w, 12, p)
        b = sweep_r2l_sliced_fast(w, 12, p)
        good = a == b
        print(f"w={w}: sliced-fast == fast (j=1..12): "
              f"{'OK' if good else 'FAIL'}", flush=True)
        ok &= good
    if free_gb() > 4.0:               # big probe only with headroom
        t0 = time.time()
        tot = sweep_r2l_sliced_fast(26, 29, p)
        a26 = sweep_r2l_fast(26, 29, p)
        print(f"w=26 sliced-fast == fast: {'OK' if tot == a26 else 'FAIL'} "
              f"({time.time()-t0:.1f}s)", flush=True)
        ok &= tot == a26
    else:
        print("w=26 probe deferred: free RAM below 4 GiB "
              "(algebra already gated at w=8,10,12)", flush=True)
    print("GATE %s (fast step)" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def free_gb():
    import ctypes
    import ctypes.wintypes as wint
    class M(ctypes.Structure):
        _fields_ = [("dwLength", wint.DWORD), ("dwMemoryLoad", wint.DWORD),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
    m = M()
    m.dwLength = ctypes.sizeof(M)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.ullAvailPhys / 2**30


def mode_work(resfile, deadline, kmax=26):
    """Checkpointed production: per prime p (set B29), per k=1..kmax, sweep the
    R->L fast DP over 29 rows, append residues + stamp. Skips anything whose
    2-array peak exceeds half of free RAM; resumes from the checkpoint file."""
    import datetime as dt
    dl = dt.datetime.strptime(deadline, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=dt.timezone.utc)
    primes = gen_primes(N_PRIMES, B29_START)
    budget = free_gb() / 2.0
    done = set()
    try:
        for line in open(resfile, encoding='utf-8'):
            if line.startswith('p='):
                f = dict(t.split('=') for t in line.split())
                done.add((f['p'], f['k']))
    except FileNotFoundError:
        pass
    import time
    with open(resfile, 'a', encoding='utf-8', newline='\n') as out:
        for p in primes:
            for k in range(1, kmax + 1):
                if (str(p), str(k)) in done:
                    continue
                peak = 2 * (1 << k) * 8 / 2**30
                if peak > budget:
                    sliced_peak = 2.5 * (1 << (k - 1)) * 8 / 2**30
                    if k >= 2 and sliced_peak <= budget:
                        t0 = time.time()
                        tot = sweep_r2l_sliced_fast(k, ROWS, p)
                        mode = 'sliced-fast'
                        stamp = dt.datetime.now(dt.timezone.utc).strftime(
                            '%Y-%m-%dT%H:%M:%SZ')
                        for j in range(1, ROWS + 1):
                            out.write(f"p={p} k={k} j={j} r={int(tot[j-1])}\n")
                        out.write(f"# stamp={stamp} p={p} k={k} mode={mode} "
                                  f"secs={time.time()-t0:.0f}\n")
                        out.flush()
                        if dt.datetime.now(dt.timezone.utc) > dl:
                            out.write(f"# soft deadline {deadline} reached, "
                                      f"stopping cleanly\n")
                            return 0
                        continue
                    out.write(f"# k={k} skipped: fast-mono peak {peak:.2f} GB "
                              f"> half-free budget {budget:.2f} GB "
                              f"(sliced {sliced_peak:.2f} GB also over)\n")
                    out.flush()
                    continue
                t0 = time.time()
                tot = sweep_r2l_fast(k, ROWS, p)
                stamp = dt.datetime.now(dt.timezone.utc).strftime(
                    '%Y-%m-%dT%H:%M:%SZ')
                for j in range(1, ROWS + 1):
                    out.write(f"p={p} k={k} j={j} r={int(tot[j-1])}\n")
                out.write(f"# stamp={stamp} p={p} k={k} mode=fast "
                          f"secs={time.time()-t0:.0f}\n")
                out.flush()
                if dt.datetime.now(dt.timezone.utc) > dl:
                    out.write(f"# soft deadline {deadline} reached, "
                              f"stopping cleanly\n")
                    return 0
    print("ALL DONE", flush=True)
    return 0


if __name__ == "__main__":
    m = sys.argv[1]
    if m == "primes":
        mode_primes()
        sys.exit(0)
    if m == "gate":
        sys.exit(mode_gate())
    if m == "gate-mod":
        sys.exit(mode_gate_mod())
    if m == "gate-sliced":
        sys.exit(mode_gate_sliced())
    if m == "gate-fast":
        sys.exit(mode_gate_fast())
    if m == "work":
        kmax = int(sys.argv[4]) if len(sys.argv) > 4 else 26
        sys.exit(mode_work(sys.argv[2], sys.argv[3], kmax))
    sys.exit(2)
