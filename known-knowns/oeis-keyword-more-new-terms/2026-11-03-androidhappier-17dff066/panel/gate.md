# Honesty gate: oeis-keyword-more-new-terms / A331783(21)=10950456 (run 2026-11-03-2004-ldsemi)

status: CONFIRMED_SOLUTION
confirmed_scope: For the live OEIS entry A331783 (locally disjoint rooted semi-identity trees with n unlabeled vertices; keyword nonn,more; offset 1; DATA and the synthesized b-file end at a(20) = 4242226, with no links, extensions, or pending drafts; re-fetched 2026-11-03T21:22Z), the claim is A331783(21) = 10950456, using the entry's own definition (name, comments and Mathematica disjunsQ code: one branch, or non-leaf branches pairwise distinct and every two branches equal or with empty intersection, applied recursively). n = 21 is the first missing index, A331783 is not excluded by the bank, the bank criterion is quoted verbatim, PREREG predates all programs, two independently written claim programs (C id-set backtracking, Go literal partition x tuple transcription) plus the reproduce skeptic's own C checker and the criterion skeptic's literal Python transcription all reproduce a(1..20) = DATA and give 10950456, and OEIS value searches for 10950456 and 4242226,10950456 return no results. By-products a(22..23) are out of scope.

Gate session: executor main-session gate, separate from the three panel sessions; it wrote no panel vote.
Read: panel/reproduce.md (context: subagent (reproduce), pass: true), panel/novelty.md (context: subagent (novelty), pass: true),
panel/criterion.md (context: subagent (criterion), pass: true, carries confirmed_scope). 3/3 pass. The three files differ.
Gate time: 2026-11-03T21:23Z (16:23 EST).

## Live re-fetch at the gate (one plain curl GET each, User-Agent "V3R1T4S research"; gate/gate_fetchlog.txt)
- 2026-11-03T21:22:21Z 200 https://oeis.org/search?q=id:A331783&fmt=text -> gate_A331783_text.txt b9aa4fc4fd4e573dbd6493aa0c5f1b5af30ba2af30cb7e3efd935792c381eb6c (identical to claim time)
- 2026-11-03T21:22:21Z 200 https://oeis.org/A331783/b331783.txt -> gate_b331783.txt bd1ee9692bce2e1bd74db2a43f918454dee55914378836357e556ce029e860f6 (identical to claim time)
- 2026-11-03T21:22:21Z 200 https://oeis.org/history?seq=A331783 -> gate_history.html 9c54da5d2a533d339ce26d9cca53cbafd366ad55493905e8debb3fb65267da36
- 2026-11-03T21:22:21Z 200 https://oeis.org/search?q=4242226,10950456&fmt=text -> gate_vs_ctx.txt d91f3da127d0e3e57a5e5a2aa0624b424e6e98c4a61a4aae51891790a9406c79 ("No results.", identical to claim time)
- 2026-11-03T21:22:21Z 200 https://oeis.org/search?q=10950456&fmt=text -> gate_vs_bare.txt 1903127e6f6c3f4a4c14fad8ea180c2136f0f0b8d0555104f84ced16c7bddaa0 ("No results.", identical to claim time)
- Entry: %I #6 Feb 02 2020 09:03:41; %K nonn,more; %O 1,3; DATA ends 4242226 (n = 20). b-file last line "20 4242226".
- History: newest revision #6 (Susanna Cuyler, Feb 02 2020, proposed -> approved); #1-#5 Gus Wiseman, Jan 2020; the "editing"/"proposed"
  strings are historical status changes of #3/#5/#6; no pending draft. "10950456" occurs 0 times in entry text, b-file and history.
  (History page hash differs from claim time; content checked: same revisions #1-#6, no new entry; dynamic page bytes.)

## PREREG timing (file mtimes, box clock America/New_York)
- PREREG.md "frozen 2026-11-03T20:05:19Z"; mtime 15:05:19 EST (= 20:05:19Z).
- Earliest program: attempts/exact-eval-first/code/progA.c 15:05:36 EST; Go main.go 15:06:03; Python progC.py 15:06:27; claim/ 15:07:38.
  Only data/ fetches (15:04:59-15:05:00) precede PREREG. PREREG precedes every program, computed value and the claim.
- PREREG: 'null_test: not needed because' (exact deterministic count). Thresholds (A and B reproduce a(1..20) and agree on a(21);
  negative fixture differs from DATA; no OEIS value hit; no pending draft) are met per the panel and this gate.

## Independent recomputation at the gate
- Fresh copy of claim/ in a scratch folder: gcc -O2 progA.c; ./pA 21 -> a(1..20) = DATA, a(21) = 10950456 (gate/pA_21.gate.out);
  go build; ./pB 21 -> same (gate/pB_21.gate.out); ./pA 16 nodisj -> a(16) = 177604 (A306200-type, != DATA 99880).

## Downgrade audit (statuses only go down)
- Hedging panelist: none. All three end 'pass: true' without conditions. REPRODUCE notes its own checker shares Program A's
  algorithm family (independent code, not independent algorithm); Program B (Go literal transcription) and the criterion
  skeptic's literal Python lit.py are the algorithmically different confirmations. Disclosed, not a downgrade.
- Reproduction mismatch: none. a(1..20) = DATA and a(21) = 10950456 in pA, pB, the reproduce checker, criterion lit.py, and this gate.
- Value not new: first missing index n = 21; absent from entry, b-file, history, drafts; both value searches "No results."
- Stretched criterion / hidden quantifier: no. Two independently written programs in different languages and algorithms, both
  reproduce all 20 existing terms. Same contributor/session wrote both; disclosed.
- Scope wider than reproduced: no. One cell n = 21; a(22..23) by-products not claimed.
- Sample as complete / capped search / probable prime: n/a (exact exhaustive count).
- Table value by evasion: no. Plain GETs, HTTP 200.
- Several objects bundled: no.
- Bank exclusion: "331783" in repo/bank/targets.json: 0 hits; none in TROPHY_CASE.md / known-knowns; not repdigit/repunit.
- Benchmark baseline: n/a.
- Own-team disclosure: sibling run 2026-11-03-2000-locdisj (A316471, identity version) is a different cell; grep for 10950456 in
  that run and in outbox/: 0 hits. Not modified.
- Sibling A316473 (non-semi-identity version, extended Feb 2026 by R. P. P. McKone) holds different values; novelty skeptic found no leakage.

## Decision
Full success criterion met for one cell. status: CONFIRMED_SOLUTION, standing only if kit/check_run.py prints CHECK_RUN: PASS
for the package and the run; otherwise PROMISING.
