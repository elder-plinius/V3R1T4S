#!/usr/bin/env python
"""Run A: ROW-SWEEP broken-profile DP for A210662 column k (bank p2, row 28).

Ported from the a(28) Run B column DP (runs/2026-10-28-0734, proven): axes swapped —
the 28 x k board is scanned ROW-major; the frontier is the current row's k cells.
State after processing cell (row j, col i): k-bit mask; bit set = cell covered by a
domino hanging into the next row (cross-row) or by the within-row left-domino
(verified by the gate below against rect_tables.py and the b-file).

Per outer step j the empty-frontier value dp[0] = T(j+1, k) EXACTLY (no overhang =
complete tiling of rows 0..j), so one sweep records the whole column j = 1..28.

Residue discipline: per-step sums touch at most 2 int64 terms (<= 2(p-1) < 2^63 for
61-bit p); np.remainder after every inner step; values read as dp[0] (no .sum()).

Modes:
  gate                     exact big-int sweep k = 1..12, all j, vs rect_tables + b-file
  primes                   the 13 set-A primes (first proven primes > 2^61 + 1_000_000)
  work <resfile> <deadline_UTC>   checkpointed loop, appends "p=.. k=.. j=.. r=.."
"""
import sys
import time
import datetime as dt
import numpy as np

ROWS = 28


def is_probable_prime(n, witnesses=(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)):
    """Deterministic Miller-Rabin, valid for n < 3.3e24 (bases 2..37)."""
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


def gen_primes_61bit(count, start_after):
    out = []
    c = start_after | 1  # force odd (bug fix: the old parity flip was inverted and looped on evens forever)
    while len(out) < count:
        if is_probable_prime(c):
            out.append(c)
        c += 2
    return out


def run_dp(width, rows, dtype, mod):
    """Row-major sweep of a rows x width board; returns list of dp[0] after each row."""
    size = 1 << width
    dp = np.zeros(size, dtype=dtype)
    dp[0] = 1
    totals = []
    for j in range(rows):
        last_row = j == rows - 1
        for i in range(width):
            v = dp.reshape(-1, 2, 1 << i)
            bs = v[:, 1, :]
            bc = v[:, 0, :]
            new = np.empty_like(v)
            new[:, 0, :] = bs
            new[:, 0, :] += bc                       # <= 2(p-1): safe
            if last_row:
                new[:, 1, :] = 0                     # no dominoes past the board
            else:
                new[:, 1, :] = bc                    # cross-row domino
            if i < width - 1:
                w = new.reshape(-1, 2, 2, 1 << i)
                sw = bc.reshape(-1, 2, 1 << i)
                w[:, 1, 0, :] += sw[:, 0, :]         # within-row right-domino
            dp = new.reshape(-1)
            if mod:
                np.remainder(dp, mod, out=dp)
            del bs, bc, v
        totals.append(dp[0])
    return totals


def rss_mb():
    import ctypes
    import ctypes.wintypes as w
    class PMC(ctypes.Structure):
        _fields_ = [('cb', w.DWORD), ('PageFaultCount', w.DWORD),
                    ('PeakWorkingSetSize', ctypes.c_size_t),
                    ('WorkingSetSize', ctypes.c_size_t),
                    ('QuotaPeakPagedPoolUsage', ctypes.c_size_t),
                    ('QuotaPagedPoolUsage', ctypes.c_size_t),
                    ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t),
                    ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
                    ('PagefileUsage', ctypes.c_size_t),
                    ('PeakPagefileUsage', ctypes.c_size_t)]
    pmc = PMC()
    pmc.cb = ctypes.sizeof(PMC)
    ctypes.windll.psapi.GetProcessMemoryInfo(
        ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb)
    return pmc.PeakWorkingSetSize / 2**20


def mode_gate():
    sys.path.insert(0, '.')
    from rect_tables import matchings
    bad = 0
    for k in range(1, 13):
        tot = run_dp(k, ROWS, object, 0)
        for j in range(1, ROWS + 1):
            ref = matchings(k, j)
            if int(tot[j - 1]) != ref:
                print(f"FAIL k={k} j={j} sweep={tot[j-1]} ref={ref}")
                bad += 1
    print("GATE %s (row sweeps vs from-definition DP, k=1..12, all j=1..28: %d cells)"
          % ("PASS" if bad == 0 else "FAIL", 12 * ROWS))
    return 1 if bad else 0


def mode_primes():
    ps = gen_primes_61bit(13, (1 << 61) + 1_000_000)
    for p in ps:
        assert (1 << 63) > 2 * (p - 1)
        print(p, flush=True)


def mode_work(resfile, deadline):
    dl = dt.datetime.strptime(deadline, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    primes = gen_primes_61bit(13, (1 << 61) + 1_000_000)
    done = set()
    try:
        for line in open(resfile, encoding='utf-8'):
            if line.startswith('p='):
                f = dict(x.split('=') for x in line.split())
                done.add((f['p'], f['k']))
    except FileNotFoundError:
        pass
    with open(resfile, 'a', encoding='utf-8', newline='\n') as out:
        for p in primes:
            for k in range(1, 28):
                if (str(p), str(k)) in done:
                    continue
                t0 = time.time()
                tot = run_dp(k, ROWS, np.int64, p)
                stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                for j in range(1, ROWS + 1):
                    out.write(f"p={p} k={k} j={j} r={int(tot[j-1])}\n")
                out.write(f"# stamp={stamp} k={k} p={p} secs={time.time()-t0:.0f} "
                          f"peak_rss_mb={rss_mb():.0f}\n")
                out.flush()
                if dt.datetime.now(dt.timezone.utc) > dl:
                    out.write(f"# soft deadline {deadline} reached, stopping cleanly\n")
                    print(f"deadline reached after k={k}", flush=True)
                    return 0
    print("ALL DONE", flush=True)
    return 0


if __name__ == "__main__":
    m = sys.argv[1]
    if m == "gate":
        sys.exit(mode_gate())
    if m == "primes":
        mode_primes()
        sys.exit(0)
    if m == "work":
        sys.exit(mode_work(sys.argv[2], sys.argv[3]))
    sys.exit(2)
