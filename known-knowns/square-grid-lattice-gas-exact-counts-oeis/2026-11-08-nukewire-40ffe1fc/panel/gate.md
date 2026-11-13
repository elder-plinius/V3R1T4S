status: CONFIRMED_PARTIAL
confirmed_scope: The 17 integers T(29,k) for k=12..28 of OEIS A210662 (monomer-dimer tiling counts of the 29 x k board) — the cells of row 29 beyond the entry's published columns k=1..11 — are correct as claimed (two-run CRT verified with all 378 published cells and the 27-cell row-28 anchor reproduced, from-definition exact DP confirmation for k=12..15, growth on the published trajectory below Finch's constant), meeting bank partial win p2 for target square-grid-lattice-gas-exact-counts-oeis.

Gate session notes (2026-11-08T21:35Z, the run's main session): all three
round-3 panel files read in full; all end "pass: true"; no hedging; the
novelty fetch (21:10Z) is fresh (< 6 h). Disclosed caveats accepted as
honest, none a downgrade trigger: reproduce's k=16..28 cells rest on the
two-run CRT over proven-prime moduli above the 3^(29k) bound (the frozen
criterion's own design, with k=12..15 additionally exact-DP-confirmed and
19,140 residues cross-checked); novelty documents an OEIS integer-search
blind spot and compensates structurally (the width>=12 column sequences do
not exist; PR diffs checked; controls prove the search methods work).
HISTORY: rounds 1-2 (preserved in panel_28cell_round1/ and
panel_23cell_round2/) failed novelty on cells k=1..11 (published in the
entry's cross-referenced column sequences A000045/A030186/A033506-514 or
mechanically derivable from the published A033508/A033509 generating
functions); the claim was narrowed twice (PREREG.v2, PREREG.v3) with no
threshold or gate weakened; the same finding taints PR #960 (row 28,
k=1..11) — disclosure comment offered to the human, awaiting their word.
