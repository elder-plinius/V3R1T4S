# Honesty gate (codetables-binary-linear)

status: CONFIRMED_SOLUTION
confirmed_scope: The object is a valid [163,11,104] code over GF(4) (rank 11, exact minimum distance 104 by full enumeration of all 4^11 - 1 messages, 7956 minimum-weight words) whose distance strictly exceeds the live lower bound 103 (upper 113); it is a refile of closed PR #101 (not a prior record by ruling R1), under the literal GF(q) reading of the criterion.

## Gate notes
- Object: object/win_q4_n163_k11_d104.json, sha256 28103164e334b8d35cdcb6e2d2dac8be21a26b82a9acaad2b53d835d25456b8f.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Scope: the bank target codetables-binary-linear is named for binary codes, but its success criterion and partial-win text are written for GF(q) and the live codetables.de table has this cell; no non-binary claim on this target has been merged yet, so the maintainer may rule on scope.
- Refile of the contributor's PR #101, closed unmerged on 2026-10-14 in the bulk close of about thirty early PRs during a handoff, not for a defect.
