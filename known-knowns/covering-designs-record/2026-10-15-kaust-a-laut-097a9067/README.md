# C(61,25,3) <= 27: a (61,25,3) covering design with 27 blocks

## What
The file C61_25_3_27blocks.txt (sha256 097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e) is a (61,25,3) covering design with 27 blocks (all 35990 3-subsets of {1,...,61} checked exhaustively), one fewer than the 28 listed for (61,25,3) in the m = t coveringrepository.com archive as saved by the claim from its fetch at 2026-10-15T23:10:40Z and in the La Jolla Covering Repository Zenodo v1.2 coverdata.json as re-fetched at 2026-10-15T23:18:02Z.

Target: covering-designs-record (V3R1T4S bank). One cell: (v,k,t) = (61,25,3), plain covering (every 3-subset in at
least one block), b = 27.

## Check it yourself
From this folder, in a fresh shell:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (a few seconds on a laptop; Python 3 standard library only). The checker enumerates all
35990 3-subsets of {1,...,61}. Its real output is in verify-it-yourself/RECEIPTS.md.

## Compared to
- coveringrepository.com, plain (v,k,t) table (m = t rows), cell (61,25,3): 28.
  https://coveringrepository.com/download_archive_vkt.aspx, fetched 2026-10-15T23:10:40Z (HTTP 200) and again by the
  NOVELTY panelist at 2026-10-15T23:15:56Z (HTTP 200, same bytes). Details in the-record-we-beat/.
- La Jolla Covering Repository (D. M. Gordon), Zenodo v1.2 (2026-04-24, the latest version): C(61,25,3) size 28,
  lower bound 22, set 2009-01-21 by "Simple construction from (60,24,3)".
- dmgordo/LJCR GitHub coverdata.json (last commit 2022-12-19): no entry with k = 25.
- GitHub, arXiv and web searches over the last 24 months (NOVELTY panelist): no value of 27 or less for this cell.

## Not claimed
- Not claimed optimal: the best lower bound we know of is 22 (LJCR low_bd); the Schonheim bound is 20.
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
