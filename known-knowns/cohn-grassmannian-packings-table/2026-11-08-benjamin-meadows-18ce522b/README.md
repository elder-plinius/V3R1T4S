# cohn-grassmannian-packings-table, 11-4-66: minimum squared chordal distance 2.57776955247730

## What

66 four-dimensional subspaces of R^11 (object/11-4-66.txt; m = 11, n = 4) whose minimum squared chordal distance 2.57776955247730714341 (Decimal at 60 digits after orthonormalisation) is higher than the table value 2.5777278197 for the unstarred row (11, 4, 66) at https://cohn.mit.edu/grassmannian/ by 4.17e-5 and below its bound 2.5846153847.

This package contains one object only: object/11-4-66.txt. Its first line is a `#` header (cell, value, table value), which every checker here skips.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; about a second on a laptop. It checks the object's sha256, the number of subspaces and the digits per coordinate, recomputes the minimum squared chordal distance from the definition in Decimal at 60 digits, and compares it with the claimed value and with the table value (`value - table = 4.173277730714341e-5  (need >= 1e-9)`). Details and the basin test: RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Table of Grassmannian packings (Henry Cohn) | (m, n, N) = (11, 4, 66) | 2.5777278197 | https://cohn.mit.edu/grassmannian/ | 2026-11-08T02:47:23Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing: only one above the table row, below the listed bound.
- Not a new construction: a small re-polish of the posted configuration behind the table entry, in the same basin (HOW_WE_FOUND_IT.md).
- Not new to the public record today: the same configuration is in packing-records v1.3 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.24046261), our own release, published about two hours before the panel ran.
- The table keeper was told: Benjamin Meadows emailed Henry Cohn on 2026-11-08 with this and the other packing-records v1.3 rows. Nothing was uploaded to any table site.

## Credits

- Henry Cohn, Table of Grassmannian packings, https://cohn.mit.edu/grassmannian/
- N. J. A. Sloane, Table of best Grassmannian packings, https://neilsloane.com/grass/grassTab.html (the listed (11, 4, 66) packing)
- Benjamin Meadows (search lane, checking and packaging).
