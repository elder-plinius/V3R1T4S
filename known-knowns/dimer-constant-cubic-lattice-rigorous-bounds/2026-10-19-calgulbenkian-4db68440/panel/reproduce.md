# reproduce: cubic-dimer-h3-ub-54 (p2, h3 <= 0.7859681 from the (5,4) monomer-dimer layer matrix)

context: Claude Code subagent, fresh context [Sonnet 5.5]

## Setup
- Hashes: `sha256sum -c the contributor's hash list` run inside the package folder gave OK for all 17 files. The two certificate parts concatenated have sha256 4db684405f609065a95ffe192fcdf672742b3910e7dfff37ed80b02ec0f74c0c (matches README.md). I worked in a private copy of the package; my own files (a column-contraction applier in C, a driver script, and the saved outputs of my runs) are not shipped in this package.
- Network not used. The earlier (3,3) filing was not needed; its certificate shipped inside this package (verify-it-yourself/cert_md_h3_33_sibling.txt) was used for the cross-check.

## Definition used (quoted from object/DERIVATION.md, section 3)
"T^MD[U,W] := sum over S subset of (V minus U) of per A[S, W]", with V = Z/m x Z/n, A[u,v] = 1 iff v-u in D = {(0,0),(1,0),(0,1)}, per A[S,W] = 0 unless |S| = |W|. Bound: h3 <= (1/(mn)) log max_U (T^MD x)_U / x_U (Collatz-Wielandt, x positive).

## My independent applier (written before opening any author code)
Not the author's per-vertex DP over S. Mine (my own C program, not shipped in this package): with g[C] = sum over W of x[W] * sum over S subset of C of per A[S,W], row U of T^MD x equals g[V minus U]. I compute g by a column-by-column tensor contraction over the m columns of the torus (vertex v = a*n+b). Each column has a local kernel K(C,P,Q), counting the ways its sources in C choose monomer / same-column target b / same-column target b+1 / next-column target b, with P the set of next-column targets used and Q the set of same-column targets used. Distinctness is enforced per column, and the column a target set is W_a = P_{a-1} disjoint-union Q_a. The cyclic wrap is handled by fixing P_{m-1} externally (16 runs) and contracting x one column at a time. Arithmetic is unsigned 128-bit; the final maximum is taken in Python with arbitrary-precision integers, comparing y_U * x_V > y_V * x_U (exact cross-multiplication) over all 1048576 states. Orbit expansion (my own driver script, not shipped): I rebuilt the 20 translations of Z/5 x Z/4, computed the minimum-image mask for every state, and checked that the file's ids are 0..52487, its masks are distinct and equal exactly the set of canonical masks (52488 orbits, covering all states), and that all x are positive and below 2^63.

Validation of my applier against the definition itself (a plain recursive enumeration of all S subset of V minus U and all injective target choices, in Python):
- (3,3): all 512 rows agree with g (0 mismatches).
- (5,4): 60 random rows with up to 9 free vertices (U with few free vertices; full rows are infeasible by enumeration), 0 mismatches.

## Results (output of my own driver script run for the (5,4) case, 17.7 s wall)
(3,3) sibling cross-check (the sibling certificate is invariant under the translations and the coordinate swap, 44 orbits; I used that group for the 3x3 case):
```
orbits 44 oracle mismatches on all 512 rows: 0
ratio 731051554747087/618837374495 argmax states [255, 383, 447, 479, 495, 503, 507, 509, 510] log/9 0.786044083039587
```
This matches the sibling's known ratio exactly.

(5,4):
```
whole sha256 4db684405f609065a95ffe192fcdf672742b3910e7dfff37ed80b02ec0f74c0c
orbits 52488 x>0 all True
direct-definition oracle rows 60 mismatches 0
best (y,x) (1891821269973664, 281869529)
ratio 1891821269973664/281869529 6711691.315784843
log(r)/20 = 0.7859680768085332074213493868858...
ceil to 7 places 0.7859681   claimed 0.7859681 >= h: True and 0.7859680 < h: True
exact check 0.7859681: r <= exp(20*0.7859681)? True
```
- The max ratio over all 1048576 states is exactly 1891821269973664/281869529. The argmax set is the 20 translates of "all vertices except one" (U with exactly one vertex missing; first is state 524031 = 0b1111111111011111111), a single translation orbit, so the maximum is attained consistently on the orbit.
- log(ratio)/20 = 0.785968076808533207..., with the same normalisation as the sibling (dividing by m*n = 20; the (3,3) value divides by 9). 7-place round-up is 0.7859681, which is strictly above the exact value and 0.7859680 is strictly below it, so 0.7859681 is rounded UP, correctly. The claimed bound is below the FKLM comparator 0.7862023450 by 2.34e-4.

## Author's run_checks.sh (run in my private copy of the package, `sh verify-it-yourself/run_checks.sh`, after my checker)
Its output ended with `ALL CHECKS PASS`. Key lines (the full tail is in the saved output of that run, not shipped): (3,3) ratio 731051554747087/618837374495, bound 0.7860441; (5,4) `RESULT mdcert dims=5,4 states=1048576 orbits=52488 argmax_state=524031 ratio=1891821269973664/281869529`, `log(ratio)/20 = 0.785968076808533207`, PASS exact ratio, PASS 0.7859681, trace identity EQUAL for (2,2,4), (3,2,4), (2,2,6), total 17.5 s. It agrees with my result in the ratio, the argmax state, and every digit. No mismatch.

## Answers to open questions concerning reproduction
- Q4 (orbit vector expanded by translations only): acceptable. The Collatz-Wielandt test requires only a positive vector on all 2^20 states and the full matrix applied to it; I applied the whole matrix to every state and took the maximum over every state, so validity does not depend on the translations being a symmetry. The translation orbit structure was verified (exact canonical orbit set). For (5,4) the swap is not available and was not used.
- Q5 (C applier as independent program): yes. My applier uses a different algorithm (column contraction with a local kernel, not the shipped per-vertex DP over S), was written from the definition without reading the shipped C, agrees with a plain definition-level enumeration on all (3,3) rows and 60 sampled (5,4) rows, reproduces the (3,3) sibling ratio exactly, and gives the identical (5,4) ratio on all states. The shipped C is therefore corroborated, and the matrix not being stored is not a problem.
- Q1 (does (5,4) need more than (3,3)), reproduction side only: the derivation steps use m,n >= 2 generally; the trace identity is checked by the author at an unequal pair (3,2) as well; nothing in E1-E5 uses m = n. Whether the extension itself is proved is a criterion question and I did not judge it; I only note that nothing in the reproduction is sensitive to m differing from n. (The orientation of rows U and columns W does not matter, since rho(T) = rho(T transpose), and the Collatz-Wielandt direction used here, (Tx)_U / x_U with x the right vector, is valid for any nonnegative matrix.)
- Q2, Q3: literature/derivation questions, not reproduction; not judged here.

## Mismatches
None.

pass: true
