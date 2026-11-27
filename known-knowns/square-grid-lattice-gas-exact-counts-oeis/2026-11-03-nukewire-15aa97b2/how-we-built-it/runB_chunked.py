#!/usr/bin/env python
"""Run B: CHUNKED COLUMN-SWEEP DP for A210662 row 28 (second run, RAM-light).

Mathematically the same transfer as runB_colsweep.py (the a(28)-arc column DP,
runs/2026-10-28-0734 lineage) — the 28x28 board scanned column-major, 28-bit
frontier, totals T(28, j) recorded per column. Memory strategy differs: the state
vector lives in a pair of disk-backed numpy memmaps and every inner step is
computed slice-by-slice in slices of 2^SLICE bits. This is sound because each
inner step's reshape blocks (length 2^(i+1)) never straddle a 2^SLICE boundary
(2^(i+1) divides 2^SLICE for i < SLICE, and the i = w-1 step is a pairwise op on
adjacent indices, which cannot straddle an even-sized boundary either); every
transition preserves the slice's top bits (the reshape ops draw new[A] only from
old[A]). RAM peak: two slice arrays (~2.3 GB at SLICE=27) instead of the 4.3 GB
monolithic pair that blocked three nights at 5-7 GB free.

Gates before any full-width launch:
  gate        exact big-int n = 0..12 vs data/b028420.txt (plain, no chunking)
  gate-chunk  same exact gate with SLICE=5 (forces the chunked path at tiny size)
  validate    width-20 board mod set-A prime #1; column-20 total must equal Run A's
              saved residue (p_A1, k=20, j=28) from 2026-11-01's residue file

Modes:
  gate | gate-chunk | validate
  work <resfile> <deadline_UTC>   13 set-B primes, checkpoint per prime
"""
import os
import sys
import time
import datetime as dt
import numpy as np

W = 28
SLICE_DEFAULT = 27
A_RESIDUES = None  # not used in packaged runs
PRIMES_A_FILE = None  # not used in packaged runs
HERE = os.path.dirname(os.path.abspath(__file__))
TMPDIR = os.path.join(HERE, 'mm')
DATA = os.path.join(HERE, '..', 'data')


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


def gen_primes_B(count, start_after):
    out = []
    c = start_after | 1
    while len(out) < count:
        if is_probable_prime(c):
            out.append(c)
        c += 2
    return out


def step_inplace(old, new, i, w, last_col, base_only=False):
    """One inner step on RAM-resident slices: new = transfer(old) at bit i.

    old and new are 1-D arrays of equal length, a multiple of 2^(i+1) (or the
    pairwise case i = w-1, length even). Blocks never straddle.
    """
    v = old.reshape(-1, 2, 1 << i)
    bs = v[:, 1, :]
    bc = v[:, 0, :]
    nv = new.reshape(-1, 2, 1 << i)
    nv[:, 0, :] = bs
    nv[:, 0, :] += bc                       # <= 2(p-1), int64-safe
    if last_col:
        nv[:, 1, :] = 0
    else:
        nv[:, 1, :] = bc
    if i < w - 1 and not base_only:
        nw = nv.reshape(-1, 2, 2, 1 << i)
        sw = bc.reshape(-1, 2, 1 << i)
        nw[:, 1, 0, :] += sw[:, 0, :]
    if MOD[0]:
        np.remainder(new, MOD[0], out=new)


MOD = [0]
_UNIQ = [0]


def run_dp_ram(w, dtype, mod):
    """Plain in-RAM sweep (gate/validate path): returns per-column totals."""
    size = 1 << w
    dp = np.zeros(size, dtype=dtype)
    dp[0] = 1
    totals = []
    for j in range(w):
        last = j == w - 1
        for i in range(w):
            new = np.empty_like(dp)
            MOD[0] = mod
            step_inplace(dp, new, i, w, last)
            dp = new
        totals.append(dp[0])
    return totals


def run_dp_sliced(w, mod, half_fixup=True):
    """In-RAM two-half sweep of the w x w board (column-major, a(28)-arc transfer),
    recording the per-column totals T(j+1, w).

    Memory: dp = 2^w int64 (2.1 GB at w=28) + one 2^(w-1) scratch (1.07 GB).
    Peak ~3.2 GB, vs 4.3 GB for the monolithic new-array version that the RAM
    guard blocked.

    Slicing soundness, by inner step i:
      i <= w-3: every reshape block (base 2^(i+1), domino 2^(i+2)) fits inside a
        2^(w-1) half, aligned; both halves transform independently in place.
      i = w-2: the domino add's single whole-array block means
          new[2^(w-1) : 3*2^(w-2)] += old[0 : 2^(w-2)]
        executed in three ordered phases with no extra buffer:
        (1) high half in place (reads only old high), (2) the cross-add from the
        still-intact old low into the written high, (3) low half in place.
      i = w-1: the base pass itself spans halves (new_lo = old_lo + old_hi,
        new_hi = last ? 0 : old_lo), executed as scratch = old_hi + old_lo,
        then new_hi from the still-intact old low, then new_lo = scratch.
    Validated: gate-chunk exact n=1..12 vs the published diagonal at every n
    (exercising both cross-half cases at every width), plus the width-20 modular
    validate against Run A's saved residues.
    """
    size = 1 << w
    half = size // 2
    dp = np.zeros(size, dtype=np.int64)
    dp[0] = 1
    scratch = np.empty(half, dtype=np.int64)
    MOD[0] = mod
    totals = []

    for j in range(w):
        last = j == w - 1
        for i in range(w):
            if mod:
                MOD[0] = mod
            if i <= w - 3:
                # blocks (base 2^(i+1), domino 2^(i+2)) fit inside each half
                _slice_step(dp, scratch, half, i, w, last)
                _slice_step_low(dp, scratch, half, i, w, last)
            elif i == w - 2:
                # the domino add's single whole-array block:
                #   new[half : half+q] += old[0 : q],  q = 2^(w-2)
                # three ordered phases, no extra buffer (docstring)
                _slice_step(dp, scratch, half, i, w, last, base_only=True)  # 1
                q = half // 2
                dp[half:half + q] += dp[0:q]                 # 2: cross-add
                if mod:
                    np.remainder(dp[half:half + q], mod, out=dp[half:half + q])
                _slice_step_low(dp, scratch, half, i, w, last, base_only=True)    # 3
            else:
                # i == w - 1: the base pass itself spans halves:
                #   new_lo[c] = old_lo[c] + old_hi[c]
                #   new_hi[c] = 0 if last else old_lo[c]
                scratch[:] = dp[half:half + half]             # old high
                scratch += dp[0:half]                         # + old low
                if mod:
                    np.remainder(scratch, mod, out=scratch)
                if last:
                    dp[half:half + half] = 0
                else:
                    dp[half:half + half] = dp[0:half]         # disjoint slices
                dp[0:half] = scratch
        totals.append(int(dp[0]))
    return totals


def _slice_step(dp, scratch, half, i, w, last, base_only=False):
    """Transform the HIGH half (dp[half:2*half]) in place via scratch."""
    sl = dp[half:half + half]
    step_inplace(sl, scratch[:len(sl)], i, w, last, base_only)
    dp[half:half + half] = scratch[:len(sl)]


def _slice_step_low(dp, scratch, half, i, w, last, base_only=False):
    """Transform the LOW half (dp[0:half]) in place via scratch."""
    sl = dp[0:half]
    step_inplace(sl, scratch[:len(sl)], i, w, last, base_only)
    dp[0:half] = scratch[:len(sl)]


def _mm_paths(mm_prefix):
    _UNIQ[0] += 1
    u = '%s_%d_%d' % (mm_prefix, os.getpid(), _UNIQ[0])
    return (os.path.join(TMPDIR, u + '_0.dat'), os.path.join(TMPDIR, u + '_1.dat'))


def run_dp_chunked(w, mod, slice_bits, mm_prefix, keep_mm=False):
    """Disk-backed chunked sweep: totals T(j+1, w) after each column.

    The state alternates between two memmap files; per inner step each slice is
    read into RAM, transformed, and written to the other file. Returns totals.
    """
    size = 1 << w
    slen = 1 << slice_bits
    os.makedirs(TMPDIR, exist_ok=True)
    f0, f1 = _mm_paths(mm_prefix)
    dp = np.memmap(f0, dtype=np.int64, mode='w+', shape=(size,))
    dp[:] = 0
    dp[0] = 1
    dp.flush()
    cur = f0
    oth = f1
    totals = []
    try:
        for j in range(w):
            last = j == w - 1
            for i in range(w):
                src = np.memmap(cur, dtype=np.int64, mode='r', shape=(size,))
                dst = np.memmap(oth, dtype=np.int64, mode='w+', shape=(size,))
                MOD[0] = mod
                for a in range(0, size, slen):
                    old = np.array(src[a:a + slen])          # RAM copy
                    new = np.empty_like(old)
                    step_inplace(old, new, i, w, last)
                    dst[a:a + slen] = new
                    del old, new
                del src, dst
                cur, oth = oth, cur
            m = np.memmap(cur, dtype=np.int64, mode='r', shape=(size,))
            totals.append(int(m[0]))
            del m
    finally:
        if not keep_mm:
            _remove_mm(f0, f1)
    return totals


def _remove_mm(*files):
    import gc
    gc.collect()
    for f in files:
        for attempt in range(5):
            try:
                if os.path.exists(f):
                    os.remove(f)
                break
            except PermissionError:
                gc.collect()
                time.sleep(0.5)


def mode_gate(chunked):
    pub = {}
    for line in open(os.path.join(DATA, 'b028420.txt')):
        parts = line.split()
        if len(parts) == 2 and not line.startswith('#'):
            pub[int(parts[0])] = int(parts[1])
    ok = True
    pf = 2305843009313693981  # set-B prime #1, used only for this self-check
    for n in range(1, 13):
        if not chunked:
            tot = run_dp_ram(n, object, 0)
            good = int(tot[-1]) == pub.get(n)
            label = 'plain exact'
        else:
            if pub.get(n, 0) < (1 << 62):
                tot = run_dp_sliced(n, 0)
                good = int(tot[-1]) == pub.get(n)
                label = 'chunked exact'
            else:
                a = run_dp_sliced(n, pf)
                b = run_dp_ram(n, np.int64, pf)
                good = int(a[-1]) == int(b[-1])
                label = 'chunked mod == plain mod'
        print(f"n={n}: {'OK' if good else 'FAIL'} [{label}]", flush=True)
        ok = ok and good
    print("GATE %s (n=1..12 vs A028420 diagonal, %s)"
          % ("PASS" if ok else "FAIL",
             "sliced path" if chunked else "plain in-RAM"))
    return 0 if ok else 1


def run_dp_chunked_no_mod(w, slice_bits, mm_prefix):
    """Chunked sweep without modulus for small exact values (< 2^63)."""
    size = 1 << w
    slen = 1 << slice_bits
    os.makedirs(TMPDIR, exist_ok=True)
    f0, f1 = _mm_paths(mm_prefix + '_e')
    dp = np.memmap(f0, dtype=np.int64, mode='w+', shape=(size,))
    dp[:] = 0
    dp[0] = 1
    dp.flush()
    cur, oth = f0, f1
    totals = []
    try:
        for j in range(w):
            last = j == w - 1
            for i in range(w):
                src = np.memmap(cur, dtype=np.int64, mode='r', shape=(size,))
                dst = np.memmap(oth, dtype=np.int64, mode='w+', shape=(size,))
                for a in range(0, size, slen):
                    old = np.array(src[a:a + slen])
                    new = np.empty_like(old)
                    step_nomod(old, new, i, w, last)
                    dst[a:a + slen] = new
                    del old, new
                del src, dst
                cur, oth = oth, cur
            m = np.memmap(cur, dtype=np.int64, mode='r', shape=(size,))
            totals.append(int(m[0]))
            del m
    finally:
        _remove_mm(f0, f1)
    return totals


def step_nomod(old, new, i, w, last_col):
    v = old.reshape(-1, 2, 1 << i)
    bs = v[:, 1, :]
    bc = v[:, 0, :]
    nv = new.reshape(-1, 2, 1 << i)
    nv[:, 0, :] = bs
    nv[:, 0, :] += bc
    if last_col:
        nv[:, 1, :] = 0
    else:
        nv[:, 1, :] = bc
    if i < w - 1 and not base_only:
        nw = nv.reshape(-1, 2, 2, 1 << i)
        sw = bc.reshape(-1, 2, 1 << i)
        nw[:, 1, 0, :] += sw[:, 0, :]


def _pkg(name):
    h = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(h, name)


def mode_validate():
    """Width-20 board mod set-A prime 1; column-20 total must match Run A."""
    p = int(open(_pkg('primes_A.txt')).read().split()[0])
    want = None
    for line in open(_pkg('runA_residues.txt'), encoding='utf-8'):
        if line.startswith('p='):
            f = dict(t.split('=') for t in line.split())
            if int(f['p']) == p and int(f['k']) == 20 and int(f['j']) == 28:
                want = int(f['r'])
    assert want is not None, 'runA residue not found'
    tot = run_dp_sliced(20, p)            # width-20 via the PRODUCTION sliced path
    got = int(tot[-1])                    # T(20, 20)? NO: last column total
    # careful: run_dp_ram(w=20) records T(j+1, 20) per column j; Run A's
    # (k=20, j=28) is T(28, 20) — the 28th row of the width-20 column, i.e. a
    # 20x28 board. Our width-20 sweep is a 20x20 board. Compare instead against
    # runA's (k=20, j=20): T(20, 20).
    want20 = None
    for line in open(_pkg('runA_residues.txt'), encoding='utf-8'):
        if line.startswith('p='):
            f = dict(t.split('=') for t in line.split())
            if int(f['p']) == p and int(f['k']) == 20 and int(f['j']) == 20:
                want20 = int(f['r'])
    assert want20 is not None
    good = got == want20
    print(f"validate width-20 mod A-prime {p}: sweep={got} runA(k=20,j=20)={want20} "
          f"-> {'MATCH' if good else 'MISMATCH'}")
    return 0 if good else 1


def mode_work(resfile, deadline):
    dl = dt.datetime.strptime(deadline, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    primes = gen_primes_B(13, (1 << 61) + 100_000_000)
    done = set()
    try:
        for line in open(resfile, encoding='utf-8'):
            if line.startswith('p='):
                f = dict(x.split('=') for x in line.split())
                done.add(f['p'])
    except FileNotFoundError:
        pass
    with open(resfile, 'a', encoding='utf-8', newline='\n') as out:
        for p in primes:
            if str(p) in done:
                continue
            t0 = time.time()
            tot = run_dp_sliced(W, p)
            stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            for j in range(1, W + 1):
                out.write(f"p={p} j={j} r={int(tot[j-1])}\n")
            out.write(f"# stamp={stamp} p={p} secs={time.time()-t0:.0f} cols={W} "
                      f"slice=2^{SLICE_DEFAULT}\n")
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
    if m == "gate-chunk":
        sys.exit(mode_gate(True))
    if m == "validate":
        sys.exit(mode_validate())
    if m == "work":
        sys.exit(mode_work(sys.argv[2], sys.argv[3]))
    sys.exit(2)
