# Honesty gate: oeis-keyword-more-new-terms / A316471(21)=482706 (run 2026-11-03-2000-locdisj)

status: CONFIRMED_SOLUTION
confirmed_scope: A316471 (bank-eligible, keyword more, live 2026-11-03T21:17Z) has DATA/b-file ending at a(20)=214490, and two independent programs matching the entry's definition (C and Go, rebuilt by me) both reproduce a(1..20) and give a(21)=482706, a value absent from OEIS search, the entry and its history; by-products a(22..26) are not covered.

Gate session: run main-session gate (executor), separate from the three panel sessions; it wrote no panel vote.
Read: panel/reproduce.md (context: subagent (reproduce), pass: true), panel/novelty.md (context: subagent (novelty), pass: true),
panel/criterion.md (context: subagent (criterion), pass: true). 3/3 pass. The three files differ.
Gate time: 2026-11-03T21:30:07Z (16:30 EST).

## Live re-fetch at the gate (one plain curl GET each, User-Agent "V3R1T4S research (plain request)"; gate/gate_fetchlog.txt)
- 2026-11-03T21:29:31Z 200 b425e36d75f6f8f075d40e40597e572b05e5bd77d77c3c405074d7292f075a87 https://oeis.org/search?q=id:A316471&fmt=text -> gate_A316471_text.txt
- 2026-11-03T21:29:32Z 200 da35dd33b0431ceb71f73d6b1ad7ab3efad7dccb999314daf2deeb205227c4f5 https://oeis.org/A316471/b316471.txt -> gate_b316471.txt
- 2026-11-03T21:29:33Z 200 403a5aa12f521ec8d8ec99f1c7332cc114a33a522922f8e15eb17473f67e07eb https://oeis.org/history?seq=A316471 -> gate_history.html
- 2026-11-03T21:29:34Z 200 8a2d3f20a02f6239d9813e01286e40adc7738602bcbabfba258d5918fe093edb https://oeis.org/search?q=214490,482706&fmt=text -> gate_valuesearch.txt
- 2026-11-03T21:29:35Z 200 2587c2336704d3a3d81f88fde3b1654dbda23ff33e58cf13150c0d1a16540bc4 https://oeis.org/search?q=482706&fmt=text -> gate_bare482706.txt
- Entry: %I #6 Jul 05 2018 02:30:18; %K nonn,more; %O 1,4; DATA ends 214490 (n=20). Entry text and b-file have the same sha256 as at claim time (b425e36d..., da35dd33...); b-file last line "20 214490".
- History: newest revision #6 (Susanna Cuyler, Jul 05 2018, STATUS proposed -> approved); #1-#5 Gus Wiseman, Jul 04 2018; no pending draft. "482706" occurs 0 times in entry text, b-file and history.
- Value search 214490,482706: "No results." Bare value search 482706: "No results." (same sha256 as claim time).
- Panel fetches were at 2026-11-03T21:17Z, under 6 hours old; this gate fetch is an extra check, not a required one.

## PREREG timing (file mtimes, box clock America/New_York)
- PREREG.md "frozen 2026-11-03T20:01:18Z"; mtime 15:01:18 EST (= 20:01:18Z).
- Earliest attempts/ file: attempts/exact-eval-first/code/progA.c, 15:01:52 EST; all outputs and claim/ later. PREREG precedes every attempt and every computed value.
- PREREG: 'null_test: not needed because' (exact deterministic count). Thresholds (A and B reproduce a(1..20) and agree on a(21); negative fixture gives A004111 in both; no OEIS value hit; pre-claim re-fetch shows DATA ending at a(20) and no draft) are met per the panel and this gate.

## Recomputation at the gate
- panel/reproduce_check.py (the REPRODUCE skeptic's own checker, written from the definition) rerun by the gate: `python3 panel/reproduce_check.py 21` -> a(1..20) = DATA, "21 482706", 0.65 s.

## Downgrade audit (statuses only go down)
- Hedging panelist: none. All three end 'pass: true' without conditions. Novelty states it did not verify the count, and criterion states web/literature novelty is the novelty seat's job: statements of role, each covered by another seat (REPRODUCE verified the count with its own checker plus programs A, B, C; NOVELTY searched OEIS, siblings incl. the Feb 2026 A316473 extension by Robert P. P. McKone, and the repo/PRs).
- Reproduction mismatch: none. Skeptic's checker, Program A (C) and Program B (Go) give a(1..20) = DATA and a(21) = 482706; Program C (Python/sympy, Matula-Goebel) agrees for n <= 11 only (an oracle, not one of the two claim programs).
- Value not new: n = 21 is the first missing index; value absent from entry, b-file, history, drafts and value searches.
- Stretched criterion / hidden quantifier: no. Two independently written programs (C canonical-id backtracking with a mark array vs Go literal partition x tuple filter), both reproduce all 20 existing terms. Same contributor and run wrote both; the bank wording "different algorithms or languages" is met as written. Disclosed in the package.
- Scope wider than reproduced: no. One cell n = 21; by-products a(22..26) printed by Program A are not covered and not claimed.
- Sample presented as complete / capped search as exclusion / probable prime as proof: n/a (exhaustive exact enumeration).
- Table value by evasion: no. Plain GETs, HTTP 200.
- Several objects bundled: no.
- Bank exclusion: A316471 not named in bank/targets.json or bank/proposed (criterion and novelty: 0 hits); not a repdigit/repunit sequence.
- Benchmark baseline: n/a.

## Decision
Full success criterion met for one cell. status: CONFIRMED_SOLUTION, standing only if kit/check_run.py prints CHECK_RUN: PASS
for the package and the run; otherwise PROMISING.
