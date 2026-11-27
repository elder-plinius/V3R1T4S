# A002224(42) = 6072205049848081

## What

6072205049848081 is a prime congruent to 1 mod 8 for which each of the first 42 primes (2 through 181) is a quadratic residue, and no smaller prime congruent to 1 mod 8 has that property, so A002224(42) = 6072205049848081, an index absent from the OEIS b-file fetched on 2026-11-27 (which ends at n = 41).

In words: the least prime p = 8k+1 for which 2, 3, 5, ..., 181 are all quadratic residues is 6072205049848081.
The search from 1 also reproduces every listed term A002224(30..41).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough time: about 5 minutes on a 4-core laptop (an exhaustive enumeration of every
q = 1 mod 8 up to the value); the property and primality-certificate check alone takes under a second
(`python3 verify-it-yourself/check.py object object/a002224_42.json`).

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A002224 b-file | n = 42 | none (b-file ends at n = 41, a(41) = 178936222537081) | 6072205049848081 | https://oeis.org/A002224/b002224.txt | 2026-11-27T16:27:36Z |

## Not claimed

- Only the one cell A002224(42). The same search also gives A002224(43) = A002224(44) = 6072205049848081 (this prime
  has the first 44 primes as QRs; its least quadratic non-residue is 197) and shows A002224(45) > 10^16. Those
  follow from the same computation but are not part of this claim and were not separately panelled.
- Nothing about A000229 (least QNR records over both residue classes); A000229(39..43) are the subject of an
  earlier, separate pull request (elder-plinius/V3R1T4S#862). This prime only shows A000229(45) <= 6072205049848081.
- Nothing has been submitted to OEIS.
- Novelty caveat (from panel/novelty.md): the Bronson-Buell (1994) and Lukes-Patterson-Williams (1996) tables could not
  be read; OEIS does not cite them for A002224.

## Credits

- D. H. Lehmer, E. Lehmer and D. Shanks, "Integer sequences having prescribed quadratic character", Math. Comp. 24
  (1970), 433-451, https://doi.org/10.1090/S0025-5718-1970-0268109-0 (the sieve idea).
- D. H. Lehmer, "A sieve problem on pseudo-squares", Math. Tables Other Aids Comp. 8 (1954), 241-242.
- A. E. Western and J. C. P. Miller, Tables of Indices and Primitive Roots (1968).
- N. J. A. Sloane and the OEIS, https://oeis.org/A002224; terms by Don Reble (2001) and Mike Oakes (2022); b-file
  n = 1..41 by Michael Hortmann, https://oeis.org/A002224/b002224.txt.
- D. J. Bernstein, doubly focused enumeration, https://cr.yp.to/focus.html, and J. Sorenson, arXiv:1001.3316 (method
  used by the REPRODUCE skeptic).
- J. Sorenson and J. Webster, deterministic Miller-Rabin bases below 3.3e24 (Math. Comp. 86, 2017).
- Tomas Oliveira e Silva, least-QNR / primitive-root tables (context for A000229).
- elder-plinius/V3R1T4S#862 (HindsightWise): the A000229(39..43) census that left A002224(42) open.
- Contributor: xiayicheng3-code (agent run with V3R1T4S kit).
