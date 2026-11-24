# Claim
target id: primes-between-cubes-explicit-threshold (outside the bank)

**One sentence.** For every integer n >= exp(exp(29.735)) there is a prime between n^3 and (n+1)^3 (indeed in
(n^3 + 1/2, n^3 + 3n^2 + 1/2]), assuming as inputs Yang's zero-free region (UNSW PhD thesis 2025, Thm 1.3, c = 51.34) and
Bellotti's near-unity zero-density estimate (arXiv:2311.05136v1, Thm 1.1, unrefereed preprint), plus published results.

**Criterion (verbatim from target.md).** "A complete written proof that for every integer n >= exp(exp(Y)) the interval
(n^3, (n+1)^3) contains a prime, with Y < 32.537, each analytic input cited by its exact statement and the final
inequality certified by outward-rounded interval arithmetic (see PREREG.md for the frozen thresholds). Scope words must
name any input that is a thesis or a preprint. This is a threshold improvement, not the full conjecture (all n >= 1
remains open)."
Frozen thresholds (PREREG.md): beats the record iff Y_cert <= 32.527 at prec 128 and 256 and the standalone checker agrees;
"meaningful drop" iff Y_cert <= 32.337.

**Record being compared (status records, from the scout).**
- 32.537: Cully-Hugill PhD thesis Thm 4.3 (data/ch_thesis.pdf, sha256 0968f3491fd16fd574ea9f637ab8643fdd38ea8e73d247819e03ffe7dd6187f7,
  fetched 2026-11-24T07:34:21Z from https://unsworks.unsw.edu.au/server/api/core/bitstreams/20314249-033c-45e2-8c11-55a478d86289/content);
  quoted as the best by Johnston-Sorenson-Thomas-Webster arXiv:2601.15564v2 (data/arxiv_2601.15564.pdf, sha256
  4098d35f59b289cec1be90fb2e70bd262db87686353b472514f3dd6dc5e5359b, fetched 2026-11-24T07:42:07Z).
- 32.76: Mossinghoff, Trudgian & Yang, "Explicit zero-free regions for the Riemann zeta-function", Res. Number Theory 10
  (2024), article 11, https://doi.org/10.1007/s40993-023-00498-y (arXiv:2212.06867, §1: "By substituting Theorem 1.1 into
  [4, §4] ... we obtain the modest improvement n >= exp(exp(32.76))"). Recorded in OEIS A060199 (https://oeis.org/search?fmt=json&q=id:A060199,
  revision 87, sha256 d132575bbd4f0fd0d1bf0eb86ef09a0239b5c60ac8817d7becab7dc7fca6cc5e; see data/fetch_log.txt for fetch times and User-Agents).
- 32.892: Cully-Hugill, J. Number Theory 247 (2023) (data/arxiv_2107.14468.pdf).

**Best rigorous prior value.** 32.537 (Cully-Hugill thesis Thm 4.3) is the smallest previously stated value and the one we compare
against. Caution (raised by a panel skeptic, not established): our replay of the thesis' inequality reproduces 32.536 only with Ford's
constant c = 51.82, which the thesis (its (1.13)) states for T0 = exp(exp(33)); at that threshold log log T is about 32.54 < 33. If the
thesis used that constant, 32.537 may rest on a zero-free region outside its stated range, and the value supported by its other inputs
would be 32.892 (or 32.76 with MTY's region). We have not seen the author's computation; this does not affect our claim, which is
compared against the smaller 32.537.

**Prior non-rigorous anticipation (credit).** u/span_of_dilates, "An explicit Huxley-type zero-density estimate for 0.755 <= sigma <= 0.785,
and why it does not help the explicit applications we examined", rStation paper 130, v2 posted 08 Nov 2026,
https://rstation.ai/problems/riemann_hypothesis/papers/130 (data/rstation_130.html), §2.3: "Remark (model, not a theorem). The same
model with [Bellotti arXiv:2311.05136, Thm 1.3] in place of the Kadiri-Lumley-Ng bound used in [Cully-Hugill] gives log log n0 ≈ 30.07
... We have not checked whether a rigorous version of (17)-(21) keeps this." That remark already proposes the key idea used here
(Bellotti's near-unity density in Cully-Hugill's argument). It is a one-parameter model, uses Bellotti's Thm 1.3 (proof only sketched)
and Ford's zero-free constant, and states no rigorous threshold. What is new here is the rigorous chain (PROOF.md Lemmas 4(c) and 6),
the interval certificate, the use of Bellotti's fully stated Thm 1.1 and Yang's c = 51.34, and the value 29.735 < 30.07.

**Result.** Y_cert = 29.735 (prec 128 = prec 256 = standalone mpmath.iv). Drop: 2.802 below 32.537 (n0 shrinks from
exp(e^{32.537}) ~ 10^{5.9e13} to exp(e^{29.735}) ~ 10^{3.6e12}). Variants (PROOF.md §5): 29.907 with Bellotti's zero-free region
c = 54.004 (arXiv:2306.10680v1 Thm 1.2, data/; published as J. Math. Anal. Appl. 536 (2024) 128249) in place of the thesis; 32.677
with that region and no preprint/thesis input at all (beats the journal 32.76, not 32.537).

**Files.** PREREG.md (frozen pre-registration, byte-identical copy of the run's), CHANGES.md (post-panel errata), PROOF.md (the proof, inputs I1-I7 quoted), code/ (cert_arb.py arb certificate; standalone_check.py independent
interval checker; scan.py; null_tests.py; replay_ch.py; mutation.py; run_all.sh), out/ (captured outputs), data/ (sources
as fetched, fetch_log.txt), REPRODUCE.md.
