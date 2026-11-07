# PREREG (frozen 2026-10-25T05:54:46Z, from date -u, before this run's claim folder exists)

Honest note on timing: the (6, 256) object, runs/2026-10-24-1639/attempts/polish/out/deep/deep_6_256.txt, was made
by run 2026-10-24-1639 (interior-point SLP polish of the code Pavlos Moros posted for (6, 256); its log
deep_6_256.log ends with the trust radius at 2.8e-12, i.e. at a local stationary point) and was float-screened by
later runs and by this folder's scout read (data/queue_scout.out: 3.325e-5 below the row by double-precision max).
No exact checker has been run on it in this folder yet. The scout read (05:50:23Z), the propagated-bar screen
(already-settled lens), the posted-code control and the literature reads are status reads. The object is copied
unchanged into attempts/claim-object/result/ and frozen there (sha256) before the claim folder is built.

## Criterion (verbatim from bank/targets.json, as in target.md)

Success means N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates given to >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs more optimization' (improving an entry the table itself flags as unconverged is partial win p2, never a claim), AND the row is not superseded by a newer arXiv result for the same (d, N) (search arXiv for 'spherical code' / 'Tammes' and N), AND the result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 the claim belongs to the bank target kissing-number-low-dim and is not counted here). Uploading to /upload-code is an external submission and is never done without explicit permission from the human; the claim is for the verified code.

Partial wins p1, p2, p3: verbatim in target.md (lines starting "- **p1**", "- **p2**", "- **p3**").

## Statistic and checkers

- c* = max over pairs i < j of <x_i, x_j> / (|x_i| |x_j|), computed from the saved coordinate file by
  checker/check_mp.py (mpmath, 50 significant digits) and checker/check_exact.py (exact rationals: decides
  c* < bar by comparing squared quantities with signs, no floating point). Both must print "beats" for a claim.
  Both are re-tested in this folder on a known negative (the posted (6, 256) code against its own table value), a
  seeded flaw and a known positive before the claim object is judged.
- The bar for (d, N) is the 12-decimal cosine of the (d, N) row in the live /plain fetched at the claim moment
  (checker/fetch_live.sh claim<k>, as the very last step after the last text edit; render and check in one step),
  with the HTML row checked for no '&ast;' and no "needs more optimization".

## Thresholds

- Claim (full criterion, one cell, (6, 256)): c* <= bar - 1e-10 by both checkers; row unstarred, unlabelled and
  present in /plain at the claim-moment fetch; no arXiv result of the last 24 months for (6, 256) at or below
  c* + 1e-10 (arXiv API searches plus the per-instance data of every arXiv paper that covers the cell, read, not
  inferred); propagated bar min over listed d' <= 6 and N' >= 256 (live /plain, live index, the three 2610.19988
  tables, ImprovEvolve's benchmark rows) above c* by >= 1e-10; the kissing clause cannot apply (d = 6 is outside
  9..23). Not in an open pull request of the repository and not in a sibling workspace's runs/ or outbox/.
- If the (6, 256) row changes value, gains a label or a star, or a propagated-region row drops to or below the row
  between the scout read and the claim moment, the claim stops (status NOTHING for this cell) and is re-judged in a
  new folder if still alive.
- Lens outputs for other cells are screens, not claims. d6-polish: a labelled d = 6 row counts toward a future p2
  batch only if float64 c* is below the row by >= 1e-9 at the read the lens used, the row is labelled, unstarred and
  in /plain, not in an open PR, and below the propagated bar over d' <= 6 and N' >= N; the batch itself is judged
  in its own folder under its own PREREG.

null_test: not needed because every result here is an explicit coordinate file judged by two deterministic checkers against a table value (no search statistic, key, period or "beats chance" claim).

## Kill rules for lenses

A lens line dies when three seeds or three cells give no gain >= 1e-9 over the table, or when its structural
premise is shown false. The (6, 256) claim is dropped (kept as a lead) if its claim moment cannot happen by
2026-10-25T08:30Z.
