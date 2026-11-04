"""estimator2.py -- independent energy estimator for VarBench J1J2 square_L^2_P states (lens exact-scorer-first,
run 2026-10-23-1501).  Written from the definitions; it does not use the sampler, local energy or statistics of the
model code.  From nqs.py (the state's own code) it uses only the network and the symmetry tables (perms, flips,
characters, prior mask) to evaluate the |G| image amplitudes psi0(g s); psi(s) = sum_g chi(g) psi0(g s) is recomposed
here and cross-checked against nqs.NQS.forward (instrument check I3).

Hamiltonian (VarBench, Pauli convention): H = J1 sum_<ij> sigma_i.sigma_j + J2 sum_<<ij>> sigma_i.sigma_j on the L x L
square lattice, periodic in x and y, each bond once.  Site i = y*L + x.  NN bonds: (x,y)-(x+1,y), (x,y)-(x,y+1);
diagonal bonds: (x,y)-(x+1,y+1), (x,y)-(x+1,y-1).  sigma_i.sigma_j = s_i s_j (diagonal, s = +-1) plus 2 x exchange
for an antiparallel pair.

Two statistics (PREREG.md):
  plain:  chains sample |psi|^2;  E = mean Re E_loc;  sigma = max(chain-mean spread, blocking of the chain-averaged
          series over rounds).
  IS:     chains sample q(s) ~ sum_g |psi0(g s)|^2;  w = |psi|^2 / q <= |G|;  E = sum w E_loc / sum w with
          w E_loc = sum_s' H_ss' conj(psi(s)) psi(s') / q(s) computed in log space (no division by psi(s));
          sigma = jackknife over chains;  Var(H) = sum |H psi|^2 / q / sum w - E^2.
Proposals (symmetric, Sz conserving): with prob. 1/2 a uniformly random bond (NN or diagonal), else a uniformly random
(up site, down site) pair; swap if antiparallel; Metropolis acceptance with the target log-density.
"""
import ctypes, glob, os, sys, json, time, math, fcntl, hashlib, argparse

def _site():
    import importlib.util
    sp = importlib.util.find_spec('nvidia')
    return os.path.dirname(list(sp.submodule_search_locations)[0]) if sp else ''
_venv = os.environ.get('V3R1T4S_SITE_PACKAGES') or _site()   # the folder holding nvidia/cuda_runtime
if os.environ.get('EST_DEVICE', 'cuda') == 'cuda':
    _rc = ctypes.CDLL(glob.glob(os.path.join(_venv, 'nvidia/cuda_runtime/lib/libcudart.so*'))[0]).cudaSetDeviceFlags(4)
    assert _rc == 0, 'cudaSetDeviceFlags(4) failed'
import numpy as np
import torch

DEV = os.environ.get('EST_DEVICE', 'cuda')
LOCK = os.environ.get('V3R1T4S_LOCK', '')   # optional machine-wide lock file
NOLOCK = os.environ.get('EST_NOLOCK') == '1' or not LOCK      # only for tiny CPU tests
torch.backends.cudnn.allow_tf32 = False
torch.backends.cuda.matmul.allow_tf32 = False


def utc():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


class Lock:
    def __enter__(self):
        t = time.time()
        if not NOLOCK:
            self.f = open(LOCK, 'a'); fcntl.flock(self.f, fcntl.LOCK_EX)
        self.waited = time.time() - t; self.t1 = time.time(); return self

    def held(self):
        return time.time() - self.t1

    def __exit__(self, *a):
        if DEV == 'cuda':
            torch.cuda.synchronize(); torch.cuda.empty_cache()
        if not NOLOCK:
            fcntl.flock(self.f, fcntl.LOCK_UN); self.f.close()


# ------------------------------------------------------------------ lattice (own copy, from the VarBench definition)
def lattice(L, J1=1.0, J2=0.9):
    I, J, W, K = [], [], [], []
    for y in range(L):
        for x in range(L):
            i = y * L + x
            for dx, dy, w, k in ((1, 0, J1, 1), (0, 1, J1, 1), (1, 1, J2, 2), (1, -1, J2, 2)):
                j = ((y + dy) % L) * L + (x + dx) % L
                I.append(i); J.append(j); W.append(w); K.append(k)
    I, J, W, K = map(np.array, (I, J, W, K))
    pairs = {(min(a, b), max(a, b)) for a, b in zip(I.tolist(), J.tolist())}
    assert len(pairs) == len(I) and not np.any(I == J), 'duplicate or self bond'
    return I, J, W.astype(np.float64), K


def lattice_check(L):
    I, J, W, K = lattice(L)
    N = L * L
    deg1 = np.bincount(np.concatenate([I[K == 1], J[K == 1]]), minlength=N)
    deg2 = np.bincount(np.concatenate([I[K == 2], J[K == 2]]), minlength=N)
    return dict(L=L, n_nn=int((K == 1).sum()), n_diag=int((K == 2).sum()), nn_degree=sorted(set(deg1.tolist())),
                diag_degree=sorted(set(deg2.tolist())), unique=True,
                ok=bool((K == 1).sum() == 2 * N and (K == 2).sum() == 2 * N and set(deg1.tolist()) == {4}
                        and set(deg2.tolist()) == {4}))


# ------------------------------------------------------------------ wave functions
class NQSWave:
    """Wraps an nqs.NQS model: image amplitudes from model.net, recomposed here."""
    def __init__(self, model, max_images=65536):
        self.m = model; self.N = model.N; self.G = model.perms.shape[0]; self.maxim = max_images

    @torch.no_grad()
    def images(self, x):
        m = self.m; B = x.shape[0]; G = self.G
        xs = x[:, m.perms] * m.flips[None, :, None]                       # (B, G, N)
        xs = xs.reshape(B * G, self.N)
        out = m.net(xs).view(B, G, 2).double()
        nup_odd = (((1.0 + xs) * 0.5) @ m.prior_mask).view(B, G).double()
        a = out[..., 0]
        ph = out[..., 1] + math.pi * nup_odd + m.chphase[None, :].double()
        return a, ph

    @torch.no_grad()
    def logs(self, x):
        """(log psi complex128 (B,), log q float64 (B,)) with q = sum_g |psi0(g s)|^2 (unnormalised)."""
        ch = max(1, self.maxim // self.G); lps, lqs = [], []
        for i in range(0, x.shape[0], ch):
            a, ph = self.images(x[i:i + ch])
            mx = a.max(1, keepdim=True).values
            z = (torch.exp(a - mx) * torch.exp(1j * ph)).sum(1)               # complex128
            lps.append(mx[:, 0] + torch.log(z))
            lqs.append(torch.logsumexp(2.0 * a, 1))
        return torch.cat(lps), torch.cat(lqs)


class TableWave:
    """Real amplitude table on the sorted Sz = 0 integer basis (bit k = site k, 1 = up)."""
    def __init__(self, basis, psi, N):
        self.N = N
        self.basis = torch.tensor(np.asarray(basis, dtype=np.int64), device=DEV)
        p = torch.tensor(np.asarray(psi, dtype=np.float64), device=DEV)
        self.lp = torch.log(p.abs().clamp_min(1e-300)).to(torch.complex128) + 1j * math.pi * (p < 0).double()
        self.lp = torch.where(p == 0, torch.full_like(self.lp, complex(-1e300, 0.0)), self.lp)
        self.w2 = (1 << torch.arange(N, device=DEV, dtype=torch.int64))

    @torch.no_grad()
    def logs(self, x):
        idx = (((x > 0).long()) * self.w2[None]).sum(1)
        k = torch.searchsorted(self.basis, idx)
        k = k.clamp_max(self.basis.numel() - 1)
        assert torch.all(self.basis[k] == idx), 'configuration outside the table'
        lp = self.lp[k]
        return lp, 2.0 * lp.real


# ------------------------------------------------------------------ Hamiltonian action
class Ham:
    def __init__(self, L, J1, J2):
        I, J, W, K = lattice(L, J1, J2)
        self.L, self.N = L, L * L
        self.I = torch.tensor(I, device=DEV); self.J = torch.tensor(J, device=DEV)
        self.W = torch.tensor(W, device=DEV, dtype=torch.float64)

    @torch.no_grad()
    def apply(self, wave, x, lp, lq, rows=131072, dis=False):
        """For each configuration s (row of x) with log psi(s) = lp and sampling log-density lq (unnormalised, same Z as
        |psi|^2), return Eloc = (H psi)(s)/psi(s), wE = conj(psi(s)) (H psi)(s)/q(s), h2q = |(H psi)(s)|^2/q(s),
        w = |psi(s)|^2/q(s), lnu = log nu(s), lq_used.  With dis=True the density is the defensive neighbour mixture
        m(s) = (|psi(s)|^2 + nu(s))/2, nu(s) = sum_{s''~s} |psi(s'')|^2 / n(s'') (lq is ignored).  All from exponent
        differences (no division by a small psi)."""
        B = x.shape[0]
        si, sj = x[:, self.I], x[:, self.J]
        diag = ((si * sj).double() * self.W[None]).sum(1)                         # (B,)
        anti = si != sj
        nb = int(anti.sum(1).max().item()) if B else 0
        per = max(1, rows // max(1, nb))
        G_, C_, L_, N_ = [], [], [], []
        for b0 in range(0, B, per):
            ab = anti[b0:b0 + per]
            ib, kb = ab.nonzero(as_tuple=True)
            xp = x[b0:b0 + per][ib].clone()
            ar = torch.arange(ib.numel(), device=x.device)
            xp[ar, self.I[kb]] *= -1; xp[ar, self.J[kb]] *= -1
            lpp, _ = wave.logs(xp)
            G_.append(b0 + ib); C_.append(2.0 * self.W[kb]); L_.append(lpp)
            if dis:
                N_.append((xp[:, self.I] != xp[:, self.J]).sum(1).double())
        g = torch.cat(G_); c = torch.cat(C_); lpp = torch.cat(L_)
        lnu = torch.full((B,), -float('inf'), dtype=torch.float64, device=x.device)
        if dis:
            v = 2.0 * lpp.real - torch.log(torch.cat(N_))
            mx = torch.full((B,), -float('inf'), dtype=torch.float64, device=x.device).scatter_reduce(
                0, g, v, reduce='amax', include_self=True)
            acc = torch.zeros(B, dtype=torch.float64, device=x.device).index_add_(0, g, torch.exp(v - mx[g]))
            lnu = mx + torch.log(acc)
            lq = torch.logaddexp(2.0 * lp.real, lnu) - math.log(2.0)
        off_r = torch.zeros(B, dtype=torch.complex128, device=x.device).index_add_(0, g, c * torch.exp(lpp - lp[g]))
        off_w = torch.zeros(B, dtype=torch.complex128, device=x.device).index_add_(
            0, g, c * torch.exp(lpp + lp[g].conj() - lq[g]))
        off_h = torch.zeros(B, dtype=torch.complex128, device=x.device).index_add_(
            0, g, c * torch.exp(lpp - 0.5 * lq[g]))
        Eloc = diag + off_r
        wd = torch.exp(2.0 * lp.real - lq)
        wE = diag * wd + off_w
        hq = diag * torch.exp(lp - 0.5 * lq) + off_h
        return Eloc, wE, (hq.abs() ** 2), wd, lnu, lq


def neighbour_replace(x, ham, gen):
    """With probability 1/2 per row, replace s' by a uniformly random H-neighbour (exchange across a uniformly chosen
    antiparallel H-bond).  Returns the measured configurations (the chains are not changed)."""
    C = x.shape[0]; ar = torch.arange(C, device=x.device)
    anti = (x[:, ham.I] != x[:, ham.J]).float()
    k = torch.multinomial(anti, 1, generator=gen)[:, 0]
    rep = torch.rand(C, device=x.device, generator=gen) < 0.5
    fl = torch.where(rep, -1.0, 1.0)
    xs = x.clone(); xs[ar, ham.I[k]] *= fl; xs[ar, ham.J[k]] *= fl
    return xs, rep


# ------------------------------------------------------------------ sampler
def random_sz0(C, N, gen):
    r = torch.rand(C, N, device=DEV, generator=gen)
    idx = r.argsort(1)
    x = torch.full((C, N), -1.0, device=DEV)
    x.scatter_(1, idx[:, :N // 2], 1.0)
    return x


class Sampler:
    def __init__(self, wave, ham, mode, gen):
        assert mode in ('plain', 'is', 'dis')
        self.wave, self.ham, self.mode, self.gen = wave, ham, mode, gen

    def target(self, lp, lq):
        return lq if self.mode == 'is' else 2.0 * lp.real

    @torch.no_grad()
    def steps(self, x, lp, lq, n):
        C, N = x.shape; ar = torch.arange(C, device=DEV); nb = self.ham.I.numel(); acc = 0
        for _ in range(n):
            use_bond = torch.rand(C, device=DEV, generator=self.gen) < 0.5
            k = torch.randint(0, nb, (C,), device=DEV, generator=self.gen)
            bi, bj = self.ham.I[k], self.ham.J[k]
            up = (x > 0).float(); dn = 1.0 - up
            ui = torch.multinomial(up, 1, generator=self.gen)[:, 0]
            di = torch.multinomial(dn, 1, generator=self.gen)[:, 0]
            i = torch.where(use_bond, bi, ui); j = torch.where(use_bond, bj, di)
            anti = x[ar, i] != x[ar, j]
            fl = torch.where(anti, -1.0, 1.0)              # a parallel pair is no move (stays in the sector)
            xp = x.clone(); xp[ar, i] *= fl; xp[ar, j] *= fl
            lpp, lqp = self.wave.logs(xp)
            u = torch.rand(C, device=DEV, generator=self.gen, dtype=torch.float64)
            ok = anti & (torch.log(u) < self.target(lpp, lqp) - self.target(lp, lq))
            x = torch.where(ok[:, None], xp, x)
            lp = torch.where(ok, lpp, lp); lq = torch.where(ok, lqp, lq)
            acc += int(ok.sum().item())
        return x, lp, lq, acc / max(1, n * C)


# ------------------------------------------------------------------ statistics
def fp_blocking(y):
    """Flyvbjerg-Petersen errors of the mean of the 1D series y, one per blocking level."""
    y = np.asarray(y, dtype=np.float64); out = []
    while y.size >= 4:
        out.append(float(y.std(ddof=1) / math.sqrt(y.size)))
        if y.size % 2:
            y = y[:-1]
        y = 0.5 * (y[0::2] + y[1::2])
    return out


def stats_plain(e):
    """e (T, C) real local energies."""
    T, C = e.shape
    cm = e.mean(0)
    E = float(e.mean()); s_chain = float(cm.std(ddof=1) / math.sqrt(C))
    bl = fp_blocking(e.mean(1)); s_block = max(bl[:max(1, len(bl) - 1)]) if bl else float('nan')
    return dict(E=E, sigma=max(s_chain, s_block), sigma_chain_means=s_chain, sigma_blocking=s_block,
                blocking_levels=bl, sample_var=float(e.var()), n=int(e.size), max_abs_dev=float(np.abs(e - E).max()))


def stats_is(w, wE, h2q):
    """w, wE (real part), h2q: (T, C)."""
    T, C = w.shape
    A = wE.sum(0); Bw = w.sum(0); Hq = h2q.sum(0)
    SA, SB, SH = A.sum(), Bw.sum(), Hq.sum()
    E = float(SA / SB)
    jk = (SA - A) / (SB - Bw)
    s_jk = float(math.sqrt((C - 1) / C * ((jk - jk.mean()) ** 2).sum()))
    varH = float(SH / SB - E * E)
    ess = float(w.sum() ** 2 / (w ** 2).sum())
    jkv = (SH - Hq) / (SB - Bw) - jk ** 2
    s_var = float(math.sqrt((C - 1) / C * ((jkv - jkv.mean()) ** 2).sum()))
    return dict(E=E, sigma=s_jk, varH=varH, sigma_varH=s_var, kish_ess=ess, kish_ess_fraction=ess / w.size,
                w_mean=float(w.mean()), w_max=float(w.max()), w_min=float(w.min()), n=int(w.size))


# ------------------------------------------------------------------ driver
def run(wave, ham, mode, chains, therm, gap, min_rounds, max_rounds, seed, hold=225.0, rest=20.0, log=print,
        stop=None, save=None):
    """Thermalise from random Sz = 0 states, then rounds of (gap sweeps, measure all chains).  stop(stats) -> bool is
    checked every 25 rounds after min_rounds.  Returns (stats, arrays)."""
    N = ham.N
    gen = torch.Generator(device=DEV); gen.manual_seed(seed)
    S = Sampler(wave, ham, mode, gen)
    rec = dict(e=[], eim=[], w=[], wE=[], h2q=[]); accs = []; x = None; t0 = time.time(); done = False; est = 0.0
    nthermed = 0; nrep = 0
    while not done:
        with Lock() as lk:
            log('# lock after %.1f s at %s' % (lk.waited, utc()))
            if x is None:
                x = random_sz0(chains, N, gen); lp, lq = wave.logs(x)
            while nthermed < therm and lk.held() < hold:
                x, lp, lq, a = S.steps(x, lp, lq, N); nthermed += 1
                if nthermed == therm:
                    log('# thermalised %d sweeps, last acc %.3f, %s' % (therm, a, utc()))
            while nthermed >= therm and not done and lk.held() + 1.3 * est < hold:
                t1 = time.time()
                x, lp, lq, a = S.steps(x, lp, lq, max(1, int(round(gap * N))))
                if mode == 'dis':
                    xs, rep = neighbour_replace(x, ham, gen); lps, _ = wave.logs(xs)
                    El, wE, h2q, wd, _, _ = ham.apply(wave, xs, lps, None, dis=True)
                    nrep += int(rep.sum().item())
                else:
                    El, wE, h2q, wd, _, _ = ham.apply(wave, x, lp, lq)
                rec['e'].append(El.real.cpu().numpy()); rec['eim'].append(El.imag.cpu().numpy())
                rec['w'].append(wd.cpu().numpy()); rec['wE'].append(wE.real.cpu().numpy())
                rec['h2q'].append(h2q.cpu().numpy()); accs.append(a)
                est = time.time() - t1; R = len(rec['e'])
                if R % 5 == 0:
                    log('# round %d acc %.3f %.1f s %s' % (R, a, est, utc()))
                if R >= max_rounds:
                    done = True
                elif R >= min_rounds and R % 25 == 0 and stop is not None:
                    done = bool(stop(summarise(mode, rec, accs)))
        if save is not None:
            np.savez(save, final_chains=x.cpu().numpy().astype(np.int8), **{k: np.stack(v) for k, v in rec.items() if v})
        if not done:
            time.sleep(rest)
    st = summarise(mode, rec, accs)
    st.update(seconds=time.time() - t0, chains=chains, therm_sweeps=therm, gap_sweeps=gap, seed=seed, mode=mode,
              rounds=len(rec['e']), replaced_fraction=(nrep / max(1, len(rec['e']) * chains)) if mode == 'dis' else None)
    rec['final_chains'] = x
    return st, rec


def summarise(mode, rec, accs):
    e = np.stack(rec['e']); w = np.stack(rec['w']); wE = np.stack(rec['wE']); h = np.stack(rec['h2q'])
    st = dict(acc=float(np.mean(accs)), max_abs_Im_Eloc=float(np.abs(np.stack(rec['eim'])).max()))
    if mode == 'plain':
        st.update(stats_plain(e))
    elif mode == 'dis':
        st.update(stats_is(w, wE, h)); st['plain_part_of_dis'] = None
    else:
        st.update(stats_is(w, wE, h))
    return st


def sha256(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def load_nqs(ckpt, nqs_dir):
    sys.path.insert(0, nqs_dir)
    os.environ['NQS_DEVICE'] = DEV
    import nqs
    model, d = nqs.load_ckpt(ckpt, DEV)
    model.eval()
    return nqs, model, d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ckpt'); ap.add_argument('--nqs_dir', required=True)
    ap.add_argument('--J2', type=float, default=0.9); ap.add_argument('--mode', choices=['plain', 'is', 'dis'], required=True)
    ap.add_argument('--chains', type=int, default=2048); ap.add_argument('--therm', type=int, default=50)
    ap.add_argument('--gap', type=float, default=2.0); ap.add_argument('--min_rounds', type=int, default=50)
    ap.add_argument('--max_rounds', type=int, default=400); ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--neff', type=float, default=1e5); ap.add_argument('--varH', type=float, default=None,
                    help='Var(H) used for N_eff (default: plain -> sample variance, is -> own estimate)')
    ap.add_argument('--hold', type=float, default=225.0); ap.add_argument('--out', required=True)
    ap.add_argument('--max_images', type=int, default=65536)
    a = ap.parse_args()
    if DEV == 'cuda':
        torch.cuda.set_per_process_memory_fraction(5.0 / 16.0)
    nqs, model, d = load_nqs(a.ckpt, a.nqs_dir)
    wave = NQSWave(model, a.max_images); ham = Ham(model.L, 1.0, a.J2)
    logf = open(a.out + '.log', 'a')
    def log(s):
        print(s, flush=True); logf.write(s + '\n'); logf.flush()
    info = dict(ckpt=os.path.abspath(a.ckpt), ckpt_sha256=sha256(a.ckpt), step=d.get('opt_state', {}).get('step'),
                config=model.cfg, J2=a.J2, args=vars(a), start=utc(), estimator_sha256=sha256(__file__))
    log('# ' + json.dumps(info))
    def stop(st):
        v = a.varH if a.varH is not None else (st['sample_var'] if a.mode == 'plain' else st['varH'])
        neff = v / st['sigma'] ** 2
        log('# check: E %.6f sigma %.6f N_eff %.0f' % (st['E'], st['sigma'], neff))
        return neff >= a.neff
    st, rec = run(wave, ham, a.mode, a.chains, a.therm, a.gap, a.min_rounds, a.max_rounds, a.seed, a.hold, log=log,
                  stop=stop, save=a.out + '.npz')
    v = a.varH if a.varH is not None else (st['sample_var'] if a.mode == 'plain' else st['varH'])
    st['varH_for_neff'] = v; st['N_eff'] = v / st['sigma'] ** 2
    N = model.N
    st['e_spinhalf'] = st['E'] / (4 * N); st['sigma_e_spinhalf'] = st['sigma'] / (4 * N)
    info.update(result=st, end=utc())
    json.dump(info, open(a.out + '.json', 'w'), indent=1)
    log('# RESULT ' + json.dumps(st))


if __name__ == '__main__':
    main()
