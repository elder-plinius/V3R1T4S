# Exact Count `A049507(7) = 781760467628825425251897322894619609502208` for Domino Tilings of `P_6 x P_6 x P_7`

## What

The package's value A049507(7) = 781760467628825425251897322894619609502208 (perfect matchings of P_6 x P_6 x P_7), checked in this panel by the package's own checks (parity, D_4 symmetry, 25-prime CRT bounds, the third-order calibration run reproducing A049507(0..6) and A028446(1..3), and two fresh-prime residues, which I also recomputed from the claimed integer), is not in the OEIS A049507 DATA as fetched on 2026-11-18T17:31Z, and meets p1's three literal clauses, with the two discovery engines using different vertex orders but being the same family of method and not rerun here.

## Check It Yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS` (runs in about `3` minutes on `4` CPU threads using `<= 2.12 GiB` RAM, requiring only Python 3 standard library and a C99 compiler `cc`). The standalone verifier checks `object/a049507_7_certificate.json` from first principles:
1. Verifies the 25-prime Chinese Remainder Theorem reconstructions from Engine 1 (`10` 31-bit primes, product `~ 2^310.00 > 3^4 * 4^26 * 5^56 * 6^40`) and Engine 2 (`15` disjoint primes, product `~ 2^215.17 > Bregman bound 2^173.89`).
2. Independently constructs the `126 x 126` biadjacency matrix of `P_6 x P_6 x P_7` over `GF(2)` and verifies `rank = 120` and `det = 0 == A049507(7) mod 2`.
3. Independently computes exact `H`-invariant matching counts `|Fix(H)|` for all `9` nontrivial subgroups of the horizontal dihedral group `D_4 <= Aut(P_6 x P_6 x P_7)` (`|D_4| = 8`), certifying `A049507(7) == 0 (mod 8)` (`97720058453603166350467775353912955052944` free `D_4`-orbits), plus the `z`-reflection factorization `|Fix(zeta)| = A049507(1) * A049507(3) = 385164950209515287552`.
4. Compiles a third zero-shared-code C99 verifier (`verify-it-yourself/verify_fresh_primes.c`) using a third distinct vertex order (`Order C`: `5x + 4y + 5z`), reproduces `A028446(1..3)` (including full `6 x 6 x 6`), `A049507(0..5)`, and `A028454(1..7)`, and verifies `A049507(7)` modulo two fresh primes (`21713` and `21683`) absent from both discovery engines.

## Compared To

- **Primary status sources:**
  - OEIS `A049507` (https://oeis.org/A049507, fetched `2026-11-18T07:09:01Z` and re-fetched `2026-11-18T08:15:03Z`, HTTP `200`, SHA-256 `02872f1bdd14ba0cc8a7f8529821765c2596ce4167f4ff66c73dc97362a71888`; JSON API https://oeis.org/search?q=id:A049507&fmt=json, HTTP `200`, SHA-256 `3133d67655ba11512c967f929719ddefe0b056dc109fcfd5f577b35029e091eb`).
  - OEIS `A028446` (https://oeis.org/A028446, fetched `2026-11-18T07:09:01Z` and re-fetched `2026-11-18T08:15:04Z`, HTTP `200`, SHA-256 `d397afd838e70b668e65942273252dc1c79bfcbe866fb9a281339d018c2923a7`).
- **Cell:** `A049507(7)` (number of perfect matchings of `P_6 x P_6 x P_7`, enumerated partial win `p1` of `cube-domino-tilings-a028446-8x8x8`).
- **Existing table value:** `unlisted` (`A049507` lists `n = 0..5` ending at `a(5) = 216388579168758145017797108072`, and `A028446(3)` gives `a(6) = 417898687046465734392674187695263185`).
- **Our certified value:** `A049507(7) = 781760467628825425251897322894619609502208` (`42` decimal digits).

## Not Claimed

- We do **not** claim `A028446(4)` (the `8 x 8 x 8` cube full moonshot target).
- We do **not** claim `P_6 x P_8 x P_8` (`p2`) or `A049507(8)` (`P_6 x P_6 x P_8`).
- Only the single sequence term `A049507(7) = 781760467628825425251897322894619609502208` is claimed in this package.

## Credits

- **Per Hakan Lundow**, *Computation of matching polynomials and the number of 1-factors in polygraphs* (Umea Univ. Research Report No. 12, 1996) and *Enumeration of matchings in polygraphs* (1998, https://web.archive.org/web/20171118074340/http://www.theophys.kth.se/~phl/Text/1factors2.pdf) — author of OEIS sequences `A049507`, `A028446`, and `A028454`, and computation of `A049507(0..5)` and `A028446(1..2)`.
- **Steven Kotlarz**, *A028446(3) — Mathematical Proof and Code Walkthrough* (29 Mar 2026, https://oeis.org/A028446/a028446.md.txt) — broken-profile diagonal DP computing `A028446(3) = A049507(6) = 417898687046465734392674187695263185`, reproduced by all three of our engines as the `6 x 6 x 6` calibration benchmark.
- **N. J. A. Sloane** and the **OEIS Foundation** (https://oeis.org/A049507, https://oeis.org/A028446, https://oeis.org/A028454) — sequence curation, references, and **Alois P. Heinz** (`A028454` table).
- **P. W. Kasteleyn**, *The statistics of dimers on a lattice: I. The number of dimer arrangements on a quadratic lattice*, Physica 27 (1961), 1209–1225 (https://doi.org/10.1016/0031-8914(61)90063-5), and **H. N. V. Temperley and M. E. Fisher**, *Dimer problem in statistical mechanics — an exact result*, Phil. Mag. 6 (1961), 1061–1063 (https://doi.org/10.1080/14786436108243366) — planar `6 x 6` dimer count `A049507(1) = 6728`.
- **L. M. Bregman**, *Some properties of nonnegative matrices and their permanents*, Soviet Math. Dokl. 14 (1973), 945–949 — permanent upper bound used to size unconditional CRT moduli.
- Contributor credit: `calgulbenkian`.
