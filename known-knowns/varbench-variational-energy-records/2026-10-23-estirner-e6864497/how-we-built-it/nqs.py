"""Translation-equivariant NQS for the L x L periodic J1-J2 model (Pauli convention), own sampler, local energy,
MinSR, blocking, GPU lock, checkpoints.  Lens representation-transfer, run 2026-10-22-1610.

Conventions
- sites k = r*L + c (r = row = y, c = column = x); configurations s in {-1,+1}^N as float32 (B, N).
- H = J1 sum_<ij> sigma_i.sigma_j + J2 sum_<<ij>> sigma_i.sigma_j, each bond once (2N NN + 2N diagonal),
  sigma.sigma = zz + 2(+- + -+): diagonal s_i s_j, off-diagonal 2 for an antiparallel pair (swap).
- psi(s) = sum_{g in G} chi(g) psi0(g s),  psi0(s) = prior(s) * exp(a(s) + i phi(s)),
  (a, phi) = sum over sites of a two-headed per-site output of a periodic ResNet (kernels independent of L).
- prior 'stripe': (-1)^(number of up spins on odd columns);  'marshall': (-1)^(up spins on sublattice r+c odd).
- G = C4v (8 elements, about site 0) x optional spin flip; characters for A1, A2, B1, B2 (B1: odd under the 90-degree
  rotation and the diagonal reflections, even under the axis reflections).
"""
import ctypes, glob, os, sys, json, time, math, fcntl
def _site():
    import importlib.util
    sp = importlib.util.find_spec('nvidia')
    return os.path.dirname(list(sp.submodule_search_locations)[0]) if sp else ''
_venv = os.environ.get('V3R1T4S_SITE_PACKAGES') or _site()   # the folder holding nvidia/cuda_runtime
_rc = ctypes.CDLL(glob.glob(os.path.join(_venv, 'nvidia/cuda_runtime/lib/libcudart.so*'))[0]).cudaSetDeviceFlags(4)
assert _rc == 0, 'cudaSetDeviceFlags(4) failed'
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from torch.func import functional_call, vmap, jacrev

torch.backends.cudnn.allow_tf32 = False      # strict FP32 network passes
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.benchmark = True

LOCK = os.environ.get('V3R1T4S_LOCK', '')   # optional machine-wide lock file


NOLOCK = os.environ.get('NQS_NOLOCK') == '1' or not LOCK      # only for tiny CPU tests (< 10 s)
DEVICE = os.environ.get('NQS_DEVICE', 'cuda')


class HeavyLock:
    """flock on the shared heavy-job lock; use as context manager."""
    def __enter__(self):
        self.t0 = time.time()
        if not NOLOCK:
            self.lf = open(LOCK, 'a'); fcntl.flock(self.lf, fcntl.LOCK_EX)
        self.waited = time.time() - self.t0; self.t1 = time.time(); return self
    def held(self):
        return time.time() - self.t1
    def __exit__(self, *a):
        if not NOLOCK:
            fcntl.flock(self.lf, fcntl.LOCK_UN); self.lf.close()


def sync():
    if DEVICE == 'cuda':
        torch.cuda.synchronize()


# ---------------------------------------------------------------- lattice
def bonds(L, J1=1.0, J2=0.0):
    I, Jx, W = [], [], []
    for r in range(L):
        for c in range(L):
            k = r * L + c
            for (dr, dc, w) in ((0, 1, J1), (1, 0, J1), (1, 1, J2), (1, -1, J2)):
                if w == 0.0:
                    continue
                I.append(k); Jx.append(((r + dr) % L) * L + (c + dc) % L); W.append(w)
    return np.array(I), np.array(Jx), np.array(W, dtype=np.float64)


def c4v_perms(L):
    """8 permutations p with (g s)[k] = s[p[k]], and their class labels."""
    r, c = np.meshgrid(np.arange(L), np.arange(L), indexing='ij')
    maps = {
        'e': (r, c), 'r90': (c, -r), 'r180': (-r, -c), 'r270': (-c, r),
        'mr': (-r, c), 'mc': (r, -c), 'd': (c, r), 'ad': (-c, -r)}
    out = {}
    for name, (rr, cc) in maps.items():
        out[name] = ((rr % L) * L + (cc % L)).reshape(-1)
    return out


CHARS = {  # e r90 r180 r270 mr mc d ad
    'A1': dict(e=1, r90=1, r180=1, r270=1, mr=1, mc=1, d=1, ad=1),
    'A2': dict(e=1, r90=1, r180=1, r270=1, mr=-1, mc=-1, d=-1, ad=-1),
    'B1': dict(e=1, r90=-1, r180=1, r270=-1, mr=1, mc=1, d=-1, ad=-1),
    'B2': dict(e=1, r90=-1, r180=1, r270=-1, mr=-1, mc=-1, d=1, ad=1),
}


# ---------------------------------------------------------------- network
class Block(nn.Module):
    def __init__(s, C, k):
        super().__init__()
        s.c1 = nn.Conv2d(C, C, k, padding=k // 2, padding_mode='circular')
        s.c2 = nn.Conv2d(C, C, k, padding=k // 2, padding_mode='circular')
        with torch.no_grad():
            s.c2.weight.mul_(0.1); s.c2.bias.zero_()
    def forward(s, h):
        return h + s.c2(F.gelu(s.c1(F.gelu(h))))


class ResNet(nn.Module):
    """Periodic ResNet; returns per-configuration (a, phi) = sums over sites of a 2-channel 1x1 head."""
    def __init__(s, channels=16, blocks=4, kernel=3):
        super().__init__()
        s.inp = nn.Conv2d(1, channels, kernel, padding=kernel // 2, padding_mode='circular')
        s.blocks = nn.ModuleList([Block(channels, kernel) for _ in range(blocks)])
        s.head = nn.Conv2d(channels, 2, 1)
        with torch.no_grad():
            s.head.weight.mul_(0.05); s.head.bias.zero_()
    def forward(s, x):  # x (B, N)
        B, N = x.shape; L = int(round(math.sqrt(N)))
        h = s.inp(x.view(B, 1, L, L))
        for b in s.blocks:
            h = b(h)
        return s.head(F.gelu(h)).sum((2, 3))  # (B, 2)


class NQS(nn.Module):
    """Symmetrised state.  forward(x (B,N)) -> (B,2) = (Re log psi, Im log psi)."""
    def __init__(s, L, net_cfg, prior='stripe', irrep='A1', flip=True, sym=True):
        super().__init__()
        s.L, s.N = L, L * L
        s.cfg = dict(L=L, net=net_cfg, prior=prior, irrep=irrep, flip=flip, sym=sym)
        s.net = ResNet(**net_cfg)
        s.set_symmetry(L, irrep, flip, sym, prior)

    def set_symmetry(s, L, irrep, flip, sym, prior):
        s.L, s.N = L, L * L
        s.cfg.update(L=L, irrep=irrep, flip=flip, sym=sym, prior=prior)
        P = c4v_perms(L)
        names = list(P) if sym else ['e']
        perms = [P[n] for n in names]; ch = [CHARS[irrep][n] for n in names]
        if flip:
            perms = perms + perms; fl = [1.0] * len(names) + [-1.0] * len(names); ch = ch + ch
        else:
            fl = [1.0] * len(names)
        dev = next(s.net.parameters()).device if len(list(s.net.parameters())) else 'cpu'
        s.register_buffer('perms', torch.tensor(np.stack(perms), dtype=torch.long, device=dev), persistent=False)
        s.register_buffer('flips', torch.tensor(fl, dtype=torch.float32, device=dev), persistent=False)
        # character as an added phase: 0 for +1, pi for -1
        s.register_buffer('chphase', torch.tensor([0.0 if c > 0 else math.pi for c in ch], dtype=torch.float32,
                                                  device=dev), persistent=False)
        r, c = np.meshgrid(np.arange(L), np.arange(L), indexing='ij')
        if prior == 'stripe':
            m = (c % 2 == 1)
        elif prior == 'marshall':
            m = ((r + c) % 2 == 1)
        else:
            m = np.zeros((L, L), bool)
        s.register_buffer('prior_mask', torch.tensor(m.reshape(-1), dtype=torch.float32, device=dev),
                          persistent=False)

    def forward(s, x):
        B, N = x.shape; G = s.perms.shape[0]
        xs = x[:, s.perms] * s.flips[None, :, None]           # (B, G, N)
        xs = xs.reshape(B * G, N)
        out = s.net(xs).view(B, G, 2)
        a = out[..., 0]
        nup_odd = ((1.0 + xs) * 0.5) @ s.prior_mask              # (B*G,)
        ph = out[..., 1] + math.pi * nup_odd.view(B, G) + s.chphase[None, :]
        m = a.max(1, keepdim=True).values.detach()
        e = torch.exp(a - m)
        re = (e * torch.cos(ph)).sum(1); im = (e * torch.sin(ph)).sum(1)
        logabs = m[:, 0] + 0.5 * torch.log(re * re + im * im)
        phase = torch.atan2(im, re)
        return torch.stack([logabs, phase], 1)


def build(cfg, device='cuda'):
    m = NQS(cfg['L'], cfg['net'], cfg.get('prior', 'stripe'), cfg.get('irrep', 'A1'), cfg.get('flip', True),
            cfg.get('sym', True)).to(device)
    m.set_symmetry(cfg['L'], cfg.get('irrep', 'A1'), cfg.get('flip', True), cfg.get('sym', True),
                   cfg.get('prior', 'stripe'))
    return m


def nparams(model):
    return sum(p.numel() for p in model.parameters())


# ---------------------------------------------------------------- evaluation helpers
@torch.no_grad()
def logpsi_chunked(model, x, max_images=262144):
    G = model.perms.shape[0]; ch = max(1, max_images // G)
    return torch.cat([model(x[i:i + ch]) for i in range(0, x.shape[0], ch)], 0)


class Ham:
    def __init__(s, L, J1, J2, device='cuda'):
        I, Jx, W = bonds(L, J1, J2)
        s.L, s.N, s.J1, s.J2 = L, L * L, J1, J2
        s.I = torch.tensor(I, device=device); s.J = torch.tensor(Jx, device=device)
        s.W = torch.tensor(W, device=device, dtype=torch.float64)


@torch.no_grad()
def local_energy(model, H, x, lp=None, max_images=262144, chunk=None):
    """E_loc(s) = sum_b W_b s_i s_j + sum_{b antiparallel} 2 W_b psi(s^b)/psi(s); complex128 (B,)."""
    B = x.shape[0]
    if lp is None:
        lp = logpsi_chunked(model, x, max_images)
    si, sj = x[:, H.I], x[:, H.J]                                # (B, nb)
    diag = ((si * sj).double() * H.W[None]).sum(1)
    G = model.perms.shape[0]
    rows_per = max(1, max_images // G)
    out = torch.zeros(B, dtype=torch.complex128, device=x.device)
    bchunk = chunk or max(1, rows_per // max(1, H.I.numel() // 2))
    for b0 in range(0, B, bchunk):
        xb = x[b0:b0 + bchunk]; anti = (xb[:, H.I] != xb[:, H.J])
        ib, kb = anti.nonzero(as_tuple=True)
        xp = xb[ib].clone()
        ar = torch.arange(ib.numel(), device=x.device)
        xp[ar, H.I[kb]] *= -1; xp[ar, H.J[kb]] *= -1
        lpp = logpsi_chunked(model, xp, max_images)
        d = (lpp - lp[b0 + ib]).double()
        ratio = torch.exp(torch.complex(d[:, 0], d[:, 1]))
        contrib = 2.0 * H.W[kb] * ratio
        out[b0:b0 + bchunk].index_add_(0, ib, contrib)
    return out + diag


# ---------------------------------------------------------------- sampler
def random_sz0(n, N, device, gen=None):
    r = torch.rand(n, N, device=device, generator=gen)
    idx = r.argsort(1)
    x = torch.full((n, N), -1.0, device=device)
    x.scatter_(1, idx[:, :N // 2], 1.0)
    return x


@torch.no_grad()
def metropolis(model, H, x, lp, nsteps, gen=None, p_global=0.1, max_images=262144):
    """Exchange moves at Sz=0: a random bond (NN or diagonal) of the Hamiltonian, or with prob p_global a random
    pair of sites; swap if antiparallel; accept with |psi'/psi|^2.  All proposals symmetric.  Returns x, lp, acc."""
    C, N = x.shape; nb = H.I.numel(); acc = 0.0
    ar = torch.arange(C, device=x.device)
    for _ in range(nsteps):
        k = torch.randint(0, nb, (C,), device=x.device, generator=gen)
        i, j = H.I[k], H.J[k]
        gl = torch.rand(C, device=x.device, generator=gen) < p_global
        gi = torch.randint(0, N, (C,), device=x.device, generator=gen)
        gj = (gi + torch.randint(1, N, (C,), device=x.device, generator=gen)) % N
        i = torch.where(gl, gi, i); j = torch.where(gl, gj, j)
        anti = x[ar, i] != x[ar, j]
        xp = x.clone(); xp[ar, i] *= -1; xp[ar, j] *= -1
        lpp = logpsi_chunked(model, xp, max_images)
        u = torch.rand(C, device=x.device, generator=gen)
        accept = anti & (torch.log(u) < 2.0 * (lpp[:, 0] - lp[:, 0]))
        x = torch.where(accept[:, None], xp, x); lp = torch.where(accept[:, None], lpp, lp)
        acc += accept.float().mean().item()
    return x, lp, acc / max(1, nsteps)


# ---------------------------------------------------------------- per-sample log-derivatives and MinSR
def param_dict(model):
    return {k: v.detach() for k, v in model.named_parameters()}


def jacobian(model, x, chunk=256):
    """O (B, Np) complex64: d log psi / d theta for real parameters theta (Re and Im parts)."""
    params = param_dict(model)
    def f(p, xi):
        return functional_call(model, p, (xi[None],))[0]          # (2,)
    jf = vmap(jacrev(f), in_dims=(None, 0))
    outs = []
    for i in range(0, x.shape[0], chunk):
        J = jf(params, x[i:i + chunk])                              # dict of (b, 2, *shape)
        flat = torch.cat([J[k].reshape(J[k].shape[0], 2, -1) for k in params], 2)
        outs.append(torch.complex(flat[:, 0], flat[:, 1]))
    return torch.cat(outs, 0)


def minsr_update(O, Eloc, w, lr, diag_shift=1e-4):
    """Real-parameter MinSR (stacked real/imag form, equal to SR with S = Re O^dag O via the push-through identity).
    O (Ns, Np) complex64; Eloc (Ns,) complex128; w (Ns,) weights summing to 1 (1/Ns for MC, p(s) for exact).
    Returns dtheta (Np,) float32 and info."""
    w = w.double()
    Om = (w[:, None].to(O.dtype) * O).sum(0, keepdim=True)
    sw = w.sqrt()
    Oc = (O - Om)                                                   # centred, complex64
    Em = (w * Eloc).sum()
    eps = -lr * sw * (Eloc - Em)                                     # complex128 (Ns,)
    Ns, Np = O.shape
    X = torch.cat([Oc.real, Oc.imag], 0).double() * torch.cat([sw, sw])[:, None]   # (2Ns, Np) fp64
    e = torch.cat([eps.real, eps.imag])
    if 2 * Ns <= Np:
        T = X @ X.T
        lam = diag_shift * T.diagonal().mean()
        T.diagonal().add_(lam)
        Lc, info = torch.linalg.cholesky_ex(T)
        if info.item() == 0:
            y = torch.cholesky_solve(e[:, None], Lc)[:, 0]
        else:
            y = torch.linalg.solve(T, e)
        dth = X.T @ y
    else:
        S = X.T @ X
        lam = diag_shift * (X * X).sum() / (2 * Ns)     # same lambda as the Ns-space form (mean diag of X X^T)
        S.diagonal().add_(lam)
        rhs = X.T @ e
        Lc, info = torch.linalg.cholesky_ex(S)
        if info.item() == 0:
            dth = torch.cholesky_solve(rhs[:, None], Lc)[:, 0]
        else:
            dth = torch.linalg.solve(S, rhs)
    return dth.float(), dict(lam=float(lam), E=float(Em.real), Eim=float(Em.imag))


def apply_update(model, dth):
    with torch.no_grad():
        i = 0
        for p in model.parameters():
            n = p.numel(); p.add_(dth[i:i + n].view_as(p)); i += n


# ---------------------------------------------------------------- statistics
def blocking(series):
    """series (T, C) numpy: time x chains.  Returns mean, naive error, chain-mean error, blocking error list."""
    s = np.asarray(series, dtype=np.float64)
    T, C = s.shape
    mean = s.mean()
    naive = s.std(ddof=1) / math.sqrt(s.size)
    cm = s.mean(0)
    chain_err = cm.std(ddof=1) / math.sqrt(C)
    # Flyvbjerg-Petersen on the chain-averaged time series, and on the flattened per-chain series
    out = []
    y = s.copy()
    while y.shape[0] >= 2:
        yb = y.mean(1)                     # chain average per time block -> error of the global mean
        # error from all (block, chain) entries treating blocks as independent
        n = y.size
        out.append(float(y.std(ddof=1) / math.sqrt(n)))
        if y.shape[0] % 2:
            y = y[:-1]
        y = 0.5 * (y[0::2] + y[1::2])
    return dict(mean=float(mean), naive=float(naive), chain_err=float(chain_err), blocking=out)


# ---------------------------------------------------------------- checkpoints
def save_ckpt(path, model, extra):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    torch.save(dict(state_dict=model.state_dict(), config=model.cfg, **extra), tmp)
    os.replace(tmp, path)
    with open(path.replace('.pt', '.config.json'), 'w') as f:
        json.dump(model.cfg, f, indent=1)


def load_ckpt(path, device='cuda', **override):
    d = torch.load(path, map_location=device, weights_only=False)
    cfg = dict(d['config']); cfg.update(override)
    m = build(cfg, device)
    m.load_state_dict(d['state_dict'])
    return m, d


def exact_ref_6x6_check():
    e = -0.586487; N = 36
    return 4 * N * e


def mc_evaluate(model, H, chains, rounds, gap=2.0, therm=50, seed=777, hold=225.0, rest=20.0, maxim=65536,
                log=print, ref_e=None):
    """Independent MC energy: fresh chains (new seed), thermalise, then `rounds` x (gap sweeps, E_loc of all chains).
    Holds the heavy lock in chunks <= hold s.  Error: max(blocking plateau over time, spread of chain means)."""
    dev = model.perms.device; N = model.N
    gen = torch.Generator(device=dev); gen.manual_seed(seed)
    series = []; x = None; accs = []; t_start = time.time()
    while len(series) < rounds:
        with HeavyLock() as lk:
            log('# eval lock after %.1f s at %s' % (lk.waited, time.strftime('%H:%M:%SZ', time.gmtime())))
            if x is None:
                x = random_sz0(chains, N, dev, gen); lp = logpsi_chunked(model, x, maxim)
                x, lp, acc = metropolis(model, H, x, lp, therm * N, gen, max_images=maxim)
                log('# eval thermalised %d sweeps acc %.3f' % (therm, acc))
            lp = logpsi_chunked(model, x, maxim)
            est = 0.0
            while len(series) < rounds and lk.held() + 1.3 * est < hold:
                t0 = time.time()
                x, lp, acc = metropolis(model, H, x, lp, max(1, int(gap * N)), gen, max_images=maxim)
                El = local_energy(model, H, x, lp, max_images=maxim)
                series.append(El.real.cpu().numpy()); accs.append(acc); est = time.time() - t0
                log('# eval round %d mean %.6f acc %.3f %.1fs' % (len(series), float(El.real.mean()), acc, est))
        if len(series) < rounds:
            time.sleep(rest)
    S = np.stack(series)
    b = blocking(S)
    lv = b['blocking']
    plateau = max(lv[:max(1, len(lv) - 2)])
    sigma = max(plateau, b['chain_err'])
    E = b['mean']
    r = dict(n_samples=int(S.size), chains=chains, rounds=rounds, gap_sweeps=gap, therm_sweeps=therm, seed=seed,
             acc=float(np.mean(accs)), E=E, sigma=sigma, sigma_chain_means=b['chain_err'], sigma_naive=b['naive'],
             blocking_levels=lv, var=float(S.var()), e_spinhalf=E / (4 * N), sigma_e_spinhalf=sigma / (4 * N),
             seconds=time.time() - t_start)
    if ref_e is not None:
        r.update(ref_e=ref_e, ref_E_pauli=4 * N * ref_e, rel_err=(E / (4 * N) - ref_e) / abs(ref_e),
                 rel_err_upper_3sigma=((E + 3 * sigma) / (4 * N) - ref_e) / abs(ref_e))
    return r
