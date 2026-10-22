# Honesty gate (codetables-qubit-upper-bounds-n101-256)

status: CONFIRMED_SOLUTION
confirmed_scope: Exact integer Farkas certificate (quantum weight-enumerator LP with shadow constraints, no purity assumption) that no qubit stabilizer code [[112,4,d]] with d at least 37 exists, so the upper bound for [[112,4]] is at most 36 against the live value 37 fetched 2026-10-19; the value is below the propagation closure of the live table plus the 56 listed pull-request values plus the other claimed cells.

## Gate notes
- Object: object/cert_112_4_37_sh.json, sha256 b8885ffcf45b3445a6e86ae60146ee6879e8c83b01f98456a533642db635be84.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
