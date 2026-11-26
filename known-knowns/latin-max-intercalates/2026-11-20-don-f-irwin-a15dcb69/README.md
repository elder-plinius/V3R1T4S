## What

An explicit order-28 Latin square with 3324 intercalates, strictly exceeding the 2940 bar read from the comments
and proving-list headers of A092237 and A307164, and below the proven bound 5292.

## Check it yourself

From this folder, one command:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: under 5 seconds.

## Compared to

| table | cell | value | URL | fetch time |
|---|---|---|---|---|
| OEIS A092237 | a(28) | 2940 (lower bound) | https://oeis.org/A092237/a092237_2.txt | 2026-11-20T13:09Z |
| OEIS A307164 | a(28) | 2892 (lower bound) | https://oeis.org/A307164/a307164_5.txt | 2026-11-20T13:09Z |
| OEIS A092237 comments | a(28) | 2940 | https://oeis.org/A092237 | 2026-11-20T13:09Z |
| this object | order 28 | 3324 | object/square_n28_3324.txt | 2026-11-20T12:32Z |

The bar is the maximum across both sequences = 2940. This object is 3324, strictly greater by 384.
Proven upper bound for even n (Heinrich and Wallis): n^2(n-1)/4 = 5292, not exceeded.

## Not claimed

- Not claimed as the exact maximum a(28); only a lower bound of 3324.
- Not claimed for any other order. This package covers one table cell, n = 28.
- Not claimed as the first construction of its kind: the square is a direct product ("composite squares"), a
  method already used in the proving lists. What is new here is this factorisation and this value.
- No claim about diagonal Latin squares (partial win p1 of the bank entry) is made.

## Credits

- **Richard Bean** (2004): the order-n values for n <= 9 and the composite-square constructions for orders
  2^a m and 2^a m + 1 that this construction follows. Data: https://oeis.org/A092237
- **Eduard I. Vatutin**: the proving list a092237_2.txt and the diagonal-square sequence A307164, including the
  published order-14 square used as a factor here. https://oeis.org/A092237/a092237_2.txt ,
  https://oeis.org/A307164
- **Katherine Heinrich and W. D. Wallis**: "The maximum number of intercalates in a Latin square", the proven
  upper bounds n^2(n-1)/4 (even n) and n(n-1)(n-3)/4 (odd n).
- **Matthew Kwan, Ashwin Sah, Mehtaab Sawhney, Michael Simkin**: "Substructures in Latin squares", for the
  structural fact that a 2-group multiplication table carries a very large number of intercalates.
