# Honesty gate (hadamard-maxdet-records)

status: CONFIRMED_PARTIAL
confirmed_scope: This is an enumerated partial win p2 only: a frozen Gram target for order 49 (symmetric positive-definite integer G with diagonal 49, odd off-diagonals obeying the triple congruence, sqrt(det G)/2^48 = 768469522966111493289934848 above the Orrick record 96 * 12^23 = 635974777627126753067532288, an exact rational Q with Q Q^T = G, and 48 realised +-1 rows matching the leading block), not a +-1 matrix of order 49 and not a determinant record.

## Gate notes
- Object: object/G49_p2.json, sha256 cd7ea151cb23cea573fc617f983c2ce21a340dda94ec30baf82c4180c170e347.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Refile of the contributor's PR #68, closed unmerged on 2026-10-14 in the bulk close of about thirty early PRs during a handoff, not for a defect.
