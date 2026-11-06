"""Independent FJSSP-W schedule checker, written from the instance format of jrc-rodec/FJSSP-W-Benchmarking.
Instance (.fjs): line 1 'jobs machines workers'; then one line per job: n_ops, and per operation
n_machine_choices, then per machine: machine_id n_worker_choices (worker_id duration)*, all ids 1-based.
Schedule (.json): {"ops": [[job, op, machine, worker, start], ...]} with 1-based job/op/machine/worker,
op = position of the operation inside its job.
Usage: python3 fjsspw_check.py instance.fjs schedule.json  -> prints makespan or the first violation; exit 0 iff valid."""
import json, sys


def read_instance(path):
    lines = [l.split() for l in open(path) if l.strip()]
    n_jobs, n_mach, n_work = int(lines[0][0]), int(lines[0][1]), int(round(float(lines[0][2])))
    jobs = []
    for line in lines[1:1 + n_jobs]:
        v = list(map(int, line)); i = 1; ops = []
        for _ in range(v[0]):
            k = v[i]; i += 1; opt = {}
            for _ in range(k):
                m = v[i]; nw = v[i + 1]; i += 2
                for _ in range(nw):
                    opt[(m, v[i])] = v[i + 1]; i += 2
            ops.append(opt)
        if i != len(v):
            raise ValueError('job line not fully consumed')
        jobs.append(ops)
    if len(jobs) != n_jobs:
        raise ValueError('expected %d job lines, found %d' % (n_jobs, len(jobs)))
    return n_mach, n_work, jobs


def check(inst, sched):
    n_mach, n_work, jobs = read_instance(inst)
    rows = json.load(open(sched))['ops']
    seen, end, by_m, by_w = {}, {}, {}, {}
    for j, o, m, w, s in rows:
        if not all(isinstance(x, int) for x in (j, o, m, w, s)) or s < 0:
            return None, 'non-integer or negative entry %r' % ([j, o, m, w, s],)
        if not (1 <= j <= len(jobs) and 1 <= o <= len(jobs[j - 1])):
            return None, 'unknown operation %d.%d' % (j, o)
        if (j, o) in seen:
            return None, 'operation %d.%d scheduled twice' % (j, o)
        d = jobs[j - 1][o - 1].get((m, w))
        if d is None:
            return None, 'pair (machine %d, worker %d) not eligible for %d.%d' % (m, w, j, o)
        seen[(j, o)] = s; end[(j, o)] = s + d
        by_m.setdefault(m, []).append((s, s + d, j, o)); by_w.setdefault(w, []).append((s, s + d, j, o))
    for j, ops in enumerate(jobs, 1):
        for o in range(1, len(ops) + 1):
            if (j, o) not in seen:
                return None, 'operation %d.%d missing' % (j, o)
            if o > 1 and seen[(j, o)] < end[(j, o - 1)]:
                return None, 'precedence broken at %d.%d' % (j, o)
    for name, res in (('machine', by_m), ('worker', by_w)):
        for r, iv in res.items():
            iv.sort()
            for a, b in zip(iv, iv[1:]):
                if b[0] < a[1]:
                    return None, '%s %d overlap: %d.%d and %d.%d' % (name, r, a[2], a[3], b[2], b[3])
    return max(end.values()), 'ok'


if __name__ == '__main__':
    mk, msg = check(sys.argv[1], sys.argv[2])
    print('VALID makespan=%d' % mk if mk is not None else 'INVALID: ' + msg)
    sys.exit(0 if mk is not None else 1)
