# Honesty gate (fmm-ternary-integer-ring-upgrade)

status: CONFIRMED_SOLUTION
confirmed_scope: The file object/4x14x15_m569_Z.json is an exact integer (class Z, largest absolute coefficient 2) bilinear scheme of rank 569 for the 4x14x15 format whose Brent equations hold over Z, and rank 569 is strictly below the Z rank 572 in the live Perminov README table, not below the overall best rank 557 and not matched by any Z-class scheme file in the two named repositories at the fetch time.

## Gate notes
- Object: object/4x14x15_m569_Z.json, sha256 a736e53a74f68425c0211816e0972faf8c027d4845885509b530644e9f64c52b.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Full success criterion met for this cell, clauses (1) to (4); not a partial win. One cell per claim.
- Reproduce: exact Brent check over Z with the skeptic's own int64 checker (bound proven below 2^63), full tensor, no sampling; negative control rejected. Criterion: exact evaluation on random integer matrices plus the shipped checker. Novelty: live Perminov README, schemes tree, pull requests, issues and commits, MerlijnW70 tree, fmm_sota.json, V3R1T4S pull requests (pages 1 to 5) and TROPHY_CASE, all fetched 2026-10-18 from 14:20Z.
- Refile of the author's pull request #36, closed unmerged on 2026-10-14 in the bulk close of about thirty early pull requests during a handoff between sessions, not for a defect; the object file is the same scheme, re-checked from scratch by this panel.
- No downgrade triggers found.
