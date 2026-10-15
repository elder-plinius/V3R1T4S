"""Exact local search on the integer pixel-map grid, seeded from the best surrogate point.

State: integer d (pixel map x = v + off + m*d). Each iteration: the gradient of a soft (tanh, temperature beta)
surrogate margin L_c - L_t at the current integer point proposes move sets (top-k pixels by |grad|, random subsets of
the top pixels, random flips); all candidates are scored EXACTLY with the validated integer model (bnn4864.py) and
with the soft margin M. Score F = G + mu*M (G = exact integer lead of class c over the true class).
Simulated-annealing acceptance on F; restart from the best after a stall. Checkpoint every <= 60 s.

Usage: python -I localsearch.py --data DATA --inst model_48_idx_6371_eps_3 --secs 900 --out DIR --init ckpt.json
       [--cls C] [--seed 0] [--beta 3] [--mu 0.5]
"""
import argparse, glob, json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'exact-solver', 'code'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'surrogate-attack', 'code'))
from bnn4864 import Net, parse_box, rebox, convert_d
from surrogate import build
import jax, jax.numpy as jnp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--eps', type=int, default=None); ap.add_argument('--data', required=True); ap.add_argument('--inst', required=True); ap.add_argument('--secs', type=float, default=600)
    ap.add_argument('--out', required=True); ap.add_argument('--init', default=None); ap.add_argument('--cls', type=int, default=None)
    ap.add_argument('--seed', type=int, default=0); ap.add_argument('--beta', default='3,3,3,3'); ap.add_argument('--hard', default='1,0,0,0'); ap.add_argument('--mu', type=float, default=0.5)
    ap.add_argument('--ncand', type=int, default=48); ap.add_argument('--inner-eps', type=int, default=None); ap.add_argument('--lam', type=float, default=3.0); ap.add_argument('--kick', type=int, default=0); ap.add_argument('--stall', type=int, default=60); ap.add_argument('--focus', type=int, default=-1); ap.add_argument('--focus-unit', type=int, default=-1); ap.add_argument('--mu2', type=float, default=0.1); ap.add_argument('--temp', type=float, default=1.0)
    a = ap.parse_args()
    tag = a.inst.split('_')[1]
    net = Net(glob.glob(f'{a.data}/onnx/3_{tag}_*.onnx.gz')[0]); S = net.S
    lo, hi, tgt = parse_box(f'{a.data}/vnnlib/{a.inst}.00000.vnnlib.gz', (S, S, 3))
    base_eps = int(a.inst.split('_eps_')[1]); lo0, hi0 = lo, hi
    cur_eps = a.eps if a.eps is not None else base_eps
    if cur_eps != base_eps: lo, hi = rebox(lo0, hi0, base_eps, cur_eps)
    net.setup_box(lo, hi, 9)
    def load_d(j):
        dd = np.asarray(j['d'], dtype=np.int64).reshape(S, S, 3); e = int(j.get('eps', int(j['inst'].split('_eps_')[1])))
        return dd if e == cur_eps else convert_d(dd, rebox(lo0, hi0, base_eps, e) if e != base_eps else (lo0, hi0), (lo, hi))
    pre = build(net)
    v = jnp.asarray(net.v + net.off, jnp.float32); m = np.float32(net.m)
    _, qs = pre(v[None], jnp.ones(4), 1.0, 0.0)
    sig = jnp.asarray([float(jnp.std(q)) for q in qs], jnp.float32)
    rng = np.random.default_rng(a.seed)
    os.makedirs(a.out, exist_ok=True)
    ck_path = os.path.join(a.out, f'{a.inst}.json')
    d = np.zeros((S, S, 3), np.int64); cls = a.cls
    for p in [a.init, ck_path]:
        if p and os.path.exists(p):
            j = json.load(open(p))
            if j.get('d') is not None and (p == a.init or j['G'] > -10**8):
                d = load_d(j)
                if cls is None: cls = j['cls']
    FOC = {}
    def exactG(D):
        o = net.forward(D); L = o['L']; Lo = L.copy(); Lo[:, tgt] = -1e9
        if FOC:   # exact signed distance (u units) of the focus dense unit to its threshold, toward the wanted side
            j = FOC['j']; q = np.where(net.posd[j], o['u'][:, j] - net.Td[j], net.Td[j] - o['u'][:, j])
            FOC['last'] = FOC['sgn'] * q
        return L[:, cls] - L[:, tgt], Lo.max(1) - L[:, tgt], Lo.argmax(1)
    if cls is None:
        _, _, am = exactG(d[None]); cls = int(am[0])
    BV = jnp.asarray([float(t) for t in a.beta.split(',')], jnp.float32); HV = jnp.asarray([float(t) for t in a.hard.split(',')], jnp.float32)
    def soft(dd):
        L, _ = pre((v + m * dd)[None], sig, BV, HV)
        return L[cls] - L[tgt]
    gfun = jax.jit(jax.value_and_grad(soft))
    sfun = jax.jit(jax.vmap(soft))
    dmin, dmax = net.dmin, net.dmax
    if a.focus >= 0:
        o = net.forward(d[None]); dw = net.d2[:, cls] - net.d2[:, tgt]; h = o['hd'][0]
        wrong = np.nonzero((dw != 0) & (h != np.sign(dw)))[0]
        dist = np.abs(o['u'][0] - net.Td)[wrong]
        j = int(wrong[np.argsort(dist)[a.focus]]) if a.focus_unit < 0 else a.focus_unit; FOC.update(j=j, sgn=float(np.sign(dw[j])))
        print('focus unit', j, 'signed distance (u units)', float(np.where(net.posd[j], o['u'][0][j] - net.Td[j], net.Td[j] - o['u'][0][j]) * np.sign(dw[j])), flush=True)
    Gc, Gall, _ = exactG(d[None]); G = int(Gc[0]); M = float(gfun(jnp.asarray(d, jnp.float32))[0])
    # box-penalty homotopy: search in the (wider) current box, penalise every pixel outside the inner box
    INN = None
    if a.inner_eps is not None:
        lo_in, hi_in = (lo0, hi0) if a.inner_eps == base_eps else rebox(lo0, hi0, base_eps, a.inner_eps)
        INN = dict(lo=lo_in, hi=hi_in, best=-10**9)
    vv, oo = net.v + net.off, net.m
    def pen(D):
        if INN is None: return np.zeros(len(D))
        x = vv + oo * D
        return (np.maximum(0, x - INN['hi']) + np.maximum(0, INN['lo'] - x)).reshape(len(D), -1).sum(1)
    def lam_now():
        return a.lam * min(1.0, (time.time() - t0) / (0.7 * a.secs)) if INN is not None else 0.0
    t0 = time.time()
    F = G + a.mu * M + (a.mu2 * min(float(FOC['last'][0]), 0) if FOC else 0)
    best = dict(G=int(Gall[0]), Gc=G, d=d.copy(), cls=cls)
    print(f'inst {a.inst} tgt {tgt} cls {cls} start Gc={G} Gall={int(Gall[0])} M={M:.2f}', flush=True)
    last_ck = 0; it = 0; stall = 0; nacc = 0
    def save():
        json.dump(dict(inst=a.inst, eps=cur_eps, tgt=tgt, G=int(best['G']), Gc=int(best['Gc']), cls=int(best['cls']), pw=9,
                       d=best['d'].astype(int).reshape(-1).tolist(), elapsed=round(time.time() - t0, 1), iters=it,
                       accepted=nacc), open(ck_path + '.tmp', 'w'))
        os.replace(ck_path + '.tmp', ck_path)
    while time.time() - t0 < a.secs:
        it += 1
        _, gr = gfun(jnp.asarray(d, jnp.float32)); gr = np.asarray(gr, np.float64)
        step = np.sign(gr).astype(np.int64)
        if INN is not None:
            xc = vv + oo * d; outside = (xc > INN['hi']) | (xc < INN['lo'])
            step = np.where(outside, np.where(xc > INN['hi'], -1, 1), step)
            gr = np.where(outside, np.maximum(np.abs(gr), lam_now() * 0.5 * (np.maximum(0, xc - INN['hi']) + np.maximum(0, INN['lo'] - xc))), gr)
        room = (d + step >= dmin) & (d + step <= dmax) & (step != 0)
        score = np.where(room, np.abs(gr), 0.0).reshape(-1)
        order = np.argsort(-score)
        npos = int((score > 0).sum())
        cands = []
        for k in (1, 2, 3, 5, 8, 13, 21, 34):
            if k <= npos: cands.append(order[:k])
        top = order[:min(npos, 256)]
        while len(cands) < a.ncand and npos > 0:
            k = int(rng.integers(1, 12))
            cands.append(rng.choice(top, size=min(k, len(top)), replace=False))
        D = np.repeat(d[None], len(cands), 0)
        for i, idx in enumerate(cands):
            flat = D[i].reshape(-1); flat[idx] += step.reshape(-1)[idx]
        # a few pure random moves (any direction) to escape gradient traps
        for i in range(len(cands) - 8, len(cands)):
            flat = D[i].reshape(-1); j = rng.integers(0, flat.size, size=3)
            flat[j] = np.clip(flat[j] + rng.choice([-1, 1], size=3), dmin.reshape(-1)[j], dmax.reshape(-1)[j])
        Gc_, Gall_, am_ = exactG(D)
        Ms = np.asarray(sfun(jnp.asarray(D, jnp.float32)), np.float64)
        Fs = Gc_ + a.mu * Ms + (a.mu2 * np.minimum(FOC['last'], 0) if FOC else 0)
        if INN is not None:
            lm = lam_now(); Ps = pen(D); Fs = Fs - lm * Ps
            F = G + a.mu * M - lm * float(pen(d[None])[0])
            ins = np.nonzero(Ps == 0)[0]
            if len(ins) and Gall_[ins].max() > INN['best']:
                k = int(ins[Gall_[ins].argmax()])
                din = convert_d(D[k], (lo, hi), (INN['lo'], INN['hi']))
                net.setup_box(INN['lo'], INN['hi'], 9); Lq = net.forward(din[None])['L'][0]; net.setup_box(lo, hi, 9)
                Lqo = Lq.copy(); Lqo[tgt] = -1e9; gq = int(Lqo.max() - Lq[tgt])
                if gq > INN['best']:
                    INN.update(best=gq, d=din, cls=int(Lqo.argmax()))
                    json.dump(dict(inst=a.inst, eps=a.inner_eps, tgt=tgt, G=gq, cls=int(Lqo.argmax()), pw=9, d=din.astype(int).reshape(-1).tolist(),
                                   note='inner-box point found by the box-penalty homotopy, re-scored exactly in the inner box'),
                              open(ck_path.replace('.json', f'_inner_eps{a.inner_eps}.json'), 'w'))
                    print(f'  t={time.time()-t0:7.1f}s it {it} INNER best G={gq} cls={int(Lqo.argmax())} lam={lm:.2f}', flush=True)
        bi = int(Fs.argmax())
        if Gall_.max() > best['G']:
            j = int(Gall_.argmax()); best.update(G=int(Gall_[j]), Gc=int(Gc_[j]), d=D[j].copy(), cls=int(am_[j]))
            print(f'  t={time.time()-t0:7.1f}s it {it} new best G={best["G"]} (cls {best["cls"]})', flush=True)
        T = a.temp * max(0.05, 1 - (time.time() - t0) / a.secs)
        if Fs[bi] > F or rng.random() < np.exp((Fs[bi] - F) / T):
            stall = 0 if Fs[bi] > F + 1e-9 else stall + 1
            d = D[bi]; F = float(Fs[bi]); G = int(Gc_[bi]); M = float(Ms[bi]); nacc += 1
        else:
            stall += 1
        if stall > a.stall:
            d = best['d'].copy()
            if a.kick > 0:   # iterated local search: perturb the incumbent before climbing again
                n = int(rng.integers(max(1, a.kick // 15), a.kick + 1)); fl = d.reshape(-1); j = rng.choice(fl.size, n, replace=False)
                fl[j] = rng.integers(dmin.reshape(-1)[j], dmax.reshape(-1)[j] + 1)
            Gc0, _, _ = exactG(d[None]); G = int(Gc0[0])
            M = float(gfun(jnp.asarray(d, jnp.float32))[0]); F = G + a.mu * M; stall = 0
        if it % 50 == 0:
            print(f'it {it} t={time.time()-t0:.0f}s cur Gc={G} M={M:.2f} F={F:.2f} best G={best["G"]}', flush=True)
        if time.time() - last_ck > 60:
            save(); last_ck = time.time()
    save()
    print('FINAL', a.inst, 'G', best['G'], 'cls', best['cls'], 'iters', it)


if __name__ == '__main__':
    main()
