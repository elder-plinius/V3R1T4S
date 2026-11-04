# fmm-catalogue-small-format-rank: main success criterion, <13,14,15> rank 1644 over Q

## What
The files object/u.txt (sha256 caef7bb7...), object/v.txt (b31e5e77...) and object/w.txt (79b90daf...) define a bilinear scheme over Q with exactly 1644 rank-one terms and no zero factors that satisfies all 7452900 Brent equations for <14,15,13> in exact arithmetic (and, after the cyclic relabelling, for <13,14,15>), which is strictly below the rank 1681 that fmm_sota.json, the Lille page 13x14x15.html and the minimum of Perminov's ZT/Z/Q columns in docs/ranks.md each list for (13,14,15) as re-fetched at 2026-10-28T22:33Z, strictly below the rank 1645 merged in this repository, and in a cell where MerlijnW70/fmm-schemes lists no scheme.

Path note: claim/ (the run's claim folder) was frozen at 2026-10-28T22:10Z (panel/claim.sha256, 17 files) and checked unchanged after each skeptic; three
fresh subagents ran one after another, each with only its own copy of claim/: REPRODUCE (Claude Sonnet 5.5), NOVELTY
and CRITERION (Claude Opus 5.5). The first CRITERION verdict (also a pass) quoted the criterion's URL template with
angle brackets, which the package check rejects as an unfilled placeholder; rather than edit it, a fresh
CRITERION subagent was run on an unchanged copy of claim/ and panel/criterion.md is its verdict (panel/gate.md; the gate was amended at 22:38:34Z to record the re-run). The
panel files are copied as written, except that a few words on how the skeptic sessions were screened were reworded. Where they name claim/ files:
- claim/object/ is object/ and claim/verify-it-yourself/ is verify-it-yourself/ (byte-identical except run_checks.sh,
  which here is the version that writes no temporary files into the package folder; RECEIPTS.md added).
- claim/CLAIM.md and claim/REPRODUCE.md are in how-we-built-it/ (REPRODUCE.md unchanged, its paths refer to the claim
  folder; CLAIM.md with a one-token edit of the URL template in the criterion: the angle-bracket form of the template written with braces, {n}x{m}x{p});
  claim/TABLE_RECORD.md is the-record-we-beat/TABLE_RECORD.md (unchanged).
- claim/rebuild/*.py is how-we-built-it/code/ (byte-identical); claim/rebuild/run_rebuild.sh is replaced by the
  commands in how-we-built-it/COMMANDS.md. The LITA parent 15x15x15_r1977.npz is third-party data and is not shipped:
  fetch it as COMMANDS.md says and compare its sha256.
- claim/the-record-we-beat/13x14x15_r1645_Q.json is the merged record's object, already in this repository at
  known-knowns/faster-matrix-multiplication/2026-10-15-anonymous-c6d1e0ab-49ee1c4f/object/ (same sha256); not shipped again.
- Workspace names that are not part of this package: the run id 2026-10-28-2200 (panel/gate.md), the lead
  runs/2026-10-25-0343/leads/13x14x15_r1644/D1709_ax2.c8_r1644.json (how-we-built-it/PREREG.md; exporting it gives
  object/ byte for byte), target.md (PREREG.md; its criterion text is the 'Success criterion' section of
  how-we-built-it/CLAIM.md), the skeptics' working folders mine/, fetch/, scripts/, work/, claimcopy/, sorted/, copy1/ and copy2/ (not shipped; their results, URLs, times and sha256 values are in panel/), NEXT_RUN.md and attempts/contrarian/evasion_grep.txt (panel/gate.md: the run's note to the packaging step and its table-access audit), mycheck.py and the run id 2026-10-26-2200 (how-we-built-it/PREREG.md: the independent exact checker written in the earlier run behind pull request #791; "the two earlier packages" there are earlier packages of this contributor, and the same check_scheme.py ships byte-identical in our pull requests #708, #752, #791 and #805), rebuild_slice.py and scanD.py (named in how-we-built-it/code/rebuild_chain.py: the 2026-10-25 run's scripts, whose three fixed steps rebuild_chain.py replays), and the self-break notes, summarised in how-we-built-it/SELF_BREAK.md.

Corrections to the panel text:
- the-record-we-beat/TABLE_RECORD.md (the panel's input, unchanged) lists #178 among the pull requests whose title or body mentions (13,14,15); #178 names only (13,14,14). It also calls the "16448" in #399 a kissing-number count; it is the number of rows on spherical-codes.org. Neither affects the result.
- how-we-built-it/REPRODUCE.md (a frozen claim file): its "expected output" of the rebuild shows the
  input path as ../../data/lita/15x15x15_r1977.npz and a different "wrote ... to" path than a run from the claim folder
  prints. The hashes and the result are the same.

Level: the main success criterion of fmm-catalogue-small-format-rank (max(13,14,15) = 15 <= 16; sorted format not
(3,3,3) or (4,4,4)), not a partial win. The three skeptic reports and the honesty gate are in panel/.
The object is stored in the orientation <14,15,13> (A 14x15 times B 15x13); a cyclic rotation of the three factors
gives a scheme with the same 1644 terms for the sorted format <13,14,15>, and the CRITERION skeptic built and checked
that rotated scheme exactly. The scheme comes from Khoruzhii, Serafin, Gelss and Pokutta's published LITA 15x15x15
rank-1977 scheme by three exact one-slice cuts, each followed by an exact absorption pass (the second removed nothing; 1977 -> 1865 -> 1836 -> 1709 -> 1677
-> 1644); the rebuild is deterministic and byte-identical (how-we-built-it/COMMANDS.md).

The margin over this repository's merged record is 1: <13,14,15> rank 1645, contributed in pull request #166
(known-knowns/faster-matrix-multiplication/2026-10-15-anonymous-c6d1e0ab-49ee1c4f/). Three of the four catalogue sources list 1681; the fourth, MerlijnW70/fmm-schemes, has no scheme for this format. No pull request, open or closed, claims 1644 or lower for this format.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS`. Needs only python3 (standard library), no network; about 10 s on the build laptop. It
checks all 7,452,900 Brent equations exactly and runs three exact random evaluations. The last lines it prints:

    trial 1: 0 of 182 entries of C differ from AB
    trial 2: 0 of 182 entries of C differ from AB
    trial 3: 0 of 182 entries of C differ from AB
    PASS
    PASS

RUN_IT_YOURSELF.md has the full expected output.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| fmm_sota.json (Lille catalogue digest, createdAt 2026-10-19T20:46:33) | [13, 14, 15] | 1681 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-28T22:01:18Z, 22:08:49Z and 22:28:45Z by the run; 22:16-22:19Z (NOVELTY), 22:23Z and 22:33Z (CRITERION) by the panel; same sha256 every time |
| Lille per-format page | <13x14x15> | 1681 | https://fmm.univ-lille.fr/13x14x15.html | 2026-10-28T22:01:18Z, 22:08:49Z and 22:28:45Z by the run; by both panel skeptics; same sha256 |
| Perminov docs/ranks.md (min over ZT / Z / Q) | 13x14x15 | ZT 1681 (?), Z 1681 (1714), Q 1681 (1714); minimum 1681 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 2026-10-28T22:01:19Z, 22:08:49Z and 22:28:46Z by the run; by both panel skeptics; same sha256 |
| MerlijnW70/fmm-schemes | 13x14x15 (any orientation) | none (no scheme for this format) | https://github.com/MerlijnW70/fmm-schemes | tree and SHA256SUMS 2026-10-28T22:01:19Z, 22:08:49Z/50Z and 22:28:46Z by the run; by both panel skeptics |
| this repository, merged (kit/POLICY.md, fast matrix multiplication rule 1) | <13,14,15> | 1645 (pull request #166, merged 2026-10-15) | https://github.com/elder-plinius/V3R1T4S/pull/166 | TROPHY_CASE.md row 48, fetched 2026-10-28T22:28:46Z |

The minimum over the four named sources is 1681 (the Lille index at https://fmm.univ-lille.fr/ also lists 1681);
1644 is 37 below it and 1 below the merged 1645. No source blocked a request. Snapshots: the-record-we-beat/.

Pull requests: all 781 (numbers 1 to 811, every state) read through the pulls list API at 2026-10-28T22:01Z, 22:08Z and
22:28Z by the run, and separately by the NOVELTY skeptic. The only claims for this format are #4 (closed, unmerged,
1646) and #166 (merged, 1645). The criterion asks for all four sources to be re-fetched immediately before claiming;
the last fetch of all four was at 2026-10-28T22:33Z (CRITERION).

## Not claimed
- Nothing about any other format: this package is one cell, <13,14,15>. A second 1644 scheme from the same parent
  (a different third cut) exists; it is not part of this package.
- Not the tensor rank of <13,14,15>: 1644 is an upper bound (a scheme with 1644 multiplications), not a proof that
  fewer are impossible.
- Not a ring upgrade: the coefficients are rationals (least common denominator 5440; the checker scales by 54400, also
  a common denominator); nothing is claimed over Z or GF(2).
- Not a new search method: LITA's public 15x15x15 scheme cut three times and reduced by exact absorption, the same
  technique as earlier merged records of this family. It is not a composition, padding or block split of known schemes,
  and 1644 equals no value listed anywhere we looked.

## Credits
- Kirill Khoruzhii, Luzian Serafin, Patrick Gelss and Sebastian Pokutta, LITA (Local Improvements to Trilinear
  Aggregation), https://github.com/khoruzhii/lita: the 15x15x15 rank-1977 scheme (schemes/15x15x15_r1977.npz) this
  one is cut from.
- The contributor of pull request #166 (https://github.com/elder-plinius/V3R1T4S/pull/166; credited there as anonymous-c6d1e0ab), whose merged <13,14,15>
  rank 1645 is the record compared against.
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
