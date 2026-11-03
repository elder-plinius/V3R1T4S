# Honesty gate: C(53,20,3) <= 34

gate written: 2026-10-16T02:31:45Z (date -u), after reading reproduce.md, novelty.md and criterion.md in claims/C53_20_3/panel/.

## Panel
- reproduce.md: context subagent (fresh, saw only claim/); own checker written from the definition, self-tested on a
  Fano plane and 6 broken variants; exhaustive check of all 23426 triples twice, 0 uncovered; hash matches;
  deterministic; REPRODUCE.md commands agree. pass: true.
- novelty.md: context subagent (fresh, saw only claim/); one plain fetch of the live table at 2026-10-16T02:08:27Z,
  HTTP 200, byte-identical to the claim's copy, row "53 20 03 03 35"; Zenodo v1.2 (latest) size 35, low_bd 30;
  GitHub LJCR 2022 size 35, low_bd 30; arXiv, GitHub, hobbyist and web searches (including irsi.ai/tables.html)
  found no value <= 34; TROPHY_CASE.md and open PRs: nothing on covering designs. pass: true.
- criterion.md: context subagent (fresh, saw only claim/); every clause met literally; clause 4 (6-month search)
  settled by NOVELTY. pass: true.

## Downgrade checks (kit/RUN.md step 7)
- Hedging panelist: no.
- Reproduction mismatch: none. Strictly better than the live table: 34 < 35 (live table re-fetched at
  2026-10-16T02:08:27Z, HTTP 200).
- Stretched criterion or subsumption: no. No cell with v' >= 53, k' <= 20, t' >= 3 has value <= 34.
- Scope wider than reproduced: no. Sample presented as complete: no (all 23426 triples checked exhaustively).
  Bundling: one cell. Table access: one plain curl request per URL with V3R1T4S User-Agent.

status: CONFIRMED_SOLUTION
confirmed_scope: The file C53_20_3_34blocks.txt (sha256 ab13770f500eb1e64f71e63b1cd61f98500ddb58e0f22f985cef400861950a5e) contains 34 distinct blocks of size 20 over {1..53} that exhaustively cover all C(53,3) = 23426 3-subsets, which is one fewer than the 35 blocks listed for (53,20,3) in the coveringrepository.com plain table as fetched at 2026-10-15T23:10:40Z and in LJCR Zenodo v1.2 and dmgordo/LJCR GitHub coverdata.json.
