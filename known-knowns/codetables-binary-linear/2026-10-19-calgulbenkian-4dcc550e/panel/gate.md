# Honesty gate (codetables-binary-linear)

status: CONFIRMED_PARTIAL
confirmed_scope: Exact-rational Delsarte LP dual certificate (degree 3) that no (unrestricted or linear) code of length 148, size 4^7 and minimum distance at least 107 exists over an alphabet of size 4, so U(4,148,7) is at most 106 against the live table value 107; not implied by one-step propagation from the live neighbours I fetched; the target-scope reading for q = 4 follows the literal GF(q) text of the criterion (the target id and merged precedent are binary).

## Gate notes
- Object: object/lp_cert_q4_n148_k7_dub107.json, sha256 4dcc550e39a57e8eb177a9765ac46586d28ea8efb9d55ad873425904d3d010fa.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Scope: the bank target codetables-binary-linear is named for binary codes, but its success criterion and partial-win text are written for GF(q) and the live codetables.de table has this cell; no non-binary claim on this target has been merged yet, so the maintainer may rule on scope.
