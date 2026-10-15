"""Surrogate (STE / annealed tanh) PGD on the continuous relaxation of the pixel-map step d, scored exactly.

Every candidate is snapped to the integer pixel map (x = v + off + m*d, d integer) and scored with the validated exact
model (exact-solver/code/bnn4864.py). The score is G = max_{c != t} L_c - L_t (integer logits); G >= 2 is a lead.
Checkpoint JSON (best d per instance and the best per target class) is rewritten at least every 60 s.

Usage: python -I surrogate.py --data DATA --inst model_48_idx_6371_eps_3 --secs 600 --out ckpt_dir [--batch 32]
       [--seed 0] [--init ckpt.json]
"""
import argparse, glob, json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'exact-solver', 'code'))
from bnn4864 import Net, parse_box, rebox, convert_d
import jax, jax.numpy as jnp
from jax import lax


def build(net):
    f32 = jnp.float32
    hwio = lambda w: jnp.asarray(w.transpose(2, 3, 1, 0), f32)
    W1, W2, W3 = hwio(net.w1), hwio(net.w2), hwio(net.w3)
    b3 = None if net.b3 is None else jnp.asarray(net.b3, f32)
    def bn(p, prm):
        sc, b, mu, s = (jnp.asarray(a, f32) for a in prm)
        return sc * (p - mu) / s + b
    D1, D2 = jnp.asarray(net.d1, f32), jnp.asarray(net.d2, f32)
    dmul, dadd = jnp.asarray(net.dmul, f32), jnp.asarray(net.dadd, f32)
    conv = lambda x, w: lax.conv_general_dilated(x, w, (1, 1), 'VALID', dimension_numbers=('NHWC', 'HWIO', 'NHWC'))
    pool = lambda x: lax.reduce_window(x, -jnp.inf, lax.max, (1, 2, 2, 1), (1, 2, 2, 1), 'VALID')
    bn3 = None
    if net.big:
        # recover BN3 params from T3/pos3 is lossy; rebuild from the graph instead
        from onnx import numpy_helper
        I = {t.name: numpy_helper.to_array(t) for t in net.model.graph.initializer}
        n3 = [n for n in net.model.graph.node if n.op_type == 'BatchNormalization'][2]
        eps = [a.f for a in n3.attribute if a.name == 'epsilon'][0]
        sc, b, mu, var = (I[n3.input[i]].astype(np.float64) for i in range(1, 5))
        bn3 = (sc, b, mu, np.sqrt(var + np.float64(np.float32(eps))))

    def pre(x, sig, beta, hard):
        """x: (1,S,S,3). Returns logits; signs are tanh(beta*q/sig) with optional STE hard forward."""
        bv = jnp.broadcast_to(jnp.asarray(beta, jnp.float32), (4,)); hv = jnp.broadcast_to(jnp.asarray(hard, jnp.float32), (4,))
        def act(q, k):   # beta / hard may be scalars or per-layer 4-vectors
            s = jnp.tanh(bv[k] * q / sig[k])
            h = jnp.where(q >= 0, 1.0, -1.0)
            return s + hv[k] * lax.stop_gradient(h - s)
        q1 = bn(pool(conv(x, W1)), net.bn1); h1 = act(q1, 0)
        q2 = bn(pool(conv(h1, W2)), net.bn2); h2 = act(q2, 1)
        if net.big:
            q3 = bn(pool(conv(h2, W3)), bn3)
        else:
            q3 = conv(h2, W3) + b3
        h3 = act(q3, 2).reshape(1, -1)
        q4 = (h3 @ D1) * dmul + dadd; h4 = act(q4, 3)
        return (h4 @ D2)[0], (q1, q2, q3, q4)
    return pre


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--eps', type=int, default=None); ap.add_argument('--data', required=True); ap.add_argument('--inst', required=True); ap.add_argument('--secs', type=float, default=600)
    ap.add_argument('--out', required=True); ap.add_argument('--batch', type=int, default=32); ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--init', default=None); ap.add_argument('--steps', type=int, default=400)
    ap.add_argument('--classes', default='top6', help="'top6' (default), 'all', or a comma list of target classes")
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
    dmin = np.asarray(net.dmin, np.float32); dmax = np.asarray(net.dmax, np.float32)
    o0 = net.forward(np.zeros((1, S, S, 3)))
    L0 = o0['L'][0]
    order = [int(c) for c in np.argsort(-L0) if c != tgt]
    # layer scales from the centre point
    _, qs = pre(v[None], jnp.ones(4), 1.0, 0.0)
    sig = jnp.asarray([float(jnp.std(q)) for q in qs], jnp.float32)
    print('inst', a.inst, 'tgt', tgt, 'centre G', int(np.delete(L0, tgt).max() - L0[tgt]), 'top classes', order[:6], 'sig', np.round(np.array(sig), 3), flush=True)

    def margin(d, c, beta, hard):
        L, _ = pre((v + m * d)[None], sig, beta, hard)
        return L[c] - L[tgt]
    g = jax.jit(jax.vmap(jax.value_and_grad(margin), in_axes=(0, 0, None, 0)))

    rng = np.random.default_rng(a.seed)
    os.makedirs(a.out, exist_ok=True)
    ck_path = os.path.join(a.out, f'{a.inst}.json')
    best = dict(G=-10**9, d=None, cls=None)
    best_by_cls = {}
    if a.init and os.path.exists(a.init):
        j = json.load(open(a.init)); best.update(G=j['G'], d=load_d(j), cls=j['cls'])
        best_by_cls = {int(k): vv for k, vv in j.get('by_cls', {}).items()}
    if os.path.exists(ck_path):
        j = json.load(open(ck_path))
        if j['G'] > best['G']:
            best.update(G=j['G'], d=load_d(j), cls=j['cls'])
        for k, vv in j.get('by_cls', {}).items():
            if int(k) not in best_by_cls or vv > best_by_cls[int(k)]: best_by_cls[int(k)] = vv
    if best['d'] is not None:   # re-score in THIS box (an init may come from another radius)
        Lb = net.forward(best['d'][None])['L'][0]; Lbo = Lb.copy(); Lbo[tgt] = -1e9
        best.update(G=int(Lbo.max() - Lb[tgt]), cls=int(Lbo.argmax())); print('init re-scored G', best['G'], 'cls', best['cls'], flush=True)
    t0 = time.time(); last_ck = 0; rnd = 0
    def save():
        json.dump(dict(inst=a.inst, eps=cur_eps, tgt=tgt, G=int(best['G']), cls=best['cls'], pw=9,
                       d=None if best['d'] is None else best['d'].astype(int).reshape(-1).tolist(),
                       by_cls={str(k): int(vv) for k, vv in best_by_cls.items()},
                       elapsed=round(time.time() - t0, 1), rounds=rnd), open(ck_path + '.tmp', 'w'))
        os.replace(ck_path + '.tmp', ck_path)
    B = a.batch
    while time.time() - t0 < a.secs:
        rnd += 1
        # per-restart config: target class, init, hard/soft, step size
        cl = order[:6] if a.classes == 'top6' else (order if a.classes == 'all' else [int(t) for t in a.classes.split(',')])
        off = rng.integers(len(cl))
        cls = np.array([cl[(i + off) % len(cl)] for i in range(B)])
        hard = (np.arange(B) % 2).astype(np.float32)
        d = rng.uniform(dmin, dmax, size=(B, S, S, 3)).astype(np.float32) * rng.uniform(0, 1, size=(B, 1, 1, 1)).astype(np.float32)
        if best['d'] is not None and rnd > 1:
            k = B // 2
            noise = rng.random((k, S, S, 3)) < rng.uniform(0.0, 0.1, size=(k, 1, 1, 1))
            dd = np.where(noise, rng.integers(net.dmin, net.dmax + 1, size=(k, S, S, 3)), best['d'][None]).astype(np.float32)
            d[:k] = dd; cls[:k] = best['cls'] if best['cls'] in cl else cls[:k]
        lr0 = 0.25 * (dmax - dmin) / 2
        T = a.steps
        for it in range(T):
            fr = it / max(T - 1, 1)
            beta = float(np.exp(np.log(0.5) + fr * (np.log(8.0) - np.log(0.5))))
            lr = lr0 * (0.5 * (1 + np.cos(np.pi * fr))) + 0.02
            val, gr = g(jnp.asarray(d), jnp.asarray(cls), beta, jnp.asarray(hard))
            gr = np.asarray(gr)
            d = np.clip(d + lr * np.sign(gr), dmin, dmax)
            if it % 20 == 19 or it == T - 1:
                Dq = np.rint(d).astype(np.int64)
                L = net.forward(Dq)['L']
                Lo = L.copy(); Lo[:, tgt] = -1e9
                G = Lo.max(1) - L[:, tgt]
                for b in range(B):
                    for c in set([int(Lo[b].argmax()), int(cls[b])]):
                        gc = int(L[b, c] - L[b, tgt])
                        if c not in best_by_cls or gc > best_by_cls[c]: best_by_cls[c] = gc
                bi = int(G.argmax())
                if G[bi] > best['G']:
                    best.update(G=int(G[bi]), d=Dq[bi].copy(), cls=int(Lo[bi].argmax()))
                    print(f'  t={time.time()-t0:7.1f}s round {rnd} it {it} new best G={best["G"]} cls={best["cls"]}', flush=True)
            if time.time() - last_ck > 60:
                save(); last_ck = time.time()
            if time.time() - t0 > a.secs: break
        print(f'round {rnd} done t={time.time()-t0:.0f}s best G={best["G"]} by_cls={dict(sorted(best_by_cls.items(), key=lambda kv: -kv[1])[:5])}', flush=True)
    save()
    print('FINAL', a.inst, 'G', best['G'], 'cls', best['cls'])


if __name__ == '__main__':
    main()
