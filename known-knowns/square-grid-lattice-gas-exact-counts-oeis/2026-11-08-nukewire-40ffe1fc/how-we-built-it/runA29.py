#!/usr/bin/env python
"""Run A for A210662 row 29: LEFT-TO-RIGHT ROW-SWEEP broken-profile DP.

Per k = 1..28, a 29-step sweep with a k-bit frontier records T(j,k) mod p for
j = 1..29 (the frontier empties at each row boundary). Memory under the
half-free rule: k <= K_MONO runs the monolithic form (dp + new, peak
2 x 2^k x 8 B); k > K_MONO runs the two-half in-place sliced form (dp + one
half-scratch; the two cross-half steps at inner index i = k-2 and i = k-1 are
the same ordered-phase cases derived and gated in the row-28 Run B work —
see runs/2026-11-02-0831). A start-time RAM guard picks the layout and refuses
anything that would exceed the budget.

Prime set A29 (frozen in PREREG): first 22 proven primes > 2^61 + 3_000_000.
Deterministic Miller-Rabin, bases 2..37 (valid < 3.3e24); 2(p-1) < 2^63.

Modes:
  gate            exact big-int n = 1..12 vs data/b028420.txt (diagonal)
  gate-sliced     sliced path at small widths, exact, same diagonal
  primes          the 22 set-A29 primes
  work <resfile> <deadline_UTC> [kmax]   checkpointed loop k = 1..kmax
"""
import datetime as dt
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
ROWS = 29
K_MONO = 26
MOD = [0]


def is_probable_prime(n, witnesses=(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)):
    if n < 2:
        return False
    for p in witnesses:
        if n % p == 0:
            return n == p
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


def step_inplace(old, new, i, w, last, base_only=False):
    """One inner step on RAM slices: new = transfer(old) at bit i. Blocks never
    straddle the slice when the slice is a multiple of 2^(i+2) (see docstring).
    Sums are at most 2(p-1) + the single domino add -> reduced immediately."""
    v = old.reshape(-1, 2, 1 << i)
    bs = v[:, 1, :]
    bc = v[:, 0, :]
    nv = new.reshape(-1, 2, 1 << i)
    nv[:, 0, :] = bs
    nv[:, 0, :] += bc
    if last:
        nv[:, 1, :] = 0
    else:
        nv[:, 1, :] = bc
    if i < w - 1 and not base_only:
        nw = nv.reshape(-1, 2, 2, 1 << i)
        sw = bc.reshape(-1, 2, 1 << i)
        nw[:, 1, 0, :] += sw[:, 0, :]
    if MOD[0]:
        np.remainder(new, MOD[0], out=new)


def run_dp_ram(width, rows, dtype, mod):
    """Monolithic sweep; returns list of dp[0] after each row (T(j+1,width))."""
    size = 1 << width
    dp = np.zeros(size, dtype=dtype)
    dp[0] = 1
    totals = []
    for j in range(rows):
        last = j == rows - 1
        for i in range(width):
            new = np.empty_like(dp)
            MOD[0] = mod
            step_inplace(dp, new, i, width, last)
            dp = new
        totals.append(dp[0])
    return totals


def run_dp_sliced(width, rows, mod):
    """Two-half in-place sweep: dp = 2^width int64 + one half scratch.
    Cases by inner step i (w = width): i <= w-3 plain halves; i = w-2 the
    domino add new[half:half+q] += old[0:q] (q = 2^(w-2)) in three ordered
    phases; i = w-1 the base pass new_lo = old_lo + old_hi,
    new_hi = last ? 0 : old_lo via scratch. Validated by gate-sliced."""
    size = 1 << width
    half = size // 2
    dp = np.zeros(size, dtype=np.int64)
    dp[0] = 1
    scratch = np.empty(half, dtype=np.int64)
    totals = []
    for j in range(rows):
        last = j == rows - 1
        for i in range(width):
            MOD[0] = mod
            if i <= width - 3:
                _half_hi(dp, scratch, half, i, width, last)
                _half_lo(dp, scratch, half, i, width, last)
            elif i == width - 2:
                _half_hi(dp, scratch, half, i, width, last, base_only=True)
                q = half // 2
                dp[half:half + q] += dp[0:q]
                if mod:
                    np.remainder(dp[half:half + q], mod, out=dp[half:half + q])
                _half_lo(dp, scratch, half, i, width, last, base_only=True)
            else:
                scratch[:] = dp[half:half + half]
                scratch += dp[0:half]
                if mod:
                    np.remainder(scratch, mod, out=scratch)
                if last:
                    dp[half:half + half] = 0
                else:
                    dp[half:half + half] = dp[0:half]
                dp[0:half] = scratch
        totals.append(int(dp[0]))
    return totals


def _half_hi(dp, scratch, half, i, w, last, base_only=False):
    sl = dp[half:half + half]
    step_inplace(sl, scratch[:len(sl)], i, w, last, base_only)
    dp[half:half + half] = scratch[:len(sl)]


def _half_lo(dp, scratch, half, i, w, last, base_only=False):
    sl = dp[0:half]
    step_inplace(sl, scratch[:len(sl)], i, w, last, base_only)
    dp[0:half] = scratch[:len(sl)]


def free_gb():
    import ctypes
    import ctypes.wintypes as w
    class M(ctypes.Structure):
        _fields_ = [("dwLength", w.DWORD), ("dwMemoryLoad", w.DWORD),
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


def mode_gate(sliced):
    pub = {}
    for line in open(os.path.join(DATA, 'b028420.txt')):
        parts = line.split()
        if len(parts) == 2 and not line.startswith('#'):
            pub[int(parts[0])] = int(parts[1])
    ok = True
    for n in range(1, 13):
        if not sliced:
            tot = run_dp_ram(n, n, object, 0)
            good = int(tot[-1]) == pub.get(n)
            label = 'plain exact'
        else:
            # exact where the value fits int64 (n <= 8), else mod-vs-plain
            pf = 2305843009214694311
            if pub.get(n, 0) < (1 << 62):
                tot = run_dp_sliced(n, n, 0)
                good = int(tot[-1]) == pub.get(n)
                label = 'sliced exact'
            else:
                a = run_dp_sliced(n, n, pf)
                b = run_dp_ram(n, n, np.int64, pf)
                good = int(a[-1]) == int(b[-1])
                label = 'sliced mod == plain mod'
        print(f"n={n}: {'OK' if good else 'FAIL'} [{label}]", flush=True)
        ok = ok and good
    print("GATE %s (n=1..12 vs A028420 diagonal, %s)"
          % ("PASS" if ok else "FAIL", "sliced" if sliced else "plain"))
    return 0 if ok else 1


def mode_primes():
    for p in gen_primes(22, (1 << 61) + 3_000_000):
        assert 2 * (p - 1) < (1 << 63)
        print(p, flush=True)


def mode_work(resfile, deadline, kmax=28):
    dl = dt.datetime.strptime(deadline, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    primes = gen_primes(22, (1 << 61) + 3_000_000)
    budget = free_gb() / 2.0
    done = set()
    try:
        for line in open(resfile, encoding='utf-8'):
            if line.startswith('p='):
                f = dict(t.split('=') for t in line.split())
                done.add((f['p'], f['k']))
    except FileNotFoundError:
        pass
    with open(resfile, 'a', encoding='utf-8', newline='\n') as out:
        for p in primes:
            for k in range(1, kmax + 1):
                if (str(p), str(k)) in done:
                    continue
                if k <= K_MONO:
                    peak = 2 * (1 << k) * 8 / 2**30
                    if peak > budget:
                        out.write(f"# k={k} skipped: mono peak {peak:.2f} GB > "
                                  f"half-free budget {budget:.2f} GB\n")
                        out.flush()
                        continue
                    t0 = time.time()
                    tot = run_dp_ram(k, ROWS, np.int64, p)
                    mode = 'mono'
                else:
                    peak = (1 << k) * 8 / 2**30 + (1 << (k - 1)) * 8 / 2**30
                    if peak > budget:
                        out.write(f"# k={k} skipped: sliced peak {peak:.2f} GB > "
                                  f"half-free budget {budget:.2f} GB\n")
                        out.flush()
                        continue
                    t0 = time.time()
                    tot = run_dp_sliced(k, ROWS, p)
                    mode = 'sliced'
                stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                for j in range(1, ROWS + 1):
                    out.write(f"p={p} k={k} j={j} r={int(tot[j-1])}\n")
                out.write(f"# stamp={stamp} p={p} k={k} mode={mode} "
                          f"secs={time.time()-t0:.0f}\n")
                out.flush()
                if dt.datetime.now(dt.timezone.utc) > dl:
                    out.write(f"# soft deadline {deadline} reached, stopping cleanly\n")
                    return 0
    print("ALL DONE", flush=True)
    return 0


if __name__ == "__main__":
    m = sys.argv[1]
    if m == "gate":
        sys.exit(mode_gate(False))
    if m == "gate-sliced":
        sys.exit(mode_gate(True))
    if m == "primes":
        mode_primes()
        sys.exit(0)
    if m == "work":
        kmax = int(sys.argv[4]) if len(sys.argv) > 4 else 28
        sys.exit(mode_work(sys.argv[2], sys.argv[3], kmax))
    sys.exit(2)
