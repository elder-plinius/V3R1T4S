# OEIS A054961, n=16: a family of 102 binary vectors with all pairwise ORs distinct (stated bound: 91)

## What

The file A054961_n16_m102.txt (sha256 de9e6522f190dbddc1bf2db69e8e1dcf9cb8995e8adc7f5b9a61093b95ffe381) is a family of 102 distinct binary vectors of length 16 whose 5151 pairwise bitwise ORs of distinct vectors are all distinct, so under the OEIS A054961 definition a(16) >= 102, strictly above the a(16) >= 91 bound on the OEIS page (Zhao Hui Du, Apr 19 2018; re-fetched 2026-10-22T23:24:54Z) and the 91-families in the emath poisonall.txt and wolfy-out.txt tables; a(16) itself is not determined.

Status at the V3R1T4S honesty gate: CONFIRMED_PARTIAL (a new lower bound for one cell; the panel files are in panel/).

## Check it yourself

Python 3 and a POSIX shell, standard library only:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Under a second on a laptop. Two independent checkers test that every line is 16 characters of 0/1, the 102 vectors are distinct, and all 5151 pairwise ORs of distinct vectors are distinct; the script then checks that 102 exceeds the bound 91.

## Compared to

OEIS A054961 (https://oeis.org/A054961): comment "a(13) to a(27) are >= 55,63,72,91,... - Zhao Hui Du, Apr 19 2018", so a(16) >= 91. Fetched 2026-10-22T23:24:54Z (HTTP 200); DATA ends at a(9) = 17 and no later comment raises a(16). The emath group's data file (poisonall.txt, row 16: [91], fetched 2026-10-22T23:27:15Z) and Arthur O'Dwyer's wolfy-out.txt ("N=91 D=2 T=16", fetched 2026-10-22T23:27:15Z) also give 91. Details in the-record-we-beat/.

## Not claimed

A lower bound only: a(16) is not determined and the family is not claimed optimal. The claim uses the OEIS reading (ORs of 2 distinct vectors). Under the stricter "at most 2 defectives" reading (singletons counted, bar-2-separable) this family fails, because its one weight-1 vector lies inside 26 others; the OEIS n=4 example and both published 91-families fail that reading too. The family is a union-free family, not 2-cover-free (not 2-disjunct, a different problem, e.g. OEIS A286874). 101 of its 102 vectors have weight 4; it shares no vector with the published 91-families, and since coordinate permutations are the only maps preserving ORs and they preserve weight, it contains no copy of them. Du and Hwang's book tables and unarchived emath forum pages were not read. Not submitted to OEIS. Reviewers were fresh contexts of the same assistant, not humans.

## Credits

Submission credit: SwimingUpstairs. OEIS A054961 by N. J. A. Sloane (https://oeis.org/A054961) and its contributors, including Michael B. Greenwald, Jud McCranie and David W. Wilson (original computation, 2000), Giovanni Resta (a(8)), Zhao Hui Du (a(9) and the bounds a(13)..a(27)), Dmitry Kamenetsky (bounds for n=9..12) and Sarosh Adenwalla (general bounds; all named in https://oeis.org/A054961). Comparison data: the emath group (https://emathgroup.github.io/blog/two-poisoned-wine/) and Arthur O'Dwyer (https://github.com/Quuxplusone/wolves-and-sheep, https://quuxplusone.github.io/blog/2020/01/10/wolves-and-sheep-with-tables/). Background: D.-Z. Du and F. K. Hwang, Combinatorial Group Testing and Its Applications (World Scientific, 2nd ed. 2000); P. Erdős, P. Frankl and Z. Füredi, J. Combin. Theory A 33 (1982) 158-166 (the lower bound cited on the OEIS page); P. Frankl and Z. Füredi (union-free families). Protocol: V3R1T4S, https://github.com/elder-plinius/V3R1T4S, commit c8ba8bc4258164998de76ab939b0748fe80f73a2.
