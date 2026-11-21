# CRITERION skeptic - run 2026-11-03-1435-dnaedit93, cell (n,d)=(9,3), w=4
context: subagent (criterion) - fresh context, worked from a private copy of claim/; no other panel files read.
date: 2026-11-03 ~15:37 EST (20:37Z)

## Criterion (bank, verbatim, as frozen in PREREG.md)
"A codeword list for a parameter cell listed in https://brocku.scholaris.ca/items/43d5f016-9190-4ec2-8066-81f3860f672b (thesis tables) or
https://arxiv.org/abs/1505.06262, checked for length, alphabet, exact constraint set as defined by that source, all-pairs Levenshtein distance >= d,
in a cell that its source does not mark as optimal (the claimant must show this, since many small cells are already exhaustively solved), with size
strictly larger than the published lower bound (sources re-fetched live immediately before claiming) and than any later value found by novelty search."

## Clause-by-clause (literal reading)
1. Codeword list: claim/object/code_n9_d3_k1042.txt, 1042 lines, sha256 b51b30e3082648bc6cb0511bd156b71ae51c967f7281a83010d2c0e844e4a93a
   (recomputed). No blank lines, no CR, no comments.
2. Cell listed in the thesis tables: (n,d)=(9,3) is row 9, column 3 of Sun Table 7.1 (also Tables 5.1, 5.2, 6.4-6.6). Yes.
3. Exact constraint set as defined by the source. I re-read Sun Sec. 1.5 myself (DSpace extracted-text bitstream of the thesis,
   one web-fetch read ~20:27Z; a plain curl got no connection, not retried). The source defines an (n,d,w)_4 DNA code by:
   (1) "d_edit(x,y) >= d for all x,y in C, with x != y"; (2) "d_edit(x^RC,y) >= d for all x,y in C, including x = y";
   (3) fixed GC weight w, "we present results for a fixed GC weight of floor(n/2)"; edit distance = Levenshtein (substitution, insertion, deletion).
   For n=9: w=4. The claim and all checkers use exactly this set (no band on GC, no homopolymer rule, no extra constraint, not Hamming,
   not indel-only). No stretched definition found.
4. All-pairs Levenshtein >= d: own independent C checker (written from the definition above, full 10x10 DP, ordered pairs, checks
   d(x,y), d(rc(x),y) for all x != y separately rather than relying on the symmetry d(rc(x),y)=d(x,rc(y)), and d(rc(x),x)):
   output "lines=1042 K=1042 CR=0 min_xy=3 min_rcx_y(x!=y)=3 min_self_rc=3"; all words length 9, ACGT, GC=4, distinct.
   Claim's checkers/check2.c recompiled: "VALID 1042 words n=9 d=3 gc=4 min=3". Agreement.
5. Not marked optimal: Table 7.1 row 9 reads "9 32256 15558g 939g 161g 34e lle 5e,g 2 1" -> (9,3) = 939 with superscript g
   ("best known bound was found by Randomized GA"; bold = exact values, the unmarked remaining values = exhaustive exact).
   Table 5.2 gives 914* (exhaustive search did not finish in two weeks -> lower bound). The only upper bound in the source is
   Theorem 3 (<= 1/2 E^GC(n,d,w)), with no numeric value for (9,3). So the cell is open in the source. Shown.
6. Strictly larger than the published lower bound, source re-read live: 1042 > 939 (my own live read at ~20:27Z today shows 939g unchanged). Yes.
7. "and than any later value found by novelty search": this is the NOVELTY skeptic's job; I did not do a literature search and do not
   certify it. The claim's own notes find no later edit-metric GC+RC value for (9,3); Hamming-metric GC+RC tables are a different metric
   (an edit-d code is a Hamming-d code, so those are not bars). Pass here is conditional on the NOVELTY verdict, as the gate requires anyway.

## Hidden quantifiers / traps checked
- "including x = y" for RC: checked (min self-rc = 3). Odd n, so no self-complementary words exist anyway.
- GC "exactly floor(n/2)" vs a band: exactly 4 for every word.
- Size convention: Sun counts C itself (C and C^RC disjoint by the RC constraint; Theorem 3 proof). The claim counts the 1042 words of C,
  not C u C^RC (2084). Same convention.
- Constraint-model sanity vs a Sun exact cell: my own exact Bron-Kerbosch max clique on the same constraint model for (4,3): 72 admissible
  words, maximum 6 = Sun exact value 6. (5,3) exact clique (Python) did not finish within a 600 s cap; not used. (No n=9 clique run.)
- Composition across cells / partial-win stretch: none. This is one explicit object for one cell; the full criterion, not a partial win
  ("tie-largest-cell", "clique-optimality") is claimed, and it is not subsumed by either.
- Not subsumed by prior in-repo work: the pre-existing 1011-word candidate (disclosed in PREREG) is smaller, unpublished, and shares only 37
  words (up to rc) with the claimed object per the claim; 1042 > 1011 regardless.
- Null model: not applicable (explicit object, deterministic exhaustive checker against a fixed table value); PREREG says
  "null_test: not needed" with that reason, which matches RUN.md step 3b.

## Process notes (not criterion stretches)
- PREREG push budget "<= 30 min": claim reports push 14:37-15:08 EST with 1800 s per-job timeouts; the 1042 object was FOUND at t=612.7 s of
  its job, well inside 30 min. Borderline overall wall clock (~31 min) does not affect the criterion; PREREG made no hard reject on it.
- PREREG decision rule (largest code all checkers report VALID at end of budget) selects 1042; consistent.
- I did not re-run the search regeneration (REPRODUCE skeptic's job).

confirmed_scope: The 1042-word list in claim/object/code_n9_d3_k1042.txt (sha256 b51b30e3082648bc6cb0511bd156b71ae51c967f7281a83010d2c0e844e4a93a) is a code of length 9 over {A,C,G,T} with every word of GC weight 4 and Levenshtein distance at least 3 between any two distinct words and between any word and the reverse complement of any word including itself, which is strictly larger than the lower bound 939 (not marked exact) given for cell (n,d)=(9,3) in Table 7.1 of J. Sun's 2009 Brock M.Sc. thesis under that thesis's own constraint set; whether it also beats every later published value is left to the NOVELTY check.
pass: true
