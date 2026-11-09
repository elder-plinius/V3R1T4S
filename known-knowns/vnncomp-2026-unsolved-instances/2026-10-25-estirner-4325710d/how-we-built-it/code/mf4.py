"""H3b + H7: target propagation with a CONTINUOUS layer-1 realisation step, iterated (IProp-like loop).
 round r: (A) relaxed layer-1 moment search from the current realised pattern h_r (free unstable bits, flip cost
          c_j * rho_j with rho_j raised x4 for bits that failed to realise in earlier rounds) -> target t (crossing with
          surplus >= GMIN preferred, cheapest such sample);
          (C) continuous realisation: x = lo + (hi-lo)*sigmoid(u) (strictly inside), minimise
          sum_j w_j * relu(MARG - t_j*(maxpool(conv1(x)) - T1)_j) - lam*softgap(x) by Adam; every 10 steps x is snapped
          to the 2^-9 grid strictly inside (conv1 exact in float32) and scored EXACTLY (max-rival gap, float64 conv1);
          the best snapped x and its realised pattern h_{r+1} start the next round.
Usage: mf4.py SIZE IDX SECS RIVAL [rounds] [rho] [gmin] [lam] [seed]
"""
import sys, os, time, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bnnx
from bnnx import torch, np, F
from relax1 import unstable_l1
from mf1 import Phi
from mf_relax import moments_from_h1

GRID = 2.0 ** -9


def main():
    a = sys.argv
    size, idx, secs, rival = int(a[1]), int(a[2]), float(a[3]), int(a[4])
    rounds = int(a[5]) if len(a) > 5 else 4
    rho0 = float(a[6]) if len(a) > 6 else 1.0
    gmin = float(a[7]) if len(a) > 7 else 30
    lam = float(a[8]) if len(a) > 8 else 0.0
    seed = int(a[9]) if len(a) > 9 else 0
    eps = int(os.environ.get('EPS', '1'))
    tag = '%d_%d_e%d_r%d_rho%g_g%g_l%g_s%d' % (size, idx, eps, rival, rho0, gmin, lam, seed)
    sp = bnnx.Spec(size, idx, eps); sp.size = size
    net = bnnx.ExactNet(size, sp); dev = net.dev
    torch.manual_seed(seed)
    true = sp.true; others = torch.tensor([j for j in range(43) if j != true], device=dev)
    dW = net.W5[:, rival] - net.W5[:, true]
    fixed, U = unstable_l1(net, sp)
    lo = torch.tensor(sp.lo.transpose(2, 0, 1)[None], dtype=torch.float64, device=dev)
    hi = torch.tensor(sp.hi.transpose(2, 0, 1)[None], dtype=torch.float64, device=dev)
    T1 = torch.tensor(net.T1, dtype=torch.float64, device=dev)[None, :, None, None]
    w1d = net.w1.double()

    def snap(x):
        xs = torch.round(x / GRID) * GRID
        xs = torch.maximum(xs, lo + GRID); xs = torch.minimum(xs, hi - GRID)
        return xs

    def exact_from_x(xs):
        p1 = F.max_pool2d(F.conv2d(xs, w1d), 2)
        h1 = torch.where(p1 >= T1, 1.0, -1.0).float()
        L = net.forward_from_h1(h1)
        return L, h1, p1

    # centre
    x0 = torch.tensor((net.v + net.off).transpose(2, 0, 1)[None], dtype=torch.float64, device=dev)
    L, hcur, _ = exact_from_x(snap(x0)); hcur = hcur[0]
    h0 = hcur.clone()
    best = float((L[0, others].max() - L[0, true])); best_x = snap(x0)
    keepw = float(os.environ.get('KEEPW', '0.3'))
    if os.environ.get('START_X'):
        xs0 = np.load(os.environ['START_X']).astype(np.float64)
        xs0 = torch.tensor(xs0.transpose(2, 0, 1)[None], dtype=torch.float64, device=dev)
        assert bool((xs0 > lo).all()) and bool((xs0 < hi).all())
        assert bool((snap(xs0) == xs0).all()), 'start x not on the 2^-9 grid'
        L, hcur, _ = exact_from_x(xs0); hcur = hcur[0]
        best = float((L[0, others].max() - L[0, true])); best_x = xs0.clone()
        tag += '_from'
        print('start from', os.environ['START_X'], 'gap', best, flush=True)
    kt = net.kthr[None]
    c_on = -F.max_pool2d(-kt, 2)[0]; c_off = F.max_pool2d(1 - kt, 2)[0]
    rho = torch.full_like(fixed, rho0)
    t0 = time.time(); log = []; found = False
    per = secs / rounds
    xcur = best_x.clone()
    for r in range(rounds):
        tr = time.time()
        # flip cost relative to the current realised pattern: distance (conv units) of the current pooled pre-act to T1
        _, _, pcur = exact_from_x(xcur)
        dist = ((pcur[0] - T1[0]).abs().float() / (75.0 * eps)).clamp(min=1.0 / 75)
        # ---- (A) relaxed search from hcur
        phi = torch.where(hcur > 0, 2.0, -2.0).clone().requires_grad_(True)
        opt = torch.optim.Adam([phi], lr=0.1)
        bestA = -1e9; tgt = None
        while time.time() - tr < 0.4 * per:
            frac = (time.time() - tr) / (0.4 * per)
            p = torch.sigmoid(phi)
            hm = torch.where(U, 2 * p - 1, fixed)[None]
            m4, v4 = moments_from_h1(net, hm)
            mg = (m4 @ dW)[0]; sg = ((v4 @ dW ** 2)[0] + 1e-4).sqrt()
            pflip = torch.where(hcur > 0, 1 - p, p) * U
            obj = mg + (1 - frac) * sg - (rho * dist * pflip).sum()
            opt.zero_grad(); (-obj).backward(); phi.grad.nan_to_num_(0.0, 0.0, 0.0); opt.step()
            with torch.no_grad():
                p = torch.sigmoid(phi)
                Hs = torch.where(torch.rand((256,) + p.shape, device=dev) < p[None], 1.0, -1.0)
                Hs[0] = torch.where(p > 0.5, 1.0, -1.0)
                Hs = torch.where(U[None], Hs, fixed[None])
                Lh = net.forward_from_h1(Hs); g = Lh[:, rival] - Lh[:, true]
                tc = (((Hs != hcur[None]) & U[None]).float() * (rho * dist)[None]).sum(dim=(1, 2, 3))
                val = torch.where(g >= gmin, 1e6 - tc, g - tc * 1e-3)
                k = int(val.argmax())
                if float(val[k]) > bestA:
                    bestA = float(val[k]); tgt = Hs[k].clone(); tgap = float(g[k])
        nflip = int(((tgt != hcur) & U).sum())
        # ---- (C) continuous realisation
        fl = ((tgt != hcur) & U).float()
        wgt = torch.where(fl > 0, 1.0, keepw) * U.float()
        u = torch.logit(((xcur - lo) / (hi - lo)).clamp(1e-4, 1 - 1e-4)).float().clone().requires_grad_(True)
        optc = torch.optim.Adam([u], lr=0.05)
        lo32, hi32, T132 = lo.float(), hi.float(), T1.float()
        it = 0; rbest_x = xcur.clone(); rb_h = hcur.clone()
        with torch.no_grad():
            Lc_, _, _ = exact_from_x(xcur)
            rbest = float(Lc_[0, others].max() - Lc_[0, true]) if os.environ.get('NOREGRESS') else -1e9
        while time.time() - tr < per:
            it += 1
            x = lo32 + (hi32 - lo32) * torch.sigmoid(u)
            pp = F.max_pool2d(F.conv2d(x, net.w1), 2)
            viol = torch.relu(1.0 - tgt[None] * (pp - T132))
            loss = (wgt[None] * viol).sum()
            optc.zero_grad(); loss.backward(); optc.step()
            if it % 10 == 0:
                with torch.no_grad():
                    xs = snap((lo32 + (hi32 - lo32) * torch.sigmoid(u)).double())
                    Lx, hx, _ = exact_from_x(xs)
                    mg_ = float(Lx[0, others].max() - Lx[0, true])
                    if mg_ > rbest:
                        rbest = mg_; rbest_x = xs.clone(); rb_h = hx[0].clone()
                    if mg_ > best:
                        best = mg_; best_x = xs.clone()
                    if best >= 2:
                        found = True; break
        real = float((((rb_h == tgt) & (fl > 0)).float().sum()) / max(1.0, float(fl.sum())))
        failed = (rb_h != tgt) & (fl > 0)
        rho = torch.where(failed, rho * 4, rho)
        collat = int(((rb_h != tgt) & U & (fl == 0)).sum())
        log.append(dict(round=r, target_gap=tgap, target_flips=nflip, realised_frac=round(real, 3), collateral=collat, round_best=rbest,
                        global_best=best, iters=it, t=round(time.time() - t0, 1)))
        print(json.dumps(log[-1]), flush=True)
        # next round starts from the round's best realised point
        xcur = rbest_x; hcur = rb_h
        if found:
            break
    xb = best_x[0].permute(1, 2, 0).cpu().numpy()
    np.save(os.path.join(bnnx.LENS, 'out/mf4_best_x_%s.npy' % tag), xb)
    if found:
        np.save(os.path.join(bnnx.LENS, 'out/mf4_cross_x_%s.npy' % tag), xb)
        print('*** CROSSING (exact model)', best, flush=True)
    res = dict(tag=tag, best_maxrival=best, found=found, rounds=log)
    print(json.dumps(dict(tag=tag, best_maxrival=best, found=found)), flush=True)
    json.dump(res, open(os.path.join(bnnx.LENS, 'out/mf4_%s.json' % tag), 'w'))


if __name__ == '__main__':
    main()
