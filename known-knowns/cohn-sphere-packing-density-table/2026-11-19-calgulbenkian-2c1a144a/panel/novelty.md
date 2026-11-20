context: Claude Code subagent, fresh context [Sonnet 5.5]

# NOVELTY report, 2c1a144a (d19 non-isometric packing P19_II_vtx, claimed partial win p1)

## Fetch log
| UTC | URL | HTTP | sha256 |
|---|---|---|---|
| 2026-11-19T11:51:55Z | https://cohn.mit.edu/sphere-packing/ (once, no retries) | 200 | 55a59ce23bf1c0b3450ce2476d27fab76f927de54b2a990316519f37ec673601 |
| 2026-11-19T11:52:00Z | https://arxiv.org/e-print/2505.02394 (TeX source) | 200 | e114460c10a5770100eaafd647426bc5c7eb8e915aed9d2b3179cb36789a821e (same as the package's snapshot) |
| 2026-11-19T11:52:10Z | https://arxiv.org/abs/2607.20359 | 200 | 4d58c7411e9e92213835b951406e39d411313975ca732559b1d978f1769f5964 |
| 2026-11-19T11:52:10Z | arXiv API query "antipode" AND "sphere packing", newest first | 200 | 474c0e8bc57496bb209c5451bac38fc292c9c7b81bbd34148e2eb155dd954310 |
| 2026-11-19T11:53:19Z | https://arxiv.org/abs/2511.13391 | 200 | 5c4a80ea9dc291e57ce54cfed0dd2735e328a73d743781e14960767a1b8cf5e0 |
| 2026-11-19T11:53:19Z | https://arxiv.org/abs/2603.10425 | 200 | 712f6e1caac46bd5b9b3d1bf3c7e3eb594e296fc4f7edb5f1d2e94a8d206cb39 |

I also ran two web searches (standard mode) and read-only `gh pr list` searches.

## Status source, n = 19 entry
The row reads: n = 19, center density 3^-9 · 5^-21/2 · 13^19/2, # = 6, density 0.0041473691458627…, upper bound 0.0092288097047995, ratio 2.226, references [8, 25]. Reference [8] is Chen, Hu, Li, Wang and Wu, arXiv:2505.02394, which is the only lower-bound source. Reference [25] is the upper-bound source. The value equals the claimed density, so this is a tie with the record. No better value has appeared since the package's own fetch.

## Is the packing already published?
- **The record packing.** The paper's dimension-19 packing is a 6-translate antipode packing built from one rank-5, determinant-300 section K of the Leech lattice. It gives center density 13^9.5 · 3^-9 · 5^-10.5 = 0.08896, with beta = 8/15 and M = (1/60)·[[21,9,9,12,12], …]. The paper says it takes "suboptimal cross-sections" and gives exactly one embedding matrix A for n = 19. It does not enumerate or classify other determinant-300 sections.
- **My own check.** Using the package's Golay/Leech generator only, I built all 196560 minimal vectors of the Leech lattice. The paper's A rows correspond to the package's A_I_ref: they have Gram [[4,0,0,-1,-1],[0,4,0,-2,-1],[0,0,4,-1,-2],[-1,-2,-1,4,0],[-1,-1,-2,0,4]].
- **The package's new section.** A_II has the same Gram matrix, so K_II and K_I are isometric as abstract lattices, with different embeddings in the Leech lattice.
- **Complement norm-4 counts.** The count of norm-4 Leech vectors orthogonal to the section is 6942 for the published section and 6858 for the new one. The complement lattices therefore differ, so the two embeddings are not related by the Leech automorphism group Co_0.
- **Matching the package.** This matches the package's invariants norm4(L_ref) = 6942 and norm4(L_new) = 6858. I reproduced the counts independently of the package's JSON and of its verifiers.
- **Other literature.** I found nothing listing a second determinant-300 or rank-5 section for n = 19, and no 2024-2026 follow-up. The arXiv antipode search returns only 2505.02394, 2607.20359 (dimensions 38-43 only) and the older 1996/2002 Conway-Sloane papers. The kissing-number papers 2603.10425 and 2511.13391 do not touch this. A web search found no other source. The package also cites Kravatskiy (upper bounds) and finds nothing for n = 19 there; I did not re-fetch that repository.
- **Not a trivial edit.** The new object is a different Leech embedding of the same lattice K, with a different complement lattice. That is not a deletion, restriction, propagation rule, relabelling or Co_0 symmetry of the published packing. The package's extra ray slide only isolates the packing as a contact-graph vertex. It is a numerical-polish-style step, but it is applied to an already different section, so it does not carry the novelty claim.

## Repository PRs
`gh pr list` searches on elder-plinius/V3R1T4S found no PR for cohn-sphere-packing-density-table or this target. The terms tried were: the target id, "sphere packing density", "dimension 19", "d19", "non-isometric", "Leech", "antipode", "periodic packing", "center density" and "P19". The hits were unrelated claims (fmm, packomania-hyperspheres, cohn-harmonic-energy). Local TROPHY_CASE.md and the repository's known-knowns folder have no Cohn sphere-packing-table entry (only packomania entries).

## Limits and caveats
- This is a tie with the record by design: p1 explicitly allows matching the best known density with a non-isometric packing. It is not a record and is not claimed as one.
- The paper does not state that its section is the only one. A sibling embedding is a natural variation, but it is not published, listed or implied anywhere I could find.
- I did not independently check the packing-level claims: min_sq = 52/15, the six per-translate kissing numbers, the trivial translation stabiliser, or the contact-Jacobian ranks. Those belong to the reproduce role. The non-isometry of the full packings rests on the trivial coset translation stabiliser, so that stabiliser result must hold for the complement-lattice argument to carry over.

pass: true
