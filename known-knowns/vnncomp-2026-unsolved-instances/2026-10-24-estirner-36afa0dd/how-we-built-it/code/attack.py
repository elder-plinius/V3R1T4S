"""GPU multi-disjunct margin attack for one VNN-COMP instance (lens evaluator-throughput).

  python attack.py --onnx NET.onnx.gz --vnnlib PROP.vnnlib.gz --out OUTDIR [--budget 600] [--restarts 256]
                   [--steps 200] [--top 3] [--seed 0] [--batch 2048]

Margin of disjunct d at x: min_i (A_d[i] . f(x) + b_d[i]); the property holds (counterexample) iff max_d margin >= 0.
Stage 1: every disjunct, R restarts each (uniform, strict-box corners, centre+noise; first 10% of steps ODI-style random
output directions), S steps of sign-gradient ascent with momentum and a cosine step schedule, x clamped to the strict
box [lo_s, hi_s] (float32 values strictly inside [lo, hi]). Stage 2 until the budget: the top-K disjuncts by best
margin, fresh restarts plus restarts around the best points, alternating sign-PGD and Adam on a sigmoid
reparametrisation. Every improvement of the overall best is replayed on CPU onnxruntime (float32). Outputs:
OUTDIR/summary.json (per-disjunct best GPU margins, best CPU-replayed margin, timings), OUTDIR/best_x.npy (best point,
float32, strict box), OUTDIR/candidate_<k>.npy for any point whose CPU-replayed margin is > 0.
"""
import argparse, json, math, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cuda_blocking  # noqa: F401  (blocking sync before torch touches the GPU; machine rule 7)
import numpy as np
import torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import netload, vnnspec

ap = argparse.ArgumentParser()
ap.add_argument('--onnx', required=True); ap.add_argument('--vnnlib', required=True); ap.add_argument('--out', required=True)
ap.add_argument('--budget', type=float, default=600); ap.add_argument('--restarts', type=int, default=256)
ap.add_argument('--steps', type=int, default=200); ap.add_argument('--top', type=int, default=3)
ap.add_argument('--seed', type=int, default=0); ap.add_argument('--batch', type=int, default=2048)
ap.add_argument('--stage2-restarts', type=int, default=1024)
ap.add_argument('--topk', type=int, default=0, help='stage 1 attacks only the K disjuncts with the largest margin at the box centre (0 = all)')
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
torch.backends.cuda.matmul.allow_tf32 = False; torch.backends.cudnn.allow_tf32 = False
torch.set_num_threads(1); torch.manual_seed(a.seed); np.random.seed(a.seed)
dev = 'cuda'
T0 = time.time()
spec = vnnspec.load(a.vnnlib)
raw = netload.read_bytes(a.onnx)
sess = netload.ort_session(raw)
net = netload.torch_model(raw, dev)
for p in net.parameters():
    p.requires_grad_(False)
ishape = spec['ishape']; nx = int(np.prod(ishape))
lo, hi = spec['lo'], spec['hi']
w = hi - lo
assert (w > 0).all(), 'pinned or empty coordinates: strict interior impossible'
# strict box in float32: lo_s > lo and hi_s < hi exactly (compared in float64)
d = np.maximum(1e-6 * w, 0.0)
lo_s = (lo + d).astype(np.float32); hi_s = (hi - d).astype(np.float32)
bad = lo_s.astype(np.float64) <= lo
lo_s[bad] = np.nextafter(lo_s[bad], np.float32(np.inf))
bad = hi_s.astype(np.float64) >= hi
hi_s[bad] = np.nextafter(hi_s[bad], np.float32(-np.inf))
assert (lo_s.astype(np.float64) > lo).all() and (hi_s.astype(np.float64) < hi).all() and (lo_s < hi_s).all()
LO = torch.from_numpy(lo_s).to(dev); HI = torch.from_numpy(hi_s).to(dev); SPAN = HI - LO
D = spec['disjuncts']; nd = len(D)
A = [torch.tensor(Ad, dtype=torch.float32, device=dev) for Ad, _ in D]
B = [torch.tensor(bd, dtype=torch.float32, device=dev) for _, bd in D]
shape_b = [-1] + list(ishape[1:]) if ishape[0] == 1 else [-1] + list(ishape)


def f(x):  # x [n, nx] -> outputs [n, ny]
    return net(x.view(shape_b)).reshape(x.shape[0], -1)


def margins(y, k):  # disjunct k margin for outputs y [n, ny]
    return (y @ A[k].T + B[k]).min(dim=1).values


def all_margins(y):
    return torch.stack([margins(y, k) for k in range(nd)], 1)


def cpu_margin(x32):
    y = netload.ort_forward(sess, x32, ishape).astype(np.float64)
    ms = [min(float(Ad[i] @ y + bd[i]) for i in range(len(bd))) for Ad, bd in D]
    k = int(np.argmax(ms))
    return ms[k], k, y


centre = ((lo + hi) / 2).astype(np.float32)
yc = netload.ort_forward(sess, centre, ishape)
with torch.no_grad():
    yt = f(torch.from_numpy(centre).to(dev)[None]).cpu().numpy().ravel()
conv_err = float(np.abs(yc - yt).max())
m0, k0, _ = cpu_margin(centre)
log = dict(onnx=os.path.basename(a.onnx), vnnlib=os.path.basename(a.vnnlib), n_inputs=nx, n_disjuncts=nd,
           conversion_max_abs_diff_at_centre=conv_err, centre_cpu_margin=m0, centre_best_disjunct=k0,
           seed=a.seed, budget_s=a.budget, restarts=a.restarts, steps=a.steps)
print(json.dumps(log), flush=True)
best = dict(gpu=-float('inf'), cpu=-float('inf'), k=None, x=None)
best_per_d = [-float('inf')] * nd
best_x_per_d = [None] * nd
n_cand = 0
evals = 0


def consider(x, m, k):
    """x [n, nx] strict-box points, m [n] margins for disjunct k: update bests, replay improvements on CPU."""
    global n_cand
    j = int(torch.argmax(m)); mj = float(m[j])
    if mj > best_per_d[k]:
        best_per_d[k] = mj; best_x_per_d[k] = x[j].detach().clone()
    if mj > best['gpu'] or (mj > 0 and best['cpu'] <= 0):
        x32 = x[j].detach().float().cpu().numpy()
        mc, kc, _ = cpu_margin(x32)
        if mj > best['gpu']:
            best.update(gpu=mj)
        if mc > best['cpu']:
            best.update(cpu=mc, k=kc, x=x32.copy())
            np.save(os.path.join(a.out, 'best_x.npy'), x32)
        if mc > 0:
            np.save(os.path.join(a.out, 'candidate_%d.npy' % n_cand), x32); n_cand += 1
            print('CANDIDATE cpu margin %.9g disjunct %d (gpu %.9g) t=%.1f' % (mc, kc, mj, time.time() - T0), flush=True)


def pgd(k, x, steps, odi=0.1, mode='sign'):
    """ascend disjunct k's margin from x [n, nx]; returns final x; tracks bests."""
    global evals
    n = x.shape[0]
    mom = torch.zeros_like(x)
    nodi = int(odi * steps)
    wodi = torch.empty(n, A[k].shape[1], device=dev).uniform_(-1, 1)
    if mode == 'adam':
        u = torch.logit(((x - LO) / SPAN).clamp(1e-6, 1 - 1e-6)).requires_grad_(True)
        opt = torch.optim.Adam([u], lr=0.1)
    for s in range(steps):
        if mode == 'adam':
            opt.zero_grad()
            xx = LO + SPAN * torch.sigmoid(u)
            y = f(xx); m = margins(y, k)
            (-m.sum()).backward(); opt.step()
            for g in opt.param_groups:
                g['lr'] = 0.1 * 0.5 * (1 + math.cos(math.pi * s / steps)) + 0.005
            with torch.no_grad():
                consider(xx.detach(), m.detach(), k)
            evals += n
            continue
        x.requires_grad_(True)
        y = f(x)
        if s < nodi:
            obj = (y * wodi).sum()
            m = None
        else:
            m = margins(y, k); obj = m.sum()
        g, = torch.autograd.grad(obj, x)
        with torch.no_grad():
            if m is not None:
                consider(x.detach(), m.detach(), k)
            lr = 0.01 + 0.24 * 0.5 * (1 + math.cos(math.pi * s / steps))
            mom = 0.75 * mom + g / (g.abs().mean(dim=1, keepdim=True) + 1e-20)
            x = torch.max(torch.min(x + lr * SPAN * mom.sign(), HI), LO)
        evals += n
    if mode == 'adam':
        return (LO + SPAN * torch.sigmoid(u)).detach()
    with torch.no_grad():
        consider(x, margins(f(x), k), k)
    return x.detach()


def starts(n, around=None, scale=0.1):
    u = torch.rand(n, nx, device=dev)
    x = LO + u * SPAN
    q = n // 4
    corners = torch.where(torch.rand(q, nx, device=dev) < 0.5, LO, HI)
    x[:q] = corners
    c = (LO + HI) / 2
    x[q:2 * q] = (c + (torch.rand(q, nx, device=dev) - 0.5) * SPAN * 0.2).clamp(LO, HI)
    if around is not None:
        x[2 * q:3 * q] = (around[None] + (torch.rand(q, nx, device=dev) - 0.5) * SPAN * scale).clamp(LO, HI)
    return torch.max(torch.min(x, HI), LO)


def run_chunks(k, n, steps, mode, around=None, scale=0.1):
    done = 0
    while done < n:
        m = min(a.batch, n - done)
        pgd(k, starts(m, around, scale), steps, mode=mode)
        done += m


# stage 1: all disjuncts (or the top-K by centre margin)
t1 = time.time()
yc64 = yc.astype(np.float64)
cm = [min(float(Ad[i] @ yc64 + bd[i]) for i in range(len(bd))) for Ad, bd in D]
stage1_list = sorted(range(nd), key=lambda k: -cm[k])[:a.topk] if a.topk > 0 else list(range(nd))
log['stage1_disjuncts'] = stage1_list
for k in stage1_list:
    run_chunks(k, a.restarts, a.steps, 'sign')
    if time.time() - T0 > a.budget * 0.5:
        break
log['stage1_s'] = time.time() - t1
log['stage1_best_per_disjunct'] = best_per_d[:]
print('stage1 done %.1fs best gpu %.6g cpu %.6g' % (log['stage1_s'], best['gpu'], best['cpu']), flush=True)
# stage 2: top disjuncts until budget
order = sorted(range(nd), key=lambda k: -best_per_d[k])[:a.top]
rounds = 0
while time.time() - T0 < a.budget and best['cpu'] < 1e-4:
    for k in order:
        mode = 'adam' if rounds % 2 else 'sign'
        run_chunks(k, a.stage2_restarts, a.steps, mode, around=best_x_per_d[k], scale=0.1 / (1 + rounds % 3))
        if time.time() - T0 > a.budget or best['cpu'] >= 1e-4:
            break
    rounds += 1
log.update(stage2_rounds=rounds, stage2_order=order, best_per_disjunct=best_per_d, best_gpu_margin=best['gpu'],
           best_cpu_margin=best['cpu'], best_cpu_disjunct=best['k'], n_candidates=n_cand, evals=evals,
           wall_s=time.time() - T0, peak_gpu_mem_gb=torch.cuda.max_memory_allocated() / 1e9)
json.dump(log, open(os.path.join(a.out, 'summary.json'), 'w'), indent=1)
print('DONE best cpu margin %.9g (disjunct %s) gpu %.9g candidates %d evals %d wall %.1fs' % (
    best['cpu'], best['k'], best['gpu'], n_cand, evals, time.time() - T0), flush=True)
