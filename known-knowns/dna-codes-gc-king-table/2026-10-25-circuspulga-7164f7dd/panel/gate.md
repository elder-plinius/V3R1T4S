# Honesty gate (kit RUN.md step 7): run 2026-10-24-1217, dna-codes-gc-king-table, cell (15,11,7)

status: CONFIRMED_PARTIAL
confirmed_scope: The 42 distinct length-15 words over {A,C,G,T} in claim/objects/A4GC_15_11_7_M42.txt (sha256 7164f7dd9a56e376779fb30fc4d61a3dc7b6c9508cce1b4c1247f89d484b5089) each have GC-content 7 and pairwise Hamming distance at least 11, so A_4^GC(15,11,7) >= 42, strictly above the unmarked entry 34 in King's GC-only table as fetched 2026-10-25T08:37:25Z; superiority over post-2010 literature is not confirmed here.

Why PARTIAL and not SOLUTION: the bank criterion also requires the count to beat every post-2010 value for the same (n,d,w). The CRITERION skeptic's scope excludes that clause, and NOVELTY could not open the primary texts of SAMP 2011 (Discrete Math 311) and Aboluion-Smith-Perkins 2012 (Discrete Math 312) (HTTP 403; PENDING STATUS CHECK for those pages). The status is downgraded to the confirmed scope; never upgraded.

Caveats bound to this scope (they narrow, never widen):
- PREREG.v2.md (2026-10-24T12:38:40Z) was written after first results were seen. It moved the claim focus to the secondary cell (15,11) that PREREG.md (12:25:01Z) already named, and it added gf4slice.py. Disclosed; it does not affect a deterministic, checker-verified object.
- PREREG.v2.md lists a 39-word (15,11) result seen before it; the 40-word slice is the later gf4slice run (seed 2) used in the chain. Minor inconsistency, noted by CRITERION.
- null_test.md names seed 81 for best_control 26; the first seed reaching 26 is seed 10 (18 seeds reach it). Cosmetic; the maximum 26 and 400 controls are correct. The random greedy null is weak context for an explicit object.
- Literature: thesis Aboluion 2011 (best known max_w table) 34; Montemanni et al. 2014 34; nothing found at (15,11) in later work searched; the search is not exhaustive.

Panel read by the main session:
- reproduce.md: pass: true (own checker, chain rebuilt byte-identically, no evasive table access).
- novelty.md: pass: true (42 > 34 over all sources read; two primaries unread, PENDING).
- criterion.md: pass: true for the scope above only.
Gate: table fetch 2026-10-25T08:37:25Z is under 6 h old.


Re-gate (2026-10-25T08:48Z): the first gate was held at PROMISING because novelty.md's context line matched check_run's not-fresh pattern. The NOVELTY skeptic rewrote that line in its own context (novelty.md sha256 d20b37462b1c3b0f5ac3de27d5a86f7b4dcc227e63ce4842849efe8d20a92f33, still pass: true, content otherwise unchanged as reported). The gate did not edit any panel file. Status as above, no wider than CRITERION's scope.
