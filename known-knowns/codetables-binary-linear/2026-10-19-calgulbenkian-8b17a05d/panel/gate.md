# Honesty gate (codetables-binary-linear)
[Edited 2026-11-19 at the maintainer's request on the pull request: the scope clause about the target id and precedent was removed from the confirmed_scope sentence, and the Scope note was deleted. The checks, numbers and verdict are unchanged; the confirmed_scope sentence lost that clause.]

status: CONFIRMED_PARTIAL
confirmed_scope: Exact-rational Delsarte LP dual certificate (degree 3) that no (unrestricted or linear) code of length 153, size 4^7 and minimum distance at least 111 exists over an alphabet of size 4, so U(4,153,7) is at most 110 against the live table value 111; not implied by one-step propagation from the live neighbours I fetched.

## Gate notes
- Object: object/lp_cert_q4_n153_k7_dub111.json, sha256 8b17a05d526aa1c9c9a60a151ddcbddf0c59d09fd98333cc798c1ed6b23bd8e2.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- 2026-11-19, at the maintainer's request on the pull request: the scope clause about the binary target id and precedent was removed from the confirmed_scope sentence here, in README.md and in panel/criterion.md, because GF(4) results on this target are settled; the Scope note was deleted for the same reason. The verdicts and numbers are unchanged. The sentence otherwise reads as before.
