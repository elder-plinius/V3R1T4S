# fmm-catalogue-small-format-rank: main success criterion, <14,15,15> rank 1836 over Q

## What
The files object/u.txt (sha256 74ccb3a6…), object/v.txt (sha256 0f86e47a…) and object/w.txt (sha256 cac452b5…) define an explicit bilinear scheme for the format <14,15,15> with exactly 1836 rank-one terms (no zero factors, no mergeable duplicates) that satisfies all 9,922,500 Brent equations exactly over Q (common denominator 54400), and 1836 is strictly below every bar the criterion names as re-fetched at 2026-10-26T22:25Z (fmm_sota.json 1848, fmm.univ-lille.fr/14x15x15.html 1890, Perminov ranks.md min of ZT 1894 / Z 1892 / Q 1848 = 1848, MerlijnW70/fmm-schemes no entry for this format or any permutation).

Path note: claim/ (the run's claim folder) was frozen at 2026-10-26T22:08:55Z (panel/claim.sha256, 15 files); three fresh subagents ran one after
another, each with only its own copy of claim/: REPRODUCE (Claude Sonnet 5.5), NOVELTY and CRITERION (Claude Opus 5.5).
The panel files are copied as written, except that a few words on how the skeptic sessions were set up or screened were reworded. Where they name claim/ files:
- claim/object/ is object/ and claim/verify-it-yourself/ is verify-it-yourself/ (byte-identical except run_checks.sh, which was changed after the
  panel only so that it no longer writes temporary files into the package folder; RECEIPTS.md added).
- Workspace names that are not part of this package: the run id 2026-10-26-2200 (panel/gate.md: the run of
  2026-10-26), the folder runs/2026-10-25-0343/leads/14x15x15_r1836/stage/object/
  (how-we-built-it/PREREG.md; its three files are byte-identical to object/), target.md (how-we-built-it/PREREG.md; its
  criterion text is the 'Success criterion' section of how-we-built-it/CLAIM.md) and the run report's 'Needs you' list
  (panel/gate.md).
- claim/CLAIM.md, claim/REPRODUCE.md are in how-we-built-it/. REPRODUCE.md is unchanged (its paths refer to the claim
  folder); CLAIM.md has one edit: the criterion's Lille URL template is written {n}x{m}x{p} instead of with angle
  brackets, because the package checker reads angle-bracket names as unfilled placeholders (so its sha256 differs from
  panel/claim.sha256); claim/TABLE_RECORD.md is the-record-we-beat/TABLE_RECORD.md (unchanged).
- claim/rebuild/*.py is how-we-built-it/code/ (byte-identical). The LITA parent file 15x15x15_r1977.npz is third-party
  data and is not shipped: fetch it as how-we-built-it/COMMANDS.md says and compare its sha256.
- The skeptics' working files (their fetched pages and their own checkers) are not shipped; their results, URLs, times
  and sha256 values are in panel/.
- self_break.md (named in panel/gate.md) is summarised in how-we-built-it/SELF_BREAK.md.

Level: the main success criterion of fmm-catalogue-small-format-rank (max(14,15,15) = 15 <= 16; sorted format not
(3,3,3) or (4,4,4)), not a partial win. The three skeptic reports and the honesty gate are in panel/. The
scheme comes from Khoruzhii, Serafin, Gelss and Pokutta's published LITA 15x15x15 rank-1977 scheme by one exact
one-slice cut (112 terms vanish) followed by exact absorption of 29 terms; the rebuild is deterministic and
byte-identical (how-we-built-it/COMMANDS.md).

**First public mention: pull request #752.** This same scheme was first named in public on 2026-10-25T11:18:58Z, in the
body of this contributor's open pull request #752 (the <14,14,15> rank-1709 claim), as the unclaimed intermediate of
its rebuild chain; that pull request ships the code that regenerates it, but not the scheme files. Under the policy for
this family (kit/POLICY.md, fast matrix multiplication, rules 2 and 3) we ask that the credit date be that filing,
2026-10-25T11:18:58Z. Apart from #752's own mention of this scheme, nothing at or below 1836 for this format was public then or is now.
panel/novelty.md takes #752 as setting the credit date, not as making the claim non-novel, and records the stricter
reading (that #752's mention itself makes the value "already public") as a caveat.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS`. Needs only python3 (standard library), no network; 9 s on the build laptop. It checks
all 9,922,500 Brent equations exactly and runs three exact random evaluations. The last lines it prints:

    trial 1: 0 of 210 entries of C differ from AB
    trial 2: 0 of 210 entries of C differ from AB
    trial 3: 0 of 210 entries of C differ from AB
    PASS
    PASS

RUN_IT_YOURSELF.md has the full expected output.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| fmm_sota.json (Lille catalogue digest) | [14, 15, 15] | 1848 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-26T22:01:19Z and 22:30:40Z by the run; 22:13Z and 22:25Z by the panel (same sha256) |
| Lille per-format page | <14x15x15> | 1890 | https://fmm.univ-lille.fr/14x15x15.html | 2026-10-26T22:01:19Z and 22:30:40Z by the run; 22:13Z and 22:25Z by the panel (same sha256) |
| Perminov docs/ranks.md (min over ZT / Z / Q) | 14x15x15 | ZT 1894, Z 1892, Q 1848; minimum 1848 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 2026-10-26T22:01:20Z and 22:30:40Z by the run; 22:13Z and 22:25Z by the panel (same sha256) |
| MerlijnW70/fmm-schemes | 14x15x15 (any orientation) | none (no scheme for this format) | https://github.com/MerlijnW70/fmm-schemes | tree 2026-10-26T22:01:21Z and 22:30:41Z by the run; 22:13Z and 22:25Z by the panel |

The minimum over the four named sources is 1848 (fmm_sota.json and Perminov's Q column; the Lille index at
https://fmm.univ-lille.fr/ also lists 1848, the per-format page 1890); 1836 is 12 below it. No source blocked a request.

Values already public in this repository (not table values; the claim is below them):
| source | cell | value | URL |
|---|---|---|---|
| merged known-knowns, TROPHY_CASE.md entry 44 | <14,15,15> over Q | 1842 | https://github.com/elder-plinius/V3R1T4S/blob/main/TROPHY_CASE.md |
| open pull request #752 (this contributor) | names this <14,15,15> scheme as an unclaimed intermediate | 1836 (this object) | https://github.com/elder-plinius/V3R1T4S/pull/752 |

The panel read all 755 pull requests of this repository: none other holds a (14,15,15) scheme at or below 1841. The
criterion asks for all four sources to be re-fetched immediately before claiming; the run's last fetch of all four was at
2026-10-26T22:30:40Z. Snapshots: the-record-we-beat/.

## Not claimed
- Nothing about any other format: this package is one cell, <14,15,15>. The <14,14,15> rank 1709 derived from this
  scheme is pull request #752's claim, not this one.
- Not the tensor rank of <14,15,15>: 1836 is an upper bound (a scheme with 1836 multiplications), not a proof that fewer
  are impossible.
- Not a ring upgrade: the coefficients are rationals (least common denominator 5440); nothing is claimed over Z or GF(2).
- Not a new search method: the scheme is LITA's public 15x15x15 scheme cut once and reduced by exact absorption. It is
  not a composition, padding or block split of known schemes, and 1836 equals no value listed anywhere we looked.
- Against this repository's own record: the merged <14,15,15> entry is 1842, so 1836 improves it by 6. A precedent for a
  further improvement of a cell the repository already lists: pull request #197, 1762 against a merged 1763.

## Credits
- Kirill Khoruzhii, Luzian Serafin, Patrick Gelss and Sebastian Pokutta, LITA (Local Improvements to Trilinear Aggregation), https://github.com/khoruzhii/lita: the
  15x15x15 rank-1977 scheme (schemes/15x15x15_r1977.npz) this one is cut from.
- Alexandre Sedoglavic, the Lille fast matrix multiplication catalogue, https://fmm.univ-lille.fr/, and its digest
  fmm_sota.json, https://github.com/sedoglavic/fmm_digest.
- Perminov (dronperminov), FastMatrixMultiplication, https://github.com/dronperminov/FastMatrixMultiplication
  (docs/ranks.md compared against).
- MerlijnW70, fmm-schemes, https://github.com/MerlijnW70/fmm-schemes (checked: no scheme for this format).
- The maintainers and contributors of this repository: the merged <14,15,15> rank 1842 (TROPHY_CASE.md entry 44),
  https://github.com/elder-plinius/V3R1T4S/blob/main/TROPHY_CASE.md; the contributors whose exact absorption chains are
  in pull requests #164, #166, #172, #177, #178 and #197
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
