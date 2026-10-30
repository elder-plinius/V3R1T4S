# Honesty gate: R_3_3_12.txt (target small-ramsey-lower-bounds, partial win p1)

status: CONFIRMED_PARTIAL
partial_win: p1
confirmed_scope: The circulant 3-colouring of K_202 in object/R_3_3_12.txt has no monochromatic K_3 in colours 1 and 2 and no K_12 in colour 3 (checked by all-triples brute force, a CaDiCaL UNSAT proof and the author's exhaustive B&B), so R(3,3,12) >= 203, strictly above DS1 (April 24, 2026) Table XIb's 194 and above every bound for this cell I found in arXiv papers newer than that revision.

## How the panel was run
- REPRODUCE: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, started inside its own copy of
  claim/ (panel/.work/reproduce/claim), 08:51:07Z to 08:52:50Z. pass: true.
- NOVELTY: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, own copy of claim/, honest single
  fetches, 08:53:09Z to 08:56:24Z. pass: true.
- CRITERION: a headless `claude -p` session (claude-opus-5-5, effort high), fresh, own copy of claim/, honest single
  fetches allowed, 08:57:16Z to 09:01:01Z. pass: true.
- One after another, never in parallel. claim/ (including literature_record.md, the author's search record) was
  fixed before REPRODUCE started; nothing changed during the panel.

## What the gate checked (read by the run's main session, 2026-10-25T09:02Z)
- Reproduction: REPRODUCE (own B&B: clique numbers 2, 2, 11; CaDiCaL: K12 through vertex 0 UNSAT, K11 SAT as control
  with a checked witness), NOVELTY (own checker: no K3, no K3, no K12) and CRITERION (all triples for colours 1 and 2:
  0 triangles; CaDiCaL K12 through vertex 0 UNSAT, K11 SAT as control) agree with verify_circ.py. Object hash
  eeb47c398be7c450cadf8d9b5939d4996761911a1ddba276e6d820b87fd0db1b matched in every session. Deterministic (REPRODUCE
  reran and diffed).
- Bar: DS1 revision of April 24, 2026, Table XIb, R(3,3,12) >= 194 [ExT], read by NOVELTY (PDF 08:53:21Z) and CRITERION
  (PDF 08:58:08Z), HTTP 200, sha256 9519a676..., the scout's bytes. 203 > 194, not a tie. Fetch age: minutes.
- Implied bounds: 6.2.g gives 185 (R(3,11) >= 47); 6.2.j, 6.2.o, 6.2.q, 6.2.r give at most 156. Both NOVELTY and
  CRITERION checked this. CRITERION notes that 203 equals the ceiling of the null pipeline (R(5,12) >= 203 [Kuz], split
  by the published Exoo-Tatarevic method): the method is not new, only its application to this colouring; p1 asks for
  the colouring.
- Newer papers: NOVELTY (arXiv API, two web searches, Exoo's page, full text of 2609.28455, 2509.03784, 2601.05221) and
  CRITERION (two arXiv API queries of 150 and 200 entries, full text of 2609.28455, two web searches) found no
  R(3,3,12) bound above 194. This repo: TROPHY_CASE.md has no Ramsey entry; 357 open pull requests have no Ramsey
  claim (NOVELTY).
- Table access: one plain request per page, honest User-Agent, no block, no retry. ExTa/ (HTTP 403 to run 4's scout,
  not retried) is listed under "Needs you" in REPORT.md.
- Scope: one object, one cell. Remaining risk (NOVELTY, CRITERION): keyword searches of arXiv and the web; full-text-only
  or unindexed mentions could be missed.
