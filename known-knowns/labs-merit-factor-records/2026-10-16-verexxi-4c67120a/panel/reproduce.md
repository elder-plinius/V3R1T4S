# REPRODUCE verdict, claim L = 232

context: subagent (same VM)

Input read: only the claim folder (CLAIM.md, REPRODUCE.md, baseline.tsv, parent.txt, sequence.txt, source_excerpts.txt, sources_checked.md, check_energy.py, plus my own files in work-reproduce/). TROPHY_CASE.md was not used.

## Definition used (quoted from CLAIM.md)
"Definitions: s_i in {+1,-1}, C_k = sum_{i=0}^{L-1-k} s_i s_{i+k}, E = sum_{k=1}^{L-1} C_k^2, F = L^2/(2E).
Encoding of sequence.txt: character 0 means +1, character 1 means -1 (E is invariant under global negation)."
Criterion: strictly smaller integer energy than the best published energy for the length; compare integer energies, not rounded merit factors.

## My checker (written before opening check_energy.py)
work-reproduce/my_check.py : pure integer double loop over k and i, 0 -> +1, 1 -> -1.
Second independent method (full cross-correlation product, E = (sum of squares of all lags - L^2)/2) also run.

## Checks
1. sequence.txt: one line, 232 characters (plus newline), alphabet {0,1}, 109 zeros / 123 ones. PASS
2. Energy of sequence.txt: my_check.py prints "232 3032"; second method gives 3032; F = 53824/6064 = 8.87598944591. Matches claimed E = 3032. PASS
3. Parent: parent.txt cites 2210.15962 line 509: "229 & 2810 & 9.3311 & 87% & 0x0F81FF03DFF1E7BCE6CB9B1517328" (source_excerpts.txt).
   I decoded the 29 hex digits to 116 bits, took the low 115 bits (= (229+1)/2), and expanded to length 229 by skew-symmetry s_{n+j} = (-1)^j s_{n-j}, n = 114. The result equals parent_sequence in parent.txt exactly. Its energy is 2810 (my checker), and 229^2/(2*2810) = 9.3311, matching the printed values. No "repair:" or "note:" is present in parent.txt, so those checks do not apply. PASS
4. Operation: operation_code "prefix=- suffix=000 trim_start=0 trim_end=0" (empty prefix, suffix 000). parent_sequence + "000" == sequence.txt exactly (3 appended elements, as CLAIM.md states). PASS
5. baseline.tsv (3 rows for L = 232), each against source_excerpts.txt:
   - knauer2004: excerpt "232* 3752 7.1727 <116 run lengths>". Run lengths sum to 232; decoded with alternating signs, energy 3752 (F 7.17270789), equal to printed E 3752. The only integer E consistent with F = 7.1727 (+-5e-5) is 3752. PASS
   - 2206.12070: excerpt row "$232$ ... fffad0296b1ca397ca63d8cedc5b991edc4c9d260d7920db0782b c1555 & 7.1727 & 8.05748502994". Concatenating the two hex groups gives 58 digits, 232 bits; energy 3340, F = 8.05748502994012, equal to the printed F. The only integer E consistent with the printed F is 3340. PASS
   - 2206.12070-oldMF: the same row's old-column F 7.1727 gives E = 3752 only; there is no separate sequence. PASS
   baseline_E = min(3752, 3340, 3752) = 3340, as claimed. 3032 < 3340 strictly. PASS
6. Agreement of baseline.tsv, source_excerpts.txt and sources_checked.md on which sources have a row for L = 232: sources_checked.md marks "yes" for 2206.12070 and knauer2004 only, and "no" for the other 8 sources. The excerpts contain L=232 lines only from 2206.12070 and knauer2004. The 2011.00068 and 2210.15962 excerpts show only odd lengths (229, 231, 233, ... ), so there is no 232 line, as sources_checked.md says. The other sources' ranges (449, 450..573, 67..119, 92..120) exclude 232; 1406.5301 (181..401, 16 lengths) has no excerpt line in L-3..L+8, consistent with "no". No mismatch. PASS (I did not re-fetch any sources; judged from the saved excerpts only.)
7. Comparison with check_energy.py: prints "232 3032" on sequence.txt and "229 2810" on the parent, identical to my checker. Two repeated runs of both checkers gave identical output (deterministic). PASS

## Real outputs
my_check.py on sequence.txt : 232 3032
check_energy.py on sequence.txt : 232 3032
parent : 229 2810 (both checkers)
2206.12070 L=232 hex row : 3340 ; Knauer L=232 runs : 3752

Not judged here: completeness of the literature (NOVELTY and CRITERION skeptics).

pass: true
