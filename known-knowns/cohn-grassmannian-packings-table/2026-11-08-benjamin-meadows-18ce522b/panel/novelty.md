# NOVELTY verdict: cohn-grassmannian-packings-table, cell 11-4-66

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-08T02:37:22Z

## Value computed here
- Live table https://cohn.mit.edu/grassmannian fetched 2026-11-08T02:34:22Z: HTTP 200, 629,039 bytes, sha256 7ba705c673db669ed4e3ec33fd45cd26f9648019a648fb21eb45761e113a0a66. No Last-Modified header and no "last updated" date on the page.
- Row (11, 4, 66): squared chordal distance 2.5777278197, bound 2.5846153847, no star (the neighbouring rows (11, 4, 67) and (11, 4, 68) are starred, this one is not). Note: "[31]" only, which credits N. J. A. Sloane, *Table of best Grassmannian packings*, 1997 (https://neilsloane.com/grass/grassTab.html). The note does not say "optimal packing", "proof of optimality" or "tight bound". Rows (11, 4, 63/64/65) credit [24] (Benjamin Meadows, packing-records v1.0.0, Zenodo 10.5281/zenodo.23906181).
- object/11-4-66.txt (sha256 18ce522b…058532, matches CLAIM.md): 264 vectors in R^11 = 66 blocks of 4. Every entry has at least 27 significant digits. My own script orthonormalises each block by Gram-Schmidt with reorthogonalisation in mpmath at 50 digits and checks all 2,145 pairs of n − ||U_i^T U_j||_F^2.
- Minimum squared chordal distance = 2.57776955247730714341341965172, at block pair (31, 42) (0-indexed). Only one pair lies within 1e-12 of the minimum. A float64 numpy QR cross-check gives 2.577769552477307.
- Margin over the live value: +4.17327773e-5, which clears the 1e-9 threshold by about 4×10^4. Distance below the bound: 6.84583222e-3, so the value is under the bound, as it must be.
- Prior claims at V3R1T4S, fetched 2026-11-08T02:35Z:
  - `gh pr list --state all --search "grassmannian"` returns 2 PRs, #846 and #761. Both are polytof PRs and mention Gr(3, F_2^6) only in passing. Neither concerns this target.
  - The searches "11-4-66", "(11, 4, 66)" and "11,4,66" return nothing. The search "11 4 66" returns three unrelated claims (#66, #11, #4).
  - A scan of the titles and bodies of all 960 listed PRs (highest number #1008) finds nothing for "grassmann", "cohn-grass", "subspace pack" or 11/4/66.
  - `gh search issues "cohn-grassmannian"` returns nothing. The target file exists at known-unknowns/packings-physics/cohn-grassmannian-packings-table.md.
  - TROPHY_CASE.md on main (31,306 bytes, sha256 83af764f…356113) has no match for grassmann, cohn or 11-4-66.
  - No prior claim found.
- Earlier publication of the same object: https://github.com/TheBenMeadows/packing-records commit d0841ec0f9 (2026-11-08T00:38:48Z, "v1.3: Cohn tables …") adds grassmannian/11-4-66.txt. That file is byte-identical to object/11-4-66.txt (same sha256). Zenodo 10.5281/zenodo.23906181 now resolves to version 1.3.0, published 2026-11-08. This is the same object from the same author line that the table already credits as [24], not a competing value. It is still a public release made before this claim.
- Literature: I ran arXiv API queries sorted by submittedDate, newest 15 each, for "Grassmannian packing", "Grassmannian packings", "subspace packing", "fusion frame" and "line packing", fetched 2026-11-08T02:35:43Z, all HTTP 200. The 2025–2026 hits are 2606.26464, 2604.19904, 2501.06178, 2610.05302, 2608.13972, 2607.26684, 2606.11454, 2511.20642, 2610.29041, 2609.08531, 2601.17294 and others. Their abstracts are about modulation, beamforming, filter-bank EITFF/ECTFF characterisation, LP relaxations, equi-isoclinic counting bounds and spherical designs. None reports a numerical packing for (m, n, N) = (11, 4, 66) or any real 4-plane packing table.
- Sloane's 1997 table https://neilsloane.com/grass/grassTab.html: HTTP 200, 149,883 bytes, sha256 d2e8e777…2675b5. Its computer section covers n ≤ 3 only (for m = 11, only n = 1, 2, 3), and its hand-construction section has no 11 4 66 row. So that page has no explicit entry for this cell. Cohn's [31] credit presumably refers to Sloane's file archive, and the live value 2.5777278197 is the value to beat.

## Clauses checked
- Live table re-fetched now; row (11, 4, 66) exists with value 2.5777278197 and bound 2.5846153847 — PASS
- Row is unstarred — PASS
- Note does not say "optimal packing" or "proof of optimality" (it reads "[31]", crediting Sloane 1997) — PASS
- Computed minimum (2.577769552477307…) exceeds the live value by at least 1e-9 (margin 4.17e-5) — PASS
- Computed minimum does not exceed the bound by more than 1e-10 (it is 6.85e-3 below) — PASS
- At least 20 significant digits per entry (minimum 27) — PASS
- No prior V3R1T4S PR and no TROPHY_CASE.md entry claims this cell — PASS
- No arXiv result in the searched windows gives a larger value for (11, 4, 66) — PASS
- Sloane 1997 table has no larger value for this cell (no explicit row) — PASS
- No steering instructions found in claim/CLAIM.md or the object header (the header is a metadata comment only) — PASS

## Decision
The object beats the live, unstarred, uncredited-as-optimal Cohn row for (11, 4, 66) by 4.17e-5, stays well below the bound, and I found no prior V3R1T4S claim and no larger published value. The residual novelty risks are these:
1) The table has no visible last-change date, so the "published after the last change" window can only be bounded loosely (the latest references are 2026).
2) arXiv full-text tables, non-arXiv venues, and anything Cohn may have received privately but not yet posted are not covered.
3) The identical object has already been made public by its author (packing-records v1.3, about 2 hours before this check). That is not a competing larger value, but the parent should know the release predates the claim.

pass: true
