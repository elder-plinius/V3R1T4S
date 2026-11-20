"""Out-of-sample comparison of two model-selection criteria on FLIP GB1 three_vs_rest.

No model is fitted here.  Every number is a literal copied from a saved `.out` file in an
earlier run's bundle or from this run's own `scores.out`, and the file each one comes from is
printed next to it so it can be checked by hand.

  criterion CV     : 5-fold random-fold cross-validation Spearman inside the fitting rows.
                     This is the criterion that actually selected run 2026-11-20-0215's models.
  criterion EXTRAP : fit on the fitting rows with no_mut <= 2, predict the fitting rows with
                     no_mut == 3, Spearman.  Declared in that run's PREREG section 8, frozen
                     2026-11-20T02:26:31Z, and deliberately not allowed to select.

Usage: python -I criterion_compare.py
"""
from itertools import combinations

from scipy.stats import spearmanr

SRC_0215 = "runs/2026-11-20-0215/claim/scores.out (= claim/the-earlier-runs/run-0215-scores.out)"
SRC_HERE = "this run: attempts/sealed-scoring/scores.out (= claim/result/scores.out)"
SRC_2355A = "runs/2026-11-20-0215/claim/the-previous-run/p2_all_scores.out"
SRC_2355T = "runs/2026-11-20-0215/claim/the-previous-run/p2_trainonly_scores.out"

# The six models the CV criterion selected in run 2026-11-20-0215, with all three columns.
# (cv_mean, extrapolation_rho, test_rho) - every triple copied from SRC_0215.
SIX = [
    ("all  seed1  s2=1   s3=1    a=0.3 log0.1", 0.935895, 0.778303, 0.895591),
    ("all  seed2  s2=2   s3=1    a=1   log0.1", 0.936529, 0.754478, 0.887735),
    ("all  seed3  s2=1   s3=0.5  a=0.3 log0.1", 0.934421, 0.771981, 0.893644),
    ("tr   seed1  s2=2   s3=1    a=1   log0.1", 0.932661, 0.745480, 0.886541),
    ("tr   seed2  s2=1   s3=0.5  a=0.1 log0.1", 0.931854, 0.759558, 0.890334),
    ("tr   seed3  s2=2   s3=1    a=0.3 log0.1", 0.934103, 0.743324, 0.882926),
]

# The two models the EXTRAP criterion selected, recorded unscored before this run and scored by
# it.  extrapolation_rho from claim/the-earlier-runs/extrap_select.out; test_rho from SRC_HERE.
# Their CV score is unknown: obtaining it would mean re-running the 3,859-configuration grid,
# which is out of this run's scope, so they enter the EXTRAP column only.
TWO = [
    ("A  all  s2=0.5 s3=0.25 a=0.03  log0.001", None, 0.797099, 0.902852),
    ("B  tr   s2=1   s3=1    a=0.001 log0.01 ", None, 0.777742, 0.897451),
]

# Earlier run 2026-11-19-2355's three-seed means, from SRC_2355A / SRC_2355T.
M2355 = {"all": 0.900143, "trainonly": 0.897626}
# Run 2026-11-20-0215's three-seed means, from SRC_0215.
M0215 = {"all": 0.892323, "trainonly": 0.886601}


def tau_b_like(x, y):
    """Fraction of concordant pairs among all pairs with no tie in either column, and the
    count of pairs, so a six- or eight-point statement can be read as what it is."""
    conc = disc = ties = 0
    for i, j in combinations(range(len(x)), 2):
        a, b = x[i] - x[j], y[i] - y[j]
        if a == 0 or b == 0:
            ties += 1
        elif a * b > 0:
            conc += 1
        else:
            disc += 1
    return conc, disc, ties


def show(label, pairs, src):
    x = [p[0] for p in pairs]
    y = [p[1] for p in pairs]
    rho = float(spearmanr(x, y).statistic)
    conc, disc, ties = tau_b_like(x, y)
    print("%-52s n=%d  spearman %+.4f  concordant %d / discordant %d (ties %d)"
          % (label, len(x), rho, conc, disc, ties))
    print("%-52s source: %s" % ("", src))
    return rho


def main():
    print("=" * 100)
    print("1. The six models run 2026-11-20-0215's CV criterion selected, all three columns")
    print("=" * 100)
    print("%-42s %9s %9s %9s" % ("model", "CV", "EXTRAP", "TEST"))
    for n, cv, ex, te in SIX:
        print("%-42s %9.6f %9.6f %9.6f" % (n, cv, ex, te))
    print("\nRank agreement with the TEST column over those six (reproducing "
          "criterion_vs_test.out):")
    show("  CV     vs TEST, 6 points", [(c, t) for _, c, _, t in SIX], SRC_0215)
    show("  EXTRAP vs TEST, 6 points", [(e, t) for _, _, e, t in SIX], SRC_0215)

    print("\n" + "=" * 100)
    print("2. The two models the EXTRAP criterion itself selected, recorded unscored, scored now")
    print("=" * 100)
    print("%-42s %9s %9s %9s" % ("model", "CV", "EXTRAP", "TEST"))
    for n, cv, ex, te in TWO:
        print("%-42s %9s %9.6f %9.6f" % (n, "n/a", ex, te))
    print("\nRank agreement with the TEST column over all eight points where both columns "
          "exist:")
    eight = [(e, t) for _, _, e, t in SIX + TWO]
    show("  EXTRAP vs TEST, 8 points", eight, SRC_0215 + " + " + SRC_HERE)
    print("  CV     vs TEST, 8 points: NOT COMPUTABLE - the CV score of the two new models is")
    print("                            unknown without re-running the 3,859-configuration grid,")
    print("                            which is outside this run's scope.  The honest statement")
    print("                            is the six-point one above plus the two out-of-sample")
    print("                            points below.")

    print("\n" + "=" * 100)
    print("3. The out-of-sample test: does the withheld criterion's pick beat the criterion")
    print("   that did the selecting, on the same fit set and the same test set?")
    print("=" * 100)
    for fs, key, new in (("all", "all", 0.902852), ("trainonly", "trainonly", 0.897451)):
        print("  fitset %-9s  CV criterion (run 0215, 3-seed mean) %.6f  ->  EXTRAP pick "
              "%.6f   difference %+.6f" % (fs, M0215[key], new, new - M0215[key]))
    print("  source: %s and %s" % (SRC_0215, SRC_HERE))
    print()
    for fs, key, new in (("all", "all", 0.902852), ("trainonly", "trainonly", 0.897451)):
        print("  fitset %-9s  CV criterion (run 2355, smaller grid) %.6f  ->  EXTRAP pick "
              "%.6f   difference %+.6f" % (fs, M2355[key], new, new - M2355[key]))
    print("  source: %s and %s" % (SRC_2355A, SRC_2355T))

    print("\n" + "=" * 100)
    print("4. How strong is this?  The arithmetic, so nobody has to take a word for it.")
    print("=" * 100)
    print("  * A perfect rank agreement over 6 points has one-sided permutation probability")
    print("    1/6! = 1/720 = %.6f, and over 8 points 1/8! = 1/40320 = %.8f, IF the ranks were"
          % (1 / 720, 1 / 40320))
    print("    exchangeable and the points independently chosen.")
    print("  * They were not.  The six points are the CV criterion's OWN winners, so the CV")
    print("    column is restricted to a narrow high range (%.6f to %.6f, a spread of %.6f)"
          % (min(c for _, c, _, _ in SIX), max(c for _, c, _, _ in SIX),
             max(c for _, c, _, _ in SIX) - min(c for _, c, _, _ in SIX)))
    print("    while the TEST column spreads over %.6f.  A criterion evaluated only on its own"
          % (max(t for _, _, _, t in SIX) - min(t for _, _, _, t in SIX)))
    print("    near-ties cannot show rank skill; that is a selection effect, not a measurement.")
    print("  * The EXTRAP column was also examined AFTER those six test scores existed.")
    print("  * So the defensible statement is the two out-of-sample points in section 3, of")
    print("    which one (B, trainonly) is fully clean and one (A, all) shares its kernel shape")
    print("    with a configuration whose test score the author of the sealed record had seen.")
    print("  * Both out-of-sample points fall in the predicted direction, by +0.0105 and")
    print("    +0.0109, against a bootstrap half-width of about 0.0046 on each number - so each")
    print("    single comparison is about two standard errors, but the two share a test set and")
    print("    are not independent, and two points cannot establish a method.")
    print("  * VERDICT ON THE EVIDENCE: suggestive, not established.  No claim rests on it.")


if __name__ == "__main__":
    main()
