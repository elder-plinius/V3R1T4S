#!/usr/bin/env python3
"""Build a corrupted copy of object/ for the checker's self-test. Standard library only.
usage: corrupt.py <mode> <object_dir>      modes: ruler_all ruler_one rescale drop leak"""
import csv, gzip, os, sys

mode, OBJ = sys.argv[1], sys.argv[2]
F = lambda tag, i, w="test_predictions": os.path.join(OBJ, "%s_split_%d_%s.csv.gz" % (tag, i, w))


def read(p):
    with gzip.open(p, "rt", newline="") as fh:
        r = csv.DictReader(fh)
        return r.fieldnames, list(r)


def write(p, fields, rows):
    with gzip.open(p, "wt", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


if mode in ("ruler_all", "ruler_one"):
    for i in (range(10) if mode == "ruler_all" else [0]):
        f, rows = read(F("seed42", i))
        for r in rows:
            r["pred_PotencyTransfer"] = r["pred_NaiveMeanEffectsPredictor"]
        write(F("seed42", i), f, rows)
elif mode == "rescale":
    for i in range(10):
        f, rows = read(F("seed42", i))
        mu = sum(float(r["pred_NaiveMeanEffectsPredictor"]) for r in rows) / len(rows)
        for r in rows:
            r["pred_NaiveMeanEffectsPredictor"] = "%.6f" % (mu + 3.0 * (float(r["pred_NaiveMeanEffectsPredictor"]) - mu))
        write(F("seed42", i), f, rows)
elif mode == "drop":
    for i in range(10):
        f, rows = read(F("seed42", i))
        err = {}
        for r in rows:
            e = abs(float(r["response"]) - float(r["pred_PotencyTransfer"]))
            a = err.setdefault(r["pubchem_id"], [0.0, 0]); a[0] += e; a[1] += 1
        worst = sorted(err, key=lambda d: -err[d][0] / err[d][1])[:5]
        write(F("seed42", i), f, [r for r in rows if r["pubchem_id"] not in set(worst)])
elif mode == "leak":
    p = os.path.join(OBJ, "seed42_split_drug_roles.csv.gz")
    f, rows = read(p)
    victim = next(r["pubchem_id"] for r in rows if r["CV_split"] == "0" and r["role"] == "test")
    rows.append({"CV_split": "0", "role": "train", "pubchem_id": victim})
    write(p, f, rows)
elif mode == "digit":
    f, rows = read(F("seed42", 0))
    v = rows[0]["pred_PotencyTransfer"]
    rows[0]["pred_PotencyTransfer"] = v[:-1] + ("1" if v[-1] != "1" else "2")
    write(F("seed42", 0), f, rows)
else:
    sys.exit("unknown mode %s" % mode)
print("corrupted: %s" % mode)
