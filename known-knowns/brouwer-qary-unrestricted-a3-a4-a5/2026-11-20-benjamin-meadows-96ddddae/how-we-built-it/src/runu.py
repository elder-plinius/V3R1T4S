"""Overnight unit runner for the orbit search.

usage: python runu.py plan.tsv jobs deadline_epoch [workdir]
plan.tsv columns: cell alph d bar ub family lo hi samples seed tlim maxv maxk
For each plan row: generate the subgroup sample (groups/<cell>/<fam>/), then run osg once per subgroup with
target = bar (so a hit of size bar is the positive control and a hit above bar is a win). One result file per
(cell, family, subgroup): res/<cell>/<fam>/g<k>.out; an existing file is skipped. Units run interleaved across
plan rows. Every unit ends before the deadline (time limit shortened, process killed at the deadline); a unit cut
short is recorded as TIMEOUT or KILLED, never as a negative.
"""
import os, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def slug(s):
    return re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_')


def gen(row, wd):
    cell, alph, d, bar, ub, fam, lo, hi, samples, seed = row[:10]
    gd = os.path.join(wd, 'groups', cell, slug(fam))
    if not os.path.exists(os.path.join(gd, 'manifest.tsv')):
        r = subprocess.run([PY, os.path.join(HERE, 'mkgroups.py'), alph, fam, lo, hi, samples, seed, gd, row[12]], capture_output=True, text=True)
        with open(os.path.join(wd, 'gen.log'), 'a') as f:
            f.write(f'{cell} {fam}: {r.stdout.strip()} {r.stderr.strip()[-300:]}\n')
    if not os.path.exists(os.path.join(gd, 'manifest.tsv')):
        return []
    return [(row, gd, l.split('\t')) for l in open(os.path.join(gd, 'manifest.tsv')) if l.strip()]


def run_unit(u, wd, deadline):
    row, gd, m = u
    cell, alph, d, bar, ub, fam = row[:6]; tlim = float(row[10])
    maxv = str(min(int(row[11]), int(os.environ.get('MAXV', row[11]))))
    tlim = min(tlim, float(os.environ.get('TLIM', tlim)))
    k = m[0]
    rd = os.path.join(wd, 'res', cell, slug(fam)); os.makedirs(rd, exist_ok=True)
    out = os.path.join(rd, f'g{k}.out')
    if os.path.exists(out):
        return
    left = deadline - time.time()
    tl = min(tlim, left - 120)
    if tl < 20:
        return
    code = os.path.join(rd, f'code_g{k}.txt')
    cmd = [os.path.join(HERE, 'osg'), alph, d, os.path.join(gd, f'g{k}.txt'), bar, str(int(tl)), maxv, code]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=max(30, deadline - time.time() - 30))
        line = (p.stdout.strip() or p.stderr.strip()).replace('\n', ' ')
    except subprocess.TimeoutExpired as e:
        line = ((e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or '')).strip() + ' KILLED'
    dt = time.time() - t0
    mb = re.search(r'best=(-?\d+)', line)
    best = int(mb.group(1)) if mb else -1
    status = 'WIN' if best > int(bar) else ('BAR' if best == int(bar) else '-')
    with open(out, 'w') as f:
        f.write(f'{cell}\t{fam}\tg{k}\t{m[1]}\t{m[3].strip() if len(m) > 3 else ""}\tbar={bar}\tub={ub}\ttl={int(tl)}\tsecs={dt:.0f}\t{status}\t{line}\n')
    if status != 'WIN' and os.path.exists(code):
        os.remove(code)
    if status == 'WIN':
        with open(os.path.join(wd, 'WINS.tsv'), 'a') as f:
            f.write(f'{cell}\t{fam}\tg{k}\torder={m[1]}\tsize={best}\tbar={bar}\tub={ub}\t{code}\n')


def main():
    plan, jobs, deadline = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    wd = sys.argv[4] if len(sys.argv) > 4 else os.getcwd()
    rows = [l.rstrip('\n').split('\t') for l in open(plan) if l.strip() and not l.startswith('#')]
    os.makedirs(wd, exist_ok=True)
    log = os.path.join(wd, 'units.log')
    with open(log, 'a') as f:
        f.write(f'{time.ctime()} start: {len(rows)} plan rows, {jobs} jobs, deadline {time.ctime(deadline)}\n')
    chunk = 4 * jobs
    with ThreadPoolExecutor(jobs) as ex:
        for c in range(0, len(rows), chunk):
            if deadline - time.time() < 150:
                break
            part = rows[c:c + chunk]
            lists = list(ex.map(lambda r: gen(r, wd), part))
            units = [L[i] for i in range(max(map(len, lists), default=0)) for L in lists if i < len(L)]
            list(ex.map(lambda u: run_unit(u, wd, deadline), units))
            with open(log, 'a') as f:
                f.write(f'{time.ctime()} rows {c}..{c + len(part) - 1} done ({len(units)} units)\n')
    with open(log, 'a') as f:
        f.write(f'{time.ctime()} finished\n')
    open(os.path.join(wd, 'DONE'), 'w').write(time.ctime() + '\n')


if __name__ == '__main__':
    main()
