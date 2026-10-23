# Honesty gate: C(20,6,3) <= 70 (claim/, target covering-designs-record, full success criterion)
status: CONFIRMED_SOLUTION
confirmed_scope: The 70-block file C20_6_3_70blocks.txt (sha256 a6c6ddb8...4c6f) is an exhaustively verified (20,6,3) covering design, so C(20,6,3) <= 70, one block below the value 71 in the dmgordo/LJCR GitHub data (re-fetched 2026-10-17T15:01Z), the newest Zenodo LJCR release v1.2, and the live coveringrepository.com (v,k,t) row as hand-read by the operator at 2026-10-17T14:57Z, with no competing value of 70 or less found in a repo-level GitHub/arXiv search of the last 6 months.
gate_utc: 2026-10-17T15:06:11Z
gate_by: the workspace's main assistant session (not one of the three skeptics), on the human's explicit go-ahead in chat

## What I read
- reproduce.md, novelty.md, criterion.md in this folder. Each was written by a separate subagent that was given only its own copy of claim/ (each file has its own context: line). All three end with pass: true.
- REPRODUCE: its own checker found 70 distinct valid 6-subsets of 1..20, 1140/1140 triples covered (exhaustive), Schonheim 64, sha256 matches, negative controls fail as expected, no block is redundant, two runs gave identical output. claim/checker.py agrees.
- NOVELTY: dmgordo/LJCR GitHub re-fetched (HTTP 200, 15:00:48Z): 71. coveringrepository.com home and latest-improvements pages (HTTP 200, 15:00:49-51Z): no (20,6,3) improvement row. Live per-cell value: the operator's hand read, 71. Literature, lottery-wheel, hobbyist, TROPHY_CASE.md and PR searches found nothing at 70 or below.
- CRITERION: checked every clause of criterion.md literally (no partial win is claimed). It met the full criterion. The weaker points (the unhashed hand read, the LJCR clause) are argued in its file. Its confirmed_scope is copied above verbatim.

## Downgrade checks (RUN.md step 7)
- Hedging panelist: no. Every caveat is stated as non-blocking with reasons, and every verdict is a plain pass: true.
- Reproduction mismatch: none. The three skeptics' own checkers, claim/checker.py and the earlier independent rebuild (reverify/, not shown to the panel) all agree: 70 blocks, 0 uncovered.
- Strictly better than the live table: yes. 70 < 71 in every source read: the live coveringrepository.com row (operator hand read, 2026-10-17T14:57Z), dmgordo/LJCR GitHub (re-fetched 15:00-15:01Z) and Zenodo LJCR v1.2 (file fetched 14:51:27Z; CRITERION confirmed at 15:00-15:04Z that v1.2 is still the newest version). The panel's fetches are under 6 hours old, so the gate did not fetch again.
- Stretched criterion or hidden quantifier: checked, no downgrade. "the live LJCR value (https://dmgordon.org/covering-designs/)": that page is a landing page with no per-cell values. The old per-cell LJCR site is frozen and being retired (TLS error, not retried). The bank statement itself names dmgordo/LJCR GitHub as LJCR's permanent data location, and that file was re-fetched live (71, no commits since April). I accept this as meeting the clause and say so in the package. "re-fetched at verification time" for coveringrepository.com: the per-cell page is Cloudflare-challenged for machines. kit/RULES.md rule 5 makes a human's hand check the sanctioned way to clear a challenged table, and the operator did it about 4 minutes before the panel.
- Scope wider than what was reproduced: no. confirmed_scope is CRITERION's sentence verbatim and covers only this one cell.
- Sample presented as complete: no (exhaustive over all 1140 triples). Capped search used as an exclusion: no (nothing is excluded; the run's capped push to 69 is not claimed). Probable prime: not applicable.
- Table value obtained by evasion: no. Every machine fetch was a single plain request. Every 403 or challenge (Zenodo for NOVELTY, coveringrepository.com home for CRITERION, per-cell pages since 2026-10-14) was not retried or bypassed.
- Several objects bundled as one claim: no. One design, one cell.
- REPRODUCE order slip: REPRODUCE disclosed that it saw claim/checker.py (printed in the same command as CLAIM.md) before writing its own checker, which breaks the order in its role text. Decision: no downgrade. The kit's step 7 downgrade list does not include this. It is not a mismatch, a hedge or a sample, and the slip cannot lead to accepting a wrong object:
  - REPRODUCE's checker uses a different method (a per-triple containment test rather than building the set of covered triples). It computes Schonheim exactly and found no disagreement.
  - The coverage property is fully determined by the 70-line file. NOVELTY and CRITERION each wrote their own checker from the definition (CRITERION states "not checker.py") and got 1140/1140.
  - The pre-panel re-verification also used a checker written from scratch.
  - The slip is disclosed here and in the package.

## Caveats carried into the package (honest, not blocking)
- The live coveringrepository.com value (71) rests on the operator's hand read (2026-10-17 10:57 America/New_York = 14:57Z), pasted verbatim into claim/CLAIM.md. There is no saved page or hash, because the per-cell page is challenged for machines.
- LJCR clause: met via the dmgordo/LJCR GitHub data (71). The old per-cell LJCR page was unreachable (TLS error), and dmgordon.org/covering-designs/ has no per-cell values.
- NOVELTY's own Zenodo fetch got 403 (not retried). The Zenodo v1.2 value 71 comes from the 14:51:27Z fetch, and CRITERION confirmed that v1.2 is still the newest version.
- The 6-month GitHub search was at repo and README level, not code level (GitHub code search needs authentication).
- REPRODUCE saw claim/checker.py before writing its own (see above).
- All three skeptics were subagents of the same assistant product, and per their context: lines they shared the parent's conversation history. They were separate contexts that each worked only from claim/, but they are not independent of the product or of what the parent had said.
- The method is classical: an exact orbit cover under A5 (order 60) acting on PG(1,19). It is new only as a table entry. 70 is optimal only within that orbit family, and C(20,6,3) stays open (64..70).

Result: passes the gate. The status takes effect only if kit/check_run.py prints CHECK_RUN: PASS.

## Post-gate check_run note
- First package check (2026-10-17 ~15:08Z) failed on a never-publish false positive: a bare 4-letter entry matched inside the hobbyist repo name "thebrockchain". The status was temporarily PROMISING and the package was staged outside outbox/.
- The human decided at 2026-10-17T15:10Z to replace that bare entry with full-name forms. No panel, PREREG or object file was edited. Status restored to CONFIRMED_SOLUTION; it stands only if check_run prints CHECK_RUN: PASS.
