# REPRODUCE verdict, claim L = 384

context: subagent (same VM)

Folder read: the claim folder only (CLAIM.md, REPRODUCE.md, sequence.txt, parent.txt, baseline.tsv, source_excerpts.txt, sources_checked.md, check_energy.py after my own checker). TROPHY_CASE.md was not used. My files: work-reproduce/my_check.py, work-reproduce/derive.py.

## Definition used (quoted from CLAIM.md)
"s_i in {+1,-1}, C_k = sum_{i=0}^{L-1-k} s_i s_{i+k}, E = sum_{k=1}^{L-1} C_k^2, F = L^2/(2E). Encoding of sequence.txt: character 0 means +1, character 1 means -1."
Criterion: integer energy strictly smaller than the best published energy for L; compare integer energies.

## My checker (written before opening check_energy.py), real outputs
- work-reproduce/my_check.py on sequence.txt: raw length 385 bytes (384 chars + newline), alphabet ['0','1'], L = 384, E = 10192, F = 147456/20384.
- Second independent method (full integer autocorrelation by double loop, symmetry and C_0 checked): L=384, E=10192, C_0 = 384, symmetric, max |C_k| = 24.

## Checks
1. sequence.txt length 384, alphabet {0,1} only: PASS.
2. Energy of sequence.txt = 10192 (two independent computations): PASS, matches claimed 10192 and F = 147456/20384.
3. Parent: source line "[2206.12070 ... line 885] $387$ ... 7ffffff0007fe033c1f66139c2d327c96786f078d8dc39b33339b 48d8da52e5a61ca730f49b166294b356aa5552aaaaaa & 7.1502 & 7.19974040958". Not a "repair:" parent and no inconsistency note. I decoded the hex (whitespace removed, 97 hex digits = 388 bits, the single dropped leading bit is 0) to 387 bits; it equals parent_sequence in parent.txt exactly. Its energy is 10401, and 387^2/(2*10401) = 7.19974040958, equal to the printed merit factor (matches parent.txt "recomputed E 10401"): PASS.
4. operation_code "prefix=- suffix=- trim_start=1 trim_end=2": child = parent[1:-2] has length 384, is identical to sequence.txt, energy 10192: PASS. Matches the 3-element edit stated in CLAIM.md and parent.txt.
5. baseline.tsv: one row for L=384, source 2206.12070, printed_E empty, printed_F 7.08923076923, smallest consistent E 10400, E of printed sequence 10400. Source line "[2206.12070 ... line 882] $384$ ... ffffffc001ff81cc673391e39cc3cc63c06f078e58f0fc9c9cad2 d86da52e54b64cb4c9b691b3264c95aa9554aaaaaaa & - & 7.08923076923". I decoded the hex to 384 bits (leading bits zero) and got E = 10400. 384^2/(2*10400) = 7.08923076923, the only integer E consistent with the printed F (checked integers around it). The decoded row differs from sequence.txt (and from its negation), so the claimed object is a different sequence. Baseline_E = 10400: PASS.
6. I also decoded the other excerpt rows (381..392) of 2206.12070: every printed F equals L^2/(2E) of its decoded sequence to all printed digits (e.g. 381: 10078, 383: 10367, 385: 10224, 387: 10401); none concerns L=384. The 1406.5301 excerpt line is for L=381 only (no 384 row). The first number column (7.106, 7.0314, 7.1502 ...) is a lower earlier-value column; "-" for 384 means no earlier value; it gives nothing for 384.
7. Agreement of baseline.tsv, source_excerpts.txt and sources_checked.md: only 2206.12070 has a row for L=384 in all three (excerpts contain exactly one $384$ line; sources_checked marks "yes" only for 2206.12070 and "no" for the other nine); fetch time and URL of 2206.12070 agree between baseline.tsv, parent.txt and sources_checked.md. PASS.
8. check_energy.py (read after my checker): independent integer implementation of the same definition; run 3 times on sequence.txt gave "384 10192" each time (deterministic); on the parent gave "387 10401". Matches my results and REPRODUCE.md expected output: PASS.
9. 10192 < 10400 integer comparison: PASS (claim of being below the baseline of this package holds). Literature completeness not judged here.

No mismatch, missing object or non-determinism found.

pass: true
