"""Claim run a100_1030, PREREG.md: N0 (bank null for the 1973-10-30 candidate), M1 (max-T family-wise null over the
12 templates), M2 (GEV tail, model-based), A6 (specificity of the bank tests against the A100 stack) and the
forward-scan part of A3b (S16 NCC of catalogued A100 events). Also the determinism check against the saved scan.

usage: n0_analyse.py TOOLS_DIR SCAN12.jsonl SAVED_SCAN12.jsonl LEVENT.csv N_ALL,N_1973 OUT_PREFIX
"""
import sys, json
sys.path.insert(0, sys.argv[1])
import numpy as np
import pandas as pd
from ephem import mean_anomaly_deg

SCAN, SAVED, LEV, OUT = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[6]
NPAR, NPAR73 = [int(x) for x in sys.argv[5].split(',')]  # parent-run two-station template-year scans: all, 1973 only
NS = 1_000_000_000
WS = int(np.datetime64('1973-10-30T02:25:21.509', 'ns').astype(np.int64))
FIRST_WS = int(np.datetime64('1973-11-26T07:45:58.641', 'ns').astype(np.int64))
out = {}
days = [json.loads(l) for l in open(SCAN)]
days.sort(key=lambda d: d['doy'])
nests = list(days[0]['nests'].keys())
print('days scanned: %d (doy %d..%d); nests: %s' % (len(days), days[0]['doy'], days[-1]['doy'], nests))

# determinism vs the saved scan of the lens
saved = {json.loads(l)['doy']: json.loads(l) for l in open(SAVED)}
same = 0; diff = []
for d in days:
    s = saved.get(d['doy'])
    if s is not None and all(s['nests'][n][k] == d['nests'][n][k] for n in nests for k in ('fwd_peaks', 'rev_max', 'shift_max')):
        same += 1
    else:
        diff.append(d['doy'])
print('determinism: days identical to the saved lens scan in fwd_peaks, rev_max, shift_max for all 12 nests: %d of %d; differing days: %s' % (same, len(days), diff[:20]))
out['determinism'] = dict(identical_days=same, days=len(days), differing=diff)

# per-nest full-span maxima of the 401 controls
Mx = {}
for n in nests:
    c0 = max(d['nests'][n]['rev_max'] for d in days if d['nests'][n].get('rev_max') is not None)
    nsh = max(len(d['nests'][n].get('shift_max') or []) for d in days)
    ck = [max(d['nests'][n]['shift_max'][k] for d in days if d['nests'][n].get('shift_max') and d['nests'][n]['shift_max'][k] is not None)
          for k in range(nsh)]
    Mx[n] = np.array([c0] + ck)
    print('A%-4s controls %d  C0 %.4f  best shift %.4f  best control %.4f  median %.4f' % (n, len(Mx[n]), c0, max(ck), Mx[n].max(), np.median(Mx[n])))
out['null_max'] = {n: dict(C0=float(Mx[n][0]), best_shift=float(Mx[n][1:].max()), best_control=float(Mx[n].max()),
                           n_controls=int(len(Mx[n]))) for n in nests}

# the candidate in this rerun
pk = [p for d in days if d['doy'] == 303 for p in d['nests']['100']['fwd_peaks'] if abs(p[0] - WS) <= 10 * NS]
assert len(pk) == 1, pk
cand = pk[0]
real = cand[1]
best = float(Mx['100'].max())
print('\ncandidate A100 peak: window start %s Dt %.5f ccs %s lags S14 %+.3f s S16 %+.3f s' % (
    str(np.datetime64(cand[0], 'ns'))[:23], real, cand[2], cand[3], cand[4]))
print('N0: real %.5f vs best of 401 A100 controls %.5f (C0 %.5f): real beats all controls: %s' % (real, best, Mx['100'][0], real > best))
out['candidate'] = dict(window_start=str(np.datetime64(cand[0], 'ns'))[:23] + 'Z', Dt=real, ccs=cand[2], lag_s14_s=cand[3], lag_s16_s=cand[4],
                        R7=bool(max(c for c in cand[2][:2] if c is not None) >= 0.5 and max(c for c in cand[2][2:] if c is not None) >= 0.5))
out['N0'] = dict(controls=int(len(Mx['100'])), best_control=best, C0=float(Mx['100'][0]), real=real, beats_all=bool(real > best),
                 n_controls_at_or_above_real=int((Mx['100'] >= real).sum()))
np.savetxt(OUT + '_A100_control_maxima.csv', Mx['100'], fmt='%.5f', header='full-span maxima: row 1 = C0 time-reversed, rows 2-401 = C1..C400 S16 rolled by 3600 + 180 k s', comments='# ')
# rank among all A100 forward peaks
allp = sorted([p for d in days for p in d['nests']['100']['fwd_peaks']], key=lambda p: -p[1])
rank = [i for i, p in enumerate(allp) if p[0] == cand[0]][0] + 1
print('candidate rank among %d A100 forward peaks of 1973: %d; peaks above the null: %d' % (len(allp), rank, sum(p[1] > best for p in allp)))
out['candidate']['rank_among_A100_forward_peaks'] = rank

# catalogue for labels, A6 and A3b
cat = pd.read_csv(LEV, dtype=str)
day0 = np.datetime64('1973-01-01T00:00', 'ns').astype(np.int64)
allc = cat.copy()
allc['N2'] = allc['N2'].fillna('').str.strip()
c73 = allc[allc['Y'] == '73'].copy()
c73['t'] = [int(day0 + ((int(r.JD) - 1) * 86400 + int(str(r.S).zfill(4)[:2]) * 3600 + int(str(r.S).zfill(4)[2:]) * 60) * NS) for r in c73.itertuples()]


def label(t_onset):
    m = c73[(c73['t'] >= t_onset - 600 * NS) & (c73['t'] <= t_onset + 300 * NS)]
    return '; '.join('73-%s %s T2=%s N2=%s' % (r.JD, str(r.S).zfill(4), r.T2, r.N2) for r in m.itertuples()) or 'uncatalogued'


print('\nA100 forward peaks above the null (%.4f):' % best)
for p in allp:
    if p[1] <= best:
        break
    print('  %s Dt %.4f ccs %s lags %+.3f %+.3f | %s%s' % (str(np.datetime64(p[0] + 30 * NS, 'ns'))[:23], p[1], p[2], p[3], p[4], label(p[0] + 30 * NS),
                                                       '  <- this candidate' if p[0] == cand[0] else ('  <- first claim' if abs(p[0] - FIRST_WS) < 10 * NS else '')))

# M1: max-T family-wise null over the 12 templates
Z = {}
for n in nests:
    med = np.median(Mx[n]); s = 1.4826 * np.median(np.abs(Mx[n] - med))
    Z[n] = (Mx[n] - med, s, med)
T = np.max(np.array([Z[n][0] / Z[n][1] for n in nests]), axis=0)
zc = (real - Z['100'][2]) / Z['100'][1]
nge = int((T >= zc).sum())
pFW = (1 + nge) / (len(T) + 1)
print('\nM1 max-T: A100 median %.4f robust sd %.4f; candidate z %.2f; family-wise control maxima T: max %.2f, 99th pct %.2f; #T >= z_c: %d; p_FW = %.4f' % (
    Z['100'][2], Z['100'][1], zc, T.max(), np.quantile(T, 0.99), nge, pFW))
print('   per-nest z of the largest control: %s' % {('A' + n): round(float((Mx[n].max() - Z[n][2]) / Z[n][1]), 2) for n in nests})
out['M1'] = dict(z_candidate=float(zc), T_max=float(T.max()), n_T_ge_zc=nge, p_FW=pFW, per_template_bound=1 / 402, bonferroni12=12 / 402)

# M2: GEV tail (model-based)
from scipy.stats import genextreme
c, loc, sc = genextreme.fit(Mx['100'])
p1 = float(genextreme.sf(real, c, loc, sc))
p12 = 1 - (1 - p1) ** 12
print('M2 GEV fit to the 401 A100 maxima: shape %.3f loc %.4f scale %.4f; tail P(max >= %.4f) = %.3e; Sidak over 12 templates %.3e; Bonferroni over %d parent-run template-year scans %.3e' % (
    c, loc, sc, real, p1, p12, NPAR, min(1.0, NPAR * p1)))
pe = {}
for n in nests:
    cc, ll, ss = genextreme.fit(Mx[n])
    pe['A' + n] = dict(shape=round(float(cc), 3), max=round(float(Mx[n].max()), 4), sf_at_own_max=float(genextreme.sf(Mx[n].max(), cc, ll, ss)))
print('   GEV per nest (shape, max, tail at own max):', {k: (v['shape'], v['max'], '%.2e' % v['sf_at_own_max']) for k, v in pe.items()})
out['M2'] = dict(shape=float(c), loc=float(loc), scale=float(sc), p_template=p1, p_sidak12=p12, n_parent_scans=NPAR,
                 p_bonferroni_parent=min(1.0, NPAR * p1), empirical_bonferroni_parent=NPAR / 402, per_nest=pe)
print('   empirical Bonferroni over %d parent-run template-year scans: %d/402 = %.4f; over the %d of 1973: %.4f; GEV x %d: %.3e' % (NPAR, NPAR, NPAR / 402, NPAR73, NPAR73 / 402, NPAR73, min(1.0, NPAR73 * p1)))
out['M2'].update(n_parent_scans_1973=NPAR73, empirical_bonferroni_1973=NPAR73 / 402, p_bonferroni_1973=min(1.0, NPAR73 * p1))


# A6: specificity of the bank tests (null + R7 + R9) against the A100 stack, catalogued 1973 deep moonquakes
def phase_interval(nest):
    a = allc[(allc['T2'] == 'A') & (allc['N2'] == nest)]
    t = np.array([int(np.datetime64('%d-01-01T00:00' % (1900 + int(r.Y)), 'ns').astype(np.int64)) +
                  ((int(r.JD) - 1) * 86400 + int(str(r.S).zfill(4)[:2]) * 3600 + int(str(r.S).zfill(4)[2:]) * 60) * NS for r in a.itertuples()], dtype=np.int64)
    ph = np.sort(mean_anomaly_deg(t)); n = len(ph); k = int(np.ceil(0.95 * n))
    ext = np.concatenate([ph, ph + 360]); w = ext[k - 1:k - 1 + n] - ext[:n]; i = int(np.argmin(w))
    return float(ext[i] % 360), float(ext[i + k - 1] % 360)


iv = phase_interval('100')
inv = (lambda p: iv[0] <= p <= iv[1]) if iv[0] <= iv[1] else (lambda p: p >= iv[0] or p <= iv[1])
print('\nA6: A100 phase interval [%.2f, %.2f]' % iv)
pt = np.array([p[0] + 30 * NS for p in allp], dtype=np.int64); o = np.argsort(pt); pt = pt[o]; ps = [allp[i] for i in o]
dm = c73[c73['T2'] == 'A']
rows = []
for r in dm.itertuples():
    a = np.searchsorted(pt, r.t - 300 * NS); b = np.searchsorted(pt, r.t + 600 * NS, side='right')
    if b <= a:
        rows.append((r, None)); continue
    k = a + int(np.argmax([ps[j][1] for j in range(a, b)]))
    rows.append((r, ps[k]))
res6 = {'A100': [], 'other': []}
for r, p in rows:
    if p is None:
        continue
    s14 = max([c for c in p[2][:2] if c is not None] or [-1]); s16 = max([c for c in p[2][2:] if c is not None] or [-1])
    ph = float(mean_anomaly_deg(p[0] + 30 * NS))
    ok = p[1] > best and s14 >= 0.5 and s16 >= 0.5 and inv(ph)
    rec = dict(event='73-%s %s A%s' % (r.JD, str(r.S).zfill(4), r.N2), Dt=p[1], s14=s14, s16=s16, ccs=p[2], phase=round(ph, 1),
               above_null=p[1] > best, R7=s14 >= 0.5 and s16 >= 0.5, R9=inv(ph), passes=ok)
    res6['A100' if r.N2 == '100' else 'other'].append(rec)
nA = int((dm['N2'] == '100').sum()); nO = len(dm) - nA
passO = [x for x in res6['other'] if x['passes']]; passA = [x for x in res6['A100'] if x['passes']]
print('A6: catalogued 1973 deep moonquakes: %d A100, %d other. Passing null + R7 + R9 against the A100 stack: A100 %d of %d; other nests %d of %d' % (
    nA, nO, len(passA), nA, len(passO), nO))
for x in passO:
    print('   non-A100 passing: %s Dt %.4f S14 %.3f S16 %.3f phase %.1f ccs %s' % (x['event'], x['Dt'], x['s14'], x['s16'], x['phase'], x['ccs']))
for x in sorted(res6['other'], key=lambda x: -x['Dt'])[:10]:
    print('   top non-A100 by Dt: %s Dt %.4f S14 %.3f S16 %.3f R7 %s R9 %s' % (x['event'], x['Dt'], x['s14'], x['s16'], x['R7'], x['R9']))
print('   non-A100 above the null alone: %d; with R7: %d' % (sum(x['above_null'] for x in res6['other']), sum(x['above_null'] and x['R7'] for x in res6['other'])))
out['A6'] = dict(phase_interval=iv, n_A100=nA, n_other=nO, pass_A100=passA, pass_other=passO,
                 other_above_null=sum(x['above_null'] for x in res6['other']),
                 other_above_null_R7=sum(x['above_null'] and x['R7'] for x in res6['other']))

# A3b (forward-scan part): catalogued A100 events, their S14/S16 channel NCCs
print('\nA3b (forward part): catalogued 1973 A100 events, best A100 forward peak in [start - 5 min, start + 10 min]: Dt, ccs [S14 MH1, MH2, S16 MH1, MH2]')
for x in sorted(res6['A100'], key=lambda x: x['event']):
    print('   %s Dt %.4f ccs %s phase %.1f' % (x['event'], x['Dt'], x['ccs'], x['phase']))
out['A3b_forward'] = res6['A100']
json.dump(out, open(OUT + '.json', 'w'), indent=1, default=float)
print('\nnull_test lines:')
print('controls: %d' % len(Mx['100']))
print('best_control: %.4f' % best)
print('real: %.4f' % real)
print('real_beats_all_controls: %s' % ('yes' if real > best else 'no'))
