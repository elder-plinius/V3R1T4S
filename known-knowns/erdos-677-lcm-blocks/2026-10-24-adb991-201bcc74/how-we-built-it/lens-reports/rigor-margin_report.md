# Lens report: rigor-margin (Erdős 677), run 2026-10-24-0818

(Saved by the run's main session from the lens's hand-back text. The harness refused the lens's own write. Every
number below is in out/, as named.)

claim level: progress

## Result

The R2 margin is proved in rigorous arithmetic for every k = 3..25 and every r in `deep_cf.admissible_r(k)`:
63041 of 63041 (k, r) pairs, 0 failures, 0 undecided. Two checkers, both written from the mathematics, each prove it:
- code/rig_margin.py: mpmath.iv intervals at 320 bits; ρ is enclosed in a dyadic bracket of width 2^-256, verified in
  exact integers.
- code/rig_margin_exact.py: intervals with exact rational endpoints and no floating point; ρ comes from an exact
  integer k-th root, bracket width 2^-96.

Final lines: "TOTAL pairs=63041 failures=0 undecided=0" in out/rig_margin_k3-25_X1e6_eta1e-3.txt and in
out/rig_margin_exact_k3-25_X1e6_eta1e-3.txt. The worst certified relative margin is 0.99999996, at k = 25,
r = 2737/2736.

**Statement proved.** For each k in 3..25 and each r in `deep_cf.admissible_r(k)`, with
F(Z) = ∏_{j=1..k}(Z + j − (k+1)/2), ρ = r^{1/k}, c = (k²−1)(ρ²−1)/(24ρ) and η = 1/1000: for every real X ≥ 10^6, the
unique Y > (k−1)/2 with F(Y) = rF(X) satisfies c(1−η) < X(ρX − Y) < c(1+η).

**Method** (full proof in NOTES.md, "Task B"):
- F is a strictly increasing bijection from [(k−1)/2, ∞) onto [0, ∞).
- If C > 0 and ρX0 − C/X0 > (k−1)/2, then X(ρX−Y) < C exactly when P_C(X) = X^k[rF(X) − F(ρX − C/X)] > 0. This
  domain condition is checked for every pair.
- P_C = Σ_t a_t X^{2k−2t}. Here a_0 = r − ρ^k = 0 by identity, so it is never computed. For C = c(1±η),
  a_1 = ±η·s·ρ^{k−2}(ρ²−1), with s = k(k²−1)/24.
- The sign test is a_1 > Σ_{t≥2} |a_t| X0^{−2(t−1)}, decided on interval endpoints. Anything undecided counts as a
  failure.

**Negative tests (k = 3..12, 394 pairs).** The checkers fail on wrong margins (out/*NEG*):
- η = 0: 394 undecided (both checkers).
- X0 = 10: 394 undecided.
- η = 10^-14: 394 undecided.
- Margin centred at c(1 ± 2η) instead of c: 394 FAIL each.

**Diagnostic.** With X0 = 1000, all 63041 pairs are still proved, with worst margin 0.95798066
(out/rig_margin_DIAG_k3-25_X1e3_eta1e-3.txt).

**Non-rigorous cross-check** (88 sampled pairs, out/sanity_margin_NS4.txt):
- The coefficient expansion matches direct evaluation to a relative error of 3.3e-69.
- Solving F(Y) = rF(X) at 150 digits gives |X(ρX−Y)/c − 1| ≤ 4.14e-11 at X = 10^6.

## Task A: completeness of the ratio set

Lemma A was re-derived in 9 steps (NOTES.md). The lemma allows S_A(k) = {∏_{p<k} p^{d_p} : |d_p| ≤ L_p(k)} ∩
(1, lcm(1..k)/k]. An independent generator gives S_A(k) = `admissible_r(k)` for every k = 3..25: missing 0, extra 0.
The 23 set sizes total 63041.

Two further checks agree:
- The ratios realisable by block counts (residues and CRT) form exactly S_A(k).
- All 970 equal-lcm pairs with n < m ≤ 3000 and k = 3..25 have r in the set (out/taskA_ratio_audit_NB3000.txt).

## Per-k results (exact checker; the interval checker gives identical counts)

```
k=3 pairs=1 proved=1 failures=0 undecided=0 time_s=0.0 worst_rel_margin_lower_bound=1.00000000 at r=2
k=4 pairs=1 proved=1 failures=0 undecided=0 time_s=0.0 worst_rel_margin_lower_bound=1.00000000 at r=3
k=5 pairs=7 proved=7 failures=0 undecided=0 time_s=0.0 worst_rel_margin_lower_bound=1.00000000 at r=4/3
k=6 pairs=4 proved=4 failures=0 undecided=0 time_s=0.0 worst_rel_margin_lower_bound=1.00000000 at r=2
k=7 pairs=22 proved=22 failures=0 undecided=0 time_s=0.1 worst_rel_margin_lower_bound=1.00000000 at r=6/5
k=8 pairs=13 proved=13 failures=0 undecided=0 time_s=0.1 worst_rel_margin_lower_bound=1.00000000 at r=7/5
k=9 pairs=31 proved=31 failures=0 undecided=0 time_s=0.2 worst_rel_margin_lower_bound=0.99999999 at r=8/7
k=10 pairs=37 proved=37 failures=0 undecided=0 time_s=0.2 worst_rel_margin_lower_bound=0.99999999 at r=7/6
k=11 pairs=157 proved=157 failures=0 undecided=0 time_s=1.4 worst_rel_margin_lower_bound=0.99999999 at r=36/35
k=12 pairs=121 proved=121 failures=0 undecided=0 time_s=1.3 worst_rel_margin_lower_bound=0.99999999 at r=22/21
k=13 pairs=472 proved=472 failures=0 undecided=0 time_s=6.0 worst_rel_margin_lower_bound=0.99999999 at r=56/55
k=14 pairs=337 proved=337 failures=0 undecided=0 time_s=5.5 worst_rel_margin_lower_bound=0.99999999 at r=66/65
k=15 pairs=283 proved=283 failures=0 undecided=0 time_s=5.6 worst_rel_margin_lower_bound=0.99999999 at r=78/77
k=16 pairs=202 proved=202 failures=0 undecided=0 time_s=4.0 worst_rel_margin_lower_bound=0.99999998 at r=65/63
k=17 pairs=1822 proved=1822 failures=0 undecided=0 time_s=48.3 worst_rel_margin_lower_bound=0.99999998 at r=144/143
k=18 pairs=850 proved=850 failures=0 undecided=0 time_s=25.9 worst_rel_margin_lower_bound=0.99999998 at r=221/220
k=19 pairs=5467 proved=5467 failures=0 undecided=0 time_s=187.1 worst_rel_margin_lower_bound=0.99999998 at r=936/935
k=20 pairs=3037 proved=3037 failures=0 undecided=0 time_s=123.7 worst_rel_margin_lower_bound=0.99999997 at r=1292/1287
k=21 pairs=3280 proved=3280 failures=0 undecided=0 time_s=150.4 worst_rel_margin_lower_bound=0.99999997 at r=286/285
k=22 pairs=4252 proved=4252 failures=0 undecided=0 time_s=225.1 worst_rel_margin_lower_bound=0.99999997 at r=456/455
k=23 pairs=16402 proved=16402 failures=0 undecided=0 time_s=960.3 worst_rel_margin_lower_bound=0.99999996 at r=936/935
k=24 pairs=9841 proved=9841 failures=0 undecided=0 time_s=607.5 worst_rel_margin_lower_bound=0.99999996 at r=715/714
k=25 pairs=16402 proved=16402 failures=0 undecided=0 time_s=1102.3 worst_rel_margin_lower_bound=0.99999996 at r=2737/2736
```

## Caveats (from the lens)

- **Trust base:** Python integers, fractions.Fraction, and deep_cf.admissible_r. mpmath.iv is used only by the
  interval checker.
- **Not audited by this lens:** the link to the enumeration, i.e. that deep_rig.py loops over exactly
  admissible_r(k) and uses this margin with the (p, q) = (Y, X) or (2Y, 2X) scaling. That is for the enumeration's
  owner and the panel.
- **Process slip:** around 08:35 UTC, two of this lens's processes overlapped for about a minute (logged in NOTES.md).

dead lines:
- **Residue counting (H7)** cannot shrink the ratio set: the count-realisable set equals the Lemma A set for every
  k ≤ 25.
- **Descartes/Sturm certificates (H6)** are not needed: the leading-term-dominates-tail test decides every case, with
  slack ≥ 0.99999996 at X0 = 10^6 and ≥ 0.957 at X0 = 1000.
- **Precision loss (H2/H8)** does not occur: r near 1 and large-R(k) curves (e.g. r = 2737/2736) are decided with
  wide room in both arithmetics.
- **Level off-by-one (H4)** does not occur, for either p^i < k vs ≤ k or k a prime power: missing 0, extra 0 for all k.
