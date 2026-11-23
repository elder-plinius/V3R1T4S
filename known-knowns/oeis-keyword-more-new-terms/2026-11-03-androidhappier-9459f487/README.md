# A326336(11) = 70472: set partitions of {1..11} whose capturing graph is connected

## What

Confirmed scope, quoted word for word from panel/gate.md:

> For the live OEIS entry A326336 (keyword nonn,more; offset 0; DATA and the synthesized b-file end at a(10)=12270, with no links, extensions, or pending drafts; re-fetched 2026-11-03T20:29Z), the claim is A326336(11) = 70472. This is the number of set partitions of {1..11} whose capturing-block graph is connected, using any-pair capture x<z<t<y or z<x<y<t and counting empty and one-block partitions. The definition matches the entry and all three programs. n = 11 is the first missing index, A326336 is not excluded by the bank, the bank criterion is quoted verbatim, PREREG predates all attempt artifacts, and the only OEIS value hit (A070472, n^3 mod 7) is an unrelated A-number-digit coincidence. This covers the bank criterion's conditions only; whether the programs agree and reproduce all existing terms is left to the replication skeptic, since this check did not run them.

The correctness of the count itself was checked by the REPRODUCE skeptic (panel/reproduce.md): its own checker
(panel/reproduce_checker.py, literal and fast modes), written from the definition before it read the authors' code,
and all three authors' programs give a(0..10) = DATA and a(11) = 70472.

OEIS A326336 (Gus Wiseman, June 2019) is the "Number of set partitions of {1..n} whose capturing blocks are
connected": two blocks capture if they are of the form {...x...y...} and {...z...t...} with x<z<t<y or z<x<y<t
(any pairs, not only consecutive ones), and the blocks joined by capturing edges must form a connected graph. The
empty partition and one-block partitions count. The entry gives a(0..10) = 1,1,1,1,2,7,24,100,458,2279,12270
(offset 0,5) and carries keyword more. This folder adds the next term:

    A326336(11) = 70472

The object is object/VALUE.txt, the single line `A326336(11) = 70472` (sha256
9459f487d861a49adae0c14a4e752a63813fbc1c13ac85ac585ee216278e8dcf).

How the number was obtained (sources in how-we-built-it/):
- Program A (how-we-built-it/pA_spstats.c, C): all set partitions as restricted-growth strings, explicit any-pair
  quadruple tests per block pair, union-find connectivity.
- Program B (how-we-built-it/pB_go/main.go, Go, no shared code): lowest-element bitmask generator; A captures B iff at
  least two elements of B lie strictly between min A and max A (or vice versa), via popcount; BFS connectivity.
- Program C (how-we-built-it/pC_literal.py, Python): a literal transcription of the entry's Mathematica patterns.
  how-we-built-it/pC_neg_fixture.py (crossing edges instead of capturing) fails DATA, as it should.
- All three print a(0..10) = DATA and a(11) = 70472 (how-we-built-it/outputs/).

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: a few seconds (about 4 s on the build machine). Requirements:
Python 3 (standard library only); a C compiler is optional (step 4). The script checks the sha256 of object/VALUE.txt,
then runs verify-it-yourself/verify_a326336.py, a checker written for this package from the definition (recursive
insertion into sorted blocks; the any-pair capture test, with a min/max shortcut that it first checks equals the
literal test on every block pair for n <= 8; DFS connectivity): it must give a(0..10) = DATA and a(11) equal to the
value in object/VALUE.txt. A negative control with crossing edges in place of capturing must not reproduce DATA.
With a C compiler it also builds Program A and requires its A326336 column to match for n = 0..11. Real output:
verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A326336 (revision #6, Jun 28 2019), DATA, b-file, history, drafts, value search | a(11) | absent (DATA and b-file end at a(10) = 12270; keyword nonn,more; no pending draft; value search 12270,70472: no match) | 70472 | 2026-11-03T16:25:19Z (claim time); about 2026-11-03T20:28Z-20:29Z (panel); 2026-11-03T20:40:50Z (gate) |

URL: https://oeis.org/A326336 (b-file https://oeis.org/A326336/b326336.txt, history
https://oeis.org/history?seq=A326336). The fetch record is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell, A326336(11). The programs also print a(12) = 430016 and the sibling columns A326245, A326246,
  A326249 and A326335 (how-we-built-it/outputs/) as cross-checks; those are by-products, were not judged by this
  panel and are not claimed here.
- Own-team disclosure: a separate, unpublished package by the same contributor for the sibling sequence A326335
  (nestconn, A326335(11) = 61987; package id ending 17262752) uses the same programs, so its output tables also
  print the A326336 column, including 70472 at n = 11, as a by-product. That is this contributor's own computation,
  not prior art (panel/novelty.md); A326336 is a separate cell, and that package claims only A326335(11).
- A bare OEIS search for 70472 returns only A070472 ("a(n) = n^3 mod 7", terms 0, 1, 6), a match on the A-number
  string, not a term; the novelty skeptic and the gate judged it unrelated (panel/novelty.md, panel/gate.md).
- Programs A, B and C were written by the same contributor in the same run. Their independence is in language,
  generator and capture-test algorithm. verify_a326336.py was written for this package after the gate.
- The table check is as of the fetch times above. Nothing was submitted to the OEIS, and no pull request was opened.
- The OEIS pages fetched are not shipped (third-party content); their URLs, times and sha256 are in the-record-we-beat/.
- panel/ holds the four panel files plus the reproduce skeptic's checker; one string in novelty.md was redacted
  (panel/REDACTIONS.md).

## Credits

- Gus Wiseman: the sequence A326336, its definition, Mathematica code and terms a(0..10), https://oeis.org/A326336;
  Susanna Cuyler, editor who approved revision #6.
- The OEIS Foundation, https://oeis.org; A070472 named above, https://oeis.org/A070472.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: GitHub CharanRayudu (https://github.com/CharanRayudu).
