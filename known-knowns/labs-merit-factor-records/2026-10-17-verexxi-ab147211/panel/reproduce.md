# REPRODUCE verdict, claim L = 380 (labs-merit-factor-records)

context: subagent (same VM)

Input read: only the claim folder panel-claim-L380 (CLAIM.md, REPRODUCE.md, baseline.tsv, parent.txt, sequence.txt,
source_excerpts.txt, sources_checked.md, and check_energy.py last). My files are in work-reproduce/ (mycheck.py, mycheck2.py).

## Definition used (quoted from CLAIM.md)
"s_i in {+1,-1}, C_k = sum_{i=0}^{L-1-k} s_i s_{i+k}, E = sum_{k=1}^{L-1} C_k^2, F = L^2/(2E).
Encoding of sequence.txt: character 0 means +1, character 1 means -1 (E is invariant under global negation)."
Criterion: integer energy strictly smaller than the best published energy for L; compare integer energies.

## My checkers (written before opening check_energy.py)
- work-reproduce/mycheck.py: direct double loop in Python ints, plus hex decoding of the quoted rows.
- work-reproduce/mycheck2.py: independent method (Kronecker-substituted big-integer product P(x)Q(x); C_k read off and
  checked symmetric, C_0 = L).
Real outputs:
- sequence.txt: length 380, alphabet {0,1}, E = 10058 (both methods), F = 36100/5029 = 7.17836548 (= 144400/20116, as claimed).
- parent_sequence (parent.txt): length 383, alphabet {0,1}, E = 10367.
- Two runs of mycheck.py gave byte-identical output (md5 equal): deterministic.

## Checks
1. sequence.txt is one line of 380 characters over {0,1}: PASS.
2. E(sequence.txt) = 10058 exactly, two independent methods: PASS. 10058 < 10286: PASS.
3. Parent re-derived from the quoted source line (source_excerpts.txt, 2206.12070 line 881, L=383, the "7ffffff0007fe0731..."
   row, hex split by a space in the print, concatenated: 96 hex digits = 384 bits, leading bit 0 dropped -> 383 bits).
   Decoded bit string equals parent_sequence in parent.txt exactly: PASS. Its energy is 10367; printed F 7.07480466866 vs
   recomputed 7.074804668660172; the only integer E consistent with the printed F at its printed precision is 10367:
   consistent. (Not a "repair:" parent and no inconsistency note; none applies.) The printed "7.0314" column of that row is a
   different, earlier figure and plays no role.
4. Operation: operation_code "prefix=- suffix=- trim_start=1 trim_end=2" applied to the 383-bit parent (remove 1 at start,
   2 at end) gives a 380-character string identical to sequence.txt (not just up to complement): PASS. Matches the
   description in CLAIM.md/parent.txt ("remove 1 element(s) at the start and 2 at the end").
5. baseline.tsv has one row for L=380: source 2206.12070, printed_E blank, printed_F 7.01924946529. Checked against
   source_excerpts.txt line 855 (L=380 row: E column "-", F "7.01924946529"): matches. Decoded hex of that row (95 hex digits
   = 380 bits, no padding) has energy 10286 (F 7.0192494652926...), and the only integer E consistent with the printed F is
   10286. Row says smallest_E_consistent = 10286, E_of_printed_sequence = 10286, decoding hex-full: all correct.
   baseline_E = 10286 confirmed: PASS.
6. Cross-file agreement on which sources have a row for L=380: baseline.tsv (only 2206.12070), source_excerpts.txt (the only
   L=380 line is from 2206.12070; lines for 377..388 are all present for 2206.12070, plus 1406.5301 for L=381 only, not 380),
   sources_checked.md (only 2206.12070 marked "yes"; the others "no", and their stated length ranges are consistent with
   no 380 row: 1406.5301 has 381 but not 380 in the excerpt window). The three files agree: PASS. (I cannot re-fetch sources;
   I judged only package-internal consistency with the quoted lines. Literature completeness is for NOVELTY/CRITERION.)
7. Comparison with check_energy.py: its energy() is the same definition; run on sequence.txt it prints "380 10058", on the
   parent "383 10367". Agrees with my checkers: PASS.
8. Non-determinism / missing objects: none found; all referenced files exist; no random elements.

No mismatch found.

pass: true
