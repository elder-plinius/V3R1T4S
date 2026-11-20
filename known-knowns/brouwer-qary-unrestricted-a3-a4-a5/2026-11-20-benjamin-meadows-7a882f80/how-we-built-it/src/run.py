"""Run orbsearch over every subgroup class in a group directory, in parallel.

usage: python run.py groupdir q n d target time_limit max_vertices jobs outdir [min_order]
Writes outdir/results.tsv (k, order, gens, orbsearch output line) and outdir/code_g<k>.txt for each hit.
"""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor


def main():
    gdir, q, n, d, target, tl, maxv, jobs, out = sys.argv[1:10]
    min_order = int(sys.argv[10]) if len(sys.argv) > 10 else 1
    os.makedirs(out, exist_ok=True)
    rows = [l.rstrip('\n').split('\t') for l in open(os.path.join(gdir, 'manifest.tsv'))]
    rows = [r for r in rows if int(r[1]) >= min_order]

    def one(r):
        k = r[0]
        cmd = ['./orbsearch', q, n, d, os.path.join(gdir, f'g{k}.txt'), target, tl, maxv, os.path.join(out, f'code_g{k}.txt')]
        p = subprocess.run(cmd, capture_output=True, text=True)
        line = (p.stdout.strip() or p.stderr.strip()).replace('\n', ' ')
        with open(os.path.join(out, 'results.tsv'), 'a') as f:
            f.write(f'{k}\t{r[1]}\t{r[2]}\t{line}\n')
        return line

    with ThreadPoolExecutor(int(jobs)) as ex:
        list(ex.map(one, rows))


if __name__ == '__main__':
    main()
