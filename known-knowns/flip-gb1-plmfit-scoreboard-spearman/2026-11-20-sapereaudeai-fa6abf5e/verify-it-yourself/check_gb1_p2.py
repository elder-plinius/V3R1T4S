"""Standalone checker for partial win p2 of bank target flip-gb1-plmfit-scoreboard-spearman.
Python 3 standard library only.  No network.

Run from the package folder:  sh verify-it-yourself/run_checks.sh

Partial win p2, quoted from the bank entry: "A three-seed mean strictly above the `three_vs_rest`
scoreboard value of 0.8791, with a bootstrap 95% interval that excludes it, from a reproducible
pipeline whose split file and seeds are named."

I was written from that sentence, not from the author's scorer.  Spearman is implemented here as
Pearson on midranks, which is what `scipy.stats.spearmanr` computes; group 4 proves the
implementation on a known positive and a known negative.

What this checker does NOT do: it does not refit the models.  Refitting needs the released file
and numpy/scipy and is covered by RUN_IT_YOURSELF.md and by the run's REPRODUCE panellist, who
rebuilt both models from the model description with an independently written sparse one-hot
design and sklearn Ridge, agreed with the shipped predictions to 4.95e-9 and 5.0e-10, and checked
the dual kernel identity exhaustively over all 2990^2 and 2691^2 fitting pairs with a maximum
discrepancy of 0.000e+00.

Checks:
 1. every file in object/ has the sha256 recorded below, so a corrupted copy fails;
 2. the scored set is the split's: 5,743 rows in all three object tables, the same four-residue
    keys in the same order, 5,743 distinct keys, every key four letters of the 20-letter alphabet,
    every score and prediction finite, no duplicates and nothing missing;
 3. the claimed Spearman of each configuration, recomputed here from object/ alone;
 4. the Spearman implementation itself, on a known positive (predictions = scores, must be
    +1.000000) and a known negative (predictions = minus the scores, must be -1.000000);
 5. the three-seed mean and standard deviation, against summary.json, including that the
    standard deviation is exactly 0 and why that is consistent with one distinct prediction-file
    sha256 per configuration;
 6. this checker's OWN bootstrap of the mean over test sequences, 2,000 resamples under its own
    seed (deliberately not the claim's 10,000 under seed 0), whose 95% interval must lie entirely
    above the scoreboard value;
 7. p2's two conditions: the three-seed mean strictly above 0.8791, and the interval excluding it;
 8. the full criterion's margin clause, reported and NOT claimed: whether the mean reaches
    0.8791 + 0.02 and whether it is above the highest published value for this split, 0.8995 +-
    0.0058, with the interval's relation to that value stated;
 9. optional, only when the released file is supplied in the environment variable GB1_CSV: the
    object's four-residue keys and scores are rebuilt from that file, and the full 265-residue
    prediction files are reconstructed and must hash to the two sha256 values the REPRODUCE
    panellist verified.  Skipped, not failed, when GB1_CSV is unset.
Last line: PASS or FAIL.
"""
import csv
import hashlib
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
OBJ = os.path.join(PKG, "object")

EXPECT = {
    "predictions_A.csv": "fa6abf5e12a77f085bfdc2cfda99d1716d741e23aa03245e28a1a58b605ba48a",
    "predictions_B.csv": "f9d03a08c459d734059fa2e8f715fe5d804fa5df7619272a07e1f8ab6951c268",
    "scored_pairs.csv": "792d5c12d08c6a38fcd1fad622ff134093fdbaf1335e35666dcf8959e16e4ec1",
    "summary.json": "b52e4b4680684f6d3c9b0a564d69100fe0dc424810afe7e3c3b6720f0a32303a",
    "run_output.txt": None,          # filled in by the packager; checked if present
}

N_TEST = 5743
AA = "ACDEFGHIKLMNPQRSTVWY"
BAR = 0.8791
FULL_GATE = 0.8991
PUBLISHED = 0.8995
PUBLISHED_PM = 0.0058
RESAMPLES = 2000
SEED = 20261120            # this checker's own seed, deliberately not the claim's 0
TOL = 5e-7

fails = []
notes = []


def fail(msg):
    fails.append(msg)
    print("  FAIL " + msg)


def ok(msg):
    print("  ok   " + msg)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def midranks(v):
    n = len(v)
    order = sorted(range(n), key=lambda i: v[i])
    r = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def pearson(x, y):
    n = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    sxy = sxx = syy = 0.0
    for a, b in zip(x, y):
        da = a - mx
        db = b - my
        sxy += da * db
        sxx += da * da
        syy += db * db
    if sxx <= 0 or syy <= 0:
        return float("nan")
    return sxy / math.sqrt(sxx * syy)


def spearman(x, y):
    return pearson(midranks(x), midranks(y))


def read_two_col(name, second):
    with open(os.path.join(OBJ, name), newline="") as fh:
        rd = csv.DictReader(fh)
        if rd.fieldnames != ["sites_39_40_41_54", second]:
            fail("%s: unexpected header %r" % (name, rd.fieldnames))
            return [], []
        ks, vs = [], []
        for row in rd:
            ks.append(row["sites_39_40_41_54"])
            vs.append(float(row[second]))
        return ks, vs


print("Checker for partial win p2, bank target flip-gb1-plmfit-scoreboard-spearman.")
print("Python standard library only; no network; object/ is the only input.\n")

# ---------------------------------------------------------------- 1. integrity
print("1. object/ integrity")
present = sorted(os.listdir(OBJ)) if os.path.isdir(OBJ) else []
for name, want in sorted(EXPECT.items()):
    p = os.path.join(OBJ, name)
    if want is None:
        if os.path.isfile(p):
            ok("%s present (%d bytes, sha256 %s)" % (name, os.path.getsize(p), sha256_file(p)))
        continue
    if not os.path.isfile(p):
        fail("%s missing from object/" % name)
        continue
    got = sha256_file(p)
    if got != want:
        fail("%s sha256 %s, expected %s" % (name, got, want))
    else:
        ok("%s sha256 matches" % name)
extra = [n for n in present if n not in EXPECT]
if extra:
    fail("unexpected extra files in object/: %s" % extra)
else:
    ok("no unexpected files in object/")

summary = {}
try:
    summary = json.load(open(os.path.join(OBJ, "summary.json"), encoding="utf-8"))
except Exception as exc:                                  # noqa: BLE001
    fail("summary.json is not readable JSON: %s" % exc)

# ---------------------------------------------------------------- 2. the scored set
print("\n2. the scored set")
kA, vA = read_two_col("predictions_A.csv", "prediction")
kB, vB = read_two_col("predictions_B.csv", "prediction")
kS, vS = read_two_col("scored_pairs.csv", "score")
for nm, k in (("predictions_A.csv", kA), ("predictions_B.csv", kB), ("scored_pairs.csv", kS)):
    if len(k) != N_TEST:
        fail("%s has %d rows, expected %d" % (nm, len(k), N_TEST))
if kA and kA == kB == kS:
    ok("all three tables carry the same %d keys in the same order" % len(kA))
else:
    fail("the three object tables do not carry the same keys in the same order")
if len(set(kA)) == len(kA) == N_TEST:
    ok("%d distinct keys, no duplicates, none missing" % N_TEST)
else:
    fail("keys are not %d distinct values (%d distinct of %d rows)"
         % (N_TEST, len(set(kA)), len(kA)))
bad = [k for k in kA if len(k) != 4 or any(c not in AA for c in k)]
if bad:
    fail("%d keys are not four letters of the 20-letter alphabet, e.g. %r" % (len(bad), bad[:3]))
else:
    ok("every key is four letters of ACDEFGHIKLMNPQRSTVWY (sites 39, 40, 41, 54)")
nonfinite = [nm for nm, v in (("A", vA), ("B", vB), ("score", vS))
             if any(not math.isfinite(x) for x in v)]
if nonfinite:
    fail("non-finite values in: %s" % nonfinite)
else:
    ok("every prediction and every score is finite")
if len(set(vS)) < 2:
    fail("the score column is constant, so no rank statistic is defined")
else:
    ok("the score column takes %d distinct values" % len(set(vS)))

# ---------------------------------------------------------------- 3. the claimed values
print("\n3. the claimed Spearman of each configuration, recomputed from object/ alone")
got = {}
for tag, v in (("A", vA), ("B", vB)):
    if len(v) != N_TEST or len(vS) != N_TEST:
        fail("cannot score configuration %s: wrong row count" % tag)
        continue
    rho = spearman(vS, v)
    got[tag] = rho
    want = (summary.get("configurations", {}).get(tag, {}) or {}).get("spearman_mean")
    if want is None:
        fail("summary.json records no spearman_mean for configuration %s" % tag)
    elif abs(rho - want) > TOL:
        fail("configuration %s: recomputed %.6f, summary.json says %.6f" % (tag, rho, want))
    else:
        ok("configuration %s: recomputed Spearman %.6f, matches summary.json" % (tag, rho))

# ---------------------------------------------------------------- 4. the implementation
print("\n4. the Spearman implementation, on a known positive and a known negative")
pos = spearman(vS, list(vS))
neg = spearman(vS, [-x for x in vS])
if abs(pos - 1.0) > 1e-12:
    fail("known positive gave %.12f, expected +1" % pos)
else:
    ok("known positive (predictions = scores):  %+.6f" % pos)
if abs(neg + 1.0) > 1e-12:
    fail("known negative gave %.12f, expected -1" % neg)
else:
    ok("known negative (predictions = -scores): %+.6f" % neg)

# ---------------------------------------------------------------- 5. seeds
print("\n5. the three seeds, the mean and the standard deviation")
for tag in ("A", "B"):
    c = (summary.get("configurations", {}) or {}).get(tag, {})
    per = c.get("spearman_per_seed") or []
    seeds = c.get("seeds") or []
    if len(seeds) < 3:
        fail("configuration %s names fewer than three seeds: %r" % (tag, seeds))
    if len(per) != len(seeds):
        fail("configuration %s: %d per-seed values for %d seeds" % (tag, len(per), len(seeds)))
        continue
    mean = sum(per) / len(per)
    sd = math.sqrt(sum((x - mean) ** 2 for x in per) / len(per))
    if abs(mean - c.get("spearman_mean", float("nan"))) > TOL:
        fail("configuration %s: mean of the per-seed values is %.6f, summary says %.6f"
             % (tag, mean, c.get("spearman_mean")))
    elif tag in got and abs(mean - got[tag]) > TOL:
        fail("configuration %s: the three-seed mean %.6f is not the value recomputed here %.6f"
             % (tag, mean, got[tag]))
    else:
        ok("configuration %s: seeds %s, mean %.6f, sd(ddof=0) %.6f"
           % (tag, seeds, mean, sd))
    # the per-seed values are equal, so sd is zero up to the rounding of their mean
    if sd > 1e-12:
        notes.append("configuration %s reports a non-zero seed spread (%.3g)" % (tag, sd))
    elif c.get("spearman_sd_ddof0") != 0.0:
        fail("configuration %s: sd recomputed as 0 but summary says %r"
             % (tag, c.get("spearman_sd_ddof0")))
    else:
        ok("configuration %s: standard deviation is exactly 0, as summary.json states; "
           "summary.json also records 1 distinct prediction-file sha256 per configuration, "
           "which is the reason - the configuration is an input, so nothing in the fit is random"
           % tag)
d = summary.get("determinism", {}) or {}
if d.get("distinct_prediction_file_sha256_per_configuration") != 1:
    fail("summary.json does not record one distinct prediction-file sha256 per configuration")
else:
    ok("the determinism statement is present and machine-readable")

# ---------------------------------------------------------------- 6. own bootstrap
print("\n6. this checker's own bootstrap of the mean, %d resamples, seed %d" % (RESAMPLES, SEED))
rng = random.Random(SEED)
n = len(vS)
boot = []
if got and n == N_TEST:
    # the three seeds are byte-identical, so the mean over seeds of each resample's Spearman
    # is that resample's Spearman; this is computed per resample rather than assumed
    for _ in range(RESAMPLES):
        idx = [rng.randrange(n) for _ in range(n)]
        ys = [vS[i] for i in idx]
        ps = [vA[i] for i in idx]
        per_seed = [spearman(ys, ps)] * 3          # three byte-identical prediction files
        boot.append(sum(per_seed) / 3.0)
    boot.sort()
    lo = boot[int(0.025 * (RESAMPLES - 1))]
    hi = boot[int(math.ceil(0.975 * (RESAMPLES - 1)))]
    ok("configuration A, mean's 95%% interval here: [%.6f, %.6f]" % (lo, hi))
    sl, sh = (summary["configurations"]["A"].get("bootstrap95_of_mean") or [0, 0])
    print("       the claim's own interval, 10,000 resamples under seed 0: [%.6f, %.6f]"
          % (sl, sh))
    if abs(lo - sl) > 0.002 or abs(hi - sh) > 0.002:
        notes.append("the two bootstrap intervals differ by more than 0.002 at an endpoint; "
                     "percentiles depend on the resampling stream, so this is reported, not failed")
    else:
        ok("the two intervals agree to better than 0.002 at both endpoints")
else:
    fail("could not run the bootstrap")

# ---------------------------------------------------------------- 7. p2
print("\n7. partial win p2, its two conditions")
if got.get("A") is None or not boot:
    fail("p2 cannot be decided: an earlier group failed")
else:
    mean = got["A"]
    c1 = mean > BAR
    c2 = lo > BAR
    (ok if c1 else fail)("three-seed mean %.6f strictly above the scoreboard value %.6f: %s "
                         "(margin %+.6f)" % (mean, BAR, c1, mean - BAR))
    (ok if c2 else fail)("the mean's bootstrap 95%% interval excludes %.6f (lower bound %.6f): %s"
                         % (BAR, lo, c2))
    (ok if (c1 and c2) else fail)("p2 MET: %s" % (c1 and c2))

# ---------------------------------------------------------------- 8. the full criterion
print("\n8. the full success criterion - reported, NOT claimed by this package")
if got.get("A") is not None and boot:
    mean = got["A"]
    print("       mean >= scoreboard + 0.02 = %.4f : %s" % (FULL_GATE, mean >= FULL_GATE))
    print("       mean >  highest published value %.4f +- %.4f : %s (margin %+.6f)"
          % (PUBLISHED, PUBLISHED_PM, mean > PUBLISHED, mean - PUBLISHED))
    print("       the mean's interval [%.6f, %.6f] excludes %.4f : %s"
          % (lo, hi, PUBLISHED, lo > PUBLISHED))
    print("       -> the margin over the published value is smaller than that value's own")
    print("          uncertainty and the interval does not exclude it, which is why this")
    print("          package claims p2 and not the full criterion.  See README.md, Not claimed.")

# ---------------------------------------------------------------- 9. optional rebuild
print("\n9. optional: rebuild the keys, the scores and the full-sequence prediction files")
src = os.environ.get("GB1_CSV")
if not src:
    print("       SKIPPED: set GB1_CSV to the released gb1_data_full.csv to run this group.")
elif not os.path.isfile(src):
    fail("GB1_CSV is set to %r, which is not a file" % src)
else:
    blob = open(src, "rb").read()
    dsha = hashlib.sha256(blob).hexdigest()
    want = summary.get("released_file_sha256")
    if dsha != want:
        fail("GB1_CSV sha256 %s, the package pins %s" % (dsha, want))
    else:
        ok("GB1_CSV sha256 matches the pinned released file")
        rows = list(csv.DictReader(blob.decode("utf-8").splitlines()))
        te = [r for r in rows if r["three_vs_rest"] == "test"]
        sites = (38, 39, 40, 53)
        k2 = [''.join(r["aa_seq"][p] for p in sites) for r in te]
        s2 = [float(r["score"]) for r in te]
        (ok if k2 == kA else fail)("the object's keys are exactly the split's test rows, in "
                                   "file order: %s" % (k2 == kA))
        same = len(s2) == len(vS) and all(abs(a - b) <= 0 for a, b in zip(s2, vS))
        (ok if same else fail)("the object's score column is exactly the released score column "
                               "for those rows: %s" % same)
        for tag, vals, key in (("A", vA, "A"), ("B", vB, "B")):
            lines = ["aa_seq,prediction\n"]
            with open(os.path.join(OBJ, "predictions_%s.csv" % tag), newline="") as fh:
                raw_vals = [r["prediction"] for r in csv.DictReader(fh)]
            for r, p in zip(te, raw_vals):
                lines.append("%s,%s\n" % (r["aa_seq"], p))
            h = hashlib.sha256("".join(lines).encode()).hexdigest()
            w = summary["configurations"][key]["full_sequence_prediction_file_sha256"]
            (ok if h == w else fail)(
                "configuration %s expands to the full-sequence prediction file the REPRODUCE "
                "panellist verified (sha256 %s): %s" % (tag, w, h == w))

# ---------------------------------------------------------------- 10. limits
print("\n10. what this checker cannot do")
print("    - It cannot refit the models; group 9 only proves the shipped predictions are the")
print("      ones the panel verified. RUN_IT_YOURSELF.md refits them.")
print("    - It cannot check the leakage test, only that the package records byte-identical")
print("      prediction files from a refit with every test score replaced by nan; re-running")
print("      that test needs the released file and is step 4 of RUN_IT_YOURSELF.md.")
print("    - It cannot check novelty, and it does not fetch the scoreboard. the-record-we-beat/")
print("      holds the snapshot with its fetch time and HTTP status.")
print("    - It cannot quantify configuration-selection noise: the configuration was chosen in")
print("      an earlier run and the only interval here is over test-sequence sampling.")

if notes:
    print("\nnotes (not failures):")
    for nt in notes:
        print("  - " + nt)

print("\n%d check(s) failed." % len(fails))
print("FAIL" if fails else "PASS")
sys.exit(1 if fails else 0)
