# Honesty gate (codetables-qubit-upper-bounds-n101-256)

status: CONFIRMED_SOLUTION
confirmed_scope: Exact integer Farkas certificate (quantum weight-enumerator LP with shadow constraints, no purity assumption) that no qubit stabilizer code [[124,3,d]] with d at least 41 exists, so the upper bound for [[124,3]] is at most 40 against the live value 41 fetched 2026-10-19; the value is below the propagation closure of the live table plus the 56 listed pull-request values plus the other claimed cells.

## Gate notes
- Object: object/cert_124_3_41_sh.json, sha256 44fa84d905d87798ace65c7848fff9c5d5c8edf894e5166e707ce3826564bff3.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
