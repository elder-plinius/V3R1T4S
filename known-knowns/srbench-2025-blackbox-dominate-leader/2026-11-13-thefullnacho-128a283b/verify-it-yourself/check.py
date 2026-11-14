#!/usr/bin/env python3
"""Standalone verifier for submission 2026-11-13-thefullnacho-128a283b.

Re-scores the 30 saved closed-form expressions for PMLB dataset 522_pm10
against the SRBench 2025 black-box table leader (PS-Tree, median test R2
0.300852, median model_size 4996.5). Uses only numpy, sympy and scikit-learn
(see requirements.txt); downloads the public dataset and the table's LFS
pointer to a temporary directory and verifies their hashes before scoring.

Prints PASS (last line) and exits 0 only if every check holds; otherwise
prints FAIL and exits 1.
"""
import gzip
import hashlib
import json
import re
import statistics
import sys
import tempfile
import urllib.request
from pathlib import Path

import numpy as np
import sympy as sp
from sklearn.model_selection import train_test_split as sk_tts

PKG = Path(__file__).resolve().parent.parent
DATASET_URL = "https://github.com/EpistasisLab/pmlb/raw/master/datasets/522_pm10/522_pm10.tsv.gz"
DATASET_SHA256 = "ecbabaa5a989a8c11f5a57e874c135f386da5379d6689ae6d5d4264a652fa5e0"
TABLE_POINTER_URL = ("https://raw.githubusercontent.com/cavalab/srbench/srbench_2025/"
                     "results/black-box-tuning/results.feather")
TABLE_SHA256 = "5b428264a346f6bbbeabded219f87454b9206afa70c19c012075c672533f342e"
BAR_R2 = 0.300852
BAR_SIZE = 4996.5
CLAIMED_MEDIAN_R2 = 0.331263
CLAIMED_MEDIAN_CX = 145.5

FEATURES = ['cars_per_hour', 'temperature_at_2m', 'wind_speed',
            'temperature_diff_2m_25m', 'wind_direction', 'hour_of_day', 'day']


def fail(msg):
    print("FAIL: " + msg)
    print("FAIL")
    sys.exit(1)


def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "V3R1T4S-verify/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            if resp.status != 200:
                fail("download %s returned HTTP %s" % (url, resp.status))
            data = resp.read()
    except Exception as e:  # noqa: BLE001 - any fetch failure is a FAIL
        fail("download %s failed: %s" % (url, e))
    dest.write_bytes(data)
    return data


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def complexity(expr):
    # SRBench's symbolic_utils.complexity: node count over sympy preorder traversal.
    return sum(1 for _ in sp.preorder_traversal(expr))


def parse_expr(s):
    s = s.strip()
    s = re.sub(r"\|([^|]+)\|", r"Abs(\1)", s).replace("^", "**")
    # PMLB feature names -> x_1..x_7 (longest first, word-boundary safe)
    for i, name in enumerate(FEATURES):
        s = re.sub(r"\b" + re.escape(name) + r"\b", "x_%d" % (i + 1), s)
    loc = {f"x_{i}": sp.Symbol(f"x_{i}") for i in range(1, 8)}
    loc.update({"sqrt": sp.sqrt, "log": sp.log, "exp": sp.exp, "Abs": sp.Abs,
                "Min": sp.Min, "Max": sp.Max, "sin": sp.sin, "cos": sp.cos,
                "pi": sp.pi})
    return sp.sympify(s, locals=loc)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="v3r1t4s_verify_"))
    # 1. Dataset: download and verify hash.
    ds_path = tmp / "522_pm10.tsv.gz"
    fetch(DATASET_URL, ds_path)
    if sha256_file(ds_path) != DATASET_SHA256:
        fail("dataset sha256 mismatch")
    with gzip.open(ds_path, "rt") as f:
        f.readline()
        arr = np.loadtxt(f, delimiter="\t")
    X, y = arr[:, :-1], arr[:, -1]
    if X.shape != (500, 7):
        fail("dataset shape %s, expected (500, 7)" % (X.shape,))
    print("dataset OK: 500 rows, 7 features, sha256 matches")

    # 2. Table unchanged: the live results file is a Git LFS pointer; its oid
    # must equal the sha256 recorded at claim time.
    ptr_path = tmp / "results.feather.pointer"
    raw = fetch(TABLE_POINTER_URL, ptr_path).decode("utf-8", "replace")
    m = re.search(r"oid sha256:([0-9a-f]{64})", raw)
    if not m or m.group(1) != TABLE_SHA256:
        fail("live table pointer does not match the recorded sha256")
    print("live table OK: LFS pointer oid matches the recorded table sha256")

    # 3. Object integrity: expressions file hash must match INDEX.csv.
    obj = PKG / "object" / "expressions.json"
    index_rows = (PKG / "INDEX.csv").read_text().splitlines()
    header = [h.strip() for h in index_rows[0].split(",")]
    row = [v.strip() for v in index_rows[1].split(",")]
    expected_sha = row[header.index("sha256")]
    if sha256_file(obj) != expected_sha:
        fail("object/expressions.json sha256 does not match INDEX.csv")
    print("object integrity OK: expressions.json sha256 matches INDEX.csv")

    # 4. Re-score all 30 expressions on their splits.
    res = json.loads(obj.read_text())
    per = res["per_split"]
    if len(per) != 30:
        fail("expected 30 expressions, found %d" % len(per))
    r2s, cxs = [], []
    for o in per:
        tr_i, te_i = sk_tts(np.arange(len(y)), train_size=0.75, test_size=0.25,
                            random_state=int(o["seed"]))
        expr = parse_expr(o["expr"])
        fn = sp.lambdify([sp.Symbol(f"x_{i}") for i in range(1, 8)], expr,
                         modules="numpy")
        yh = np.asarray(fn(*[X[te_i, i] for i in range(7)]), dtype=float)
        if not np.all(np.isfinite(yh)):
            fail("non-finite predictions for seed %s" % o["seed"])
        r = 1.0 - float(np.sum((y[te_i] - yh) ** 2)) / float(
            np.sum((y[te_i] - y[te_i].mean()) ** 2))
        c = complexity(expr)
        if abs(r - float(o["test_r2"])) > 0.002 or c != int(o["complexity"]):
            fail("seed %s: recomputed R2 %.4f / cx %d differs from recorded %.4f / %d"
                 % (o["seed"], r, c, o["test_r2"], o["complexity"]))
        r2s.append(r)
        cxs.append(c)
    med_r2 = float(statistics.median(r2s))
    med_cx = float(statistics.median(cxs))
    print("re-scored 30/30 splits: median R2 = %.4f, median complexity = %.1f"
          % (med_r2, med_cx))
    if abs(med_r2 - CLAIMED_MEDIAN_R2) > 0.001:
        fail("median R2 %.4f differs from claimed %.4f" % (med_r2, CLAIMED_MEDIAN_R2))
    if abs(med_cx - CLAIMED_MEDIAN_CX) > 0.5:
        fail("median complexity %.1f differs from claimed %.1f" % (med_cx, CLAIMED_MEDIAN_CX))
    if not med_r2 > BAR_R2:
        fail("median R2 %.4f does not beat the table leader %.4f" % (med_r2, BAR_R2))
    if not med_cx <= BAR_SIZE:
        fail("median complexity %.1f exceeds the leader size %.1f" % (med_cx, BAR_SIZE))
    print("bar check OK: median R2 %.4f > %.4f and median complexity %.1f <= %.1f"
          % (med_r2, BAR_R2, med_cx, BAR_SIZE))
    print("PASS")


if __name__ == "__main__":
    main()
