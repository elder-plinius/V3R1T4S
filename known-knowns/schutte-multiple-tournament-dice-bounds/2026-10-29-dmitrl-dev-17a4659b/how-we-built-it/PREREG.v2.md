path key: this is a copy of the run's frozen file, unchanged below this line. `code/check_schutte.py` and `code/encode_schutte.py` are verify-it-yourself/check_schutte.py and verify-it-yourself/encode_schutte.py in this package (also how-we-built-it/encode_schutte.py); `code/encode_alt.py` is how-we-built-it/encode_alt.py; `BRIEF.md` is the run's brief (checker tests and the calibration table), not shipped; "run 2026-10-28-1153" is the contributor's local run label.

# PREREG.v2: schutte-multiple-tournament-dice-bounds (run 2026-10-28-1153)

frozen: 2026-10-28T13:23:37Z (date -u). Supersedes the caps and the search plan of PREREG.md (frozen 2026-10-28T12:15:16Z); the
criterion, the partial win, the decision rule (items 1-5 and the p1 paragraph) and the null_test line of PREREG.md are
unchanged.

## Why a new version
- Results seen before this file: for (2,5,13) every maximum-out-degree cube is UNSAT (CaDiCaL), the single 'global' CNF
  is UNSAT with an LRAT proof that cake_lpr verified, and a second encoding (code/encode_alt.py) is UNSAT under kissat.
  For (3,6,12) no result yet: the D=11 cube was stopped after about 20 minutes; the D=10..6 cubes are running.
- The symmetry-breaking variants 'global2' and 'global3' (code/encode_schutte.py docstring, soundness argued there) were
  added after the (2,5,13) cube results and before any (3,6,12) result; they were tested on known cells (SAT side and
  UNSAT side) before use on (3,6,12).

## Changed caps and plan
- At most 2 concurrent solver or checker processes; free memory checked before each launch; cake_lpr heap set so its
  resident size stays near 1.5 GB.
- Per solver call: up to 4 hours (was 60 minutes); total wall time of the run: up to 8 hours from the start (11:53Z).
- (3,6,12): one CNF with --sb global3 under CaDiCaL with a text LRAT proof streamed through zstd; if UNSAT, cake_lpr on
  the decompressed stream. The running D=10..6 cubes continue to their caps as a cross-check.
- (2,5,13): the 'global' proof stays the p1 candidate; a smaller 'global3' proof may be produced for packaging.
- A SAT answer for (3,6,12) is a solution claim only under PREREG.md items 1-5 (both checkers PASS, composition
  check, literature recheck).
