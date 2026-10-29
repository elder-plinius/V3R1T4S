# Reproduce report, <20,21,21> rank 4471

context: subagent (Claude Sonnet 5.5, fresh context, given only a copy of claim/)

## Definition used (written before reading the author's code)

> A rank-r bilinear scheme for <n,m,p> (A is n x m, B is m x p, C = AB is n x p) is r triples (u_k, v_k, w_k) with
> m_k = (sum_{i,j} u_k[i,j] A[i,j]) (sum_{j,l} v_k[j,l] B[j,l]) and C[i',l'] = sum_k w_k[i',l'] m_k for all A, B.
> Comparing coefficients of A[i,j] B[j',l] in C[i',l'] gives the Brent equations
> T[(i,j),(j',l),(i',l')] := sum_k u_k[i,j] v_k[j',l] w_k[i',l'] = [i=i'][j=j'][l=l'] for all n*m * m*p * n*p index triples
> (this is the trilinear form trace(A B C^T) written with the C index in the same orientation as AB).

Index convention (fixed by the README / file headers, and checked against each file's `# convention` line): u index i*21+j, v index j*21+l, w index i*21+l, C[i][l] = sum_k w_k[i*21+l] m_k.

## What I checked, and how

- Files: object parts joined in numeric part order; sha256 of joined u, v, w each equals the value in CLAIM.md (3 of 3 match).
- r: CLAIM.md and STATEMENT.txt both say exactly 4471; each of the three files has exactly 4471 term lines, header `# rank 4471`, `# format 20 21 21`, convention line as above; indices in range, no duplicate index in a line.
- Zero factors: terms with a zero factor: 0 (empty or all-zero lines are counted, none found); explicit zero coefficients: 0.
- Nonzeros u 211890, v 98908, w 89223, and LCDs U 22736, V 112, W 112: both equal the values stated in CLAIM.md.
- Brent equations: ALL 77792400 index triples (420 x 441 x 420) checked, 0 wrong. Arithmetic: factors scaled to integers by their LCDs (D = Du*Dv*Dw = 285200384), then for each C-entry c the slab T[:,:,c] = Uc^T diag(W[:,c]) Vc over the terms with W[k,c] != 0 is formed as a dense matrix product and compared with D*delta; direct float64 BLAS, every partial sum provably < 2^53 (max slab bound 123033949991008 < 2^53 incl. D). No dense 3-tensor is built.
- Own checker run (python3 -I, nice -n 10): 0.7 s wall including parsing, peak RSS 266 MB.
- Independent smoke check (separate code path, Python Fractions): scheme applied to a random integer A, B pair: `20x21x21 r 4471 random exact eval (ints in [-9,9], Fractions): entries differing 0 of 420`.
- Checker validation before use: Strassen <2,2,2> rank 7 and naive <2,2,3> rank 12 pass (both arithmetic modes); Strassen with one coefficient changed, Strassen with one sign flipped, and naive <2,2,3> minus one term are all rejected (both modes).
- Negative control on this real object: w[2235] had one coefficient changed by +1/7 in memory; my checker reported 440 wrong equations and rejected it (0.8 s).
- Determinism: results are integer-exact; the author's checkers' printed output reproduced identically (see below); my checker gave the same result on re-runs of the smallest cell.

## Result vs claim

Claim: exact bilinear scheme over Q with exactly 4471 multiplications for <20,21,21>. My result: confirmed from the saved files, all 77792400 Brent equations hold exactly, exactly 4471 terms, no zero factor. The claimed numerical comparison (4471 < 4723, the rank CLAIM.md says is listed) is consistent as numbers; I did not re-fetch any table (no network), so the listed values themselves are not independently verified by me.

## Author's REPRODUCE.md, run in a copy of claim/

`sh verify-it-yourself/run_checks.sh` exited 0, last line PASS. 3 sha256 matches; check 1 (stdlib) 21 s, check 2 (numpy) 2 s, whole script 23 s wall, peak RSS 0.51 GB (/usr/bin/time -l, shared machine, nice). Both checkers printed `77792400 checked (all index triples), 0 wrong` and the output (with timing and progress lines removed) is identical, line for line, to the expected output block in REPRODUCE.md. I did not run the optional rebuild (REPRODUCE.md step 2, needs a network download) nor the negative-control script (I made my own).

## Mismatches

None. Caveats: the table-rank comparison and the provenance (LITA 21x21x21 rank 4723) are not re-checked here.

pass: true
