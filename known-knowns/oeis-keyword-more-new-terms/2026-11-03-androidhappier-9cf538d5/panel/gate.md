# Honesty gate — oeis-keyword-more-new-terms / A325786(21)=93725 (run 2026-11-03-1641-necklcomp)

status: CONFIRMED_SOLUTION
confirmed_scope: A325786(21) equals 93725 as the next term (first index beyond DATA and b-file) of OEIS A325786, counting complete necklace compositions of 21 per the entry's name and Mathematica code.

Gate session: run main-session gate (executor), separate from the three panel sessions; did not write any panel vote.
Read: panel/reproduce.md (context: subagent (reproduce), pass: true), panel/novelty.md (context: subagent (novelty), pass: true),
panel/criterion.md (context: subagent (criterion), pass: true). 3/3 pass.
Gate time: 2026-11-03T18:11:27Z (13:11 EST).

## Live re-fetch at the gate (one plain curl GET each, User-Agent "V3R1T4S research"; gate/gate_fetchlog.txt)
- 2026-11-03T18:11:27Z 200 https://oeis.org/search?q=id:A325786&fmt=text -> gate_A325786_text.txt 23b2ca2c4e2eebb6f9af01f2b217c1e74766b5b113b421031c07db9acd4d0b3a
- 2026-11-03T18:11:27Z 200 https://oeis.org/A325786/b325786.txt -> gate_b325786.txt 377da0f78ea5b996e8dddef912b383a2a7582ec240c1234c29b2a17eb03f3ba8
- 2026-11-03T18:11:27Z 200 https://oeis.org/history?seq=A325786 -> gate_history.html 103297d4dc76340d1eca19017d4d174350ac2ed70fe6900585a70bc27816568a
- 2026-11-03T18:11:27Z 200 https://oeis.org/search?q=47049,93725&fmt=short -> gate_valuesearch.html 4140317dcbc069d115d8372ae6b02cff0ab287ef60fb3b57da74abe29de6f88d
- Entry: %K nonn,more; %O 1,3; DATA ends %T 47049 (n=20). b-file last line "20 47049" (same sha256 as claim time, 377da0f7...).
- History: newest revision #6 (Susanna Cuyler, May 22 2019, approved); no pending draft. "93725" occurs 0 times in entry text, b-file and history.
- Value search 47049,93725: "Sorry, but the terms do not match anything in the table."
- Panel fetches were at about 18:08-18:10Z, under 6 hours old; this gate fetch is an extra check, not a required one.

## PREREG timing (file mtimes, box clock America/New_York; UTC stamps in files)
- PREREG.md "frozen 2026-11-03T16:42:32Z"; mtime 11:42:32 EST (= 16:42:32Z).
- Earliest attempts/ file: attempts/exact-eval-first/code/neck.c and search-engineer/code/go.mod, 11:43:49 EST.
- claim/ files 11:54 EST. PREREG precedes every attempt, every computed value and the claim.
- PREREG has 'null_test: not needed because' (exact deterministic count, no statistical inference). Its thresholds
  (A and B reproduce DATA and agree on a(21); no OEIS value/context hit; no pending draft) are met per the panel and this gate.

## Downgrade audit (statuses only go down)
- Hedging panelist: none. All three end 'pass: true' without conditions. Criterion's "minor note" (claim-time fetch 13 min
  before CLAIM.md) is resolved by its own 13:09 EST re-fetch and this gate's re-fetch; not a hedge.
- Reproduction mismatch: none. Reproduce skeptic's own bitmask checker plus pA_c, pB_go, pC_py all give a(1..20) = DATA and a(21)=93725, byte-identical.
- Value not new: first missing index; value absent from entry, b-file, history, drafts. Bare value search "93725" hits A332835
  (an unrelated sequence that has 93725 as its own term) and A093725 (A-number string). The novelty skeptic judged this a
  coincidence, not a record of the term in A325786; the gate agrees (the criterion bars the term appearing as this
  sequence's value, and the context search 25233,47049,93725 / 47049,93725 has no match). Disclosed in the package.
- Stretched criterion / hidden quantifier: no. Two independently written programs (C recursive compositions + rotation
  test vs Go cut-point subsets + difference cover with 1/period weighting), both reproduce all 20 existing terms.
- Scope wider than reproduced: no. One cell n=21; by-products n=22..30 not claimed.
- Sample presented as complete / capped search as exclusion / probable prime as proof: n/a (exhaustive exact count).
- Table value by evasion: no. Plain GETs, HTTP 200.
- Several objects bundled: no.
- Bank exclusion: A325786 not named in bank/targets.json or bank/proposed (criterion panel rg: 0 hits); not a repdigit/repunit sequence.
- Benchmark baseline: n/a.
- Note (not a trigger): panel file mtimes 13:09:31-13:10:20 EST, while criterion.md states a session window to 13:15 EST;
  the stated window end is later than the file's write time. Recorded, no effect on the verdict.

## Decision
Full success criterion met for one cell. status: CONFIRMED_SOLUTION, standing only if kit/check_run.py prints CHECK_RUN: PASS
for the package and the run; otherwise PROMISING.
