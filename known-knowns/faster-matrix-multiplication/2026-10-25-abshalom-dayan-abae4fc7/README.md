# fmm-catalogue-small-format-rank: main success criterion, <14,14,15> rank 1709 over Q

## What
The three files in claim/object/ (sha256 abae4fc7..., a05bcf35..., 041992e8...) define a bilinear scheme with exactly 1709 rank-one terms over Q for <14,14,15> that satisfies all 8,643,600 Brent equations exactly, and 1709 is strictly below the minimum 1789 of the four named sources as fetched live at 2026-10-25T10:13:20Z (fmm_sota.json 1789, Lille 14x14x15.html 1798, Perminov ranks.md min 1790, MerlijnW70 no entry), with no V3R1T4S pull request at rank <= 1709 for this format.

Path note: the sentence above and the panel files name the run's claim folder (claim/object/ is object/ here) and the
skeptics' working folders; where each named file is in this package, or that it is not shipped, is listed under
"Notes on the panel files" below.

Level: the main success criterion of fmm-catalogue-small-format-rank (max(14,14,15) = 15 <= 16; sorted format not (3,3,3)
or (4,4,4)), not a partial win. Claimed under the main criterion; the skeptic reports and the gate record are in panel/. The scheme
comes from Khoruzhii, Serafin, Gelss and Pokutta's published LITA 15x15x15 rank-1977 scheme by two exact one-slice cuts,
each followed by exact 2-reductions (112 + 105 terms vanish, 29 + 22 are removed); the rebuild is deterministic and was
byte-identical when the run's self-break session and the packaging step reran it (how-we-built-it/COMMANDS.md); the
panel did not rerun it (python-flint was not installed).

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS`. Needs only python3 (standard library), no network; it took 5 min 27 s wall clock (270 s of
CPU) on a shared laptop at low priority, about 4 minutes on an idle one, with about 1.4 GB peak memory. It joins the split object files into u.txt and
v.txt (the 1 MB per-file limit), checks their three sha256 values against the ones the panel checked (u.txt abae4fc7...f56e) and stops with FAIL on any
other file,
checks all 8,643,600 Brent equations exactly, and runs three exact random evaluations. The last lines it prints:

    trial 1: 0 of 210 entries of C differ from AB
    trial 2: 0 of 210 entries of C differ from AB
    trial 3: 0 of 210 entries of C differ from AB
    PASS
    PASS

RUN_IT_YOURSELF.md has the full expected output.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| fmm_sota.json (Lille catalogue digest) | [14, 14, 15] | 1789 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-25T07:05:01Z by the run; 10:09:20Z by the panel (same sha256) |
| Lille per-format page | <14x14x15> | 1798 | https://fmm.univ-lille.fr/14x14x15.html | 2026-10-25T07:03:39Z by the run; 10:09:20Z and 10:13:20Z by the panel (same sha256) |
| Perminov docs/ranks.md (min over ZT / Z / Q) | 14x14x15 | ZT 1798, Z 1798, Q 1790; minimum 1790 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 2026-10-25T07:05:02Z by the run; 10:09:21Z and 10:13:20Z by the panel (same sha256) |
| MerlijnW70/fmm-schemes | 14x14x15 (any orientation) | none (no scheme for this format) | https://github.com/MerlijnW70/fmm-schemes | tree 2026-10-25T07:03:41Z and SHA256SUMS 07:05:03Z by the run; tree 10:09:21Z and 10:13:50Z, page 10:13:20Z by the panel |

The minimum over the four named sources is 1789 (fmm_sota.json; the Lille index at https://fmm.univ-lille.fr/ also
lists 1789, a plain composition <14x14x1:196> + <14x14x14:1593>); 1709 is 80 below it. No source blocked a request.

Values already public in this repository (not table values; the claim is below both):
| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| merged known-knowns, TROPHY_CASE.md entry 47 | <14,14,15> over Q | 1716 | https://github.com/elder-plinius/V3R1T4S/blob/main/TROPHY_CASE.md | 2026-10-25T05:57:36Z by the run; 10:09:23Z and 10:14:17Z by the panel |
| closed, not merged pull request #6 | (14, 14, 15) over Q | 1715 | https://github.com/elder-plinius/V3R1T4S/pull/6 | pull-request search 2026-10-25T07:03:42Z by the run; 10:10:55Z and 10:13:51Z by the panel |

The panel read all 711 pull requests (a scan at filing covered all 751) of this repository for every spelling and orientation of the format: only #6 holds
a scheme for it (#399 only quotes the catalogue change 1790 -> 1789), and none is at or below 1709. Snapshots with sha256 and headers: the-record-we-beat/.

Re-fetched live immediately before filing, as the criterion asks: fmm_sota.json (2026-10-25T11:18:27Z, HTTP 200),
https://fmm.univ-lille.fr/14x14x15.html (11:18:27Z, HTTP 200) and Perminov docs/ranks.md (11:18:27Z, HTTP 200) were
byte-identical to the panel's copies (sha256 2a653515..., 63ce18bf..., 77203a71...), so 1789, 1798 and 1790 stand;
the MerlijnW70/fmm-schemes tree (11:18:37Z, HTTP 200) has 39 paths, none for this format. Pull requests up to #751:
none names this format. 1709 is 80 below the bar of 1789 and 7 below this repository's merged 1716.

## Not claimed
- Nothing about any other format: this package is one cell, <14,14,15>.
- Not the tensor rank of <14,14,15>: 1709 is an upper bound (a scheme with 1709 multiplications), not a proof that
  fewer are impossible.
- Not a ring upgrade: the coefficients are rationals (denominators up to 1560); nothing is claimed over Z or GF(2).
- Not a new search method: the scheme is built from LITA's public 15x15x15 rank-1977 scheme by two exact one-slice
  cuts, each followed by exact 2-reductions (linear dependencies among terms). It is not a composition, padding or
  block split of known schemes, and 1709 equals no value listed in the Lille construction column or anywhere else we
  looked.
- Against this repository's own record: the merged <14,14,15> entry is 1716, so 1709 is an improvement of 7 on it (and
  6 below the closed pull request #6, 1715). Whether the repository counts a further improvement of a cell it already
  lists is the maintainers' call; the panel noted the precedent of pull request #197 (1762 against a merged 1763), and the contributed ranks in #166
  and #178 superseded the maintainers' own merged entries 48 and 45. The run's charter treats cells this repository
  already improved as taken; the run still aimed here because its preregistered threshold (how-we-built-it/PREREG.md,
  Thresholds) is to beat the four tables and every value already public in this repository, which 1709 does.
- Not the intermediate <14,15,15> scheme of rank 1836 that HOW_WE_FOUND_IT.md and how-we-built-it/COMMANDS.md name
  as a step of the chain: it is not part of this package and the panel did not check it.
- The Lille per-format page (1798) lags the index and fmm_sota.json (1789); the binding bar is the minimum, 1789.
  MerlijnW70/fmm-schemes lists no scheme for the format, so that clause holds vacuously.

## Notes on the panel files
- Two edits were made after the gate and are disclosed at the end of panel/gate.md: its status line now uses the kit's
  CONFIRMED_SOLUTION, and panel/criterion.md's quote of the criterion's URL template is written with braces
  ({n}x{m}x{p}) because the kit's checker reads angle-bracket names as unfilled placeholders. No verdict or value changed.
The panel was run by the supervising session after the run had ended (the run stopped at 07:38:10Z with no panel
result), as panel/gate.md describes: claim frozen 2026-10-25T09:59:51Z, then three fresh subagents one after another,
each given only a copy of the claim folder: REPRODUCE (about 10:00 to 10:08:44Z), NOVELTY (about 10:09 to 10:12:22Z),
CRITERION (about 10:13 to 10:16:58Z), gate written about 10:18Z. The four panel files and claim.sha256 are copied
as they are, with the two disclosed edits above in panel/gate.md and panel/criterion.md. They name files of the claim folder and of the skeptics' working folders that are placed or handled
differently here:
- `claim/object/` is `object/` (u.txt and v.txt are stored as two parts each, joined byte for byte by run_checks.sh; the
  parts concatenate to the sha256 values in panel/gate.md and panel/claim.sha256).
- `claim/verify-it-yourself/` is `verify-it-yourself/`: check_scheme.py and check_random_eval.py are byte-identical to
  the claim's; only run_checks.sh differs: it joins the parts first, and, since an edit after the gate, it compares
  the three sha256 values with the files the panel checked and stops with FAIL on any other file (the gated version
  only printed them).
- `claim/CLAIM.md` and `claim/REPRODUCE.md` are in how-we-built-it/. CLAIM.md has one edit (the Lille URL template
  written {n}x{m}x{p} instead of with angle brackets, for the package checker); REPRODUCE.md is the original, and its
  paths refer to the claim folder. So their sha256 values in panel/claim.sha256 match REPRODUCE.md only.
  `claim/TABLE_RECORD.md` is the-record-we-beat/TABLE_RECORD.md with one edit (a run id removed), so its hash no
  longer matches.
- `claim/rebuild/` is how-we-built-it/code/ (scripts byte-identical; the five files sha256-listed in claim.sha256 can
  be compared). The LITA parent file 15x15x15_r1977.npz is third-party data and is not shipped: fetch it as
  how-we-built-it/COMMANDS.md says and compare its sha256 (94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33).
- `fetch/` (the NOVELTY and CRITERION skeptics' fetched bodies and fetch log) and `work/mycheck.py` (the REPRODUCE
  skeptic's checker) are not shipped; their results are in panel/ and their URLs, times and sha256 values are in
  the-record-we-beat/RECORD.md and panel/. The REPRODUCE skeptic could not run the rebuild (python-flint absent); the
  run's self-break session did (how-we-built-it/SELF_BREAK.md).
- `self_break.md` (named in panel/gate.md) is summarised in how-we-built-it/SELF_BREAK.md; the full file is not shipped
  because it names the run's private working folders.
- how-we-built-it/PREREG.md names files of the run folder that are not shipped: attempts/... (see its own note),
  target.md and scout.md.
- panel/gate.md names the run by its internal id and lane ("2026-10-25-0343, Track B"): that is the run that built
  this claim.

Other files revised after the gate: README.md, HOW_WE_FOUND_IT.md (method credit), RUN_IT_YOURSELF.md and a note in
verify-it-yourself/RECEIPTS.md (expected output), and INDEX.csv (cell written `14x14x15`, numeric table value 1789;
its sha256 is of the joined u.txt). The object, the What sentence and the panel verdicts did not change.

## Credits
- Kirill Khoruzhii, Luzian Serafin, Patrick Gelss and Sebastian Pokutta, Local Improvements to Trilinear Aggregation
  (LITA), https://github.com/khoruzhii/lita (manuscript in preparation; the repository is the citation): the 15x15x15
  rank-1977 scheme (schemes/15x15x15_r1977.npz) this one is cut from, and the 2-reduction idea (2-reducibility,
  src/reduce.h). LITA builds on Victor Pan's trilinear aggregation (V. Ya. Pan, FOCS 1978,
  https://doi.org/10.1109/SFCS.1978.34). The NOVELTY skeptic also names arXiv:2511.10786,
  https://arxiv.org/abs/2511.10786, by Khoruzhii, Gelss and Pokutta on flip-graph search for structured matrix
  multiplication, which this work does not use.
- calgulbenkian (credit name anonymous-c6d1e0ab), for the method: the slice-and-absorb approach on LITA squares in
  this repository's merged claims https://github.com/elder-plinius/V3R1T4S/pull/164,
  https://github.com/elder-plinius/V3R1T4S/pull/166, https://github.com/elder-plinius/V3R1T4S/pull/172,
  https://github.com/elder-plinius/V3R1T4S/pull/177, https://github.com/elder-plinius/V3R1T4S/pull/178 and
  https://github.com/elder-plinius/V3R1T4S/pull/197, and the flat (consensus) absorption step, which
  how-we-built-it/code/flat.py re-implements from the ca.py of merged
  https://github.com/elder-plinius/V3R1T4S/pull/179; also the author of the closed pull request
  https://github.com/elder-plinius/V3R1T4S/pull/6 (rank 1715 for this format).
- Manuel Kauers and Isaac Wood, Exploring the Meta Flip Graph for Matrix Multiplication, arXiv:2510.19787
  (https://arxiv.org/abs/2510.19787), and Manuel Kauers and Jakob Moosbauer, Flip Graphs for Matrix Multiplication,
  arXiv:2212.01175 (https://arxiv.org/abs/2212.01175) (reductions in general). Richard P. Brent, STAN-CS-70-157 (1970),
  for the Brent equations.
- Alexandre Sedoglavic, the Lille fast matrix multiplication catalogue, https://fmm.univ-lille.fr/, and its digest
  fmm_sota.json, https://github.com/sedoglavic/fmm_digest.
- A. I. Perminov (dronperminov), FastMatrixMultiplication, https://github.com/dronperminov/FastMatrixMultiplication
  (docs/ranks.md compared against), and Fast Matrix Multiplication in Small Formats, arXiv:2603.02398
  (https://arxiv.org/abs/2603.02398).
- MerlijnW70, fmm-schemes, https://github.com/MerlijnW70/fmm-schemes (checked: no scheme for this format).
- Benoit Chatain Lacelle, matmulcatalog (arXiv:2606.13408, https://arxiv.org/abs/2606.13408), https://github.com/solven-eu/matmulcatalog (catalog.json read as a further
  comparator; lowest value for the cell 1789).
- The maintainers of this repository, the merged <14,14,15> rank 1716 (TROPHY_CASE.md entry 47),
  https://github.com/elder-plinius/V3R1T4S/blob/main/TROPHY_CASE.md.
- python-flint (used by the rebuild for exact linear algebra), https://github.com/flintlib/python-flint, and NumPy,
  https://github.com/numpy/numpy.
- Found and packaged by Abshalom Dayan with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
