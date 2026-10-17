# REPRODUCE verdict, claim L = 252

context: subagent (same VM)

Instruction followed: "Before reading the author's code, write your own checker from the definition (quote it). Verify every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."

Definition used (quoted from CLAIM.md): "s_i in {+1,-1}, C_k = sum_{i=0}^{L-1-k} s_i s_{i+k}, E = sum_{k=1}^{L-1} C_k^2, F = L^2/(2E). Encoding of sequence.txt: character 0 means +1, character 1 means -1."
My checker: work-reproduce/mycheck.py (written before opening check_energy.py; exact Python integers, double loop; output saved in work-reproduce/out_mycheck.txt).
The claim is a single explicit object (not an exhaustive search), so there is no search to re-run.

## Checks and results
1. sequence.txt: one line, 252 characters (253 bytes with the newline), alphabet {0,1} only. PASS.
2. Energy of sequence.txt by my checker: L = 252, E = 3534, F = 63504/7068 = 5292/589 = 8.98472. Matches claimed E = 3534. PASS.
3. Parent (parent.txt, source 2011.00068, L = 253): parent_sequence has 253 chars over {0,1}; my E = 3670, F = 253^2/(2*3670) = 8.72057, matching the printed F 8.7206 and "recomputed E 3670". PASS.
4. Parent re-derived from its quoted source line (source_excerpts.txt, 2011.00068 line 39): the printed hex (64 digits = 256 bits) with the 3 leading zero bits dropped (last 253 bits) equals parent_sequence exactly (not the complement). PASS.
5. Operation (prefix=- suffix=- trim_start=0 trim_end=1): parent_sequence[:-1] equals sequence.txt exactly, E = 3534. PASS.
6. baseline.tsv rows for L = 252 (3 rows), checked against source_excerpts.txt:
   - knauer2004: the line "252* 4386 7.2394 ..." has 126 run lengths summing to 252; decoded sequence has E = 4386. Printed E 4386, F 7.2394 (the smallest integer E consistent with 7.2394 at 4 decimals is only 4386). PASS.
   - 2206.12070 (hex-full): the printed hex (63 digits after removing the space = 252 bits) gives E = 3738. Printed F 8.49438202247 gives 63504/(2F) = 3738.0000000008, and 3738 is the only integer consistent at 11 decimals. PASS.
   - 2206.12070-oldMF: printed F 7.2394 (old column), no sequence; the only integer E consistent is 4386. PASS.
   - baseline_E = min(4386, 3738, 4386) = 3738, as stated; 3534 < 3738 strictly. PASS.
7. Agreement of baseline.tsv, source_excerpts.txt and sources_checked.md on which sources have a row for L = 252: sources_checked.md marks "yes" only for 2206.12070 and knauer2004; baseline.tsv has rows only for those (2206.12070 twice, two columns of the same table line); source_excerpts.txt contains a 252 line only for those two. The other sources do not cover 252: 2011.00068 (odd lengths 201..303, the excerpt shows 249, 251, 253, 255, ... only), 1406.5301 (excerpt shows only 249, 259), 2210.15962 (171..247), 2504.00987 (92..120), 2607.09688 (450..573), 1512.02475, 2106.03377, 2409.07222 (ranges that exclude 252). Consistent. PASS.
8. Comparison with check_energy.py (read after my checker): same definition and encoding. Outputs: sequence -> "252 3534", parent -> "253 3670", parent minus last char -> "252 3534". Identical to my results. PASS.
9. Determinism: my checker run 3 times gave identical output (after sorting a set print; an earlier md5 difference came only from the unordered printing of the set {'0','1'} under hash randomization, not from any computed value). check_energy.py output is deterministic integers. PASS.

Not judged here: completeness of the literature (NOVELTY and CRITERION skeptics).
Note: I read only files inside the claim folder (TROPHY_CASE.md was not opened). Nothing outside it was read.

pass: true
