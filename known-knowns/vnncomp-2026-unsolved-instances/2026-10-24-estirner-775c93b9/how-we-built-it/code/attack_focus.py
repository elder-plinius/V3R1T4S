"""Focused attack on chosen disjuncts of one instance, warm-started from earlier best points (lens evaluator-throughput).
  python attack_focus.py --onnx N --vnnlib P --out DIR --disjuncts 3[,6,...] --init a.npy[,b.npy] [--budget 1800] [--seed 0]
Rounds cycle through strategies until the budget or a CPU-replayed margin >= --target (default 1e-4):
  A: sign-PGD with momentum from init points + uniform noise of scale s*span (s cycles 0.01..0.5), 500 steps, step size
     cosine from 0.10 to 0.002 of the span;
  B: Adam on a sigmoid reparametrisation from the same starts, 500 steps, lr 0.05 -> 0.001;
  C: fresh starts (uniform / vertices / centre), 300 steps sign-PGD.
Every improvement of the overall best is replayed on CPU onnxruntime (float32); points with CPU margin > 0 are saved as
candidate_*.npy. Output DIR/focus.json, DIR/best_x.npy."""
import argparse, json, math, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cuda_blocking  # noqa: F401
import numpy as np, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import netload, vnnspec
ap = argparse.ArgumentParser()
for k in ('--onnx', '--vnnlib', '--out', '--disjuncts', '--init'): ap.add_argument(k, required=True)
ap.add_argument('--budget', type=float, default=1800); ap.add_argument('--seed', type=int, default=0)
ap.add_argument('--batch', type=int, default=512); ap.add_argument('--target', type=float, default=1e-4)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
torch.backends.cuda.matmul.allow_tf32 = False; torch.backends.cudnn.allow_tf32 = False
torch.set_num_threads(1); torch.manual_seed(a.seed); dev = 'cuda'; T0 = time.time()
spec = vnnspec.load(a.vnnlib); raw = netload.read_bytes(a.onnx)
sess = netload.ort_session(raw); net = netload.torch_model(raw, dev)
for p in net.parameters(): p.requires_grad_(False)
ish = spec['ishape']; nx = int(np.prod(ish)); lo, hi = spec['lo'], spec['hi']; w = hi - lo
d = 1e-6 * w
lo_s = (lo + d).astype(np.float32); hi_s = (hi - d).astype(np.float32)
b = lo_s.astype(np.float64) <= lo; lo_s[b] = np.nextafter(lo_s[b], np.float32(np.inf))
b = hi_s.astype(np.float64) >= hi; hi_s[b] = np.nextafter(hi_s[b], np.float32(-np.inf))
assert (lo_s.astype(np.float64) > lo).all() and (hi_s.astype(np.float64) < hi).all()
LO = torch.from_numpy(lo_s).to(dev); HI = torch.from_numpy(hi_s).to(dev); SPAN = HI - LO
D = spec['disjuncts']; KS = [int(v) for v in a.disjuncts.split(',')]
A = {k: torch.tensor(D[k][0], dtype=torch.float32, device=dev) for k in KS}
B = {k: torch.tensor(D[k][1], dtype=torch.float32, device=dev) for k in KS}
shape_b = [-1] + list(ish[1:])
f = lambda x: net(x.view(shape_b)).reshape(x.shape[0], -1)
marg = lambda y, k: (y @ A[k].T + B[k]).min(1).values
inits = [torch.from_numpy(np.load(p).astype(np.float32).ravel()).to(dev).clamp(LO, HI) for p in a.init.split(',')]
best = dict(cpu=-float('inf'), gpu=-float('inf'), k=None); hist = []; ncand = 0; evals = 0
bestx = {k: inits[0].clone() for k in KS}; bestm = {k: -float('inf') for k in KS}


def cpu_check(x32):
    global ncand
    y = netload.ort_forward(sess, x32, ish).astype(np.float64)
    ms = [min(float(Ad[i] @ y + bd[i]) for i in range(len(bd))) for Ad, bd in D]
    m = max(ms)
    if m > best['cpu']:
        best.update(cpu=m, k=int(np.argmax(ms))); np.save(os.path.join(a.out, 'best_x.npy'), x32)
    if m > 0:
        np.save(os.path.join(a.out, 'candidate_%d.npy' % ncand), x32); ncand += 1
        print('CANDIDATE cpu margin %.9g disjunct %d t=%.1f' % (m, int(np.argmax(ms)), time.time() - T0), flush=True)
    return m


def track(x, m, k):
    j = int(torch.argmax(m)); mj = float(m[j])
    if mj > bestm[k]:
        bestm[k] = mj; bestx[k] = x[j].detach().clone()
    if mj > best['gpu']:
        best['gpu'] = mj; cpu_check(x[j].detach().float().cpu().numpy())


def sign_pgd(k, x, steps, lr0, lr1):
    global evals
    mom = torch.zeros_like(x)
    for s in range(steps):
        x.requires_grad_(True); m = marg(f(x), k)
        g, = torch.autograd.grad(m.sum(), x)
        with torch.no_grad():
            track(x.detach(), m.detach(), k)
            lr = lr1 + (lr0 - lr1) * 0.5 * (1 + math.cos(math.pi * s / steps))
            mom = 0.75 * mom + g / (g.abs().mean(1, keepdim=True) + 1e-20)
            x = torch.max(torch.min(x + lr * SPAN * mom.sign(), HI), LO)
        evals += x.shape[0]
    with torch.no_grad():
        track(x, marg(f(x), k), k)


def adam(k, x, steps, lr0, lr1):
    global evals
    u = torch.logit(((x - LO) / SPAN).clamp(1e-6, 1 - 1e-6)).requires_grad_(True)
    opt = torch.optim.Adam([u], lr=lr0)
    for s in range(steps):
        opt.zero_grad(); xx = LO + SPAN * torch.sigmoid(u); m = marg(f(xx), k)
        (-m.sum()).backward(); opt.step()
        for g in opt.param_groups: g['lr'] = lr1 + (lr0 - lr1) * 0.5 * (1 + math.cos(math.pi * s / steps))
        with torch.no_grad(): track(xx.detach(), m.detach(), k)
        evals += x.shape[0]


def around(k, n, s):
    src = [bestx[k]] + inits
    base = torch.stack([src[i % len(src)] for i in range(n)])
    x = base + (torch.rand(n, nx, device=dev) - 0.5) * 2 * s * SPAN
    return torch.max(torch.min(x, HI), LO)


def fresh(n):
    x = LO + torch.rand(n, nx, device=dev) * SPAN
    q = n // 3
    x[:q] = torch.where(torch.rand(q, nx, device=dev) < 0.5, LO, HI)
    return x


scales = [0.01, 0.03, 0.1, 0.3, 0.5, 0.02, 0.05, 0.2]
r = 0
while time.time() - T0 < a.budget and best['cpu'] < a.target:
    for k in KS:
        s = scales[r % len(scales)]
        strat = 'ABC'[r % 3]
        if strat == 'A': sign_pgd(k, around(k, a.batch, s), 500, 0.10, 0.002)
        elif strat == 'B': adam(k, around(k, a.batch, s), 500, 0.05, 0.001)
        else: sign_pgd(k, fresh(a.batch), 300, 0.25, 0.01)
        hist.append(dict(round=r, disjunct=k, strategy=strat, scale=s, best_gpu_k=bestm[k], best_cpu=best['cpu'], t=time.time() - T0))
        print('round %d disj %d %s s=%.2f best_k %.6g best_cpu %.6g t=%.0f' % (r, k, strat, s, bestm[k], best['cpu'], time.time() - T0), flush=True)
        if time.time() - T0 > a.budget or best['cpu'] >= a.target: break
    r += 1
out = dict(onnx=os.path.basename(a.onnx), vnnlib=os.path.basename(a.vnnlib), disjuncts=KS, init=a.init, seed=a.seed,
           budget=a.budget, best_cpu_margin=best['cpu'], best_cpu_disjunct=best['k'], best_gpu_per_disjunct=bestm,
           n_candidates=ncand, evals=evals, rounds=r, wall_s=time.time() - T0, history=hist)
json.dump(out, open(os.path.join(a.out, 'focus.json'), 'w'), indent=1, default=str)
print('DONE best cpu margin %.9g disjunct %s candidates %d evals %d wall %.0f' % (best['cpu'], best['k'], ncand, evals, time.time() - T0), flush=True)
