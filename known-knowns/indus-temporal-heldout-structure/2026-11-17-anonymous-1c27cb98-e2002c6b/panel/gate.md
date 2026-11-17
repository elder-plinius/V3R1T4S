# Honesty gate — run 5 (indus-temporal-heldout-structure, object-type predictability claim)

The run's main session read all three panel files (panel/reproduce.md, panel/novelty.md,
panel/criterion.md) and the verdicts itself. All three skeptics were fresh isolated
subagents that saw only the claim folder (NOVELTY additionally the pinned repo for its
TROPHY_CASE/known-knowns/PR check; REPRODUCE additionally a scratch copy of the claim
folder plus python3/sha256sum). All three wrote `context: subagent` and ended
`pass: true`.

## Panel verdicts
- **REPRODUCE: PASS.** Independent checker (written from the README definition before
  reading the author's code) re-derived: the full 1,613-object held-out pool
  (post-1977 + exact-sequence/identity-core dedup + M77-leak exclusion + OOV->wildcard),
  the M77 training set (3,548 lines; class split 2694/707/127/20; vocab 417), every
  per-object prediction (1,613/1,613, multiset-identical to pool_detail), the per-site
  accuracies of all three systems, and the full 10,000-resample paired bootstrap
  (re-run, seed 20261117) — all matching the stored files exactly. The frozen ctx-count
  sha256 and the reading-direction fingerprint reproduce. No unseeded RNG, no
  dict/hash-order dependence (two reruns byte-identical modulo timestamps). Discrepancies
  found are outside property A: a stale p2 block value inside output_sweep_main.json
  (all versions agree p2 is negative) and 544 stale "Bull" symfam labels (recorded DB
  cross-coding artifact).
- **NOVELTY: PASS.** Status source fetched once, honestly (GitHub API metadata for
  joyboseroy/indus_decipher, 2026-11-17T03:23:41Z, byte-identical to the scout's record):
  still undeciphered, 2026-10-03 status unchanged. 24-month literature/code search
  (Kriger & Hunt 2026, Kriger 2026, arXiv 2608.02999 SIGIL, arXiv 2604.17828, paragorth
  P1-P9/Q1-Q14/R1-R13 prereg files, the pinned repo's TROPHY_CASE.md and open/closed PRs —
  one earlier filed Indus claim, PR #570 masked-sign M77-CLSS, closed unmerged 2026-11-03
  for failing p3, a different property): no post-2026-10-03 publication occupies the
  temporal M77->post-1977 dual-baseline multi-site object-type cell. The re-run novelty
  diff (21 comparators, all NOT equivalent) matches the stored object exactly.
- **CRITERION: PASS (full criterion, not p1/p2/p3).** Literal check of every condition:
  M77-only fit (nothing held-out leaks into any fit; KN discount tuned on the in-M77 10%
  split; synthetic control built from the M77 stream); one shared resample index per site,
  p = claim <= max(KN, synth) so both baselines are beaten simultaneously on the same
  resamples; p=0.0 < 0.001 at pooled (n=1613), Mohenjo-daro (n=665) and Harappa (n=590) —
  exactly the sites (d) names, each n>=20; (a) all 1,613 objects have a documented
  post-1977 first-publication source (CISI-numbered or Dholavira/Lothal excavation-report
  class), 0 violations; (b) the 386-identity directory (sha256-verified) with length>=2
  cores gives 2,363 -> 1,613 reps, 0 duplicate (cisi, sequence) pairs; (c) not equivalent
  to any P/Q or published positional finding; (d) beats both baselines at MD and Harappa
  separately. Null test: 30,000 bootstrap controls >= 400, real beats all, command
  present, numbers match the stored null-test object exactly; the synthetic control is a
  fair SIGIL-style match (length-matched by construction; the unigram match is on the M77
  side, the honest reading of "fitted only on M77"). Baseline record: registry counts
  exact; the four in-sample Q/P tolerance misses are honestly recorded UNRESOLVED, never
  retuned. Hidden quantifiers found, none changing scope: exact-sequence dedup was not a
  separate code step (57 groups of identical sequences across different object IDs remain,
  allowed by the literal "(object ID, exact sequence)" wording; the skeptic's independent
  exact-seq-dedup re-run still gives p=0.0 beating both baselines at both sites); the
  merged corpus carries 776 duplicate cisi IDs (2,104 records) that survive as distinct
  (ID, seq) pairs; the "400-draw synthetic pool" wording in null_test.md has no code path
  (immaterial — the >=400 rule stands on the 30,000 bootstrap comparisons); M77 class
  priors (Seal 0.759) vs the held-out Seal share (0.589) are recorded; p=0.0 is a
  0/10,000 bound, not a point estimate.

## Gate decision
No downgrade trigger: no hedging panelist (all three give a clean pass with the evidence
named), no reproduction mismatch (independent re-derivation exact), the value strictly
beats both baselines at all three required sites (thinnest margin: Harappa +0.0881 over
the best control), no stretched criterion or hidden quantifier that changes scope, the
scope is exactly what was reproduced, no sample presented as complete (full 10,000-
resample bootstrap, full 1,613-object set), no capped search used as an exclusion, no
evasion-obtained values, one object (the 4-class object-type property; the 2-class
Seal-vs-Tablet is its recorded sub-property, not a second bundled claim), and the
unresolved baseline items (the in-sample Q/P tolerance misses) are documented and the
claim does not depend on them. The panel's status-source fetch (03:23:41Z) is fresh
(<6h at gate time 05:2xZ).

Final status: CONFIRMED_SOLUTION (the full success criterion of the bank target is met;
this is not a p1/p2/p3 partial win). The claim is packaged in
outbox/2026-11-17-anonymous-1c27cb98-e2002c6b (kit/SUBMIT.md section 1); the package's
check must print CHECK_RUN: PASS before the status stands.

status: CONFIRMED_SOLUTION
confirmed_scope: The class-conditional positional trigram model (n<=3, add-one, wildcard OOV, seed 20261117) fitted only on the M77 1977 corpus predicts the 4-class object type (seal/tablet/pottery/other) of the 1,613-object deduplicated post-1977 held-out pool (pooled n=1613: 0.5846 vs Kneser-Ney 0.2808 and synthetic 0.1872, p=0.0; Mohenjo-daro n=665: 0.7098 vs 0.3293/0.1173, p=0.0; Harappa n=590: 0.4017 vs 0.2153/0.2441, p=0.0; paired bootstrap 10,000 resamples), beating both baselines simultaneously at pooled, Mohenjo-daro and Harappa — a full-criterion win, not any of the enumerated partial wins p1/p2/p3.
