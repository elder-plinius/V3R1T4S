# Honesty gate: R_3_3_15.txt (target small-ramsey-lower-bounds, partial win p1)

status: CONFIRMED_PARTIAL
partial_win: p1
confirmed_scope: The 3-colouring of K_271 in object/R_3_3_15.txt has no colour-1 triangle, no colour-2 triangle and no colour-3 K_15 (checked exhaustively), so R(3,3,15) >= 272, which exceeds the R(3,3,15) >= 269 of DS1 (revision of April 24, 2026, Table XIb) and every bound I found in newer arXiv papers or implied by DS1's Section 6.2 constructions; it is a corollary of the same object's 266-vertex R(3,3,14) colouring via the folklore colour-3 join.

## How the panel was run
- REPRODUCE: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, started inside its own copy of
  claim/ (panel/.work/reproduce/claim) by weekend run 7, 11:24:23Z to 11:32:36Z. pass: true. (It started one second
  before the previous cell's CRITERION session exited; that session had already written its verdict.)
- NOVELTY: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, own copy of claim/, honest single
  fetches, 11:32:56Z to 11:43:07Z. pass: true.
- CRITERION: a headless `claude -p` session (claude-opus-5-5, effort high), fresh, own copy of claim/, honest single
  fetches allowed, 11:43:24Z to 11:51:06Z (panel/.work/criterion/started.txt). pass: true.
- One after another. claim/ was fixed at 10:03Z and 10:07Z by
  run 5 and not changed during the panel.

## What the gate checked (read by weekend run 7's main session, 2026-10-25T11:51:47Z)
- Reproduction: REPRODUCE (all triples for colours 1 and 2: no triangle, 5724 and 6655 edges; structure checked on
  the matrix; colour-3 B&B through vertex 0 on the circulant part: 13; CaDiCaL "K14 through 0": UNSAT in 281 s),
  NOVELTY (own check: 0 triangles, structure ok, 13), CRITERION (every colour-1/2 edge checked for a same-colour common
  neighbour: none; structure; B&B 13; CaDiCaL "K13 in the colour-3 neighbourhood of 0": UNSAT in 237 s) and the run's
  own checker (runs/2026-10-25-1101/attempts/evaluator-first/out/R_3_3_15.txt: B&B 13 with the same node count as
  REPRODUCE's, CaDiCaL K14 through 0 UNSAT, K13 SAT with a re-checked witness) agree with verify_join.py (colour-3
  clique number 14). Object sha256 4e457e7e... matched in every session. No panelist ran a structure-blind search on
  the whole 271-vertex colour-3 graph to completion; all rely on the structure, which each verified on the matrix
  (circulant part, block without colour-3 edges, cross edges colour 3).
- Bar: DS1 revision #18 (April 24, 2026), Table XIb, R(3,3,15) >= 269 [ExT], read by NOVELTY (PDF 11:33:22Z),
  CRITERION (11:44:21Z) and this run's scout (11:04:12Z), PDF sha256 9519a676... each time. 272 > 269, not a tie.
- Implied bounds: 6.2.g gives 4R(3,14) - 3 = 265 with DS1's current R(3,14) >= 67 (DS1's text: 261, from 66); the
  colour-3 join from DS1's R(3,3,14) >= 242 gives 247; 6.2.q/r less. None reaches 272.
- Dependence (CRITERION): the value rests on the new 266-vertex R(3,3,14) colouring, the object of the separate package
  2026-10-25-abshalom-dayan-d46e9b16 (open draft PR #733); the step 267 -> 272 is the folklore join. The scope sentence
  says so. As a cell record under p1's wording it qualifies; it is not an independent second idea, and REPORT.md
  asks the human how to file it.
- Newer papers: NOVELTY (two web searches, full text of 2509.03784, Exoo's page, the author's arXiv listings) and
  CRITERION (439 unique arXiv entries from three API queries, the four 2026 papers named in the bank, two web searches)
  found no bound for R(3,3,15) above 269; 2609.28455 is asymptotic.
- This repository: TROPHY_CASE.md has no Ramsey entry; NOVELTY read 379 open pull requests: the Ramsey ones are #731 to
  #735 (this workspace's other cells, #733 the base colouring); none concerns R(3,3,15).
- Table access: one plain request per page, honest User-Agent, no block, no retry; ExTa/ not requested.
- Scope: one object, one cell; the confirmed_scope is CRITERION's sentence, exactly.
