# Honesty gate (codetables-binary-linear)

status: CONFIRMED_PARTIAL
confirmed_scope: Exact-rational Delsarte LP dual certificate (degree 7) that no (unrestricted or linear) code of length 66, size 5^11 and minimum distance at least 45 exists over an alphabet of size 5, so U(5,66,11) is at most 44 against the live table value 45; not implied by one-step propagation from the live neighbours I fetched; the target-scope reading for q = 5 follows the literal GF(q) text of the criterion (the target id and merged precedent are binary).

## Gate notes
- Object: object/lp_cert_q5_n66_k11_dub45.json, sha256 b41542d739724fe3b0e96093fb2aee3bee570bc59b5e80212aa97bbd16fc7584.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Scope: the bank target codetables-binary-linear is named for binary codes, but its success criterion and partial-win text are written for GF(q) and the live codetables.de table has this cell; no non-binary claim on this target has been merged yet, so the maintainer may rule on scope.
