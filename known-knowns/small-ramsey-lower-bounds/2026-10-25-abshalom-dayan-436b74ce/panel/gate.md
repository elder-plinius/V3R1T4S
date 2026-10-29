# Honesty gate: R_3_5_6.txt (target small-ramsey-lower-bounds, partial win p1)

status: CONFIRMED_PARTIAL
partial_win: p1
confirmed_scope: The circulant 3-colouring of K_182 in object/R_3_5_6.txt (sha256 436b74cecb10c8263ed5c3413d66993ce1f9d34993718f7b5bb4b31890896826) has, by exhaustive enumeration, no K_3 in colour 1, no K_5 in colour 2 and no K_6 in colour 3, so R(3,5,6) >= 183, which is strictly above the bound 181 in DS1 revision #18 (April 24, 2026) Table XIb and above every R(3,5,6) lower bound in the arXiv titles and abstracts I searched on 2026-10-25 (none of them gives one).

## How the panel was run
- REPRODUCE: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, started inside its own copy of
  claim/ (panel/.work/reproduce/claim) by weekend run 7, 11:15:54Z to 11:16:52Z. pass: true. The session was short, so
  the main session reran the skeptic's own work/mycheck.py and work/sat.py from a copy at about 11:18Z: same output as
  quoted in reproduce.md (clique numbers 2, 4, 5; K3, K5, K6 absent on the full graph; K2, K4, K5 controls present).
- NOVELTY: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, own copy of claim/, honest single
  fetches, 11:17:10Z to 11:20:12Z. pass: true.
- CRITERION: a headless `claude -p` session (claude-opus-5-5, effort high), fresh, own copy of claim/, honest single
  fetches allowed, 11:20:19Z to 11:24:24Z. pass: true.
- One after another. claim/ was fixed at 09:53Z by run 5 and not
  changed during the panel.

## What the gate checked (read by weekend run 7's main session, 2026-10-25T11:25:00Z)
- Reproduction: REPRODUCE (B&B through vertex 0: 2, 4, 5; CaDiCaL on the whole graph without symmetry: K3, K5, K6
  absent, controls present; naive level-by-level clique enumeration: colour 2 counts [182, 6188, 46592, 69524, 0],
  colour 3 [182, 6734, 67704, 193466, 103012, 0]), NOVELTY (own check: K3, K5, K6 absent, K2, K4, K5 present),
  CRITERION (exhaustive bitset search on the full 182-vertex graphs; brute-force counts identical to REPRODUCE's) and
  the run's own checker (runs/2026-10-25-1101/attempts/evaluator-first/out/R_3_5_6.txt: 2, 4, 5 by B&B and CaDiCaL)
  agree with verify_circ.py. Object sha256 436b74ce... matched in every session.
- Bar: DS1 revision #18 (April 24, 2026), Table XIb, R(3,5,6) >= 181 [Ex17], read by NOVELTY (PDF 11:17:29Z), CRITERION
  (11:21:21Z) and this run's scout (11:04:12Z), PDF sha256 9519a676... each time. 183 > 181, not a tie. Panel fetches
  are under 6 hours old.
- Implied bounds: 6.2.g at best 4R(5,5) - 3 = 169 (with R(5,5) >= 43), 6.2.q at most 116, 6.2.r 68, Rowley's 6.2.j
  recurrence about 170 at most; none reaches 182 (NOVELTY and CRITERION agree). R(6,9) >= 183 [Kuz] is a two-colour
  bound and does not imply the split.
- Newer papers: NOVELTY (arXiv API 174 entries, full texts of 2601.15183 and 2509.03784 grepped, two web searches,
  Exoo's page) and CRITERION (439 unique arXiv entries from three queries, the four 2026 papers named in the bank,
  2509.03784's HTML, Exoo's page, one web search) found no bound for R(3,5,6) above 181.
- This repository: TROPHY_CASE.md has no Ramsey entry; NOVELTY read 378 open pull requests: the Ramsey ones are
  #731 to #735 (this workspace's other cells); none concerns R(3,5,6).
- Table access: one plain request per page, honest User-Agent, no block, no retry. Exoo's ExTa/ folder (HTTP 403 to
  run 4's scout) was not requested again and stays unchecked; NOVELTY notes that the DS1 entry 181 is a personal
  communication (Ex17), so unpublished Exoo data above 181 cannot be excluded.
- Scope: one object, one cell; the confirmed_scope is CRITERION's sentence (arXiv titles and abstracts searched).
