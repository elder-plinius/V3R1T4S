"""V3R1T4S — additive Fermat-quotient sweep for Wieferich pairs over B-smooth bases.

A Wieferich pair (b, p) has pow(b, p-1, p*p) == 1.  q_p(b) = (b^(p-1) - 1)/p mod p is a homomorphism
(Z/p^2)* -> Z/p, so q_p(prod r^e) = sum e*q_p(r) mod p.  For each prime p the sweep computes q_p(r) for the primes
r <= B only (pi(B) exponentiations, one gmpy2 call) and gets q_p(b) for every non-perfect-power B-smooth base b in
[BLO, BHI] as an exact integer linear form.  Every flagged (b, p) is re-verified with pow(b, p-1, p*p) == 1 in plain
Python integers before it is reported as a hit.

Exactness of the float64 screen: q_r < p < 2^43 and sum(e) <= 16 for b < 2^16, so every partial sum of the dot
product is an integer < 2^47 < 2^53 (exact in float64 BLAS).  D = S * fl(1/p) is within 2^-47 of S/p; a true hit
(S = k*p) has |D - k| < 2^-40 and is never missed.  A non-hit is flagged only when S mod p is within ~8 of 0 or p
(a near-miss, |q_p(b)| small) and is then rejected by the exact check.  Valid for p < 2^43 (~8.8e12): above that,
re-derive the margin before use.

Screens: the default is the exact meet-in-the-middle screen (class MitmScreen, since 2026-11-07); set
WIEFERICH_SCREEN=float in the environment for the float64 screen described above.

Modes (run with the workspace venv python; keep fischer_parse.py next to this file for selftest):
  sweep OUTDIR START BLK NWORKERS DEADLINE_EPOCH B BLO BHI MAX_HI
        primes START <= p in contiguous blocks of BLK, no new block after DEADLINE_EPOCH (UTC epoch), never past
        MAX_HI (which also sizes the sieve's base primes, sqrt(MAX_HI)).  Resumable: blocks already present in
        OUTDIR/blocks.jsonl are skipped.  Writes blocks.jsonl, hits.jsonl (flushed per hit), pid.txt.
        While it runs, the main thread holds a Windows keep-awake request (system and display required, see
        keep_awake), so no idle timeout can drop the machine into modern standby mid-sweep.  pid.txt records it
        ('keep_awake 0x80000003' = held).  Set V3R1T4S_KEEP_AWAKE=0 in the environment to skip it.
  summarise OUTDIR START BLK      contiguous coverage from START, primes, candidates, hits, PIDs, peak memory (JSON)
  selftest TABLE [B] [N]          replay the pipeline on N listed pairs below the table's limit (known positives;
                                  every hit in a window must be a listed pair).  Last line SELFTEST PASS|FAIL.
  bench LO [B]                    one real-size block (2e7 numbers) at LO: seconds, us/prime, peak memory (RULES 10)
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import sys, json, time, hashlib, math
import numpy as np
from gmpy2 import mpz, powmod_base_list

TOL = 2.0 ** -40
HERE = os.path.dirname(os.path.abspath(__file__))
# Exact meet-in-the-middle screen (lens evaluator-first, run 2026-11-07-1751), the default since 2026-11-07 on the
# ADMIN's decision. It was validated on both base sets: identical hits, prime counts and q-matrix sha256 to the float
# screen (references/host-mechanics.md). Its block records carry "screen": "mitm", and its candidates are exact zeros
# only. WIEFERICH_SCREEN=float selects the original float64 screen, whose candidates also include near-misses.
SCREEN = os.environ.get("WIEFERICH_SCREEN", "mitm")


class MitmScreen:
    """Exact screen: b = a*c (a over the first k primes, c over the rest); b is a Wieferich base for p iff
    X[a] = q_p(a) mod p equals Y[c] = -q_p(c) mod p.  The float64 dot products are integers < 2^45 (exact), then
    reduced mod p in int64; collisions are found by an exact per-row sort, so no tolerance is involved and every
    candidate is an exact zero of q_p(b).  Each candidate is still re-checked with pow(b, p-1, p*p)."""

    def __init__(self, R, bases, Ei, k=4):
        self.k = k
        rows = [tuple(r) for r in Ei.tolist()]
        A = sorted({r[:k] for r in rows if any(r[:k])})
        C = sorted({r[k:] for r in rows if any(r[k:])})
        ai = {t: i for i, t in enumerate(A)}
        ci = {t: i for i, t in enumerate(C)}
        self.EA = np.array(A, dtype=np.float64).T.copy()
        self.EC = np.array(C, dtype=np.float64).T.copy()
        self.pair2base, pa, pc = {}, set(), set()
        for b, r in zip(bases, rows):
            ia = ai[r[:k]] if any(r[:k]) else -1
            ic = ci[r[k:]] if any(r[k:]) else -1
            self.pair2base[(ia, ic)] = b
            if ic == -1:
                pa.add(ia)
            if ia == -1:
                pc.add(ic)
        assert len(self.pair2base) == len(bases)
        self.pureA = np.array(sorted(pa), dtype=np.int64)
        self.pureC = np.array(sorted(pc), dtype=np.int64)

    def screen(self, Qf, ps, plist, chunk=1024):
        k, cands, hits = self.k, [], []
        for c0 in range(0, len(plist), chunk):
            q, p = Qf[c0:c0 + chunk], ps[c0:c0 + chunk, None]
            X = np.remainder((q[:, :k] @ self.EA).astype(np.int64), p)
            Y = np.remainder(-(q[:, k:] @ self.EC).astype(np.int64), p)
            Z = np.concatenate([X, Y], axis=1)
            Z.sort(axis=1)
            flag = (Z[:, 1:] == Z[:, :-1]).any(axis=1)
            if len(self.pureA):
                flag |= (X[:, self.pureA] == 0).any(axis=1)
            if len(self.pureC):
                flag |= (Y[:, self.pureC] == 0).any(axis=1)
            for i in np.nonzero(flag)[0].tolist():
                pr, xr, yr = plist[c0 + i], X[i].tolist(), Y[i].tolist()
                d, found = {}, set()
                for ia, v in enumerate(xr):
                    d.setdefault(v, []).append(ia)
                for ic, v in enumerate(yr):
                    for ia in d.get(v, ()):
                        bb = self.pair2base.get((ia, ic))
                        if bb is not None:
                            found.add(bb)
                found.update(self.pair2base[(ia, -1)] for ia in self.pureA.tolist() if xr[ia] == 0)
                found.update(self.pair2base[(-1, ic)] for ic in self.pureC.tolist() if yr[ic] == 0)
                for bb in sorted(found):
                    cands.append([bb, pr])
                    if pow(bb, pr - 1, pr * pr) == 1:
                        hits.append([bb, pr])
        return cands, hits




def small_primes(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i :: i] = bytearray(len(range(i * i, n + 1, i)))
    return [i for i in range(n + 1) if s[i]]


def is_perfect_power(n):
    if n < 4:
        return False
    for k in range(2, n.bit_length() + 1):
        r = round(n ** (1.0 / k))
        for c in (r - 1, r, r + 1):
            if c > 1 and c ** k == n:
                return True
    return False


def smooth_bases(blo, bhi, B):
    """Non-perfect-power B-smooth bases blo <= b <= bhi, with their exponent matrix over the primes <= B."""
    R = small_primes(B)
    bases, rows = [], []
    for b in range(blo, bhi + 1):
        n, e = b, []
        for r in R:
            c = 0
            while n % r == 0:
                n //= r
                c += 1
            e.append(c)
        if n == 1 and not is_perfect_power(b):
            bases.append(b)
            rows.append(e)
    return R, bases, np.array(rows, dtype=np.float64)


def seg_primes(lo, hi, bp):
    """All primes lo <= p < hi; bp = odd base primes covering sqrt(hi); lo must exceed max(bp)."""
    lo_odd = lo if lo % 2 else lo + 1
    n = (hi - lo_odd + 1) // 2
    if n <= 0:
        return np.zeros(0, dtype=np.int64)
    s = np.ones(n, dtype=bool)
    for p in bp:
        pp = p * p
        if pp >= hi:
            break
        start = max(pp, ((lo_odd + p - 1) // p) * p)
        if start % 2 == 0:
            start += p
        if start >= hi:
            continue
        s[(start - lo_odd) // 2 :: p] = False
    return lo_odd + 2 * np.nonzero(s)[0].astype(np.int64)


def set_idle_priority():
    """Windows 'nice': IDLE_PRIORITY_CLASS for this process (children created afterwards inherit it).
    The types must be declared, or the pseudo-handle -1 is truncated and the call fails silently."""
    try:
        import ctypes
        k32 = ctypes.windll.kernel32
        k32.GetCurrentProcess.restype = ctypes.c_void_p
        k32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        k32.GetPriorityClass.argtypes = [ctypes.c_void_p]
        k32.SetPriorityClass(k32.GetCurrentProcess(), 0x40)
        return hex(k32.GetPriorityClass(k32.GetCurrentProcess()))
    except Exception as ex:
        return f"n/a ({ex})"


ES_CONTINUOUS, ES_SYSTEM_REQUIRED, ES_DISPLAY_REQUIRED = 0x80000000, 0x00000001, 0x00000002


def keep_awake(on=True):
    """Hold (on=True) or release (on=False) a Windows power request on the calling thread: system and display
    required, the way a video player keeps the screen on.

    While it is held, no idle timeout can turn the display off or sleep the machine, so it cannot drop into modern
    standby. On the ADMIN's laptop, standby halved sweep speed (references/host-mechanics.md). The request changes no
    power setting. Windows releases it when the thread clears it or the process exits. The power button, the cover and
    Start > Sleep still sleep the machine.

    Returns the read-back state as hex ('0x80000003' = held, '0x80000000' = released), 'failed (...)', or
    'n/a (...)' off Windows."""
    try:
        import ctypes
        k32 = ctypes.windll.kernel32
        k32.SetThreadExecutionState.argtypes = [ctypes.c_uint32]
        k32.SetThreadExecutionState.restype = ctypes.c_uint32
        flags = ES_CONTINUOUS | ((ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED) if on else 0)
        k32.SetThreadExecutionState(flags)
        now = k32.SetThreadExecutionState(flags)  # returns the state the first call set: a read-back check
        return hex(now) if now == flags else f"failed ({hex(now)})"
    except Exception as ex:
        return f"n/a ({ex})"


def peak_mem_mb():
    try:
        import ctypes
        from ctypes import wintypes

        class PMC(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                        ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                        ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]
        pmc = PMC()
        pmc.cb = ctypes.sizeof(PMC)
        k32 = ctypes.windll.kernel32
        k32.GetCurrentProcess.restype = ctypes.c_void_p
        f = k32.K32GetProcessMemoryInfo
        f.argtypes = [ctypes.c_void_p, ctypes.POINTER(PMC), wintypes.DWORD]
        ok = f(k32.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb)
        return round(pmc.PeakWorkingSetSize / 2**20, 1) if ok else "n/a (call failed)"
    except Exception as ex:
        return f"n/a ({ex})"


_STATE = {}


def init_worker(B, blo, bhi, max_hi):
    set_idle_priority()
    R, bases, E = smooth_bases(blo, bhi, B)
    _STATE["R"] = R
    _STATE["Rm"] = [mpz(r) for r in R]
    _STATE["bases"] = bases
    _STATE["ET"] = np.ascontiguousarray(E.T)
    _STATE["bp"] = [q for q in small_primes(int(math.isqrt(max_hi)) + 2) if q > 2]
    if SCREEN == "mitm":
        _STATE["mitm"] = MitmScreen(R, bases, E.astype(np.int64), int(os.environ.get("WIEFERICH_MITM_K", "4")))


def process_block(lo, hi, chunk=1024):
    t0 = time.perf_counter()
    R, Rm, bases, ET, bp = (_STATE[k] for k in ("R", "Rm", "bases", "ET", "bp"))
    ps = seg_primes(lo, hi, bp)
    plist = ps.tolist()
    n = len(plist)
    Q = np.empty((n, len(R)), dtype=np.int64)
    fermat_fail = []
    for i, p in enumerate(plist):
        pm = mpz(p)
        xs = powmod_base_list(Rm, pm - 1, pm * pm)
        if xs[0] % pm != 1:  # base-2 Fermat test of every sieved prime (sieve sanity)
            fermat_fail.append(p)
        Q[i, :] = [int(x // pm) for x in xs]
    h = hashlib.sha256(Q.tobytes()).hexdigest()
    cands, hits = [], []
    Qf = Q.astype(np.float64)
    invp = 1.0 / ps.astype(np.float64)
    if "mitm" in _STATE:
        cands, hits = _STATE["mitm"].screen(Qf, ps, plist, chunk)
    for c0 in (range(0, n, chunk) if "mitm" not in _STATE else ()):
        D = Qf[c0 : c0 + chunk] @ ET
        D *= invp[c0 : c0 + chunk, None]
        ii, jj = np.nonzero(np.abs(D - np.rint(D)) < TOL)
        for i, j in zip(ii.tolist(), jj.tolist()):
            p, b = plist[c0 + i], bases[j]
            cands.append([b, p])
            if pow(b, p - 1, p * p) == 1:
                hits.append([b, p])
    return {"lo": lo, "hi": hi, "n_primes": n,
            "first_p": plist[0] if n else None, "last_p": plist[-1] if n else None,
            "sha256_q": h, "cands": cands, "hits": hits, "fermat_fail": fermat_fail,
            "secs": round(time.perf_counter() - t0, 3), "pid": os.getpid(), "peak_mem_mb": peak_mem_mb(),
            **({"screen": "mitm"} if "mitm" in _STATE else {})}


def run_sweep(outdir, start, blk, nworkers, deadline_epoch, B, blo, bhi, max_hi):
    import multiprocessing as mp
    prio = set_idle_priority()
    awake = keep_awake(True) if os.environ.get("V3R1T4S_KEEP_AWAKE", "1") != "0" else "off (V3R1T4S_KEEP_AWAKE=0)"
    os.makedirs(outdir, exist_ok=True)
    bl_path, hit_path = os.path.join(outdir, "blocks.jsonl"), os.path.join(outdir, "hits.jsonl")
    done = set()
    if os.path.exists(bl_path):
        done = {json.loads(l)["lo"] for l in open(bl_path, encoding="utf-8") if l.strip()}
    with open(os.path.join(outdir, "pid.txt"), "w") as f:
        f.write(f"main_pid {os.getpid()} priority {prio} keep_awake {awake}\n")
    pool = mp.get_context("spawn").Pool(nworkers, initializer=init_worker, initargs=(B, blo, bhi, max_hi))
    inflight, nxt, t_start = {}, start, time.time()
    # bounded apply_async loop: Pool.imap would drain a lazy generator at once and ignore the deadline
    with open(bl_path, "a", encoding="utf-8") as bl, open(hit_path, "a", encoding="utf-8") as hf:
        while True:
            while time.time() < deadline_epoch and len(inflight) < 2 * nworkers and nxt + blk <= max_hi:
                if nxt not in done:
                    inflight[nxt] = pool.apply_async(process_block, (nxt, nxt + blk))
                nxt += blk
            if not inflight:
                break
            finished = [k for k, r in inflight.items() if r.ready()]
            if not finished:
                time.sleep(0.5)
                continue
            for k in finished:
                res = inflight.pop(k).get()
                bl.write(json.dumps(res) + "\n")
                bl.flush()
                for b, p in res["hits"]:
                    hf.write(json.dumps({"b": b, "p": p, "block_lo": res["lo"],
                                         "found_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}) + "\n")
                    hf.flush()
    pool.close()
    pool.join()
    if awake.startswith("0x"):
        keep_awake(False)
    print(json.dumps({"finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                      "wall_s": round(time.time() - t_start, 1)}))


def summarise(outdir, start, blk):
    L = [json.loads(l) for l in open(os.path.join(outdir, "blocks.jsonl"), encoding="utf-8") if l.strip()]
    by = {r["lo"]: r for r in L}
    c, contig = start, []
    while c in by:
        contig.append(by[c])
        c += blk
    return {"blocks_completed": len(L), "contiguous_from": start, "contiguous_to_exclusive": c,
            "contiguous_blocks": len(contig), "primes_in_contiguous_range": sum(r["n_primes"] for r in contig),
            "first_prime": contig[0]["first_p"] if contig else None,
            "last_prime_contiguous": contig[-1]["last_p"] if contig else None,
            "blocks_beyond_gap": len([lo for lo in by if lo >= c]),
            "primes_total_all_blocks": sum(r["n_primes"] for r in L),
            "screen_candidates": [cd for r in L for cd in r["cands"]],
            "exact_hits": [h for r in L for h in r["hits"]],
            "fermat_base2_failures": sum(len(r["fermat_fail"]) for r in L),
            "worker_pids": sorted({r["pid"] for r in L}),
            "max_peak_mem_mb": max((r["peak_mem_mb"] for r in L if isinstance(r["peak_mem_mb"], (int, float))), default=None),
            "mean_block_secs": round(sum(r["secs"] for r in L) / len(L), 1) if L else None}


def selftest(table, B=70, N=6, half=400_000):
    sys.path.insert(0, HERE)
    from fischer_parse import parse
    limit, rows, _ = parse(table)
    listed = {(b, p) for b, ps in rows.items() for p in ps}
    R, bases, _E = smooth_bases(1053, 10125, B)
    T = set(bases)
    pos = sorted((p, b) for (b, p) in listed if b in T and 1e12 < p < limit)
    pick = pos[:: max(1, len(pos) // N)][:N]
    print(f"table limit {limit:.6g}; B={B}: |R|={len(R)} |T|={len(T)}; listed smooth pairs in (1e12, limit): {len(pos)}")
    init_worker(B, 1053, 10125, int(limit * 1.02))
    found, unlisted, tp, ts = 0, [], 0, 0.0
    for p, b in pick:
        res = process_block(p - half, p + half)
        hs = {tuple(h) for h in res["hits"]}
        found += (b, p) in hs
        unlisted += [h for h in hs if h not in listed]
        tp, ts = tp + res["n_primes"], ts + res["secs"]
        print(f"  ({b}, {p}): primes={res['n_primes']} hits={sorted(hs)} cands={len(res['cands'])} "
              f"fermat_fail={len(res['fermat_fail'])} secs={res['secs']}")
    us = 1e6 * ts / max(tp, 1)
    print(f"found {found}/{len(pick)}, unlisted hits {unlisted}, {us:.2f} us/prime, {len(T)/us:.1f} bases/us, "
          f"peak_mem_mb {peak_mem_mb()}")
    ok = found == len(pick) and not unlisted and len(pick) > 0
    print("SELFTEST", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    mode, a = sys.argv[1], sys.argv[2:]
    if mode == "sweep":
        run_sweep(a[0], int(float(a[1])), int(float(a[2])), int(a[3]), float(a[4]), int(a[5]), int(a[6]), int(a[7]),
                  int(float(a[8])))
    elif mode == "summarise":
        print(json.dumps(summarise(a[0], int(float(a[1])), int(float(a[2]))), indent=1))
    elif mode == "selftest":
        sys.exit(0 if selftest(a[0], int(a[1]) if len(a) > 1 else 70, int(a[2]) if len(a) > 2 else 6) else 1)
    elif mode == "bench":
        print("priority", set_idle_priority())
        lo, B = int(float(a[0])), int(a[1]) if len(a) > 1 else 70
        init_worker(B, 1053, 10125, int(lo * 1.05))
        r = process_block(lo, lo + 20_000_000)
        print(json.dumps({k: v for k, v in r.items() if k != "cands"}))
        print("us_per_prime", round(1e6 * r["secs"] / max(r["n_primes"], 1), 2))
    else:
        sys.exit(__doc__)
