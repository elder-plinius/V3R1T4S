# REPRODUCE verdict, claim L = 242 (labs-merit-factor-records)

context: subagent (same VM)

## Definition used (quoted from CLAIM.md)
"s_i in {+1,-1}, C_k = sum_{i=0}^{L-1-k} s_i s_{i+k}, E = sum_{k=1}^{L-1} C_k^2, F = L^2/(2E).
Encoding of sequence.txt: character 0 means +1, character 1 means -1."
Claim: E = 3337 for the length-242 sequence, strictly below baseline_E = 3593.
I only read files inside the claim folder, and wrote only inside work-reproduce/ (mychk.py, derive.py, base.py).

## Own checker (work-reproduce/mychk.py, written before opening check_energy.py)
Plain Python ints, double loop over k = 1..L-1 and i = 0..L-1-k.
Output on sequence.txt: `242 3337`. An independent second computation (list of C_k, sum of squares) also gave 3337.

## Checks
1. sequence.txt: one line, 242 characters, alphabet {0,1} only. PASS
2. Energy of sequence.txt = 3337 (my checker), 3337 = claimed; F = 58564/6674 = 8.7747. PASS
3. Parent re-derivation. The quoted source line is `245 & 3226 & 9.3033 & 17\% & \texttt{0x1C38F1EFD72180453AC7548DCFC5F19}`
   (2210.15962 paper.tex line 516).
   - The hex is 31 digits = 124 bits. I took the low 123 bits as the first half s_0..s_122 (0 -> +1) of a skew-symmetric
     odd sequence (centre index 122, s_{122+j} = (-1)^j s_{122-j}) of length 245. This is my own decoding.
   - Of the 16 bit-order/orientation/sign conventions I tried, 4 gave E = 3226 (mirror/sign variants of one sequence).
     The plain one (low 123 bits, left half, 0 -> +1) reproduces parent.txt's parent_sequence exactly (equal, no negation or reversal needed).
   - E(parent) = 3226 matches the printed E, and F = 245^2/(2*3226) = 9.3033 matches the printed F.
   - Source hex was not a "repair:" and parent.txt carries no "note:", so neither check applies. PASS
4. Operation `prefix=- suffix=- trim_start=1 trim_end=2`: parent[1:-2] equals sequence.txt exactly (length 242). PASS
5. baseline.tsv rows for L=242 (3 data rows) against source_excerpts.txt:
   - 2206.12070, hex-full: hex `3ffff8846bc63c783dcc0f37852e761626f05a32d4c8b5a4b64be45daaaaa` (line split at a space,
     joined; 61 digits, 242 bits after the leading 3). I recomputed E = 3593. Printed F 8.14973559699 gives
     L^2/(2F) = 3593.000000002, and 3593 is the only integer consistent with the printed 11 decimals. Row says 3593 / 3593. PASS
   - 2206.12070-oldMF: printed 7.1893, no sequence. The only integer energy consistent with 7.1893 (4 decimals) is 4073. Row says 4073. PASS
   - knauer2004, runs-full: printed E 4073, F 7.1893. I decoded the 121 run lengths (sum 242) and recomputed E = 4073,
     F = 7.18930. Row says 4073 / 4073. PASS
   - Minimum over all rows and values = 3593 = claimed baseline_E. PASS
6. Cross-consistency of baseline.tsv, source_excerpts.txt and sources_checked.md:
   - Rows for 242 exist only in 2206.12070 and knauer2004 in all three files.
   - The excerpts show no 242 row in 2011.00068 (239, 241, 243...), 2210.15962 (odd only), or 1406.5301 (241, 249).
   - sources_checked.md marks "no" for 1406.5301, 1512.02475, 2011.00068, 2106.03377, 2210.15962, 2409.07222, 2504.00987, 2607.09688
     (ranges 67..119, 450..527, 92..120, 450..573 etc. do not contain 242 or are odd-only), consistent. PASS
   - Limit: I can only verify the ranges stated, not the full TeX sources, which are outside the folder. Literature completeness is not judged here.
7. Comparison with check_energy.py (read after the above): same definition and mapping (0 -> +1, 1 -> -1, plus +/-),
   Python ints. `python3 check_energy.py "$(cat sequence.txt)"` gave `242 3337` on two runs; my checker gave `242 3337`;
   the parent gave `245 3226`. No mismatch, no non-determinism (the computation is exact integer arithmetic). PASS
8. Claim: 3337 < 3593 holds strictly. PASS

No mismatch, no missing object. All objects named in the package (sequence, parent, operation, baseline rows) are present and reproduce.

pass: true
