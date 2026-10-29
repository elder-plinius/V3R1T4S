#!/usr/bin/env python3
"""Convert a LITA qcsr .npz scheme (U, V read row-major A, B; W writes row-major C) to the run's JSON format."""
import json, sys
import numpy as np
from fractions import Fraction

def npz_to_json(src, dst):
    z = np.load(src, allow_pickle=False)
    meta = json.loads(z["metadata_json"].item())
    n1, n2, n3 = meta["tensor"]
    R = meta["rank"]
    rows = {}
    for ax in "uvw":
        ip = z[ax + "_indptr"]; ix = z[ax + "_indices"]; nu = z[ax + "_numerators"]; de = z[ax + "_denominators"]
        rows[ax] = [[[int(ix[p]), str(Fraction(int(nu[p]), int(de[p])))] for p in range(ip[k], ip[k + 1])] for k in range(R)]
    terms = [{"u": rows["u"][k], "v": rows["v"][k], "w": rows["w"][k]} for k in range(R)]
    json.dump({"format": [n1, n2, n3], "rank": R, "ring": "Q", "terms": terms}, open(dst, "w"))

if __name__ == "__main__":
    npz_to_json(sys.argv[1], sys.argv[2])
