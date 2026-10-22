# How We Found It (contributor text, unverified)

## Brief & Observation
In A. I. Perminov's `FastMatrixMultiplication` catalogue, `6x12x14` had a 21-multiplication gap between its restricted ternary rank (`ZT = 666`) and its rational rank (`Q = 645`), and a 12-multiplication gap between `ZT = 666` and unrestricted integer rank (`Z = 654`).

## What Failed
Direct random flip walks starting from `6x12x14_m666_ZT.json` in `GF(2)` followed by generic Hensel lifting stalled because unrestricted plus-transitions (`r -> r+1 -> r`) on a `72 x 168 x 84` tensor frequently introduce `+/-2` coefficients when contracting back to lower rank.

## What Worked
We analyzed the block-tensor structure of `6x12x14` and decomposed it via `6x12x14` as a block product of `2x4x2` and `3x3x7`, combining a ternary rank-14 `2x4x2` base tensor with a signed-flip-reduced ternary `3x3x7` factor scheme (`m = 47`) and eliminating redundant block rank terms via signed ternary equivalence flips (`|c| <= 1` invariant). This directly produced an exact pure-ternary (`{-1, 0, 1}`) scheme of rank **654** over `Z` with `0` errors across all `1,016,064` Brent equations.
