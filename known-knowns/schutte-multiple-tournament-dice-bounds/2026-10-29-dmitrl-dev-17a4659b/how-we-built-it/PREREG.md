path key: this is a copy of the run's frozen file, unchanged below this line. `code/check_schutte.py` and `code/encode_schutte.py` are verify-it-yourself/check_schutte.py and verify-it-yourself/encode_schutte.py in this package (also how-we-built-it/encode_schutte.py); `code/encode_alt.py` is how-we-built-it/encode_alt.py; `BRIEF.md` is the run's brief (checker tests and the calibration table), not shipped; "run 2026-10-28-1153" is the contributor's local run label.

# PREREG: schutte-multiple-tournament-dice-bounds (run 2026-10-28-1153)

frozen: 2026-10-28T12:15:16Z (date -u), before any search output on the target cells (only the checker tests and the encoder calibration on
starred cells of BRIEF.md ran before).

## Criterion (verbatim from the bank, repo 8846324)
Give explicit adjacency matrices proving f(2,5)<=13 or f(3,6)<=12, with n>=k+1, and strictly below the best composition of all published constructions available when the claim is checked. The cited-source composition bars are 14 and 13; a later published improvement or its compositions can lower them. Unmerged pull-request values are not bars. Report whether the submitted object is itself a composition, and cite every ingredient if it is. One vertex fewer suffices because orders and the verification are exact. An exact value proved by an UNSAT certificate is partial win p1.

## Partial win (verbatim)
- p1: An exact value: an UNSAT certificate (DRAT or LRAT checked by a formally verified checker such as cake_lpr) for a CNF encoding of 'two tournaments on 13 vertices with every 5-subset dominated' (proving f(2,5) = 14) or 'three tournaments on 12 vertices with every 6-subset dominated' (proving f(3,6) = 13), with symmetry breaking proved sound and the encoding's correctness argued in a short note that a skeptic checks against Definition 2.2.

## Statistic and decision rule
Solution claim (all must hold):
1. Explicit adjacency matrices for (m,k,n) = (2,5,13) or (3,6,12) (or a smaller n for the same (m,k)), A[t][i][j] = 1
   meaning i -> j.
2. code/check_schutte.py (stdlib, written from Definition 2.1/2.2, tested in BRIEF.md) prints PASS: every matrix is a
   tournament and every k-subset has one tournament and one vertex outside it beating all of it.
3. A second checker written separately (numpy bitmask implementation, different data layout) agrees.
4. The report says whether the object is a composition in the sense of Proposition 2.3 (a split V1, V2 with each
   tournament sending one block entirely to the other) and, if so, cites its ingredients.
5. Literature recheck (status source and arXiv search) right before any claim.

Partial win p1: UNSAT of the full CNF (code/encode_schutte.py, no assumptions) or of every cube of a split whose
soundness is argued in the encoder's docstring, with a DRAT/LRAT proof per formula checked by cake_lpr. If cake_lpr
cannot be run on this laptop (arm64), an UNSAT result checked only by drat-trim/lrat-check is reported as such and is
NOT claimed as p1.

Outcome NOTHING if no object passes 1-3 and no p1 certificate exists when the budget ends; the report then gives the
lenses, the searched spaces and the solver logs (time caps, results), as negative-result information.

null_test: not needed because the claim is an explicit finite object (adjacency matrices) checked by a deterministic
exhaustive checker against an integer bar; there is no search statistic or "beats chance" component.

## Search plan (order)
1. circulant lens: all pairs of circulant tournaments on Z13 for (2,5,13).
2. sat lens: full CNF with the dom0 unit clauses for (2,5,13) and (3,6,12) under kissat and CaDiCaL, 60 minutes per call.
3. anneal lens: local search (C) on tuples, random seeds and composition-minus-vertex seeds, both cells.
4. structured SAT near the composition, then the maximum-out-degree cube split with proof logging if time remains.

## Caps
At most 2 concurrent solver or search processes, about 1.5 GB resident memory each, 60 minutes per call, total about
3.5 hours of wall time; free memory checked before each launch. Claims stay PROMISING unless the human approves a
fresh-context panel.
