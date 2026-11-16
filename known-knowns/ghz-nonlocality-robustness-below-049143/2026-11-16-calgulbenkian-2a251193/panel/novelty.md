context: Claude Code subagent, fresh context [Sonnet 5.5]

NOVELTY SKEPTIC REPORT. Claim: certified 3-qubit GHZ white-noise critical visibility v* <= 0.4913971114 (18 x 24 x 72 planar functional, exact L = 130692616) versus the target bar 0.49143.

Status source (fetched once, no retries; see a working file (not shipped))
- 2026-11-16T02:46:40Z https://arxiv.org/abs/2310.20677 : HTTP 200, sha256 57cf2fd4...6174c35. This is byte-identical to the package's own snapshot (the-record-we-beat/README.md). The page shows v1, v2 and v3 (submitted 31 Oct 2023).
- 2026-11-16T02:47:23Z https://arxiv.org/html/2310.20677v3 : HTTP 200, sha256 dfdc7344...0c62 (matches the package's snapshot). Table III, N=3: certified m=22, v = 0.49143. Uncertified m = 224: 0.49132. Putative XY-plane lower bound v_XY >= 0.49129.
- 2026-11-16T02:46:41Z https://arxiv.org/abs/1108.1998 : HTTP 200 (Vertesi and Pal, 0.496057 with 5x5x5 settings).

Best published numbers for the cell (fully local models, white noise)
- Best certified upper bound: 0.49143 (m=22, exactly 0.49142745...). The claim, at 0.4913971, is lower by about 3.0e-5, which clears the 1e-5 margin.
- Table VI of the same paper (uncertified, local bound not proven; "out of reach") lists, for N=3: m=26 0.49143, m=28 0.49141, m=32 0.49138, m=64 0.49134, m=96 0.49133, m=128 0.49133, m=224 0.49132. The m=32, 64, 96, 128 and 224 entries are numerically at or below the claimed 0.491397. They are not valid upper bounds, because the local bound is not proven maximal. The target statement and its pitfalls explicitly say they are not the record to beat. Strictly under the kit wording "any published threshold at or below the claimed value" they are an uncomfortable overlap. I treat them as non-thresholds, but the panel should weigh this.
- Best published lower bound (rigorous local model): v_XY >= 0.49129 for planar (XY-plane) strategies only (eq. 36 of the paper). No published lower bound for full-Bloch-sphere strategies was found. So the claim sits about 1.1e-4 above the planar limit; a planar improvement has at most about 1.1e-4 of room left.

Searches (names)
- arXiv API (export.arxiv.org), queries: GHZ + nonlocality + visibility (date sorted); GHZ + "Bell inequalit*" + "white noise"; BellPolytopes; "critical visibility" + GHZ; "local hidden variable" + multipartite + Frank-Wolfe. No relevant 2024-2026 follow-up showing a three-qubit GHZ threshold below 0.49143 turned up. (The API returned few and mostly irrelevant hits, so absence is weak evidence.) The package also reports a live arXiv API query for "nonlocality robustness" AND GHZ returning only v3 (not re-run by me).
- Web search: "GHZ state white noise nonlocality critical visibility three qubits local model Bell inequality 2025 2026 arXiv" returned only older papers (1005.0481, 1108.1998, quant-ph/0302165 and similar); nothing newer.
- Not done: no BellPolytopes.jl release-asset check and no Google Scholar citation list of 2310.20677; the package cites repo last push 2026-10-21 with no newer N=3 record (not re-verified by me).
- Repository: gh read-only. 300 PRs scanned by title for ghz/bell/nonlocal: none about GHZ (only an unrelated Bellman PR #801). TROPHY_CASE.md has zero mentions of GHZ. The repository's known-knowns tree has no ghz/bell/nonlocal paths. The only GHZ item is the target's own page in the repository's known-unknowns folder (the target itself). Only the first 300 PRs by default listing were scanned, and titles only.

Comparison with published objects and trivial edits
- Published objects are symmetric m x m x m regular-polygon XY-plane settings (m up to 224). The claim uses unequal party sizes 18/24/72 (polygon-subsets-of-a-72-gon structure), which is not a deletion or restriction of any published certified object (the published certified m is 22; the 72-gon appears only in uncertified-type runs, with 64/96 listed but not 72). It is not a relabelling or symmetry image of one. It could be seen as a seeded variant of the paper's method with a certified bound, which is the contribution of the claim. I could not verify that no restriction of an uncertified published object (m=32 etc.) gives the same value; those objects have no published coefficients in the paper's table, and their values are heuristic.
- I did not independently recompute L or the quantum value (outside the novelty brief); I only note the package's receipts.

Verdict
On the criterion the target defines (certified upper bound, beat 0.49143 by at least 1e-5), I found no published certified threshold, and no published functional, at or below 0.4913971. The one risk is that the uncertified Table VI entries (m >= 32) are numerically lower; they are explicitly excluded by the target and are not valid thresholds.

novelty: PASS (narrow; conditional on certified-only reading of the bar)

pass: true
