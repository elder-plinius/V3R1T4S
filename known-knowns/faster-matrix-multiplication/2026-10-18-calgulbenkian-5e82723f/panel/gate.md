# Honesty gate (fmm-ternary-integer-ring-upgrade)

status: CONFIRMED_SOLUTION
confirmed_scope: The file object/12x14x14_m1472_ZT.json is an exact integer (class ZT, largest absolute coefficient 1) bilinear scheme of rank 1472 for the 12x14x14 format whose Brent equations hold over Z, and rank 1472 is strictly below the ZT rank 1484 in the live Perminov README table, not below the overall best rank 1449 and not matched by any ZT-class scheme file in the two named repositories at the fetch time.

## Gate notes
- Object: object/12x14x14_m1472_ZT.json, sha256 0cebed78a0b198d25f02ba2e7b6960bb4b83cc57c41f4f35e6501d8f731cd006.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Full success criterion met for this cell, clauses (1) to (4); not a partial win. One cell per claim.
- Reproduce: exact Brent check over Z with the skeptic's own int64 checker (bound proven below 2^63), full tensor, no sampling; negative control rejected. Criterion: exact evaluation on random integer matrices plus the shipped checker. Novelty: live Perminov README, schemes tree, pull requests, issues and commits, MerlijnW70 tree, fmm_sota.json, V3R1T4S pull requests (pages 1 to 5) and TROPHY_CASE, all fetched 2026-10-18 from 14:20Z.
- No downgrade triggers found.
