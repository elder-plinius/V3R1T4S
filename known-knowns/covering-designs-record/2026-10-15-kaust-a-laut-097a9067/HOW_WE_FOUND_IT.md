# How we found it (contributor text, unverified)

By Kaust-a-laut, with Claude Code (Anthropic) running claude-opus-5-5.

1. The V3R1T4S research charter points at covering designs. Run 2026-10-15-1535 merged the live coveringrepository.com
   table with the LJCR Zenodo history. Cells whose value came from a generic construction ("simple construction",
   "dynamic programming") had improved about five times as often since April 2026 as cells set by local search, so
   the run screened construction-method cells.
2. A weighted tabu local search (how-we-built-it/covsearch3.c) ran cold, from random blocks, at one block below the
   live value, for 180 s per cell (how-we-built-it/screen.py). Of 157 cells it found one: C(61,25,3) with 27 blocks,
   in 157 s (how-we-built-it/search_b27.log). The cell's 28 dated from 2009 ("Simple construction from (60,24,3)").
3. What did not work in that run: warm starts from published designs minus a block (16 cells, 0 found), redundant
   blocks in published designs (0 of 4645), two-blocks-for-one surgery (0), cyclic orbit covers by MIP (0 found),
   recursive constructions over the whole table (0 beats).
4. That run was cut off before its panel. Run 2026-10-15-2309 re-fetched the tables, froze its rules
   (how-we-built-it/PREREG_panel_run.md) and gave the claim to three fresh-context skeptics (panel/); then the main
   session wrote panel/gate.md.
