# Honesty gate (fmm-ternary-integer-ring-upgrade)

status: CONFIRMED_SOLUTION
confirmed_scope: The file object/14x16x16_m2159_Z.json is an exact integer (class Z, largest absolute coefficient 6) bilinear scheme of rank 2159 for the 14x16x16 format whose Brent equations hold over Z, and rank 2159 is strictly below the Z rank 2170 in the live Perminov README table, not below the overall best rank 2128 and not matched by any Z-class scheme file in the two named repositories at the fetch time.

## Gate notes
- Object: object/14x16x16_m2159_Z.json, sha256 b7a26ff2e48fc42540d7b837421651ac747fc9b6e8b69b745ddf78091f8dffd8.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Full success criterion met for this cell, clauses (1) to (4); not a partial win. One cell per claim.
- Reproduce: exact Brent check over Z with the skeptic's own int64 checker (bound proven below 2^63), full tensor, no sampling; negative control rejected. Criterion: exact evaluation on random integer matrices plus the shipped checker. Novelty: live Perminov README, schemes tree, pull requests, issues and commits, MerlijnW70 tree, fmm_sota.json, V3R1T4S pull requests (pages 1 to 5) and TROPHY_CASE, all fetched 2026-10-18 from 14:20Z.
- No downgrade triggers found.
