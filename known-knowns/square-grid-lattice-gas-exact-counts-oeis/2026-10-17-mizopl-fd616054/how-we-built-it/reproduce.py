#!/usr/bin/env python3
"""Reproduction gate: reproduce A054759(n) for n=1..14 from the OEIS b-file, exactly.

Uses the sector transfer-matrix + float64 modular matmul + CRT (see sixvertex.py).
Published terms n=1..14 are cited from https://oeis.org/A054759/b054759.txt
(sha256: 26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada; see
../the-record-we-beat/snapshot.md). An optional local b-file path may be passed as
the third argument.

    python3 reproduce.py [nmax=14] [nprimes=8] [optional_bfile_path]
"""
import sys, time, signal, os
import sixvertex as sv

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "reproduce_output.txt")
HARD_LIMIT_S = int(os.environ.get("HARD_LIMIT_S", "900"))

# Published terms from https://oeis.org/A054759/b054759.txt
# (sha256: 26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada)
PUBLISHED_A054759 = {
    1: 4,
    2: 18,
    3: 148,
    4: 2970,
    5: 143224,
    6: 16448400,
    7: 4484823396,
    8: 2901094068042,
    9: 4448410550095612,
    10: 16178049740086515288,
    11: 139402641051212392498528,
    12: 2849295959501939989625992464,
    13: 137950545200232788276834783781648,
    14: 15844635835975276495290739119895808472,
}


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
    bvals = load_bfile(sys.argv[3]) if len(sys.argv) > 3 else dict(PUBLISHED_A054759)
    primes = sv.primes_below(1 << 20, nprimes)
    lines = []

    def emit(s):
        print(s, flush=True)
        lines.append(s)
        with open(OUT, "w") as f:
            f.write("\n".join(lines) + "\n")

    emit("# A054759 reproduction  (run at %s)" % time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    emit("# source: https://oeis.org/A054759/b054759.txt (sha256: 26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada)")
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
