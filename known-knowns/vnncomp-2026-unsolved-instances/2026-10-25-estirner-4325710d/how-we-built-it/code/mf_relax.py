"""H1b: moment-propagation search in the RELAXED layer-1 space (free unstable layer-1 signs = superset of pixel-realisable
patterns): independent Bernoulli per free bit, Gaussian moments for layers 2..4 (as mf1), Adam on the bit logits,
exact scoring of sampled patterns with forward_from_h1 (max-rival gap). A better optimiser for the H1 kill test.
Usage: mf_relax.py SIZE IDX SECS RIVAL [lr] [B] [seed]
"""
import sys, os, time, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bnnx
from bnnx import torch, np, F
from relax1 import unstable_l1
from mf1 import Phi, mp_pool


def moments_from_h1(net, h_m):
    h_v = (1 - h_m ** 2).clamp(min=0)
    m = F.conv2d(h_m, net.w2) - net.T2c[None, :, None, None]; s = (F.conv2d(h_v, net.w2 ** 2).clamp(min=0) + 1e-4).sqrt()
    p2 = mp_pool(Phi((m + 0.5) / s))
    h_m = 2 * p2 - 1; h_v = (1 - h_m ** 2).clamp(min=0)
    m = F.conv2d(h_m, net.w3); s2 = F.conv2d(h_v, net.w3 ** 2).clamp(min=0)
    if net.pool3:
        p3 = mp_pool(Phi((m - net.T3c[None, :, None, None] + 0.5) / (s2 + 1e-4).sqrt()))
    else:
        p3 = Phi((m - net.T3c[None, :, None, None] + 0.5) / (s2 + 1e-4).sqrt())
    h_m = (2 * p3 - 1).permute(0, 2, 3, 1).reshape(1, -1); h_v = (1 - h_m ** 2).clamp(min=0)
    m = h_m @ net.W4 - net.T4c[None]; s = ((h_v @ net.W4 ** 2).clamp(min=0) + 1e-4).sqrt()
    p4 = Phi((m + 0.5) / s)
    h_m = 2 * p4 - 1; h_v = (1 - h_m ** 2).clamp(min=0)
    return h_m, h_v


def main():
    a = sys.argv
    size, idx, secs, rival = int(a[1]), int(a[2]), float(a[3]), int(a[4])
    lr = float(a[5]) if len(a) > 5 else 0.1
    B = int(a[6]) if len(a) > 6 else 2048
    seed = int(a[7]) if len(a) > 7 else 0
    sp = bnnx.Spec(size, idx); sp.size = size
    net = bnnx.ExactNet(size, sp); dev = net.dev
    torch.manual_seed(seed)
    fixed, U = unstable_l1(net, sp)
    d0 = torch.zeros((1, 3, size, size), device=dev)
    L0, I0 = net.forward(d0, keep=True)
    h0 = I0['h1'][0]
    phi = torch.where(h0 > 0, 1.0, -1.0).clone().requires_grad_(True)  # start near the centre pattern
    opt = torch.optim.Adam([phi], lr=lr)
    dW = net.W5[:, rival] - net.W5[:, sp.true]
    true = sp.true; others = torch.tensor([j for j in range(43) if j != true], device=dev)
    Uf = U.float()
    best = -1e9; t0 = time.time(); it = 0; hist = []; best_h = None
    while time.time() - t0 < secs:
        it += 1
        frac = min(1.0, (time.time() - t0) / secs)
        p = torch.sigmoid(phi)
        hm = torch.where(U, 2 * p - 1, fixed)[None]
        m4, v4 = moments_from_h1(net, hm)
        mg = (m4 @ dW)[0]; sg = ((v4 @ dW ** 2)[0] + 1e-4).sqrt()
        obj = mg + (1 - frac) * sg if frac < 0.5 else torch.log(Phi((mg - 2) / sg) + 1e-30)
        opt.zero_grad(); (-obj).backward(); opt.step()
        with torch.no_grad():
            p = torch.sigmoid(phi)
            Hs = torch.where(torch.rand((B,) + p.shape, device=dev) < p[None], 1.0, -1.0)
            Hs[0] = torch.where(p > 0.5, 1.0, -1.0)
            Hs = torch.where(U[None], Hs, fixed[None])
            Ms = []
            for c in range(0, B, 512):
                L = net.forward_from_h1(Hs[c:c + 512]); Ms.append(L[:, others].max(1).values - L[:, true])
            M = torch.cat(Ms); k = int(M.argmax())
            if float(M[k]) > best:
                best = float(M[k]); best_h = Hs[k].clone()
        if it % 20 == 0:
            ham = int(((best_h != h0) & U).sum())
            hist.append((it, round(time.time() - t0, 1), float(mg), float(sg), float(M.mean()), float(M[0]), best, ham))
            print('  it %d t %.0f E[gap] %.1f sd %.1f sample-mean %.1f mode %.0f best %.0f ham %d' % hist[-1], flush=True)
    res = dict(size=size, idx=idx, rival=rival, lr=lr, B=B, iters=it, nU=int(U.sum()), best_maxrival=best, hist=hist)
    print(json.dumps({k: v for k, v in res.items() if k != 'hist'}), flush=True)
    json.dump(res, open(os.path.join(bnnx.LENS, 'out/mf_relax_%d_%d_r%d_s%d.json' % (size, idx, rival, seed)), 'w'))
    torch.save(best_h.cpu(), os.path.join(bnnx.LENS, 'out/mf_relax_h1_%d_%d_r%d_s%d.pt' % (size, idx, rival, seed)))


if __name__ == '__main__':
    main()
