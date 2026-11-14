# cohn-harmonic-energy-spheres-dim4-32, 61-21: harmonic energy 4.10394830243431

## What

61 unit vectors in R^21 (object/61-21.txt) with harmonic energy E* = sum_{i<j} |x_i - x_j|^-19 = 4.10394830243431489526 (mpmath at 40 digits and Decimal at 60), lower than the only table energy 4.1191657308 for (N, n) = (61, 21) at https://cohn.mit.edu/harmonic-energy/ by 0.0152; not a simplex or cross polytope; and in a different basin from the 2021 data set's configuration, which polishes to 4.1191657307872.

This package contains one object only: object/61-21.txt. Its first line is a `#` header (cell, value, table value), which every checker here skips.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; about a second on a laptop. It checks the object's sha256, the number of points and the digits per coordinate, recomputes the harmonic energy from the definition in Decimal at 60 digits, and compares it with the claimed value and with the table value (`table min E - E* = 1.521742836568510e-2  (need >= 1.000e-9)`). Details and the basin test: RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Table of harmonic energies (Henry Cohn) | (N, n) = (61, 21) | 4.1191657308 | https://cohn.mit.edu/harmonic-energy/ | 2026-11-08T02:47:16Z |

Details in the-record-we-beat/.

## Not claimed

- Not a global minimum or a proven optimum: only a configuration below the table, in a different basin from the posted one.
- Only (61, 21).
- Not new to the public record today: the same configuration is in packing-records v1.3 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.24046261), our own release, published about two hours before the panel ran.
- The table keeper was told: Benjamin Meadows emailed Henry Cohn on 2026-11-08 with this and the other packing-records v1.3 rows. Nothing was uploaded to any table site.

## Credits

- Henry Cohn, Table of harmonic energies, https://cohn.mit.edu/harmonic-energy/
- B. Ballinger, G. Blekherman, H. Cohn, N. Giansiracusa, E. Kelly and A. Schürmann, Experimental study of energy-minimizing point configurations on spheres, Experiment. Math. 18 (2009); data set https://hdl.handle.net/1721.1/130937 (the posted (61, 21) configuration)
- Benjamin Meadows (search lane, checking and packaging).
