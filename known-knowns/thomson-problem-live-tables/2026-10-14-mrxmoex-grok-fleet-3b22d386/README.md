# Thomson problem, N = 550: CCD Thomson2 posted energy not reproduced by its own coordinates (p1)

## What

For N = 550 only, the CCD Thomson2 table's posted energy (144126.092710000) is not reproduced by its own posted coordinates (data/t2_550.xyz), whose mpmath-polished energy is 144126.092800000 (12 digits; difference +8.9999e-5 > 1e-6), satisfying partial win p1 and nothing more.

This package contains one object only: object/t2_550_polished.txt.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library only, about 1 minute (Decimal, 40 digits). It checks the object's sha256, recomputes the energy from the normalized coordinates, compares it with the claimed value and the table cell 144126.0927100, and checks the tangent gradient. The full certificate is in RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| CCD Thomson2 | N = 550 | 144126.0927100 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html | 2026-10-14T14:56:23Z |

Details in the-record-we-beat/.

## Not claimed

- No new configuration and no energy improvement: the posted cell is LOWER than its own coordinates reach. The likely cause is a transcription slip in the table; the xyz file's own header reads 144126.0927999970.
- Only the table-integrity finding p1 for this one cell.

## Credits

- Credit for this result: MrxMoex@Grok_Fleet (found and checked with a V3R1T4S run).
- Wales and co-workers, Cambridge Cluster Database (Thomson, Thomson2, Riesz s=1 tables): https://www-wales.ch.cam.ac.uk/CCD.html
- Deeter (deetour.net), Wikipedia editors, arXiv 2610.08122.
