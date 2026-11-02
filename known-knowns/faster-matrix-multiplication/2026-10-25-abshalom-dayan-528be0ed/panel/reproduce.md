# Reproduce report, <30,30,31> rank 12395

context: subagent (Claude Sonnet 5.5, fresh context, given only a copy of claim/)

## Definition used (written before reading the author's code)

> A rank-r bilinear scheme for <n,m,p> (A is n x m, B is m x p, C = AB is n x p) is r triples (u_k, v_k, w_k) with
> m_k = (sum_{i,j} u_k[i,j] A[i,j]) (sum_{j,l} v_k[j,l] B[j,l]) and C[i',l'] = sum_k w_k[i',l'] m_k for all A, B.
> Comparing coefficients of A[i,j] B[j',l] in C[i',l'] gives the Brent equations
> T[(i,j),(j',l),(i',l')] := sum_k u_k[i,j] v_k[j',l] w_k[i',l'] = [i=i'][j=j'][l=l'] for all n*m * m*p * n*p index triples
> (this is the trilinear form trace(A B C^T) written with the C index in the same orientation as AB).

Index convention (fixed by the README / file headers, and checked against each file's `# convention` line): u index i*30+j, v index j*31+l, w index i*31+l, C[i][l] = sum_k w_k[i*31+l] m_k.

## What I checked, and how

- Files: object parts joined in numeric part order; sha256 of joined u, v, w each equals the value in CLAIM.md (3 of 3 match).
- r: CLAIM.md and STATEMENT.txt both say exactly 12395; each of the three files has exactly 12395 term lines, header `# rank 12395`, `# format 30 30 31`, convention line as above; indices in range, no duplicate index in a line.
- Zero factors: terms with a zero factor: 0 (empty or all-zero lines are counted, none found); explicit zero coefficients: 0.
- Nonzeros u 576535, v 870728, w 290715, and LCDs U 366912, V 312, W 312: both equal the values stated in CLAIM.md.
- Brent equations: ALL 778410000 index triples (900 x 930 x 930) checked, 0 wrong. Arithmetic: factors scaled to integers by their LCDs (D = Du*Dv*Dw = 35716681728), then for each C-entry c the slab T[:,:,c] = Uc^T diag(W[:,c]) Vc over the terms with W[k,c] != 0 is formed as a dense matrix product and compared with D*delta; modular: 3 primes < 2^20 (float64 BLAS, each partial sum < 2^53), CRT product 2^59 > 2*(max slab bound 354218129195553792)+1, so zero mod all primes implies exactly equal. No dense 3-tensor is built.
- Own checker run (python3 -I, nice -n 10): 24.5 s wall including parsing, peak RSS 1396 MB.
- Independent smoke check (separate code path, Python Fractions): scheme applied to a random integer A, B pair: `30x30x31 r 12395 random exact eval (ints in [-9,9], Fractions): entries differing 0 of 930`.
- Checker validation before use: Strassen <2,2,2> rank 7 and naive <2,2,3> rank 12 pass (both arithmetic modes); Strassen with one coefficient changed, Strassen with one sign flipped, and naive <2,2,3> minus one term are all rejected (both modes).
- Negative control on this real object: w[6197] had one coefficient changed by +1/7 in memory; my checker reported 2240 wrong equations and rejected it (33.4 s).
- Determinism: results are integer-exact; the author's checkers' printed output reproduced identically (see below); my checker gave the same result on re-runs of the smallest cell.

## Result vs claim

Claim: exact bilinear scheme over Q with exactly 12395 multiplications for <30,30,31>. My result: confirmed from the saved files, all 778410000 Brent equations hold exactly, exactly 12395 terms, no zero factor. The claimed numerical comparison (12395 < 12789, the rank CLAIM.md says is listed) is consistent as numbers; I did not re-fetch any table (no network), so the listed values themselves are not independently verified by me.

## Author's REPRODUCE.md, run in a copy of claim/

`sh verify-it-yourself/run_checks.sh` exited 0, last line PASS. 3 sha256 matches; check 1 (stdlib) 284 s, check 2 (numpy) 11 s, whole script 295 s wall, peak RSS 3.41 GB (/usr/bin/time -l, shared machine, nice). Both checkers printed `778410000 checked (all index triples), 0 wrong` and the output (with timing and progress lines removed) is identical, line for line, to the expected output block in REPRODUCE.md. I did not run the optional rebuild (REPRODUCE.md step 2, needs a network download) nor the negative-control script (I made my own).

## Mismatches

None. Caveats: the table-rank comparison and the provenance (LITA 21x21x21 rank 4723) are not re-checked here.

pass: true
