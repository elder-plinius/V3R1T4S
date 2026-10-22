#!/usr/bin/env python3
"""far-import counter for A089980 (independent sets of P_w x P_m), written fresh for run 2026-10-17-1913.

Decomposition: row-to-row (whole-column) transfer.  State = independent row pattern s (Fibonacci string of
length w).  v_1(s) = 1, v_{m+1}(s) = sum_{t indep, t&s=0} v_m(t), T(w,m) = sum_s v_m(s), T(w,0)=1.
The map f -> g, g(s)=sum_{t&s=0} f(t), is computed by a w-pass "butterfly" over the Fibonacci trie:
after pass k the array h_k[s_prefix(len k), t_suffix(len w-k)] holds partial sums with bits <k already
converted from t-space to s-space.  Suffixes are ranked by first bit (S_n = 0.S_{n-1} | 10.S_{n-2}),
prefixes by last bit (P_k = P_{k-1}.0 | P_{k-2}.01), so pass k is three slab copies/adds of a 2-D array.
Output is ranked by P = S-rank of the reversed string; because start vector is reversal-symmetric and the
transfer commutes with reversal, g(rev s) = g(s) and no permutation is needed (verified explicitly for small w
in selftest).  Arithmetic: uint64, inputs < p < 2^30, intermediate <= F(w+2)*p < 2^58 for w<=39, one mod per
column step.  Primes: largest primes below 2^30, descending; CRT with bound F(w+2)^m plus a check prime.
"""
import sys, os, time, json, resource

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
RES = os.path.join(WS, "res")
TSV = os.path.join(WS, "antidiag79_far.tsv")
BFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b089980.txt")
D = 79


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a  # F(0)=0, F(1)=1, F(2)=1


def is_prime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):  # deterministic for n < 3.3e24
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


def primes_below_2_30(count):
    out, n = [], (1 << 30) - 1
    while len(out) < count:
        if is_prime(n):
            out.append(n)
        n -= 1
    return out


def transfer(v, w, p):
    """v: 1-D array (S-ranked) of length F(w+2), or a 1-element list holding it (popped so the caller's
    reference is dropped and the input can be freed early). Returns g (S-ranked via symmetry). p=None -> exact."""
    if isinstance(v, list):
        v = v.pop()
    H = v.reshape(1, -1)
    del v
    for k in range(w):
        n = w - k
        A = H.shape[0]
        assert A == fib(k + 2) and H.shape[1] == fib(n + 2)
        c0 = fib(n + 1)          # t_k = 0 block, indexed by u in S_{n-1}
        c1 = fib(n)              # t_k = 1 block, indexed by v, u = 0v = first F(n) of S_{n-1}
        rA1 = fib(k + 1)         # s_prefix ending in 0 = first F(k+1) rows of P_k
        new = np.empty((A + rA1, c0), dtype=H.dtype)
        H0 = H[:, :c0]
        new[:A] = H0
        new[:A, :c1] += H[:, c0:]
        new[A:] = H0[:rA1]
        H = new
    g = H.reshape(-1)
    if p is not None:
        g %= np.uint64(p)
    return g


def transfer32(v, w, p):
    """uint32 variant: every stored value kept in [0,p) (p<2^30), the only add is followed by a branch-free
    conditional subtract min(x, x-p) (x-p wraps to >=2^32-p > x when x<p).  Same trie/ranking as transfer()."""
    if isinstance(v, list):
        v = v.pop()
    H = v.reshape(1, -1)
    del v
    P32 = np.uint32(p)
    for k in range(w):
        n = w - k
        A = H.shape[0]
        c0 = fib(n + 1); c1 = fib(n); rA1 = fib(k + 1)
        new = np.empty((A + rA1, c0), dtype=np.uint32)
        H0 = H[:, :c0]
        new[:A] = H0
        X = new[:A, :c1]
        X += H[:, c0:]
        np.minimum(X, X - P32, out=X)
        new[A:] = H0[:rA1]
        H = new
    return H.reshape(-1)


def residues(w, p, M):
    """T(w,m) mod p (or exact if p None) for m=0..M."""
    if w == 0:
        return [1] * (M + 1)
    N = fib(w + 2)
    U32 = os.environ.get("FAR_U32") == "1" and p is not None
    if p is None:
        v = np.array([1] * N, dtype=object)
    elif U32:
        v = np.ones(N, dtype=np.uint32)
    else:
        v = np.ones(N, dtype=np.uint64)
    out = [1]
    for m in range(1, M + 1):
        if m > 1:
            v = transfer32([v], w, p) if U32 else transfer([v], w, p)
        s = int(v.sum()) if p is None else int(v.sum(dtype=np.uint64)) % p
        out.append(s)
    return out


def load_bfile():
    T = {}
    for line in open(BFILE):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        k, v = map(int, line.split())
        d = int(((8 * k + 1) ** 0.5 - 1) // 2)
        while d * (d + 1) // 2 > k:
            d -= 1
        while (d + 1) * (d + 2) // 2 <= k:
            d += 1
        i = k - d * (d + 1) // 2
        T[(i, d - i)] = v
    return T


def nprimes_for(w, m, primes):
    B = fib(w + 2) ** m
    prod, n = 1, 0
    while prod <= B:
        prod *= primes[n]; n += 1
    return n


def crt(res, mods):
    x, M = 0, 1
    for r, q in zip(res, mods):
        t = ((r - x) * pow(M, -1, q)) % q
        x += M * t
        M *= q
    return x, M


def resfile(w, p):
    return os.path.join(RES, f"w{w}_p{p}.json")


def job(w, p, deadline):
    """Compute and store residues for width w, prime p (m=0..79-w). Returns (w,p,secs,maxrss_MB) or None."""
    f = resfile(w, p)
    if os.path.exists(f):
        return (w, p, 0.0, 0.0, "cached")
    if time.time() > deadline:
        return (w, p, 0.0, 0.0, "skipped-deadline")
    t0 = time.time()
    r = residues(w, p, D - w)
    secs = time.time() - t0
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 20  # macOS: bytes
    tmp = f + ".tmp"
    with open(tmp, "w") as fh:
        json.dump({"w": w, "p": p, "res": r, "secs": secs, "maxrss_MB": rss}, fh)
    os.replace(tmp, f)
    return (w, p, secs, rss, "done")


def finalize(w, primes, T):
    M = D - w
    n = nprimes_for(w, M, primes)
    chk = primes[n]
    data = {}
    for p in primes[:n + 1]:
        data[p] = json.load(open(resfile(w, p)))
    mods = primes[:n]
    pub = mism = 0
    vals = []
    for m in range(0, M + 1):
        x, Mod = crt([data[p]["res"][m] for p in mods], mods)
        assert Mod > fib(w + 2) ** m
        vals.append(x)
        if m <= D - 1 - w:
            pub += 1
            if x != T[(w, m)]:
                mism += 1
            if T[(w, m)] != T[(m, w)]:
                mism += 1
    x79 = vals[M]
    chk_ok = (x79 % chk == data[chk]["res"][M])
    # check prime also on every published cell
    for m in range(0, M + 1):
        if vals[m] % chk != data[chk]["res"][m]:
            chk_ok = False
    secs = sum(data[p]["secs"] for p in data)
    rss = max(data[p]["maxrss_MB"] for p in data)
    return dict(w=w, m=M, n=n, chk=chk, pub=pub, mism=mism, chk_ok=chk_ok, T=x79, secs=secs, rss=rss)


def selftest():
    T = load_bfile()
    bad = 0
    # 1) exact object-dtype transfer vs every published cell, w=0..12
    for w in range(0, 13):
        r = residues(w, None, D - 1 - w)
        mm = sum(1 for m in range(len(r)) if r[m] != T[(w, m)])
        bad += mm
        print(f"exact w={w}: {len(r)} published cells, mismatches={mm}")
    # 2) explicit reversal check: compute with explicit permutation on small w
    for w in range(1, 11):
        S = {0: [""], 1: ["0", "1"]}
        for n in range(2, w + 1):
            S[n] = ["0" + x for x in S[n - 1]] + ["10" + x for x in S[n - 2]]
        rank = {s: i for i, s in enumerate(S[w])}
        perm = np.array([rank[s[::-1]] for s in S[w]])  # P-rank -> S-rank
        # P-rank(s) = S-rank(rev s): output index j corresponds to string rev(S[w][j])
        rng = np.random.default_rng(w)
        f = rng.integers(0, 1000, size=len(S[w])).astype(object)
        g = transfer(f.copy(), w, None)
        # direct definition
        gd = []
        ints = [int(s, 2) if s else 0 for s in S[w]]
        for j, s in enumerate(S[w]):
            si = int(s[::-1], 2) if s else 0  # string whose P-rank is j is rev(S[w][j])
            gd.append(sum(f[i] for i, t in enumerate(ints) if t & si == 0))
        ok_def = all(int(a) == int(b) for a, b in zip(g, gd))
        # symmetry of iterated vector from all-ones
        v = np.array([1] * len(S[w]), dtype=object)
        sym = True
        for _ in range(4):
            v = transfer(v, w, None)
            sym &= all(int(v[i]) == int(v[perm[i]]) for i in range(len(v)))
        print(f"w={w}: transform==definition(random f, P-ranked) {ok_def}; iterated vector reversal-symmetric {sym}")
        bad += (not ok_def) + (not sym)
    # 3) modular vs exact on w=9..12, prime below 2^30
    pr = primes_below_2_30(3)
    for w in (9, 12, 16):
        ex = residues(w, None, 20)
        for p in pr:
            r = residues(w, p, 20)
            mm = sum(1 for a, b in zip(r, ex) if a != b % p)
            bad += mm
        print(f"modular vs exact w={w} m<=20 primes {pr}: mismatches so far {bad}")
    print("SELFTEST:", "PASS" if bad == 0 else f"FAIL ({bad})")


def bench(w, nsteps=3):
    p = primes_below_2_30(1)[0]
    N = fib(w + 2)
    v = np.ones(N, dtype=np.uint64)
    t0 = time.time()
    U32 = os.environ.get("FAR_U32") == "1"
    if U32:
        v = v.astype(np.uint32)
    for _ in range(nsteps):
        v = transfer32([v], w, p) if U32 else transfer([v], w, p)
    dt = (time.time() - t0) / nsteps
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 20
    print(f"bench w={w} F(w+2)={N} sec/step={dt:.3f} est sec/prime={dt*(D-w):.1f} maxrss_MB={rss:.0f}", flush=True)


def drive(w_lo, w_hi, nproc, deadline_iso):
    import concurrent.futures as cf
    from datetime import datetime, timezone
    deadline = datetime.fromisoformat(deadline_iso.replace("Z", "+00:00")).timestamp()
    os.makedirs(RES, exist_ok=True)
    T = load_bfile()
    primes = primes_below_2_30(45)
    print("primes(desc, first 45):", primes, flush=True)
    if not os.path.exists(TSV):
        with open(TSV, "w") as fh:
            fh.write("w\tm\tnprimes\tpub_cells\tpub_mismatch\tcheck_prime_ok\tT_w_79mw\n")
    done_w = set()
    for line in open(TSV).read().splitlines()[1:]:
        done_w.add(int(line.split("\t")[0]))
    widths = [w for w in range(w_lo, w_hi + 1) if w not in done_w]
    need = {w: primes[:nprimes_for(w, D - w, primes) + 1] for w in widths}
    pending = {w: set(need[w]) for w in widths}
    log = open(os.path.join(HERE, "timing_out.txt"), "a")
    with cf.ProcessPoolExecutor(max_workers=nproc) as ex:
        futs = []
        for w in widths:
            for p in need[w]:
                futs.append(ex.submit(job, w, p, deadline))
        next_w = 0
        for fu in cf.as_completed(futs):
            w, p, secs, rss, st = fu.result()
            print(f"{time.strftime('%H:%M:%S')} job w={w} p={p} {st} {secs:.1f}s rss={rss:.0f}MB", flush=True)
            log.write(f"w={w}\tp={p}\t{st}\t{secs:.2f}\t{rss:.0f}\n"); log.flush()
            if st in ("done", "cached"):
                pending[w].discard(p)
            # finalize widths in increasing order once complete
            while next_w < len(widths) and not pending[widths[next_w]]:
                ww = widths[next_w]
                r = finalize(ww, primes, T)
                with open(TSV, "a") as fh:
                    fh.write(f"{ww}\t{r['m']}\t{r['n']}\t{r['pub']}\t{r['mism']}\t{r['chk_ok']}\t{r['T']}\n")
                print(f"FINAL w={ww} m={r['m']} nprimes={r['n']} check_prime={r['chk']} pub={r['pub']} "
                      f"mism={r['mism']} chk_ok={r['chk_ok']} cpu_s={r['secs']:.1f} peak_rss_MB={r['rss']:.0f} "
                      f"T={r['T']}", flush=True)
                next_w += 1
    print("DRIVER DONE", time.strftime('%H:%M:%S'), flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "selftest":
        selftest()
    elif cmd == "bench":
        for w in map(int, sys.argv[2:]):
            bench(w)
    elif cmd == "drive":
        lo, hi = int(sys.argv[2]), int(sys.argv[3])
        if lo >= 33:
            # large widths: uint32 variant (validated == uint64 residues, u32_vs_u64_out.txt), one executor per
            # width, process count from the 1.4 GB memory cap with measured ~33 B/state + 40 MB per process
            os.environ["FAR_U32"] = "1"
            for w in range(lo, hi + 1):
                est = 33 * fib(w + 2) / 1e6 + 40
                npw = max(1, min(3, int(1400 // est)))
                print(f"width {w}: FAR_U32=1 nproc={npw} est_MB_per_proc={est:.0f}", flush=True)
                drive(w, w, npw, sys.argv[5])
        else:
            drive(lo, hi, int(sys.argv[4]), sys.argv[5])
