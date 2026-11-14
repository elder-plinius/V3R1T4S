#!/usr/bin/env python3
"""1G sweep: hit each input still life with one glider on every lane/phase from 4 directions.
Emit strict single-object still-life (or p2) outputs: in_apg in_cost rot lane phase period out_apg."""
import sys, os, time, argparse
sys.path.insert(0, os.path.dirname(__file__))
import lifelib
lt = lifelib.load_rules('b3s23').lifetree(n_layers=1, memory=int(os.environ.get('LT_MEM','150')))
from strict_exact import is_strict_cells
G = lt.pattern("bo$2bo$3o")
GPH = [G[i] for i in range(4)]
ROTS = ["identity", "rot90", "rot180", "rot270"]

def norm(p):
    r = p.getrect(); return p(-r[0], -r[1])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", required=True)  # lines: cost apgcode
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    lines = [l.split() for l in open(a.inputs) if l.strip()]
    lines = lines[a.shard::a.nshards]
    done = set()
    if os.path.exists(a.out):
        for l in open(a.out):
            if l.startswith("#done "): done.add(l.split()[1])
    f = open(a.out, "a"); t0 = time.time(); n = 0
    for cost, apg in lines:
        if apg in done: continue
        base0 = lt.pattern(apg)
        if not is_strict_cells([tuple(map(int, c)) for c in base0.coords()]):
            f.write(f"#done {apg}\n"); continue
        seen = set()
        for ri, rot in enumerate(ROTS):
            base = norm(base0(rot)); x, y, w, h = base.getrect()
            D = w + h + 8
            for k in range(-(h + 3), w + 4):
                for ph in range(4):
                    g = GPH[ph](k - D, -D)
                    p = (base + g)
                    gens = 4 * D + 256
                    q = p[gens]
                    n += 1
                    if q.population == 0: continue
                    q1 = q[1]
                    per = 1 if q1 == q else (2 if q[2] == q else 0)
                    if not per: continue
                    if q == base: continue
                    cells = [tuple(map(int, c)) for c in q.coords()]
                    if per == 1 and not is_strict_cells(cells): continue
                    oa = q.apgcode
                    if oa in seen: continue
                    seen.add(oa)
                    f.write(f"{apg} {cost} {ri} {k} {ph} {per} {oa}\n")
        f.write(f"#done {apg}\n"); f.flush()
    print(f"trials={n} t={time.time()-t0:.1f}s", flush=True)

if __name__ == "__main__":
    main()
