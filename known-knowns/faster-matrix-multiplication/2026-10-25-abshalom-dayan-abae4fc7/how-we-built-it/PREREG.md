# PREREG: fmm-catalogue-small-format-rank

(Package copy of the run's PREREG.md, unchanged except for removing the run id from the title and a workspace name
from the p1/p2 line, and one edit: the per-format URL template in the criterion is
written with braces, fmm.univ-lille.fr/{n}x{m}x{p}.html, because the package checker reads the angle-bracket form
as an unfilled placeholder. Note: paths of the form attempts/... in the text name files of the run's private
workspace, which are not shipped; the run's own two exact checkers named there are summarised in SELF_BREAK.md,
and the checkers shipped for you are in verify-it-yourself/.)

Written 2026-10-25T03:51:33Z, before any scored attack output of this run exists (the only output so far is the
flat-absorption control on the merged 2176 -> 2105 edge, attempts/constructor/out/control_flat_v1.log, which reproduces
a public value and is not a candidate).

## Criterion (verbatim, from target.md / bank)
See target.md: an explicit bilinear scheme for <n,m,p> with max(n,m,p) <= 16, sorted format not (3,3,3) or (4,4,4),
whose number of rank-one terms r is strictly less than ALL of: the fmm_sota.json rank for the sorted format, the rank
on https://fmm.univ-lille.fr/{n}x{m}x{p}.html, the minimum over the ZT/Z/Q columns of Perminov's docs/ranks.md, and the
lowest rank in MerlijnW70/fmm-schemes (all re-fetched live immediately before claiming), verified in exact arithmetic
over the ring it claims.

## Statistic and checker
- r = number of rank-one terms with all three factors nonzero, after merging exact duplicates.
- Validity: every Brent equation of the format holds exactly over Q. Two independent exact checkers must both PASS on
  the saved JSON: attempts/evaluator-first/code/check_stdlib.py (exact integer expansion after clearing denominators)
  and attempts/evaluator-first/code/check_flint.py (exact fmpz slice products), re-tested this run on a known positive
  (a merged record) and planted negatives before use.

## Thresholds
- Main win: r < bar(cell), bar(cell) = min(fmm_sota.json, Lille per-format page, Perminov docs/ranks.md min over
  ZT/Z/Q, MerlijnW70), fetched live before the claim, AND r below every value already public in this repo
  (TROPHY_CASE, known-knowns, every open or closed pull request) and the literature (a tie is not a record). Bars at
  scout time are in scout.md.
- p1 and p2 are not pursued this run (p1 band mined by a sibling run).
- One cell per claim. If several cells are beaten, the claim is the one with the most negative margin r - bar; ties
  broken by smaller max dimension. Others become separate leads.

null_test: not needed because every claim here is an explicit object checked by two deterministic exact checkers
against a table value; no search statistic or chance model is involved.
