# Honesty gate (codetables-binary-linear)

status: CONFIRMED_PARTIAL
confirmed_scope: Exact-rational Delsarte LP dual certificate (degree 7) that no (unrestricted or linear) code of length 55, size 7^10 and minimum distance at least 40 exists over an alphabet of size 7, so U(7,55,10) is at most 39 against the live table value 40; not implied by one-step propagation from the live neighbours I fetched; the target-scope reading for q = 7 follows the literal GF(q) text of the criterion (the target id and merged precedent are binary).

## Gate notes
- Object: object/lp_cert_q7_n55_k10_dub40.json, sha256 01a7b3f11d0b35810510fb80338c6a7f25f4d7e44606ec85fdd7c670f5e89662.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Scope: the bank target codetables-binary-linear is named for binary codes, but its success criterion and partial-win text are written for GF(q) and the live codetables.de table has this cell; no non-binary claim on this target has been merged yet, so the maintainer may rule on scope.
