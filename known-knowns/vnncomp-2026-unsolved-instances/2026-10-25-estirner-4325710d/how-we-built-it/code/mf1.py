"""H4 (imported from Bayesian deep learning: moment propagation in probabilistic BNNs, Peters & Welling 2018 /
expectation backpropagation, Soudry et al. 2014): a categorical distribution per pixel over the admissible grid values
(eps 1: {-1,0,1}); every sign layer is propagated as independent Bernoulli units with Gaussian (CLT) pre-activations,
max-pool by 1 - prod(1 - p); maximise  E[gap] + beta * sd[gap]  (optimistic, early) annealed to  P(gap >= 2), by Adam
on the per-pixel logits; every iteration samples B points from the distribution (plus the mode) and scores them EXACTLY
with the integer model (max-rival gap). Stops and saves on max-rival gap >= 2.
Usage: mf1.py SIZE IDX EPS SECS RIVAL [lr] [B] [seed] [temp_final]
"""
import sys, os, time, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bnnx
from bnnx import torch, np, F

SQ2 = math.sqrt(2.0)


def Phi(x):
    return 0.5 * (1 + torch.erf(x / SQ2))


def mp_pool(p):
    # P(max of 2x2 window active) under independence
    return 1 - F.avg_pool2d(torch.log1p(-p.clamp(max=1 - 1e-6)), 2).mul(4).exp()


def moments(net, q, vals):
    """q: (1,3,H,W,V) probabilities over vals (V,). returns mean, var of gap logits (43,) arrays."""
    mu = (q * vals).sum(-1); ex2 = (q * vals ** 2).sum(-1); var = (ex2 - mu ** 2).clamp(min=0)
    m = F.conv2d(mu, net.w1) - net.kthr; s = (F.conv2d(var, net.w1 ** 2).clamp(min=0) + 1e-4).sqrt()
    p1 = mp_pool(Phi((m + 0.5) / s))
    h_m = 2 * p1 - 1; h_v = (1 - h_m ** 2).clamp(min=0)
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
    size, idx, eps, secs, rival = int(a[1]), int(a[2]), int(a[3]), float(a[4]), int(a[5])
    lr = float(a[6]) if len(a) > 6 else 0.1
    B = int(a[7]) if len(a) > 7 else 2048
    seed = int(a[8]) if len(a) > 8 else 0
    tag = '%d_%d_e%d_r%d_s%d' % (size, idx, eps, rival, seed)
    sp = bnnx.Spec(size, idx, eps); net = bnnx.ExactNet(size, sp); dev = net.dev
    torch.manual_seed(seed)
    vals = torch.arange(-3, 4, dtype=torch.float32, device=dev) if eps == 3 else torch.tensor([-1.0, 0.0, 1.0], device=dev)
    V = vals.numel()
    mask = (vals[None, None, None, :] >= net.dmin_t[..., None]) & (vals[None, None, None, :] <= net.dmax_t[..., None])  # (3,H,W,V)
    theta = torch.zeros((3, size, size, V), device=dev)
    theta[~mask] = -1e4
    # mild preference for the centre value at start
    theta = theta + torch.where(vals == 0, 1.0, 0.0)[None, None, None, :]
    theta = theta.masked_fill(~mask, -1e4).requires_grad_(True)
    opt = torch.optim.Adam([theta], lr=lr)
    dW = (net.W5[:, rival] - net.W5[:, sp.true])
    true = sp.true; others = torch.tensor([j for j in range(43) if j != true], device=dev)
    best = -1e9; best_d = None; t0 = time.time(); it = 0; hist = []; found = False
    while time.time() - t0 < secs:
        it += 1
        frac = min(1.0, (time.time() - t0) / secs)
        q = torch.softmax(theta, -1)[None]
        h_m, h_v = moments(net, q, vals)
        mg = (h_m @ dW)[0]; sg = ((h_v @ dW ** 2)[0] + 1e-4).sqrt()
        if not torch.isfinite(mg) and it < 3:
            print('NONFINITE mg at it', it, 'theta finite', bool(torch.isfinite(theta).all()), 'q finite', bool(torch.isfinite(q).all()), flush=True)
        beta = 1.0 * (1 - frac)
        obj = mg + beta * sg if frac < 0.5 else torch.log(Phi((mg - 2) / sg) + 1e-30)
        ent = -(q * torch.log(q + 1e-12)).sum()
        loss = -obj + 1e-4 * frac * ent
        opt.zero_grad(); loss.backward()
        with torch.no_grad():
            nbad = int((~torch.isfinite(theta.grad)).sum())
            theta.grad.nan_to_num_(0.0, 0.0, 0.0)
        opt.step()
        with torch.no_grad():
            theta.nan_to_num_(0.0).clamp_(-30, 30)
            theta.masked_fill_(~mask, -1e4)
            # sample B points + the mode
            qs = torch.softmax(theta, -1)  # (3,H,W,V)
            gum = -torch.log(-torch.log(torch.rand((B,) + qs.shape, device=dev).clamp(1e-12, 1 - 1e-7)))
            idxs = (torch.log(qs + 1e-30)[None] + gum).argmax(-1).reshape(B, -1)  # Gumbel-max sampling, (B, 3HW)
            Ds = vals[idxs].reshape(B, 3, size, size)
            Ds[0] = vals[qs.argmax(-1)]
            chunk = 1024 if size == 48 else 512
            Ms = []
            for c in range(0, B, chunk):
                L = net.forward(Ds[c:c + chunk]); Ms.append(L[:, others].max(1).values - L[:, true])
            M = torch.cat(Ms)
            k = int(M.argmax())
            if float(M[k]) > best:
                best = float(M[k]); best_d = Ds[k].clone()
            if best >= 2:
                found = True
                np.save(os.path.join(bnnx.LENS, 'out/mf1_cross_%s.npy' % tag), best_d.cpu().numpy().transpose(1, 2, 0).astype(np.int64))
                print('*** CROSSING (exact model) it', it, 'maxgap', best, flush=True)
                break
        if it % 20 == 0:
            hist.append((it, round(time.time() - t0, 1), float(mg), float(sg), float(M.mean()), float(M[0]), best))
            print('  it %d t %.0f E[gap] %.1f sd %.1f sample-mean %.1f mode %.0f best %.0f' % hist[-1], 'nonfinite grads', nbad, flush=True)
    np.save(os.path.join(bnnx.LENS, 'out/mf1_best_%s.npy' % tag), best_d.cpu().numpy().transpose(1, 2, 0).astype(np.int64))
    res = dict(tag=tag, eps=eps, rival=rival, lr=lr, B=B, iters=it, best_maxrival=best, found=found, hist=hist)
    print(json.dumps({k: v for k, v in res.items() if k != 'hist'}), flush=True)
    json.dump(res, open(os.path.join(bnnx.LENS, 'out/mf1_%s.json' % tag), 'w'))


if __name__ == '__main__':
    main()
