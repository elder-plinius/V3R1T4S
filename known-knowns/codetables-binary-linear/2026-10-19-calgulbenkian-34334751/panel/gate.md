# Honesty gate (codetables-binary-linear)

status: CONFIRMED_PARTIAL
confirmed_scope: Exact-rational Delsarte LP dual certificate (degree 5) that no (unrestricted or linear) code of length 161, size 2^17 and minimum distance at least 72 exists over an alphabet of size 2, so U(2,161,17) is at most 71 against the live table value 72; not implied by one-step propagation from the live neighbours I fetched.

## Gate notes
- Object: object/lp_cert_q2_n161_k17_dub72.json, sha256 343347514df7b4c3233d7f6878fcd82ce8ad4c82f0f12016789bc8fb98ecbf9a.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- Edited 2026-11-17 at the maintainer's request on the pull request: the q = 2 scope clause was removed from confirmed_scope (the sentence is now identical in README.md, here and in criterion.md); references to open pull requests and to other cells were removed from criterion.md and novelty.md. The verdicts and numbers are unchanged.
- Edited 2026-11-17 at the maintainer's request on the pull request: removed the snapshot of pull requests and the other-folder, arXiv-query and open-pull-request lines from novelty.md, criterion.md and reproduce.md, and retitled one heading in novelty.md. The verdicts, numbers and the confirmed_scope sentence are unchanged.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
