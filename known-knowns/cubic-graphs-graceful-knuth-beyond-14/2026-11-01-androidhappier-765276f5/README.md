# Every connected cubic graph on 16, 18, 20 and 22 vertices is graceful (DS6 bound: 14; Knuth: 16)

## What

Confirmed scope, quoted word for word from panel/gate.md:

> Every connected (simple) cubic graph on 16, 18, 20 and 22 vertices is graceful, as certified by result/cert_16.txt, cert_18.txt, cert_20.txt and cert_22.txt (4,060 / 41,301 / 510,489 / 7,319,447 graphs, canonically identical to a fresh nauty 2.8.8 geng -c -d3 -D3 n run with no duplicates, every labeling verified graceful by two checkers), of which orders 18, 20 and 22 are new relative to the sources cited in CLAIM.md.

A graph with q edges is graceful if its vertices get distinct labels from {0, 1, ..., q} so that the edge
differences |f(u)-f(v)| are exactly 1, 2, ..., q. A connected cubic graph on n vertices has q = 3n/2 edges. Knuth
conjectured that every connected cubic graph is graceful (TAOCP 4B and pre-fascicle 7A, exercise 96). Gallian's
Dynamic Survey DS6 (28th edition, Oct 30, 2025) records Knuth's computer verification for 4 to 14 vertices. Knuth's
pre-fascicle 7A (Dec 5, 2024) and Kennedy (2021) cover 16 vertices. This folder gives an explicit graceful labeling
of every connected cubic graph on 16, 18, 20 and 22 vertices: 4,060 + 41,301 + 510,489 + 7,319,447 = 7,875,297
graphs. Orders 18, 20 and 22 are new. Orders 4..14 are included as a regression check.

The object is object/CERTIFICATES.txt (sha256 765276f52743141c9fa508cbe9558c8cd2814e5a7e4711e8992fd5f57d985ffc).
It pins the sha256 and size of one gzip certificate per even order n = 4..22, and of its uncompressed text. The
uncompressed sha256 values are the ones the panel checked. Each certificate has one line per graph: the graph6
string exactly as output by nauty 2.8.8 `geng -c -d3 -D3 n`, then the labels f(0) ... f(n-1) in graph6 vertex order.

- In this package (object/certs/): orders 4, 6, 8, 10, 12, 14, 16, 18 and 20 as gzip files. The order-20 file
  (12,779,779 bytes) is split into 1,000,000-byte parts; concatenating them in order gives the pinned file.
- Not in this package (too large): order 22.
  - cert_22.txt.gz: 196,915,682 bytes, sha256 6439fa6bb934916ff471f66a582728eff46b6e5cd7282f6835a468a4e5d835d1
  - uncompressed cert_22.txt: 726,142,050 bytes, sha256 dbbe54e5a91052a9ac25375d57f5fea19e7b3e5b4d4a41eea1a4cec9772eb39d

  Both are pinned in object/CERTIFICATES.txt. Either one, placed in large-files/, is checked by the same script (see
  RUN_IT_YOURSELF.md). Public archive: the submitter adds its URL to the pull request description.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. On a laptop it takes under 1 minute for orders 4..20. With large-files/cert_22.txt.gz
it takes about 5 minutes on 8 cores and about 2 GB of memory. It needs Python 3 (standard library only).

The Python checker was written from the definition and does not use nauty. For every line it checks:
- a strict graph6 decode;
- n vertices, all of degree 3, connected;
- n distinct labels in [0, 3n/2];
- edge differences exactly {1, ..., 3n/2}.

It also computes an exact canonical form of every graph (colour refinement plus individualisation over the whole
search tree). It requires the number of lines = the number of pairwise non-isomorphic graphs = A002851. Four
damaged-copy controls must fail; one of them is an isomorphic relabelled copy with a valid labeling.

Two optional extras: if a C compiler is present, a second per-line checker (checkK.c) runs too. With
`NAUTY_BIN` pointing at nauty's geng and labelg, the script also regenerates each order and matches canonical forms.
Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| Gallian, A Dynamic Survey of Graph Labeling DS6 (28th ed., Oct 30, 2025), Section 2 | largest n for which every connected cubic graph on n vertices is known to be graceful | 14 (Knuth) | 22 | 2026-11-01T15:17:13Z (scout); 16:56:19Z (panel); 17:26:55Z (packaging), unchanged |
| Knuth, TAOCP pre-fascicle 7A (Dec 5, 2024), answer to exercise 96 | same | 16 (4060 connected cubic graphs on 16 vertices) | 22 | 2026-11-01T15:18:14Z (scout); 16:56:23Z (panel) |

URL: https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6. The fetch record (times, HTTP status,
headers, hashes, quoted sentences) is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Nothing beyond 22 vertices. No proof of Knuth's conjecture. This is a finite computer verification by explicit
  certificates.
- Order 16 is not new (Knuth pre-fascicle 7A; Kennedy 2021). It is included because the bank criterion lists it.
  Orders 4..14 are regression checks.
- Disconnected cubic graphs are not covered (2K4 and 3K4 are not graceful).
- This package's run_checks.sh checks orders 4..20 out of the box. Order 22 is in the confirmed scope, because the
  panel checked it exhaustively. Here it is checked only after its file is downloaded into large-files/.
- The printed TAOCP Volume 4, Fascicle 7 (2025) was not read. Its answer to exercise 96 could state a bound newer
  than the Dec 2024 pre-fascicle. Literature novelty is as recorded in panel/novelty.md. An unindexed earlier
  verification cannot be ruled out.
- The graph lists come from nauty geng. Completeness does not rest on geng: the Python checker proves that the
  graphs are pairwise non-isomorphic connected cubic graphs, and their number equals A002851.

## Credits

- Donald E. Knuth: the conjecture and the verification up to 16 vertices (The Art of Computer Programming,
  Vol. 4B, and pre-fascicle 7A, Section 7.2.2.3, exercise 96):
  https://www-cs-faculty.stanford.edu/~knuth/taocp.html
- Joseph A. Gallian: A Dynamic Survey of Graph Labeling, Electronic Journal of Combinatorics DS6, which records the
  bound we compared against: https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6
- G. Clare Kennedy: An Algorithmic Exploration of Gracefully Labeling Cubic Graphs, Macalester College honors
  project (2021), the 16-vertex verification: https://digitalcommons.macalester.edu/mathcs_honors/54
- OEIS A002851 (number of connected cubic graphs on 2n vertices): https://oeis.org/A002851. OEIS A337965 (number of
  graceful labelings of cubic graphs on 2n vertices; Knuth, Dobbelaere): https://oeis.org/A337965
- Brendan D. McKay and Adolfo Piperno: nauty and Traces (geng, labelg), version 2.8.8:
  https://pallini.di.uniroma1.it and https://users.cecs.anu.edu.au/~bdm/nauty/
- A. Kotzig: 2K4 and 3K4 are not graceful (as cited in DS6).
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
