# PREREG (frozen before any solver output is scored)
written: 2026-10-15 13:27:14 UTC
target: card-guessing-yes-no-feedback-exact

## Criterion (verbatim from the bank)
Exact values of P+_{2,n} (two copies of each of n labels, yes/no feedback, maximise the expected number of correct guesses) as reduced rationals for EVERY n from 11 through 16 (direction: first exact values; none published), each accompanied by a Bellman certificate: the table of V+(r, f) over all reachable canonical states, which a checker verifies state by state against Luo's recursion (arXiv:2609.25062, Appendix A: p_i = C(r - e_i, f)/C(r, f), V+(r, f) = max_i { p_i [1 + V+(r - e_i, f)] + (1 - p_i) V+(r, f + e_i) }, V+ = 0 when no free position remains). The same code must reproduce Table 3 of Diaconis-Graham-Spiro for n = 2..10 to four decimals, and any newer published values found via the status source must be matched or exceeded in range.

## Statistic and checker
- Object per n: the exact value P+_{2,n} as a reduced fraction, plus a certificate table listing every reachable
  canonical state s (g, sorted (r_i,f_i) pairs of labels with r_i >= 1) with the integer W(s) = C(s) V+(s).
- Checker (written here from the definition, independent of the solver): for every listed state, recompute C(s) from
  (A.1) with exact integers; confirm C(s) > 0; for L = 0 confirm W = 0; for L >= 1 evaluate, for every label class
  (including exhausted labels when any exist), the literal right-hand side of Luo's recursion as an exact rational
  from the table's own successor values (a successor absent from the table must have C = 0 recomputed by the checker),
  and confirm V+(s) = W(s)/C(s) equals the maximum; confirm the initial state carries the claimed value. Every state
  in the table is checked (no sampling).
- Thresholds (all must hold for a solution claim; p1 = the same for n = 11, 12, 13):
  T1 exact values for n = 11..16 from this run's solver, each with a certificate passing the checker on every state;
  T2 independent agreement: this run's values equal the Codex candidate values for every n = 2..16 (two solvers,
     written separately); any disagreement means no claim until resolved by a third derivation;
  T3 raw-definition agreement: the solver equals the brute force on (n,m) = (2,2),(3,2),(4,2),(2,3),(3,3),(2,4),
     (3,1),(4,1),(5,1) exactly;
  T4 calibration strict: for n = 2..10 the exact value rounded to four decimals equals the DGS table entry;
     calibration tolerant: |exact - printed| < 10^-4 (printed is the rounding or the truncation). The n = 7 entry
     is expected to fail strict (3.0324 vs printed 3.0323) and pass tolerant; both results are reported as such and
     the claim states the discrepancy. The criterion wording "to four decimals" is read as the tolerant test; the
     CRITERION skeptic decides.
- p2 (persistence) statistic, pre-registered: over all reachable states s with L(s) >= 2 and every active label i
  whose failure successor s' = (r, f + e_i) has C(s') > 0: count pairs where class i is NOT among the maximisers at
  s' (variant any-guess), and the same restricted to i being a maximiser at s (variant optimal-guess). A p2 claim
  needs at least one optimal-guess violation, exhibited as an explicit state with exact values, AND the conjecture
  wording confirmed in the 1981/2001 sources; otherwise p2 is reported as a negative or as unconfirmed.
null_test: not needed because the objects are explicit exact rationals with Bellman certificates checked by a
deterministic checker against a published recursion and table; no search or statistical claim is made.

## Disclosure
The Codex candidate values were visible in the dossier before this prereg (data); this run's solver is written
without reading the Codex solver code.
