import subprocess, json, os, sys
exe = sys.argv[1]; tables = sys.argv[2]; EXTRA = sys.argv[3:]
def run(name, cert, tau='0.834', parts='core5d,r3_collar,r5_collar', extra=()):
    out = f'out/controls/{name}.jsonl'
    if os.path.exists(out): os.remove(out)
    p = subprocess.run(['dotnet', exe, '--cert', cert, '--tables', tables, '--parts', parts, '--frontiers', '255-255', '--threads', '1', '--tau', tau, '--out', out, *EXTRA, *extra], capture_output=True, text=True)
    rows = [json.loads(l) for l in open(out)] if os.path.exists(out) else []
    bad = []
    if p.returncode != 0 or not rows: bad.append('exit=%d %s' % (p.returncode, (p.stderr or p.stdout).strip().splitlines()[-1][:120] if (p.stderr or p.stdout).strip() else ''))
    for r in rows:
        if r.get('readErr'): bad.append(r['part'] + ' readErr: ' + r['readErr'][:70])
        if r['fails']: bad.append(r['part'] + ' failing leaves=%d' % r['fails'])
        if not r['coverOk']: bad.append(r['part'] + ' cover: ' + str(r['coverErr'])[:70])
    ms = min((r['minSlack'] for r in rows if r['fails'] == 0), default=None)
    print('%-22s tau=%-9s %s  %s' % (name, tau, 'REJECT' if bad else 'ACCEPT', '; '.join(bad)[:200] or ('min_slack=%.3e' % ms if ms is not None else '')), flush=True)
    return bool(bad)
from concurrent.futures import ThreadPoolExecutor
jobs = [('baseline', 'c0_baseline', 'work/tamper/c0_baseline', '0.834')]
for n in ['c3b_drop100_countfixed', 'c4b_dup1_countfixed', 'c1_bitflip', 'c2_truncate', 'c3_drop100', 'c4_dup1', 'c5_shrink', 'c6_grow', 'c8_samples32', 'c9_psi07', 'c12_swap_lohi', 'c14_shift', 'c15_countlie']:
    jobs.append((n, n, 'work/tamper/' + n, '0.834'))
jobs += [('tau_up_tight_pass', 'c7a_tau_0.8340004', 'work/tamper/c0_baseline', '0.8340004'), ('tau_up_tight_fail', 'c7b_tau_0.8340005', 'work/tamper/c0_baseline', '0.8340005'),
         ('tau_0.84', 'c7c_tau_0.84', 'work/tamper/c0_baseline', '0.84'), ('tau_0.8348', 'c7d_tau_0.8348', 'work/tamper/c0_baseline', '0.8348')]
with ThreadPoolExecutor(max_workers=int(os.environ.get('CONTROL_WORKERS', '6'))) as ex:   # independent runs, one thread each
    futs = [(k, ex.submit(run, name, cert, tau)) for k, name, cert, tau in jobs]
    res = {k: f.result() for k, f in futs}
json.dump(res, open('out/controls/summary.json', 'w'), indent=1)
