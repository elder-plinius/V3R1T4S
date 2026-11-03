# No Game of Life orphan fits in a 5 x 8 box: two independent SAT encodings, 32 cubes each, every cube LRAT-checked (bank target life-smaller-orphan, partial win p1)

> Partial win p1 only. The target's full success criterion (an orphan with both sides >= 5 and area below Eker's
> 12 x 8 = 96) is NOT met, and p2 is not claimed.

## What
Confirmed scope (from panel/gate.md, verbatim): verified encoding soundness (UNSAT <=> no (h+2)x(w+2) predecessor of an h x w target, B3/S23 masks 8/12), independence, 32-cube cover and all 5x8 `.res` `c_VERIFIED` rows, and rebuilt CaDiCaL+lrat-check on 3x3/4x4 plus SAT/UNSAT polarity on tiny brute-forced sizes; did not re-solve 5x8, run kissat, or perform the human LifeWiki novelty gate.

In plain words: an orphan (Garden of Eden pattern) is a pattern that no pattern can turn into after one Life
generation. We show that every pattern on a 5 x 8 box (and so on every 5 x w box with w <= 8) has a predecessor on
the surrounding 7 x 10 box. Two separately written CNF encodings of "this 5 x 8 target has a predecessor" (tcnf, a
column-transfer encoding, and mcnf, a meet-in-the-middle left/right halves encoding) were each split into 32 cubes,
one per value of target column 4 (all 2^5 values, so the cubes cover every case; a clause-subset check confirms each
cube is the full formula plus its five unit clauses). All 64 cubes are UNSAT under CaDiCaL with LRAT proofs accepted
by lrat-check (from the drat-trim repository). 5 x 7 is certified the same way in both encodings, and tcnf also
certifies 5 x 4 and 5 x 6 (5 x 2, 5 x 3 and 5 x 5 by unsplit DRAT in an earlier run).

object/certificate.tsv is the result table (one row per cube: encoding, box, cube column and value, solver exit,
proof check, clause count, times, proof size). The proofs themselves (hundreds of MB each) were checked at run time
and not kept; RUN_IT_YOURSELF.md says how to regenerate and check any cube.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs sh, sha256sum and python3). Expected last line:
`PASS`. About 2-5 s on a laptop. It checks the object's digests, that each encoding's split covers all 32 values for
5 x 7 and 5 x 8 with UNSAT and c_VERIFIED on every cube, and re-derives the orphan definition with an independent
Python column-transfer automaton against control rules with known orphan widths. Re-solving a 5 x 8 cube takes about
5-20 CPU-minutes and up to 3 GB RAM per cube (see RUN_IT_YOURSELF.md).

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| LifeWiki, Garden of Eden (human-read in a browser, 2026-11-01) | smallest proven-empty box / height-5 record | no GoE in 7x7 (Beer); no height-4 orphans (Wade 2023); shortest known height-5 orphan 5 x 45 (Eker); nothing on 5 x 8 | https://conwaylife.com/wiki/Garden_of_Eden | 2026-11-02T02:17Z (human check) |
| Wikipedia, Garden of Eden (cellular automaton) | smallest known orphan | 8 x 12 (Eker) | https://en.wikipedia.org/wiki/Garden_of_Eden_(cellular_automaton) | 2026-10-27T21:22Z |
| Beer 2023, Complex Systems 32 | 7 x 7 | no orphan | https://arxiv.org/abs/2210.07837 | 2026-11-01 |

Details: the-record-we-beat/RECORD.md and panel/novelty.md.

## Not claimed
- No orphan smaller than 12 x 8 is claimed or found; the main success criterion is not met.
- kissat was not run on the 5 x 8 instances (the main criterion (2) asks for it; p1 does not).
- Nothing about heights 6 and up, or 5 x w for w >= 9.
- The proofs were not kept; the claim rests on the run-time lrat-check of every cube, reviewer and gate re-solves of
  sample cubes (5 x 7 v23 and v11; 5 x 8 v21 in both encodings), and the reproducible encoders.

## Credits
- Steven Eker (12 x 8 record, no orphans of height <= 3, 5 x 45 orphan), via https://conwaylife.com/wiki/Garden_of_Eden
- Andrew J. Wade (no height-4 orphans, 2023): https://conwaylife.com/forums/viewtopic.php?t=6042
- Randall D. Beer (no 7 x 7 orphan, 2023): https://arxiv.org/abs/2210.07837
- Hartman, Heule, Kwekkeboom, Noels (6 x 6, symmetry, 2013): https://doi.org/10.37236/2611
- CaDiCaL (Armin Biere): https://github.com/arminbiere/cadical ; drat-trim and lrat-check (Marijn Heule et al.): https://github.com/marijnheule/drat-trim
- Contributor: anonymous (V3R1T4S kit).
