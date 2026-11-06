#!/usr/bin/env python3
"""Multi-stage stitch: build an all-glider (gen-0 gliders only) synthesis of the input from its
Shinjuku component path (later-stage gliders rewound so they arrive after the previous stage settles),
then add the delayed sweep1g glider. Writes RLE; verify separately with verify_synthesis.py."""
import sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data', 'Shinjuku'))
from shinjuku import lt
from shinjuku.transcode import realise_comp
G = lt.pattern("bo$2bo$3o"); GPH = [G[i] for i in range(4)]
ROTS = ["identity", "rot90", "rot180", "rot270"]
TFS = ["identity", "rot90", "rot180", "rot270", "flip_x", "flip_y", "swap_xy", "swap_xy_flip"]
def norm(p):
    r = p.getrect(); return p(-r[0], -r[1])

def build(lines, step, pre=0):
    P = lt.pattern(); T = 0
    for i, line in enumerate(lines):
        base, gs = realise_comp(line, separate=True)
        if base.population == 0:
            assert i == 0, "empty base after stage 0"
            P = gs[-pre].s if pre else gs.s; T = step + pre; continue
        X = P[T]
        done = False
        for k in range(8):
            Y = X[k]
            for tf in TFS:
                Bt = base(tf); rb = Bt.getrect(); ry = Y.getrect()
                dx, dy = ry[0] - rb[0], ry[1] - rb[1]
                if Bt(dx, dy) == Y:
                    P = P + gs(tf)(dx, dy)[-(T + k)].s
                    T = T + k + step; done = True; break
            if done: break
        assert done, ("stage", i, "no match", X.apgcode)
    X = P[T]
    assert X[1] == X, "input not still at T"
    return P, T

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-apg", required=True); ap.add_argument("--rot", type=int, required=True)
    ap.add_argument("--lane", type=int, required=True); ap.add_argument("--ph", type=int, required=True)
    ap.add_argument("--target", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--paths", default=os.path.join(os.path.dirname(__file__), '..', 'attempts', 'multistage', 'paths.json'))
    ap.add_argument("--step", type=int, default=512); ap.add_argument("--pre", type=int, default=0); ap.add_argument("--margin", type=int, default=30)
    a = ap.parse_args()
    info = json.load(open(a.paths))[a.in_apg]
    S, T = build(info["lines"], a.step, a.pre)
    X = S[T]
    assert X.apgcode == a.in_apg, ("built", X.apgcode)
    base = norm(lt.pattern(a.in_apg)(ROTS[a.rot])); x, y, w, h = base.getrect()
    D = w + h + 8
    g = GPH[a.ph](a.lane - D, -D)
    assert (base + g)[4 * D + 256].apgcode == a.target
    for tf in TFS:
        Bt = base(tf); gt = g(tf)
        dx = X.getrect()[0] - Bt.getrect()[0]; dy = X.getrect()[1] - Bt.getrect()[1]
        if Bt(dx, dy) != X: continue
        gt = gt(dx, dy)
        r0 = gt.getrect(); r4 = gt[4].getrect()
        ux, uy = r4[0] - r0[0], r4[1] - r0[1]
        back = T // 4 + a.margin
        g0 = gt(-ux * back, -uy * back)
        full = S + g0
        res = full[T + 4 * (back + D) + 512]
        ok = res[1] == res and res.apgcode == a.target
        print(tf, "shinjuku_cost", info["cost"], "result", res.apgcode, "ok", ok)
        if ok:
            open(a.out, "w").write(full.rle_string()); print("wrote", a.out, "pop0", full.population); return
    print("no orientation worked"); sys.exit(1)
main()
