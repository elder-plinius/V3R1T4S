# Honesty gate (codetables-qubit-upper-bounds-n101-256)

status: CONFIRMED_SOLUTION
confirmed_scope: Exact integer Farkas certificate (quantum weight-enumerator LP with shadow constraints, no purity assumption) that no qubit stabilizer code [[119,5,d]] with d at least 39 exists, so the upper bound for [[119,5]] is at most 38 against the live value 39 fetched 2026-10-19; the value is below the propagation closure of the live table plus the 56 listed pull-request values plus the other claimed cells.

## Gate notes
- Object: object/cert_119_5_39_sh.json, sha256 67b6a68a5b0b71bf4b18453b38e0119dd4be72c9e789897bbc14d7da5095c071.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Edited 2026-11-23 at the maintainer's request on the pull request: dated notes and plain wording in the three panel reports (open-question labels replaced, binary-linear material and pull-request numbers removed, the criterion report's one fetched page and its time named, the reproduce report's hash-list count corrected from 13 to 27); README.md and the-record-we-beat/README.md were edited as well. Verdicts and all other numbers are unchanged, and so is the confirmed_scope sentence.
