# How we found it (contributor text, unverified)

By Kaust-a-laut, with Claude Code (Anthropic) running claude-opus-5-5.

1. Run 2026-10-15-1535 merged the live coveringrepository.com table with the LJCR Zenodo v1.2 history and screened
   construction-method cells cold at `live - 1` for 180 s per cell. On `C(85,24,3)` (whose value 77 dated from 2009,
   "Simple construction from (86,24,3)"), that 180 s screen ended as a near miss with only 2 of 98770 3-subsets
   uncovered.
2. Run 2026-10-15-2309 froze its preregistration (`how-we-built-it/PREREG.md`) and launched a 4-seed parallel search
   (`how-we-built-it/multiseed.py`) on `C(85,24,3)` at `b = 76` with seeds `11..14` and `pnoise` values `0.2, 0.25, 0.3, 0.25`.
   Seed 11 (`pnoise = 0.2`) reached 0 uncovered triples in 302.1 s (`701893` steps, `how-we-built-it/C85_24_3_b76_s11_pn0.2.log`).
3. What did not work: pushing one block lower (`b = 75`) stalled at 1863 uncovered after 1800 s; pushing the
   neighbour `C(86,24,3)` to `b = 76` ended at 95 uncovered after 1800 s.
4. The object passed two independent exhaustive checkers and self-break controls, then went to three fresh-context
   skeptic subagents (`panel/`), all of which passed (`pass: true`).
