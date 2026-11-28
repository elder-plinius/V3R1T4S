# PREREG addendum — the counting constraint moves from the formula into the checked proof

Written 2026-11-11T22:56:28Z (time from `date -u`). State at that moment, stated plainly: the chain of class lemmas
was running (3 classes of encoding 1 finished); the derivation described below had passed its tests on small boards
for both encodings; its first full-size check (encoding 1, 11 x 11) had been started and its verdict was NOT yet known.
PREREG.md is unchanged. This file only records a change of the object, decided after PREREG.md and before any claim.

What changes
- Old object: F = the encoder's formula, which contains ONE implied constraint (sum over classes of min(|class|, 7)
  <= 121) that is true for every partition but was not derived inside the proof. PREREG.md disclosed this.
- New object: Fbase = F without the clauses of that constraint, with the same variable numbers. Fbase is a subset of
  F, so "Fbase is unsatisfiable" is the stronger statement and implies the old one. What Fbase still contains beyond
  the bare constraints: auxiliary variables with two-way definitions, and the symmetry breaking on class labels.
- The counting bound is now derived inside the proof of the final step (attempts/counting-in-proof/code/counting.py):
  new variables are introduced by definition, the bound follows by unit-propagation steps, and drat-trim checks all
  of it together with the solver's refutation: drat-trim on (Fbase + 60 lemma clauses, derivation + refutation).
- The class lemma chain is unaffected: its premises are clauses that mention one class only, and none of the removed
  clauses is of that kind. audit_chain.py is run against Fbase instead of F, so this is checked, not assumed.

What does not change: the criterion, the cell, the cross-checks on the satisfiable side, the requirement of two
independently written encodings, and the panel. If the full-size check fails or is too heavy, the object stays the
old one, with its disclosed constraint, and this file says so in the report.

null_test: not needed because the claims are certificates checked deterministically by an independent proof checker
