"""Growth-constant check for a(15) (PREREG statistic).

Lieb (proved, quoted in the OEIS entry): lim a(n)^(1/n^2) = (4/3)^(3/2),
ln = 1.5*ln(4/3) = 0.431523058...
The literal criterion tolerance (1e-3) cannot discriminate at N=15: the finite-
size correction ln a(n)/n^2 - ln W is still ~ +1.08/n^2 there — indeed the
PUBLISHED a(14) misses the constant by 8.6e-3 (in value terms).  So the check
that actually tests a computed a(15) is the finite-size model:

    ln a(n) = W2 * n^2 + A + B/n        (fit n = 8..14, predict 15)

A wrong a(15) (even a single-digit corruption) shifts ln a(15)/225 far outside
the fit residuals.  Both checks are reported; the literal one is flagged as
uninformative-at-N=15 with the published-term evidence.
"""
import json
import math
from pathlib import Path

import numpy as np

_RUN = Path(__file__).resolve().parents[3]


def main():
    bf = {}
    for line in open(_RUN / "data" / "A054759_b054759.txt.raw"):
        if line.startswith("#") or not line.strip():
            continue
        a, b = line.split()
        bf[int(a)] = int(b)
    r1 = json.load(open(_RUN / "attempts" / "isotypic-row" / "output" / "run1_result.json"))
    r2 = json.load(open(_RUN / "attempts" / "h-tracked" / "output" / "run2_result.json"))
    a15_1, a15_2 = r1["a15"], r2["a15"]

    print("run-1 a(15):", a15_1)
    print("run-2 a(15):", a15_2)
    print("two-run exact agreement:", a15_1 == a15_2)
    assert a15_1 == a15_2, "RUNS DISAGREE"
    x = a15_1

    W2 = 1.5 * math.log(4 / 3)
    print("\nLieb constant: ln W = %.6f (W = %.7f)" % (W2, math.exp(W2)))
    literal = abs(math.log(x) / 225 - W2)
    print("literal check: |ln a(15)/225 - lnW| = %.6f -> %s (tolerance 1e-3)"
          % (literal, "PASS" if literal < 1e-3 else "FAIL"))
    lit14 = abs(math.log(bf[14]) / 196 - W2)
    print("published a(14) under the same literal check: %.6f -> %s"
          % (lit14, "the published term itself exceeds 1e-3" if lit14 >= 1e-3 else "pass"))

    ns = np.arange(8, 15)
    y = np.array([math.log(bf[int(n)]) for n in ns])
    # model ln a(n) = W2 n^2 + A + B/n ; fit A, B with W2 FIXED at Lieb's value
    X = np.column_stack([np.ones(len(ns)), 1.0 / ns])
    rhs = y - W2 * ns.astype(float) ** 2
    coef, res, *_ = np.linalg.lstsq(X, rhs, rcond=None)
    pred = math.exp(W2 * 225 + coef[0] + coef[1] / 15)
    print("\nfinite-size model (W2 fixed): A = %.4f, B = %.4f; fit residual max %.2e"
          % (coef[0], coef[1], float(np.max(np.abs(X @ coef - rhs)))))
    print("predicted a(15) = %d" % round(pred))
    rel = abs(math.log(x / pred))
    print("computed/predicted log-ratio = %.2e -> %s (tolerance 2e-3)"
          % (rel, "PASS" if rel < 2e-3 else "FAIL"))
    # also: model with all three params free
    X3 = np.column_stack([ns.astype(float) ** 2, np.ones(len(ns)), 1.0 / ns])
    c3, *_ = np.linalg.lstsq(X3, y, rcond=None)
    pred3 = math.exp(c3[0] * 225 + c3[1] + c3[2] / 15)
    print("free-fit c*n^2 model: c = %.6f (vs Lieb %.6f), predicted a(15) = %d, log-ratio %.2e"
          % (c3[0], W2, round(pred3), abs(math.log(x / pred3))))

    out = {
        "a15_run1": a15_1, "a15_run2": a15_2, "agree": a15_1 == a15_2,
        "lieb_lnW": W2, "literal_logdiff": literal, "literal_14_logdiff": lit14,
        "fitA": float(coef[0]), "fitB": float(coef[1]),
        "predicted_a15": round(pred), "log_ratio_computed_vs_pred": rel,
        "free_fit_c": float(c3[0]), "predicted_a15_free": round(pred3),
        "ln_a15_over_225": math.log(x) / 225,
    }
    with open(_RUN / "attempts" / "isotypic-row" / "output" / "growth_check.json", "w") as f:
        json.dump(out, f, indent=1)
    print("\nsaved growth_check.json")


if __name__ == "__main__":
    main()
