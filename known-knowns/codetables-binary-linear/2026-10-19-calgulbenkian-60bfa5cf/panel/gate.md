# Honesty gate (codetables-binary-linear)

status: CONFIRMED_SOLUTION
confirmed_scope: The object is a valid [160,11,102] code over GF(4) (rank 11, exact minimum distance 102 by full enumeration of all 4^11 - 1 messages, 2958 minimum-weight words) whose distance strictly exceeds the live lower bound 101 (upper 111) and is not obtainable from the live neighbours or by puncturing the co-filed [163,11,104] code, under the literal GF(q) reading of the criterion.

## Gate notes
- Object: object/new_win_q4_n160_k11_d102.json, sha256 60bfa5cf703ab1750aabbe57c1bd8f9793fed9008adcfefde99cc1a6836f8474.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Scope: the bank target codetables-binary-linear is named for binary codes, but its success criterion and partial-win text are written for GF(q) and the live codetables.de table has this cell; no non-binary claim on this target has been merged yet, so the maintainer may rule on scope.
