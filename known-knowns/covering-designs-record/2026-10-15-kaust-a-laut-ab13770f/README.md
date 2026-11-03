# C(53,20,3) <= 34: a (53,20,3) covering design with 34 blocks

## What
The file C53_20_3_34blocks.txt (sha256 ab13770f500eb1e64f71e63b1cd61f98500ddb58e0f22f985cef400861950a5e) contains 34 distinct blocks of size 20 over {1..53} that exhaustively cover all C(53,3) = 23426 3-subsets, which is one fewer than the 35 blocks listed for (53,20,3) in the coveringrepository.com plain table as fetched at 2026-10-15T23:10:40Z and in LJCR Zenodo v1.2 and dmgordo/LJCR GitHub coverdata.json.

Target: covering-designs-record (V3R1T4S bank). One cell: (v,k,t) = (53,20,3), plain covering (every 3-subset in at
least one block), b = 34.

## Check it yourself
From this folder, in a fresh shell:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (a few seconds on a laptop; Python 3 standard library only). The checker enumerates all
23426 3-subsets of {1,...,53}. Its real output is in verify-it-yourself/RECEIPTS.md.

## Compared to
- coveringrepository.com, plain (v,k,t) table (m = t rows), cell (53,20,3): 35.
  https://coveringrepository.com/download_archive_vkt.aspx, fetched 2026-10-15T23:10:40Z (HTTP 200) and again by the
  NOVELTY panelist at 2026-10-16T02:08:27Z (HTTP 200, same bytes). Details in the-record-we-beat/.
- La Jolla Covering Repository (D. M. Gordon), Zenodo v1.2 (2026-04-24, the latest version): C(53,20,3) size 35,
  lower bound 30, set 2009-01-21 by "Simple construction from (54,20,3)".
- dmgordo/LJCR GitHub coverings/coverdata.json (last commit 2022-12-19): C(53,20,3) size 35, lower bound 30.
- GitHub, arXiv and web searches over the last 24 months (NOVELTY panelist): no value of 34 or less for this cell.

## Not claimed
- Not claimed optimal: the best lower bound we know of is 30 (LJCR low_bd); the Schonheim bound is 24.
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
