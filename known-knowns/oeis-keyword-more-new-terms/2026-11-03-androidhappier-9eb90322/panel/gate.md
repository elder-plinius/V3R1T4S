# Honesty gate: oeis-keyword-more-new-terms / A155520 row 6, first missing term A(6,1) = 6 (run 2026-11-03-2146-drawings)

status: CONFIRMED_SOLUTION
confirmed_scope: Row 6 of A155520 for k = 1..42 is 6,2,6,9,11,4,4,4,2,15,8,2,0,6,12,0,0,1,4,6,0,4,4,0,8,4,0,0,0,4,0,0,0,1,2,0,0,2,0,0,0,1; first missing term A(6,1) (flattened index 22) = 6.

Gate session: executor main-session gate, separate from the three panel sessions; it wrote no panel vote.
Read: panel/reproduce.md (context: subagent (reproduce), pass: true), panel/novelty.md (context: subagent (novelty), pass: true),
panel/criterion.md (context: subagent (criterion), pass: true, carries the scoped statement and "confirmed_scope: CONFIRMED -- the WHOLE
scoped statement, no part downgraded; not CONFIRMED_PARTIAL"). 3/3 pass. The three files differ.
The confirmed_scope line above is the criterion panelist's scoped-statement sentence, copied exactly.
Gate time: 2026-11-03T21:55Z (16:55 EST).

## Live re-fetch at the gate (one plain curl GET each, User-Agent "V3R1T4S research", no retries; gate/gate_fetchlog.txt)
- 2026-11-03T21:54:58Z 200 https://oeis.org/search?q=id:A155520&fmt=text -> gate/gate_A155520_text.txt 09faabfe06ade0fe0cdde54d510aaedf6d165249b505098353e8ea023ad4146d (byte-identical to the scout fetch 21:46:40Z; the pre-claim fmt=text fetch had failed HTTP 000, now recovered)
- 2026-11-03T21:54:58Z 200 https://oeis.org/A155520 -> gate/gate_A155520.html ad9d92c13f05315625c0a08a7099dadb53a5cffbd510ef45f55084e22f32a156 (dynamic page bytes; content same)
- 2026-11-03T21:54:58Z 200 https://oeis.org/A155520/b155520.txt -> gate/gate_b155520.txt 255b579936bb85108c7d7ed9ac42810e17d9826e957b574c386a584c7c44992d (identical to claim time; synthesized, ends "21 2")
- 2026-11-03T21:54:58Z 200 https://oeis.org/history?seq=A155520 -> gate/gate_history.html 8c453d0dd0544ce00bb38648c98ea36e31f91234a20b8aec95101a7a17ec933f (tag-stripped text differs from the pre-claim fetch only in the "Last modified" footer and a Cloudflare script token)
- 2026-11-03T21:54:58Z 200 https://oeis.org/search?q=6,2,6,9,11,4,4,4,2,15,8,2&fmt=text -> gate/gate_vs_row6_head.txt b3abb462... "No results." (identical to claim time)
- 2026-11-03T21:54:58Z 200 https://oeis.org/search?q=1,2,2,6,2,6,9,11&fmt=text -> gate/gate_vs_datatail_row6head.txt 0d85230e... "No results." (identical)
- 2026-11-03T21:54:58Z 200 https://oeis.org/search?q=6,2,6,9,11,4&fmt=text -> gate/gate_vs_row6_short.txt 28d10fd7... "No results." (identical)
- Entry: %I #12 Sep 24 2025; %K nonn,tabf,more; %O 1,2; DATA 1,2,3,2,4,2,6,1,1,5,2,6,9,1,4,4,4,2,1,2,2 (21 terms = rows 1..5);
  %E only "Keyword tabf added by Michel Marcus, Apr 09 2013"; no row-6 value in %C/%F/%H/%e.
- History: newest revision #12 (Andrei Zabolotskii, Sep 24 2025, approved); no pending/proposed draft above it. "6,2,6,9,11" /
  "6, 2, 6, 9" / "1787" occur 0 times in entry text, entry page and history.

## PREREG timing (file mtimes, box clock America/New_York)
- PREREG.md "frozen: 2026-11-03T21:47:04Z"; mtime 16:47:04 EST (= 21:47:04Z).
- Earliest program: attempts/exact-eval-first/code/progA.py 16:47:17 EST; progB.c 16:47:36; fixtures.py 16:47:49; claim/ 16:48:18+.
  Only data/ fetches (16:46:40 EST) precede PREREG. PREREG precedes every program, computed value and the claim.
- PREREG thresholds (A and B reproduce rows 1..5 = DATA, row sum 132, weighted sum 1787 = A014307(6), agree on full row 6;
  negative fixture differs from DATA; value searches no hit; no pending draft; zero convention disclosed): all met.
- null_test: not needed because (exact deterministic count).

## Independent recomputation at the gate
- Fresh copy of claim/ in a temp folder: python3 programs/pA_py/progA.py 8 -> gate/pA_8.gate.out; gcc -O2 progB.c; ./pB 8 -> gate/pB_8.gate.out.
  The two are byte-identical and identical to the stored progA_8.out; row 6 == claim/object/ROW6.txt; table/fixtures.py on both:
  rows 1..5 == DATA, %e cases (UDUUDD 2, UUDDUD 2, UUUDDD/UUDUDD/UDUDUD 1) reproduced, negative deletion-sequence fixture differs from DATA.

## Downgrade audit (statuses only go down)
- Hedging panelist: none. All three end 'pass: true' without conditions. CRITERION explicitly states the WHOLE scoped statement is confirmed.
- Reproduction mismatch: none. Programs A, B, the reproduce skeptic's nested-tuple checker, the criterion skeptic's third checker and this gate agree on rows 1..6 (A and B through row 8).
- Value not new: first missing flattened index 22 = A(6,1); absent from DATA, b-file, comments/links/extensions, history and drafts; three value searches "No results."; Klazar 1997 + Addendum give only aggregate totals (novelty panel).
- Stretched criterion / hidden quantifier: no. Criterion asks for "at least one new value at the first index"; A(6,1) = 6 is that value and the rest of row 6 continues from it. Two independently written programs (Python backward deletion vs C forward insertion, different encodings), both reproduce all 21 DATA terms.
- Zero convention: row 6 has interior zeros that rows 1..5 do not exhibit. A(6,1) = 6 is convention-free; the (k, A(6,k)) pairs are convention-free statements; the zero-kept listing follows the entry's %N (A(n,k) for each k). Disclosed in CLAIM.md and accepted by CRITERION as a disclosure, not a scope cut. Not a downgrade.
- Scope wider than reproduced: no. The scope is row 6 only (k = 1..42), reproduced by 4 independent codes; rows 7..8 are by-products, not claimed.
- Sample as complete / capped search / probable prime: n/a (exhaustive count over all 132 trees).
- Table value by evasion: no. Plain GETs, HTTP 200.
- Several objects bundled: no. One object (row 6 of one triangle, one target cell starting at index 22).
- Bank exclusion: "155520" absent from repo/bank/targets.json and bank/proposed; not in TROPHY_CASE.md or outbox/; not repdigit/repunit.
- Pattern caveat (novelty): A(n,1) = n is guessable from DATA, but it is computed here, not guessed; disclosed.
- Entry %e typo (second UUDDUD drawing printed equal to the first): noted by panel; count 2 matches; does not affect the reading.
- Benchmark baseline: n/a.

## Decision
Full success criterion met for the whole scoped statement. status: CONFIRMED_SOLUTION, standing only if kit/check_run.py prints
CHECK_RUN: PASS for the package and the run; otherwise PROMISING.
