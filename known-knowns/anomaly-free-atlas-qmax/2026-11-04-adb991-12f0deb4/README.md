# Anomaly-free atlas census, new rows: SM plus three right-handed neutrinos at Q_max 20 and SM at Q_max 36..38

Target: `anomaly-free-atlas-qmax` (charter quarry 5, not a bank target). Family folder in the repo:
`known-knowns/anomaly-free-atlas-qmax/`. Submission id: `2026-11-04-adb991-12f0deb4` (the first 8 hex digits of the
sha256 of `object/counts.txt`). Status: `CONFIRMED_SOLUTION` (`panel/gate.md`; claim built in run 2026-11-03-0919,
panelled in run 2026-11-04-0918).

## What

confirmed_scope: In the Allanach-Davighi-Melville convention (1 + primitive nonzero integer solutions of the six ACCs with |F| <= Q_max, modulo per-species family permutations and overall sign; reproduces all their published Q_max <= 10 solution counts), the number of inequivalent anomaly-free U(1) charge assignments is 6465226975 for the Standard Model plus three right-handed neutrinos at Q_max = 20 and 32457211, 37347334 and 42898799 for the Standard Model fermions alone at Q_max = 36, 37 and 38, each certified by a code-regenerated (not stored) canonical list of count - 1 lines identified by the sha256 in object/counts.txt, validated line by line by checker/checklist.c and matched in count by the independent counter source/mitm.c.

In plain words: Allanach, Davighi and Melville counted the inequivalent family-dependent U(1) charge assignments of
the Standard Model fermions (with and without three right-handed neutrinos) that cancel all six gauge and
gravitational anomalies, with integer charges |F| <= Q_max, for Q_max = 1..10. This package gives four further rows
of that census (`object/counts.txt`, copied unchanged from the claim):

| content | Q_max | count | list lines (count - 1) | sha256 of the uncompressed list | lister |
|---|---|---|---|---|---|
| SM + 3 nu_R | 20 | 6465226975 | 6465226974 | 4919f760902d647f6406a801bf463a9fdafdbf8189f549093f00826ed3a327cf | csenum2 (80 passes) |
| SM | 36 | 32457211 | 32457210 | 7fd525fd695292d2991dbc051bf7ddf10a35b91d3e85a7a22a165e9183e52b4f | acclist |
| SM | 37 | 37347334 | 37347333 | 06de08d7c30a9ffd285529c826037f9cd90a1afb1932c243e2a82a3ba26ae5bc | acclist |
| SM | 38 | 42898799 | 42898798 | bf99b850233b5ef48594174f48779bbe1b3bded3efaf7e854153a62ab7632393 | acclist |

Each count also equals the independent no-list counter `mitm.c` (the `mitm.c:` field of `object/counts.txt`). The
lists (roughly 300 GB as text for SMnuR 20) are not stored; `how-we-built-it/source/csenum2.c` and `acclist.c`
regenerate them byte for byte. `object/receipts/` holds the claim run's own outputs for every row (checker output,
sha256, the SMnuR 20 lister log and resident-memory log, `mitm` output), copied unchanged from the claim. Earlier
rows of the same census are separate submissions (`2026-10-23-adb991-99e267ca`: Q_max 11; `2026-10-23-adb991-81997531`:
SMnuR 12..16 and SM 12..31; `2026-10-23-adb991-0728c1c8`: SMnuR 17 and 18; `2026-10-28-adb991-f28c78af`: SMnuR 19 and
SM 32..35).

Every row was computed in run 2026-11-03-0919 after its pre-registration (`how-we-built-it/PREREG.md`). The SM
hashes equal those of the same rows listed on 2026-11-02 (run 2026-11-02-0920, whose SMnuR 20 list was killed by
the session's memory limit at 40 passes). The three-skeptic panel ran in fresh contexts in run 2026-11-04-0918.

Panel files: `panel/` holds byte-for-byte copies of the panel's four files (`reproduce.md`, `novelty.md`, `criterion.md`,
`gate.md`, run 2026-11-03-0919's `panel/`).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh          # default subset: SM 36
sh verify-it-yourself/run_checks.sh --all    # all four rows (adds SM 37, 38 and SMnuR 20: about 2.5 h)
```

Expected last line: `PASS`. The default subset ran in 571 s (`verify-it-yourself/RECEIPTS.md`); it needs
gcc, python3 and well under 1 GB of memory. `--all` also needs OpenMP and about 4.7 GB of memory for the SMnuR 20
lister at 80 passes (the claim's receipts: peak 4.66 GB resident; 40 passes need more than 7 GB). For every row it
checks, the script first reproduces the twenty published values with the counter, recounts the row without a list
(`mitm.c`), then regenerates the list and streams the same bytes into sha256, `wc -l` and the C checker.
`--rows "SM:37 SM:38"` picks rows. Details: `RUN_IT_YOURSELF.md`.

## Compared to

| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Allanach, Davighi, Melville, arXiv:1812.04602v5, Table 2 (SM) | largest tabulated row, Q_max = 10, Solutions | 23800 (no row with Q_max >= 11) | https://arxiv.org/abs/1812.04602v5 | 2026-10-23T19:38:19Z (owner-supplied PDF, sha256 022355da109e4eef72fb0cb314bea3c282fe49136f2aeae133c1ca262c275b96); abstract page 2026-11-04T09:19:34Z and 09:21:08Z, HTTP 200, v5 is the latest version |
| same paper, Table 3 (SMνR); erratum JHEP 08 (2019) 064, Table 1 | largest tabulated row, Q_max = 10, Solutions | 21546920 (no row with Q_max >= 11) | https://doi.org/10.1007/JHEP08(2019)064 | 2026-10-23T19:38:19Z (owner-supplied PDF, sha256 c6fcae4107a1e7306b58d4b0821c8b2f699e5ad06b21629e897af56b341dfcb4) |

The paper states that its lists cover "Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR". The workspace owner
supplied the two PDFs on 2026-10-23, when the contributor's machine could not reach them; they are identified by
sha256. In the panel run the arXiv abstract page (versions v1..v5, no v6) and the Zenodo record 3345889 (version
1.1.0, the last; files up to Q_max 10 for both contents) were fetched live. Snapshot, quoted table lines and hashes:
`the-record-we-beat/STATUS_RECORD.md`. The NOVELTY skeptic (`panel/novelty.md`) found no count at Q_max >= 11 for
either content in 16 arXiv API searches over 24 months, Zenodo searches, GitHub code search, `TROPHY_CASE.md`,
`known-knowns/` and the commit messages and file trees of all 908 pull-request heads of the V3R1T4S repository
(their titles and bodies could not be listed).

## Not claimed

- Only these four rows: SMnuR Q_max 20 and SM Q_max 36..38. Rows SMnuR 11..19 and SM 11..35 are other submissions;
  nothing past SMnuR 20 or SM 38 (SM 39 and 40 were counted by `mitm.c` only, not listed or claimed). The Symmetry
  column of the paper's tables is not extended.
- The lists are regenerated and hashed, not deposited. The sha256 in `object/counts.txt` pins their bytes; the
  listers in `how-we-built-it/source/` regenerate them.
- A list checker shows that every line is a distinct valid class, not that no class is missing. Completeness rests
  on the lister plus checker agreeing with an independent counter: the line count + 1 equals the count of `mitm.c`
  (a different algorithm that never lists) for all four rows, and, for the panel, the REPRODUCE skeptic's own meet-in-the-middle counter (`mycount.c`, different splits, written from the
  definition), which gave all four counts and all 40 published values. `count.c`
  was not used for these rows in the claim run (it needs about 10 GB at SM Q_max 37 and was killed by the memory
  limit); the SM 36 row of `object/counts.txt` cites a `count.c` value from run 2026-11-02-0920 that has no receipt
  in this package.
- The counting convention is the one that reproduces every published value (all 40 numbers of Tables 2 and 3);
  its wording was inferred from those values and the paper's text.
- No new physics beyond the counts: no phenomenology, model selection or interpretation of the solutions.
- The default check covers 1 of the 4 rows; `--all` covers all of them.
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
