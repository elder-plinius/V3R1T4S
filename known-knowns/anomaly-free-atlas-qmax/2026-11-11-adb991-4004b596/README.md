# Anomaly-free atlas census, new rows: SM at Q_max 41 and 42

Target: `anomaly-free-atlas-qmax` (charter quarry 5, not a bank target). Family folder in the repo:
`known-knowns/anomaly-free-atlas-qmax/`. Submission id: `2026-11-11-adb991-4004b596` (the first 8 hex digits of the
sha256 of `object/counts.txt`). Status: `CONFIRMED_SOLUTION` (`panel/gate.md`; claim built and panelled in run
2026-11-11-0917; gate written in run 2026-11-12-0008 after the owner stopped the panel run).

## What

confirmed_scope: In the convention of the anomaly-free atlas (arXiv:1812.04602 and its erratum; all 40 published values reproduced), the number of inequivalent anomaly-free integer U(1) charge assignments of the Standard Model fermions without right-handed neutrinos is 66526761 for Q_max = 41 and 79174540 for Q_max = 42 (zero assignment included), each recounted here by the independent meet-in-the-middle counter and certified by a regenerable canonical list of count - 1 lines identified by sha256, subject to the separate regeneration check of those lists.

In plain words: Allanach, Davighi and Melville counted the inequivalent family-dependent U(1) charge assignments of
the Standard Model fermions (with and without three right-handed neutrinos) that cancel all six gauge and
gravitational anomalies, with integer charges |F| <= Q_max, for Q_max = 1..10. This package gives two further rows
for the Standard Model fermions alone (`object/counts.txt`, copied unchanged from the claim):

| content | Q_max | count | list lines (count - 1) | sha256 of the uncompressed list | lister |
|---|---|---|---|---|---|
| SM | 41 | 66526761 | 66526760 | ad5133b7fcbe5ec91cc5416bda0b5a8629e0b85ba5d2d4c0aa89ef4f4282f6ec | acclist |
| SM | 42 | 79174540 | 79174539 | 8d6d0fcd99099ba8b46071ba4a6e1051fa8fcb1fb165f8c55c7f150bcbed6df2 | acclist |

Each count also equals the independent no-list counter `mitm.c` (the `mitm.c:` field of `object/counts.txt`). The
lists (about 3.3 and 4 GB as text) are not stored; `how-we-built-it/source/acclist.c` regenerates them byte for
byte. `object/receipts/` holds the claim run's own outputs for both rows (checker output, sha256, lister log, a
Python-checker sample, `mitm` output), copied unchanged from the claim. Earlier rows of the same census are separate
packages: `2026-10-23-adb991-99e267ca` (Q_max 11), `2026-10-23-adb991-81997531` (SMnuR 12..16, SM 12..31),
`2026-10-23-adb991-0728c1c8` (SMnuR 17, 18), `2026-10-28-adb991-f28c78af` (SMnuR 19, SM 32..35) and
`2026-11-04-adb991-12f0deb4` (SMnuR 20, SM 36..38) and `2026-11-08-adb991-4a46c68e` (SM 39, 40).

Both rows were computed in run 2026-11-11-0917 after its pre-registration (`how-we-built-it/PREREG.md`). `mitm.c`
was first rerun on the certified rows SM 36..40, which it reproduced. The three-skeptic panel ran in fresh contexts
in the same run; `panel/` holds byte-for-byte copies of its four files.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh          # default subset: SM 41
sh verify-it-yourself/run_checks.sh --all    # both rows
```

Expected last line: `PASS`. The default subset (SM 41) ran in 1447 s on a 4-core machine, with other jobs running beside it
(`verify-it-yourself/RECEIPTS.md`); it needs gcc, python3 and well under 1 GB of memory. For every row it checks, the script first reproduces the twenty published values with the counter,
recounts the row without a list (`mitm.c`), then regenerates the list and streams the same bytes into sha256,
`wc -l` and the C checker. Details: `RUN_IT_YOURSELF.md`.

## Compared to

| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Allanach, Davighi, Melville, arXiv:1812.04602v5, Table 2 (SM) | largest tabulated row, Q_max = 10, Solutions | 23800 (no row with Q_max >= 11) | https://arxiv.org/abs/1812.04602v5 | 2026-10-23T19:38:19Z (owner-supplied PDF, sha256 022355da109e4eef72fb0cb314bea3c282fe49136f2aeae133c1ca262c275b96); abstract page 2026-11-08T09:19:36Z, HTTP 200, v5 is the latest version |

The paper states that its lists cover "Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR". Snapshot, quoted table lines
and hashes: `the-record-we-beat/STATUS_RECORD.md`. The NOVELTY skeptic (`panel/novelty.md`) found no count past Q_max 10 for this census in the 121 papers citing the
atlas (INSPIRE), the INSPIRE full-text index (0 hits for either number; a published value as positive control),
arXiv API searches, Zenodo (the atlas record's files stop at Q_max 10) and GitHub.

## Not claimed

- Only these two rows: SM Q_max 41 and 42. Nothing for SM + 3 nu_R past Q_max 20 (other packages cover SMnuR
  11..20 and SM 11..40). The Symmetry column of the paper's tables is not extended.
- The lists are regenerated and hashed, not deposited. The sha256 in `object/counts.txt` pins their bytes.
- A list checker shows that every line is a distinct valid class, not that no class is missing. Completeness rests
  on the lister plus checker agreeing with an independent counter: the line count + 1 equals the count of `mitm.c`
  (a different algorithm that never lists) for both rows. For the panel, the REPRODUCE skeptic regenerated both lists in full
  through the claim's checker and its own strict checker, and its own counter (`mycount.c`, written from the definition,
  a different split of the same multiset-Moebius-Burnside method) gave both counts; its explicit Python lister is
  byte-identical to `acclist` for Q_max <= 12.
- The counting convention is the one that reproduces every published value (all 40 numbers of Tables 2 and 3); its
  wording was inferred from those values and the paper's text.
- The rows are SM only. The CRITERION skeptic read "with and without three right-handed neutrinos" as describing the
  census, which is extended row by row (`panel/criterion.md`); under the stricter reading that every claim must hold
  both contents, this package alone would not qualify.
- The list checkers (`checklist.c`, `check_list.py`) do not enforce the exact line format (they accept extra
  whitespace and blank lines); the sha256 pins the bytes, and the REPRODUCE skeptic's strict checker passed both lists.
- No new physics beyond the counts: no phenomenology, model selection or interpretation of the solutions.
- The PDFs used for the comparison were supplied by the workspace owner and checked against their own hashes, not
  fetched from arXiv or Springer.
- No pull request, issue or message was sent to the authors or anyone else by the run.

## Credits

- B. C. Allanach, J. Davighi and S. Melville, "An anomaly-free atlas: charting the space of flavour-dependent
  gauged U(1) extensions of the Standard Model", JHEP 02 (2019) 082, https://arxiv.org/abs/1812.04602 , erratum
  JHEP 08 (2019) 064, https://doi.org/10.1007/JHEP08(2019)064 , data and program
  http://doi.org/10.5281/zenodo.3345889 (the census, its convention and the table compared against).
- Physlib, https://github.com/leanprover-community/physlib (its formal anomaly conditions were used in an earlier run
  of this target to check the six equations).
- GCC.
- V3R1T4S, https://github.com/elder-plinius/V3R1T4S (the run protocol, panel and gate).
- Contributor: ADB991 (an AI-agent run under the V3R1T4S kit; see `HOW_WE_FOUND_IT.md` and `prompt/`).
