"""Standalone checker for the polaris/pkis2-lok-slk-c-1 claim, written from the definition.

Python standard library only. Run from the package folder:
    python3 verify-it-yourself/checker.py
The last output line is exactly `VERIFY_LOKSLK: PASS` on success.

It re-implements PR-AUC (stepped PR-curve area with tie grouping, the definition of
average precision) and ROC-AUC (Mann-Whitney U with tie correction) from scratch, then:
  1. checks the prediction file against the official inputs record (rows, order, ranges);
  2. recomputes every claimed value;
  3. checks the margin and the 10,000-resample bootstrap rule from the bank criterion;
  4. reproduces the harness calibration (a constant all-positive prediction must give
     exactly the listed null-model values 24/132 and 13/132);
  5. cross-checks the extracted labels against their recorded pins (positive counts,
     split sizes, bar values).

The official inputs record (object/official_inputs.json) also pins the sha256 of the
official parquet and benchmark metadata; an online cross-check that re-downloads those
files and compares hashes is in run_checks.sh (informational when offline). Anyone with
pandas+pyarrow can re-extract the labels from the official parquet directly; the one-line
command is in RUN_IT_YOURSELF.md.
"""
import json
import os
import random
import sys

OK = True
PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # the package folder


def load(rel):
    return os.path.join(PKG, rel)


def fail(msg):
    global OK
    OK = False
    print("FAIL: " + msg)


def average_precision(y, s):
    pairs = sorted(zip(s, y), key=lambda t: -t[0])
    P = sum(1 for _, v in pairs if v > 0)
    if P == 0:
        return 0.0
    ap = 0.0
    tp = fp = 0
    prev_recall = 0.0
    i, n = 0, len(pairs)
    while i < n:
        score = pairs[i][0]
        j = i
        while j < n and pairs[j][0] == score:
            if pairs[j][1] > 0:
                tp += 1
            else:
                fp += 1
            j += 1
        recall = tp / P
        ap += (tp / (tp + fp)) * (recall - prev_recall)
        prev_recall = recall
        i = j
    return ap


def roc_auc(y, s):
    order = sorted(range(len(s)), key=lambda i: s[i])
    ranks = [0.0] * len(s)
    i, n, r = 0, len(s), 1
    while i < n:
        j = i
        while j < n and s[order[j]] == s[order[i]]:
            j += 1
        avg = (2 * r + (j - i) - 1) / 2.0
        for k in range(i, j):
            ranks[order[k]] = avg
        r += j - i
        i = j
    pos = sum(1 for v in y if v > 0)
    neg = len(y) - pos
    ssum = sum(ranks[i] for i in range(len(y)) if y[i] > 0)
    return (ssum - pos * (pos + 1) / 2.0) / (pos * neg)


def main():
    inp = json.load(open(load("object/official_inputs.json")))
    rows = []
    with open(load("object/preds.csv")) as f:
        header = f.readline().strip().split(",")
        if header != ["row_index", "CLASS_LOK", "CLASS_SLK"]:
            fail("unexpected columns: %r" % header)
        for line in f:
            a, b, c = line.strip().split(",")
            rows.append((int(a), float(b), float(c)))

    te = inp["test_index_array"]
    if len(rows) != len(te):
        fail("prediction rows %d != official test rows %d" % (len(rows), len(te)))
    if [r[0] for r in rows] != list(te):
        fail("row order does not equal the official split[1] array")
    if inp["n_train"] != 508 or inp["n_test"] != 132:
        fail("unexpected split sizes")
    if sum(inp["train_index_array"]) != 163609 or sum(te) != 40871:
        fail("split arrays do not match the official indices (checksum)")
    if len(inp["labels"]) != 132 or sorted(int(k) for k in inp["labels"]) != sorted(te):
        fail("label records do not match the official test rows")
    for r in rows:
        if not (0.0 <= r[1] <= 1.0 and 0.0 <= r[2] <= 1.0):
            fail("probability out of [0,1] at row %d" % r[0])

    yL = [inp["labels"][str(i)]["CLASS_LOK"] for i in te]
    yS = [inp["labels"][str(i)]["CLASS_SLK"] for i in te]
    pL = [r[1] for r in rows]
    pS = [r[2] for r in rows]
    nposL = sum(1 for v in yL if v > 0)
    nposS = sum(1 for v in yS if v > 0)
    if nposL != 24 or nposS != 13:
        fail("label positives %d/%d, expected 24/13" % (nposL, nposS))

    apL, apS = average_precision(yL, pL), average_precision(yS, pS)
    rocL, rocS = roc_auc(yL, pL), roc_auc(yS, pS)
    mean_ap = 0.5 * (apL + apS)
    bar = inp["bar"]
    listed = inp["listed_pr_auc_values"]
    print("recomputed CLASS_LOK pr_auc %.12f roc_auc %.12f" % (apL, rocL))
    print("recomputed CLASS_SLK pr_auc %.12f roc_auc %.12f" % (apS, rocS))
    print("recomputed mean pr_auc %.12f" % mean_ap)

    spec = json.load(open(load("object/spec.json")))
    for name, got, want in [
            ("CLASS_LOK pr_auc", apL, spec["claimed_values"]["CLASS_LOK_pr_auc"]),
            ("CLASS_LOK roc_auc", rocL, spec["claimed_values"]["CLASS_LOK_roc_auc"]),
            ("CLASS_SLK pr_auc", apS, spec["claimed_values"]["CLASS_SLK_pr_auc"]),
            ("CLASS_SLK roc_auc", rocS, spec["claimed_values"]["CLASS_SLK_roc_auc"]),
            ("mean pr_auc", mean_ap, spec["claimed_values"]["mean_pr_auc"])]:
        if abs(got - want) > 1e-9:
            fail("%s %.12f != claimed %.12f" % (name, got, want))
        else:
            print("match %s %.12f" % (name, got))

    if not all(apL > v for v in listed):
        fail("CLASS_LOK pr_auc does not beat every listed value")
    if apL < bar + 0.020:
        fail("margin +0.020 not met")
    else:
        print("margin ok: %.12f >= %.12f" % (apL, bar + 0.020))
    if mean_ap < bar + 0.020:
        fail("mean-interpretation margin not met")

    rng = random.Random(20261118)
    n = len(te)
    below = degenerate = 0
    for _ in range(10000):
        idx = [rng.randrange(n) for _ in range(n)]
        yy = [yL[k] for k in idx]
        if min(yy) == max(yy):
            degenerate += 1
            below += 1
            continue
        if average_precision(yy, [pL[k] for k in idx]) <= bar:
            below += 1
    frac = 1 - below / 10000
    print("stdlib 10,000-resample bootstrap: fraction above bar %.6f (degenerate %d)" % (frac, degenerate))
    if frac < 0.95:
        fail("bootstrap rule not met (%.6f < 0.95)" % frac)

    # harness calibration: constant all-positive predictor reproduces the listed null models
    ones = [1.0] * n
    calL, calS = average_precision(yL, ones), average_precision(yS, ones)
    if abs(calL - 24 / 132) > 1e-12 or abs(calL - 0.18181818181818182) > 1e-12:
        fail("CLASS_LOK calibration %.12f != listed 0.18181818181818182" % calL)
    if abs(calS - 13 / 132) > 1e-12 or abs(calS - 0.09848484848484848) > 1e-12:
        fail("CLASS_SLK calibration %.12f != listed 0.09848484848484848" % calS)
    print("calibration ok: constant-1 gives %.17f / %.17f (the listed null-model values)" % (calL, calS))

    print("VERIFY_LOKSLK: " + ("PASS" if OK else "FAIL"))
    return 0 if OK else 1


if __name__ == "__main__":
    sys.exit(main())
