# Criterion skeptic verdict, L = 380

context: subagent (same VM)

confirmed_scope: The explicit +-1 sequence in sequence.txt (length 380) has exactly recomputed integer energy E = 10058, strictly below 10286, which is the only published L = 380 value found in the ten sources actually read (arXiv:2206.12070 row for 380, merit factor 7.01924946529, decoded sequence energy 10286; arXiv:2607.09688, 2504.00987 and 1406.5301, 1512.02475, 2011.00068, 2106.03377, 2210.15962, 2409.07222 and Knauer's 2004 table have no L = 380 row), so it beats the baseline as read but not a baseline that is proven complete, because the Boskovic et al. records repository pages, the journal-only versions and any arXiv result newer than 2607.09688 could not be read.

## Element-by-element check
- Explicit sequence: sequence.txt is 380 characters over {0,1}; mapping 0 -> +1, 1 -> -1 as stated.
- Length range: 67 <= 380 <= 600, satisfied.
- Exact integer energy: I recomputed independently (check_energy.py, Python ints) and got 380 10058. The parent (L=383, printed F 7.0748) recomputes to 10367, and parent[1:-2] equals sequence.txt exactly, so the "remove 1 at the start, 2 at the end" provenance is true.
- Baseline: I decoded the 2206.12070 hex string for L=380 (B_379 o eta1 o eta1 o eta3) myself; its energy is 10286, and 380^2/(2*7.01924946529) = 10286.0, so printed F, decoded sequence and baseline.tsv agree. Other rows in source_excerpts (377..388) decode to energies that match their printed F to the printed digits, so the decoding convention is sound.
- Comparison is integer, strict: 10058 < 10286 (difference 228). F = 7.178 vs 7.019 is only for illustration.
- One table cell: L=380. No tie, no rounding.

## Hidden quantifiers and stretched definitions
- The criterion says "minimum over the tables in 2607.09688, 2504.00987, the Boskovic et al. repository, and any newer arXiv result". Of those, 2607.09688 (lengths 450..527, 573) and 2504.00987 (92..120) were read and have no row for 380; the repository was NOT read (git_labs 403/404) and no arXiv search was possible (429). So "minimum over the named tables" is established only over what was read. This is a real gap, not a formality, and the claim must stay worded "as read".
- No stretched definition found: E is the standard sum of squared aperiodic autocorrelations, F = L^2/(2E) is not used for the comparison, and the sequence is not a periodic or rotated variant counted differently.
- No partial win is enumerated in CLAIM.md; only the full criterion is available and I judge against that.

## Null models and local checks (work-criterion/)
- Near-neighbour end-edit null: from the published records at L=377..388 in source_excerpts (decoded by me), I tried every removal of up to 3 elements per end combined with every fill of up to 3 added +-1 elements to reach L=380 (611 candidates). The minimum is 10058 and it is reached by 15 candidates, all the same sequence up to equal ends (from 383 and 384); no candidate is lower. So the claim is not a lucky draw that a slightly wider obvious edit would trivially beat, and the published baseline 10286 is clearly not tight for this simple family (it used one specific append sequence from 379).
- Local polish: the claimed sequence is a strict 2-flip local minimum (best single flip 10246, best double flip 10466). A person polishing it would not get below 10058 that way, which reduces the chance that some published polished object sits just under it.
- Cross-length check: the published 381 record decodes to 10078 (2206.12070), but its 1-element trims give 10306, and 378 (even, 10037) is a different length; neither yields a competing 380 table entry.

## Parity and coverage specific to L = 380
- 380 is even, so skew-symmetry (odd lengths only) does not apply to the object; the skew-symmetric searches (Brest/Boskovic 2018 and 2022, 2210.15962, MENDEL 2022) target odd lengths and would not list 380. Even-length values for L > 304 in the literature are derived by operators from odd parents, which is exactly how the 7.019 baseline arose, and the only comprehensive table over this range (2206.12070, 330 lengths 172..1006) was read. 2607.09688 (June 2026) cites only [boskovic17, dimitrov22] as the prior art for 172..527. Knauer's table stops at 304, 1406.5301 lists 16 mostly odd lengths in 181..401 without 380. This makes an unread better value at 380 unlikely but not excluded: the unread repository and a post-June-2026 arXiv paper are the residual risk, in my estimate a few percent.

## Is an end-operator result from another length's record genuine and non-subsumed?
- Under the criterion as written there is no originality clause: it asks for an explicit sequence with strictly smaller exact energy than the table minimum for that L. The object is not in any table read, it is not a rescaling or a re-listing of a published L=380 object, and it does not equal a sequence of any published row (the only 380 row is a different sequence, 10286). It is derived from a published L=383 record by three deletions, which is the same kind of operation the baseline itself uses, so it is a modest, honestly provenanced win, not a deep one. It is subsumed only if some published table already lists an L=380 object with E <= 10058, which none of the read sources does.
- The claim text discloses the derivation and the sources, which is the right way to present it.

## Decision
All literal elements verify and the strict inequality holds against everything that was readable. The unread repository and newer arXiv results keep the baseline provisional, so the confirmed scope is limited to the sources read and the pass is for that scope only.

pass: true
