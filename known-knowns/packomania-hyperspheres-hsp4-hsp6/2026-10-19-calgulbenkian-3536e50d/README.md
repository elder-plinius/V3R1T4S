# Packing of 170 equal balls in the unit 4-ball (Packomania hsp4, N = 170)

## What

A 170-point packing in the unit 4-ball with exact feasible radius 0.2156450594683900081 (checked here), above the live Packomania hsp4 row for N=170 (0.215589695168) by 5.5e-5 and non-isometric to the posted file; the unresolved Moki and Julio bundle could still hold an equal or higher value.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: a few seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Packomania hsp4 `radius.txt` | N = 170 | 0.215589695168 (N = 169: 0.215785895566; N = 171: 0.215441346347; the largest row at any N' from 170 to 300 is the N = 170 row) | https://packomania.com/hsp4/txt/radius.txt | 2026-10-19T05:37:26Z (HTTP 200) |
| Packomania hsp4 page, History of updates | N = 170 | last entries 04, 05, 06 Jul 2025 only; no 2026 entry | https://packomania.com/hsp4/hsp4.html | 2026-10-19T05:37:27Z (HTTP 200) |
| Packomania pending requests | hsp4 | no hsp4, hsp5 or hsp6 entry; the category-unspecified 26-Sep-2026 bundle of 4666 candidates is still listed | https://packomania.com/pending-requests.html | 2026-10-19T05:37:25Z (HTTP 200) |
| Packomania posted file for N = 170 | N = 170 | radius 0.215589695168; a different arrangement (largest difference of sorted pairwise distances 9.0e-3) | https://packomania.com/hsp4/txt/hsp4-170.txt | 2026-10-19T04:37:21Z (HTTP 200, triage fetch) |
| Moki and Julio v2.7 manifest (Zenodo record 22986800) | hsp4 N = 170 | 0.2155917530134953 (the largest manifest value at N' from 170 up is this row); the claim is above it by 5.3e-5 | https://zenodo.org/api/records/22986800 | 2026-10-19T05:37:46Z (record, HTTP 200); manifest read from the zip, 05:38:21Z to 05:48:07Z |
| Cohn's table of spherical codes (4D rows, converted to ball packings) | N from 170 up | best converted value 0.20897 (the 169-point code plus a central ball), far below the claim | https://spherical-codes.org/plain | 2026-10-19T05:42:49Z (HTTP 200) |
| V3R1T4S `TROPHY_CASE.md` and known-knowns | hsp4 N = 170 | no entry; the only matching item is the contributor's own closed pull request #106 (same radius) | https://github.com/elder-plinius/V3R1T4S | 2026-10-19T05:37:22Z (HTTP 200) |

Value of this package: r* = 0.2156450594683900081281903, above the live row by 5.5364e-5. Snapshot metadata with HTTP status and page sha256: `the-record-we-beat/README.md`. The panel's novelty report is `panel/novelty.md`.

## Not claimed

- No optimality claim. This is one explicit configuration with a verified radius, not a proof that no better packing exists for N = 170 in the 4-ball.
- The unresolved Moki and Julio bundle (26-Sep-2026, 4666 candidates, category not specified, still in Packomania's pending list) could still hold an equal or higher value for hsp4 N = 170. The panel could read only the published v2.7 manifest, which is lower (0.2155917530134953), and not the queued bundle. The live table may also change after the fetch times given above.
- Nothing is claimed for any other N, for hsp5 or hsp6, or for the N = 301 extension that the contributor's code also produced.
- The radius is computed from the coordinates (half the smallest pair distance or the wall distance, whichever is smaller; the wall binds). The header line of the object file gives a radius that differs from the exact value in the 17th digit; the header is not used.
- The check of non-isometry with the posted Packomania file was done by the builder and the panel with the posted file; that third-party file is not shipped (see `RUN_IT_YOURSELF.md` to redo it).
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Filing history

This is a refile of the contributor's earlier pull request #106 (the same object: same r* = 0.2156450594683900081281903, same file sha256). Pull request #106 was closed unmerged on 2026-10-14 in the bulk close of about thirty early pull requests during a handoff between sessions, not for a defect.

## Credits

- **Eckard Specht** and the Packomania site (https://packomania.com): the table of best known radii for equal balls in the unit 4-ball and the posted coordinate files; the bank text names Specht as the author of almost all rows of the hsp tables. The record compared against and the starting packings of the construction (N = 166 and N = 169) are his posted files.
- **Moki and Julio**: the v2.7 packing collection on Zenodo (record 22986800, https://zenodo.org/api/records/22986800) whose manifest was compared against.
- **Cohn**: the table of spherical codes at https://spherical-codes.org/plain, compared against after conversion to ball packings.
- Contributor credit: `calgulbenkian`. The configuration was found by an AI search agent (Gemini) working for the contributor.
