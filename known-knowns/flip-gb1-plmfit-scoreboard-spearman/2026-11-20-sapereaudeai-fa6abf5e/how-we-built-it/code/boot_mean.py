"""Score prediction files and bootstrap THE MEAN over seeds (PREREG section 5).

Written from the bank's criterion, not from any model.  The criterion asks for "the mean and
standard deviation over at least three seeds, with a bootstrap 95% interval over test sequences
that excludes the published bar"; p2 asks for "a three-seed mean strictly above ... with a
bootstrap 95% interval that excludes it".  So the interval that gates is the interval of the
MEAN: each bootstrap resample of the test sequences is scored under every seed's predictions and
the three Spearmans are averaged, giving one mean per resample.  Per-seed intervals are printed
for information only; no per-seed gate is imposed.

Usage:
  python -I boot_mean.py <csv> <split> <bar> <pred.csv> ... [--nboot N] [--full FULLWIN]
                         [--published P]
  python -I boot_mean.py --selftest <csv> <split>
"""
import csv
import hashlib
import sys

import numpy as np
from scipy.stats import spearmanr


def load(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    return (hashlib.sha256(raw).hexdigest(),
            list(csv.DictReader(raw.decode("utf-8").splitlines())))


def main():
    argv = sys.argv[1:]
    if argv[0] == "--selftest":
        sha, rows = load(argv[1])
        te = [r for r in rows if r[argv[2]] == "test"]
        y = np.array([float(r["score"]) for r in te])
        pos = float(spearmanr(y, y).statistic)
        neg = float(spearmanr(y, -y).statistic)
        print("data sha256:", sha)
        print("selftest test rows: %d" % len(y))
        print("known positive (prediction = target):  rho = %.6f" % pos)
        print("known negative (prediction = -target): rho = %.6f" % neg)
        ok = abs(pos - 1.0) < 1e-12 and abs(neg + 1.0) < 1e-12
        print("SELFTEST:", "PASS" if ok else "FAIL")
        return

    nboot = 10000
    full = None
    published = None
    for flag in ("--nboot", "--full", "--published"):
        if flag in argv:
            i = argv.index(flag)
            v = float(argv[i + 1])
            if flag == "--nboot":
                nboot = int(v)
            elif flag == "--full":
                full = v
            else:
                published = v
            del argv[i:i + 2]

    path, split, bar = argv[0], argv[1], float(argv[2])
    preds = argv[3:]
    sha, rows = load(path)
    te = [r for r in rows if r[split] == "test"]
    seqs = [r["aa_seq"] for r in te]
    truth = {r["aa_seq"]: float(r["score"]) for r in te}
    y = np.array([truth[s] for s in seqs])
    print("data sha256: %s" % sha)
    print("data rows: %d ; split column: %s ; test rows: %d" % (len(rows), split, len(te)))
    print("bar (carried over, PENDING STATUS CHECK): %.6f" % bar)

    P, rhos = [], []
    for pf in preds:
        with open(pf, newline="") as fh:
            pr = list(csv.DictReader(fh))
        seen = {}
        dup = 0
        for r in pr:
            if r["aa_seq"] in seen:
                dup += 1
            seen[r["aa_seq"]] = float(r["prediction"])
        extra = [s for s in seen if s not in truth]
        missing = [s for s in truth if s not in seen]
        ok = (dup == 0 and not extra and not missing and len(seen) == len(truth))
        with open(pf, "rb") as fh:
            h = hashlib.sha256(fh.read()).hexdigest()
        name = pf.replace("\\", "/").split("/")[-1]
        print("\n### %s  sha256 %s" % (name, h))
        print("COVERAGE: %s  rows=%d unique=%d duplicates=%d extras=%d missing=%d"
              % ("PASS" if ok else "FAIL", len(pr), len(seen), dup, len(extra), len(missing)))
        if not ok:
            print("NOT SCORED (coverage gate)")
            continue
        p = np.array([seen[s] for s in seqs])
        P.append(p)
        rho = float(spearmanr(y, p).statistic)
        rhos.append(rho)
        print("spearman: %.6f" % rho)

    if not P:
        return
    P = np.array(P)
    v = np.array(rhos)
    print("\n--- seeds and spread ---")
    print("per-seed spearman: %s" % ["%.6f" % x for x in rhos])
    print("mean %.6f  sd(ddof=0) %.6f  sd(ddof=1) %.6f"
          % (v.mean(), v.std(ddof=0), v.std(ddof=1) if len(v) > 1 else 0.0))

    print("\n--- bootstrap of THE MEAN over seeds: %d resamples, "
          "numpy.random.default_rng(0) ---" % nboot)
    rng = np.random.default_rng(0)
    n = len(y)
    means = np.empty(nboot)
    per = np.empty((nboot, len(P)))
    for b in range(nboot):
        idx = rng.integers(0, n, n)
        yb = y[idx]
        for k in range(len(P)):
            per[b, k] = spearmanr(yb, P[k][idx]).statistic
        means[b] = per[b].mean()
    lo, hi = float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))
    print("mean's bootstrap 95%% interval: [%.6f, %.6f]" % (lo, hi))
    for k, pf in enumerate([p.replace("\\", "/").split("/")[-1] for p in preds[:len(P)]]):
        print("  (info only, no gate) per-seed interval %s: [%.6f, %.6f]"
              % (pf, float(np.percentile(per[:, k], 2.5)),
                 float(np.percentile(per[:, k], 97.5))))

    print("\n--- gates, exactly as PREREG section 5 fixes them ---")
    print("p2: mean > bar                     : %.6f > %.6f -> %s"
          % (v.mean(), bar, v.mean() > bar))
    print("p2: mean's interval excludes bar   : lo %.6f > %.6f -> %s" % (lo, bar, lo > bar))
    print("p2 MET (both of the above)         : %s" % bool(v.mean() > bar and lo > bar))
    if full is not None:
        print("full: mean >= bar + 0.02 = %.6f  : %.6f -> %s"
              % (full, v.mean(), v.mean() >= full))
    if published is not None:
        print("full: mean > highest published %.6f : %.6f -> %s"
              % (published, v.mean(), v.mean() > published))
        if full is not None:
            print("full criterion MET (all three)     : %s"
                  % bool(v.mean() >= full and lo > bar and v.mean() > published))
    print("margin over bar: %+.6f" % (v.mean() - bar))


if __name__ == "__main__":
    main()
