#!/usr/bin/env python3
"""Reproduction gate: reproduce A054759(n) for n=1..14 from the b-file, exactly.

Uses the sector transfer-matrix + float64 modular matmul + CRT (see sixvertex.py).
(This is the de-machined copy: the original hardcoded an absolute b-file path; here the
b-file path is an argument, default 'b054759.txt' in this folder.)

    python3 reproduce.py [nmax=14] [nprimes=8] [bfile=b054759.txt]
"""
import sys, time, signal, os
import sixvertex as sv

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "reproduce_output.txt")
HARD_LIMIT_S = int(os.environ.get("HARD_LIMIT_S", "900"))


def on_alarm(signum, frame):
    raise TimeoutError("hard wall-clock limit %ds reached" % HARD_LIMIT_S)


signal.signal(signal.SIGALRM, on_alarm)
signal.alarm(HARD_LIMIT_S)


def load_bfile(path):
    d = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) >= 2:
                d[int(parts[0])] = int(parts[1])
    return d


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    nprimes = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    bpath = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "b054759.txt")
    bvals = load_bfile(bpath)
    primes = sv.primes_below(1 << 20, nprimes)
    lines = []

    def emit(s):
        print(s, flush=True)
        lines.append(s)
        with open(OUT, "w") as f:
            f.write("\n".join(lines) + "\n")

    emit("# A054759 reproduction  (run at %s)" % time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    emit("# primes (%d, each < 2^20): %s" % (nprimes, primes))
    emit("# hard limit: %ds" % HARD_LIMIT_S)
    emit("# %3s %42s %42s  match  secs  Mbits" % ('n', 'computed', 'published'))
    all_ok = True
    t_all = time.time()
    for n in range(1, nmax + 1):
        t0 = time.time()
        val, M, res = sv.compute_a(n, primes)
        dt = time.time() - t0
        pub = bvals.get(n)
        ok = (pub is not None and val == pub)
        all_ok = all_ok and ok
        emit("  %3d %42d %42s  %5s  %6.1f  %d" % (n, val, str(pub), 'OK' if ok else 'FAIL', dt, M.bit_length()))
    emit("# total wall %.1fs   RESULT: %s" % (time.time() - t_all, 'ALL MATCH' if all_ok else 'MISMATCH'))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
