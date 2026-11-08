"""Own ED reference for R3(a): 4x4 periodic J1-J2 (Pauli convention), Sz=0 sector (12870 states), scipy eigsh.
Checks: J2=0.5 vs VarBench -33.83169340557936; local-energy code reproduces E0 on the exact GS; symmetry
characters of the GS; sign-rule agreement (Marshall, stripe-x, stripe-y, symmetrised stripe prior).
Writes out/ed4x4.json and out/ed4x4_gs_J2_0.9.npy (basis ints + GS vector)."""
import sys, os, json, math, time
sys.path.insert(0, os.path.dirname(__file__))
import nqs
import numpy as np, torch, torch.nn as nn
import scipy.sparse as sp, scipy.sparse.linalg as sla
from itertools import combinations

OUT = os.path.join(os.path.dirname(__file__), '..', 'out')
L = 4; N = 16


def basis():
    ints = []
    for comb in combinations(range(N), N // 2):
        v = 0
        for k in comb:
            v |= 1 << k
        ints.append(v)
    ints = np.array(sorted(ints), dtype=np.int64)
    conf = ((ints[:, None] >> np.arange(N)[None]) & 1) * 2 - 1      # +1 = up
    return ints, conf.astype(np.float32)


def hamiltonian(ints, conf, J1, J2):
    I, J, W = nqs.bonds(L, J1, J2)
    D = len(ints); rows, cols, vals = [], [], []
    diag = (conf[:, I] * conf[:, J] * W[None]).sum(1)
    for b in range(len(I)):
        anti = conf[:, I[b]] != conf[:, J[b]]
        idx = np.nonzero(anti)[0]
        flipped = ints[idx] ^ ((1 << I[b]) | (1 << J[b]))
        tgt = np.searchsorted(ints, flipped)
        assert np.all(ints[tgt] == flipped)
        rows.append(idx); cols.append(tgt); vals.append(np.full(len(idx), 2.0 * W[b]))
    rows = np.concatenate(rows + [np.arange(D)]); cols = np.concatenate(cols + [np.arange(D)])
    vals = np.concatenate(vals + [diag])
    return sp.csr_matrix((vals, (rows, cols)), shape=(D, D))


def perm_index(ints, conf, perm, flip=False):
    """index of g s for every basis state s, with (g s)[k] = s[perm[k]]."""
    c = conf[:, perm] * (-1 if flip else 1)
    v = (((c > 0).astype(np.int64)) << np.arange(N)[None]).sum(1)
    t = np.searchsorted(ints, v); assert np.all(ints[t] == v)
    return t


class Table(nn.Module):
    def __init__(s, ints, logpsi):
        super().__init__()
        s.ints = torch.tensor(ints, device='cuda'); s.lp = logpsi
        s.register_buffer('perms', torch.zeros(1, N, dtype=torch.long, device='cuda'))
    def forward(s, x):
        v = (((x > 0).long()) << torch.arange(N, device=x.device)[None]).sum(1)
        t = torch.searchsorted(s.ints, v)
        return s.lp[t]


def main():
    res = {}
    ints, conf = basis(); D = len(ints); res['dim'] = int(D)
    P = nqs.c4v_perms(L)
    Tx = ((np.arange(L)[:, None] * L + (np.arange(L)[None, :] + 1) % L)).reshape(-1)
    for J2 in (0.5, 0.55, 0.9):
        Hm = hamiltonian(ints, conf, 1.0, J2)
        w, v = sla.eigsh(Hm, k=4, which='SA', tol=1e-13)
        o = np.argsort(w); w, v = w[o], v[:, o]
        gs = v[:, 0]
        r = dict(E0=float(w[0]), E1=float(w[1]), E2=float(w[2]), E3=float(w[3]), e_spinhalf=float(w[0] / (4 * N)))
        ch = {}
        for name, perm in P.items():
            ch[name] = float(gs @ gs[perm_index(ints, conf, perm)])
        ch['flip'] = float(gs @ gs[perm_index(ints, conf, np.arange(N), True)])
        ch['Tx'] = float(gs @ gs[perm_index(ints, conf, Tx)])
        r['characters'] = ch
        p = gs ** 2
        cc = conf.reshape(D, L, L)
        nup = lambda m: ((cc > 0) & m[None]).sum((1, 2))
        rr, cl = np.meshgrid(np.arange(L), np.arange(L), indexing='ij')
        signs = {'marshall': (-1.0) ** nup((rr + cl) % 2 == 1), 'stripe_x': (-1.0) ** nup(cl % 2 == 1),
                 'stripe_y': (-1.0) ** nup(rr % 2 == 1)}
        agree = {}
        for k, sg in signs.items():
            a = float((p * (np.sign(gs) == sg)).sum()); agree[k] = max(a, 1 - a)
        # symmetrised stripe prior with the GS irrep (uniform amplitude): its sign agreement and its energy
        for irrep in ('A1', 'B1'):
            amp = np.zeros(D)
            for name, perm in P.items():
                amp += nqs.CHARS[irrep][name] * signs['stripe_x'][perm_index(ints, conf, perm)]
            nz = np.abs(amp) > 1e-12
            a = float((p * (np.sign(amp) == np.sign(gs)) * nz).sum()); agree['sym_stripe_' + irrep] = max(a, float((p * nz).sum()) - a)
            agree['sym_stripe_' + irrep + '_support'] = float((p * nz).sum())
            if np.any(nz):
                agree['sym_stripe_' + irrep + '_E'] = float(amp @ (Hm @ amp) / (amp @ amp))
        r['sign_agreement_weighted'] = agree
        # local-energy check with the exact GS through the nqs.local_energy code path
        lp = torch.tensor(np.stack([np.log(np.abs(gs) + 1e-300), np.where(gs < 0, math.pi, 0.0)], 1),
                          dtype=torch.float32, device='cuda')
        tab = Table(ints, lp)
        Hq = nqs.Ham(L, 1.0, J2)
        x = torch.tensor(conf, device='cuda')
        El = nqs.local_energy(tab, Hq, x).cpu().numpy()
        r['Eloc_check_sum_p_Eloc'] = float((p * El.real).sum())
        r['Eloc_check_max_abs_dev_on_support'] = float(np.max(np.abs(El - w[0])[p > 1e-12]))
        res['J2=%g' % J2] = r
        print(J2, json.dumps(r, indent=1), flush=True)
        if J2 == 0.9:
            np.save(os.path.join(OUT, 'ed4x4_gs_J2_0.9.npy'), np.stack([ints.astype(np.float64), gs]))
    res['varbench_J2_0.5'] = -33.83169340557936
    res['dev_J2_0.5'] = res['J2=0.5']['E0'] - (-33.83169340557936)
    res['J2_0.55_minus_0.5'] = res['J2=0.55']['E0'] - res['J2=0.5']['E0']
    json.dump(res, open(os.path.join(OUT, 'ed4x4.json'), 'w'), indent=1)
    print('dev J2=0.5 vs VarBench', res['dev_J2_0.5'])


if __name__ == '__main__':
    main()
