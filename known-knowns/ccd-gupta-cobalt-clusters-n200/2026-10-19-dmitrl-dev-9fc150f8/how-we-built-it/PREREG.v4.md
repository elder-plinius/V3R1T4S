# PREREG.v4 (changed plan during part B; earlier PREREG files unchanged)

Reason: lens 3 (decahedral family) found no gain at 54 chain members. Etch chains end close to E_best next to the
seeds (196->195 -0.0059 eV, 200->199 -0.0189, 113->112 -0.0269, 101->100 -0.0300, 121->120 -0.0423), while every
growth step is far worse (-0.47..-0.77 eV at the first step). The growth move only used three-fold hollow sites above
triangles; it never offers the four-fold hollows of (100) facets, where Marks decahedra grow. This is a defect of the
move set, so lens 3b repeats ONLY the growth chains with a corrected site set.
Lens 3b: for each surface atom (coordination < 10), 40 directions (Fibonacci sphere) at distance 0.95; keep a point
if its nearest atom is at >= 0.85 and it has >= 3 atoms within 1.15 (3-fold and 4-fold hollows, some bridges);
deduplicate at 0.25; quick relax every candidate, polish the best three. Chains as in PREREG.v3 (growth only):
95 -> 96..100, 101 -> 102..107, 113 -> 114..119, 122 -> 123..128, 198 -> 199; plus 196 -> 197 and 121 -> 122 as
positive controls of the move (the Co.zip energies of 197 and 122 should be reached or approached).
Same potential and budget rule (part B total <= 2 h wall from 04:02Z).
null_test: not needed because the claim is an explicit object (coordinates) checked by a deterministic checker against a table value
FROZEN 2026-10-19T04:34:38Z
