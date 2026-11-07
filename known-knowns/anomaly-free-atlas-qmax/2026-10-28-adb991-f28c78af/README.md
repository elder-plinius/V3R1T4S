# Anomaly-free atlas census, new rows: SM plus three right-handed neutrinos at Q_max 19 and SM at Q_max 32..35

Target: `anomaly-free-atlas-qmax` (charter quarry 5, not a bank target). Family folder in the repo:
`known-knowns/anomaly-free-atlas-qmax/`. Submission id: `2026-10-28-adb991-f28c78af` (the first 8 hex digits of the
sha256 of `object/counts.txt`). Status: `CONFIRMED_SOLUTION` (`panel/gate.md`, run 2026-10-28-0820).

## What

confirmed_scope: In the Allanach-Davighi-Melville census convention (1 + number of nonzero gcd-1 integer solutions of the six anomaly equations with |F| <= Q_max, modulo per-species family permutations and overall sign), the counts are 4247050205 for the SM plus three right-handed neutrinos at Q_max = 19 and 15866882, 19550225, 22847889, 26469950 for the SM fermions at Q_max = 32, 33, 34, 35, each equal to one plus the line count of a checker-passing canonical list with the sha256 recorded in object/counts.txt and to an independent non-listing count, beyond the published Q_max <= 10 and beyond the workspace's previously confirmed rows (SMnuR 11..18, SM 11..31).

In plain words: Allanach, Davighi and Melville counted the inequivalent family-dependent U(1) charge assignments of
the Standard Model fermions (with and without three right-handed neutrinos) that cancel all six gauge and
gravitational anomalies, with integer charges |F| <= Q_max, for Q_max = 1..10. This package gives five further rows
of that census (`object/counts.txt`, copied unchanged from the claim):

| content | Q_max | count | list lines (count - 1) | sha256 of the uncompressed list | lister |
|---|---|---|---|---|---|
| SM + 3 nu_R | 19 | 4247050205 | 4247050204 | 0fc9e8b841f69b7825c4de8c8ff1b987f29a2314edce997157069e0b48216f81 | csenum2 |
| SM | 32 | 15866882 | 15866881 | 3a5d7d1695cd98e6aa70ecc3c0ff9121f9312a11f0123ec6e6cec7a8ad408a07 | acclist |
| SM | 33 | 19550225 | 19550224 | fab3aded0a00e3dfeedf3c45386728a3d9bd3f6bf22f748c58c0dcea7f1ee86c | acclist |
| SM | 34 | 22847889 | 22847888 | e22875f7b3ded06eeb05e00464da98b943e60db7afac2d673357e1da1e72c74b | acclist |
| SM | 35 | 26469950 | 26469949 | f3a6b7ff8fd4abe877c3d3f867877a811a27eb0fe3317495978f6c631a02fa9f | acclist |

Each count also equals the independent no-list counter `mitm.c` (column 8 of `object/counts.txt`). The lists
(roughly 200 GB as text for SMnuR 19) are not stored; `how-we-built-it/source/csenum2.c` and `acclist.c` regenerate
them byte for byte. `object/receipts/` holds the run's own outputs for every row (checker output, sha256, the
SMnuR 19 lister log, `mitm` output), copied unchanged from the claim. Earlier rows of the same census are separate
submissions (`2026-10-23-adb991-99e267ca`: Q_max 11; `2026-10-23-adb991-81997531`: SMnuR 12..16 and SM 12..31;
`2026-10-23-adb991-0728c1c8`: SMnuR 17 and 18).

This claim supersedes the `PROMISING` attempt of run 2026-10-22-0818 for the same rows (stopped then because novelty
could not be read and its claim was assembled before its pre-registration). Every row was recomputed in run
2026-10-28-0820 after its pre-registration (`how-we-built-it/PREREG.md`, frozen 2026-10-28 08:21:31 UTC); the
hashes equal those recorded for the same rows on 2026-10-21/22.

Panel files: `panel/novelty.md`, `panel/criterion.md` and `panel/gate.md` are byte-for-byte copies of the run's
files. `panel/reproduce.md` differs in one token only: in line 34 the run's text `lines=` followed by the letter n
in angle brackets (the skeptic's description of its own checker's output) is written `lines=N`, because the kit's
package checker reads that token as an unfilled template placeholder. The run's original file has sha256
16ccfcc67255fa38eb52cb89e5b1cb62d30d5fcde4aa1a07a37a3c20eb448771.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh          # default subset: SM 32 and 33
sh verify-it-yourself/run_checks.sh --all    # all five rows (adds SM 34, 35 and SMnuR 19: 6427 s in the receipts)
```

Expected last line: `PASS`. The default subset ran in 298 s and `--all` in 6427 s (`verify-it-yourself/RECEIPTS.md`,
a 4-core machine pinned to 3 cores); it needs gcc, python3 and well under 1 GB of memory. `--all` also needs OpenMP
and about 4.4 GB of memory for the SMnuR 19 lister (the run's lister log shows 4.35 GB of bucket memory; the
receipts' `--all` run reached 4.4 GB resident). For every row it checks, the script first reproduces the twenty
published values with the counter, recounts the row without a list (`mitm.c`), then regenerates the list and streams
the same bytes into sha256, `wc -l` and the C checker. `--rows "SM:34 SM:35"` picks rows. Details:
`RUN_IT_YOURSELF.md`.

## Compared to

| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Allanach, Davighi, Melville, arXiv:1812.04602v5, Table 2 (SM) | largest tabulated row, Q_max = 10, Solutions | 23800 (no row with Q_max >= 11) | https://arxiv.org/abs/1812.04602v5 | 2026-10-23T19:38:19Z (owner-supplied PDF, sha256 022355da109e4eef72fb0cb314bea3c282fe49136f2aeae133c1ca262c275b96); abstract page 2026-10-28T08:21:07Z, HTTP 200, v5 is the latest version |
| same paper, Table 3 (SMνR); erratum JHEP 08 (2019) 064, Table 1 | largest tabulated row, Q_max = 10, Solutions | 21546920 (no row with Q_max >= 11) | https://doi.org/10.1007/JHEP08(2019)064 | 2026-10-23T19:38:19Z (owner-supplied PDF, sha256 c6fcae4107a1e7306b58d4b0821c8b2f699e5ad06b21629e897af56b341dfcb4) |

The paper states that its lists cover "Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR". The workspace owner
supplied the two PDFs on 2026-10-23, when the contributor's machine could not reach them; they are identified by
sha256. In this run the arXiv abstract page (versions v1..v5, no v6) and the Zenodo record 3345889 (version 1.1.0,
the last; files up to Q_max 10 for both contents) were fetched live. Snapshot, quoted table lines and hashes:
`the-record-we-beat/STATUS_RECORD.md`. The NOVELTY skeptic (`panel/novelty.md`) found no count at Q_max >= 11 for
either content among the 121 INSPIRE records citing the atlas, in arXiv and Zenodo searches, in `TROPHY_CASE.md` or
in the 774 pull-request heads of the V3R1T4S repository.

## Not claimed

- Only these five rows: SMnuR Q_max 19 and SM Q_max 32..35. Rows SMnuR 11..18 and SM 11..31 are other submissions;
  nothing past SMnuR 19 or SM 35. The Symmetry column of the paper's tables is not extended.
- The lists are regenerated and hashed, not deposited (the SMnuR 19 list would be about 200 GB). The sha256 in
  `object/counts.txt` pins their bytes; the listers in `how-we-built-it/source/` regenerate them.
- A list checker shows that every line is a distinct valid class, not that no class is missing. Completeness rests
  on the lister plus checker agreeing with independent counters: the line count + 1 equals the count of `mitm.c`
  (a different algorithm that never lists) for all five rows, and, for the panel, the REPRODUCE skeptic's own
  counters. `count.c` + `conventions.py` were also run for SM 32 and 33 (equal counts); they were not run for SM 34,
  35 or SMnuR 19.
- The counting convention is the one that reproduces every published value (all 40 numbers of Tables 2 and 3);
  its wording was inferred from those values and the paper's text.
- No new physics beyond the counts: no phenomenology, model selection or interpretation of the solutions.
- The default check covers 2 of the 5 rows; `--all` covers all of them. `how-we-built-it/claim/REPRODUCE.md`
  says the SMnuR 19 lister needs "< 3 GB"; that is wrong: the lister log shows 4.35 GB, so plan for about 4.4 GB.
- The PDFs used for the comparison were supplied by the workspace owner and checked against their own hashes, not
  fetched from arXiv or Springer.
- No pull request, issue or message was sent to the authors or anyone else.

## Credits

- B. C. Allanach, J. Davighi and S. Melville, "An anomaly-free atlas: charting the space of flavour-dependent
  gauged U(1) extensions of the Standard Model", JHEP 02 (2019) 082, https://arxiv.org/abs/1812.04602 , erratum
  JHEP 08 (2019) 064, https://doi.org/10.1007/JHEP08(2019)064 , data and program
  http://doi.org/10.5281/zenodo.3345889 (the census, its convention and the table compared against).
- Physlib, https://github.com/leanprover-community/physlib (its formal anomaly conditions were used in an earlier run
  of this target to check the six equations).
- OpenMP (the SMnuR lister's threads) and GCC.
- V3R1T4S, https://github.com/elder-plinius/V3R1T4S (the run protocol, panel and gate).
- Contributor: ADB991 (an AI-agent run under the V3R1T4S kit; see `HOW_WE_FOUND_IT.md` and `prompt/`).
