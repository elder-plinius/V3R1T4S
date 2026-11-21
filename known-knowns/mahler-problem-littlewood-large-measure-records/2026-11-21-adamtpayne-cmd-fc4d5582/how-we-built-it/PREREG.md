# PREREG (written 2026-11-21T19:27:25Z)
Honest timeline: the unseeded search (2 min per even degree 32..60) and the certification of d = 32, 36, 40 ran before this file (~18:50-19:10Z). The criterion is the bank's fixed rule (certified M > table max + 1e-9, Arb or two methods to 20 digits), so there is no threshold to tune.
Checker: code/certify.py (Arb ball lower end minus table value > 1e-9; mpmath 60-digit cross-check).
null_test: not needed because each claim is an explicit polynomial whose Mahler measure is certified by rigorous ball arithmetic and compared with a table value.
