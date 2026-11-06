"""Polish near-table candidates with SLP, write result files for cells the independent
checker certifies, and produce a summary table (summary.tsv)."""
import numpy as np, sys, os, subprocess
from multiprocessing import Pool
from run import load_best, save, T, HERE
from polish import slp
RES = os.path.join(HERE, '../../results/hsp4-a')
TAB = os.path.join(HERE, '../../data/packomania.com_hsp4_txt_radius.txt')

def pol(N):
    r0, x = load_best(N)
    if x is None: return N, None, None
    if r0 - T[N] > -3e-5:
        y, r = slp(x)
        if r > r0: save(N, y, r); return N, r0, r
    return N, r0, r0

if __name__ == '__main__':
    Ns = [n for n in range(120, 211) if n != 170]
    with Pool(4) as p: out = p.map(pol, Ns)
    rows = []
    for N, r0, r in out:
        if r is None: rows.append((N, T[N], None, 'no')); continue
        src = os.path.join(HERE, 'best', f'hsp4-{N}.txt')
        beaten = 'no'
        if r - T[N] > 5e-11:
            res = subprocess.run([sys.executable, os.path.join(RES, 'check.py'), src, TAB], capture_output=True, text=True)
            line = res.stdout.strip()
            if res.returncode == 0 and 'BEATEN' in line and 'NOT_BEATEN' not in line:
                beaten = 'yes'
                body = [l for l in open(src) if not l.startswith('#')]
                with open(os.path.join(RES, f'hsp4-{N}.txt'), 'w') as fh:
                    fh.write(f'# cell hsp4 N={N}; value r*={r:.16f}; table={T[N]:.12f}; checker: {line}\n')
                    fh.writelines(body)
        rows.append((N, T[N], r, beaten))
    with open(os.path.join(HERE, 'summary.tsv'), 'w') as fh:
        for N, t, r, b in rows:
            fh.write(f'{N}\t{t:.12f}\t' + (f'{r:.12f}\t{r-t:+.3e}' if r is not None else 'NA\tNA') + f'\t{b}\n')
    print(open(os.path.join(HERE, 'summary.tsv')).read())
