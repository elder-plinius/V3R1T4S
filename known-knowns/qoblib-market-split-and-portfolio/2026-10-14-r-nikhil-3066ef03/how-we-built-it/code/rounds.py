"""crossover lens driver: rounds of (per-period ILS on all active periods, WORKERS at a time) -> chain DP over all
per-period pools + the base -> exact full descent polish. The best full solution becomes the next round's base.
Every child runs under nice -n 15 and the operator's timeout; child PIDs are logged.

Usage: rounds.py PYTHON QUOTER_CODE_DIR CROSS_CODE_DIR INSTANCE_DIR B LAMBDA NAME START_SOL OUT_DIR ROUNDS SECS WORKERS
       [EXTRA_SOL ...]   (extra .sol files join every DP)
"""
import glob
import os
import shutil
import subprocess
import sys
import time

TIMEOUT = os.environ.get("TIMEOUT_BIN", "timeout")  # local path redacted for publication (a GNU-compatible timeout)


def objective_of(sol):
    with open(sol) as f:
        for line in f:
            if line.startswith("objective"):
                return int(line.split()[1])
    return None


def main():
    (py, qcode, xcode, inst, B, lam, name, start, out, rounds, secs, workers) = sys.argv[1:13]
    extra = sys.argv[13:]
    rounds, secs, workers = int(rounds), int(secs), int(workers)
    os.makedirs(out, exist_ok=True)
    log = open(os.path.join(out, "rounds.log"), "a")
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")

    def mark(s):
        log.write("%s %s\n" % (time.strftime("%H:%M:%S", time.gmtime()), s))
        log.flush()

    base = os.path.join(out, "base_r00.sol")
    shutil.copy(start, base)
    best = objective_of(base)
    mark("start base %s objective %s" % (start, best))
    nper = 9
    for r in range(1, rounds + 1):
        rd = os.path.join(out, "r%02d" % r)
        os.makedirs(rd, exist_ok=True)
        queue = list(range(nper))
        running = []
        while queue or running:
            while queue and len(running) < workers:
                k = queue.pop(0)
                cmd = ["nice", "-n", "15", TIMEOUT, str(secs + 60), py, "-I", os.path.join(xcode, "period_ils.py"), qcode,
                       inst, B, lam, base, str(k), str(1000 * r + k), "4", str(secs), "400", os.path.join(rd, "p%d" % k)]
                p = subprocess.Popen(cmd, stdout=open(os.path.join(rd, "p%d.out" % k), "w"), stderr=subprocess.STDOUT, env=env)
                mark("round %d period %d pid %d" % (r, k, p.pid))
                running.append(p)
            time.sleep(1)
            running = [p for p in running if p.poll() is None]
        files = [base] + extra + sorted(glob.glob(os.path.join(rd, "p*.npz")))
        prev = sorted(glob.glob(os.path.join(out, "r*", "p*.npz")))
        files += [f for f in prev if f not in files][-90:]
        cmd = ["nice", "-n", "15", TIMEOUT, "900", py, "-I", os.path.join(xcode, "pool_dp2.py"), qcode, inst, B, lam, name,
               os.path.join(rd, "dp"), "300"] + files
        res = subprocess.run(cmd, capture_output=True, text=True, env=env)
        open(os.path.join(rd, "dp_output.txt"), "w").write(res.stdout + res.stderr)
        pol = os.path.join(rd, "dp_polished.sol")
        val = objective_of(pol) if os.path.exists(pol) else None
        mark("round %d DP+polish objective %s (base %s)" % (r, val, best))
        if val is not None and val < best:
            best = val
            base = os.path.join(out, "base_r%02d.sol" % r)
            shutil.copy(pol, base)
            mark("round %d NEW BASE %d" % (r, best))
    mark("END best %s base %s" % (best, base))


if __name__ == "__main__":
    main()
