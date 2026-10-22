"""LP domination checks on the law tables written by gate3 (see gate.py for the model).
usage: python gate_lp.py <table file> <q>
"""
import sys

import numpy as np

from gate import dominated


def main():
    fn, q = sys.argv[1], float(sys.argv[2])
    L = {}
    for line in open(fn):
        w = line.split()
        if w[0] == "dims":
            head = line.strip()
            fsize = list(map(int, w[w.index("fsize") + 1:]))
        elif w[0] == "root":
            root = np.array(list(map(float, w[1:])))
        else:
            L[(int(w[1]), int(w[2]))] = np.array(list(map(float, w[3:])))
    tot = root.sum()
    worst = (dominated(root / tot, q, 6), "root")
    print("%s q=%s: P(G nonempty) = %.6f; root max-flow %.6f" % (head, q, tot, worst[0]))
    for fin in range(6):
        T = np.array([L[(fin, t)] for t in range(1 << fsize[fin])])
        fw = (1.0, None)
        for U in range(1, 1 << fsize[fin]):
            law = T[[t for t in range(1 << fsize[fin]) if t & U]].sum(axis=0)
            if law.sum() <= 0:
                continue
            v = dominated(law / law.sum(), q, 5)
            if v < fw[0]:
                fw = (v, bin(U))
        print("  entry face %d: worst max-flow %.6f at U=%s" % (fin, fw[0], fw[1]))
        if fw[0] < worst[0]:
            worst = (fw[0], "entry face %d U=%s" % (fin, fw[1]))
    print("WORST %.6f (deficit %.2e) at %s" % (worst[0], 1 - worst[0], worst[1]))


if __name__ == "__main__":
    main()
