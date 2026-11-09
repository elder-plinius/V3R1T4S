"""Memetic tabu search in the skew-symmetric space on the GPU (island model), host side vectorised.
Each generation: every walker gets a child (binary-tournament parents from its island pool, uniform crossover on
the free half, per-bit mutation), runs one tabu episode on the GPU, and its episode best joins the island pool."""
import argparse, json, time
import numpy as np
from labsgpu import SkewGPU, energy_ref, energy_pure, is_skew, bits

def skew_expand_batch(H):
    W, NV = H.shape; n = NV - 1
    j = np.arange(1, n + 1); sign = np.where(j % 2 == 0, 1, -1).astype(np.int8)
    return np.concatenate([H, H[:, n - j] * sign], axis=1).astype(np.int8)

class Pools:
    """Per-island elite pools; uniqueness modulo the 4 skew-preserving symmetries via a 64-bit hash."""
    def __init__(self, islands, size, NV, rng):
        self.I, self.P, self.NV = islands, size, NV
        self.E = np.full((islands, size), np.iinfo(np.int64).max, dtype=np.int64)
        self.H = np.ones((islands, size, NV), dtype=np.int8)
        self.K = np.zeros((islands, size), dtype=np.uint64)
        self.cnt = np.zeros(islands, dtype=np.int64)
        self.wts = rng.integers(1, 2**63, size=NV, dtype=np.uint64) | np.uint64(1)
        self.alt = np.where(np.arange(NV) % 2 == 0, 1, -1).astype(np.int8)
    def keys(self, H):
        V = np.stack([H, -H, H * self.alt, -H * self.alt], axis=1)          # (m,4,NV)
        h = ((V > 0).astype(np.uint64) * self.wts).sum(axis=2, dtype=np.uint64)
        return h.min(axis=1)
    def add(self, isl, E, H):
        K = self.keys(H)
        for i in np.unique(isl):
            sel = isl == i
            Ei = np.concatenate([self.E[i, :self.cnt[i]], E[sel]]); Hi = np.concatenate([self.H[i, :self.cnt[i]], H[sel]])
            Ki = np.concatenate([self.K[i, :self.cnt[i]], K[sel]])
            order = np.lexsort((Ki, Ei)); Ei, Hi, Ki = Ei[order], Hi[order], Ki[order]
            _, first = np.unique(Ki, return_index=True); keep = np.sort(first)[:self.P]
            m = len(keep); self.cnt[i] = m
            self.E[i, :m], self.H[i, :m], self.K[i, :m] = Ei[keep], Hi[keep], Ki[keep]
    def best(self):
        i, j = np.unravel_index(np.argmin(self.E), self.E.shape); return int(self.E[i, j]), self.H[i, j]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--L', type=int, required=True)
    ap.add_argument('--walkers', type=int, default=492)
    ap.add_argument('--islands', type=int, default=12)
    ap.add_argument('--pool', type=int, default=64)
    ap.add_argument('--ep-mult', type=float, default=1.0)
    ap.add_argument('--tenure-frac', type=float, default=0.20, help='tenure_min = frac * NV (free variables)')
    ap.add_argument('--pmut', type=float, default=-1)
    ap.add_argument('--pcross', type=float, default=0.9)
    ap.add_argument('--prandom', type=float, default=0.02)
    ap.add_argument('--seconds', type=float, default=60)
    ap.add_argument('--target', type=int, default=0)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--out', type=str, default='')
    ap.add_argument('--heads', type=str, default='', help="'' = none; 'auto' = grid; or 'r1,r2,r3;r1,r2,r3;...'")
    ap.add_argument('--r1', type=str, default='26-30'); ap.add_argument('--r2', type=str, default='12-15')
    ap.add_argument('--r3', type=str, default='9-12')
    ap.add_argument('--exploit', type=float, default=0.7); ap.add_argument('--top-arms', type=int, default=6)
    ap.add_argument('--mode', type=str, default='tabu', choices=['tabu', 'saw'])
    ap.add_argument('--walk', type=int, default=0, help='SAW walk length (steps); default 8*NV')
    ap.add_argument('--seed-file', type=str, default='', help='0/1 lines (skew, length L): warm starts for a dedicated unfrozen arm')
    ap.add_argument('--seed-share', type=float, default=0.5, help='fraction of walkers on the warm-start arm')
    a = ap.parse_args()
    L, W = a.L, a.walkers; n = (L - 1) // 2; NV = n + 1
    pmut = a.pmut if a.pmut > 0 else 1.0 / NV
    rng = np.random.default_rng(a.seed)
    g = SkewGPU(L, W)
    rr = lambda t: range(int(t.split('-')[0]), int(t.split('-')[-1]) + 1)
    if a.heads == 'auto': heads = [(x, y, z) for x in rr(a.r1) for y in rr(a.r2) for z in rr(a.r3)]
    elif a.heads: heads = [tuple(int(v) for v in h.split(',')) for h in a.heads.split(';')]
    else: heads = []
    seeds = []
    if a.seed_file:
        for line in open(a.seed_file):
            b = line.strip()
            if len(b) == L:
                sq = np.array([1 if ch == '1' else -1 for ch in b], dtype=np.int8)
                if is_skew(sq): seeds.append(sq)
                else: print('seed skipped (not skew-symmetric)', flush=True)
        print(f"{len(seeds)} warm-start seeds, best E {min(energy_ref(x) for x in seeds) if seeds else None}", flush=True)
        if seeds and not heads: heads = [()]
        elif seeds: heads = [()] + heads             # arm 0 = warm-start arm, nothing frozen
    if heads:
        a.islands = len(heads)
        HB = np.zeros((len(heads), NV), dtype=np.int8); HP = np.zeros(len(heads), dtype=np.int64)
        for i, h in enumerate(heads):
            hb = []; sg = 1
            for r in h: hb += [sg] * r; sg = -sg
            if not h: HP[i] = 0; continue
            hb.append(sg); HB[i, :len(hb)] = hb; HP[i] = len(hb)
        assert HP.max() < NV
        print(f"{len(heads)} head arms, e.g. {heads[:3]} ... frozen prefix {HP.min()}..{HP.max()} of {NV} free variables", flush=True)
    isl = np.arange(W) % a.islands
    pools = Pools(a.islands, a.pool, NV, rng)
    def apply_heads(H, isl):
        if not heads: return H
        m = np.arange(NV)[None, :] < HP[isl][:, None]
        return np.where(m, HB[isl], H).astype(np.int8)
    def assign(gen):
        if not heads: return np.arange(W) % a.islands
        bestarm = np.array([pools.E[i, 0] if pools.cnt[i] else np.iinfo(np.int64).max for i in range(len(heads))])
        order = np.argsort(bestarm, kind='stable'); top = order[:a.top_arms]
        ks = int(a.seed_share * W) if seeds else 0
        k = int(a.exploit * (W - ks)) if gen > 0 else 0
        out = np.empty(W, dtype=np.int64); out[:ks] = 0
        if seeds: top = top[top != 0] if len(top[top != 0]) else top
        out[ks:ks + k] = top[np.arange(k) % len(top)]
        lo_arm = 1 if seeds and len(heads) > 1 else 0
        out[ks + k:] = rng.integers(lo_arm, len(heads), size=W - ks - k); return out
    isl = assign(0)
    if heads: g.set_frozen(HP[isl])
    if seeds:
        SH = np.stack([x[:NV] for x in seeds]); pools.add(np.zeros(len(SH), dtype=np.int64), np.array([energy_ref(x) for x in seeds], dtype=np.int64), SH.copy())
    pm1 = np.array([-1, 1], dtype=np.int8)
    H0 = apply_heads(rng.choice(pm1, size=(W, NV)), isl)
    if seeds:                                        # warm-start walkers begin from lightly mutated seeds
        on = np.where(isl == 0)[0]; base = SH[np.arange(len(on)) % len(SH)].copy()
        fl = rng.random(base.shape) < (1.0 / NV); fl[:1] = False; base[fl] = -base[fl]; H0[on] = base
    g.set_start(np.arange(W), skew_expand_batch(H0))
    t0 = time.time(); best_E = None; gen = 0; steps_total = 0
    outf = open(a.out, 'a') if a.out else None
    while True:
        if a.mode == 'saw':
            ep = a.walk if a.walk > 0 else 8 * NV
            tbl = 1 << max(6, int(np.ceil(np.log2(2 * ep + 2))))
            g.run_saw(ep, min(tbl, 16384), seed=int(rng.integers(1 << 31)))
        else:
            ep = max(8, int(a.ep_mult * L * rng.uniform(0.5, 1.5)))
            g.run(ep, max(1, int(a.tenure_frac * NV)), max(1, NV // 10), seed=int(rng.integers(1 << 31)))
        steps_total += ep * W
        bE, bS, _, _ = g.get()
        pools.add(isl, bE.astype(np.int64), bS[:, :NV].copy())
        w0 = int(np.argmin(bE))
        if best_E is None or int(bE[w0]) < best_E:
            s = bS[w0]; best_E = int(bE[w0]); best_s = s.copy()
            assert energy_ref(s) == best_E and is_skew(s)
            rec = dict(L=L, E=best_E, F=round(L * L / (2 * best_E), 6), t=round(time.time() - t0, 3), gen=gen,
                       steps=int(steps_total), head=(list(heads[isl[w0]]) if heads else None), seq=bits(s))
            print(f"[{rec['t']:8.2f}s gen {gen:6d}] L={L} E={best_E} F={rec['F']:.4f} head={rec['head']}", flush=True)
            if outf: outf.write(json.dumps(rec) + '\n'); outf.flush()
        gen += 1
        if (a.target and best_E <= a.target) or time.time() - t0 > a.seconds: break
        if gen % 50 == 0 and a.islands > 1 and not heads:
            bi = np.argmin(pools.E, axis=1)
            mig_E = pools.E[np.arange(a.islands), bi]; mig_H = pools.H[np.arange(a.islands), bi]
            pools.add((np.arange(a.islands) + 1) % a.islands, mig_E, mig_H.copy())
        isl = assign(gen)
        if heads: g.set_frozen(HP[isl])
        cnt = pools.cnt[isl]
        def tour():
            i = (rng.random(W) * np.maximum(cnt, 1)).astype(np.int64); j = (rng.random(W) * np.maximum(cnt, 1)).astype(np.int64)
            Ei, Ej = pools.E[isl, i], pools.E[isl, j]; pick = np.where(Ei <= Ej, i, j)
            return pools.H[isl, pick]
        p1, p2 = tour(), tour()
        cross = (rng.random(W) < a.pcross)[:, None] & (rng.random((W, NV)) < 0.5)
        child = np.where(cross, p2, p1).astype(np.int8)
        flip = rng.random((W, NV)) < pmut; child[flip] = -child[flip]
        rnd = (rng.random(W) < a.prandom) | (cnt == 0)
        if rnd.any(): child[rnd] = rng.choice(pm1, size=(int(rnd.sum()), NV))
        g.set_start(np.arange(W), skew_expand_batch(apply_heads(child, isl)))
    el = time.time() - t0
    assert energy_pure(best_s) == best_E
    summ = dict(L=L, best_E=best_E, best_F=round(L * L / (2 * best_E), 6), seconds=round(el, 2), gens=gen,
                steps=int(steps_total), steps_per_s=int(steps_total / el), args=vars(a), seq=bits(best_s), final=True)
    print(json.dumps({k: v for k, v in summ.items() if k not in ('seq', 'args')}), flush=True)
    if outf: outf.write(json.dumps(summ) + '\n'); outf.close()

if __name__ == '__main__':
    main()
