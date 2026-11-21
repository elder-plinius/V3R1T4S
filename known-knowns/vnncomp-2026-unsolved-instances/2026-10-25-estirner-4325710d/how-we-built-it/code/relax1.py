"""Kill test H1: relaxed search in layer-1 sign space.
Free variables = pooled layer-1 neurons whose sign is not fixed over the REAL eps box (interval bounds of conv1 are exact
per position); all other layer-1 signs are fixed to their (common) value. Layers 2.. are exact. If tabu search in this
SUPERSET cannot reach logit gap >= 2, a pixel-level search (a subset) is very unlikely to.
Tabu search: each step evaluates every single flip in batch (exact gap + lam * soft gap), takes the best non-tabu move.
Usage: relax1.py SIZE IDX SECONDS [rivals comma list] [lam] [tenure]
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bnnx
from bnnx import torch, np, F


def unstable_l1(net, sp):
    """returns (fixed_h1 (32,Hp,Wp) +-1 tensor with arbitrary values at unstable spots, unstable bool mask)."""
    dev = net.dev
    w = net.w1.double()
    lo = torch.tensor(sp.lo.transpose(2, 0, 1)[None], dtype=torch.float64, device=dev)
    hi = torch.tensor(sp.hi.transpose(2, 0, 1)[None], dtype=torch.float64, device=dev)
    amax = F.conv2d(hi, w.clamp(min=0)) + F.conv2d(lo, w.clamp(max=0))
    amin = F.conv2d(lo, w.clamp(min=0)) + F.conv2d(hi, w.clamp(max=0))
    T1 = torch.tensor(net.T1, device=dev)[None, :, None, None]
    can_on = F.max_pool2d(amax, 2) >= T1
    always_on = F.max_pool2d(amin, 2) >= T1
    unst = (can_on & ~always_on)[0]
    fixed = torch.where(always_on[0], 1.0, -1.0).float()
    return fixed, unst


def soft_from_h1(net, h1, tau=(2.0, 4.0, 8.0)):
    n2 = torch.round(F.conv2d(h1, net.w2))
    p2 = F.max_pool2d(n2, 2)
    z2 = p2 - net.T2c[None, :, None, None] + 0.5
    s2 = (z2 / tau[0]).clamp(-1, 1)
    n3 = F.conv2d(s2, net.w3)
    if net.pool3:
        n3 = F.max_pool2d(n3, 2)
    z3 = n3 - net.T3c[None, :, None, None] + 0.5
    s3 = (z3 / tau[1]).clamp(-1, 1)
    f3 = s3.permute(0, 2, 3, 1).reshape(s3.shape[0], -1)
    z4 = f3 @ net.W4 - net.T4c[None] + 0.5
    s4 = (z4 / tau[2]).clamp(-1, 1)
    return s4 @ net.W5


def evaluate(net, H, rival, true, lam, chunk=512):
    """H: (B,32,Hp,Wp). returns exact gap (B,), score (B,)"""
    gaps, scores = [], []
    for i in range(0, H.shape[0], chunk):
        h = H[i:i + chunk]
        L = net.forward_from_h1(h)
        g = L[:, rival] - L[:, true]
        S = soft_from_h1(net, h)
        sg = S[:, rival] - S[:, true]
        gaps.append(g); scores.append(g + lam * sg)
    return torch.cat(gaps), torch.cat(scores)


def tabu(net, sp, rival, secs, lam=0.5, tenure=30, seed=0, h_start=None, log=None):
    fixed, unst = unstable_l1(net, sp)
    idx = torch.nonzero(unst.reshape(-1)).squeeze(1)
    if os.environ.get('SMOKE'):
        idx = idx[:16]
    nU = idx.numel()
    # centre pattern
    d0 = torch.zeros((1, 3, sp.size, sp.size), device=net.dev)
    L0, I0 = net.forward(d0, keep=True)
    h = I0['h1'][0].clone() if h_start is None else h_start.clone()
    hflat = h.reshape(-1)
    h0flat = I0['h1'][0].reshape(-1).clone()
    tabu_until = torch.zeros(nU, dtype=torch.long, device=net.dev)
    g, s = evaluate(net, h[None], rival, sp.true, lam)
    best_g, best_s = float(g[0]), float(s[0]); best_h = h.clone()
    cur_s = float(s[0])
    t0 = time.time(); step = 0
    gen = torch.Generator(device=net.dev); gen.manual_seed(seed)
    hist = []
    while time.time() - t0 < secs:
        step += 1
        H = hflat[None].repeat(nU, 1)
        ar = torch.arange(nU, device=net.dev)
        H[ar, idx] = -H[ar, idx]
        G, S = evaluate(net, H.reshape(nU, *h.shape), rival, sp.true, lam)
        S = S + 1e-3 * torch.rand(nU, generator=gen, device=net.dev)
        allowed = (tabu_until < step) | (G > best_g)
        Sm = torch.where(allowed, S, torch.full_like(S, -1e9))
        k = int(torch.argmax(Sm))
        hflat[idx[k]] = -hflat[idx[k]]
        tabu_until[k] = step + tenure + int(torch.randint(0, tenure, (1,), generator=gen, device=net.dev))
        cur_g, cur_s = float(G[k]), float(S[k])
        if cur_g > best_g or (cur_g == best_g and cur_s > best_s):
            best_g, best_s = cur_g, cur_s; best_h = hflat.reshape(h.shape).clone()
        if step % (5 if os.environ.get('SMOKE') else 50) == 0:
            ham = int((hflat != h0flat).sum())
            hist.append((step, round(time.time() - t0, 1), cur_g, round(cur_s, 2), best_g, ham))
            if log:
                print('  step', step, 't', round(time.time() - t0, 1), 'cur_gap', cur_g, 'score', round(cur_s, 2), 'best_gap', best_g, 'hamming', ham, flush=True)
    return dict(rival=rival, nU=nU, steps=step, best_gap=best_g, best_score=best_s, centre_gap=float(L0[0, rival] - L0[0, sp.true]),
                hamming_best=int((best_h.reshape(-1) != h0flat).sum()), hist=hist), best_h


def main():
    size, idx, secs = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    sp = bnnx.Spec(size, idx); sp.size = size
    net = bnnx.ExactNet(size, sp)
    d0 = torch.zeros((1, 3, size, size), device=net.dev)
    L0 = net.forward(d0)[0].cpu().numpy()
    order = [int(j) for j in np.argsort(-L0) if j != sp.true]
    rivals = [int(r) for r in sys.argv[4].split(',')] if len(sys.argv) > 4 and sys.argv[4] else order[:2]
    lam = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
    tenure = int(sys.argv[6]) if len(sys.argv) > 6 else 30
    res = []
    for r in rivals:
        out, bh = tabu(net, sp, r, secs / len(rivals), lam=lam, tenure=tenure, log=True)
        print(size, idx, 'rival', r, json.dumps({k: v for k, v in out.items() if k != 'hist'}), flush=True)
        res.append(out)
        torch.save(bh.cpu(), os.path.join(bnnx.LENS, 'out/relax1_h1_%d_%d_r%d.pt' % (size, idx, r)))
    json.dump(res, open(os.path.join(bnnx.LENS, 'out/relax1_%d_%d.json' % (size, idx)), 'w'))


if __name__ == '__main__':
    main()
