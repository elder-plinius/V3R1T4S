# How we found it

*Contributor text, unverified.*

Agent runs on 2026-10-24 and 2026-10-25 (one AI agent session each, with fresh-context subagents for the checks)
worked on the spherical-codes table. The first found that most from-scratch and structured constructions stay above
the table, and that what works is polishing the codes the table itself posts, with sequential linear programming on
the exact objective: linearise every near-maximal inner product, minimise their common bound in a small trust region
(HiGHS), and accept only steps that lower the true maximum cosine. Many recent uploads turned out to be unconverged.

For (6, 256), the code posted by Pavlos Moros (2026) went through a 45-second sweep (gain 1.151e-5) and then a deep
polish that ran until its trust radius fell below 1e-15 (138 steps, gain 3.325e-5 in all). The result sat unclaimed
for a day while other cells were claimed. This run checked that the row was still unstarred, unlabelled and
unchanged, that no pull request in the V3R1T4S repository (open or closed) and no arXiv paper in the saved searches touched
(6, 256), and that no listed code with d' <= 6 and N' >= 256 reaches the new value, then froze the object unchanged:
maximum cosine 0.7048987224974410, 3.32469e-5 below the table value, with 1,331 pairs within 1e-14 of the maximum
and every point in such a pair (more contacts than the 1,265 degrees of freedom of 256 points on S^5 modulo
rotations). Points moved by 0.023 (median) and at most 0.055 from the posted code. Two basin-hopping restarts and a
remove-and-reinsert move from the object all ended at the same or a slightly worse maximum cosine.

The object is a local refinement of that posted code, so the seed is Pavlos Moros's work. The table row carries no
"needs more optimization" label, so by the target's rule this is a record claim and not the partial win for
labelled rows.

Before the panel, an internal break-it pass ran in a fresh context. It raised wording and record points: a dimension regex that missed "dimensions 5, 6, and 7", paper statements
resting on background knowledge that were not marked so, two kissing-number papers missing from a list, an earlier
fetch line not copied into the claim, and an imprecise sentence about the polish's last trust radius. These were
fixed and the table re-read as the very last step, at 2026-10-25T06:26:36Z. Then three skeptics, each in a fresh
context on Opus 5.5 and one after another, worked through the claim: REPRODUCE (its own checker, every pair exactly, no
network), NOVELTY (re-read the live table at 06:33:58Z, byte-identical to the claim read, plus its own arXiv
searches and the repository's pull requests) and CRITERION (every conjunct of the criterion, no network). Their
verdict files are in panel/.
