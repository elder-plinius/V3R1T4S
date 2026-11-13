# A Lychrel number in base 13 (template-closure proof)

## What

In base 13, the 134-digit number n of result/seed_base13.txt equals T_0(0) of the 10 affine run-length templates in result/lychrel_base13.json, and a mechanically checked symbolic carry computation with threshold 0 (re-run in jobs 2340 and 2344, cross-checked by integer brute force for m <= 400 and a 100000-step simulation in job 2347) proves RA(T_i(m)) = T_(i+1)(m) for i < 9 and RA(T_9(m)) = T_0(m+1) for every m >= 0, with no T_i(m) a palindrome, so n is a Lychrel number in base 13 at the level of partial win p1 (novelty not established by this package).

The object is in object/: the seed (base-13 digits in seed_base13.txt, digits 0-9, a=10, b=11, c=12; decimal value in
seed_decimal.txt) and the period-10 cycle of affine run-length templates (lychrel_base13.json; the same templates in
plain text in b13.tpl). The growing block is one run of equal digits at the centre of the number that alternates
between 4s and 8s (each step doubles it modulo 12, with the carry), a "diagonal" bulk rather than the 0 / b-1 pairs of
the previously known constructions.

## Check it yourself

From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3 standard library). Expected last line: `PASS`.
It takes a few seconds on a laptop. Optional independent long simulation (C):
`gcc -O2 -o lo verify-it-yourself/longorbit.c && ./lo object/b13.tpl 100000`, expected
`RESULT base=13 steps=100000 final_len=30134 template_checks=100001 mismatches=0 palindromes=0`.

## Compared to

| table | cell | value there | URL | fetched (UTC) |
|---|---|---|---|---|
| Wikipedia "Lychrel number", list of bases with a proven Lychrel number | base 13 | not listed ("11, 17, 20, 26, and all powers of 2") | https://en.wikipedia.org/wiki/Lychrel_number | 2026-10-23T22:36:25Z (panel), 2026-10-23T18:38:33Z (scout) |

Details in the-record-we-beat/RECORD.md and panel/novelty.md.

## Not claimed

- Not that this is the smallest Lychrel number in base 13 (OEIS A060382 lists conjectured smallest values; only a(2)
  is proved there). The seed has 134 base-13 digits.
- Not a full CONFIRMED_SOLUTION of the bank target: the panel's level is partial win p1 ("verified proof, novelty
  unconfirmed"); expert confirmation of novelty is pending. The literature search was bounded (see panel/novelty.md).
- Nothing about base 10 or about 196.
- The proof is computer-assisted: an exact symbolic run-length/carry computation valid for every parameter m >= 0
  (threshold 0), cross-checked by exact integer computation for m <= 200 in this checker (m <= 400 by the panel).

## Credits

- David Seal, January 1996 rec.puzzles post with the base 4, 11, 17, 20 and 26 cycles, as reproduced on K. S. Brown's
  [MathPages](https://www.mathpages.com) (page dseal.htm, cited by Wikipedia as "Letter from David Seal"): the
  template-cycle form this proof uses and the calibration cycles for our checker.
- The anonymous author of "Search for and classification of Lychrel numbers" (2016, public domain,
  [p196.org lychrel842.zip](https://www.p196.org/files/lychrel842.zip)): the outside-in construction of exteriors with
  0 / b-1 bulks, which our exterior automaton generalizes.
- [dew-web/lychrel-self-similar](https://github.com/dew-web/lychrel-self-similar) (first commit 2026-10-10): an
  independent, earlier claim of a base-9 Lychrel family by the same family of exact methods (two-run self-similar
  cycles; base-10 exclusions to period 15). Not the same base; our base-9 object (not packaged here) ties with it.
- Rostand S. Kuitche, "On the Construction of Some Lychrel Numbers" (2023, [Research Square rs-2659802](https://www.researchsquare.com/article/rs-2659802/v1)): read for novelty; its results cover bases 3 to 10.
- [Wikipedia "Lychrel number"](https://en.wikipedia.org/wiki/Lychrel_number) and [OEIS A060382](https://oeis.org/A060382), [A023108](https://oeis.org/A023108) for the status.
- Contributed by jndk.
