# How we found it (contributor text, unverified)

By Kaust-a-laut, with Claude Code (Anthropic) running claude-opus-5-5.

1. Run 2026-10-15-1535 merged the live coveringrepository.com table with the LJCR Zenodo v1.2 history and found that
   cells whose record came from a generic construction ("Simple construction from ...") improved ~5x more often than
   cells already searched by local search.
2. Run 2026-10-15-2309 froze its preregistration (`how-we-built-it/PREREG.md`) and screened 80 unscreened `t = 3`
   simple-construction cells cold at `live - 1` for 180 s per cell (`how-we-built-it/screen.py`, `pnoise = 0.25`).
3. On `C(53,20,3)` (whose value 35 dated from 2009-01-21, "Simple construction from (54,20,3)"), `covsearch3` reached 0
   uncovered triples at `b = 34` in 33.3 s (`142760` steps, `how-we-built-it/search_b34.log`).
4. What did not work: pushing one block lower (`b = 33`) ended at 75 uncovered triples after 600 s; pushing the
   neighbour `C(54,20,3)` to `b = 34` ended at 116 uncovered triples after 600 s.
