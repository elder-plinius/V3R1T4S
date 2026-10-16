# Honesty gate: C(85,24,3) <= 76

gate written: 2026-10-16T01:54:15Z (date -u), after reading reproduce.md, novelty.md and criterion.md in claims/C85_24_3/panel/.

## Panel
- reproduce.md: context subagent (fresh, saw only claim/); own checker written from the definition, self-tested on a
  Fano plane and 6 broken variants; exhaustive check of all 98770 triples two ways, 0 uncovered; hash matches;
  deterministic; REPRODUCE.md commands agree. pass: true.
- novelty.md: context subagent (fresh, saw only claim/); one plain fetch of the live table at 2026-10-15T23:26:02Z,
  HTTP 200, byte-identical to the claim's copy, row "85 24 03 03 77"; latest-improvements page has no (85,24,3) entry;
  Zenodo v1.2 (latest) size 77, low_bd 61; GitHub LJCR 2022 size 77, low_bd 61; arXiv, GitHub, hobbyist and web
  searches (24 and 6 months) found no value <= 76; TROPHY_CASE.md and 16 open PRs: nothing on covering designs.
  pass: true.
- criterion.md: context subagent (fresh, saw only claim/); every clause met literally; clause 4 (6-month search)
  left to NOVELTY, which settled it. pass: true.

## Downgrade checks (kit/RUN.md step 7)
- Hedging panelist: no. CRITERION names two dependencies: the 6-month search (done by NOVELTY, pass) and its own
  blocked re-fetch of coveringrepository.com (below). Neither is a doubt about the object or the comparison.
- Reproduction mismatch: none. Strictly better than the live table: 76 < 77 (fetch at 23:26:02Z by NOVELTY, under 6 h
  old, so no new fetch is needed). Stretched criterion: no; "live LJCR value" is read as the Zenodo v1.2 data linked
  from dmgordon.org/covering-designs/.
- Scope wider than reproduced: no. Sample presented as complete: no (exhaustive). Capped search used as an
  exclusion: no. Bundling: one cell. Probable prime: not applicable.
- Table access: every fetch was one plain curl request with a User-Agent naming V3R1T4S. CRITERION's extra re-fetch
  at 2026-10-15T23:28:41Z got HTTP 403 (Cloudflare block); it was not retried. The live value had already been read
  with HTTP 200 at 23:10:40Z (main session) and 23:26:02Z (NOVELTY), so no value was obtained by evasion.

status: CONFIRMED_SOLUTION
confirmed_scope: The file C85_24_3_76blocks.txt (sha256 d111b0feb0cd74f5af84f8bbf660d65979caca2eb05885191dbd3fb63c14ea53) is a (85,24,3) covering design with 76 blocks, covering all 98770 3-subsets of {1..85} as checked exhaustively, which is one fewer than the 77 listed for (85,24,3) in the coveringrepository.com plain table as fetched by the claimant at 2026-10-15T23:10:40Z and in the LJCR Zenodo v1.2 and dmgordo/LJCR GitHub coverdata.json files as re-fetched at 2026-10-15T23:29:59Z and 23:30:17Z.
