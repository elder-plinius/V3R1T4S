# Honesty gate (codetables-binary-linear)

status: CONFIRMED_SOLUTION
confirmed_scope: The object is a valid [163,11,104] code over GF(4) (rank 11, exact minimum distance 104 by full enumeration of all 4^11 - 1 messages, 7956 minimum-weight words) whose distance strictly exceeds the live lower bound 103 (upper 113); it is a refile of closed PR #101.

## Gate notes
- Object: object/win_q4_n163_k11_d104.json, sha256 28103164e334b8d35cdcb6e2d2dac8be21a26b82a9acaad2b53d835d25456b8f.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Edited 2026-11-17 at the maintainer's request on the pull request: the confirmed_scope sentence (here, in README.md and in panel/criterion.md) no longer carries the ruling note or the literal GF(q) clause, and the scope note and the bulk-close wording were removed. The verdicts and numbers are unchanged.
- This package refiles closed PR #101.
