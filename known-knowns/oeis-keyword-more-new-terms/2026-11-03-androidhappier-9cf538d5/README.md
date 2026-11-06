# A325786(21) = 93725: the number of complete necklace compositions of 21

## What

Confirmed scope, quoted word for word from panel/gate.md:

> A325786(21) equals 93725 as the next term (first index beyond DATA and b-file) of OEIS A325786, counting complete necklace compositions of 21 per the entry's name and Mathematica code.

OEIS A325786 (Gus Wiseman, May 2019) is the "Number of complete necklace compositions of n". A necklace composition
of n is a sequence of positive integers summing to n that is lexicographically minimal among its cyclic rotations
(ties allowed, the entry's neckQ). It is complete if every integer 1..n is the sum of some circular subsequence
(consecutive parts, first and last counted as consecutive; the entry's subalt). The entry gives a(1..20) =
1,1,2,2,4,7,12,19,41,71,141,255,509,924,1882,3395,6838,12715,25233,47049 (offset 1,3) and carries keyword more.
This folder adds the next term:

    A325786(21) = 93725

The object is object/VALUE.txt, the single line `A325786(21) = 93725` (sha256
9cf538d5a41058aa72a6ce79df5852e594cd1d0c0ff8c68b3354332ec38125c5).

How the number was obtained (sources in how-we-built-it/):
- Program A (how-we-built-it/pA_neck.c, C): recursive enumeration of compositions, pruned by "no later part smaller
  than the first", a rotation-minimality test with ties allowed, and a check that the circular block sums cover 1..n.
- Program B (how-we-built-it/pB_go/main.go, Go, no shared code): every composition as a set of cut points in Z_n;
  complete iff the circular difference set covers every nonzero residue; necklaces counted by giving each complete
  composition of minimal period p the weight 1/p (exact rationals).
- Program C (how-we-built-it/pC_literal.py, Python): a literal transcription of the entry's Mathematica code;
  how-we-built-it/pC_neg_fixture.py (neckQ dropped) gives a(3) = 3, so it fails DATA as it should.
- All three print a(1..20) = DATA and a(21) = 93725 (how-we-built-it/outputs/).

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: well under a minute (about 5 s on the build machine). Requirements:
Python 3 (standard library only); a C compiler is optional (step 4). The script checks the sha256 of object/VALUE.txt,
then runs verify-it-yourself/verify_a325786.py, a checker written for this package from the definition (compositions
as cut bitmasks, rotation test, circular block sums as a bitmask): it must give a(1..20) = DATA and a(21) equal to the
value in object/VALUE.txt. A negative control without the necklace test must not reproduce DATA. With a C compiler it
also builds Program A and requires byte-identical output for n = 1..21. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A325786 (revision #6, May 22 2019), DATA, b-file, history, drafts, value search | a(21) | absent (DATA and b-file end at a(20) = 47049; keyword nonn,more; no pending draft; context search 25233,47049,93725: no match) | 93725 | 2026-11-03T16:41:07Z (claim time); about 2026-11-03T18:08Z-18:10Z (panel); 2026-11-03T18:11:27Z (gate) |

URL: https://oeis.org/A325786 (b-file https://oeis.org/A325786/b325786.txt, history
https://oeis.org/history?seq=A325786). The fetch record is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell, A325786(21). The programs also printed values for n = 22..30 (how-we-built-it/outputs/); those are
  by-products, were not judged by the panel and are not claimed.
- A bare OEIS search for 93725 returns A332835, an unrelated sequence that has 93725 as its own a(21), and A093725
  (A-number string match). Neither records the value as a term of A325786; the novelty skeptic and the gate judged
  this a coincidence (panel/novelty.md, panel/gate.md).
- Programs A, B and C were written by the same contributor in the same run. Their independence is in language,
  generator and test algorithm. verify_a325786.py was written for this package after the gate.
- The table check is as of the fetch times above. Nothing was submitted to the OEIS, and no pull request was opened.
- The OEIS pages fetched are not shipped (third-party content); their URLs, times and sha256 are in the-record-we-beat/.
- panel/ holds the four panel files exactly as written; no redaction was needed.

## Credits

- Gus Wiseman: the sequence A325786, its definition, Mathematica code and terms a(1..20), https://oeis.org/A325786;
  Susanna Cuyler, editor who approved revision #6.
- The OEIS Foundation, https://oeis.org; A332835 and A093725 named above, https://oeis.org/A332835,
  https://oeis.org/A093725.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: GitHub CharanRayudu (https://github.com/CharanRayudu).
