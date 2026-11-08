# Honesty gate (codetables-binary-linear)

status: CONFIRMED_SOLUTION
confirmed_scope: The object is a valid [157,10,102] code over GF(4) (rank 10, exact minimum distance 102 by full enumeration of all 4^10 - 1 messages, 5304 minimum-weight words) whose distance strictly exceeds the live lower bound 101 (upper 110) and is not implied by the live neighbours.

## Gate notes
- Object: object/new_win_q4_n157_k10_d102.json, sha256 40b6f0180e9248f1b86c69053b8c5e200f01156b917179cc619c63f659469d81.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence; on 2026-11-08, at the maintainer's request on the pull request, its clause about the two unmerged codes of the same batch and its scope clause were removed (GF(4) results on this target are settled). The numbers and checks are unchanged.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
