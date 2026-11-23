# How We Found It

_Note: contributor text, unverified._

## Brief

We targeted `codetables-eaqecc-qubit-gaps` on cells `(n, k, c)` (`c >= 1`) in Markus Grassl's binary EAQECC table (`http://www.codetables.de/EAQECC/qubit.php`, last updated `10.07.2025`) that are simultaneously absent from recent 2026 preprints (`arXiv:2610.41183`, `arXiv:2607.02170`, `arXiv:2609.31300`, `arXiv:2606.02137`) and protected by the `GF(4)` Griesmer bound against lengthening of quaternary Hermitian LCD (`l' = 0`) and small-hull (`l' in {1, 2}`) classical codes.

## What Failed First

1. Unstructured binary simulated annealing over `Sp(2n, GF(2))` transvections and `S`-coset shifts on tight small-`n` cells (`n in {8, 9, 10, 11}`, gap `1..2`) stalled `2..4` low-weight dual codewords away from `d_lower + 1`, consistent with upper-bound slack on small lengths.
2. During an early coset-polish prototype, modifying a logical generator without immediately refreshing the dual basis `S` allowed stale steps to perturb the isotropic radical; adding a standalone `S`-only verifier immediately caught and fixed that bug.

## What Worked

1. Using the normal-basis trace-symplectic isometry `phi(x*w + z*w^2) = (x | z)` between `(GF(4)^n, <., .>_h, wt_H)` and `(GF(2)^{2n}, <., .>_s, wt_s)`, we parameterized `[19, 6]_4` codes `C = H_0 (+) W` with an exact `l = 4` dimensional Hermitian self-orthogonal hull `H_0` (`|S cap S^{perp_s}| = 4^4 = 256`) and a `k = 2` dimensional Hermitian-nondegenerate complement `W`.
2. Crucially, the objective in `how-we-built-it/search_gf4_hull.c` penalizes only coset vectors in `C \ H_0` (`S^{perp_s} \ S`), leaving vectors inside the isotropic radical `H_0` unconstrained so that degenerate EAQECCs (`d_EA > d(C)`) are reachable.
3. Combining sparse `U(19, GF(4))` unitary reflections/transvections with parity-checked `C^{perp_h}` coset shifts found an explicit degenerate `[[19, 2, 11; 9]]_2` code in `< 2` seconds (`d_EA = 11`, while `H_0` contains `6` weight-4, `21` weight-8, and `12` weight-10 stabilizer vectors, so classical non-degenerate Hermitian-hull searches see `d(C) = 4` and discard it).
