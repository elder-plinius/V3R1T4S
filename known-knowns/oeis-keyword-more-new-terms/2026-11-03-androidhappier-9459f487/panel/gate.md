# Honesty gate: oeis-keyword-more-new-terms / A326336(11)=70472 (run 2026-11-03-1625-capconn)

status: CONFIRMED_SOLUTION
confirmed_scope: For the live OEIS entry A326336 (keyword nonn,more; offset 0; DATA and the synthesized b-file end at a(10)=12270, with no links, extensions, or pending drafts; re-fetched 2026-11-03T20:29Z), the claim is A326336(11) = 70472. This is the number of set partitions of {1..11} whose capturing-block graph is connected, using any-pair capture x<z<t<y or z<x<y<t and counting empty and one-block partitions. The definition matches the entry and all three programs. n = 11 is the first missing index, A326336 is not excluded by the bank, the bank criterion is quoted verbatim, PREREG predates all attempt artifacts, and the only OEIS value hit (A070472, n^3 mod 7) is an unrelated A-number-digit coincidence. This covers the bank criterion's conditions only; whether the programs agree and reproduce all existing terms is left to the replication skeptic, since this check did not run them.

Gate session: run main-session gate (executor), separate from the three panel sessions; it wrote no panel vote.
Read: panel/reproduce.md (context: subagent (reproduce), pass: true), panel/novelty.md (context: subagent (novelty), pass: true),
panel/criterion.md (context: subagent (criterion), pass: true). 3/3 pass. The three files differ.
Gate time: 2026-11-03T20:41:30Z (15:41 EST).

## Live re-fetch at the gate (one plain curl GET each, User-Agent "V3R1T4S research"; gate/gate_fetchlog.txt)
- 2026-11-03T20:40:50Z 200 https://oeis.org/search?q=id:A326336&fmt=text -> gate2_A326336_text.txt c41509d2f024635586f257c056a31118c498ce8e0a53e6d58af8a1cda2a088ed
- 2026-11-03T20:40:50Z 200 https://oeis.org/A326336/b326336.txt -> gate2_b326336.txt c1111d16bc01d67edf407e7d6725b23dac3b3581d6838cbb16fe8fec5741e0c0
- 2026-11-03T20:40:50Z 200 https://oeis.org/history?seq=A326336 -> gate2_history.html 357c0ac6263034263da6be5603057e7d2a7aed10197aa7925bd25388c03d9bf0
- 2026-11-03T20:40:50Z 200 https://oeis.org/search?q=12270,70472&fmt=short -> gate2_valuesearch.html 985827398e2e57c393a052ec66f60b14c3abff48557a2eee78aa4999becee3b6
- 2026-11-03T20:40:50Z 200 https://oeis.org/search?q=70472&fmt=short -> gate2_bare70472.html fbd0d448432833e9b4b49a4fd222d100b91bd8661ac99b086704a64201d78b7c
- Entry: %I #6 Jun 28 2019 21:14:48; %K nonn,more; %O 0,5; %S ends 12270 (n=10). b-file last line "10 12270" (same sha256 as claim time, c1111d16...).
- History: newest revision #6 (Susanna Cuyler, Jun 28 2019, STATUS approved); #1-#5 Gus Wiseman 2019; no pending draft.
  "70472" occurs 0 times in entry text, b-file and history.
- Value search 12270,70472: "Sorry, but the terms do not match anything in the table."
- Bare value search 70472: 1 result, A070472 (a(n) = n^3 mod 7; A-number string match, terms only 0,1,6). Unrelated; disclosed.
- Panel fetches were at 2026-11-03T20:28-20:29Z, under 6 hours old; this gate fetch is an extra check, not a required one.

## PREREG timing (file mtimes, box clock America/New_York)
- PREREG.md "frozen 2026-11-03T16:25:52Z"; mtime 11:25:52 EST (= 16:25:52Z).
- Earliest attempts/ files: attempts/exact-eval-first/code/spstats.c, attempts/search-engineer/code/main.go and go.mod, 11:26:34 EST.
  claim/ files 11:28 EST. PREREG precedes every attempt, every computed value and the claim.
- PREREG: 'null_test: not needed because' (exact deterministic count). Thresholds (A and B reproduce DATA and agree on
  a(11); no OEIS value hit holding it as this count; no pending draft) are met per the panel and this gate.

## Independent recomputation at the gate
- gate/sp.c (written from the OEIS definition by the earlier gate session, before reading claim/programs), rerun now:
  mode 2 (capturing, BFS connectivity) n=0..11 -> 1,1,1,1,2,7,24,100,458,2279,12270,70472 (gate/A326336.gate.out).

## Downgrade audit (statuses only go down)
- Hedging panelist: none. All three end 'pass: true' without conditions. The criterion sentence's last clause ("whether the
  programs agree and reproduce all existing terms is left to the replication skeptic") states that seat's role, not a doubt;
  REPRODUCE verified it with its own checker (literal and fast modes, written before reading claim code) plus pA C, pB Go, pC Python.
- Reproduction mismatch: none. a(0..10) = DATA and a(11) = 70472 in all five computations plus gate/sp.c.
- Value not new: first missing index n=11; absent from entry, b-file, history, drafts; context search no match.
- Stretched criterion / hidden quantifier: no. Two independently written programs (C RGS + any-pair quadruple test + union-find
  vs Go bitmask generator + min/max-interval popcount test + BFS), both reproduce all 11 existing terms. Same contributor/session
  wrote both; the bank wording "different algorithms or languages" is met as written. Disclosed.
- Scope wider than reproduced: no. One cell n=11; sibling columns (A326245, A326246, A326249, A326335) printed only as cross-checks.
- Sample presented as complete / capped search as exclusion / probable prime as proof: n/a (exhaustive exact count over Bell(11)=678570 partitions).
- Table value by evasion: no. Plain GETs, HTTP 200.
- Several objects bundled: no.
- Bank exclusion: A326336 not in bank/targets.json, bank/proposed, known-knowns, TROPHY_CASE (criterion and novelty: 0 hits); not repdigit/repunit.
- Benchmark baseline: n/a.
- Own-team disclosure: the unpublished sibling package (nestconn, A326335(11)=61987, outbox id ending 17262752) prints the A326336
  column including 70472 at n=11 as a by-product. Same contributor's own computation, not external prior art (novelty skeptic agrees).
  Disclosed in the package; the sibling package was not modified.
- Scout literature note: OEISHeadroom's survey.json lists A326336 with DATA only, no new term (scout.md). Not prior art.

## Decision
Full success criterion met for one cell. status: CONFIRMED_SOLUTION, standing only if kit/check_run.py prints CHECK_RUN: PASS
for the package and the run; otherwise PROMISING.
