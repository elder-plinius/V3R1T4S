# How we found it (contributor text, unverified)

By Kaust-a-laut, with Claude Code (Anthropic) running claude-opus-5-5.

1. Run 2026-10-15-1535 checked table-level recursive constructions R1 to R5 (including the average-degree bound
   `C(v-1,k-1,t-1) <= floor(k * C(v,k,t) / v)`) across all 9490 cells and found 0 improvements over the live table.
2. In run 2026-10-15-2309, the `constructor` lens (`how-we-built-it/derived.py`) noticed that the table-level formula
   only bounds the *average* point degree `k * b / v` of a `(v,k,t)` design, whereas an actual block file with uneven
   point degrees gives `C(v-1,k-1,t-1) <= min_p deg(p)`.
3. Scanning all 9482 published block files in the LJCR Zenodo v1.2 `covers.json` (`how-we-built-it/derived_output.txt`)
   found 2456 ties with the live table and one improvement: the 8735-block `C(42,13,6)` design has average
   point degree `2703.7`, but its point degrees span `2207` to `3091`. Deriving at the minimum-degree point `p = 16`
   (`how-we-built-it/derive_at_point.py`) gave a 2207-block `(41,12,5)` covering design, beating the live
   coveringrepository.com value of 2244 by 37 blocks and Zenodo v1.2's 2245 by 38 blocks. The object is this derived
   design exactly (no search); the live (42,13,6) record is 8718, a different design we did not examine.
4. What did not work in the same lens: point-blowup rule R6 (0 beats, 1408 ties), pair-derived rule R8 (0 beats), and
   propagating the new values through R1 to R5 (0 beats).
