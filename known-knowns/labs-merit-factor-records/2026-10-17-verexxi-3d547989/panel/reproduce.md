# REPRODUCE verdict, claim L = 377 (labs-merit-factor-records)

context: subagent (same VM)

Files used (all inside the claim folder): CLAIM.md, sequence.txt, parent.txt, baseline.tsv, source_excerpts.txt, sources_checked.md, REPRODUCE.md, check_energy.py (read only after my own checker). My work files are in work-reproduce/ (mycheck.py, derive.py, alt.py).

## Definition used (quoted from CLAIM.md)
"s_i in {+1,-1}, C_k = sum_{i=0}^{L-1-k} s_i s_{i+k}, E = sum_{k=1}^{L-1} C_k^2, F = L^2/(2E). Encoding of sequence.txt: character 0 means +1, character 1 means -1."
Claim: E = 9452 for the length-377 sequence, strictly below baseline 9668 (F = 142129/18904).
Criterion: integer energies are compared, direction min.

## My checker (work-reproduce/mycheck.py, exact Python ints; second independent method alt.py via full pairwise autocorrelation table, which also asserts symmetry and C_0 = L)
- sequence.txt: length 377, alphabet {0,1} only, file is 378 bytes (377 chars + newline). PASS
- mycheck: `sequence 377 9452 142129/18904 7.518461701227253` PASS (E = 9452, F = 142129/18904 matches the claim exactly)
- alt.py (run twice): `377 9452` both times. PASS (deterministic, two methods agree)
- 9452 < 9668. PASS

## Parent re-derivation (derive.py)
- Quoted source line: 2206.12070 bare_jrnl.tex line 854, L = 379, B_379^{27,13,10,5}, hex (two chunks joined) = 95 hex digits = 380 bits, leading hex digit 7 so 1 leading zero bit, stripping it gives 379 bits. Printed MF 7.33685769742 (older MF column 7.2422).
- Decoded sequence energy 9789; F = 7.336857697415466, rounds to printed 7.33685769742; the only integer E consistent with the printed MF is 9789. PASS
- Decoded bits equal parent_sequence in parent.txt exactly (no complement needed). PASS
- parent.txt header (printed E -, printed F 7.33685769742, recomputed E 9789): all match my values. PASS
- This is not a "repair:" parent and has no "note:" about an inconsistent merit factor; none needed.
- operation_code `prefix=- suffix=- trim_start=1 trim_end=1`: removing 1 element at each end of the 379-sequence gives 377 characters identical to sequence.txt. PASS (check_energy on parent also gives 9789)

## Baseline rows vs source_excerpts.txt
- Row 1 (2206.12070, L=377, line 852): hex 1ffffffc001ff80e...555555, 95 hex digits = 380 bits, 3 leading zero bits, 377 bits; decoded energy 9668 (F = 7.35048613984278, matches printed 7.35048613984; only consistent integer E is 9668). Baseline row says printed_F 7.35048613984, smallest_E 9668, E_of_printed_sequence 9668. PASS
- Row 2 (2206.12070-oldMF): printed 7.2249 (older MF column on the same line 852); implied integer E = 9836 only; no sequence printed. Matches the row (9836, blank sequence energy, "no sequence printed"). PASS
- baseline_E = min(9668, 9836) = 9668 as stated in CLAIM.md. PASS
- source_excerpts.txt covers L-3..L+8 = 374..385 for 2206.12070 (all 12 lengths present, exactly one line for 377, no duplicate row) plus the one 1406.5301 line (L=381), which is not a row for 377.
- Agreement of baseline.tsv, source_excerpts.txt and sources_checked.md: 2206.12070 is the only source with "row for L? yes" and the only one with baseline rows and a 377 excerpt line; the nine other sources (1406.5301 181..401 w/ 16 lengths, 1512.02475, 2011.00068, 2106.03377, 2210.15962, 2409.07222, 2504.00987, 2607.09688, knauer2004) are "no" and have no row for 377 in baseline.tsv or excerpts. PASS (consistent). I cannot re-fetch sources (no web access, and nothing outside the folder is read), so I verified only against the saved excerpts.

## Comparison with check_energy.py
- `python3 -I check_energy.py "$(cat sequence.txt)"` run twice: `377 9452` both times; code is the same definition as mine (0 -> +1, 1 -> -1, sum of squared C_k). PASS. Output equals REPRODUCE.md's stated expected output.

## Caveats (not REPRODUCE failures)
- Completeness of the literature (unreadable sources listed in sources_checked.md, e.g. git_labs records, open.dat) is for NOVELTY/CRITERION skeptics.
- Verification of quoted source lines is limited to the saved excerpts.

All checks confirmed; no mismatch, missing object or non-determinism found.

pass: true
