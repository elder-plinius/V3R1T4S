# Honesty gate: C(41,12,5) <= 2207

gate written: 2026-10-16T02:31:30Z (date -u), after reading reproduce.md, novelty.md and criterion.md in claims/C41_12_5/panel/.

## Panel
- reproduce.md: context subagent (fresh, saw only claim/); own checker written from the definition, self-tested on a
  Fano plane and 7 broken variants; exhaustive check of all 749398 5-subsets twice, 0 uncovered; hash matches;
  deterministic; REPRODUCE.md commands agree. pass: true.
- novelty.md: context subagent (fresh, saw only claim/); one plain fetch of the live table at 2026-10-16T02:08:02Z,
  HTTP 200, byte-identical to the claim's copy, row "41 12 05 05 2244"; latest-improvements page has no (41,12,5)
  entry; Zenodo v1.2 (latest) size 2245, low_bd 1121; GitHub LJCR 2022 size 2429, low_bd 1121; arXiv, GitHub,
  hobbyist and web searches (including irsi.ai/tables.html) found no value <= 2207 (or < 2244); TROPHY_CASE.md and
  open PRs: nothing on covering designs. pass: true.
- criterion.md: context subagent (fresh, saw only claim/); every clause met literally; clause 4 (6-month search)
  settled by NOVELTY. pass: true.

## Downgrade checks (kit/RUN.md step 7)
- Hedging panelist: no.
- Reproduction mismatch: none. Strictly better than the live table: 2207 < 2244 by 37 blocks (and < 2245 in Zenodo
  v1.2 by 38 blocks). Live table re-fetched at 2026-10-16T02:08:02Z (HTTP 200).
- Stretched criterion or subsumption: no. Elementary table-level bounds give >= 2421; the 2207-block design comes from
  the minimum-degree point (p = 16, degree 2207) of the specific 8735-block C(42,13,6) design in Zenodo v1.2
  covers.json (whose average point degree is 2703.7), and neither coveringrepository.com nor LJCR noticed or applied
  point-derivation to that block file.
- Scope wider than reproduced: no. Sample presented as complete: no (all 749398 5-subsets checked exhaustively).
  Bundling: one cell. Table access: one plain curl request per URL with V3R1T4S User-Agent.

status: CONFIRMED_SOLUTION
confirmed_scope: The file C41_12_5_2207blocks.txt (sha256 ec985f89dd793006ccf15346b6937419e1ce4e922034d73b18e769fb958778aa) is a valid (41,12,5) covering design with 2207 blocks covering all 749398 5-subsets of {1..41} (checked exhaustively), 37 fewer than the 2244 listed in coveringrepository.com (fetched 2026-10-15T23:10:40Z) and 38 fewer than the 2245 in LJCR Zenodo v1.2.
