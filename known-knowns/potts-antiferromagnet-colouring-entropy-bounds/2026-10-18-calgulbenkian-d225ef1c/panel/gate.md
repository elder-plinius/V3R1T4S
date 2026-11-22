# Honesty gate (potts-antiferromagnet-colouring-entropy-bounds)

status: CONFIRMED_SOLUTION
confirmed_scope: Provided the shipped vector satisfies y = C v (reproduce) and the literature search finds nothing as good (novelty), inequality (6) of Lundow and Markstrom with the even circumference 14 (k=7) and the proper 5-colouring cycle transfer matrix gives W_sq(5) <= 3.25040520587854968506, which is smaller than their printed upper bound 3.250407145038276 by about 1.939159726e-6, more than 1e-9.

## Gate notes
- Objects: 12 files under object/ (sha256 of each in the package folder's INDEX.csv and SHA256SUMS).
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Full success criterion met for this cell (one of the eight published bounds, upper side, strictly improved by more than the 1e-9 margin); not a partial win. One cell per claim.
- The criterion skeptic confirmed_scope is conditional on two checks it left to the other roles: y = C v at the claimed width (the reproduce skeptic recomputed C v with its own C program on the FULL transfer matrix of the definition, not the quotient, and matched the shipped y in every orbit, 0 mismatches) and the literature search (the novelty skeptic, pass). Both conditions are discharged.
- Citation: the inequality is equation (6) of Lundow and Markstrom (2008), Section 4, quoted by the criterion skeptic from the paper (open PDF fetched 2026-10-18T18:25:57Z, sha256 63dfff93). The package folder calls it "Theorem 2.2"; that label is wrong and the package must cite equation (6).
- Criterion run 1 failed only because the paper was not readable then (abstract only); it is kept as panel/criterion_run1.md. This was the one re-dispatch; the new run read the paper itself.
- Rounding: the rigorous bound rounded upward at 20 decimals is 3.25040520587854968506, equal to the claim.
- No downgrade triggers found.
