# C(85,24,3) <= 76: a (85,24,3) covering design with 76 blocks

## What
The file C85_24_3_76blocks.txt (sha256 d111b0feb0cd74f5af84f8bbf660d65979caca2eb05885191dbd3fb63c14ea53) is a (85,24,3) covering design with 76 blocks, covering all 98770 3-subsets of {1..85} as checked exhaustively, which is one fewer than the 77 listed for (85,24,3) in the coveringrepository.com plain table as fetched by the claimant at 2026-10-15T23:10:40Z and in the LJCR Zenodo v1.2 and dmgordo/LJCR GitHub coverdata.json files as re-fetched at 2026-10-15T23:29:59Z and 23:30:17Z.

Target: covering-designs-record (V3R1T4S bank). One cell: (v,k,t) = (85,24,3), plain covering (every 3-subset in at
least one block), b = 76.

## Check it yourself
From this folder, in a fresh shell:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (a few seconds on a laptop; Python 3 standard library only). The checker enumerates all
98770 3-subsets of {1,...,85}. Its real output is in verify-it-yourself/RECEIPTS.md.

## Compared to
- coveringrepository.com, plain (v,k,t) table (m = t rows), cell (85,24,3): 77.
  https://coveringrepository.com/download_archive_vkt.aspx, fetched 2026-10-15T23:10:40Z (HTTP 200) and again by the
  NOVELTY panelist at 2026-10-15T23:26:02Z (HTTP 200, same bytes). Details in the-record-we-beat/.
- La Jolla Covering Repository (D. M. Gordon), Zenodo v1.2 (2026-04-24, the latest version): C(85,24,3) size 77,
  lower bound 61, set 2009-01-21 by "Simple construction from (86,24,3)".
- dmgordo/LJCR GitHub coverings/coverdata.json (last commit 2022-12-19): C(85,24,3) size 77, lower bound 61.
- GitHub, arXiv and web searches over the last 24 months (NOVELTY panelist): no value of 76 or less for this cell.

## Not claimed
- Not claimed optimal: the best lower bound we know of is 61 (LJCR low_bd); the Schonheim bound is 54.
- No other cell, no lottery (v,k,t,m) covering, no lower bound.
- The table may change after the fetch times above; recheck the cell before relying on it.

## Credits
- Found by Kaust-a-laut, with Claude Code (Anthropic) running claude-opus-5-5, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
- The record compared against and the table history: the La Jolla Covering Repository by Daniel M. Gordon
  (https://dmgordon.org/covering-designs/, data https://github.com/dmgordo/LJCR and
  https://doi.org/10.5281/zenodo.10779736), and the Covering Repository (https://coveringrepository.com/), which
  carries the live table.
- The search is a weighted tabu local search in the style of Nurmela and Ostergard, as the V3R1T4S bank entry
  suggests (we did not reopen their paper). C compiled with Zig via the ziglang PyPI package (https://ziglang.org/).
