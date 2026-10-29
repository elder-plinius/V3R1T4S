# Honesty gate: R_3_4_7.txt (target small-ramsey-lower-bounds, partial win p1)

status: CONFIRMED_PARTIAL
partial_win: p1
confirmed_scope: The circulant 3-colouring of K_153 in object/R_3_4_7.txt (sha256 e9fa8b95...6a40) has no colour-1 K3, no colour-2 K4 and no colour-3 K7, which I verified exhaustively by 3 independent methods, so R(3,4,7) >= 154, which is strictly above the R(3,4,7) >= 152 in DS1 revision #18 (April 24, 2026) Table XIb and above every bound for that cell in arXiv papers whose metadata (searched 2026-10-25) mentions Ramsey and that were submitted since April 2026.

## How the panel was run
- REPRODUCE: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, started inside its own copy of
  claim/ (panel/.work/reproduce/claim) by weekend run 5, 09:29:17Z to 09:30:28Z. pass: true. The session was short, so
  weekend run 7's main session reran the skeptic's own work/mycheck.py and work/sat.py from a copy at about 11:17Z:
  same output as quoted in reproduce.md (clique numbers 2, 3, 6; K3, K4, K7 UNSAT; controls K2 [1, 2], K3 [1, 3, 5],
  K6 [1, 7, 13, 24, 35, 74] SAT and valid). claim/ is unchanged since that copy (diff -r, work/ excluded).
- NOVELTY: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, own copy of claim/, honest single
  fetches, started by weekend run 7, 11:03:53Z to 11:12:15Z. pass: true.
- CRITERION: a headless `claude -p` session (claude-opus-5-5, effort high), fresh, own copy of claim/, honest single
  fetches allowed, 11:12:19Z to 11:15:37Z. pass: true.
- One after another, never in parallel. claim/ was fixed at
  09:47Z and not changed during the panel.

## What the gate checked (read by weekend run 7's main session, 2026-10-25T11:16:18Z)
- Reproduction: REPRODUCE (exhaustive B&B over all 153 vertices without symmetry: clique numbers 2, 3, 6; CaDiCaL
  UNSAT for K3, K4, K7 with all vertices free; negative control detected), NOVELTY (own search through vertex 0: 2, 3,
  6), CRITERION (triangle and K4 counts over all vertices 0 and 0; Bron-Kerbosch: colour-3 maximum 6; CaDiCaL UNSAT
  in N(0)) and the run's own checker (runs/2026-10-25-1101/attempts/evaluator-first: bitset B&B through vertex 0 after
  verifying the expanded matrix is circulant, plus CaDiCaL: 2, 3, 6) agree with verify_circ.py. Object sha256
  e9fa8b95... matched in every session. Deterministic (REPRODUCE reran and hashed).
- Bar: DS1 revision #18 (April 24, 2026), Table XIb, R(3,4,7) >= 152 [ExT], read by NOVELTY (PDF 11:04:18Z), CRITERION
  (about 11:13:06Z) and this run's scout (11:04:12Z); PDF sha256 9519a676... each time, the bytes of run 5's scout.
  154 > 152, not a tie. Panel fetches are under 6 hours old.
- Implied bounds: 6.2.g gives 4R(4,6) - 3 = 141, 6.2.q 96, other DS1 constructions less; NOVELTY's and CRITERION's
  checks agree. Smaller cells do not reach 154.
- Newer papers: NOVELTY (arXiv API 93 entries, all-fields query "R(3,4,7)" 0 entries, the four 2026 papers named in the
  bank, one web search, Exoo's page) and CRITERION (all 362 arXiv entries with Ramsey in the metadata submitted since
  April 2026, two web searches) found no bound for R(3,4,7) above 152.
- This repository: TROPHY_CASE.md has no Ramsey entry; NOVELTY read 369 open pull requests (pages 1 to 5): the Ramsey
  ones are #731 to #735, this workspace's own five other cells; none concerns R(3,4,7).
- Table access: one plain request per page, honest User-Agent, no block, no retry. Exoo's ExTa/ folder (HTTP 403 to
  run 4's scout, not retried) stays unchecked.
- Scope: one object, one cell. The confirmed_scope is CRITERION's sentence; its remaining risk is arXiv metadata only,
  not full texts. No hedging verdict: NOVELTY's caveat ("a modest and derived one") is about significance, not about
  whether 154 > 152.
