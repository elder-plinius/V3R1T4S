# How we found it (contributor text, unverified)

The brief was a V3R1T4S run on the bank target odd-graceful-trees-beyond-12: extend the computer-verified bound for
Gnanajothi's conjecture that every tree is odd-graceful from order 12 (Barrientos, as cited in Gallian's Dynamic
Survey DS6, Oct 30 2025) to order 22, with a certificate, or find a counterexample.

- First, the checker (exact-eval-first): a C program that regenerates every tree by leaf addition, deduplicates by a
  centre-rooted AHU canonical code, and matches a certificate against that set. It was tested on hand-made fixtures:
  a valid path labelling passes; a duplicate label, a wrong difference, an even difference, a missing tree and a
  duplicate tree all fail.
- What worked: a largest-difference-first randomized backtracking search (how-we-built-it/oglabel.c). The largest
  difference 2n-3 forces labels 0 and 2n-3 on one edge, and each smaller odd difference labels one new vertex adjacent
  to the labelled part. With random restarts it labelled every tree of orders 2..22 with no failure; order 22
  (5,623,756 trees) took 161 s on 8 cores.
- What did not work or was not needed:
  - Going through alpha-labelings (which imply odd-graceful labelings) gave valid labelings but covered too few
    trees.
  - A contrarian lens hunted for counterexample candidates: every tree that failed a deliberately tiny search budget
    was solved with a larger one, so there was no candidate.
  - A literature lens found no bound above 12 in DS6 or in the last 24 months of papers and code.
- A second checker in Python (counts from Otter's formula, no regeneration) and then a three-skeptic panel
  (reproduce, novelty, criterion; each in a fresh context with its own code) confirmed the scope quoted in README.md.
