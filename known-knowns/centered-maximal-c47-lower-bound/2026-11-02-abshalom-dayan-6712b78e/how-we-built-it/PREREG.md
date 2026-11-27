# Pre-registration (written 2026-11-02T15:21:25Z, before any measurement of this run)

Earlier run's numbers are known to the author: L2 1.708711820985, L3 1.711011823672 from runs/2026-11-01-2110. They are treated as suspect until shown otherwise. Nothing of this run has been measured yet.

Criterion (bank, verbatim): Success means an explicit measure mu (finitely many point masses, or a periodic arrangement with a finite period cell) with exact algebraic or rational parameters, plus a proof-carrying computation showing alpha |{x : M mu(x) >= alpha}| / ||mu|| > L, where L is STRICTLY GREATER (direction: max) than the largest lower bound on the live page https://teorth.github.io/optimizationproblems/constants/47a.html and in any open pull request touching constants/47a.md at https://github.com/teorth/optimizationproblems/pulls, both re-fetched live immediately before claiming. The area of the super-level set must be computed exactly (polygonal regions bounded by lines where square averages equal alpha, which for point masses are piecewise axis-parallel/diagonal) or enclosed by interval arithmetic with a strictly positive margin, in two independent implementations. For periodic measures the reduction to a period cell must be stated and checked.

Candidate object, frozen: runs/2026-11-01-2110/attempts/continuum/out/clean/L3.json, copied unchanged. A later member is allowed only if L3 fails on a reparable technicality, under a new PREREG.v2.md. No search for a higher value.

Statistic: value V = alpha * area(S mod periods) / cell mass, at alpha = 1, for the periodic measure, where S is a subset of {x : M mu(x) >= 1} that is proved certified. Exact rational or rigorous interval enclosure only. Floats and sampling are tests, never evidence.

Bars, read live before claiming: largest lower bound on https://teorth.github.io/optimizationproblems/constants/47a.html and in open PRs touching constants/47a.md (bank's L). Also public off-page: Tomar's 1.7027237335 (Zenodo 10.5281/zenodo.23716077, newest version to be re-read) and anything arXiv shows. The claim must strictly beat the highest of them.

Kill rules, frozen (any one means the claim falls or stays below CONFIRMED, and the report says exactly why):
K1. Definition. The computed quantity must be the bank's: closed axis-parallel centred squares, average mu(Q)/|Q|, alpha |{M mu >= alpha}| / ||mu||. Written reduction from the periodic measure to one cell, and from Dirac masses to L^1 functions, must be a complete proof. A gap here stops the claim.
K2. Reach. Either reach 6 provably only undercounts (lower bound stays valid) or the claim falls.
K3. Calibration. On Lin's and Tomar's measures the same checkers must return their published values: Lin 1.6855099933 and Tomar 1.7027237335, each within 1e-8 after accounting for the rounding of the measure to dyadics, the difference being explained. A miss with no explanation stops the claim.
K4. Third checker. A checker written in a fresh context from the definition alone must agree with check_a and check_b on V for L3 to within its stated enclosure, and on the calibration measures. Disagreement above the enclosure stops the claim.
K5. Pointwise test from the definition. At 1,000,000 uniform random points of the cell, M mu(x) from the definition (all critical radii over periodic images out to a stated reach): any point claimed inside S with M mu(x) < 1 in exact arithmetic kills the checker's area. The sampled covered fraction must lie within 5 standard errors of area(S)/cell.
K6. Finite truncation. For a finite N x N block of cells with no periodicity, at sampled points, the measured ratio must approach V from below as N grows, consistent with the reduction.
K7. Family. L1, L2, L3 and at least one finer discretisation stated by one formula. Value against discretisation measured; limit labelled NUMERICAL unless proved. Not chasing a higher value.
K8. Panel. REPRODUCE, NOVELTY and CRITERION as kit/RUN.md step 6, each pass: true, then the gate. Any fail means no package. NOVELTY's earlier objection (continuation of Tomar's measure, ascent not converged) is judged by NOVELTY again, not by the author.

Margin: the claim stands only if exact V exceeds the highest bar by at least 1e-6, and checkers agree to 1e-9 on the same object.

null_test: not needed because the claim is one explicit object checked by deterministic exact checkers against a table value; the pointwise sampling in K5 and K6 tests the checkers, it does not support any beats-chance claim.

No outward step. No changes to other packages in outbox/. Peak memory under 3 GB, at most 2 CPU-heavy workers.
