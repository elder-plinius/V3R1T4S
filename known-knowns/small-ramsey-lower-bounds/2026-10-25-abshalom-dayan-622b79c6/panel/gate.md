# Honesty gate: R_3_3_11.txt (target small-ramsey-lower-bounds, partial win p1)

status: CONFIRMED_PARTIAL
partial_win: p1
confirmed_scope: The circulant 3-colouring of K_182 in object/R_3_3_11.txt (sha256 622b79c6...1270) has no triangle in colours 1 and 2 and no K_11 in colour 3, verified exhaustively by two independent methods, so R(3,3,11) >= 183, strictly above the bound 174 in DS1 revision #18 (April 24, 2026) Table XIb and above every R(3,3,11) lower bound in the arXiv papers my searches found.

## How the panel was run
- REPRODUCE: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, started inside its own copy of
  claim/ (panel/.work/reproduce/claim), 08:41:18Z to 08:42:29Z. pass: true.
- NOVELTY: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, own copy of claim/, honest single
  fetches, 08:43:32Z to 08:46:34Z. pass: true.
- CRITERION: a headless `claude -p` session (claude-opus-5-5, effort high), fresh, own copy of claim/, honest single
  fetches allowed, 08:46:49Z to 08:50:35Z. pass: true.
- One after another, never in parallel. claim/ (including literature_record.md, the author's search record) was
  fixed before REPRODUCE started; nothing changed during the panel.

## What the gate checked (read by the run's main session, 2026-10-25T08:51:09Z)
- Reproduction: REPRODUCE (full-matrix branch and bound from every vertex: clique numbers 2, 2, 10; CaDiCaL: K11 UNSAT,
  K10 SAT as control), NOVELTY (own clique search through vertex 0: maxima 2, 2, 10) and CRITERION (all C(182,3)
  triples for colours 1 and 2: 0 triangles; CaDiCaL K11 through vertex 0 UNSAT) agree with the run's check_fast.py
  (alpha.c and CaDiCaL) and verify_circ.py. Object hash 622b79c6... matched in every session. Deterministic.
- Bar: DS1 revision of April 24, 2026, Table XIb, R(3,3,11) >= 174 [ExT], read by NOVELTY (PDF 08:44:00Z) and CRITERION
  (PDF 08:47:40Z), HTTP 200, sha256 9519a676..., the scout's bytes. 183 > 174, not a tie. Fetch age: minutes.
- Implied bounds: 6.2.g gives 157 (R(3,10) >= 40); 6.2.j less; R(5,11) >= 183 [Kuz] does not imply the cell (no such
  rule in DS1; the split had to be found). Both NOVELTY and CRITERION checked this.
- Newer papers: NOVELTY (two arXiv API queries, two web searches, Exoo's page, full text of arXiv:2509.03784 and
  2601.15183) and CRITERION (two arXiv API queries of 300 entries, id_list check of the 2026 papers named by the bank,
  full text of 2609.28455 and 2509.03784) found no R(3,3,11) bound above 174. This repo: TROPHY_CASE.md has no Ramsey
  entry; 357 open pull requests have no Ramsey claim (NOVELTY).
- Table access: one plain request per page, honest User-Agent, no block, no retry. ExTa/ (HTTP 403 to run 4's scout,
  not retried) is listed under "Needs you" in REPORT.md.
- Scope: one object, one cell. Remaining risk (CRITERION, NOVELTY): arXiv titles and abstracts only; full-text-only
  mentions could be missed.
