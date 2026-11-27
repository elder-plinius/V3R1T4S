# Honesty gate: R_3_5_7.txt (target small-ramsey-lower-bounds, partial win p1)

status: CONFIRMED_PARTIAL
partial_win: p1
confirmed_scope: The circulant 3-colouring of K_251 in object/R_3_5_7.txt (sha256 3728547a...351976) has, by two independent exact checks, no monochromatic K3 in colour 1, K5 in colour 2 or K7 in colour 3, so R(3,5,7) >= 252, strictly above the bound 241 in DS1 revision #18 (April 24, 2026, Table XIb) and above every lower bound for R(3,5,7) found in arXiv titles and abstracts up to 2026-10-21.

## How the panel was run
- REPRODUCE: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, started inside its own copy of
  claim/ (panel/.work/reproduce/claim), 09:01:46Z to 09:02:41Z. pass: true. The session was short; the main session
  reran the skeptic's own checker (work/chk.py) from a copy and got byte-identical output (sha256 4d0f0aaa...e818, the
  hash the verdict quotes; 0.8 s), so the reported results are real.
- NOVELTY: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, own copy of claim/, honest single
  fetches, 09:07:49Z to 09:10:16Z. pass: true.
- CRITERION: a headless `claude -p` session (claude-opus-5-5, effort high), fresh, own copy of claim/, honest single
  fetches allowed, 09:10:51Z to 09:15:33Z. pass: true.
- One after another, never in parallel. claim/ (including literature_record.md, the author's search record) was
  fixed before REPRODUCE started; nothing changed during the panel.

## What the gate checked (read by the run's main session, 2026-10-25T09:16Z)
- Reproduction: REPRODUCE (own exhaustive search over all 251 vertices without symmetry: no K3, K5, K7, controls K2,
  K4, K6 found; CaDiCaL: UNSAT for each forbidden clique through vertex 0, SAT for each control), NOVELTY (own search:
  clique numbers 2, 4, 6) and CRITERION (Bron-Kerbosch: 2, 4, 6; CaDiCaL UNSAT through vertex 0) agree with
  verify_circ.py. Object hash 3728547a... matched in every session. Deterministic (REPRODUCE reran and hashed).
- Bar: DS1 revision of April 24, 2026, Table XIb, R(3,5,7) >= 241 (reference 6.2.g), read by NOVELTY (PDF 09:08:09Z)
  and CRITERION (PDF 09:11:57Z), HTTP 200, sha256 9519a676..., the scout's bytes. 252 > 241, not a tie.
- Implied bounds: 6.2.g at best 241 (the table entry itself), 6.2.j at most 236, 6.2.o/q/r less; R(7,9) >= 252 [Kuz]
  implies nothing for R(3,5,7) without the split. Both NOVELTY and CRITERION checked this.
- Newer papers: NOVELTY (arXiv API 300 entries, two web searches, full texts of Rowley 2203.13476, Exoo-Tatarevic,
  Kuznetsov, 2509.03784; Exoo's page) and CRITERION (four arXiv API queries plus an id_list check of the named 2026
  papers) found no R(3,5,7) bound above 241. This repo: TROPHY_CASE.md has no Ramsey entry; open pull requests pages 1
  and 2 have no Ramsey claim (NOVELTY; R(3,3,12)'s NOVELTY scanned all 357 the same morning).
- Table access: one plain request per page, honest User-Agent, no block, no retry. ExTa/ (HTTP 403 to run 4's scout,
  not retried) is listed under "Needs you" in REPORT.md.
- Scope: one object, one cell. Remaining risk (CRITERION): arXiv titles and abstracts only.
