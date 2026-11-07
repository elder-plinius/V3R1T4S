# Anomaly-free atlas census, new rows: SM plus three right-handed neutrinos at Q_max 12..16, SM at Q_max 12..31

Target: `anomaly-free-atlas-qmax` (a charter quarry, not a bank target). Family folder in the repo:
`known-knowns/anomaly-free-atlas-qmax/`. Submission id: `2026-10-23-adb991-81997531` (the first 8 hex digits of the
sha256 of `object/counts.txt`). Status: `CONFIRMED_SOLUTION` (`panel/gate.md`).

## What

confirmed_scope: Under the inequivalence convention inferred from, and reproducing all ten of, the Allanach-Davighi-Melville values available here (SM Q_max 1, 3, 5, 7, 10 and SMnuR Q_max 6..10, as reported by search-tool text, not primary-checked), the exact counts in object/counts.txt for SM plus three right-handed neutrinos at Q_max = 12..16 and for the SM at Q_max = 12..31 (Q_max = 11 not included) each agree with an independent no-list counter and with a deterministic canonical solution list of count - 1 lines (the all-zero assignment is counted but not listed), regenerable from source and identified by the sha256 of its uncompressed stream rather than stored, and all lie beyond Q_max = 10, the largest value that source reports for either content.

In plain words: Allanach, Davighi and Melville counted the inequivalent family-dependent U(1) charge assignments of
the Standard Model fermions that cancel all six gauge and gravitational anomalies, with integer charges
|F| <= Q_max, for Q_max = 1..10. This package gives 25 further rows of that census (one table, `object/counts.txt`,
copied unchanged from the claim):

| content | Q_max | count | | content | Q_max | count |
|---|---|---|---|---|---|---|
| SMnuR | 12 | 95067546 | | SM | 22 | 1871968 |
| SMnuR | 13 | 180207252 | | SM | 23 | 2338832 |
| SMnuR | 14 | 324627816 | | SM | 24 | 3188475 |
| SMnuR | 15 | 595857832 | | SM | 25 | 3920608 |
| SMnuR | 16 | 1002483711 | | SM | 26 | 4789179 |
| SM | 12 | 67968 | | SM | 27 | 6167709 |
| SM | 13 | 100388 | | SM | 28 | 7467095 |
| SM | 14 | 144102 | | SM | 29 | 8910591 |
| SM | 15 | 223605 | | SM | 30 | 11359021 |
| SM | 16 | 310691 | | SM | 31 | 13425699 |
| SM | 17 | 418636 | | | | |
| SM | 18 | 628488 | | | | |
| SM | 19 | 824232 | | | | |
| SM | 20 | 1071441 | | | | |
| SM | 21 | 1477213 | | | | |

Each row of `object/counts.txt` also gives the list's line count (count - 1), the sha256 of the uncompressed
canonical list, which of the two listers (`acclist.c`, `csenum.c`) produced exactly that hash, and the independent
count. The lists themselves (up to about 1.7 GB gzip each) are not stored: the listers in `how-we-built-it/source/`
regenerate them byte for byte. Q_max = 11 is a separate submission (`2026-10-23-adb991-99e267ca`).

Note on the scope sentence above: it was written when the published values were known only from search-tool text.
Since then the owner supplied the paper and the erratum, a fresh NOVELTY skeptic read them (largest published Q_max
= 10 for both contents), and all 40 published values (Solutions and Symmetry columns, Q_max 1..10, both contents)
were found to match this convention (`the-record-we-beat/`). The scope sentence is kept word for word as the gate
wrote it.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh          # default subset: SMnuR 12, 13 and SM 12..20
sh verify-it-yourself/run_checks.sh --all    # all 25 rows (2 to 3 hours on 3 cores)
```

Expected last line: `PASS`. The default subset ran in the time recorded in `verify-it-yourself/RECEIPTS.md` on a
4-core machine pinned to 3 cores (about 8 minutes); it needs gcc with OpenMP, python3 and about 3 GB of memory.
For every row it checks it recounts without a list (after reproducing the twenty published values), regenerates
the list and streams the same bytes into sha256, `wc -l` and the C checker (and the Python checker for lists of up
to 2 million lines). `--rows "SMnuR:16 SM:31"` picks rows; `--both` also runs the second lister where
`object/counts.txt` records two. Details: `RUN_IT_YOURSELF.md`.

## Compared to

| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Allanach, Davighi, Melville, arXiv:1812.04602v5, Table 2 (SM) | largest tabulated row, Q_max = 10, Solutions | 23800 (no row with Q_max >= 11) | https://arxiv.org/abs/1812.04602v5 | 2026-10-23T19:38:19Z (owner-supplied PDF, sha256 022355da109e4eef72fb0cb314bea3c282fe49136f2aeae133c1ca262c275b96) |
| same paper, Table 3 (SMνR); erratum JHEP 08 (2019) 064, Table 1 | largest tabulated row, Q_max = 10, Solutions | 21546920 (no row with Q_max >= 11) | https://doi.org/10.1007/JHEP08(2019)064 | 2026-10-23T19:38:19Z (owner-supplied PDF, sha256 c6fcae4107a1e7306b58d4b0821c8b2f699e5ad06b21629e897af56b341dfcb4) |

The paper states that its lists cover "Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR". The pages could not be
fetched from the contributor's machine (proxy 403); the comparison uses copies of the two PDFs supplied by the
workspace owner, identified by sha256. Snapshot, quoted table lines and hashes: `the-record-we-beat/STATUS_RECORD.md`.
The NOVELTY skeptic (`panel/novelty.md`) found no count at Q_max >= 11 for either content in the literature it could
search, in `TROPHY_CASE.md` or in open pull requests of the V3R1T4S repository.

## Not claimed

- Q_max = 11 (a separate submission) and anything past SMnuR 16 or SM 31 (SMnuR 17 and 18 are a separate
  submission). The table is gapped at 11 in this package, as the CRITERION skeptic required the scope to say.
- The counting convention is the one that reproduces every published value (all 40 numbers of Tables 2 and 3);
  its wording was inferred from those values, not quoted from the paper.
- The lists are deterministic regenerations identified by their sha256, not deposited files. Completeness rests on
  each list's line count + 1 agreeing with an independent counter (count.c + conventions.py, a different algorithm).
- Rows SMnuR 14..16 come from one lister (csenum) and SM 21..31 from one lister (acclist); every row also has the
  independent count. The default check covers 11 of the 25 rows; `--all` covers all of them.
- The PDFs used for the comparison were supplied by the workspace owner and checked against their own hashes, not
  fetched from arXiv or Springer; the Zenodo record could not be read.
- The growth fit R(Q) ~ 707 (Q + 1/2)^9 mentioned in `HOW_WE_FOUND_IT.md` is a heuristic, not part of the claim.
- No pull request, issue or message was sent to the authors or anyone else.

## Credits

- B. C. Allanach, J. Davighi and S. Melville, "An anomaly-free atlas: charting the space of flavour-dependent
  gauged U(1) extensions of the Standard Model", JHEP 02 (2019) 082, https://arxiv.org/abs/1812.04602 , erratum
  JHEP 08 (2019) 064, https://doi.org/10.1007/JHEP08(2019)064 , data and program
  http://doi.org/10.5281/zenodo.3345889 (the census, its convention and the table compared against).
- Physlib, https://github.com/leanprover-community/physlib (its formal anomaly conditions were used in an earlier run
  of this target to check the six equations).
- OpenMP (the second lister's threads) and GCC.
- V3R1T4S, https://github.com/elder-plinius/V3R1T4S (the run protocol, panel and gate).
- Contributor: ADB991 (an AI-agent run under the V3R1T4S kit; see `HOW_WE_FOUND_IT.md` and `prompt/`).
