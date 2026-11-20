"""Wave-2 unit runner for the orbit search (runu.py with the wave-2 sampler and long re-runs).

usage: python runu2.py plan.tsv jobs deadline_epoch [workdir]
plan.tsv columns: cell alph d bar ub family lo hi samples seed tlim maxv maxk focus excl tlong
For each plan row: generate the subgroup sample with mkgroups2.py (groups/<cell>/<fam>/), then run osg once per
subgroup with target = bar (a hit of size bar is the positive control, a hit above bar is a win). One result file
per (cell, family, subgroup): res/<cell>/<fam>/g<k>.out; an existing file is skipped. Rows are taken in plan order,
units interleaved across the rows of a chunk. When tlong > tlim, a unit that times out at tlim is run again with
tlong into g<k>.long.out (at most LONG_PER_ROW per row). Every unit ends before the deadline (time limit
shortened, process killed at the deadline); a unit cut short is recorded as TIMEOUT or KILLED, never as a negative.
Environment: MAXV and TLIM cap the plan's vertex cap and time limit on this host; MAXV_FLOOR raises the vertex cap
of every row to at least that value (big-RAM hosts).
"""
import os, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
LONG_PER_ROW = 3
LOCK = threading.Lock()
CLAIMS = {}  # long re-runs started by this process, per result dir


def slug(s):
    return re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_')


def gen(row, wd):
    cell, alph, d, bar, ub, fam, lo, hi, samples, seed, tlim, maxv, maxk, focus, excl = row[:15]
    gd = os.path.join(wd, 'groups', cell, slug(fam))
    if not os.path.exists(os.path.join(gd, 'manifest.tsv')):
        r = subprocess.run([PY, os.path.join(HERE, 'mkgroups2.py'), alph, fam, lo, hi, samples, seed, gd, maxk, focus, excl],
                           capture_output=True, text=True)
        with LOCK, open(os.path.join(wd, 'gen.log'), 'a') as f:
            f.write(f'{cell} {fam}: {r.stdout.strip()} {r.stderr.strip()[-300:]}\n')
    if not os.path.exists(os.path.join(gd, 'manifest.tsv')):
        return []
    return [(row, gd, l.split('\t')) for l in open(os.path.join(gd, 'manifest.tsv')) if l.strip()]


def run_osg(row, gd, m, wd, deadline, tlim, out):
    cell, alph, d, bar, ub, fam = row[:6]
    maxv = str(min(max(int(row[11]), int(os.environ.get('MAXV_FLOOR', 0))), int(os.environ.get('MAXV', row[11]))))
    k = m[0]
    rd = os.path.dirname(out)
    left = deadline - time.time()
    tl = min(tlim, left - 120)
    if tl < 20:
        return None
    code = os.path.join(rd, f'code_g{k}{".long" if out.endswith(".long.out") else ""}.txt')
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
        regen = ' '.join([alph, fam] + row[6:10] + [row[12], row[13], row[14]])
        with LOCK, open(os.path.join(wd, 'WINS.tsv'), 'a') as f:
            f.write(f'{cell}\t{fam}\tg{k}\torder={m[1]}\tsize={best}\tbar={bar}\tub={ub}\t{code}\tmkgroups2: {regen}\n')
    return line


def run_unit(u, wd, deadline):
    row, gd, m = u
    tlim = min(float(row[10]), float(os.environ.get('TLIM', row[10])))
    tlong = float(row[15]) if len(row) > 15 and row[15] not in ('', '-') else 0
    k = m[0]
    rd = os.path.join(wd, 'res', row[0], slug(row[5])); os.makedirs(rd, exist_ok=True)
    out = os.path.join(rd, f'g{k}.out')
    if os.path.exists(out):
        line = open(out).read()
    else:
        line = run_osg(row, gd, m, wd, deadline, tlim, out)
        if line is None:
            return
        line = open(out).read()
    if tlong > tlim and ' TIMEOUT best=-' in line and '\t-\t' in line:
        lout = os.path.join(rd, f'g{k}.long.out')
        with LOCK:
            done = {f for f in os.listdir(rd) if f.endswith('.long.out')} | CLAIMS.get(rd, set())
            if os.path.exists(lout) or len(done) >= LONG_PER_ROW:
                return
            CLAIMS.setdefault(rd, set()).add(os.path.basename(lout))
        run_osg(row, gd, m, wd, deadline, tlong, lout)


def main():
    plan, jobs, deadline = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    wd = sys.argv[4] if len(sys.argv) > 4 else os.getcwd()
    rows = [l.rstrip('\n').split('\t') for l in open(plan) if l.strip() and not l.startswith('#')]
    os.makedirs(wd, exist_ok=True)
    log = os.path.join(wd, 'units.log')
    with open(log, 'a') as f:
        f.write(f'{time.ctime()} start: {len(rows)} plan rows, {jobs} jobs, deadline {time.ctime(deadline)}\n')
    # the next chunk of rows is sampled while the current chunk's units run; at most 2*jobs units wait in the
    # queue, so a long unit never holds the other workers at a chunk boundary
    chunk = 2 * jobs
    sem = threading.BoundedSemaphore(3 * jobs)
    with ThreadPoolExecutor(jobs) as ex, ThreadPoolExecutor(max(2, jobs // 2)) as gx:
        futs = [gx.submit(gen, r, wd) for r in rows[0:chunk]]
        for c in range(0, len(rows), chunk):
            if deadline - time.time() < 150:
                break
            lists = [f.result() for f in futs]
            futs = [gx.submit(gen, r, wd) for r in rows[c + chunk:c + 2 * chunk]]
            units = [L[i] for i in range(max(map(len, lists), default=0)) for L in lists if i < len(L)]
            for u in units:
                sem.acquire()
                ex.submit(run_unit, u, wd, deadline).add_done_callback(lambda _f: sem.release())
            with open(log, 'a') as f:
                f.write(f'{time.ctime()} rows {c}..{min(c + chunk, len(rows)) - 1} queued ({len(units)} units)\n')
        for f in futs:
            f.cancel()
    with open(log, 'a') as f:
        f.write(f'{time.ctime()} finished\n')
    open(os.path.join(wd, 'DONE'), 'w').write(time.ctime() + '\n')


if __name__ == '__main__':
    main()
