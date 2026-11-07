# Every tree on at most 22 vertices is odd-graceful (DS6 bound: 12)

## What

Confirmed scope, quoted word for word from panel/gate.md:

> Every tree on at most 22 vertices is odd-graceful: for each n = 2..22 the certificate lists A000055(n) pairwise non-isomorphic trees, each with a verified odd-graceful labeling (distinct labels in [0, 2n-3], edge differences exactly {1, 3, ..., 2n-3}).

Odd-graceful (Gnanajothi 1991): a graph with q edges is odd-graceful if its vertices get distinct labels from
{0, 1, ..., 2q-1} so that the edge differences |f(u)-f(v)| are exactly 1, 3, ..., 2q-1. Gnanajothi conjectured that
every tree is odd-graceful. Gallian's Dynamic Survey DS6 (Oct 30, 2025) records it as verified for all trees of
order up to 12 (Barrientos). This folder raises that to 22: 9,113,298 trees of orders 13..22, each with an explicit
labeling (9,114,284 trees of orders 2..22 in all).

The object is object/CERTIFICATES.txt (sha256 79df75225a75f48b971b2e7ea2a91e325a129d836720df7542d056dfed2971af).
It pins the sha256 and size of one gzip certificate per order n = 2..22. Each certificate has one line per tree:
`p_1 ... p_{n-1} | f(0) ... f(n-1)`, where p_i is the parent of vertex i (0 <= p_i < i) and f(v) is the label of
vertex v. The certificates for orders 2..20 are in object/certs/. Those over 1 MB are split into 1,000,000-byte
parts; concatenating them in order gives the pinned file. The order-21 and order-22 files are too large for a
package (48,911,418 and 134,933,581 bytes). They are listed in object/CERTIFICATES.txt with their sha256 and are
verified by the same script once placed in large-files/ (see RUN_IT_YOURSELF.md). They are the files the panel
checked: their sha256 values match the panel's claim folder.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. On a laptop it takes about 1 minute for orders 2..20, and about 5 minutes with the
order-21 and order-22 files in large-files/. It needs Python 3 (standard library only). If a C compiler is present,
a second checker runs too: it regenerates every tree of order n by leaf addition and matches the certificate tree
by tree. The script checks every line of every certificate present: labels, differences, tree shape, no duplicate
tree, and number of trees = A000055(n). It also runs three damaged-copy controls, which must fail. Its summary line
lists the orders actually checked. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

The 29th edition of Gallian’s survey (November 6, 2026), section 3.6, also records the bound 12.
See https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS6/pdf/.

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| Gallian, Dynamic Survey of Graph Labeling DS6 (Oct 30, 2025), Section 3.6 | largest n such that all trees of order at most n are known to be odd-graceful | 12 (Barrientos) | 22 | 2026-11-01T02:26:39Z (scout); 03:00:08Z (panel); 03:12:12Z (gate), unchanged |

URL: https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6. The fetch record (times, HTTP status,
headers, hashes, the quoted sentence) is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Nothing beyond order 22. Order 1 (one vertex, no edges) is degenerate and not covered by the files.
- No proof of the conjecture and no new construction for any infinite family. This is a finite computer
  verification by explicit certificates.
- This package's own run_checks.sh checks orders 2..20 out of the box. Orders 21 and 22 are covered by the confirmed
  scope (the panel checked them exhaustively), but here they are checked only after their two files are downloaded
  into large-files/.
- The trees were listed with networkx, not nauty gentreeg. No claim rests on the generator: both checkers establish
  completeness independently, one by Otter's count plus distinct canonical forms and one by regeneration.
- Literature novelty is as recorded in panel/novelty.md (DS6, 24 months of literature and code, this repository).
  An obscure, unindexed earlier verification cannot be ruled out.

## Credits

- R. B. Gnanajothi: the definition of odd-graceful graphs and the conjecture (thesis, Madurai Kamaraj University,
  1991), verified for order at most 10.
- Christian Barrientos: the previous bound, order at most 12, and results on caterpillar forests and trees of
  diameter at most 5 (https://arxiv.org/abs/0807.3738).
- Joseph A. Gallian: A Dynamic Survey of Graph Labeling, Electronic Journal of Combinatorics DS6, which records the
  bound we compared against: https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6
- OEIS A000055 (number of trees with n unlabeled nodes): https://oeis.org/A000055, and R. Otter (1948) for the
  counting formula.
- NetworkX (nonisomorphic_trees, after Wright, Richmond, Odlyzko and McKay): https://networkx.org
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
