# How we found it (contributor text, unverified)

**Brief.** Charter quarry 11 takes Justin Sun Prize catalog problems; JSP-000550 is Erdős Problem 677: must
M(m, k) = lcm(m+1, …, m+k) differ from M(n, k) whenever m ≥ n + k? An earlier run of this workspace (2026-10-15-0724)
had built the tools: Lemma A (in a counterexample, f(m)/f(n) is one of finitely many ratios r of small primes, so the
later block sits in a narrow linear window and contains no prime), a hash-based window search complete in m, and a
continued-fraction enumeration of each curve F(Y) = r·F(X). Its enumeration result ("k ≤ 22, n ≤ 10^494") was never
panelled, and its margin was checked only in 80-digit floating point, so it was NUMERICAL. This run (2026-10-24-0818)
pre-registered one claim, C-R2 ("every k ≤ K*, n ≤ 10^494, every m", made only if K* ≥ 23), with a judge requiring
the margin in rigorous arithmetic (`how-we-built-it/PREREG.md`, frozen 2026-10-24T08:24:04Z before any attack program
ran).

**What worked.** Three lenses ran in parallel.
- *extender-r2* reran the small-X search for n + k ≤ 1.1·10^6 (2 candidates, the known near-misses (3, 4, 13) and
  (4, 18, 53), 0 exact-equal) and pushed the enumeration from k = 23 to k = 25 at QMAX = 10^495: 1,174,616 window
  candidates over k = 3..25, none an exact solution.
- *rigor-margin* re-derived Lemma A, audited the ratio set (an independent generator agrees with `admissible_r` for
  every k = 3..25, 63041 ratios; all 970 equal-lcm pairs with n < m ≤ 3000 have their ratio in the set), and proved
  the margin twice, with interval arithmetic and with exact rational intervals: 63041 pairs, 0 failures, 0 undecided.
  Negative controls (η = 0, X0 = 10, a margin centred off c) made both checkers fail or stay undecided, as they should.
- *extender-r1* extended the all-k window search to n + k ≤ 2·10^8 (still only the 2 tiny near-misses). That is a
  lens result and not part of this claim.

**What failed, and the patch.** While the enumeration ran, the main session found a completeness hole in
`deep_rig.py`: its float64 pre-filter computed a quantity that loses its relative accuracy when a continued-fraction
ratio q_m/q_{m+1} is tiny, so a valid pair could have been dropped before the high-precision check. A fully exact fix
was about 6× slower; the final patch computes that quantity from the exact integer only where cancellation could
matter (`how-we-built-it/PATCH_NOTE.md`). All enumeration outputs here come from the patched code; for k = 3..18 the
per-k counts equal those of the unpatched code, so no pair had in fact been lost there. The full problem stays out of
reach: every k ≥ 3 has genuine overlapping solutions (lcm(3,4,5) = lcm(4,5,6)), so only disjointness rules them out,
and each k needs a global Diophantine argument; the enumeration covers n ≤ 10^494 only.

**Panel.** Three fresh-context skeptics read only the claim folder. REPRODUCE reran every step, including the
enumeration for all k = 3..25 (all 23 per-k lines identical to the saved outputs), the interval margin for k = 3..25
and the exact margin for k = 3..24, wrote its own small-X program, ratio generator and an exact-integer enumerator
for k = 3..10, and ran validate mode against brute force for q ≤ 4000, k = 3..18. CRITERION checked the hidden
quantifiers (m uncapped, n = 0, k = 1, 2, both parities, m = n + k, the X = 10^6 split), gave an error analysis of the
float stage and cross-checked 123 sampled curves with an independent exact enumerator (0 mismatches), and wrote the
scope sentence. NOVELTY read the catalog, the problem page and forum, arXiv and both repositories' pull requests,
found k = 3 settled by Chan (arXiv:2408.01306) and only finite searches for larger k, and passed on condition that
the record notes the k ≤ 3 prior coverage. The gate (`panel/gate.md`) wrote CONFIRMED_PARTIAL, recording that the
new content is 4 ≤ k ≤ 25.
