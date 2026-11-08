# spherical-codes-cohn-table, 29-727: maximum pairwise cosine 0.23650296945765

## What

727 unit vectors in R^29 (object/29_727.txt) whose maximum pairwise cosine c* = 0.23650296945765818255 (Decimal and mpmath at 50 or more digits) is lower than the spherical-codes.org table cosine 0.240054045231 for (d, N) = (29, 727) by 0.00355; the row has no proven-optimal mark and no "needs more optimization" note, and d = 29 is outside the kissing-number range 9..23.

This package contains one object only: object/29_727.txt. Its first line is a `#` header (cell, value, table value), which every checker here skips.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; about two seconds on a laptop. It checks the object's sha256, the number of vectors and the digits per coordinate, recomputes the maximum pairwise cosine from the definition in Decimal at 60 digits, and compares it with the claimed value and with the table value (`table cos - c* = 3.551075773341817e-3  (need >= 1e-10)`). Details and the basin test: RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Table of spherical codes (spherical-codes.org) | (d, N) = (29, 727) | 0.240054045231 | https://spherical-codes.org/plain | 2026-11-08T02:46:53Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal code: only a code better than the table row.
- Only (29, 727). Other rows from the same lane are in packing-records v1.3 and are not part of this claim.
- Not new to the public record today: the same configuration is in packing-records v1.3 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.24046261), our own release, published about two hours before the panel ran.
- The table keeper was told: Benjamin Meadows emailed Henry Cohn on 2026-11-08 with this and the other packing-records v1.3 rows. Nothing was uploaded to any table site.

## Credits

- Henry Cohn and co-maintainers, Table of spherical codes, https://spherical-codes.org/
- Azmi C. Özgen, the posted (29, 727) code the table lists (2026)
- Benjamin Meadows (search lane, checking and packaging).
