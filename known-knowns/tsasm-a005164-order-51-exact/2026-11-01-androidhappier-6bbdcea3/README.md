# A005164(25): totally symmetric alternating sign matrices of order 51

## What

Confirmed scope, quoted word for word from panel/gate.md:

> A005164(25), the number of 51 x 51 alternating sign matrices invariant under all eight symmetries of the square, equals 30533896243799704017627552102998416 by exact transfer-matrix enumeration in two programs with different sweep orders and disjoint prime sets (plus exact mod-2^128 arithmetic). Both programs also reproduce the published a(0)..a(24), and the value was absent from OEIS A005164 DATA when re-fetched at 2026-11-01T03:03:53Z.

The value is in object/A005164_25.txt as one line, `25 30533896243799704017627552102998416` (sha256
6bbdcea3372a91c60f07506f99ec6b9660bc885517e741f43460352421d6b745). a(n) counts the (2n+1) x (2n+1) alternating sign
matrices invariant under all eight symmetries of the square (OEIS offset 0, so n = 25 is order 51).

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. It takes about 1-3 minutes on a laptop (Python 3, standard library only, one core). It
recomputes a(0..25) with exact integers by a height-function DP written from the definition, checks a(0..24)
against the published terms and a(0..8) against a brute-force count of the matrices themselves, and compares
a(25) with the object. Details: RUN_IT_YOURSELF.md and verify-it-yourself/RECEIPTS.md.

## Compared to

| table | cell | table value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A005164 (DATA and b-file) | a(25), order 51 | absent (DATA and b-file end at a(24) = 52893528399758443649956432899616; no pending drafts) | 30533896243799704017627552102998416 | 2026-11-01T02:07:52Z; re-fetched 03:00Z, 03:03:53Z, 03:08:49Z and 03:09:51Z, unchanged |

URL: https://oeis.org/A005164. The snapshot record (fetch times, HTTP status, headers, sha256s, the extracted cell)
is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only a(25). a(26) = 21803726922561140477661463807927741216 appears in how-we-built-it/result/ as a by-product
  (two programs agree on it) but is not part of this package. Nor are the run's single-program values a(27..42).
- Not a new formula and not a proof of any formula. The count is an exact enumeration. It does not evaluate the
  Hagendorf-Lienardy multiple-contour-integral formula (which arXiv:2509.09209 proves), and it says nothing about that
  formula's correctness at n = 25.
- No claim that a(0..24) were wrong. They are reproduced exactly, so there are no disagreements to report.
- The mod-3 pattern seen in the run's data (a live lead) is not claimed.
- panel/ holds the panel files as written, except that two machine-local paths were replaced. panel/REDACTIONS.md
  lists both changes and the original files' sha256.

## Credits

- OEIS A005164 and its contributors, including M. Bousquet-Melou and L. Habsieger (early terms) and Jean Lienardy
  (a(14)-a(24), 2020 and 2022): https://oeis.org/A005164
- C. Hagendorf and J. Lienardy, arXiv:2008.03220 (the conjectured contour-integral formula), and arXiv:2509.09209
  (Lienardy et al., its proof): https://arxiv.org/abs/2008.03220, https://arxiv.org/abs/2509.09209
- D. P. Robbins, Symmetry classes of alternating-sign matrices (2000), https://arxiv.org/abs/math/0008045, and
  R. P. Stanley (1986), who listed the class. G. Kuperberg's VSASM formula (OEIS A005156) was used as a
  sanity check of half of the reduction.
- James Guillochon's transfer-matrix counts of the neighbouring class A005162, which suggested the approach:
  https://github.com/guillochon/oeis-results
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
