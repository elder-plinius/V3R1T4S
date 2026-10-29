# Honesty gate: C(29,5,3) <= 399 (claim/, target covering-designs-record, full success criterion)
status: CONFIRMED_SOLUTION
confirmed_scope: The file claim/C29_5_3_399blocks.txt (sha256 816c287640bc50f50a87d27707aaae2c77ff99c1580a07336a594d3b94a56bbb) is a valid (29,5,3) covering design with 399 blocks, verified exhaustively over all 3654 triples, so C(29,5,3) <= 399, which is 14 fewer than the value 413 shown on 2026-10-19 by the dmgordo/LJCR GitHub data, the Zenodo LJCR v1.2 dataset and our own browser read (as submitters) of the live coveringrepository.com plain-coverings row.
gate_utc: 2026-10-19T23:54:39Z
gate_by: an executor session delegated by the workspace's main assistant session to carry out kit/RUN.md step 7 (not one of the three skeptics), after our own browser read (as submitters) of the live table was supplied in chat

## What I read
- reproduce.md, novelty.md, criterion.md in this folder. Each was written by a separate subagent that was given only its own copy of claim/ (each file has its own context: line). All three end with pass: true.
- REPRODUCE: wrote its own checker from the definition before opening claim/checker.py (quoted in its file). It found 399 distinct valid 5-subsets of 1..29, 3654/3654 triples covered (exhaustive), Schonheim 366 (also by hand), sha256 matches, no CR bytes, two runs gave identical output, no redundant block, and every negative control (its own four and the two packaged ones) fails with the same uncovered count under both checkers.
- NOVELTY: dmgordo/LJCR GitHub coverdata.json re-fetched (HTTP 200, 23:49:50Z, sha256 0984bb8b...7fef): 413. Zenodo concept 10779736 versions (HTTP 200, 23:49:51Z): v1.2 is still the newest; its value is 413. coveringrepository.com home and latest-improvements pages (HTTP 200, 23:49:49-51Z): no (29,5,3) row. Live per-cell value: our own browser read (as submitters), 413. arXiv (24 months), web, lottery-wheel, hobbyist repo, TROPHY_CASE.md and all 560 repo PRs: nothing at 413 or below.
- CRITERION: checked every clause of criterion.md literally (no partial win is claimed) and met the full criterion. Its weaker points (the unhashed browser read, the LJCR clause, the search-level arXiv grep) are argued in its file. Its confirmed_scope is copied above verbatim.

## Downgrade checks (RUN.md step 7)
- Hedging panelist: no. Every caveat is stated as non-blocking with reasons, and every verdict is a plain pass: true.
- Reproduction mismatch: none. The three skeptics' own checkers, claim/checker.py, reverify/verify3.py and tools/check_cover.py (run 2300 evaluator; reverify/ and tools/ were not shown to the panel) all agree: 399 blocks, 0 uncovered, histogram 1:3528, 2:56, 3:56, 13:14.
- Strictly better than the live table: yes. 399 < 413 in every source read: the live coveringrepository.com plain row (our own browser read as submitters, 2026-10-19T23:43Z), dmgordo/LJCR GitHub (re-fetched by the panel 23:49:50-23:50:05Z) and Zenodo LJCR v1.2 (file fetched 23:06:16Z; NOVELTY and CRITERION confirmed at 23:49-23:50Z that v1.2 is still the newest version). The panel's fetches are minutes old (well under 6 hours), so the gate did not fetch again.
- Stretched criterion or hidden quantifier: checked, no downgrade. "the live LJCR value (https://dmgordon.org/covering-designs/)": that page is a landing page with no per-cell values and links to the GitHub/Zenodo data (413); the old per-cell LJCR host gave a TLS error and was not retried. Accepted as meeting the clause, as for the earlier C(20,6,3) package, and stated in the package. "re-fetched at verification time" for coveringrepository.com: per-cell values are filled by JavaScript and per-cell pages are Cloudflare-challenged for machines; kit/RULES.md rule 5 makes a human browser check the sanctioned way, and we did it ourselves as submitters about 6 minutes before the panel.
- Scope wider than what was reproduced: no. confirmed_scope is CRITERION's sentence verbatim and covers only this one cell.
- Sample presented as complete: no (exhaustive over all 3654 triples). Capped search used as an exclusion: no (the CP-SAT orbit cover that produced the design was FEASIBLE/capped, and 399 is not claimed optimal in any family; the run's capped push to 398 found nothing and is not claimed). Probable prime: not applicable.
- Table value obtained by evasion: no. Every machine fetch was a single plain curl with an honest User-Agent; per-cell coveringrepository.com pages were never requested by the machine; the TLS error on the old LJCR host and the arXiv API timeout were not retried.
- Several objects bundled as one claim: no. One design, one cell.
- Subsumed: no. TROPHY_CASE.md and all repo PRs have no (29,5,3) entry; no neighbouring cell implies C(29,5,3) <= 413 (C(30,5,3) = 459).

## Caveats carried into the package (honest, not blocking)
- The live coveringrepository.com value (413) rests on our own browser read as submitters (2026-10-19 7:43 PM America/New_York = 23:43Z), pasted verbatim into claim/CLAIM.md. There is no saved page or hash.
- LJCR clause: met via the dmgordo/LJCR GitHub and Zenodo data (413). https://dmgordon.org/covering-designs/ has no per-cell values; the old per-cell page was unreachable (TLS error, not retried).
- The 6-month GitHub/arXiv search was at search/title/abstract/README level, not a full-text grep of every PDF or code file.
- All three skeptics were subagents of the same assistant product. They were separate contexts that each worked only from claim/, but they are not independent of the product, and they may have shared the parent's conversation history.
- The gate itself was written by a delegated executor session rather than by the run's original main session (which built the design and the claim folder); it read all three panel files itself.
- The method is classical: an orbit cover under PSL(2,7) acting on 14+14+1 points, found by a capped CP-SAT solve (FEASIBLE, not OPTIMAL). It is new only as a table entry. C(29,5,3) stays open (366..399).
- The design was found by run 2026-10-19-1303 (abandoned before reporting) and picked up, re-verified and panelled by run 2026-10-19-2300.

Result: passes the gate. The status takes effect only if kit/check_run.py prints CHECK_RUN: PASS.
