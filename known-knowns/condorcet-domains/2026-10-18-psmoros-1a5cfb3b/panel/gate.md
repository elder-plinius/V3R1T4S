# Honesty gate (kit RUN.md step 7), run folder 2026-10-18-0238

written by the main session at 2026-10-18T03:57:09Z (Opus 5.5, model claude-opus-5-5), after reading all three panel files in full.

status: CONFIRMED_SOLUTION
confirmed_scope: The three files object/n21_orders.txt.xz.part_aa, part_ab and part_ac, joined in that order and xz-decompressed (sha256 0cb0dd880cc7a0ad640634f505b7520bd2a5c0bb95fd7a2ce4d56fbeb8578e27), list 7467760 distinct linear orders on the alternatives 1..21 whose restriction to each of the 1330 triples satisfies a never condition, so they form a Condorcet domain on 21 alternatives (in the odd-profile sense of arXiv:2601.07336v1, Section 2) strictly larger than 6674931, the n = 21 entry of Table 4 of arXiv:2601.07336v1, the only version of that paper at the human's hand check of 2026-10-18T00:58Z.

## Panel (three fresh contexts, Agent tool, model opus each)

- REPRODUCE: pass: true. Its own strict C checker was written before it read the author's code and was tested on its own Fishburn domains (n = 3..9, sizes 4..488) and on 6 negatives. On the object it found 7467760 distinct orders, 1330/1330 triples passing, no cyclic triple, and deterministic output over two runs. Its own DFS from the assignment reproduced the list byte for byte, and all five sha256 values match.
- NOVELTY: pass: true. It made no request to arxiv.org or any mirror (stopped host). It read the status source as the scout's honest HTTP 200 copy of v1 (2026-10-17T22:25:36Z) plus the human's hand check of the abstract page (2026-10-18T00:58Z, v1 only). It checked TROPHY_CASE.md, all 363 repo PRs, repo code, the 2025-2026 literature and the CDL repository: nothing at or above 7467760 for n = 21.
- CRITERION: pass: true, with the confirmed_scope above. It read every clause literally. It checked the odd-profile meaning on 3 alternatives (63/63 agree) and the rule 3 non-subsumption: all 21 restrictions to 20 alternatives exceed the published 3155366. It asked for the record of PREREG rule 2's re-check. The record is data/prs_search_preclaim.txt: a gh search of open and closed PRs for condorcet, "Condorcet domain", "linear orders", "never condition", "majority rule" and 2601.07336 at 2026-10-18T03:40:39Z found no hits, and TROPHY_CASE.md has 0 Condorcet matches. A WebSearch at about 03:41Z found nothing newer than arXiv:2601.07336. The NOVELTY skeptic's own sweep (03:42Z-03:53Z) is also on record. arXiv itself could only be covered by the human's hand check.

## Gate checks

- No hedging panelist. The NOVELTY and CRITERION files state their limits: the Table 4 cells come from the scout's copy, and the scope is tied to Table 4. Both give clear verdicts. The scope sentence is no wider than what was reproduced.
- No reproduction mismatch. The main session's own checker (code/main_check/mcheck.c, cross-checked against code/cdcheck.py on 7 small domains) printed PASS on the joined, decompressed parts: 7467760 distinct, 1330 triples, 0 violations, at 2026-10-18T03:40:32Z (code/main_check/verify_n21_carrier_0238.txt). The ledger-audit lens's independent strict checker and DP counter, and the vcycle lens's checker, also passed this list.
- The value is strictly better than the table: 7467760 > 6674931 (+11.8777 %), not a tie.
- Table fetch age: the scout's fetch was at 2026-10-17T22:25:36Z, under 6 hours before this gate, and the human's hand check was at 00:58Z. A new fetch is impossible (arxiv.org is stopped after HTTP 429); no evasion was used, and every fetch used the run's honest helper.
- No capped search used as an exclusion, no sample presented as complete, one object and one n (rule 4: n = 21 has the largest verified relative gain among n <= 22; n = 22 is next at +10.20 %).
- This folder's claim is new and separate from runs/2026-10-17-2220. That folder's gate (PROMISING, for the smaller 7402109-order object, panelled before the human's hand check existed) is not changed.
- A CONFIRMED status stands only if python3 repo/kit/check_run.py prints CHECK_RUN: PASS; see REPORT.md.
