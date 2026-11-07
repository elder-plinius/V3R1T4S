# Anomaly-free atlas past Q_max = 10: exact counts at Q_max = 11 for the SM (37006) and the SM plus three right-handed neutrinos (45378378)

Target: `anomaly-free-atlas-qmax` (a charter quarry, not a bank target). Family folder in the repo:
`known-knowns/anomaly-free-atlas-qmax/`. Submission id: `2026-10-23-adb991-99e267ca` (the first 8 hex digits of the
sha256 of `object/counts.txt`). Status: `CONFIRMED_SOLUTION` (`panel/gate.md`).

## What

confirmed_scope: In the counting convention that exactly reproduces all ten published Allanach-Davighi-Melville counts available to the claim (SM Q_max 1, 3, 5, 7, 10; SMnuR Q_max 6-10), the number of inequivalent anomaly-free integer U(1) charge assignments with |F| <= 11 is 37006 for the SM and 45378378 for the SM plus three right-handed neutrinos, certified by the included SM list (37005 nonzero classes) and by an SMnuR list of 45378377 nonzero classes that is deterministically regenerated and identified by sha256 f4e16ec8...96dbdaf4, one step beyond Q_max = 10, the largest ADM value according to the claim's secondary (not byte-exact) source.

In plain words: a new U(1) gauge symmetry acting on the Standard Model fermions with family-dependent integer
charges F, |F| <= Q_max, must satisfy six anomaly cancellation conditions (written out in
`how-we-built-it/claim/CLAIM.md`). Allanach, Davighi and Melville counted the inequivalent solutions for
Q_max = 1..10. This package gives the next row, Q_max = 11, for both field contents.

| content | Q_max | count (published convention) | list lines (count - 1) | sha256 of the uncompressed list |
|---|---|---|---|---|
| SM (15 charges) | 11 | 37006 | 37005 | 723e21fb6c46023dcfe04c77eee556a2759066277d57c7ab092c430b80667d68 (`object/SM_q11.txt.gz`) |
| SM + 3 nu_R (18 charges) | 11 | 45378378 | 45378377 | f4e16ec8613a78ef6437fde6c43e56320fbb6bc901fa072c0889667d96dbdaf4 (regenerated, not stored) |

The object is `object/counts.txt` (copied unchanged from the claim) plus the stored SM list `object/SM_q11.txt.gz`.
The SMnuR list (417 MB as gzip) is not stored; `how-we-built-it/source/acclist.c` regenerates it byte for byte.

Convention ("inequivalent"): count = 1 + the number of nonzero integer solutions with |F| <= Q_max and gcd 1, modulo
independent permutations of the three families within each species and the overall sign F -> -F (the 1 is the
all-zero assignment, which the paper's captions say every row contains). It was fixed by calibration when the run was
made. Note on the scope sentence above: it was written when the published values were known only from search-tool
text. Since then the owner supplied the paper and the erratum, a fresh NOVELTY skeptic read them (largest published
Q_max = 10 for both contents), and all 40 published values (Solutions and Symmetry columns, Q_max 1..10, both
contents) were found to match this convention (`the-record-we-beat/`). The scope sentence is kept word for word as
the gate wrote it.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh      # from this folder; needs gcc, python3, sha256sum (or shasum)
```

Expected last line: `PASS`. The default checks both rows: the stored SM list, the twenty published values as a
calibration of the counter, a recount of both rows without listing, and both lists regenerated and streamed into
sha256, `wc -l` and the C checker (the Python checker also reads the SM lists). It took the time recorded in
`verify-it-yourself/RECEIPTS.md` on a 4-core machine pinned to 3 cores (about 2 minutes); the SMnuR lister needs about
2.5 GB of memory. Details and the commands behind it: `RUN_IT_YOURSELF.md`.

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

- Only Q_max = 11. Larger rows of the same census are separate submissions.
- The counting convention is the one that reproduces every published value (all 40 numbers of Tables 2 and 3);
  its wording was inferred from those values, not quoted from the paper.
- The SMnuR list is a deterministic regeneration identified by its sha256, not a deposited file. The SM list is
  stored. Completeness rests on the agreement of the list's line count with an independent counter
  (count.c + conventions.py, a different algorithm), as the CRITERION skeptic accepted.
- The PDFs used for the comparison were supplied by the workspace owner and checked against their own hashes, not
  fetched from arXiv or Springer. No live fetch of the Zenodo record was possible, so a later Zenodo version with
  larger Q_max cannot be excluded by a direct read (none was found by search).
- The paper's program (on Zenodo) could produce Q_max = 11 for anyone who runs it; the claim is that no count at
  Q_max = 11 was published, not that it was hard to compute.
- The C checker `verify-it-yourself/checklist.c` was written in a later run of the same target
  (2026-10-18-0817) and validated there against the Python checker on 29 lists and 7 negatives; the panel of this
  claim used the Python checker (`verify-it-yourself/check_list.py`) and its own checkers.
- No pull request, issue or message was sent to the authors or anyone else.

## Credits

- B. C. Allanach, J. Davighi and S. Melville, "An anomaly-free atlas: charting the space of flavour-dependent
  gauged U(1) extensions of the Standard Model", JHEP 02 (2019) 082, https://arxiv.org/abs/1812.04602 , erratum
  JHEP 08 (2019) 064, https://doi.org/10.1007/JHEP08(2019)064 , data and program
  http://doi.org/10.5281/zenodo.3345889 (the census, its convention and the table compared against).
- Physlib, https://github.com/leanprover-community/physlib (its formal anomaly conditions `SMRHN.PlusU1 3` were
  used in the run to check the six equations; see `HOW_WE_FOUND_IT.md`).
- V3R1T4S, https://github.com/elder-plinius/V3R1T4S (the run protocol, panel and gate).
- Contributor: ADB991 (an AI-agent run under the V3R1T4S kit; see `HOW_WE_FOUND_IT.md` and `prompt/`).
