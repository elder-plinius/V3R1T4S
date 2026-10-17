# 2026-10-16-opdahl-e20a22f5

## What

The confirmed scope, quoted from `panel/gate.md`:

> The minimizer order [3,4,1,0,5,6,2,7] for (w=12, k=3), evaluated with the published notebook's own rank composition, has mean density 0.136644513466 at n=2,000,000 over seeds 0,1,2, which is strictly lower than the smallest value listed for that cell in k_extension_k16_w12.csv (0.138389448, angle-based) by 1.2609% relative, exceeding the required 0.5% margin.

A minimizer scheme samples a DNA sequence. In each window of w consecutive k-mers, the scheme keeps
the position of the smallest k-mer. A fixed ranking gives the order of the k-mers. The density is the
fraction of positions that the scheme keeps. The density sets the memory cost and the time cost of an
aligner or an assembler.

GreedyMini ranks the k-mers in two steps. First, it changes each base to one bit. Second, it orders
the classes that result. For k=3, eight classes exist. Thus 40320 rankings exist.

This package gives one ranking. This ranking beats all values that the public tables list for
(w=12, k=3).

The object is eight numbers. The object uses 64 bytes. The order needs constant space. The order does not need a table of 4^k entries.

## Check it yourself

Run this command:

    sh verify-it-yourself/run_checks.sh

The last line of the output must be PASS. The command needs two to four minutes on a laptop. The
command needs python3 and numpy.

The output of the real run is in `verify-it-yourself/RECEIPTS.md`.

## Compared to

The table is `k_extension_k16_w12.csv` from OrensteinLab/10-minimizers. The cell is w=12, k=3.

The smallest value in this cell is 0.138389448. The scheme angle-based holds this value. The value
for GreedyMini is 0.138843.

The table was fetched one time. The fetch was a plain GET on 2026-10-16T18:57Z. The HTTP status was
200. The sha256 of the page is 88c4f8fc. For more data, see `the-record-we-beat/table.md`.

Two orders were measured with the same code and the same sequences:

- this order: 0.136644513466
- GreedyMini: 0.138882166707

The improvement against the smallest listed value is 1.2609%. The improvement against GreedyMini is
1.61%.

## Not claimed

- This package does not claim an expected density over all sequences. The values are particular
  densities. The published notebook generates the sequences at random. Each value is the mean of
  three seeds. Both sides of the comparison use the same estimator. Thus the comparison is fair. The
  sampling error is about 0.2%. The margin is 1.26%.
- This package does not claim a practical speedup. This package does not claim a result for a real
  genome. The result is a statement about one table cell.
- This package does not claim a general method. k=3 is a special case. The space of 40320 orderings is
  small. Thus an exhaustive search is possible. A search can beat a published heuristic in this
  space. No result is claimed for the k values that occur in practice.
- This package does not claim the first result for this target. An earlier entry in `TROPHY_CASE.md`
  for the same cell, with an equal or better value, replaces this result.

## Credits

- OrensteinLab/10-minimizers (A. Shur, I. Tziony, Y. Orenstein, WABI 2026). This package uses the
  density tables and the measurement notebook. https://github.com/OrensteinLab/10-minimizers
- OrensteinLab/GreedyMini (S. Golan, I. Tziony, M. Kraus, Y. Orenstein, A. Shur, Bioinformatics 2025).
  This package uses the incumbent order. https://github.com/OrensteinLab/GreedyMini
- The authors of the angle-based, decycling, double decycling and mod-minimizer entries. These
  entries are the comparison set.
