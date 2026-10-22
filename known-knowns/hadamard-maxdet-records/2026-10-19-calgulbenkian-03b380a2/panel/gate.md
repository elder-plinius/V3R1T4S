# Honesty gate (hadamard-maxdet-records)

status: CONFIRMED_PARTIAL
confirmed_scope: This is an enumerated partial win p2 only: a frozen Gram target for order 81 (symmetric positive-definite integer G with diagonal 81, odd off-diagonals obeying the triple congruence, sqrt(det G)/2^80 = 138538465099776000000000000000000000000000000000000000 above the Orrick record 196 * 20^39 = 107752139522048000000000000000000000000000000000000000, an exact rational Q with Q Q^T = G, and 80 realised +-1 rows matching the leading block), not a +-1 matrix of order 81 and not a determinant record.

## Gate notes
- Object: object/G81_p2.json, sha256 03b380a2074785deac39cb19b68c0853cd52ea469f7b848600cc756df42c8992.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Refile of the contributor's PR #69, closed unmerged on 2026-10-14 in the bulk close of about thirty early PRs during a handoff, not for a defect.
