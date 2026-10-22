# Packing of 739 equal spheres in the unit cube (Packomania scu, N = 739)

## What

The point file in this cell is a valid cube packing with exact feasible radius r* = 0.0586275441666459796140567 (checked here), strictly above both the live Packomania scu row for N=739 and the best live row at any larger N up to 1000, with the posted file non-isometric; whether the unresolved Moki and Julio bundle or a later table revision already holds a higher value is not decidable from the folder.

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
| Packomania scu `radius.txt` | N = 739 | 0.058531064606 | https://packomania.com/scu/txt/radius.txt | 2026-10-19T05:37:23Z (HTTP 200) |
| Packomania scu `radius.txt`, largest row at any N' from 739 up to 1000 (the propagated bar) | N' = 740 and 741 | 0.058627036756; the claim is above it by 5.1e-7 | https://packomania.com/scu/txt/radius.txt | 2026-10-19T05:37:23Z (HTTP 200) |
| Packomania scu page, History of updates | N = 739 | last entry 17-Oct-2026 ("The table has been reorganized"); no 2026 entry names N = 739, while neighbours were updated that day | https://packomania.com/scu/scu.html | 2026-10-19T05:37:24Z (HTTP 200) |
| Packomania pending requests | scu | no scu entry; the category-unspecified 26-Sep-2026 bundle of 4666 candidates is still listed and cannot be read | https://packomania.com/pending-requests.html | 2026-10-19T05:37:25Z (HTTP 200) |
| Packomania posted file for N = 739 | N = 739 | a different, stale arrangement (largest difference of sorted pairwise distances about 7.7e-2) | https://packomania.com/scu/txt/scu739.txt | 2026-10-19T04:35:18Z (HTTP 200, triage fetch) |
| Moki and Julio v2.7 manifest (Zenodo record 22986800) | scu N = 739 | 0.0586073866758; the claim is above it by 2.0e-5 | https://zenodo.org/api/records/22986800 | 2026-10-19T05:37:46Z (record, HTTP 200); manifest read from the zip, 05:38:21Z to 05:48:07Z |
| V3R1T4S `TROPHY_CASE.md` and known-knowns (scu folder) | scu N = 739 | no entry for this N | https://github.com/elder-plinius/V3R1T4S | 2026-10-19T05:37:22Z (HTTP 200) |

Value of this package: r* = 0.0586275441666459796140567, above the live row for N = 739 by 9.65e-5 and above the propagated bar by 5.1e-7. Snapshot metadata with HTTP status and page sha256: `the-record-we-beat/README.md`. The panel's novelty report is `panel/novelty.md`.

## Not claimed

- The margin over the propagated bar is small. The live row for N = 739 (0.058531064606) is lower than the rows for some larger N (the table was reorganized on 17-Oct-2026), and a packing of N spheres of the larger radius follows by deleting spheres from a posted larger packing. The bar the panel used is therefore the largest live row at any N' from 739 up to 1000, 0.058627036756 at N' = 740 and 741, and the claim is above that bar by only 5.1e-7. Relative to the row for N = 739 itself the gain (9.65e-5) is much larger, but that row is stale.
- The object is not a value that follows from the table by deleting spheres alone: it was made from the posted N = 741 packing by deleting 2 spheres and re-jamming, and its radius is strictly above the radius the larger posted packing gives. The panel counted it as a separate, if small, record. The non-isometry clause was checked against the posted file for N = 739 (a different arrangement), not against the posted N = 741 packing it was derived from.
- Whether the unresolved Moki and Julio bundle (26-Sep-2026, 4666 candidates, category not specified) or a later revision of the table already holds a higher value is not decidable from this folder. The published v2.7 manifest is lower (0.0586073866758); the queued bundle could not be read. The table was rewritten on 04, 05, 06, 08 and 17 October 2026, so the live row for N = 739 could still change.
- Only rows with N' up to 1000 were examined for the propagated bar. Nothing is claimed for any other N, and no optimality is claimed.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Credits

- **Eckard Specht** and the Packomania site (https://packomania.com): the table of best known radii for equal spheres in the cube and the posted coordinate files; the bank text names Specht among the table's authors.
- **Vidit Patankar**: the posted N = 741 packing the object was derived from, and the N = 740 packing, whose radius is the largest at N' >= 739 (both credited to him in Packomania's scu/txt/author.txt, fetched 2026-10-19T22:52:53Z). This package improves on that radius by about 5.1e-7. Credit added after an independent reviewer (DmitrL-dev) pointed out the omission on this pull request.
- **Moki and Julio**: the v2.7 packing collection on Zenodo (record 22986800, https://zenodo.org/api/records/22986800) whose manifest was compared against.
- Contributor credit: `calgulbenkian`. The configuration was found by an AI search agent (Gemini) working for the contributor.
