"""Lens object-as-data — known positives for the p1 base set (70-smooth, non-perfect-power, 10126..65536).

The partial win p1 needs only p > 1e12 (no table covers these bases), and the pair density per prime is ~1/p, so the
cell just above 1e12 is ~4.8x richer than the full-win frontier at 4.8e12.  Before sweeping it, prove the pipeline on
THIS base set: (1) direct search finds Wieferich pairs for sampled bases at 65536 < p < 3e6 (where q_p is defined for
every base); (2) the sweep pipeline, built for the whole p1 base set, must return exactly the brute-force pair set in
windows around them (every base, every prime: no miss, no extra); (3) one real-size block just BELOW 1e12 (not
p1-eligible, so not attack output) for time and peak memory.
"""
import sys, os, time, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wieferich_sweep as ws

print("priority", ws.set_idle_priority())
R, bases, E = ws.smooth_bases(10126, 65536, 70)
print(f"p1 base set: B=70 |R|={len(R)} |T|={len(bases)} (non-perfect-power 70-smooth in 10126..65536)")
P = [p for p in ws.small_primes(3_000_000) if p > 65536]
sample = bases[:: max(1, len(bases) // 40)][:40]
t0 = time.time()
found = []
for b in sample:
    for p in P:
        if pow(b, p - 1, p * p) == 1:
            found.append((b, p))
print(f"direct search: {len(sample)} bases x {len(P)} primes in (65536, 3e6): {len(found)} pairs {found[:12]} "
      f"({time.time()-t0:.1f} s)")
ws.init_worker(70, 10126, 65536, 4_000_000)
HALF = 15_000
ok_all = True
for b, p in found[:3]:
    lo, hi = max(65537, p - HALF), p + HALF
    res = ws.process_block(lo, hi)
    pipe = {tuple(h) for h in res["hits"]}
    primes = ws.seg_primes(lo, hi, ws._STATE["bp"]).tolist()
    brute = {(bb, pp) for pp in primes for bb in bases if pow(bb, pp - 1, pp * pp) == 1}
    same = pipe == brute
    ok_all &= same and (b, p) in pipe
    print(f"  window [{lo},{hi}) around ({b},{p}): primes={res['n_primes']} pipeline={sorted(pipe)} brute={sorted(brute)} "
          f"identical={same}")
print("P1_PIPELINE_SELFTEST", "PASS" if ok_all and found else "FAIL")
sys.stdout.flush()
ws.init_worker(70, 10126, 65536, int(1.05e12))
lo = 1_000_000_000_000 - 20_000_000
r = ws.process_block(lo, lo + 20_000_000)
print("bench below 1e12:", json.dumps({k: v for k, v in r.items() if k not in ("cands",)}))
print("us_per_prime", round(1e6 * r["secs"] / r["n_primes"], 2), "bases_per_us", round(len(bases) / (1e6 * r["secs"] / r["n_primes"]), 1))
