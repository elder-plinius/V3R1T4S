"""f(p): the largest q (to 1e-4) that every non-root check dominates, from a gate3 table at one p.
The root is started fully open (a positive-probability event; the coupling runs under that conditioning), so its
children are independent with success r(full face) each: the root needs only r(full face) >= q.
usage: python fmax.py <gate3 table> [<table> ...]
"""
import sys

import numpy as np

from gate import dominated


def load(fn):
    L = {}
    for line in open(fn):
        w = line.split()
        if w[0] == "dims":
            head = line.strip()
            fsize = list(map(int, w[w.index("fsize") + 1:]))
        elif w[0] == "L":
            L[(int(w[1]), int(w[2]))] = np.array(list(map(float, w[3:])))
    laws = []
    for fin in range(6):
        T = np.array([L[(fin, t)] for t in range(1 << fsize[fin])])
        for U in range(1, 1 << fsize[fin]):
            law = T[[t for t in range(1 << fsize[fin]) if t & U]].sum(axis=0)
            if law.sum() > 0:
                laws.append(((fin, U), law / law.sum()))
    return head, laws


def ok(laws, q):
    for key, law in laws:
        if dominated(law, q, 5) < 1 - 1e-9:
            return False, key
    return True, None


def main():
    for fn in sys.argv[1:]:
        head, laws = load(fn)
        lo, hi = 0.0, 1.0
        # quick screen: marginals bound q from above
        while hi - lo > 1e-4:
            mid = (lo + hi) / 2
            if ok(laws, mid)[0]:
                lo = mid
            else:
                hi = mid
        print("%s: f(p) = %.4f (fails at q = %.4f: %s)" % (head, lo, hi, ok(laws, hi)[1]))


if __name__ == "__main__":
    main()
