# cohn-harmonic-energy-spheres-dim4-32, 64-20: harmonic energy 6.68546368135722

## What

64 unit vectors in R^20 (object/64-20.txt) with harmonic energy E* = sum_{i<j} |x_i - x_j|^-18 = 6.68546368135722749098 (mpmath at 40 digits and Decimal at 60), lower than the only table energy 6.7232495038 for (N, n) = (64, 20) at https://cohn.mit.edu/harmonic-energy/ by 0.0378; a nondegenerate local minimum; not a simplex or cross polytope; and in a different basin from the 2021 data set's configuration, which polishes to 6.7232495037738.

This package contains one object only: object/64-20.txt. Its first line is a `#` header (cell, value, table value), which every checker here skips.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; about a second on a laptop. It checks the object's sha256, the number of points and the digits per coordinate, recomputes the harmonic energy from the definition in Decimal at 60 digits, and compares it with the claimed value and with the table value (`table min E - E* = 3.778582244277251e-2  (need >= 1.000e-9)`). Details and the basin test: RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Table of harmonic energies (Henry Cohn) | (N, n) = (64, 20) | 6.7232495038 | https://cohn.mit.edu/harmonic-energy/ | 2026-11-08T02:47:16Z |

Details in the-record-we-beat/.

## Not claimed

- Not a global minimum or a proven optimum: only a configuration below the table, in a different basin from the posted one.
- Only (64, 20). The lane's (64, 19) improvement used as a seed is not part of this claim.
- Not new to the public record today: the same configuration is in packing-records v1.3 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.24046261), our own release, published about two hours before the panel ran.
- The table keeper was told: Benjamin Meadows emailed Henry Cohn on 2026-11-08 with this and the other packing-records v1.3 rows. Nothing was uploaded to any table site.

## Credits

- Henry Cohn, Table of harmonic energies, https://cohn.mit.edu/harmonic-energy/
- B. Ballinger, G. Blekherman, H. Cohn, N. Giansiracusa, E. Kelly and A. Schürmann, Experimental study of energy-minimizing point configurations on spheres, Experiment. Math. 18 (2009); data set https://hdl.handle.net/1721.1/130937 (the posted (64, 20) configuration)
- Benjamin Meadows (search lane, checking and packaging).
