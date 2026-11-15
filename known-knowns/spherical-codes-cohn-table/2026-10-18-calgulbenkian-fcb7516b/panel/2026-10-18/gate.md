# Honesty gate (spherical-codes-cohn-table)

status: CONFIRMED_PARTIAL
confirmed_scope: In dimension 7, 24 distinct rows (N = 177, 178, 204, 212, 215, 308 to 310, 312 to 318, 322, 323, 325, 362, 364 to 368) that the saved index rows label 'needs more optimization' each have a saved object whose 50-digit maximum normalised inner product is lower than the saved /plain cosine by at least 3.19e-9 (largest 1.377e-4 at N=308), which meets partial win p2 and no wider claim.

## Gate notes
- Objects: 24 files under object/ (sha256 of each in the package folder's INDEX.csv and SHA256SUMS).
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the package folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Partial win p2 only: 24 rows in dimension 7, all labelled "needs more optimization" in the live index, each improved by at least 1e-10 (smallest 3.19e-9 at N = 362, largest 1.377e-4 at N = 308); the threshold is 20 rows. These rows are flagged unconverged by the table, so this is never a record claim.
- Reproduce: own 50-digit mpmath check over all pairs for every row. Novelty: live table re-fetched 2026-10-18T17:50Z, unchanged.
- No downgrade triggers found.
