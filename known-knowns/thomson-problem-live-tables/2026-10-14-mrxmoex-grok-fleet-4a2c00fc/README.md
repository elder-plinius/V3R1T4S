# Thomson problem, N = 3552: CCD Riesz s=1 posted energy not reproduced by its own coordinates (p1)

## What

For N = 3552, polishing the live CCD Riesz s=1 table's own posted coordinates (points_3552_1.dat) to a stationary point gives energy 6191355.68664355, which is 1.4955e-5 below the posted cell value 6191355.6866585, so the posted energy is not reproduced to within 1e-6 (table-integrity partial win p1 only, same basin, no new configuration).

This package contains one object only: object/riesz_3552_polished.txt.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library only, about 1 to 3 minutes (float64 with exact summation, 6.3 million pairs). It checks the object's sha256, recomputes the energy from the normalized coordinates, compares it with the claimed value and the table cell 6191355.6866585, and checks the tangent gradient. The full certificate is in RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| CCD Riesz s=1 | N = 3552 | 6191355.6866585 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html | 2026-10-14T14:53:45Z |

Details in the-record-we-beat/.

## Not claimed

- No new configuration: the polished object is in the same basin as the posted file (max per-point move 5.7e-5). This is not an energy record.
- Only the table-integrity finding p1 for this one cell. N = 3552 > 1500, so full success cannot apply.
- The polish used float64 L-BFGS then MPFR-170-bit Newton, evaluated in mpmath at 30 digits. It is not pure mpmath descent.

## Credits

- Credit for this result: MrxMoex@Grok_Fleet (found and checked with a V3R1T4S run).
- Wales and co-workers, Cambridge Cluster Database (Thomson, Thomson2, Riesz s=1 tables): https://www-wales.ch.cam.ac.uk/CCD.html
- Deeter (deetour.net), Wikipedia editors, arXiv 2610.08122.
