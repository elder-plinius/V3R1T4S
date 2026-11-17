# A326335(11) = 61987: set partitions of {1..11} whose nesting graph is connected

## What

Confirmed scope, quoted word for word from panel/gate.md:

> As of 2026-11-03 14:12 EST, A326335 carries keyword 'more', is not excluded by the V3R1T4S bank, and has DATA and b-file ending at a(10)=10696 (so n=11 is the first missing index), while the claimed definition and all three programs' nesting tests match the entry's consecutive-pair definition, PREREG.md predates every attempts/ file, and 61987 appears in neither the entry, its history, nor any OEIS search hit for this sequence; this vote does not verify that 61987 is the correct count.

The correctness of the count itself was checked by the REPRODUCE skeptic (panel/reproduce.md): its own checker,
written from the definition before it read the authors' code, and all three authors' programs give a(0..10) = DATA
and a(11) = 61987.

OEIS A326335 (Gus Wiseman, June 2019) is the "Number of set partitions of {1..n} whose blocks, joined by an edge when
they nest, form a connected graph" (entry comment: two blocks nest if they are of the form {...x,y...} and
{...z,t...} with x<z<t<y or z<x<y<t, where x,y and z,t are consecutive in their blocks, per the entry's Mathematica
code). The empty partition and one-block partitions count. The entry gives a(0..10) =
1,1,1,1,2,6,21,86,394,1974,10696 (offset 0,5) and carries keyword more. This folder adds the next term:

    A326335(11) = 61987

The object is object/VALUE.txt, the single line `A326335(11) = 61987` (sha256
1726275264dcaacd920d82809a0363b4c5b93c894297cf7f8d2166e9a80350bc).

How the number was obtained (sources in how-we-built-it/):
- Program A (how-we-built-it/pA_spstats.c, C): all set partitions as restricted-growth strings, explicit
  consecutive-pair tests per block pair, union-find connectivity.
- Program B (how-we-built-it/pB_go/main.go, Go, no shared code): lowest-element bitmask generator; two blocks nest iff
  some gap between consecutive elements of one holds at least two elements of the other (popcount); BFS connectivity.
- Program C (how-we-built-it/pC_literal.py, Python): a literal transcription of the entry's Mathematica patterns.
  how-we-built-it/pC_neg_fixture.py (nesting tested on any pairs, not consecutive ones) fails DATA, as it should.
- All three print a(0..10) = DATA and a(11) = 61987 (how-we-built-it/outputs/).

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: a few seconds (about 3 s on the build machine). Requirements:
Python 3 (standard library only); a C compiler is optional (step 4). The script checks the sha256 of object/VALUE.txt,
then runs verify-it-yourself/verify_a326335.py, a checker written for this package from the definition (recursive
insertion into sorted blocks, the consecutive-pair nesting test as stated, DFS connectivity): it must give
a(0..10) = DATA and a(11) equal to the value in object/VALUE.txt. A negative control with nesting tested on any pairs
must not reproduce DATA. With a C compiler it also builds Program A and requires its A326335 column to match for
n = 0..11. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A326335 (revision #6, Jun 28 2019), DATA, b-file, history, drafts, value search | a(11) | absent (DATA and b-file end at a(10) = 10696; keyword nonn,more; no pending draft; value search 10696,61987: no match) | 61987 | 2026-11-03T16:25:13Z (claim time); about 2026-11-03T19:12Z-19:13Z (panel); 2026-11-03T19:16:29Z (gate) |

URL: https://oeis.org/A326335 (b-file https://oeis.org/A326335/b326335.txt, history
https://oeis.org/history?seq=A326335). The fetch record is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell, A326335(11). The programs also print a(12) = 381614 and the sibling columns A326245, A326246,
  A326249 and A326336 (how-we-built-it/outputs/) as cross-checks; those are by-products, were not judged by the panel
  and are not claimed here.
- A bare OEIS search for 61987 returns A209399, an unrelated sequence (subsets of {1..n} containing two elements whose
  difference is 3) that has 61987 as one of its own terms, and A061987, A220933, A243426, A302318 (A-number or
  unrelated hits). None records the value as a term of A326335; the novelty skeptic and the gate judged this a
  coincidence (panel/novelty.md, panel/gate.md).
- Programs A, B and C were written by the same contributor in the same run (the criterion skeptic notes that the C and
  Go sources share one file time). Their independence is in language, generator and test algorithm.
  verify_a326335.py was written for this package after the gate.
- The table check is as of the fetch times above. Nothing was submitted to the OEIS, and no pull request was opened.
- The OEIS pages fetched are not shipped (third-party content); their URLs, times and sha256 are in the-record-we-beat/.
- panel/ holds the four panel files; one string in criterion.md was redacted (panel/REDACTIONS.md).

## Credits

- Gus Wiseman: the sequence A326335, its definition, Mathematica code and terms a(0..10), https://oeis.org/A326335;
  Susanna Cuyler, editor who approved revision #6.
- The OEIS Foundation, https://oeis.org; A209399, A061987, A220933, A243426 and A302318 named above,
  https://oeis.org/A209399, https://oeis.org/A061987, https://oeis.org/A220933, https://oeis.org/A243426,
  https://oeis.org/A302318.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: GitHub CharanRayudu (https://github.com/CharanRayudu).
