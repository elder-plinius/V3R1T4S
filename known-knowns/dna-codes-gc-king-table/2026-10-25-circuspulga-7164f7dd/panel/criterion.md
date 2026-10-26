# CRITERION skeptic — dna-codes-gc-king-table, cell (n,d,w) = (15,11,7)
context: subagent (fresh context, knowledgeWork), given only claim/ (CLAIM.md, PREREG.md, PREREG.v2.md, null/), plus own read-only checks on claim/objects and claim/data
checked at (date -u): Sun Oct 25 08:42:59 UTC 2026

## 1. Literal reading of the bank criterion (quoted in claim/CLAIM.md)
Clauses and finding:
- "table entry ... NOT followed by '.' or ':'": claim/data/dnacodes.html (sha256 25d6e9f8...18c5), first table
  "Lower bounds for A4^GC(n,d,w)", row n=15, column d=11 reads "34 v" (the 9th value of the row, d=3..20 header).
  No '.' or ':'. The GC,RC table is a different problem and is correctly not claimed. PASS.
- "length n over {A,C,G,T}", "distinct", "pairwise Hamming distance >= d": own independent script (not the
  author's checker) on claim/objects/A4GC_15_11_7_M42.txt: 42 lines, 42 distinct, all length 15, alphabet
  {A,C,G,T}, GC-count set {7}, minimum pairwise Hamming distance 11. PASS. (NUMERICAL, deterministic)
- "exactly the table's GC-content w (w = floor(n/2), confirm from King 2003)": King 2003 itself is not in the
  package, so the convention is not confirmed from the primary source here. It does not matter for this cell:
  n = 15 is odd, and swapping G<->A, C<->T maps GC-content 7 words to GC-content 8 words preserving Hamming
  distance, so A4^GC(15,11,7) = A4^GC(15,11,8); the object is valid under either reading of w. Hidden-quantifier
  risk on w: none for this cell. PASS.
- "count strictly greater than the table entry re-fetched live immediately before claiming": 42 > 34 against the
  copy fetched 2026-10-25T08:37:25Z (HTTP 200, same hash as the scout copy). The "immediately before claiming"
  re-fetch belongs to the NOVELTY skeptic / gate. Not re-fetched by me (inputs restricted to claim/).
- "AND strictly greater than any value for the same (n,d,w) found by a novelty search of post-2010 literature
  (e.g. Limbachiya-Gupta-Rao, Montemanni-Smith, arXiv 1903.03535, 2108.02033)": the package records only
  Montemanni-Smith-Koul 2014 (34) and Aboluion 2011 thesis ("34m2"). The bank's other named examples
  (Limbachiya-Gupta-Rao altruistic-algorithm papers, arXiv 1903.03535, arXiv 2108.02033) are NOT recorded as read.
  This clause is NOT confirmed by this skeptic; it is owned by the NOVELTY skeptic and the gate must not issue
  CONFIRMED_SOLUTION without a NOVELTY pass that explicitly covers those three sources.
- Upper-bound sanity: REPRODUCE.md states King 2003 Thm 4 gives <= 77; 42 is below it (not recomputed here).

## 2. Is PREREG valid? Does PREREG.v2 (written after seeing results) invalidate the claim?
- PREREG.md (frozen 2026-10-24T12:25:01Z) already named (15,11,7) as the secondary cell, table value 34, and froze
  the threshold "size > table value and checker VALID -> candidate for the full criterion" for any cell. That
  threshold is unchanged in v2.
- PREREG.v2.md (2026-10-24T12:38:40Z) is honest about being written AFTER results (it lists a 39-word (15,11) code
  already seen; the brief speaks of 40 words, the 40-word slice is the later gf4slice run in REPRODUCE.md: minor
  inconsistency, no effect). It did not edit PREREG.md, it is a separate timestamped file, as kit/RUN.md step 3
  requires. Procedure followed.
- Moving the focus to (15,11) after seeing results is cell selection after looking (forking paths across
  (15,12), (15,11), (20,15), (19,14), (18,13), (16,12), (20,16)). That would invalidate a statistical or
  "beats chance" claim. It does not invalidate this claim: the claim is an explicit object whose properties are
  checked deterministically (an existence/lower-bound statement). Either 42 such words exist or they do not; no
  choice of cell, threshold or seed after the fact can make a false lower bound true. The construction result is
  verifiable independently of the preregistration, and I verified it (section 1).
- Consequence of the forking: v2 correctly demotes (20,15,10) and (19,14,9) to exploratory; only one cell is
  claimed (kit rule 4: one cell per claim). Respected.

## 3. Null test
- null/null_test.md: controls 400, best_control 26, real 42, real_beats_all_controls yes.
- Recounted from null/null_15_11_*.out: 400 lines, 400 distinct seeds (1..400), maximum size 26 (reached by 18
  seeds; null_test.md names seed 81, but the first seed with 26 is seed 10: cosmetic, the maximum is correct).
  >= 400 controls: PASS. Caveat: random-order greedy is a weak null; for an explicit object the null is
  context, not the evidence (PREREG.md itself allows "not needed" for deterministic checker claims).

## 4. Hidden quantifiers / stretched definitions
- "Only objects produced by code in attempts/": chain gf4slice (40) -> gcmc (41) -> gcmc (42) is documented with
  intermediate files; the 42-word object is not a site code file. Rebuild is REPRODUCE's job, not re-run here.
- No "solved/record/first" wording in CLAIM.md beyond the table comparison. A lower bound 42 is not an optimality
  claim and the claim does not say it is.

## Verdict
Construction meets every literal clause of the bank criterion that can be checked from claim/ (alphabet, length,
GC-content, distinctness, distance, unmarked cell, 42 > 34). The prereg change is disclosed and does not affect a
deterministic construction claim. The literature clause is outside what this skeptic confirms and must be carried
by NOVELTY (with the three named sources) before the gate may write any CONFIRMED status.
confirmed_scope: The 42 distinct length-15 words over {A,C,G,T} in claim/objects/A4GC_15_11_7_M42.txt (sha256 7164f7dd9a56e376779fb30fc4d61a3dc7b6c9508cce1b4c1247f89d484b5089) each have GC-content 7 and pairwise Hamming distance at least 11, so A_4^GC(15,11,7) >= 42, strictly above the unmarked entry 34 in King's GC-only table as fetched 2026-10-25T08:37:25Z; superiority over post-2010 literature is not confirmed here.
pass: true
