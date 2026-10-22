# Honesty gate (codetables-binary-linear)

status: CONFIRMED_PARTIAL
confirmed_scope: Exact-rational Delsarte LP dual certificate (degree 3) that no (unrestricted or linear) code of length 153, size 4^7 and minimum distance at least 111 exists over an alphabet of size 4, so U(4,153,7) is at most 110 against the live table value 111; not implied by one-step propagation from the live neighbours I fetched; the target-scope reading for q = 4 follows the literal GF(q) text of the criterion (the target id and merged precedent are binary).

## Gate notes
- Object: object/lp_cert_q4_n153_k7_dub111.json, sha256 8b17a05d526aa1c9c9a60a151ddcbddf0c59d09fd98333cc798c1ed6b23bd8e2.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Scope: the bank target codetables-binary-linear is named for binary codes, but its success criterion and partial-win text are written for GF(q) and the live codetables.de table has this cell; no non-binary claim on this target has been merged yet, so the maintainer may rule on scope.
