"""Instrument checks I1, I2, I3 of PREREG.md (run 2026-10-23-1501), using estimator2.py.
Usage: python checks.py I1|I2|I3 <outdir>
I1: exact 4x4 J2 = 0.9 ground state (table) + perturbed known negative.
I2: trained 4x4 NQS (ckpt r4_J0.9.pt): exact <H>, Var(H) by enumeration vs plain MC (seed 501) and IS (seed 502).
I3: lattice check at 10x10; estimator2 psi and E_loc vs nqs.py on 256 random 10x10 Sz = 0 configurations (seed 7).
"""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(1, os.path.join(HERE, 'ref'))
import estimator2 as E2
import numpy as np, torch

R1610 = 'runs/2026-10-22-1610/attempts'
NQS_DIR = 'runs/2026-10-23-1501/attempts/representation-transfer/code'
GS = R1610 + '/exact-scorer-first/out/gs_4x4_J2_0.9.npz'
R4 = R1610 + '/representation-transfer/ckpt/r4_J0.9.pt'
R10 = R1610 + '/representation-transfer/ckpt/r10_J0.9_B1.pt'


def basis_configs(basis, N):
    b = np.asarray(basis, dtype=np.int64)
    bits = (b[:, None] >> np.arange(N)[None, :]) & 1
    return torch.tensor(2.0 * bits - 1.0, dtype=torch.float32, device=E2.DEV)


def enumerate_exact(wave, ham, x):
    with E2.Lock():
        lp, lq = wave.logs(x)
        El, wE, h2q, wd, _, _ = ham.apply(wave, x, lp, lq)
    lp = lp.cpu().numpy(); El = El.cpu().numpy()
    p = np.exp(2 * (lp.real - lp.real.max())); p /= p.sum()
    E = float((p * El.real).sum())
    return lp, El, p, E


def I1(out):
    d = np.load(GS); N = 16; E0 = float(d['E0']); basis = d['basis']; psi = d['psi']
    ham = E2.Ham(4, 1.0, 0.9); x = basis_configs(basis, N)
    res = dict(E0=E0, start=E2.utc())
    wave = E2.TableWave(basis, psi, N)
    lp, El, p, E = enumerate_exact(wave, ham, x)
    m = np.abs(psi) ** 2 > 1e-12 * (np.abs(psi) ** 2).max()
    res['max_abs_Eloc_minus_E0'] = float(np.abs(El[m] - E0).max()); res['enum_E'] = E
    st, _ = E2.run(wave, ham, 'plain', 2048, 50, 2.0, 49, 49, seed=101, log=lambda s: None)
    res['mc_exact_state'] = st
    res['mc_minus_E0'] = st['E'] - E0
    # known negative: psi' = psi (1 + 0.5 u)
    u = np.random.default_rng(11).random(psi.size); psi2 = psi * (1 + 0.5 * u)
    import ed
    Hm, b2 = ed.build_H(4, 1.0, 0.9)
    assert np.array_equal(b2, basis)
    E_sp = float(psi2 @ (Hm @ psi2) / (psi2 @ psi2))
    wave2 = E2.TableWave(basis, psi2, N)
    _, El2, p2, Eex2 = enumerate_exact(wave2, ham, x)
    st2, _ = E2.run(wave2, ham, 'plain', 2048, 50, 2.0, 49, 49, seed=102, log=lambda s: None)
    res['perturbed'] = dict(E_exact_enum=Eex2, E_exact_sparse_ref=E_sp, above_E0=Eex2 - E0, mc=st2,
                            z=(st2['E'] - Eex2) / st2['sigma'])
    res['I1_pass'] = bool(res['max_abs_Eloc_minus_E0'] < 1e-8 and abs(res['mc_minus_E0']) < 1e-8
                          and Eex2 - E0 > 1e-3 and abs(st2['E'] - Eex2) < 3 * st2['sigma'])
    res['end'] = E2.utc()
    json.dump(res, open(os.path.join(out, 'I1.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k not in ('mc_exact_state',)}, default=str)[:3000])


def I2(out):
    nqs, model, d = E2.load_nqs(R4, NQS_DIR)
    wave = E2.NQSWave(model); ham = E2.Ham(4, 1.0, 0.9)
    dd = np.load(GS); basis = dd['basis']; x = basis_configs(basis, 16)
    res = dict(ckpt=R4, ckpt_sha256=E2.sha256(R4), step=d['opt_state']['step'], config=model.cfg, start=E2.utc())
    lp, El, p, E = enumerate_exact(wave, ham, x)
    import ed
    Hm, b2 = ed.build_H(4, 1.0, 0.9); assert np.array_equal(b2, basis)
    psi = np.exp(lp - lp.real.max())
    nrm = np.vdot(psi, psi).real
    Hpsi = Hm @ psi
    E_sp = float(np.vdot(psi, Hpsi).real / nrm); Var_sp = float(np.vdot(Hpsi, Hpsi).real / nrm - E_sp ** 2)
    var_eloc = float((p * np.abs(El - E_sp) ** 2).sum())
    w_img = None
    res['exact'] = dict(E=E_sp, E_from_Eloc=E, Var=Var_sp, Var_from_Eloc_sum=var_eloc,
                        weight_p_below_1em6=float(p[p < 1e-6].sum()),
                        var_share_p_below_1em6=float((p * np.abs(El - E_sp) ** 2)[p < 1e-6].sum() / var_eloc),
                        var_share_p_below_1em8=float((p * np.abs(El - E_sp) ** 2)[p < 1e-8].sum() / var_eloc),
                        max_abs_Eloc=float(np.abs(El).max()))
    st_mc, rec_mc = E2.run(wave, ham, 'plain', 2048, 50, 2.0, 64, 64, seed=501, log=lambda s: None)
    st_is, rec_is = E2.run(wave, ham, 'is', 2048, 50, 2.0, 64, 64, seed=502, log=lambda s: None)
    Eex = E_sp
    z4 = (st_mc['E'] - Eex) / st_mc['sigma']; b4 = (st_mc['E'] - Eex) / abs(Eex)
    res['plain'] = st_mc; res['is'] = st_is
    res['I2a'] = dict(E_IS_minus_exact=st_is['E'] - Eex, z_IS=(st_is['E'] - Eex) / st_is['sigma'],
                      varH_IS=st_is['varH'], varH_ratio=st_is['varH'] / Var_sp,
                      pass_=bool(abs(st_is['E'] - Eex) < 3 * st_is['sigma'] and abs(st_is['varH'] / Var_sp - 1) < 0.25))
    res['I2b'] = dict(E_MC_minus_exact=st_mc['E'] - Eex, z4=z4, b4=b4, sample_var_MC=st_mc['sample_var'],
                      sample_var_over_exact=st_mc['sample_var'] / Var_sp, gate_applies=bool(abs(z4) > 3))
    res['end'] = E2.utc()
    json.dump(res, open(os.path.join(out, 'I2.json'), 'w'), indent=1)
    print(json.dumps(dict(exact=res['exact'], I2a=res['I2a'], I2b=res['I2b'],
                          plain=dict(E=st_mc['E'], sigma=st_mc['sigma'], acc=st_mc['acc']),
                          is_=dict(E=st_is['E'], sigma=st_is['sigma'], ess=st_is['kish_ess_fraction'])), default=str))


def I3(out):
    res = dict(lattice=E2.lattice_check(10), start=E2.utc())
    nqs, model, d = E2.load_nqs(R10, NQS_DIR)
    wave = E2.NQSWave(model); ham = E2.Ham(10, 1.0, 0.9)
    gen = torch.Generator(device=E2.DEV); gen.manual_seed(7)
    x = E2.random_sz0(256, 100, gen)
    with E2.Lock():
        lp, lq = wave.logs(x)
        ref = nqs.logpsi_chunked(model, x, 65536).double()
        El, wE, h2q, wd, _, _ = ham.apply(wave, x, lp, lq)
        Href = nqs.Ham(10, 1.0, 0.9, E2.DEV)
        Elr = nqs.local_energy(model, Href, x, max_images=65536)
    lp = lp.cpu().numpy(); ref = ref.cpu().numpy(); El = El.cpu().numpy(); Elr = Elr.cpu().numpy()
    keep = lp.real > lp.real.max() + math.log(1e-6)
    dabs = np.abs(lp.real - ref[:, 0]); dph = np.abs(np.angle(np.exp(1j * (lp.imag - ref[:, 1]))))
    res['n_kept'] = int(keep.sum())
    res['max_dlogabs'] = float(dabs[keep].max()); res['max_dphase'] = float(dph[keep].max())
    res['max_dEloc'] = float(np.abs(El - Elr).max()); res['tol_Eloc'] = 1e-6 * 253.668
    res['max_abs_Eloc'] = float(np.abs(El).max())
    res['w_le_16'] = bool((wd.cpu().numpy() <= 16 * (1 + 1e-9)).all())
    res['I3_pass'] = bool(res['lattice']['ok'] and res['max_dlogabs'] < 1e-4 and res['max_dphase'] < 1e-4
                          and res['max_dEloc'] < res['tol_Eloc'])
    res['end'] = E2.utc()
    json.dump(res, open(os.path.join(out, 'I3.json'), 'w'), indent=1)
    print(json.dumps(res, default=str))


def I2v2(out):
    """PREREG.v2 I2': DIS estimator on the trained 4x4 state (seed 503), identity sum nu = sum |psi|^2, plain seed 504."""
    nqs, model, d = E2.load_nqs(R4, NQS_DIR)
    wave = E2.NQSWave(model); ham = E2.Ham(4, 1.0, 0.9)
    dd = np.load(GS); basis = dd['basis']; x = basis_configs(basis, 16)
    res = dict(ckpt=R4, ckpt_sha256=E2.sha256(R4), start=E2.utc(), Var_ex_PREREG=0.09134263343298699)
    lp, El, p, E = enumerate_exact(wave, ham, x)
    with E2.Lock():
        lpt, lqt = wave.logs(x)
        _, _, _, _, lnu, _ = ham.apply(wave, x, lpt, None, dis=True)
    lnu = lnu.cpu().numpy(); ref = lp.real.max()
    s_psi = np.exp(2 * (lp.real - ref)).sum(); s_nu = np.exp(lnu - 2 * ref).sum()
    res['identity'] = dict(sum_psi2=float(s_psi), sum_nu=float(s_nu), rel_diff=float(abs(s_nu / s_psi - 1)))
    import ed
    Hm, b2 = ed.build_H(4, 1.0, 0.9); assert np.array_equal(b2, basis)
    psi = np.exp(lp - lp.real.max()); nrm = np.vdot(psi, psi).real; Hpsi = Hm @ psi
    Eex = float(np.vdot(psi, Hpsi).real / nrm); Var_ex = float(np.vdot(Hpsi, Hpsi).real / nrm - Eex ** 2)
    res['exact'] = dict(E=Eex, Var=Var_ex)
    st_d, _ = E2.run(wave, ham, 'dis', 2048, 50, 2.0, 64, 64, seed=503, log=lambda s: None)
    st_p, _ = E2.run(wave, ham, 'plain', 2048, 50, 2.0, 64, 64, seed=504, log=lambda s: None)
    res['dis'] = st_d; res['plain'] = st_p
    zd = (st_d['E'] - Eex) / st_d['sigma']; vr = st_d['varH'] / Var_ex
    z4 = (st_p['E'] - Eex) / st_p['sigma']
    res['I2prime'] = dict(E_DIS_minus_exact=st_d['E'] - Eex, z_DIS=zd, varH_DIS=st_d['varH'], varH_ratio=vr,
                          identity_ok=bool(res['identity']['rel_diff'] < 1e-10),
                          pass_=bool(abs(zd) < 3 and abs(vr - 1) < 0.25 and res['identity']['rel_diff'] < 1e-10))
    res['I2b_fresh'] = dict(E_MC_minus_exact=st_p['E'] - Eex, z4=z4, b4=(st_p['E'] - Eex) / abs(Eex),
                            gate_applies=bool(abs(z4) > 3), sample_var_over_exact=st_p['sample_var'] / Var_ex)
    res['end'] = E2.utc()
    json.dump(res, open(os.path.join(out, 'I2v2.json'), 'w'), indent=1)
    print(json.dumps(dict(identity=res['identity'], exact=res['exact'], I2prime=res['I2prime'], I2b_fresh=res['I2b_fresh'],
                          dis=dict(E=st_d['E'], sigma=st_d['sigma'], ess=st_d['kish_ess_fraction'],
                                   w_max=st_d['w_max'], replaced=st_d['replaced_fraction']),
                          plain=dict(E=st_p['E'], sigma=st_p['sigma'])), default=str))


def I3v2(out):
    """PREREG.v2 I3'(b): estimator2 vs nqs.py both with a float64 copy of the model; float32 differences recorded."""
    import copy
    nqs, model, d = E2.load_nqs(R10, NQS_DIR)
    m64 = copy.deepcopy(model).double()
    w32 = E2.NQSWave(model); w64 = E2.NQSWave(m64); ham = E2.Ham(10, 1.0, 0.9)
    gen = torch.Generator(device=E2.DEV); gen.manual_seed(7)
    x = E2.random_sz0(256, 100, gen); x64 = x.double()
    Href = nqs.Ham(10, 1.0, 0.9, E2.DEV)
    with E2.Lock():
        lp64, lq64 = w64.logs(x64); El64, *_ = ham.apply(w64, x64, lp64, lq64)
        ref64 = nqs.logpsi_chunked(m64, x64, 65536).double(); Elr64 = nqs.local_energy(m64, Href, x64, max_images=65536)
        lp32, lq32 = w32.logs(x); El32, *_ = ham.apply(w32, x, lp32, lq32)
        ref32 = nqs.logpsi_chunked(model, x, 65536).double(); Elr32 = nqs.local_energy(model, Href, x, max_images=65536)
    f = lambda t: t.cpu().numpy()
    lp64, ref64, El64, Elr64, lp32, ref32, El32, Elr32 = map(f, (lp64, ref64, El64, Elr64, lp32, ref32, El32, Elr32))
    ph = lambda a, b: np.abs(np.angle(np.exp(1j * (a - b))))
    res = dict(start=E2.utc(), n=256)
    res['est64_vs_nqs64'] = dict(max_dlogabs=float(np.abs(lp64.real - ref64[:, 0]).max()),
                                 max_dphase=float(ph(lp64.imag, ref64[:, 1]).max()),
                                 max_dEloc=float(np.abs(El64 - Elr64).max()))
    res['est32_vs_all64'] = dict(max_dlogabs=float(np.abs(lp32.real - lp64.real).max()),
                                 max_dEloc=float(np.abs(El32 - El64).max()), mean_dEloc=float((El32 - El64).real.mean()))
    res['nqs32_vs_all64'] = dict(max_dlogabs=float(np.abs(ref32[:, 0] - lp64.real).max()),
                                 max_dEloc=float(np.abs(Elr32 - El64).max()), mean_dEloc=float((Elr32 - El64).real.mean()))
    r = res['est64_vs_nqs64']
    res['I3prime_b_pass'] = bool(r['max_dlogabs'] < 1e-8 and r['max_dphase'] < 1e-8 and r['max_dEloc'] < 1e-7)
    res['end'] = E2.utc()
    json.dump(res, open(os.path.join(out, 'I3v2.json'), 'w'), indent=1)
    print(json.dumps(res, default=str))


if __name__ == '__main__':
    if E2.DEV == 'cuda':
        torch.cuda.set_per_process_memory_fraction(5.0 / 16.0)
    {'I1': I1, 'I2': I2, 'I3': I3, 'I2v2': I2v2, 'I3v2': I3v2}[sys.argv[1]](sys.argv[2])
