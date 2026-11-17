# Anomaly-free atlas census, new rows: SM at Q_max 39 and 40

Target: `anomaly-free-atlas-qmax` (charter quarry 5, not a bank target). Family folder in the repo:
`known-knowns/anomaly-free-atlas-qmax/`. Submission id: `2026-11-08-adb991-4a46c68e` (the first 8 hex digits of the
sha256 of `object/counts.txt`). Status: `CONFIRMED_SOLUTION` (`panel/gate.md`; claim built and panelled in run
2026-11-08-0917).

## What

confirmed_scope: In the published atlas convention (family permutations within each species and overall sign identified, gcd 1, max |charge| <= Q_max, the all-zero assignment counted), the number of inequivalent anomaly-free integer U(1) charge assignments of the Standard Model fermions without right-handed neutrinos is 51237625 for Q_max = 39 and 58626334 for Q_max = 40, which goes past the published range (Q_max <= 10), with each row certified by a deterministic canonical list (count - 1 lines, sha256 in object/counts.txt) and an independent count; this skeptic reproduced the convention on all 40 published values and re-ran the independent counter at 39 and 40, but did not regenerate the lists.

In plain words: Allanach, Davighi and Melville counted the inequivalent family-dependent U(1) charge assignments of
the Standard Model fermions (with and without three right-handed neutrinos) that cancel all six gauge and
gravitational anomalies, with integer charges |F| <= Q_max, for Q_max = 1..10. This package gives two further rows
for the Standard Model fermions alone (`object/counts.txt`, copied unchanged from the claim):

| content | Q_max | count | list lines (count - 1) | sha256 of the uncompressed list | lister |
|---|---|---|---|---|---|
| SM | 39 | 51237625 | 51237624 | 0ec7c2c03acf589cbce61249d265f7352db69f43ebaaeee3d1bcc74c6f348743 | acclist |
| SM | 40 | 58626334 | 58626333 | 8d83e4182d630423ce5fa25512de702d30cb1889af96bdeaea001ebf7e673694 | acclist |

Each count also equals the independent no-list counter `mitm.c` (the `mitm.c:` field of `object/counts.txt`). The
lists (about 2.5 and 2.9 GB as text) are not stored; `how-we-built-it/source/acclist.c` regenerates them byte for
byte. `object/receipts/` holds the claim run's own outputs for both rows (checker output, sha256, lister log, a
Python-checker sample, `mitm` output), copied unchanged from the claim. Earlier rows of the same census are separate
submissions: `2026-10-23-adb991-99e267ca` (Q_max 11), `2026-10-23-adb991-81997531` (SMnuR 12..16, SM 12..31),
`2026-10-23-adb991-0728c1c8` (SMnuR 17, 18), `2026-10-28-adb991-f28c78af` (SMnuR 19, SM 32..35) and
`2026-11-04-adb991-12f0deb4` (SMnuR 20, SM 36..38).

Both rows were computed in run 2026-11-08-0917 after its pre-registration (`how-we-built-it/PREREG.md`). `mitm.c`
had given the same two counts on 2026-11-02, before any list existed. The three-skeptic panel ran in fresh contexts
in the same run; `panel/` holds byte-for-byte copies of its four files.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh          # default subset: SM 39
sh verify-it-yourself/run_checks.sh --all    # both rows
```

Expected last line: `PASS`. The default subset ran in 949 s on a 4-core machine, with another check running beside
it (`verify-it-yourself/RECEIPTS.md`); it needs gcc, python3 and well under 1 GB of memory. For every row it checks, the script first reproduces the twenty published values with the counter,
recounts the row without a list (`mitm.c`), then regenerates the list and streams the same bytes into sha256,
`wc -l` and the C checker. Details: `RUN_IT_YOURSELF.md`.

## Compared to

| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Allanach, Davighi, Melville, arXiv:1812.04602v5, Table 2 (SM) | largest tabulated row, Q_max = 10, Solutions | 23800 (no row with Q_max >= 11) | https://arxiv.org/abs/1812.04602v5 | 2026-10-23T19:38:19Z (owner-supplied PDF, sha256 022355da109e4eef72fb0cb314bea3c282fe49136f2aeae133c1ca262c275b96); abstract page 2026-11-08T09:19:36Z, HTTP 200, v5 is the latest version |

The paper states that its lists cover "Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR". Snapshot, quoted table lines
and hashes: `the-record-we-beat/STATUS_RECORD.md`. The NOVELTY skeptic (`panel/novelty.md`) found no count past Q_max 10 for this census in the 121 papers citing the
atlas (INSPIRE), the INSPIRE full-text index (0 hits for either number), arXiv API searches, Zenodo (the atlas
record's files stop at Q_max 10) and GitHub; the only related V3R1T4S entries are this contributor's own earlier
rows.

## Not claimed

- Only these two rows: SM Q_max 39 and 40. Nothing for SM + 3 nu_R past Q_max 20 (other submissions cover SMnuR
  11..20 and SM 11..38). The Symmetry column of the paper's tables is not extended.
- The lists are regenerated and hashed, not deposited. The sha256 in `object/counts.txt` pins their bytes.
- A list checker shows that every line is a distinct valid class, not that no class is missing. Completeness rests
  on the lister plus checker agreeing with an independent counter: the line count + 1 equals the count of `mitm.c`
  (a different algorithm that never lists) for both rows. For the panel, the REPRODUCE skeptic's own counter (`orbcount.c`, written from the
  definition, a different split of the same multiset-Burnside-Moebius method) gave both counts too, and its own strict
  checker passed both regenerated lists.
- The counting convention is the one that reproduces every published value (all 40 numbers of Tables 2 and 3); its
  wording was inferred from those values and the paper's text.
- The rows are SM only. The CRITERION skeptic read "with and without three right-handed neutrinos" as describing the
  census, which is extended row by row (`panel/criterion.md`); under the stricter reading that every claim must hold
  both contents, this package alone would not qualify.
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
