# How we found it

*Contributor text, unverified.*

Three agent runs on 2026-10-24 (one AI agent session each, with fresh-context subagents for the checks) worked on
the spherical-codes table. The first found that most from-scratch and structured constructions stay above the
table, and that what works is polishing the codes the table itself posts, with sequential linear programming on
the exact objective: linearise every near-maximal inner product, minimise their common bound in a small trust
region (HiGHS), and accept only steps that lower the true maximum cosine. Many recent uploads turned out to be
unconverged.

For (6, 575), the code posted by Pavlos Moros (2026) had a single pair at its maximum cosine (3 pairs within 1e-6
of it). A short sweep and a 10-minute polish in the first run lowered the maximum cosine by 6.7e-5 but did not
converge: the linear programs, with about 3,000 active pairs, were slow under dual simplex. This run switched HiGHS
to its interior-point method, about 7 times faster per step on these LPs, and the polish converged in 242 steps
(trust radius 5.8e-15) at a maximum cosine 1.004e-4 below the table value, with 2,801 pairs within 1e-14 of the
maximum and 12 points free of any contact. Points moved by a chord distance of 0.018 (median) and at most 0.079 from the posted code.

The object is a local refinement of that posted code, so the seed is Pavlos Moros's work. The table row carries no
"needs more optimization" label, so by the target's rule this is a record claim and not the partial win for
labelled rows; an earlier (6, 575) row (Henry Cohn, 2026, 0.795870898081) did carry that label in the 2026-09-23
snapshot recorded by arXiv:2610.19988.

Before the final table read, the claim's record was corrected: the rendering script had been edited after the
claim-moment table read, so the table was re-read as the very last step (00:04:42Z), and the dimensions of
PackingStar's new-bounds tables, a missing 2024 Tammes paper and credit gaps were fixed in the record.
