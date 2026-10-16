# REPRODUCE verdict, claim L = 328 (labs-merit-factor-records)

context: subagent (same VM)

Only files inside the claim folder (CLAIM.md, REPRODUCE.md, TROPHY_CASE.md present, sequence.txt, parent.txt, baseline.tsv,
source_excerpts.txt, sources_checked.md, check_energy.py) were read; work files are in work-reproduce/ (mychk.py, run.py).

## Definition used (quoted from CLAIM.md)
"s_i in {+1,-1}, C_k = sum_{i=0}^{L-1-k} s_i s_{i+k}, E = sum_{k=1}^{L-1} C_k^2, F = L^2/(2E).
Encoding of sequence.txt: character 0 means +1, character 1 means -1."
Claim: E = 7148 for sequence.txt (L = 328), strictly below baseline_E = 7444.
My checker (work-reproduce/mychk.py) was written before opening check_energy.py: exact Python ints, direct double sum.

## Checks and results
1. sequence.txt: one line, length 328, alphabet {0,1} only. PASS.
2. My energy: E = 7148 (run.py). Cross-check by a separate full-convolution computation: E = 7148, C_0 = 328, symmetric
   in k. Global negation: E = 7148. F = 107584/14296 = 7.525461667599. PASS (claimed 7148 matches exactly).
3. Parent. Source line (2206.12070/bare_jrnl.tex line 780, L=327) hex, spaces removed: 82 hex digits = 328 bits; leading
   bit is 0 (hex begins 7), so the 327-bit sequence is the last 327 bits. My decode has E = 6883, F = 7.767615865175, equal
   to the printed 7.76761586518; the only integer E consistent with that printed F (to 11 decimals) is 6883. The printed
   7.3009 in the other column is not used by the claim. The decoded sequence is identical to parent_sequence in parent.txt
   (327 chars) and parent.txt says printed E "-", printed F 7.76761586518, recomputed E 6883: all agree. No repair/note case
   applies (parent is not a "repair:" parent). PASS.
4. Operation. operation_code "prefix=- suffix=1 trim_start=0 trim_end=0": my parent decode + "1" == sequence.txt exactly
   (checked as strings). PASS.
5. Baseline. baseline.tsv has exactly one data row for L = 328 (source 2206.12070, printed_E empty, printed_F 7.22622246104,
   smallest_E_consistent 7444, E_of_printed_sequence 7444, decoding hex-full). Source line 781 (L=328) prints "-" for the
   first value column and 7.22622246104 in the last. I decoded its 82 hex digits (328 bits, no leading bits to drop): E = 7444,
   F = 7.226222461042, equal to the printed value; the only integer E consistent with the printed F is 7444. So all three
   baseline columns re-derive and baseline_E = 7444 holds. 7148 < 7444 strictly. PASS.
   (My decode of the sibling rows L=325..336 also reproduced their printed F values, which confirms the hex decoding convention:
   take the last L bits.) The new sequence differs from the published L=328 sequence in 126 of 328 positions (202 under
   global negation), so it is a different object, not a re-encoding.
6. Consistency of the package about which sources have a row for L=328: sources_checked.md lists 2206.12070 as "yes" and
   all other nine sources as "no"; source_excerpts.txt contains lines only from 2206.12070; baseline.tsv has only the
   2206.12070 row. The three files agree. The stated length ranges of the "no" sources (67..119, 92..120, 171..247, 201..303,
   10..304, 449, 450..527, 450..573) exclude 328; 1406.5301 (16 lengths within 181..401) cannot be confirmed from the folder
   alone (its tables are not included); I take the package's "no" at face value and leave source completeness to
   NOVELTY/CRITERION. No mismatch found within the package. PASS (within REPRODUCE scope).
7. check_energy.py compared with mine: same definition and mapping (0 -> +1, 1 -> -1, also accepts +/-); output for
   sequence.txt "328 7148", identical to mine, and identical on a second run (deterministic). The REPRODUCE.md expected
   output "328 7148" matches. PASS.
8. Exhaustiveness: this claim is a single explicit object with an exactly computed energy, not an exhaustive-search claim,
   so no search needs re-running. Non-determinism: none (pure integer arithmetic, two runs identical).

## My checker's real outputs
- sequence.txt: len 328, E 7148
- parent 327: E 6883, F 7.767615865175069; parent.txt string == decoded hex; sequence == parent + "1": True
- published L=328: E 7444, F 7.22622246104245
- check_energy.py (two runs): "328 7148" and "328 7148"

No mismatch, missing object or non-determinism found.

pass: true
