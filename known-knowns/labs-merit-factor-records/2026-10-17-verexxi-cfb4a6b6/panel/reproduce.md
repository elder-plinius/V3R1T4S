# REPRODUCE verdict, claim L = 391 (labs-merit-factor-records)

context: subagent (same VM)

Only files inside the claim folder were read (CLAIM.md, REPRODUCE.md, TROPHY_CASE.md not needed, baseline.tsv, parent.txt, sequence.txt, source_excerpts.txt, sources_checked.md, check_energy.py). My work files: work-reproduce/mychk.py (own checker, written before opening check_energy.py).

## Definition used (quoted from CLAIM.md)
"s_i in {+1,-1}, C_k = sum_{i=0}^{L-1-k} s_i s_{i+k}, E = sum_{k=1}^{L-1} C_k^2, F = L^2/(2E).
Encoding of sequence.txt: character 0 means +1, character 1 means -1 (E is invariant under global negation)."
Claim: E = 10471 for L = 391, strictly below baseline_E = 10675. Comparison is on integer energies.

## My checker outputs (work-reproduce/mychk.py, pure integer arithmetic; run 3x, identical)
- sequence.txt: `391 10471`
- second independent method (big-integer polynomial product, ad hoc): `391 10471`
- parent (parent_sequence from parent.txt): `389 10234`
- printed L=391 sequence decoded from hex in source_excerpts.txt: `391 10675`

## Checks
1. sequence.txt: one line, 391 characters (plus newline), alphabet {0,1} only. PASS
2. Energy of sequence.txt = 10471 (two methods, deterministic over repeated runs). PASS
   F = 391^2/(2*10471) = 152881/20942 = 7.30021..., matches CLAIM.md.
3. Parent source line (source_excerpts.txt, 2206.12070 bare_jrnl.tex line 887, row 389): 98 hex digits (after removing the printed line-wrap space), top 3 pad bits zero, right-aligned decoding gives 389 bits (0 bit -> '0'). Decoded string equals parent_sequence in parent.txt exactly (not negated). PASS. Its energy is 10234; the printed F 7.39305256987 gives 389^2/(2F) = 10233.99999999..., the only integer in the rounding interval is 10234. Consistent. (This is a plain hex parent, no "repair:" or "note:" in parent.txt.) PASS
4. operation_code `prefix=- suffix=01 trim_start=0 trim_end=0`: empty prefix, suffix "01", no trimming. parent_sequence + "01" equals sequence.txt exactly (string equality, 389 + 2 = 391). PASS
5. baseline.tsv rows for L = 391 (2 rows), checked against source_excerpts.txt line 889 (row 391, B_391^{27,13,10,7,1}):
   - 2206.12070 row: printed F 7.16070257611 -> E = 152881/(2*7.16070257611) = 10675.000000004; unique integer in the rounding interval = 10675 (matches smallest_E_consistent 10675). Printed hex (98 digits, 1 pad bit zero) decodes to 391 bits with recomputed E = 10675 (matches E_of_printed_sequence 10675, decoding hex-full). PASS
   - 2206.12070-oldMF row: the other printed F in the same line, 7.1553 -> E = 10683.06; unique integer in rounding interval = 10683 (matches). No sequence printed for that column. PASS
   - baseline_E = min(10675, 10683) = 10675, as claimed. PASS
   - printed F, URLs, fetch times of both rows match sources_checked.md (2206.12070 fetched 2026-10-16T17:00:24Z, HTTP 200). PASS
   - The printed L=391 sequence differs from sequence.txt (it is the 10675 one), so the new object is not just a copy of the baseline. PASS
6. Cross-consistency of the three package files about which sources have a row for 391: sources_checked.md marks "yes" only for 2206.12070; baseline.tsv has rows only for 2206.12070 (two columns of the same table line); source_excerpts.txt quotes lines L-3..L+8 (388..399, 12 lines) only from 2206.12070 and no other source. All 9 other sources are marked "no" and none appear in baseline.tsv or the excerpts. PASS
7. 10471 < 10675 strictly (integer compare). PASS
8. check_energy.py (read after my checker): same definition (0->+1, 1->-1, sum over k=1..L-1 of C_k^2, Python ints); output `391 10471` on sequence.txt and `389 10234` on the parent; identical to my results. REPRODUCE.md expected output matches. PASS

## Notes outside REPRODUCE scope (for other skeptics)
- sources_checked.md itself lists unread items (arXiv:2011.00068 v1 reportedly tabulating odd 301..401; git_labs even/odd record pages; Mertens open.dat; journal versions). Literature completeness is for NOVELTY/CRITERION.

## Mismatches / non-determinism / missing objects
None found.

pass: true
