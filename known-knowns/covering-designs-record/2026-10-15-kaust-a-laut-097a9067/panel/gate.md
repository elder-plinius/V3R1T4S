# Honesty gate: C(61,25,3) <= 27 (claim carried from run 2026-10-15-1535)

gate written: 2026-10-15T23:26:54Z (date -u), by the run's main session after reading reproduce.md, novelty.md and criterion.md.

## Panel
- reproduce.md: context subagent (fresh, saw only claim/); own checker written from the definition, tested on a
  Fano plane and 7 broken variants; exhaustive check of all 35990 triples two ways, 0 uncovered; hash matches;
  deterministic; REPRODUCE.md commands agree. pass: true.
- novelty.md: context subagent (fresh, saw only claim/); one plain fetch of the live table at 2026-10-15T23:15:56Z,
  HTTP 200, byte-identical to the claim's copy, row "61 25 03 03 28"; the archive matches all 100 entries of the
  latest-improvements page; Zenodo v1.2 (still latest) size 28, low_bd 22; GitHub LJCR 2022 has no k = 25 entry;
  arXiv, GitHub, hobbyist and web searches (24 and 6 months) found no value <= 27; TROPHY_CASE.md and 14 open PRs:
  nothing on covering designs. pass: true.
- criterion.md: context subagent (fresh, saw only claim/); every clause met literally; clause 4 (6-month search)
  left to NOVELTY, which settled it. pass: true.

## Downgrade checks (kit/RUN.md step 7)
- Hedging panelist: no. CRITERION names two dependencies: the 6-month search (done by NOVELTY, pass) and its own
  blocked re-fetch of coveringrepository.com (below). Neither is a doubt about the object or the comparison.
- Reproduction mismatch: none. Strictly better than the live table: 27 < 28 (fetch at 23:15:56Z, under 6 h old,
  so no new fetch is needed). Stretched criterion: no; "live LJCR value" is read as the Zenodo v1.2 data because the
  LJCR site says its database was frozen after 2026-03-01 and lives on GitHub/Zenodo (stated openly by CRITERION).
- Scope wider than reproduced: no. Sample presented as complete: no (exhaustive). Capped search used as an
  exclusion: no. Bundling: one cell. Probable prime: not applicable.
- Table access: every fetch was one plain curl request with a User-Agent naming V3R1T4S. CRITERION's extra re-fetch
  at 2026-10-15T23:16:56Z got HTTP 403 (Cloudflare block); it was not retried. The live value had already been read
  with HTTP 200 at 23:10:40Z (main session) and 23:15:56Z (NOVELTY), so no value was obtained by evasion. No further
  requests go to coveringrepository.com in this run.

status: CONFIRMED_SOLUTION
confirmed_scope: The file C61_25_3_27blocks.txt (sha256 097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e) is a (61,25,3) covering design with 27 blocks (all 35990 3-subsets of {1,...,61} checked exhaustively), one fewer than the 28 listed for (61,25,3) in the m = t coveringrepository.com archive as saved by the claim from its fetch at 2026-10-15T23:10:40Z and in the La Jolla Covering Repository Zenodo v1.2 coverdata.json as re-fetched at 2026-10-15T23:18:02Z.
