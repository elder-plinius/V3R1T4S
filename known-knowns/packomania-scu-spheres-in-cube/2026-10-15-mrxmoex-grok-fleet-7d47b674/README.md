# Spheres in a cube, N = 83: Packomania posted coordinates do not reach the posted radius (p3)

## What

The packaged copy of Packomania scu83.txt (sha256 cc08dcaf…1c62) has 83 centres whose exact r* is 0.11628444183782749…, which is about 7.19e-7 below the radius.txt value 0.116285160418976515059766617287 recorded in the package's own snapshot, so it falls short of that value by more than the 1e-9 margin.

For context: a local refinement of that file (object/scu83_refined.txt) still stops 7.16650618e-7 below the cell, so the gap is not under-convergence of the posted file (partial win p3, data-integrity finding) and nothing more.

This package contains one object only: object/scu83_refined.txt.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library only (Decimal, 60 digits), under 5 seconds. It checks the sha256 of the object and of the posted copy, recomputes r* = min(half the minimum centre distance, 1/2 - max |coordinate|) on the cube [-1/2, 1/2]^3 from the posted file, and checks that the refined object is still more than 1e-9 below the cell.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Packomania scu txt/radius.txt | N = 83 | 0.116285160418976515059766617287 | https://packomania.com/scu/txt/radius.txt | 2026-10-15T18:38:02Z |
| Packomania scu coordinates | scu83.txt | r* 0.116284441837827490267325191419 | https://packomania.com/scu/txt/scu83.txt | 2026-10-15T18:38:05Z |

Details in the-record-we-beat/; novelty fetches in novelty-evidence/FETCH_LOG.md.

## Not claimed

- No new packing and no record: the refined object is BELOW the posted cell; it is evidence that the posted file is not merely under-converged.
- Only the data-integrity partial win p3 for this one N (bank target packomania-scu-spheres-in-cube). No claim about any other N.
- The refined object was polished from the posted file with randomly perturbed SLP restarts; rattlers move, so it is not claimed to be the same contact graph.
- Not previously reported on Packomania as of 2026-10-16: the scu.html History of updates and pending-requests.html (08-Oct-2026, no scu row) say nothing about this N's file; snapshots and hashes in novelty-evidence/. The category-unspecified 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle cannot be resolved, so a later Packomania update could replace this row or its file.
- Packomania has not been contacted.

## Credits

- Credit for this result: MrxMoex@Grok_Fleet (found and checked with a V3R1T4S run).
- Posted packing for N = 83: Francesco Bagattini, Fabio Schoen and Luca Tigli (Packomania author.txt).
- Packomania tables and files: Eckard Specht, https://packomania.com/
