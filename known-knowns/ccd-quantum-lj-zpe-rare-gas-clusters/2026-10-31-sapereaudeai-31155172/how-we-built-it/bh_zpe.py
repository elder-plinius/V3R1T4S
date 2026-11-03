"""Lens landscape: ZPE-ranked basin-hopping on the classical LJ surface.

Every quench is on the classical E_LJ surface (the convention: a classical minimum plus its harmonic ZPE); the
Metropolis acceptance uses E_sp of the quenched minimum for one species. Distinct minima are counted; the best
minimum per species is tracked; any minimum whose fast E_sp is within reach of the table bar is Newton-polished
and written with 17 digits for the decimal checker.

Usage: python -I bh_zpe.py --tools DIR --bars FILE --n N --species Ne --minutes M --out DIR --rng SEED [--seed FILE ...]
"""
import argparse, ctypes, json, os, sys, time
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--tools", required=True)
ap.add_argument("--bars", required=True)
ap.add_argument("--n", type=int, required=True)
ap.add_argument("--species", default="Ne")
ap.add_argument("--minutes", type=float, default=10)
ap.add_argument("--out", required=True)
ap.add_argument("--rng", type=int, default=1)
ap.add_argument("--T", type=float, default=0.8)
ap.add_argument("--seed", action="append", default=[])
ap.add_argument("--reset", type=int, default=400)
a = ap.parse_args()
sys.path.insert(0, a.tools)
import ljfast as L

try:  # low priority (Windows BELOW_NORMAL_PRIORITY_CLASS)
    _k = ctypes.windll.kernel32
    _k.GetCurrentProcess.restype = ctypes.c_void_p
    _k.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
    _k.SetPriorityClass(_k.GetCurrentProcess(), 0x4000)
except Exception:
    pass


def peak_mb():
    try:
        class PMC(ctypes.Structure):
            _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong), ("PeakWorkingSetSize", ctypes.c_size_t),
                        ("WorkingSetSize", ctypes.c_size_t), ("a", ctypes.c_size_t), ("b", ctypes.c_size_t),
                        ("c", ctypes.c_size_t), ("d", ctypes.c_size_t), ("PagefileUsage", ctypes.c_size_t),
                        ("PeakPagefileUsage", ctypes.c_size_t)]
        p = PMC(); p.cb = ctypes.sizeof(PMC)
        k = ctypes.windll.kernel32
        k.GetCurrentProcess.restype = ctypes.c_void_p
        k.K32GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32]
        k.K32GetProcessMemoryInfo(k.GetCurrentProcess(), ctypes.byref(p), p.cb)
        return p.PeakWorkingSetSize / 2**20
    except Exception:
        return -1.0


os.makedirs(a.out, exist_ok=True)
tag = "N%d_%s_r%d" % (a.n, a.species, a.rng)
open(os.path.join(a.out, tag + ".pid"), "w").write("%d\n" % os.getpid())
bars = {}
for line in open(a.bars):
    t = line.split("\t")
    if t[0] == str(a.n):
        bars[t[1]] = float(t[2])
rng = np.random.default_rng(a.rng)
N = a.n
Rc = 1.3 * N ** (1 / 3) + 1.0


def random_start():
    x = rng.uniform(-1, 1, (N * 4, 3))
    x = x[(x ** 2).sum(1) < 1][:N] * (0.65 * N ** (1 / 3))
    return x


def contain(x):
    x = x.reshape(-1, 3) - x.reshape(-1, 3).mean(0)
    r = np.sqrt((x ** 2).sum(1))
    far = r > Rc
    x[far] *= (0.8 * Rc / r[far])[:, None]
    return x


def move(x, step):
    x = x.reshape(-1, 3).copy()
    if rng.random() < 0.25:   # surface move: relocate the least-bound atom onto the surface
        d = np.sqrt(((x[:, None] - x[None]) ** 2).sum(-1)); np.fill_diagonal(d, np.inf)
        ei = (4 * (d ** -12 - d ** -6)).sum(1)
        i = int(np.argmax(ei))
        c = x.mean(0); rmax = np.sqrt(((x - c) ** 2).sum(1)).max()
        u = rng.normal(size=3); u /= np.sqrt(u @ u)
        x[i] = c + u * (rmax + 0.2)
    else:
        x += rng.uniform(-step, step, x.shape)
    return contain(x)


seeds = [L.read_xyz(s) for s in a.seed] or [random_start()]
x, p = L.quench_check(contain(seeds[0]))
cur_x, cur_e = x, p["E_" + a.species]
best = {sp: (p["E_" + sp], x.copy(), dict(p)) for sp in ("Xe", "Ar", "Ne")}
seen = {}
step = 0.4
acc = 0
t0 = time.time(); last_ck = t0
nq = nbad = 0
since_improve = 0
written = {}


def key(p):
    return (round(p["E_LJ"], 5), round(p["E_Ne"], 4))


def checkpoint(final=False):
    summ = {"tag": tag, "N": N, "species_accept": a.species, "T": a.T, "quenches": nq, "rejected_not_minimum": nbad,
            "distinct_minima": len(seen), "elapsed_s": round(time.time() - t0, 1), "step": round(step, 3),
            "peak_working_set_MB": round(peak_mb(), 1), "final": final, "best": {}}
    for sp in ("Xe", "Ar", "Ne"):
        e, bx, bp = best[sp]
        summ["best"][sp] = {"E_sp_fast": e, "E_LJ": bp["E_LJ"], "bar": bars.get(sp), "bar_minus_E": (bars[sp] - e) if sp in bars else None}
    json.dump(summ, open(os.path.join(a.out, tag + ".json"), "w"), indent=1)
    # lowest 30 distinct minima by the acceptance species
    lst = sorted(seen.values(), key=lambda q: q["E_" + a.species])[:30]
    with open(os.path.join(a.out, tag + "_lowest.tsv"), "w") as f:
        f.write("E_LJ\tE_Xe\tE_Ar\tE_Ne\tminnz\n")
        for q in lst:
            f.write("%.6f\t%.6f\t%.6f\t%.6f\t%.4e\n" % (q["E_LJ"], q["E_Xe"], q["E_Ar"], q["E_Ne"], q["minnz"]))


for s in seeds:
    xs, ps = L.quench_check(contain(s))
    if ps["ok"]:
        seen[key(ps)] = ps
        for sp in best:
            if ps["E_" + sp] < best[sp][0]:
                best[sp] = (ps["E_" + sp], xs.copy(), dict(ps))
seed_pool = [L.quench_check(contain(s))[0] for s in seeds]

while time.time() - t0 < a.minutes * 60:
    xn, pn = L.quench_check(move(cur_x, step))
    nq += 1
    if not pn["ok"]:
        nbad += 1
        continue
    k = key(pn)
    seen.setdefault(k, pn)
    improved = False
    for sp in best:
        if pn["E_" + sp] < best[sp][0] - 1e-7:
            best[sp] = (pn["E_" + sp], xn.copy(), dict(pn))
            if sp == a.species:
                improved = True
            if sp in bars and bars[sp] - pn["E_" + sp] > 2e-4:   # within reach: polish and write for the checker
                xp, ep, gp = L.newton_polish(xn)
                pp = L.esp_all(xp)
                if pp["maxzero"] < 1e-6 and pp["minnz"] > 1e-6 and bars[sp] - pp["E_" + sp] > 3e-4:
                    fn = os.path.join(a.out, "cand_%s_%s.xyz" % (tag, sp))
                    L.write_xyz(fn, xp, "N=%d %s E_LJ=%.9f E_%s=%.9f bar=%s gradnorm=%.2e (fast evaluator; judge with check_lj_zpe.py)" % (N, sp, pp["E_LJ"], sp, pp["E_" + sp], bars[sp], gp))
                    written[sp] = pp["E_" + sp]
    since_improve = 0 if improved else since_improve + 1
    en = pn["E_" + a.species]
    if en < cur_e or rng.random() < np.exp(-(en - cur_e) / a.T):
        cur_x, cur_e = xn, en
        acc += 1
    if nq % 50 == 0:
        rate = acc / 50.0
        step = min(0.9, step * 1.1) if rate > 0.5 else max(0.15, step / 1.1)
        acc = 0
    if since_improve > a.reset:   # restart from a seed or the best so far, perturbed
        base = best[a.species][1] if rng.random() < 0.5 else seed_pool[rng.integers(len(seed_pool))]
        cur_x, pr = L.quench_check(move(base, 0.5))
        cur_e = pr["E_" + a.species] if pr["ok"] else np.inf
        since_improve = 0
    if time.time() - last_ck > 60:
        checkpoint(); last_ck = time.time()
checkpoint(final=True)
print(json.dumps(json.load(open(os.path.join(a.out, tag + ".json")))))
