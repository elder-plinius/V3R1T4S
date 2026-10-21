#!/usr/bin/env python3
"""Kick: remove R words chosen uniformly at random (numpy default_rng(SEED)) from a code (sorted int64 .npy) and save
the remaining words as a sorted int64 .npy (the input format of lb_lns_gen.py). A subset of a valid code is valid,
so the output is checked only for size and subset-ness here. usage: kick.py IN.npy R SEED OUT.npy"""
import json
import sys

import numpy as np


def main():
    src, r, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    a = np.unique(np.load(src).astype(np.int64))
    if not 0 <= r < len(a):
        sys.exit("R out of range")
    rng = np.random.default_rng(seed)
    keep = np.sort(rng.choice(len(a), size=len(a) - r, replace=False))
    b = a[keep]
    assert len(b) == len(a) - r and np.isin(b, a).all()
    np.save(out, b)
    print(json.dumps({"in": src, "M_in": int(len(a)), "removed": r, "seed": seed, "out": out, "M_out": int(len(b))}))


if __name__ == "__main__":
    main()
