"""MinSR training of the symmetrised periodic-ResNet NQS with own Metropolis sampler (Sz=0 exchange moves).
Holds the shared heavy lock in chunks of <= --hold seconds, checkpoints after every chunk, sleeps --rest seconds.
Log line per step: step, E mean (Pauli), sigma (naive sqrt(var/Ns)), variance, acceptance, lr, time.
Optional exact evaluation (L=4: full Sz=0 enumeration) every --exact_every steps.

Example: python train.py --L 6 --J2 0.8 --irrep B1 --tag r6 --steps 2000 --ns 4096
"""
import sys, os, json, math, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nqs
import numpy as np, torch

ap = argparse.ArgumentParser()
ap.add_argument('--L', type=int, required=True); ap.add_argument('--J2', type=float, required=True)
ap.add_argument('--channels', type=int, default=16); ap.add_argument('--blocks', type=int, default=3)
ap.add_argument('--kernel', type=int, default=3)
ap.add_argument('--prior', default='stripe'); ap.add_argument('--irrep', default='A1')
ap.add_argument('--flip', type=int, default=1); ap.add_argument('--sym', type=int, default=1)
ap.add_argument('--ns', type=int, default=2048, help='chains = samples per step')
ap.add_argument('--sweeps', type=float, default=1.0, help='sweeps (N moves) between steps')
ap.add_argument('--therm', type=int, default=20, help='thermalisation sweeps at start')
ap.add_argument('--steps', type=int, default=500); ap.add_argument('--lr', type=float, default=0.02)
ap.add_argument('--lr_end', type=float, default=None); ap.add_argument('--warm', type=int, default=30)
ap.add_argument('--ds', type=float, default=1e-4, help='relative diagonal shift')
ap.add_argument('--max_dth', type=float, default=1.0, help='clip |dtheta|_2')
ap.add_argument('--init', default=None, help='checkpoint to warm start from (kernel transfer across L)')
ap.add_argument('--resume', default=None, help='checkpoint to resume (same L): restores step, chains, rng')
ap.add_argument('--tag', required=True); ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--hold', type=float, default=225.0); ap.add_argument('--rest', type=float, default=20.0)
ap.add_argument('--deadline', type=float, default=None, help='unix time: stop (after checkpoint) before this')
ap.add_argument('--exact_every', type=int, default=0)
ap.add_argument('--jchunk', type=int, default=256); ap.add_argument('--pidfile', default=None)
ap.add_argument('--sched_start', type=int, default=0, help='cosine lr schedule runs from this step to --steps')
ap.add_argument('--eval_rounds', type=int, default=0); ap.add_argument('--eval_chains', type=int, default=4096)
ap.add_argument('--eval_seed', type=int, default=777); ap.add_argument('--eval_gap', type=float, default=2.0)
ap.add_argument('--ref_e', type=float, default=None)
a = ap.parse_args()

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CK = os.path.join(ROOT, 'ckpt', a.tag + '.pt'); LOG = os.path.join(ROOT, 'out', a.tag + '.log')
if a.pidfile:
    with open(a.pidfile, 'a') as f:
        f.write('%d python train.py tag=%s started %s\n' % (os.getpid(), a.tag, time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))
dev = nqs.DEVICE
if dev == 'cuda':
    torch.cuda.set_per_process_memory_fraction(7.0 / 16.0)
torch.manual_seed(a.seed); gen = torch.Generator(device=dev); gen.manual_seed(a.seed)
logf = open(LOG, 'a')
def log(s):
    print(s, flush=True); logf.write(s + '\n'); logf.flush()

log('# start %s args %s' % (time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), json.dumps(vars(a))))
L, N = a.L, a.L * a.L
cfg = dict(L=L, net=dict(channels=a.channels, blocks=a.blocks, kernel=a.kernel), prior=a.prior, irrep=a.irrep,
           flip=bool(a.flip), sym=bool(a.sym))
step0 = 0; x = None; hist = []
if a.resume:
    model, d = nqs.load_ckpt(a.resume, dev)
    step0 = d['opt_state']['step']; x = d['chains'].to(dev); hist = d.get('hist', [])
    if x.shape[0] != a.ns:
        x = None; log('# chain count changed: fresh chains')
    if 'gen_state' in d:
        try:
            gen.set_state(d['gen_state'].to('cpu'))
        except RuntimeError as e:
            log('# rng state not restored (%s); seed %d used' % (str(e)[:60], a.seed))
    log('# resumed from %s at step %d' % (a.resume, step0))
elif a.init:
    src, d = nqs.load_ckpt(a.init, dev)
    model = nqs.build(cfg, dev)
    assert src.cfg['net'] == cfg['net'], 'architecture mismatch for transfer'
    model.net.load_state_dict(src.net.state_dict())
    log('# kernel transfer from %s (L=%d, J2 from its log) to L=%d' % (a.init, src.cfg['L'], L))
    del src
else:
    model = nqs.build(cfg, dev)
cfg = model.cfg
H = nqs.Ham(L, 1.0, a.J2, dev)
Np = nqs.nparams(model); log('# params %d  group size %d  config %s' % (Np, model.perms.shape[0], json.dumps(cfg)))
maxim = int(min(131072, 0.25e9 / (4 * a.channels * N)))
w = torch.full((a.ns,), 1.0 / a.ns, device=dev, dtype=torch.float64)
lr_end = a.lr if a.lr_end is None else a.lr_end

exact = None
if a.exact_every and L == 4:
    sys.path.insert(0, HERE)
    import ed4x4
    ints, conf = ed4x4.basis(); Hm = ed4x4.hamiltonian(ints, conf, 1.0, a.J2)
    xe = torch.tensor(conf, device=dev)
    def exact_energy():
        lp = nqs.logpsi_chunked(model, xe, maxim).double()
        lp[:, 0] -= lp[:, 0].max()
        psi = (torch.exp(lp[:, 0]) * torch.exp(1j * lp[:, 1])).cpu().numpy()
        return float(np.real(np.vdot(psi, Hm @ psi)) / np.real(np.vdot(psi, psi)))


def lr_at(t):
    u = min(1.0, max(0.0, (t - a.sched_start) / max(1, a.steps - a.sched_start)))
    base = lr_end + (a.lr - lr_end) * 0.5 * (1 + math.cos(math.pi * u))
    return base * min(1.0, (t + 1) / max(1, a.warm))


def checkpoint(step):
    nqs.save_ckpt(CK, model, dict(opt_state=dict(step=step, lr=a.lr, lr_end=lr_end, warm=a.warm, steps=a.steps,
                                                 ds=a.ds, optimizer='MinSR (stateless)'),
                                  chains=x.detach().cpu(), gen_state=gen.get_state(), hist=hist, args=vars(a),
                                  J2=a.J2))


step = step0; est = 10.0; first = True
while step < a.steps:
    if a.deadline and time.time() > a.deadline - 2 * est - 60:
        log('# deadline reached'); break
    with nqs.HeavyLock() as lk:
        log('# lock acquired after %.1f s wait at %s' % (lk.waited, time.strftime('%H:%M:%SZ', time.gmtime())))
        if x is None:
            x = nqs.random_sz0(a.ns, N, dev, gen)
        lp = nqs.logpsi_chunked(model, x, maxim)
        if first:
            t0 = time.time()
            x, lp, acc = nqs.metropolis(model, H, x, lp, a.therm * N, gen, max_images=maxim)
            log('# thermalised %d sweeps acc %.3f in %.1f s' % (a.therm, acc, time.time() - t0)); first = False
        while step < a.steps and lk.held() + 1.3 * est < a.hold:
            if a.deadline and time.time() > a.deadline - 2 * est - 60:
                break
            t0 = time.time()
            x, lp, acc = nqs.metropolis(model, H, x, lp, max(1, int(a.sweeps * N)), gen, max_images=maxim)
            t1 = time.time()
            El = nqs.local_energy(model, H, x, lp, max_images=maxim)
            t2 = time.time()
            O = nqs.jacobian(model, x, a.jchunk)
            t3 = time.time()
            lr = lr_at(step)
            dth, info = nqs.minsr_update(O, El, w, lr, a.ds)
            del O
            nrm = float(dth.norm())
            if not math.isfinite(nrm):
                log('# non-finite update at step %d; skipped' % step); step += 1; continue
            if nrm > a.max_dth:
                dth *= a.max_dth / nrm
            nqs.apply_update(model, dth)
            lp = nqs.logpsi_chunked(model, x, maxim)
            nqs.sync(); t4 = time.time()
            Er = El.real; var = float(Er.var()); Em = float(Er.mean())
            rec = dict(step=step, E=Em, sig=math.sqrt(var / a.ns), var=var, Eim=float(El.imag.mean()), acc=acc,
                       lr=lr, dth=nrm, t=t4 - t0, t_mc=t1 - t0, t_el=t2 - t1, t_jac=t3 - t2, t_sr=t4 - t3)
            if exact is None and a.exact_every and L == 4 and (step % a.exact_every == 0 or step == a.steps - 1):
                rec['E_exact'] = exact_energy()
            hist.append(rec)
            log('step %d E %.6f sigma %.6f var %.5f e/site(spin1/2) %.7f acc %.3f lr %.4g |dth| %.3g time %.2f '
                '(mc %.2f el %.2f jac %.2f sr %.2f)%s' % (step, Em, rec['sig'], var, Em / (4 * N), acc, lr, nrm,
                rec['t'], rec['t_mc'], rec['t_el'], rec['t_jac'], rec['t_sr'],
                ('  E_exact %.8f' % rec['E_exact']) if 'E_exact' in rec else ''))
            est = 0.7 * est + 0.3 * (t4 - t0) if step > step0 else (t4 - t0)
            step += 1
        checkpoint(step)
        log('# checkpoint %s step %d at %s  peak mem %.2f GB' % (CK, step, time.strftime('%H:%M:%SZ', time.gmtime()),
            torch.cuda.max_memory_allocated() / 1e9 if dev == 'cuda' else 0.0))
    if step < a.steps:
        time.sleep(a.rest)
log('# done step %d at %s' % (step, time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))
if a.eval_rounds and step >= a.steps:
    time.sleep(a.rest)
    r = nqs.mc_evaluate(model, H, a.eval_chains, a.eval_rounds, a.eval_gap, 50, a.eval_seed, a.hold, a.rest, maxim,
                        log, a.ref_e)
    r.update(ckpt=CK, step=step, J2=a.J2, config=model.cfg, end=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    json.dump(r, open(os.path.join(ROOT, 'out', 'eval_' + a.tag + '.json'), 'w'), indent=1)
    log('# EVAL ' + json.dumps({k: v for k, v in r.items() if k != 'blocking_levels'}))
