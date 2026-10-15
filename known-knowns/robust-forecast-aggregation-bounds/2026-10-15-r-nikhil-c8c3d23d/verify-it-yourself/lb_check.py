#!/usr/bin/env python3
"""lb_check.py: exact-rational checker for a LOWER BOUND on the minimax regret of prior-agnostic robust forecast
aggregation with conditionally independent (CI) experts (Chen, Peng, Tang, arXiv:2604.24517v2, Section 2, Section 3,
Theorem 3.4). Written from the definition, standard library only.

Object checked: an adversary distribution D over finitely many environments. Each environment has
  theta = [theta1, theta2] with 0 <= theta1 <= theta2 <= 1   (binary state space, Bernoulli outcome means)
  prior = [lambda1, lambda2]                                    (prior over the two states, sums to 1)
  experts = [E1, E2], each with likelihoods[state][signal] = Pr[signal | theta_state] (rows sum to 1)
  weight = D's probability of this environment (weights sum to 1)
Signals are CI given the state: pi(s1, s2 | theta) = pi1(s1 | theta) * pi2(s2 | theta).
Reports: x_i(s_i) = Pr[omega = 1 | s_i] = E[theta | s_i]. Omniscient: fBayes(s) = Pr[omega = 1 | s1, s2] = E[theta | s].
Loss: squared. Regret of f in an environment: L(f) = E[(f(x(s)) - omega)^2 - (fBayes(s) - omega)^2].
Statement certified (Yao's principle, as in the proof of Theorem 3.4):
  for every aggregation function f: sup_env L(f | env) >= E_D[L(f | env)] >= min_g E_D[L(g | env)] = LB(D),
  where the minimiser g = f* is the D-weighted conditional mean of fBayes given the report pair.
Output: LB(D) as an exact fraction, computed two independent ways, and the comparison with the bar 31/1326.
Exit code 0 only if the object is well formed, both computations agree, and LB(D) > 31/1326.
"""
import sys, json
from fractions import Fraction as F

BAR = F(31, 1326)

def frac(x):
    if isinstance(x, str):
        return F(x)
    if isinstance(x, int):
        return F(x)
    raise ValueError("numbers must be strings like '1/6' or integers, got %r" % (x,))

def load(path):
    with open(path) as fh:
        d = json.load(fh)
    envs = []
    for k, e in enumerate(d["environments"]):
        w = frac(e["weight"])
        th = [frac(t) for t in e["theta"]]
        pr = [frac(p) for p in e["prior"]]
        ex = [[[frac(v) for v in row] for row in exp["likelihoods"]] for exp in e["experts"]]
        envs.append((w, th, pr, ex))
    return envs

def validate(envs):
    assert len(envs) >= 1, "no environments"
    assert sum(w for w, *_ in envs) == 1, "weights must sum to 1"
    for k, (w, th, pr, ex) in enumerate(envs):
        assert 0 <= w <= 1, "env %d: weight out of [0,1]" % k
        assert len(th) == 2 and len(pr) == 2, "env %d: binary state space required" % k
        assert 0 <= th[0] <= th[1] <= 1, "env %d: need 0 <= theta1 <= theta2 <= 1" % k
        assert all(0 <= p <= 1 for p in pr) and sum(pr) == 1, "env %d: prior must be a distribution" % k
        assert len(ex) == 2, "env %d: two experts required" % k
        for i, lik in enumerate(ex):
            assert len(lik) == 2, "env %d expert %d: one likelihood row per state" % (k, i)
            ns = len(lik[0])
            assert ns >= 1 and len(lik[1]) == ns, "env %d expert %d: ragged likelihoods" % (k, i)
            for row in lik:
                assert all(0 <= v <= 1 for v in row) and sum(row) == 1, "env %d expert %d: rows must be distributions" % (k, i)

def analyse(envs):
    """Returns (LB via variance form, LB via literal loss definition, number of distinct report pairs)."""
    M0, M1, M2 = {}, {}, {}
    # literal-definition accumulator needs f* first, so store per-environment signal data
    records = []  # (w, theta, P(theta,s) table, report pair key, fBayes)
    for (w, th, pr, ex) in envs:
        lik1, lik2 = ex
        n1, n2 = len(lik1[0]), len(lik2[0])
        # expert reports x_i(s_i) = E[theta | s_i]
        def reports(lik, ns):
            out = []
            for s in range(ns):
                ps = pr[0] * lik[0][s] + pr[1] * lik[1][s]
                if ps == 0:
                    out.append(None)
                else:
                    out.append((pr[0] * lik[0][s] * th[0] + pr[1] * lik[1][s] * th[1]) / ps)
            return out
        x1 = reports(lik1, n1)
        x2 = reports(lik2, n2)
        fb_by_key = {}
        for s1 in range(n1):
            for s2 in range(n2):
                p = [pr[0] * lik1[0][s1] * lik2[0][s2], pr[1] * lik1[1][s1] * lik2[1][s2]]  # P(theta_j, s1, s2)
                ps = p[0] + p[1]
                if ps == 0:
                    continue
                fbayes = (p[0] * th[0] + p[1] * th[1]) / ps
                key = (x1[s1], x2[s2])
                # within one environment fBayes must be a function of the report pair (it is, under CI; verify)
                if key in fb_by_key:
                    assert fb_by_key[key] == fbayes, "fBayes is not a function of the reports inside an environment"
                fb_by_key[key] = fbayes
                M0[key] = M0.get(key, F(0)) + w * ps
                M1[key] = M1.get(key, F(0)) + w * ps * fbayes
                M2[key] = M2.get(key, F(0)) + w * ps * fbayes * fbayes
                records.append((w, th, p, key, fbayes))
    fstar = {k: M1[k] / M0[k] for k in M0}
    lb_var = sum(M2[k] - M1[k] * M1[k] / M0[k] for k in M0)
    # literal definition: E[ (f*(x)-omega)^2 - (fBayes-omega)^2 ], omega ~ Bern(theta_j); E[(a-omega)^2] = a^2 - 2 a theta + theta
    lb_lit = F(0)
    for (w, th, p, key, fbayes) in records:
        a = fstar[key]
        for j in range(2):
            if p[j] == 0:
                continue
            lb_lit += w * p[j] * ((a * a - 2 * a * th[j]) - (fbayes * fbayes - 2 * fbayes * th[j]))
    return lb_var, lb_lit, len(M0), fstar

def main():
    if len(sys.argv) < 2:
        print("usage: lb_check.py mixture.json [--bar p/q]"); sys.exit(2)
    bar = BAR
    if "--bar" in sys.argv:
        bar = F(sys.argv[sys.argv.index("--bar") + 1])
    envs = load(sys.argv[1])
    validate(envs)
    lb_var, lb_lit, npairs, fstar = analyse(envs)
    print("environments: %d" % len(envs))
    print("distinct report pairs: %d" % npairs)
    print("LB_variance_form: %s" % lb_var)
    print("LB_literal_definition: %s" % lb_lit)
    print("LB_float: %.12f" % float(lb_var))
    print("bar: %s (%.12f)" % (bar, float(bar)))
    agree = (lb_var == lb_lit)
    print("two_computations_agree: %s" % ("yes" if agree else "no"))
    better = agree and lb_var > bar
    print("LB_strictly_greater_than_bar: %s" % ("yes" if better else "no"))
    if better:
        print("margin: %s (%.3e)" % (lb_var - bar, float(lb_var - bar)))
    print("verdict: %s" % ("LOWER_BOUND_BEATS_BAR" if better else "NO_IMPROVEMENT"))
    sys.exit(0 if better else 1)

if __name__ == "__main__":
    main()
