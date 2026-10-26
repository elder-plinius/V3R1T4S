# Honesty gate: C(38,6,3) <= 469 (claim/C38_6_3_469, target covering-designs-record, full success criterion)
status: CONFIRMED_SOLUTION
confirmed_scope: The file object/C38_6_3_469blocks.txt (sha256 09d52bad9c72663e43634c83520d60931a47aa3f3bf45f5947018c18ef79345b) is a (38,6,3) covering design with 469 blocks, checked exhaustively over all 8436 triples, so C(38,6,3) <= 469, which is strictly below the value 510 shown on 2026-10-20 by the live coveringrepository.com plain table (read with a rule-5-compliant client), the LJCR GitHub data and the LJCR Zenodo v1.2 record.
gate_utc: 2026-10-20T16:42:25Z
gate_by: an executor session delegated by the workspace's main assistant session to carry out kit/RUN.md step 7 (not one of the three skeptics); it read all three panel files itself

## What I read
- reproduce.md, novelty.md, criterion.md in panel/, each written by a separate subagent given only its own copy of claim/ (each has its own context: line). All three end with pass: true.
- REPRODUCE: wrote its own checker from the definition before opening claim/checker.py (quoted). 469 distinct valid 6-subsets of 1..38, 8436/8436 triples covered (exhaustive), Schonheim 425 (also by hand), sha256 matches, deterministic on rerun, coverage multiplicities sum to 469*20, four own negative controls plus the two packaged ones all rejected by both checkers with matching counts. Optional rebuild not run (ortools missing); the claim rests on the block file.
- NOVELTY: plain curl of coveringrepository.com/download_archive_vkt.aspx at 2026-10-20T16:35:04Z, HTTP 200, sha256 3bc89519...f331f7: 38 06 03 03 510. Fixed live_cell.py search-form read at 16:35:24Z: 510. LJCR GitHub coverdata.json (16:35:04Z, HTTP 200): 510; Zenodo v1.2 still newest (16:35:05Z). Latest-improvements page: no (38,6,3) row. arXiv (site search; API unreachable, not retried), web, lottery wheels, hobbyist repo (TheEslabonGroup, ex-thebrockchain), TROPHY_CASE.md and all 583 repo PRs: nothing at or below 510.
- CRITERION: every clause of claim/criterion.md checked literally; no partial win claimed; full criterion met. It explicitly refused to rely on the 16:26:03Z read (Mozilla-prefixed User-Agent, cookie replay: RULES.md rule 5) and relied on its own plain curl of the archive (16:35:40Z, HTTP 200, same sha256, 510) plus one run of the fixed tool. Its confirmed_scope is copied above verbatim, with the object path given as it is in this package (object/).

## Downgrade checks (RUN.md step 7)
- Hedging panelist: no. Caveats are stated as non-blocking with reasons; all verdicts are plain pass: true.
- Reproduction mismatch: none. Both skeptics' own checkers, claim/checker.py, and the run's tools/check_cover.py (attempts/structured/output/selfbreak.txt) agree: 469 blocks, 0 uncovered, histogram 1:8148, 3:168, 5:84, 7:8, 9:28.
- Strictly better than the live table: yes, 469 < 510 (by 41) in every source: live coveringrepository.com plain cell (compliant reads 16:34:06Z, 16:34:13Z, 16:35:04Z, 16:35:40Z), dmgordo/LJCR GitHub and Zenodo LJCR v1.2. Panel fetches are minutes old (under 6 hours), so the gate did not fetch again.
- Table value obtained by evasion: the original 16:26:03Z search-form read WAS non-compliant (User-Agent beginning "Mozilla/5.0", ASP.NET session cookie replayed from GET to POST; RULES.md rule 5). It is voided and superseded, not relied on. The comparison rests on the compliant reads above: two single plain curl GETs by panelists (honest V3R1T4S User-Agent, no cookies, no retries, HTTP 200) and the fixed tool (V3R1T4S User-Agent, no cookie jar, no retries). All give 510. No challenged page was requested; the unreachable old LJCR host and the arXiv API were not retried.
- Claim folder edited after the panel: yes, packaging fixes only, required by CRITERION. data/live_coveringrepository_C38_6_3.txt and CLAIM.md now cite the compliant reads and state that the 16:26:03Z read was superseded because of rule 5; REPRODUCE.md's "cd claim/C38_6_3_469" was corrected to "cd claim" (the files sit directly in claim/, the same nit the C35 REPRODUCE skeptic reported). The object file (sha256 09d52bad...345b), checker and controls are unchanged.
- Stretched criterion or hidden quantifier: "the live LJCR value (https://dmgordon.org/covering-designs/)": that page has no per-cell values and points to the GitHub/Zenodo data (510); the old per-cell host failed (TLS), not retried. Accepted as for the C(20,6,3) and C(29,5,3) packages, and stated in the package. Not a downgrade.
- Scope wider than reproduced: no. confirmed_scope is CRITERION's sentence verbatim and covers only this cell.
- Sample presented as complete: no (exhaustive over all 8436 triples). Capped search used as exclusion: no (469 is MIP-optimal only within the PSL(2,7) 24+14 G-set; not claimed optimal). Probable prime: not applicable.
- Several objects bundled: no. One design, one cell. The corollary C(37,6,3) <= 468 is not part of this claim.
- Subsumed: no. No (38,6,3) entry in TROPHY_CASE.md or any repo PR; the only near-hit (#64, C(38,16,3)) is a different cell.

## Caveats carried into the package (honest, not blocking)
- The fixed tool's 16:34:13Z search-form read has a saved raw page and sha256 (be283df7...08bc) but the tool did not log its HTTP status; the HTTP 200 status is carried by the panelists' plain curl archive reads. The search-form read is a GET then a POST of the site's own form (what clicking Search does), so the single-request archive reads are the primary evidence.
- NOVELTY and CRITERION, at the orchestrator's instruction, also grepped/inspected the fixed lookup tool's request-building lines to judge rule-5 compliance (disclosed in their context lines); otherwise they saw only claim/.
- The arXiv check rests on arxiv.org's own search page (API unreachable, not retried); the 6-month GitHub/arXiv search was at search/title/abstract/README level.
- All three skeptics were subagents of the same assistant product: separate contexts working from claim/, but not independent of the product.
- Method is classical (orbit cover under PSL(2,7) on 24+14 points, exact MIP within that G-set). New only as a table entry. C(38,6,3) stays open (425..469).

Result: passes the gate. The status takes effect only if kit/check_run.py prints CHECK_RUN: PASS.
