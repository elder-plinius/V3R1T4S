# PREREG (frozen 2026-10-31T22:26Z, before any lens output of this run exists)

null_test: not needed because the claim is a deterministic check of an explicit finite certificate (a bit-encoded subdivision tree) against a numeric threshold, not a search or statistical result; instead the checker must pass tamper/negative controls (below).

## Claim to be judged (partial win p1, literal arithmetic)
Criterion (bank p1, verbatim): "An independent rigorous replay of one of the 2026 lower-bound certificates (Mishra 0.8344, arXiv:2608.30538; Zeng 0.834, arXiv:2609.01284; or Xie 0.833, arXiv:2606.04458) in a separate checker with outward-rounded interval or exact arithmetic, published as a re-runnable replay note that confirms the bound or reports a defect."
Candidate claims (at most ONE is packaged; the highest-value that passes):
 (M) Mishra cert_B_08344 (disc, Reuleaux triangle, Reuleaux pentagon, tau = 0.8344) replayed on all leaves by a checker whose every real-number operation on the leaf path is a Interval operation with outward rounding (each + - * / sqrt result widened by one ulp downward and upward; this encloses every IEEE-754 round-to-nearest result), constants enclosed by intervals, membership and order tests decided only by interval bounds (undecidable = fail), area lower bound from the interval shoelace.
 (Z) Zeng's Zenodo certificate (arXiv:2609.01284, tau = 0.834) replayed completely by an independent interval checker with the same discipline.

## Statistic and thresholds (zero tolerance)
1. Decoding: header parse; forest identity (nodes = 2*leaves - seeds) holds exactly; no trailing or missing bits; node and leaf counts equal the paper's (M: 486,799,600 / 245,496,952). A mismatch is a defect report, not a checker failure.
2. Per leaf: interval lower bound of area conv(union of witness points) >= tau + 1e-12 (M) with all witness points certified inside their bodies by interval membership. ALL leaves must pass. One failing leaf = the claim is a defect report for that leaf only if shown genuine.
3. Coverage: regenerated leaf boxes cover the compactified placement domain; the interval implementation must prove child boxes cover the parent (interval comparison of children bounds with parent bounds, outward) at every split.
4. Analytic lemmas: written as complete proofs with machine-checked constants (lens lemma-proofs). Lemmas stay labelled KNOWN/SKETCH/PROVED-HERE honestly; the claim scope says exactly "conditional on the paper's lemmas as re-derived in LEMMAS.md".
5. Controls (all must be rejected by the interval checker): 12 tampered certificates from the previous run (flipped bits, truncated, tau raised to 0.8348, tmax 0.65, negative inflation, ...). Positive controls: the author's small valid certificate (certB_test) accepted; the interval and the rigorous-double checkers agree leaf by leaf (min slack difference reported) on a stratified sample of >= 1e6 leaves.
6. Cross-implementation: second-checker lens reproduces interval bounds for >= 2,000 leaves (random + near-worst) in a different language/design; every cross value must satisfy |independent lower bound - C# interval lower bound| <= 1e-6 and neither exceeds the exact polygon area.
7. No tolerance change after results: slack thresholds above are final. A changed plan becomes PREREG.v2.md.

## Baseline (step 3c)
Not an empirical benchmark score. Baseline-equivalent: the previous run's rigorous-double replay (same cert, same leaf count) is the comparator for the agreement test in 5.
