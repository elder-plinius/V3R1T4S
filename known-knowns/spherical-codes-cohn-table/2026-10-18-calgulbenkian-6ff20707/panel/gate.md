# Honesty gate (spherical-codes-cohn-table)

status: CONFIRMED_SOLUTION
confirmed_scope: For the single row (d=28, N=59) the saved object has maximum normalised inner product 0.039154189772, which is lower than the saved live /plain cosine 0.039154654978 by 4.65205e-7, at least 1e-10, on an index row with no ast mark and no 'needs more optimization' text and outside the kissing-number range, as fetched 2026-10-18T17:39Z.

## Gate notes
- Object: object/28x59.txt, sha256 6ff207079c8818db282ab0d1f5f5dbf5c71f16733dad09cad4e827cc820b1fcb.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Full success criterion met for this one (d, N) row; not a partial win. One cell per claim.
- Reproduce: own 50-digit mpmath check over all pairs, no sampling. Novelty: live /plain and index re-fetched 2026-10-18T17:50Z, unchanged from the claim record; V3R1T4S pull requests pages 1 to 5, TROPHY_CASE, arXiv.
- Residual named by the novelty skeptic: the Zenodo data set behind arXiv:2610.19988 (Vahteristo) was not fetched for size; the live table postdates the paper and cites it, so it is not a downgrade.
- No downgrade triggers found.
