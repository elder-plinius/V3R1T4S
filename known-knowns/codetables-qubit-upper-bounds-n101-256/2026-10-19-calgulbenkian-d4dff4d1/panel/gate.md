# Honesty gate (codetables-qubit-upper-bounds-n101-256)

status: CONFIRMED_SOLUTION
confirmed_scope: Exact integer Farkas certificate (quantum weight-enumerator LP with shadow constraints, no purity assumption) that no qubit stabilizer code [[111,3,d]] with d at least 37 exists, so the upper bound for [[111,3]] is at most 36 against the live value 37 fetched 2026-10-19; the value is below the propagation closure of the live table plus the 56 listed pull-request values plus the other claimed cells.

## Gate notes
- Object: object/cert_111_3_37_sh.json, sha256 d4dff4d15478be83f0f3913f2d3cf3be348a48bc93e5970bab708cf9440b096e.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- On 2026-11-17, at the maintainer's request on the pull request, the three reports were edited (dated notes in each): plain statements replace the open-question labels and the open-questions heading. Verdicts, numbers and the confirmed_scope sentence are unchanged.
