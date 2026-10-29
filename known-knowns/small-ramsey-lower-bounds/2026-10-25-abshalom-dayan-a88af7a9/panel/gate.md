# Honesty gate: R_3_3_9.txt (target small-ramsey-lower-bounds, partial win p1)

status: CONFIRMED_PARTIAL
partial_win: p1
confirmed_scope: The circulant 3-colouring of K_132 in object/R_3_3_9.txt (sha256 a88af7a9fb8fc8eb0ddf226628db6f59df6c1fb8504ed3ec80d2eeaf972a64cd) has no monochromatic K_3 in colours 1 and 2 and no K_9 in colour 3 (checked exhaustively by three independent methods), so R(3,3,9) >= 133, which is strictly above the 129 in DS1 revision #18 (April 24, 2026) Table XIb and above every bound I found in arXiv papers posted or updated after that revision.

## How the panel was run
- REPRODUCE: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, started inside its own copy of
  claim/ (panel/.work/reproduce/claim), 09:16:18Z to 09:21:10Z. pass: true.
- NOVELTY: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, own copy of claim/, honest single
  fetches, 09:21:49Z to 09:24:14Z. pass: true.
- CRITERION: a headless `claude -p` session (claude-opus-5-5, effort high), fresh, own copy of claim/, honest single
  fetches allowed, 09:24:36Z to 09:28:53Z. pass: true.
- One after another, never in parallel. claim/ (including literature_record.md, the author's search record) was
  fixed before REPRODUCE started; nothing changed during the panel.

## What the gate checked (read by the run's main session, 2026-10-25T09:29Z)
- Reproduction: REPRODUCE (own B&B through vertex 0: clique numbers 2, 2, 8; CaDiCaL: K9 through vertex 0 UNSAT, K8
  SAT as control; deterministic over two reruns), NOVELTY (own search: 2, 2, 8; colours 1 and 2 together are exactly
  the K5-free colour of Kuznetsov's (5,9) circulant) and CRITERION (B&B 2, 2, 8; CaDiCaL UNSAT; and a full-graph check
  without symmetry: 0 triangles in colours 1 and 2, clique number 8 in colour 3) agree with verify_circ.py and the
  run's check_fast.py. Object hash a88af7a9... matched in every session.
- Bar: DS1 revision of April 24, 2026, Table XIb, R(3,3,9) >= 129 [Ex18], read by NOVELTY (PDF 09:22:07Z) and CRITERION
  (PDF 09:25:26Z), HTTP 200, sha256 9519a676..., the scout's bytes. 133 > 129, not a tie.
- Implied bounds: 6.2.g gives 109, 6.2.j at most 104, 6.2.o/q/r at most 88, monotonicity 103; R(5,9) >= 133 [Kuz] does
  not imply the cell (Exoo and Tatarevic note that splitting can fail). Both NOVELTY and CRITERION checked this.
- Newer papers: NOVELTY (arXiv API since 2024-10, Exoo's page, Exoo-Tatarevic and Kuznetsov full texts) and CRITERION
  (three arXiv API queries, 580 entries since 2026-04-24, id_list check of the named 2026 papers, five full PDFs)
  found no R(3,3,9) bound above 129. This repo: TROPHY_CASE.md has no Ramsey entry; open pull requests pages 1 and 2
  and an issue search have no Ramsey claim (NOVELTY).
- Table access: one plain request per page, honest User-Agent, no block, no retry. ExTa/ (HTTP 403 to run 4's scout,
  not retried) is listed under "Needs you" in REPORT.md.
- Scope: one object, one cell. Remaining risk (CRITERION): keyword searches; a bound given only in a paper's body
  could be missed.
