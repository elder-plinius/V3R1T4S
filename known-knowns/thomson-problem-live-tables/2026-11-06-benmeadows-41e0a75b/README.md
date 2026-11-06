# Thomson problem, N = 436: E* = 90020.681268073, below Deeter's 90020.71608562

## What

436 points on the unit sphere (object/thomson-436.txt) with Coulomb energy E* = 90020.681268073012 (mpmath, 30 digits), lower than the only live table value for N = 436 (Wayne Deeter's table, 90020.71608562, fetched 2026-11-06) by 0.0348; a certified strict local minimum (tangent gradient norm below 1e-26, all 869 non-rotational tangent Hessian eigenvalues positive, lowest 0.511); and a different basin from both posted N = 436 configurations (Deeter e.436.txt and CCD xyz/436.xyz polish to 90020.716085629).

This package contains one object only: object/thomson-436.txt (436 lines of x,y,z, 30 significant digits).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3; about one second. It checks the object's sha256, recomputes E* from the normalised coordinates in Decimal at
50 digits, compares it with the claimed value and with the table value, and, if numpy is installed, checks the
tangent gradient and that the tangent Hessian has 869 positive eigenvalues. The full mpmath certificate and the polish
of the posted files: RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Deeter, Thomson problem | N = 436 | 90020.71608562 | https://deetour.net/oppp/thomson/ | 2026-11-06T19:30:58Z |

CCD Thomson, CCD Thomson2, CCD Riesz s = 1 and Wikipedia have no N = 436 row. Details in the-record-we-beat/.

## Not claimed

- Not a global minimum: only a strict local minimum below every live table value.
- Only N = 436. Neighbour moves from this configuration to N = 420..452 did not beat the tables.
- No table keeper has been told yet.

## Credits

- Wayne Deeter, Thomson problem table and point files, https://deetour.net/oppp/thomson/ (the search started from his posted N = 437 configuration).
- David J. Wales and co-workers, Cambridge Cluster Database Thomson tables, https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html
- Benjamin Meadows (search lane, certification and packaging).
