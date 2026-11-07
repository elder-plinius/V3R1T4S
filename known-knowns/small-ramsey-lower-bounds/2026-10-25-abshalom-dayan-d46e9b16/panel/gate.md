# Honesty gate: R_3_3_14.txt (target small-ramsey-lower-bounds, partial win p1)

status: CONFIRMED_PARTIAL
partial_win: p1
confirmed_scope: The circulant 3-colouring of K_266 in object/R_3_3_14.txt (sha256 d46e9b16…34ba) has no monochromatic K_3 in colours 1 and 2 and no K_14 in colour 3, verified exhaustively by a SAT/UNSAT search and by the author's branch and bound, so R(3,3,14) ≥ 267, which is strictly above DS1's (April 24, 2026) bound of 242 and above every bound for this cell that I found on arXiv up to 2026-10-21 (titles and abstracts only).

## How the panel was run
- REPRODUCE: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, started inside its own copy of
  claim/ (panel/.work/reproduce/claim). pass: true.
- NOVELTY: a headless `claude -p` session (claude-opus-5-5, effort high), fresh, started inside its own copy of claim/
  (panel/.work/novelty/claim), with web access for honest single fetches. pass: true.
- CRITERION, first session (claude-opus-5-5, effort high, 08:25:48Z to 08:33:59Z): pass: false. Kept unchanged as
  panel/criterion_attempt1.md. Its only reason: p1 also requires N+1 above "any newer arXiv paper for that multicolour
  cell", claim/ held no search record for that clause, and it had no web access, so it could not
  check the clause itself. It found the object correct by two exact methods.
- CRITERION, second session (claude-opus-5-5, effort high, started 08:35:46Z): a new fresh session, after two changes
  (below). Its file is panel/criterion.md.
- All sessions ran one after another, never in parallel; each wrote its own verdict file.

## Changes during the panel (recorded so nothing is hidden)
- After the first CRITERION verdict, the main session added claim/literature_record.md: the author's arXiv API searches
  (runs 4 and 5, four queries, URLs, fetch times, HTTP status and hashes; one new query at 08:34:36Z) and the other
  sources read. CLAIM.md, the object, REPRODUCE.md, table_record.md and verify_circ.py were not changed. REPRODUCE and
  NOVELTY saw claim/ without that file.
- The CRITERION rerun was given honest web access to check every clause itself, and literature_record.md was marked
  as the author's record, not a verdict. The CRITERION role is unchanged.
- Whether a rerun after a procedural fail is acceptable is your call: see REPORT.md, "Needs you".

## What the gate checked (read by the run's main session, 2026-10-25T08:41:09Z)
- Reproduction: every exact check agrees. REPRODUCE: own branch and bound (clique number of colour 3 exactly 13,
  1943452 nodes, deterministic over two runs) and own CaDiCaL encoding (size 13 SAT, size 14 UNSAT); explicit-matrix
  triangle count 0 in colours 1 and 2. NOVELTY: own branch and bound (no 13-clique in the 172 colour-3 neighbours of 0,
  12-clique found as control). CRITERION (second session): own CaDiCaL search split into 86 orbit subproblems, all UNSAT,
  K13 witness re-checked as control. CRITERION (first session): own bitset branch and bound plus CaDiCaL UNSAT (295.4 s)
  with mutation controls. The run's own checkers (check_fast.py: alpha.c and CaDiCaL; verify_circ.py) agree. No
  mismatch; the object hash d46e9b16... matched in every session.
- Bar: DS1 revision of April 24, 2026, Table XIb, R(3,3,14) >= 242 [ExT], read by NOVELTY (PDF fetched 07:59:00Z) and
  by CRITERION (PDF fetched 08:37:01Z), both HTTP 200 with sha256 9519a676..., the same bytes as the scout's copy.
  267 > 242: not a tie. Fetch age at the gate: under 2 hours.
- Implied bounds: both NOVELTY and CRITERION worked through DS1 6.2 (6.2.g gives 241 with R(3,13) >= 61); none reaches
  267. R(5,14) >= 267 [Kuz] does not imply the cell (the split had to be found).
- Newer papers: NOVELTY (arXiv API, 48 entries; abstract pages of the 2026 Ramsey papers; ScaleAutoResearch-Ramsey)
  and CRITERION (two arXiv API queries, 300 and 86 entries, to 2026-10-21; one web search) found nothing for this cell.
  This repo: TROPHY_CASE.md has no Ramsey entry; 353 open pull requests have no Ramsey claim (NOVELTY).
- Table access: every fetch was one plain request with an honest User-Agent; no block, no retry. The Exoo-Tatarevic
  ExTa/ folder answered 403 to run 4's scout once and was not retried (REPORT.md, "Needs you").
- Scope: one object, one cell. Other cells built the same way are separate claims in their own run folders.
- Remaining risk, stated by CRITERION: arXiv titles and abstracts only; a paper that gives this cell only in its full
  text would not have been found.
