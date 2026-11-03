# Honesty gate: C(36,5,3) <= 812 (claim/C36_5_3_812, target covering-designs-record, full success criterion)
status: CONFIRMED_SOLUTION
confirmed_scope: The 812 blocks in object/C36_5_3_812.txt form a valid (36,5,3) covering design (all 7140 triples covered, 812 distinct 5-subsets of {1..36}), so C(36,5,3) <= 812, which is strictly below the value 821 listed on 2026-10-20 by coveringrepository.com (archive and live search) and by dmgordo/LJCR GitHub coverdata.json, and above the Schonheim bound 756.
gate_utc: 2026-10-20T23:21:00Z
gate_by: an executor session delegated by the workspace's main assistant session to carry out kit/RUN.md step 7 (not one of the three skeptics); it read all three panel files itself

## What I read
- reproduce.md, novelty.md, criterion.md in panel/. Each has its own context line ("subagent (fresh
  executor, saw only claim/)") and ends with pass: true.
- REPRODUCE: own tuple/set checker written from the quoted definition before opening claim/check_cover.py. sha256
  f7a9401c...51da6b23 matches; 812 lines, 812 distinct valid 5-subsets of 1..36; 7140/7140 triples covered
  (exhaustive); Schonheim 756 recomputed; deterministic. The author's checker agrees. It states that the table
  comparison is out of its scope; that is a scope note, not a hedge.
- NOVELTY: one plain GET of coveringrepository.com/download_archive_vkt.aspx at 2026-10-20T23:14:58Z (UA
  "V3R1T4S-skeptic", no cookies, no retries), HTTP 200, sha256 3bc89519...f331f7, row "36 05 03 03 821";
  dmgordo/LJCR GitHub coverdata.json HTTP 200 at 23:15:18Z, C(36,5,3) 821 (low_bd 756); dmgordon.org landing page
  HTTP 200 (no per-cell values). TROPHY_CASE.md and the repo's PRs (open and closed): no (36,5,3). GitHub and web
  search: nothing below 821. The arXiv API hung once and was not retried (CRITERION's arXiv query did return).
- CRITERION: clause by clause against the bank criterion; archive GET 23:15:17Z (821, sha256 identical to the
  claim's copy), live systems.aspx search 23:15:54Z (821), GitHub coverdata.json (821); GitHub repo/issue search and
  shallow clones of recent covering-design repos, arXiv API since 2026-04-20: no (36,5,3) claim. Its
  confirmed_scope is copied above verbatim, with the object path given as it is in this package (object/).
- My own check at the gate (2026-10-20T23:20Z): sha256 unchanged; claim/check_cover.py prints "VALID v=36 k=5 t=3
  b=812 distinct=812 bad_blocks=0 uncovered=0 of 7140 schonheim=756"; my own itertools checker also gives 812
  distinct blocks and 0 of 7140 uncovered; for no point p do the blocks avoiding p cover the other 35 points.

## Downgrade checks (RUN.md step 7)
- Hedging panelist: no. All three end plain pass: true; caveats are stated limitations (unauthenticated GitHub code
  search, arXiv API hang in one panelist) with the gap covered by the other searches.
- Reproduction mismatch: none (two skeptics' own checkers, claim/check_cover.py and my own check agree).
- Strictly better than the live table: yes, 812 < 821 (by 9) on the coveringrepository.com archive and live search
  and in dmgordo/LJCR GitHub coverdata.json. Panel fetches were at 23:14:58Z-23:15:54Z, minutes old at the gate
  (well under 6 hours), so the gate did not fetch again.
- Table value obtained by evasion: no. The author's reads (scout.md, data/fetch_log.txt, claim/table/) are single
  honest requests; the 23:04:56Z per-cell read used tools/live_cell.py after its 12:34 EDT fix (no "Mozilla/5.0"
  UA, no cookie jar). A search of the run folder for browser UAs, cookie replay or retries found none. CRITERION
  does not say how its own GET-then-POST live search handled cookies; the comparison does not rest on that read
  (the plain archive GETs, the compliant 23:04:56Z per-cell read and GitHub coverdata.json each give 821).
- Stretched criterion or hidden quantifier: "the live LJCR value (https://dmgordon.org/covering-designs/)": that
  page has no per-cell values and points to coveringrepository.com and the GitHub/Zenodo data (821); the legacy
  per-cell host failed once (TLS), not retried. Accepted as in the earlier covering-designs gates. Not a downgrade.
- Scope wider than reproduced: no. confirmed_scope is CRITERION's sentence verbatim and covers only this cell.
- Sample presented as complete: no (exhaustive over all 7140 triples). Capped search used as exclusion: no (not
  claimed optimal; the SCIP OPTIMAL is only within the PSL(2,7) 14+14+8 orbit model). Probable prime: n/a.
- Several objects bundled: no. One design, one cell.
- Claim folder edited after the panel: no (claim/ files 19:08 EDT, panel files 19:15-19:18 EDT).

## Subsumption check (stated plainly, checked myself)
- Our own pending PR #596 claims C(35,5,3) <= 713. Adding one point to a
  (35,5,3) covering needs a C(35,4,2) on the old points for the triples through the new point; C(35,4,2) = 105
  (coverdata.json size 105 = low_bd 105, so it cannot be lower). 713 + 105 = 818 > 812: not subsumed.
  With the table's own C(35,5,3) (732 archive, 733 GitHub) the same route gives 837/838.
- CRITERION used 732/733 in its own one-point-extension check rather than our 713 (it saw only claim/); the 713
  route above closes that gap and still leaves a 6-block margin.
- Point deletion from C(37,5,3): table 886, and this workspace has no C(37,5,3) claim (its PSL(2,7) 21+8+8 row is
  capped at 910). Other own covering claims are k=6 cells (C(37,6,3) 468, C(38,6,3) 469) or C(29,5,3) 399, whose
  sum constructions with 7 points are far above 812 (CRITERION's best split was about 837).
- GitHub coverdata.json lists C(35,5,3) = 733 while the coveringrepository archive lists 732; irrelevant to this
  cell under every route above.
- Not a corollary: the 821 record has stood since 2009 and the design is a new PSL(2,7) orbit cover.

## Caveats (honest, not blocking)
- GitHub code search was unauthenticated (repo/issue search plus clones, not a full code grep).
- All three skeptics were subagents of the same assistant product: separate contexts working only from claim/.
- Not claimed optimal; C(36,5,3) stays open (756..812).

Result: passes the gate. The status takes effect only if kit/check_run.py prints CHECK_RUN: PASS.
