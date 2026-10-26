# CRITERION skeptic: A_4^GC(19,14,9) >= 44
context: fresh subagent for the CRITERION role, given only claim/ and the step-6 instruction, with its own scratch folder; it also opened the bank file cited in CLAIM.md to check the quote.

## 1. Does the object meet the literal bank criterion, and is the quote faithful?
- Quote: the text in claim/CLAIM.md and claim/PREREG.md matches line 11 of known-unknowns/biology/dna-codes-gc-king-table.md at the pinned repo commit 1ebdef41c30414cd2a036b00f5e81d0fc4c1dc25, character for character. Faithful.
- Independent checker, written from the definition (not the author's code), on claim/objects/A4GC_19_14_9_M44.txt (sha256 8b28d53b3639dc0cc9d1a1afd37dfca139f5c3852c66003db5ee118b476c1a1a, matches CLAIM.md): 44 words, 44 distinct, all length 19, alphabet {A,C,G,T}, GC count of every word = 9 (= floor(19/2)), minimum pairwise Hamming distance = 14. PROVED-HERE (exhaustive pairwise check).
- Table: claim/data/dnacodes.html (sha256 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5, matches CLAIM.md), row n=19, column d=14 reads "38 v", with no '.' or ':', so the cell is unmarked and eligible. 44 > 38. The author's checker (claim/code/check_gc_code.py) also prints "VERDICT: VALID, beats_table=True".
- w: the page's header is A_4^GC(n,d,w) and the bank text defines w = floor(n/2). King 2003 was not opened here, so "confirm from King 2003" rests on the bank text (KNOWN, low risk).
- Clause NOT confirmed here: "strictly greater than any value for the same (n,d,w) found by a novelty search of post-2010 literature". CLAIM.md says plainly that it is not met in the package and leaves it to NOVELTY. The criterion is a conjunction, so a full win needs NOVELTY to cover post-2010 literature (16 years, not just the default 24 months) and find nothing >= 44. The "re-fetched live immediately before claiming" clause also belongs to NOVELTY/gate: the copy in the package was fetched 2026-10-25T10:17:08Z.
- Not a partial win: neither enumerated partial win (tie-unmarked-mid, new-optimality-proof) applies. The claim is a strict improvement on one cell, nothing else.
- No browser User-Agent, cookie, retry or challenge-bypass strings in claim/code or claim/null.

## 2. Was PREREG frozen before measuring?
- sha256 of claim/PREREG.md = 84b4f7b324bf29dfa9516744f9f9e39ae2ab0a4ece9c12471a803629cd44a817, equal to claim/PREREG.sha256. The code hashes listed in PREREG match claim/code/gf4slice.py (d37c340e...), claim/code/check_gc_code.py (ba053c3e...) and claim/null/nullsample.c (7c5e3d1a...).
- claim/chronology.md gives a consistent order: PREREG 10:17:04Z, table fetch 10:17:08Z, object regeneration 10:17:48Z, null 10:27:12Z. Caveat: the hash proves integrity, not time. These times are file mtimes the author copied into chronology.md, with no external timestamp, so they cannot be checked independently from claim/.
- Prior sight: PREREG has a "prior sight (disclosed)" section saying the result was already seen in an earlier exploratory sweep and in an earlier run whose CRITERION skeptic failed, and that this run is "a clean re-formalization, not a blind search". It also writes the expected object hash into the PREREG. The misleading hand-typed folder name of the sweep is explained in both PREREG and chronology.md. This is honest and clear.
- Acceptable? Yes, for this kind of claim. It is an explicit object judged by a deterministic checker against a fixed table value. Prior sight cannot inflate that verdict: no threshold, statistic or selection among many outcomes was tuned. The freeze still adds value: it fixes the checker, the cell and the regeneration command in advance.

## 3. At least 400 controls?
- The four files in claim/null/*.out contain 400 "seed S size K" lines with 400 distinct seeds covering exactly 1..400, none missing and none duplicated (98 + 102 + 97 + 103). Best control 25, real 44, so real > max. This matches claim/null/null_test.md.
- The resume points (99 and 298) match the cut-off noted in null_test.md. Seeds are deterministic: an independent recompile of claim/null/nullsample.c reproduced seed 99 -> 22 and seed 250 -> 25 exactly.
- Note: the null (random-order greedy) is weak, about 22 on average. For a deterministic construction it is a sanity baseline, not the evidence. The evidence is the checker result above.

## Verdict
The object meets every clause of the bank criterion that can be checked from the package. The quote is faithful. The freeze and the prior sight are correctly declared. The null has 400 distinct seeds. The post-2010 literature clause is outside this file and must come from NOVELTY. The gate must not report a full win without it.

confirmed_scope: The 44-word list in claim/objects/A4GC_19_14_9_M44.txt (sha256 8b28d53b...c1a1a) is a quaternary code of length 19 with exactly 9 G/C per word, all words distinct and minimum Hamming distance 14, so A_4^GC(19,14,9) >= 44, strictly above the unmarked value 38 in the copy of King's table in claim/data/dnacodes.html fetched 2026-10-25T10:17:08Z; post-2010 literature not checked here.
pass: true
