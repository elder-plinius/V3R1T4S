# A_4^GC,RC(20,15,10) >= 16

## What

The 16-word list in object/code_20_15_16.json is a valid length-20 DNA code with GC count 10, minimum Hamming distance 15 and reverse-complement distance at least 15 (self-pairs included), so A_4^GC,RC(20,15,10) >= 16, exceeding the unmarked live King-table entry 15 (re-fetched 2026-10-17T23:07Z) and every post-2010 published value for (20,15) found in the sources checked (all 15), with one paywalled 2023 IEEE TIT paper unread.

The object is `object/code_20_15_16.txt`: 16 DNA words of length 20, one per line.

## Check it yourself

From this folder: `sh verify-it-yourself/run_checks.sh` (Python 3, standard library). Expected last line: `PASS`.
Under a second on a laptop. Optional Lean 4 proof: `verify-it-yourself/lean/`.

## Compared to

Gaborit and King table, A_4^GC,RC(n,d,w), cell (n,d) = (20,15): 15 (superscript v, not marked optimal),
https://rambutan.umassmed.edu/king/dnacodes.html, fetched 2026-10-17T22:36:36.846803+00:00 and again by the panel at 2026-10-17T23:07:32Z
(page sha256 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5). Every later published value found for (20,15) is 15; see `the-record-we-beat/README.md`.

## Not claimed

- No upper bound: 17 or more words at (20,15) are not excluded.
- Not optimality, and not a value for other GC contents w.
- One paywalled paper was not read: Dougherty, Korban, Sahinkaya, Ustun, IEEE Trans. Inf. Theory 69(3) (2023),
  doi:10.1109/TIT.2022.3217518.
- A literature search cannot exclude unpublished or unindexed results.

## Credits

- Table: P. Gaborit and O. D. King, https://rambutan.umassmed.edu/king/dnacodes.html; P. Gaborit, O. D. King,
  Linear constructions for DNA codes, Theoretical Computer Science 334 (2005) 99-113.
- Previous value 15: R. Montemanni, D. H. Smith (variable neighbourhood search, J. Math. Modelling Algorithms 7
  (2008); MIC 2009); R. Montemanni, D. H. Smith, N. Koul, Lecture Notes in Management Science 6 (2014) 167-175.
- Best-known tables compared: N. Aboluion, D. H. Smith, S. Perkins, Discrete Mathematics 312 (2012) 1062-1075;
  N. A. Aboluion, PhD thesis, University of Glamorgan (2011); D. Limbachiya, B. Rao, M. K. Gupta, arXiv:1607.00266.
- Found by MikhailLevit1987 with an AI research agent following the V3R1T4S kit.
