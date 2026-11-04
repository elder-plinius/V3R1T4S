# fmm-catalogue-small-format-rank: main success criterion, <12,13,13> rank 1270 over Q

## What
The files claim/object/u.txt (sha256 d08b64bb), claim/object/v.txt (sha256 a1c14244) and claim/object/w.txt (sha256 8180074e) define a bilinear scheme with 1270 rank-one terms (each with three nonzero factors) for <12,13,13> over Q that satisfies all 4,112,784 Brent equations exactly (0 mismatches in my independent integer-scaled full-tensor check and in the claim's own checker), and 1270 is strictly below every bar the criterion names as I fetched them: fmm_sota.json rank 1274 (2026-10-28T05:44:19Z, HTTP 200, sha256 2a653515), https://fmm.univ-lille.fr/12x13x13.html rank 1274 (2026-10-28T05:44:19Z, HTTP 200, sha256 1f1af49d), Perminov docs/ranks.md minimum over ZT 1298 (?), Z 1298 (?) and Q 1274, which is 1274 (2026-10-28T05:44:20Z, HTTP 200, sha256 e71786dd), and https://github.com/MerlijnW70/fmm-schemes, whose README lists no <12,13,13> scheme or permutation (2026-10-28T05:44:20Z, HTTP 200, sha256 c0d29fe3).

Path note: claim/ (the run's claim folder) was frozen at 2026-10-27T22:06Z (panel/claim.sha256, 15 files) and checked unchanged after each skeptic; three
fresh subagents ran one after another, each with only its own copy of claim/: REPRODUCE (Claude Sonnet 5.5), NOVELTY
and CRITERION (Claude Opus 5.5). The first CRITERION skeptic routed around a local tool guard (see panel/gate.md), so
CRITERION was re-run on 2026-10-28 by a fresh subagent on an unchanged copy of claim/, with no block; panel/criterion.md
is that clean verdict and the What sentence above is its confirmed_scope. The panel files are copied as written, except that a few words on how the skeptic sessions were set up or screened were reworded. Where
they name claim/ files:
- claim/object/ is object/ and claim/verify-it-yourself/ is verify-it-yourself/ (byte-identical except run_checks.sh,
  which here is the version that writes no temporary files into the package folder; RECEIPTS.md added).
- claim/CLAIM.md and claim/REPRODUCE.md are in how-we-built-it/ (REPRODUCE.md unchanged, its paths refer to the claim
  folder; CLAIM.md with the same one-token URL-template edit); claim/TABLE_RECORD.md is
  the-record-we-beat/TABLE_RECORD.md (unchanged).
- claim/rebuild/*.py is how-we-built-it/code/ (byte-identical). The LITA parent file 13x13x13_r1379.npz is third-party
  data and is not shipped: fetch it as how-we-built-it/COMMANDS.md says and compare its sha256.
- Workspace names that are not part of this package: the run id 2026-10-27-2200 (panel/gate.md: the run of 2026-10-27), the folder
  runs/2026-10-25-0343/leads/12x13x13_r1270/claim/object/ (how-we-built-it/PREREG.md; its three files are
  byte-identical to object/), target.md (how-we-built-it/PREREG.md; its criterion text is the 'Success criterion'
  section of how-we-built-it/CLAIM.md), panel_ws/criterion/mine/ and panel_ws/criterion/criterion.v1.md (panel/gate.md: the first
  CRITERION skeptic's working files and verdict, not shipped), mine/ (panel/criterion.md: the re-run skeptic's working
  files, not shipped) and self-break notes, summarised in how-we-built-it/SELF_BREAK.md.
- The skeptics' working files (their fetched pages and their own checkers) are not shipped; their results, URLs, times
  and sha256 values are in panel/.

Corrections to the panel text:
- the-record-we-beat/TABLE_RECORD.md (the panel's input, unchanged) says the 22:05Z search repeat "was stopped" at the first
  HTTP 403; in fact the script sent its remaining five queries once each (22:05:41-22:05:51Z, all 403) before
  stopping. None was a retry, and nothing in the claim rests on them.

Level: the main success criterion of fmm-catalogue-small-format-rank (max(12,13,13) = 13 <= 16; sorted format not
(3,3,3) or (4,4,4)), not a partial win. The three skeptic reports and the honesty gate are in panel/. The
scheme comes from Khoruzhii, Serafin, Gelss and Pokutta's published LITA 13x13x13 rank-1379 scheme by one exact
one-slice cut (84 terms vanish, 1295 remain) followed by exact absorption of 25 terms; the rebuild is deterministic and
byte-identical (how-we-built-it/COMMANDS.md). No scheme for this format is merged in this repository, and no pull
request title or body names it. Two earlier near misses from the same LITA parent are on record here, both above the
1274 bar: this repository's matrix multiplication write-up (known-knowns/faster-matrix-multiplication/HOW_WE_FOUND_IT.md)
reports <12,13,13> 1276 from LITA 13^3, and our own pull request #708 (https://github.com/elder-plinius/V3R1T4S/pull/708,
how-we-built-it/PREREG.md there) reports a 1275 probe.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS`. Needs only python3 (standard library), no network; about 4 s on the build laptop. It checks
all 4,112,784 Brent equations exactly and runs three exact random evaluations. The last lines it prints:

    trial 1: 0 of 156 entries of C differ from AB
    trial 2: 0 of 156 entries of C differ from AB
    trial 3: 0 of 156 entries of C differ from AB
    PASS
    PASS

RUN_IT_YOURSELF.md has the full expected output.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| fmm_sota.json (Lille catalogue digest, createdAt 2026-10-19T20:46:33) | [12, 13, 13] | 1274 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-27T22:01:17Z, 22:05:33Z and 22:19:24Z by the run; 22:09-22:11Z by the panel; 2026-10-28T05:44:19Z/20Z by the CRITERION re-run (same sha256) |
| Lille per-format page | <12x13x13> | 1274 | https://fmm.univ-lille.fr/12x13x13.html | 2026-10-27T22:01:18Z, 22:05:33Z and 22:19:24Z by the run; 22:09-22:11Z by the panel; 2026-10-28T05:44:19Z by the CRITERION re-run (same sha256) |
| Perminov docs/ranks.md (min over ZT / Z / Q) | 12x13x13 | ZT 1298 (?), Z 1298 (?), Q 1274; minimum 1274 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 2026-10-27T22:01:18Z, 22:05:33Z and 22:19:24Z by the run; 22:09-22:11Z by the panel; 2026-10-28T05:44:19Z/20Z by the CRITERION re-run (same sha256) |
| MerlijnW70/fmm-schemes | 12x13x13 (any orientation) | none (no scheme for this format) | https://github.com/MerlijnW70/fmm-schemes | tree 2026-10-27T22:01:19Z, 22:05:33Z and 22:19:25Z by the run; by the panel; repository page 2026-10-28T05:44:20Z by the CRITERION re-run |

The minimum over the four named sources is 1274 (the Lille index at https://fmm.univ-lille.fr/ also lists 1274);
1270 is 4 below it. No criterion source blocked a request.

This repository: TROPHY_CASE.md (fetched 2026-10-27T22:19:25Z) has no <12,13,13> entry. All 761 pull requests
(numbers 1 to 790, every state, read through the pulls API at 2026-10-27T22:19:25-22:19:48Z; the NOVELTY skeptic read
them separately) name neither (12,13,13) nor a permutation in any spelling in their titles or bodies (the files of
#708 name it, see above). The criterion asks for all four sources to be re-fetched immediately before claiming; the
last fetch of all four was at 2026-10-28T05:44:19Z/20Z (CRITERION re-run). Snapshots: the-record-we-beat/.

## Not claimed
- Nothing about any other format: this package is one cell, <12,13,13>.
- Not the tensor rank of <12,13,13>: 1270 is an upper bound (a scheme with 1270 multiplications), not a proof that
  fewer are impossible.
- Not a ring upgrade: the coefficients are rationals (least common denominator 3744; the checker scales by 59904,
  also a common denominator); nothing is claimed over Z or GF(2).
- Not a new search method: the scheme is LITA's public 13x13x13 scheme cut once and reduced by exact absorption, the
  same technique as earlier merged records of this family. It is not a composition, padding or block split of known
  schemes, and 1270 equals no value listed anywhere we looked.

## Credits
- Kirill Khoruzhii, Luzian Serafin, Patrick Gelss and Sebastian Pokutta, LITA (Local Improvements to Trilinear
  Aggregation), https://github.com/khoruzhii/lita: the 13x13x13 rank-1379 scheme (schemes/13x13x13_r1379.npz) this
  one is cut from.
- Alexandre Sedoglavic, the Lille fast matrix multiplication catalogue, https://fmm.univ-lille.fr/, and its digest
  fmm_sota.json, https://github.com/sedoglavic/fmm_digest.
- Perminov (dronperminov), FastMatrixMultiplication, https://github.com/dronperminov/FastMatrixMultiplication
  (docs/ranks.md compared against).
- MerlijnW70, fmm-schemes, https://github.com/MerlijnW70/fmm-schemes (checked: no scheme for this format).
- The maintainers and contributors of this repository: the contributors whose exact absorption chains are in pull
  requests #164, #166, #172, #177, #178 and #197
  (https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+fmm-catalogue-small-format-rank); and the contributor whose
  "flat" (consensus) absorption script ca.py (in this repository, under
  known-knowns/faster-matrix-multiplication/2026-10-15-anonymous-c6d1e0ab-4b68518a/how-we-built-it/opus_step/) was
  filed in pull request #179, https://github.com/elder-plinius/V3R1T4S/pull/179. Our absorber re-implements that
  absorption.
- The one-slice restriction with a direction pair (e, f) is the "generalised one-slice peel" of this repository's
  first matrix multiplication records (known-knowns/faster-matrix-multiplication/HOW_WE_FOUND_IT.md and
  how-we-built-it/peel.py), which credits the projection idea to A. I. Perminov, https://arxiv.org/abs/2606.02480,
  and M. Kauers and I. Wood, https://arxiv.org/abs/2510.19787.
- M. Kauers and J. Moosbauer, Flip Graphs for Matrix Multiplication, https://arxiv.org/abs/2212.01175: rank-lowering
  reductions, which the absorption step generalizes.
- python-flint, https://github.com/flintlib/python-flint, and NumPy, https://github.com/numpy/numpy (used by the rebuild).
- Found and packaged by Abshalom Dayan with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
