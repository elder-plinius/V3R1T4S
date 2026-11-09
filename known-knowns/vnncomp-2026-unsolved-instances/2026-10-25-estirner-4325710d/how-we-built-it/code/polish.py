"""Exact greedy polish around a near-miss point x (HWC float, 2^-9 grid, strictly inside): every step scores ALL
single-pixel moves to {lo+g, centre value, hi-g, x-0.5, x+0.5} (snapped, strictly inside) exactly; score =
max-rival gap + 0.05 * soft layer-4 gap (exact h3, hard-tanh(z4/8)) for the focus rival; takes the best non-tabu move.
Stops and saves on max-rival gap >= 2.  Usage: polish.py SIZE IDX XPATH SECS RIVAL [seed]"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bnnx
from bnnx import torch, np, F

G = 2.0 ** -9


def main():
    size, idx, xpath, secs, rival = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], float(sys.argv[4]), int(sys.argv[5])
    seed = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    sp = bnnx.Spec(size, idx); net = bnnx.ExactNet(size, sp); dev = net.dev
    gen = torch.Generator(device=dev); gen.manual_seed(seed)
    true = sp.true; others = torch.tensor([j for j in range(43) if j != true], device=dev)
    lo = torch.tensor(sp.lo.transpose(2, 0, 1), dtype=torch.float64, device=dev).reshape(-1)
    hi = torch.tensor(sp.hi.transpose(2, 0, 1), dtype=torch.float64, device=dev).reshape(-1)
    ctr = torch.tensor((net.v + net.off).transpose(2, 0, 1), dtype=torch.float64, device=dev).reshape(-1)
    T1 = torch.tensor(net.T1, dtype=torch.float64, device=dev)[None, :, None, None]
    w1d = net.w1.double()
    x = torch.tensor(np.load(xpath).transpose(2, 0, 1), dtype=torch.float64, device=dev).reshape(-1)
    n = x.numel(); shp = (3, size, size)
    dW = net.W5[:, rival] - net.W5[:, true]

    def score(X):  # X (B, n) float64
        p1 = F.max_pool2d(F.conv2d(X.reshape(-1, *shp), w1d), 2)
        h1 = torch.where(p1 >= T1, 1.0, -1.0).float()
        L, I = net.forward_from_h1(h1, keep=True)
        mx = L[:, others].max(1).values - L[:, true]
        s4 = (I['z4'] + 0.5).div(8.0).clamp(-1, 1) @ dW
        return mx, mx + 0.05 * s4

    def snapc(v):
        v = torch.round(v / G) * G
        return torch.minimum(torch.maximum(v, lo + G), hi - G)

    m0, s0 = score(x[None]); best = float(m0[0]); cur_s = float(s0[0])
    print('start gap', best, flush=True)
    np.save(os.path.join(bnnx.LENS, 'out/polish_best_%d_%d_s%d.npy' % (size, idx, seed)), x.reshape(shp).permute(1, 2, 0).cpu().numpy())
    tabu = torch.zeros(n, dtype=torch.long, device=dev)
    t0 = time.time(); step = 0; found = False
    while time.time() - t0 < secs:
        step += 1
        cands = torch.stack([lo + G, ctr, hi - G, x - 0.5, x + 0.5])  # (5, n)
        cands = snapc(cands)
        P = torch.arange(n, device=dev).repeat(5); V = cands.reshape(-1)
        keep = V != x[P]
        P, V = P[keep], V[keep]
        if os.environ.get('SMOKE'):
            P, V = P[:64], V[:64]
        Ms, Ss = [], []
        for c in range(0, P.numel(), 512):
            pp, vv = P[c:c + 512], V[c:c + 512]
            Xb = x[None].repeat(pp.numel(), 1); Xb[torch.arange(pp.numel(), device=dev), pp] = vv
            m, s = score(Xb); Ms.append(m); Ss.append(s)
        M, S = torch.cat(Ms), torch.cat(Ss)
        S = S + 1e-4 * torch.rand(S.numel(), generator=gen, device=dev, dtype=S.dtype)
        allowed = (tabu[P] < step) | (M >= 2)
        k = int(torch.argmax(torch.where(allowed, S, torch.full_like(S, -1e9))))
        x[P[k]] = V[k]; tabu[P[k]] = step + 30
        if float(M[k]) > best:
            best = float(M[k])
            np.save(os.path.join(bnnx.LENS, 'out/polish_best_%d_%d_s%d.npy' % (size, idx, seed)), x.reshape(shp).permute(1, 2, 0).cpu().numpy())
        if step % 10 == 0 or float(M[k]) >= 2:
            print('  step %d t %.0f cur %.0f score %.3f best %.0f' % (step, time.time() - t0, float(M[k]), float(S[k]), best), flush=True)
        if float(M[k]) >= 2:
            found = True
            xo = x.reshape(shp).permute(1, 2, 0).cpu().numpy()
            np.save(os.path.join(bnnx.LENS, 'out/polish_cross_%d_%d_s%d.npy' % (size, idx, seed)), xo)
            print('*** CROSSING (exact model) step', step, 'gap', float(M[k]), flush=True)
            break
    print(json.dumps(dict(size=size, idx=idx, rival=rival, steps=step, best=best, found=found)), flush=True)


if __name__ == '__main__':
    main()
