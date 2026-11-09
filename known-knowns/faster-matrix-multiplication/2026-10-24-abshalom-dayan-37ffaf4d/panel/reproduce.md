# REPRODUCE skeptic verdict: <18,18,19> rank 3225 over Q

context: subagent (Claude Sonnet 5.5, fresh context, given only a copy of claim/)

## 1. My own checker (written before reading any author code)

Definition used (quoted from my checker header): a bilinear scheme of rank R for <n,m,p> (A n x m, B m x p, C n x p) is
C[i][l] = sum_k w_k[(i,l)] * (sum u_k[(i,j)] A[i][j]) * (sum v_k[(j,l)] B[j][l]),
equivalently the Brent equations: for ALL a=(i,j), b=(j2,l), c=(i2,l2): sum_k u_k[a] v_k[b] w_k[c] = [j==j2][i==i2][l==l2].
Index convention inferred from the README file-format text and tested: a = i*18+j, b = j*19+l, c = i*19+l (C not transposed).

My checker is independent code (stdlib only, Fractions for parsing and exact integer arithmetic after scaling by my own computed per-matrix LCDs). Results from the saved files object/u.txt, object/v.part1.txt + object/v.part2.txt, object/w.txt:

- Parsing is strict: every line is index:coefficient with an integer or p/q only (regex), indices in range and unique per line, no zero coefficients, no empty factor, headers `# format 18 18 19` and `# rank 3225`, exactly 3225 term lines in each of u, v, w. All passed. Ring Q: all coefficients are exact rationals (no floats, no mod-p); denominators 1, 2, 4, 5, 7, 10, 12, 14, 25, 28, 50, 84, 300, 600, 1200; my LCDs U 8400, V 84, W 84 (match the claim).
- Brent equations: 37,896,336 index triples checked (= 324 * 342 * 342, every triple including those that must be 0), 0 wrong; exactly 6156 = 18*18*19 triples have target 1 (as expected).
- 3 random exact evaluations C = AB with random rational A (18x18), B (18x19) (own seed 777): 0 of 342 entries differ, each time.
- Term count: 3225, zero-factor terms 0; nonzeros u 102579, v 145368, w 64253 (match the claim).
- Mergeability: 0 pairs of terms share two proportional factors, for each of the pairs (u,v), (u,w), (v,w) (own check; matches the claim).
- Convention reconciliation: the claim's convention (README/REPRODUCE.md: m_k = (sum u_k[i*18+j] A[i][j]) (sum v_k[j*19+l] B[j][l]); C[i][l] = sum_k w_k[i*19+l] m_k) is the one I tested and it is correct. Negative controls on my checker: (a) perturbing one w coefficient gives 1100 wrong equations and a differing random evaluation; (b) the transposed-C convention (c = l*18+i) gives 12240 wrong equations. So the checker discriminates and the stated convention is the one that makes the scheme correct.
- Peak memory of my checker 105 MB, 18.7 s, run under nice -n 10.

## 2. sha256 of the object files

Recomputed independently with shasum: u.txt 37ffaf4dc24686ccb944605fd965f8b981088a74cf5246a54d6bcf5a2b665eca, w.txt 0f0a3d5cffe4ba63b5aa9a464c87abe0c17a501028c2d7f0d02cc128ea4fd93a, cat v.part1.txt v.part2.txt = 5d15717baf763e44e9fb2808ff92335e66ec76f0940c0f75839a79a33ea4c5be. All three match CLAIM.md.

## 3. Author's verify-it-yourself/run_checks.sh (run twice, under nice -n 10, /usr/bin/time -l)

- Run 1: exit 0, last line PASS, 76.0 s wall, peak RSS 1.27 GB. Run 2: exit 0, PASS, 75.6 s, peak RSS 1.16 GB. Both under the 1.5 GB limit.
- Stdout of the two runs is byte-identical (no non-determinism seen), and it matches the output block in REPRODUCE.md / verify-it-yourself/RECEIPTS.md line for line (hashes, nonzero counts, LCDs, 37896336 checked, 0 wrong, 3 random evaluations, both checkers PASS). The 352800 figure printed by the second checker is, as CLAIM.md says, a scaling factor and not an LCD.
- Skimming check_brent_stdlib.py afterwards: same index convention as mine (a = i*n2+j etc.), so no convention discrepancy.
- REPRODUCE.md step 2 (rebuild from LITA's npz, code/rebuild_lita_slices.py, code/drop_accounting.py) needs a network download of schemes/19x19x19_r3633.npz plus numpy/python-flint; NOT run (offline). The deterministic-rebuild claim and the per-slice kill counts (180, 28, 19, 179) are therefore taken from COMMANDS.md as stated and not independently reproduced. The scheme's validity does not depend on this, since the saved object was verified directly.

## 4. Drop-accounting arithmetic (README.md / how-we-built-it/COMMANDS.md), re-derived

- Slice 1: 180 + 28 = 208 killed; 3633 - 208 = 3425; one 2-reduction: 3424.
- Slice 2: 19 + 179 = 198 killed; 3424 - 198 = 3226; one 2-reduction: 3225.
- Total removed: 208 + 1 + 198 + 1 = 408 = 3633 - 3225. Correct.
- Side figures: 3633 - 38 = 3595; 3633 - 76 = 3557; 3424 - 29 = 3395; 324 + 3031 = 3355 (Lille index construction); 2 * 1762 = 3524 (Lille page Kronecker construction). All correct, and 3225 < 3355 < 3524.

## 5. Not verified by me (outside this panel's offline scope)

The table values (3355 in fmm_sota.json, 3355 on the Lille index, 3524 on the Lille page) and the novelty claims about other V3R1T4S PRs rest on fetches I did not repeat (no network); I only checked the arithmetic and that the claim's own saved record is consistent. The claim as worded (the files define a rank-3225 scheme over Q for <18,18,19>, and 3225 is below the quoted listed ranks) is fully confirmed for everything checkable offline.

## Verdict

Every property of the object was confirmed from the saved files with an independently written exact checker: all 37,896,336 Brent equations, term count 3225, ring Q, sha256 matches, convention matches, random exact evaluations, author's script passes twice with identical output and within memory limits. No mismatch, missing object or non-determinism found.

pass: true
