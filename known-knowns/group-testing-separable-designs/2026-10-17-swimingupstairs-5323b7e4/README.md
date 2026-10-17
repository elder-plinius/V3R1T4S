# OEIS A054961, n=15: a family of 79 binary vectors with all pairwise ORs distinct (stated bound: 72)

## What

The file A054961_n15_m79.txt (sha256 5323b7e4a596e3f8d9e33f3d8feddc4ef0a3c05e933494bb873a93e221e41118) is a family of 79 distinct binary vectors of length 15 whose 3081 pairwise bitwise ORs are all distinct, so OEIS A054961 a(15) >= 79, strictly above the a(15) >= 72 bound in revision #89 (re-fetched 2026-10-17T05:12:45Z).

## Check it yourself

Python 3 and a POSIX shell, standard library only:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Under a second on a laptop. Checks that the file has only 0/1 characters, every vector has length 15, all vectors are distinct, all 3081 pairwise ORs are distinct, and that 79 exceeds the bound 72.

## Compared to

OEIS A054961 (https://oeis.org/A054961), revision #89 (Nov 14 2024): comment "a(13) to a(27) are >= 55,63,72,... - Zhao Hui Du, Apr 19 2018", so a(15) >= 72. Fetched 2026-10-16T16:33:12Z (HTTP 200), unchanged at 2026-10-17T05:12:45Z. The emath group's data file and Arthur O'Dwyer's tables also give 72. Details in the-record-we-beat/.

## Not claimed

A lower bound only: a(15) is not determined and the family is not claimed optimal. Not 2-disjunct or 2-bar-separable (those are different problems, e.g. OEIS A286874). Not submitted to OEIS. Literature search covered OEIS (A054961, A054962, A304041, A361928), the emath group's forum and blog mirror, O'Dwyer's tables, Math Stack Exchange, the union-free (strongly union-free) and separable-code literature, GitHub/Zenodo/arXiv, Chinese-language sources, and this repo's trophies and PRs; the original emath blog (expired TLS certificate) and MSE question 639 could not be read. Reviewers were fresh contexts of the same assistant, not humans.

## Credits

Submission credit: SwimingUpstairs. OEIS A054961 by N. J. A. Sloane (https://oeis.org/A054961) and its contributors, including Michael B. Greenwald, Jud McCranie and David W. Wilson (original computation, 2000), Giovanni Resta (a(8)), Zhao Hui Du (a(9) and the bounds a(13)..a(27)), Dmitry Kamenetsky (bounds for n=9..12; all named in https://oeis.org/A054961) and Sarosh Adenwalla (general bounds). Comparison data: the emath group (https://emathgroup.github.io/blog/two-poisoned-wine/) and Arthur O'Dwyer (https://quuxplusone.github.io/blog/2020/01/10/wolves-and-sheep-with-tables/, https://github.com/Quuxplusone/RecreationalMath). Background: D.-Z. Du and F. K. Hwang, Combinatorial Group Testing and Its Applications (World Scientific, 2nd ed. 2000); Math Stack Exchange question 639 (https://math.stackexchange.com/q/639) and 1528962 (https://math.stackexchange.com/q/1528962); P. Erdős, P. Frankl and Z. Füredi, J. Combin. Theory A 33 (1982) 158-166. Protocol: V3R1T4S, https://github.com/elder-plinius/V3R1T4S, commit c8ba8bc4258164998de76ab939b0748fe80f73a2.
