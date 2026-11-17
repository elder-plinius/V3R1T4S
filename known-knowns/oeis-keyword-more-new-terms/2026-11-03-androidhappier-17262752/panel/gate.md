# Honesty gate — oeis-keyword-more-new-terms / A326335(11)=61987 (run 2026-11-03-1625-nestconn)

status: CONFIRMED_SOLUTION
confirmed_scope: As of 2026-11-03 14:12 EST, A326335 carries keyword 'more', is not excluded by the V3R1T4S bank, and has DATA and b-file ending at a(10)=10696 (so n=11 is the first missing index), while the claimed definition and all three programs' nesting tests match the entry's consecutive-pair definition, PREREG.md predates every attempts/ file, and 61987 appears in neither the entry, its history, nor any OEIS search hit for this sequence; this vote does not verify that 61987 is the correct count.

Gate session: run main-session gate (executor), separate from the three panel sessions; did not write any panel vote.
Read: panel/reproduce.md (context: subagent (reproduce), pass: true), panel/novelty.md (context: subagent (novelty), pass: true),
panel/criterion.md (context: subagent (criterion), pass: true). 3/3 pass.
Gate time: 2026-11-03T19:17:00Z (14:17 EST).

## Live re-fetch at the gate (one plain curl GET each, User-Agent "V3R1T4S research"; gate/gate_fetchlog.txt)
- 2026-11-03T19:16:29Z 200 https://oeis.org/search?q=id:A326335&fmt=text -> gate_A326335_text.txt 13a9a46a27dd80a6a4eca780f83bd00e03b73f6448b4f9e41035f8fbabb477bb
- 2026-11-03T19:16:29Z 200 https://oeis.org/A326335/b326335.txt -> gate_b326335.txt 22e6ca0a969c252d87b19b0b6ec2f24567a3ebcc2f186dfedc62f9989eb987fb
- 2026-11-03T19:16:29Z 200 https://oeis.org/history?seq=A326335 -> gate_history.html 0c2ebe1e29055d32834c2d719f31d39c5c98ceea40eecc76867302e5c2a0b96e
- 2026-11-03T19:16:29Z 200 https://oeis.org/search?q=10696,61987&fmt=short -> gate_valuesearch.html 02ceb0695fd680171807a3c49810d6044849988492ebe1bde2d7f264274579bc
- 2026-11-03T19:16:29Z 200 https://oeis.org/search?q=61987&fmt=short -> gate_bare61987.html 9057348cf2e5c0d1f9e7d17e8a6c4b94d6f1ff48922fa90b8e6b3474b34624fd
- Entry: %I #6 Jun 28 2019; %K nonn,more; %O 0,5; DATA ends 10696 (n=10). b-file last line "10 10696" (same sha256 as claim time, 22e6ca0a...).
- History: newest revision #6 (Susanna Cuyler, Jun 28 2019, approved); #1-#5 Gus Wiseman 2019; no pending draft. "61987" occurs 0 times in entry text, b-file and history.
- Value search 10696,61987: "Sorry, but the terms do not match anything in the table."
- Bare value search 61987: 5 results, A209399 (subsets of {1..n} with two elements differing by 3; 61987 is its own term), A061987, A220933, A243426, A302318.
  None is A326335 or records 61987 as a term of it. Judged a coincidence, as by the novelty skeptic; disclosed in the package.
- Panel fetches were at about 19:12-19:13Z, under 6 hours old; this gate fetch is an extra check, not a required one.

## PREREG timing (file mtimes, box clock America/New_York; UTC stamps in files)
- PREREG.md "frozen 2026-11-03T16:25:52Z"; mtime 11:25:52 EST (= 16:25:52Z).
- Earliest attempts/ files: attempts/exact-eval-first/code/spstats.c, attempts/search-engineer/code/main.go and go.mod, 11:26:33 EST.
  claim/ files 11:28 EST. PREREG precedes every attempt, every computed value and the claim.
- PREREG has 'null_test: not needed because' (exact deterministic count). Its thresholds (A and B reproduce DATA and agree on
  a(11); no OEIS value hit holding it as this count; no pending draft) are met per the panel and this gate.

## Independent recomputation at the gate (earlier gate session, before panel)
- gate/sp.c (sha256 14b81d1a3f044682...), written from the OEIS definition: ./sp 1 0 11 -> 1,1,1,1,2,6,21,86,394,1974,10696,61987.

## Downgrade audit (statuses only go down)
- Hedging panelist: none. All three end 'pass: true' without conditions. The criterion sentence ends "this vote does not verify
  that 61987 is the correct count": a statement of that seat's role (correctness belongs to REPRODUCE), not a doubt about the
  criterion. REPRODUCE verified the count with its own checker written first from the definition, plus all three claim programs.
  The gate keeps the sentence exactly, as the kit requires; it is narrower, not wider, than the evidence.
- Reproduction mismatch: none. Reproduce skeptic's own checker plus pA_c, pB_go, pC_py all give a(0..10) = DATA and a(11)=61987.
- Value not new: first missing index; value absent from entry, b-file, history, drafts; context search no match.
- Stretched criterion / hidden quantifier: no. Two independently written programs (C RGS + quadruple tests + union-find vs Go
  bitmask generator + gap/popcount test + BFS), both reproduce all 11 existing terms. Same contributor/session wrote both
  (criterion caveat on identical mtimes); the bank wording "different algorithms or languages" is met as written. Disclosed.
- Scope wider than reproduced: no. One cell n=11; sibling columns (A326245, A326246, A326249, A326336) printed as cross-checks
  only, not claimed.
- Sample presented as complete / capped search as exclusion / probable prime as proof: n/a (exhaustive exact count, Bell(11)=678570 partitions).
- Table value by evasion: no. Plain GETs, HTTP 200.
- Several objects bundled: no.
- Bank exclusion: A326335 not in bank/targets.json, bank/proposed, known-knowns, TROPHY_CASE (criterion and novelty: 0 hits); not repdigit/repunit.
- Benchmark baseline: n/a.

## Decision
Full success criterion met for one cell. status: CONFIRMED_SOLUTION, standing only if kit/check_run.py prints CHECK_RUN: PASS
for the package and the run; otherwise PROMISING.
