# Honesty gate

status: CONFIRMED_PARTIAL
confirmed_scope: under reading B, a(15) = 4310182149988584261406143524214457416387448 is confirmed as the next unknown term of A054759 produced under the two-run and reproduction rules with all margins verified, with the documented caveat that the full criterion's literal 1e-3 growth clause is unsatisfiable at N=15 for any correct value while the value is consistent with Lieb's constant under the published terms' own finite-size model (1.354e-4).

## Gate reasoning (main session, after reading all three panel files)

- REPRODUCE (context: subagent, pass: true): re-ran crt_check.py (OVERALL PASS; both CRTs -> value.txt;
  28/28 residues consistent; prime sets disjoint; moduli 2^209.5/2^208.6 vs rigorous bound 2^168.8,
  margins 1.8e12/9.7e11), re-ran both ladder modes fresh (14/14 OK each, outputs identical to the saved
  JSONs), and executed the bank's fresh-prime verification with its own prime (29881): both programs
  printed 10495 = value.txt mod 29881. Found and the main session repaired: REPRODUCE.md's prime-bound
  text (exactness guard requires P < 2^15; fail-fast, no wrong output) - a documentation defect, not an
  arithmetic one.
- NOVELTY (context: subagent, pass: true): live OEIS entry/b-file end at a(14) (McKay 2024-04-18); the
  claimed value appears nowhere; revision history shows no term additions in the recent window; external
  searches (arXiv incl. full-text of Finch errata, GitHub, GenericTensorNetworks) found no prior a(15);
  a(15)/a(14) agrees with Lieb's growth prediction to 0.05%.
- CRITERION (repair round 1, context: subagent (repair round 1, criterion lane), pass: true): resolved
  the inheritance question the first lane left open by the bank's own words - p1's "same two-run and
  reproduction rules" lifts clauses 2 and 3 verbatim; clause 4's operative words appear nowhere in p1 -
  so the narrower literal reading (B) holds, and reading A would make p1 unwinnable by construction
  (the 1e-3 clause fails for the PUBLISHED a(14) harder than for the claimed a(15): 0.0055 vs 0.0048;
  n^2*delta ~ 1.08 stable over n = 4..15; first attainable ~N >= 33). Independently re-verified: own
  CRT implementation (both sets -> value.txt), own live b-file fetch (a(15) absent), 28/28 ladder
  congruences, bound arithmetic, growth model reproduction (50/50 checks). The first criterion lane's
  pass:false verdict is preserved at claim/criterion.v1.md.
- Downgrade checklist (step 7): no hedging panelist; no reproduction mismatch; the cell was EMPTY
  (a(15) unknown) so the value strictly beats the live table; no stretched criterion (the repair lane
  explicitly considered and rejected the stretch, choosing the narrower reading); scope no wider than
  reproduced; no samples-as-complete; no capped-search exclusions; no probable primes; no bundled
  objects; no empirical baseline involved (explicit-object target). Panel table fetches are fresh
  (< 6 h, re-fetched by the repair lane).
- Residual criterion defect recorded for the bank: the full criterion's growth clause is defective at
  small N for this sequence (documented in claim/growth.json; bank-amendment draft PR accompanies the
  claim PR).

verdict: partial win p1 of square-grid-lattice-gas-exact-counts-oeis, CONFIRMED_PARTIAL.
