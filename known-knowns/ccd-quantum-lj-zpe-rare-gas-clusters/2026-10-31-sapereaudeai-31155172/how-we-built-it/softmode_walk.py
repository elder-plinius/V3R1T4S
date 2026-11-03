"""Lens representation: search in normal-mode coordinates.

From each seed minimum (the table's posted structures, Newton-polished), step along its softest normal modes
(single modes and random pairs of the softest six) with several amplitudes, quench on the classical E_LJ surface,
and keep a frontier of distinct minima ranked by E_sp for one species; always expand the lowest unexpanded one
(a best-first walk through soft-mode neighbours). Records every species' best and writes any minimum within
reach of the table bar with 17 digits for the decimal checker.

Usage: python -I softmode_walk.py --tools DIR --bars FILE --species Ne --minutes M --out DIR --sizes 31,32 --points DIR
"""
import argparse, ctypes, heapq, json, os, sys, time
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--tools", required=True)
ap.add_argument("--bars", required=True)
ap.add_argument("--points", required=True)
ap.add_argument("--good", required=True, help="file listing labels whose point files match the table")
ap.add_argument("--sizes", required=True)
ap.add_argument("--species", default="Ne")
ap.add_argument("--minutes", type=float, default=10)
ap.add_argument("--out", required=True)
ap.add_argument("--rng", type=int, default=7)
a = ap.parse_args()
sys.path.insert(0, a.tools)
import ljfast as L

try:
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
sizes = [int(s) for s in a.sizes.split(",")]
tag = "S%s_%s" % ("-".join(map(str, sizes)), a.species)
open(os.path.join(a.out, tag + ".pid"), "w").write("%d\n" % os.getpid())
good = set(open(a.good).read().split())
allbars = {}
for line in open(a.bars):
    t = line.rstrip("\n").split("\t")
    if t[0].isdigit():
        allbars.setdefault(int(t[0]), {})[t[1]] = float(t[2])
rng = np.random.default_rng(a.rng)
AMPS = (0.35, 0.7, 1.1)
summary = {"tag": tag, "species_rank": a.species, "sizes": {}}
t_all = time.time()
per_size = a.minutes * 60 / len(sizes)


def key(p):
    return (round(p["E_LJ"], 5), round(p["E_Ne"], 4))


for N in sizes:
    t0 = time.time()
    bars = allbars[N]
    seeds = [l for l in sorted(good) if l[:-1] == str(N)]
    reg = {}      # key -> (props, x)
    heap = []     # (E_sp, counter, key)
    expanded = set()
    cnt = 0
    nq = nbad = 0
    best = {sp: (np.inf, None, None) for sp in ("Xe", "Ar", "Ne")}

    def add(x, p, src):
        global cnt
        k = key(p)
        if k in reg:
            return False
        reg[k] = (p, x, src)
        cnt += 1
        heapq.heappush(heap, (p["E_" + a.species], cnt, k))
        for sp in best:
            if p["E_" + sp] < best[sp][0]:
                best[sp] = (p["E_" + sp], x.copy(), dict(p))
                if bars.get(sp) is not None and bars[sp] - p["E_" + sp] > 2e-4:
                    xp, ep, gp = L.newton_polish(x)
                    pp = L.esp_all(xp)
                    if pp["maxzero"] < 1e-6 and pp["minnz"] > 1e-6 and bars[sp] - pp["E_" + sp] > 3e-4:
                        L.write_xyz(os.path.join(a.out, "cand_N%d_%s.xyz" % (N, sp)), xp,
                                    "N=%d %s E_LJ=%.9f E_%s=%.9f bar=%s gradnorm=%.2e (fast evaluator; judge with check_lj_zpe.py)" % (N, sp, pp["E_LJ"], sp, pp["E_" + sp], bars[sp], gp))
        return True

    for s in seeds:
        x, e, g = L.newton_polish(L.read_xyz(os.path.join(a.points, s)))
        p = L.esp_all(x)
        add(x, p, "seed " + s)
    while heap and time.time() - t0 < per_size:
        e0, _, k = heapq.heappop(heap)
        if k in expanded:
            continue
        expanded.add(k)
        p0, x0, src = reg[k]
        lam, V = L.modes(x0)
        idx = np.argsort(np.abs(lam))[6:]
        idx = idx[np.argsort(lam[idx])][:8]          # the 8 softest nonzero modes
        moves = []
        for j in idx:
            v = V[:, j].reshape(-1, 3)
            v = v / np.sqrt((v ** 2).sum(1)).max()
            for amp in AMPS:
                for sg in (1, -1):
                    moves.append(sg * amp * v)
        for _ in range(12):                           # random pairs among the 6 softest
            j1, j2 = rng.choice(idx[:6], 2, replace=False)
            v = (rng.normal() * V[:, j1] + rng.normal() * V[:, j2]).reshape(-1, 3)
            v = v / np.sqrt((v ** 2).sum(1)).max()
            moves.append(rng.choice(AMPS) * v)
        for dv in moves:
            if time.time() - t0 >= per_size:
                break
            xn, pn = L.quench_check(x0.reshape(-1, 3) + dv)
            nq += 1
            if not pn["ok"]:
                nbad += 1
                continue
            add(xn, pn, "from " + str(k))
    rec = {"seeds": seeds, "quenches": nq, "rejected_not_minimum": nbad, "distinct_minima": len(reg),
           "expanded": len(expanded), "elapsed_s": round(time.time() - t0, 1), "best": {}}
    for sp in best:
        e, bx, bp = best[sp]
        rec["best"][sp] = {"E_sp_fast": e, "E_LJ": bp["E_LJ"] if bp else None, "bar": bars.get(sp),
                           "bar_minus_E": (bars[sp] - e) if sp in bars else None}
    summary["sizes"][N] = rec
    summary["peak_working_set_MB"] = round(peak_mb(), 1)
    json.dump(summary, open(os.path.join(a.out, tag + ".json"), "w"), indent=1)
    lst = sorted((v[0] for v in reg.values()), key=lambda q: q["E_" + a.species])[:20]
    with open(os.path.join(a.out, "%s_N%d_lowest.tsv" % (tag, N)), "w") as f:
        f.write("E_LJ\tE_Xe\tE_Ar\tE_Ne\tminnz\n")
        for q in lst:
            f.write("%.6f\t%.6f\t%.6f\t%.6f\t%.4e\n" % (q["E_LJ"], q["E_Xe"], q["E_Ar"], q["E_Ne"], q["minnz"]))
summary["total_s"] = round(time.time() - t_all, 1)
json.dump(summary, open(os.path.join(a.out, tag + ".json"), "w"), indent=1)
print(json.dumps(summary))
