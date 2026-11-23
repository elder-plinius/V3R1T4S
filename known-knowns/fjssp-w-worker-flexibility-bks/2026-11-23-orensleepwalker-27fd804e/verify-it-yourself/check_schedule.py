"""FJSSP-W instance parser and independent schedule checker (written from the repository's instance format).
Instance: line 1 'jobs machines workers'; per job: n_ops, then per op: n_machine_choices, then per machine:
machine_id n_worker_choices (worker_id duration)*  (ids 1-based).
Schedule JSON: {"instance": name, "ops": [[job, op, machine, worker, start, duration], ...]} (job/op 0-based, machine/worker 1-based)."""
import json, sys

def parse(path):
    tok = open(path).read().split()
    J, M, W = int(tok[0]), int(tok[1]), int(tok[2])
    # the header may carry a 4th token (average machines per op); detect by trying both
    for skip in (3, 4):
        try:
            p = skip; jobs = []
            for _ in range(J):
                n = int(tok[p]); p += 1; ops = []
                for _ in range(n):
                    nm = int(tok[p]); p += 1; alt = {}
                    for _ in range(nm):
                        m = int(tok[p]); nw = int(tok[p + 1]); p += 2
                        for _ in range(nw):
                            w = int(tok[p]); d = int(tok[p + 1]); p += 2
                            assert 1 <= m <= M and 1 <= w <= W and d > 0
                            assert (m, w) not in alt
                            alt[(m, w)] = d
                    assert alt; ops.append(alt)
                jobs.append(ops)
            if p == len(tok): return J, M, W, jobs
        except (AssertionError, IndexError, ValueError):
            continue
    raise ValueError('cannot parse ' + path)

def check(inst_path, sched):
    """Return (ok, makespan, errors)."""
    J, M, W, jobs = parse(inst_path); err = []; seen = {}
    for rec in sched['ops']:
        if len(rec) != 6 or any(type(x) is not int for x in rec): err.append('bad record %r' % (rec,)); continue
        j, o, m, w, s, d = rec
        if not (0 <= j < J and 0 <= o < len(jobs[j])): err.append('unknown op %r' % (rec,)); continue
        if (j, o) in seen: err.append('duplicate op %d,%d' % (j, o)); continue
        if (m, w) not in jobs[j][o]: err.append('ineligible pair %r' % (rec,)); continue
        if jobs[j][o][(m, w)] != d: err.append('wrong duration %r' % (rec,)); continue
        if s < 0: err.append('negative start %r' % (rec,)); continue
        seen[(j, o)] = (m, w, s, s + d)
    total = sum(len(x) for x in jobs)
    if len(seen) != total: err.append('ops scheduled %d of %d' % (len(seen), total))
    for j in range(J):
        for o in range(1, len(jobs[j])):
            if (j, o) in seen and (j, o - 1) in seen and seen[(j, o)][2] < seen[(j, o - 1)][3]:
                err.append('precedence job %d op %d' % (j, o))
    for idx, label in ((0, 'machine'), (1, 'worker')):
        by = {}
        for k, v in seen.items(): by.setdefault(v[idx], []).append((v[2], v[3], k))
        for r, lst in by.items():
            lst.sort()
            for a, b in zip(lst, lst[1:]):
                if b[0] < a[1]: err.append('%s %d overlap %r %r' % (label, r, a[2], b[2]))
    mk = max((v[3] for v in seen.values()), default=None)
    return (not err), mk, err

if __name__ == '__main__':
    ok, mk, err = check(sys.argv[1], json.load(open(sys.argv[2])))
    print('VALID makespan=%d' % mk if ok else 'INVALID ' + '; '.join(err[:3]))
