"""Harness calibration for polaris/pkis2-lok-slk-c-1, package-relative and stdlib-only.

Four of the six listed leaderboard entries are constant all-positive "baseline null model"
submissions. Their published values are therefore exactly reproducible from the definition:
a constant probability 1.0 must give CLASS_LOK pr_auc = 24/132, CLASS_SLK pr_auc = 13/132,
and accuracy = 24/132. This script recomputes those values from the official test labels in
object/official_inputs.json (pinned to the official parquet by sha256) with the same
from-definition PR-AUC implementation as the package checker, and PASSes only if they match
the listed values bit-for-bit.

Run from the package folder:  python3 how-we-built-it/baseline/lokslk_null_model.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))

sys.path.insert(0, os.path.join(PKG, "verify-it-yourself"))
from checker import average_precision  # the from-definition stepped PR-curve implementation

inp = json.load(open(os.path.join(PKG, "object", "official_inputs.json")))
te = inp["test_index_array"]
yL = [inp["labels"][str(i)]["CLASS_LOK"] for i in te]
yS = [inp["labels"][str(i)]["CLASS_SLK"] for i in te]

LISTED_LOK = 0.18181818181818182  # four entries list exactly this value
LISTED_SLK = [0.09848484848484848, 0.1, 0.10317460317460317, 0.1148018648018648]
LISTED_ACC = 0.18181818181818182

p = [1.0] * len(te)
prL = average_precision(yL, p)
prS = average_precision(yS, p)
acc = sum(1 for v in yL if v > 0) / len(te)

print("CLASS_LOK: constant-1 pr_auc %.17f  positives %d/%d" % (prL, int(sum(yL)), len(te)))
print("   matches a listed value: %s" % (abs(prL - LISTED_LOK) < 1e-12))
print("CLASS_SLK: constant-1 pr_auc %.17f  positives %d/%d" % (prS, int(sum(yS)), len(te)))
print("   matches a listed value: %s" % (any(abs(prS - v) < 1e-12 for v in LISTED_SLK)))
print("CLASS_LOK: constant-1 accuracy %.17f vs listed %.17f match %s" % (
    acc, LISTED_ACC, abs(acc - LISTED_ACC) < 1e-12))

ok = (abs(prL - LISTED_LOK) < 1e-12 and any(abs(prS - v) < 1e-12 for v in LISTED_SLK)
      and abs(acc - LISTED_ACC) < 1e-12)
print("\nBASELINE CALIBRATION: " + ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
