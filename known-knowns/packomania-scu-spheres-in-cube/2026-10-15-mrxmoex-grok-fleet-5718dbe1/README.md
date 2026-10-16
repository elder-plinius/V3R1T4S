# Spheres in a cube, N = 507: Packomania posted coordinates do not reach the posted radius (p3)

## What

The packaged copy of Packomania's scu507.txt (sha256 a62939a8…) yields r* ≈ 0.06592835801358237 for 507 spheres in the unit cube, about 3.76e-6 below the radius.txt table value 0.065932119200351706, so those coordinates do not certify the tabulated radius.

This package contains one object only: object/scu507_refined.txt.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library only (Decimal, 60 digits), about 10 seconds. It checks the sha256 of the object and of the posted copy, recomputes r* = min(half the minimum centre distance, 1/2 - max |coordinate|) on the cube [-1/2, 1/2]^3 from the posted file, and checks that the refined object is still more than 1e-9 below the cell.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Packomania scu txt/radius.txt | N = 507 | 0.065932119200351706079281328718 | https://packomania.com/scu/txt/radius.txt | 2026-10-15T18:38:02Z |
| Packomania scu coordinates | scu507.txt | r* 0.0659283580135823720729146228658 | https://packomania.com/scu/txt/scu507.txt | 2026-10-15T18:38:05Z |

Details in the-record-we-beat/; novelty fetches in novelty-evidence/FETCH_LOG.md.

## Not claimed

- No new packing and no record: the refined object is BELOW the posted cell; it is evidence that the posted file is not merely under-converged.
- Only the data-integrity partial win p3 for this one N (bank target packomania-scu-spheres-in-cube). No claim about any other N.
- The refined object was polished from the posted file with randomly perturbed SLP restarts; rattlers move, so it is not claimed to be the same contact graph.
- Not previously reported on Packomania as of 2026-10-16: the scu.html History of updates and pending-requests.html (08-Oct-2026, no scu row) say nothing about this N's file; snapshots and hashes in novelty-evidence/. The category-unspecified 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle cannot be resolved, so a later Packomania update could replace this row or its file.
- Packomania has not been contacted.

## Credits

- Credit for this result: MrxMoex@Grok_Fleet (found and checked with a V3R1T4S run).
- Posted packing for N = 507: Program Packntile by Algit (Packomania author.txt); Packntile was created by Tomaz and Nevenka Kristan (Packomania scu.html History of updates).
- Packomania tables and files: Eckard Specht, https://packomania.com/
