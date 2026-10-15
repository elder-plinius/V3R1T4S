#!/usr/bin/env python3
"""build_symmetric.py: rebuild a mirror-symmetric two-environment adversary mixture from its two parameters.

Written at packaging time (2026-10-15). During the run, the step that wrote the final object (an exact evaluation of
11 rational points of this family, see how-we-built-it/COMMANDS.md) was an inline script that was not saved; this file
re-implements that step from the family's definition and reproduces object/mixture.json byte for byte for
x_H = 33307/40000 and mu_A = 417121/1000000. Python 3 standard library only.

Usage:  python3 -I build_symmetric.py X_H MU_A OUT.json      e.g.  33307/40000 417121/1000000 rebuilt.json

Family (the shape of Theorem 3.4 of arXiv:2604.24517v2, which is the point x_H = 5/6, mu_A = 5/12):
  both experts in both environments report x_L = 1 - x_H or x_H (binary signals);
  environment A, weight 1/2: states theta = (0, x_H), prior mean mu_A;
  environment B, weight 1/2: the mirror image under x -> 1 - x: states theta = (x_L, 1), prior mean 1 - mu_A.
In each environment the prior is lambda_2 = (mu - theta_1)/(theta_2 - theta_1), each expert reports x_H with
probability q = (mu - x_L)/(x_H - x_L) (Bayes plausibility), and the likelihoods Pr[signal | state] are the ones
that make the reports equal the posterior means (the same formula as lik() in mix_opt.py).
"""
import sys, json
from fractions import Fraction as Fr


def env(th1, th2, mu, xl, xh):
    d = th2 - th1
    lam2 = (mu - th1) / d
    lam1 = 1 - lam2
    q = (mu - xl) / (xh - xl)
    pl = (xl - th1) / d
    ph = (xh - th1) / d
    assert 0 <= th1 < th2 <= 1 and 0 < lam1 < 1 and 0 < q < 1
    lik = [[str((1 - pl) * (1 - q) / lam1), str((1 - ph) * q / lam1)],
           [str(pl * (1 - q) / lam2), str(ph * q / lam2)]]
    return {"weight": "1/2", "theta": [str(th1), str(th2)], "prior": [str(lam1), str(lam2)],
            "experts": [{"likelihoods": lik}, {"likelihoods": [row[:] for row in lik]}],
            "reports": [[str(xl), str(xh)], [str(xl), str(xh)]], "mu": str(mu)}


def main():
    if len(sys.argv) != 4:
        print("usage: build_symmetric.py X_H MU_A OUT.json")
        sys.exit(2)
    xh, mu_a, out = Fr(sys.argv[1]), Fr(sys.argv[2]), sys.argv[3]
    xl = 1 - xh
    assert Fr(1, 2) < xh < 1 and xl < mu_a < xh
    d = {"environments": [env(Fr(0), xh, mu_a, xl, xh), env(xl, Fr(1), 1 - mu_a, xl, xh)]}
    with open(out, "w") as f:
        json.dump(d, f, indent=1)
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
