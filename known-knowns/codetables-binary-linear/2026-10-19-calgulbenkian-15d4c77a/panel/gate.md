# Honesty gate (codetables-binary-linear)

status: CONFIRMED_PARTIAL
confirmed_scope: Exact-rational Delsarte LP dual certificate (degree 3) that no (unrestricted or linear) code of length 67, size 8^5 and minimum distance at least 56 exists over an alphabet of size 8, so U(8,67,5) is at most 55 against the live table value 56; not implied by one-step propagation from the live neighbours I fetched; the target-scope reading for q = 8 follows the literal GF(q) text of the criterion (the target id and merged precedent are binary).

## Gate notes
- Object: object/lp_cert_q8_n67_k5_dub56.json, sha256 15d4c77a8595afddc79a2c9a96a7d24d7e9152fbb10258401b7def9dd6abfebb.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Scope: the bank target codetables-binary-linear is named for binary codes, but its success criterion and partial-win text are written for GF(q) and the live codetables.de table has this cell; no non-binary claim on this target has been merged yet, so the maintainer may rule on scope.
