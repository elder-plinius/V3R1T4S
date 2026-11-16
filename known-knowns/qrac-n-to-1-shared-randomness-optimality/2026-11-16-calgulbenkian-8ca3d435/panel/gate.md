# Honesty gate (qrac-n-to-1-shared-randomness-optimality)

status: CONFIRMED_SOLUTION
confirmed_scope: A re-runnable mpmath interval-arithmetic branch-and-bound certificate (43,476 dyadic leaves in canonical symmetry-reduced coordinates, which I re-checked numerically) shows that the maximum over four unit vectors in R^3 of 1/2 + (1/128) sum_x ||sum_i x_i v_i|| is at most 0.741481799559635, below 0.741482, which is criterion (a) for the 4-to-1 single-qubit QRAC with shared randomness; it says nothing about other n, and literature novelty was not assessed by me.

## Gate notes
- Object: object/certificate_qrac4.json, sha256 8ca3d435fdd22f906e7113aadfa38c09762836b6077d27a8b301a77e91847788.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- The reproduce skeptic re-checked all 43,476 leaves with its own outward-rounded integer-interval arithmetic; on 7,432 leaves its cruder bounds needed extra bisection (15,108 sub-boxes), and the largest bound it found was 0.7414819969, below the criterion's 0.741482. The certificate also closes under the package's own checker, which the skeptic re-ran after its verdict.
- The novelty skeptic found the (4,1) case still listed as open on the status page on 2026-11-16 and no earlier rigorous proof; the published optimum is numerical.
