#!/usr/bin/env python3
"""check_declared_fields.py: checks that every field declared in the object file is consistent with the structure.

Written at packaging time (2026-10-15), Python 3 standard library only, exact rationals. lb_check.py and
independent_recheck.py compute the certified bound from the weights, states (theta), priors and likelihoods only; the
object also declares, for the reader, each environment's prior mean ("mu") and each expert's report values
("reports"). This script recomputes those from the definition of Section 2 of arXiv:2604.24517v2
(mu = E[theta]; report x_i(s_i) = Pr[omega = 1 | s_i] = E[theta | s_i], listed in signal order) and fails if any
declared value differs, if a model constraint is violated, or if the file has fields it does not know.
Usage: python3 -I check_declared_fields.py mixture.json        Exit code 0 only if everything is consistent.
"""
import sys, json
from fractions import Fraction as F

KNOWN_ENV_KEYS = {"weight", "theta", "prior", "experts", "reports", "mu"}


def main(path):
    with open(path) as fh:
        d = json.load(fh)
    problems = []
    if set(d) != {"environments"}:
        problems.append("top-level keys %s (expected only 'environments')" % sorted(d))
    envs = d.get("environments", [])
    total = sum((F(e["weight"]) for e in envs), F(0))
    if total != 1:
        problems.append("weights sum to %s, not 1" % total)
    for k, e in enumerate(envs):
        extra = set(e) - KNOWN_ENV_KEYS
        if extra:
            problems.append("env %d: unknown keys %s" % (k, sorted(extra)))
        th = [F(x) for x in e["theta"]]
        lam = [F(x) for x in e["prior"]]
        w = F(e["weight"])
        if not (0 <= w <= 1):
            problems.append("env %d: weight %s outside [0,1]" % (k, w))
        if not (len(th) == 2 and 0 <= th[0] < th[1] <= 1):
            problems.append("env %d: need 0 <= theta_1 < theta_2 <= 1, got %s" % (k, e["theta"]))
        if not (len(lam) == 2 and min(lam) >= 0 and sum(lam) == 1):
            problems.append("env %d: prior is not a distribution: %s" % (k, e["prior"]))
        mu = lam[0] * th[0] + lam[1] * th[1]
        if "mu" in e and F(e["mu"]) != mu:
            problems.append("env %d: declared mu %s but prior and states give %s" % (k, e["mu"], mu))
        if len(e["experts"]) != 2:
            problems.append("env %d: two experts required" % k)
        for i, ex in enumerate(e["experts"]):
            L = [[F(v) for v in row] for row in ex["likelihoods"]]
            if len(L) != 2 or len(L[0]) != len(L[1]) or any(min(r) < 0 or sum(r) != 1 for r in L):
                problems.append("env %d expert %d: likelihood rows are not distributions" % (k, i))
                continue
            rep = []
            for s in range(len(L[0])):
                ps = lam[0] * L[0][s] + lam[1] * L[1][s]
                rep.append(None if ps == 0 else (lam[0] * L[0][s] * th[0] + lam[1] * L[1][s] * th[1]) / ps)
            if "reports" in e:
                declared = [F(x) for x in e["reports"][i]]
                if declared != rep:
                    problems.append("env %d expert %d: declared reports %s but likelihoods give %s"
                                    % (k, i, e["reports"][i], [str(x) for x in rep]))
            print("env %d expert %d: weight %s, theta %s, mu %s, reports %s" % (k, i, w, [str(x) for x in th], mu,
                                                                               [str(x) for x in rep]))
    for p in problems:
        print("problem: " + p)
    print("declared fields consistent: %s" % ("no" if problems else "yes"))
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: check_declared_fields.py mixture.json")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
