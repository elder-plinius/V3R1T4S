# C(41,12,5) <= 2207: a (41,12,5) covering design with 2207 blocks

## What
The file C41_12_5_2207blocks.txt (sha256 ec985f89dd793006ccf15346b6937419e1ce4e922034d73b18e769fb958778aa) is a valid (41,12,5) covering design with 2207 blocks covering all 749398 5-subsets of {1..41} (checked exhaustively), 37 fewer than the 2244 listed in coveringrepository.com (fetched 2026-10-15T23:10:40Z) and 38 fewer than the 2245 in LJCR Zenodo v1.2.

Target: covering-designs-record (V3R1T4S bank). One cell: (v,k,t) = (41,12,5), plain covering (every 5-subset in at
least one block), b = 2207.

## Check it yourself
From this folder, in a fresh shell:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (~10 seconds on a laptop; Python 3 standard library only). The checker enumerates all
749398 5-subsets of {1,...,41}. Its real output is in verify-it-yourself/RECEIPTS.md.

## Compared to
- coveringrepository.com, plain (v,k,t) table (m = t rows), cell (41,12,5): 2244.
  https://coveringrepository.com/download_archive_vkt.aspx, fetched 2026-10-15T23:10:40Z (HTTP 200) and again by the
  NOVELTY panelist at 2026-10-16T02:08:02Z (HTTP 200, same bytes). Details in the-record-we-beat/.
- La Jolla Covering Repository (D. M. Gordon), Zenodo v1.2 (2026-04-24, the latest version): C(41,12,5) size 2245,
  lower bound 1121, set 2026-02-28 by Jan de Heer and Steve Muir ("Private Tools").
- dmgordo/LJCR GitHub coverings/coverdata.json (last commit 2022-12-19): C(41,12,5) size 2429, lower bound 1121.
- GitHub, arXiv and web searches over the last 24 months (NOVELTY panelist): no value of 2207 or less (or below 2244)
  for this cell.

## Not claimed
- Not claimed optimal: the best lower bound we know of is 1121 (LJCR low_bd); the Schonheim bound is 1070.
- No other cell, no lottery (v,k,t,m) covering, no lower bound.
- The table may change after the fetch times above; recheck the cell before relying on it.

## Credits
- Derived from de Heer & Muir's design (no search) by Kaust-a-laut, with Claude Code (Anthropic) running
  claude-opus-5-5, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
- Built by single-point derivation (rule R7, at minimum-degree point p = 16, degree 2207) from the published
  8735-block (42,13,6) covering design in the La Jolla Covering Repository Zenodo v1.2 archive (contributed by Jan de
  Heer and Steve Muir, 2026-02-28).
- The live coveringrepository.com (42,13,6) record is 8718 (already so in the 2026-10-15T23:10:40Z fetch, and again
  at 2026-10-17T00:52:19Z). That is a different design, which we did not examine.
- The record compared against and the table history: the La Jolla Covering Repository by Daniel M. Gordon
  (https://dmgordon.org/covering-designs/, data https://github.com/dmgordo/LJCR and
  https://doi.org/10.5281/zenodo.10779736), and the Covering Repository (https://coveringrepository.com/), which
  carries the live table.
