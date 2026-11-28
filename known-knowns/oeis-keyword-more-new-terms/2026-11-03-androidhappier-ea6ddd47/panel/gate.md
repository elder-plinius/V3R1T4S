# Honesty gate: oeis-keyword-more-new-terms / A214570(17) = 3360 (run 2026-11-03-2128-maxembed)

status: CONFIRMED_SOLUTION
confirmed_scope: A214570(17) = 3360 -- one new term at the first missing index (n=17) of an OEIS keyword-more sequence, computed by two independently written programs (different algorithms) that agree and both reproduce DATA a(1..16), not present in the entry, its edit history (incl. pending drafts), or an OEIS value search as this count, and A214570 not named in the V3R1T4S bank.

Gate session: executor gate session, separate from the three panel sessions; it wrote no panel vote.
Read: panel/reproduce.md (context: subagent (reproduce), pass: true), panel/novelty.md (context: subagent (novelty), pass: true),
panel/criterion.md (context: subagent (criterion), pass: true, "full CONFIRMED_SOLUTION-eligible, not CONFIRMED_PARTIAL").
3/3 pass. The three files differ. The confirmed_scope line above is the criterion panelist's confirmed_scope sentence (the quoted statement), copied exactly.
Gate time: 2026-11-03T22:23Z-22:25Z (17:23-17:25 EST).

## Live re-fetch at the gate (one plain curl GET each, User-Agent "V3R1T4S research", no retries; gate/gate_fetchlog.txt)
- 2026-11-03T22:23:33Z 200 01439a4fa1cf899471a8162720f7f6416b55844665b938189a7539645b177991 https://oeis.org/search?q=id:A214570&fmt=text -> gate_A214570_text.txt
- 2026-11-03T22:23:34Z 200 f01619000f7e1dcca8c97de72b77c2e2406ebb7fac1e749c0822957717805021 https://oeis.org/A214570 -> gate_A214570.html
- 2026-11-03T22:23:34Z 200 1990f8783a5b76c374ab6f8acc0c1eeb4e635546884e1ec13b255421788ebb64 https://oeis.org/A214570/b214570.txt -> gate_b214570.txt
- 2026-11-03T22:23:34Z 200 527993fcec307651759c3c07e41e8e9ad8330a9a2e78108a47009d3ce0e70a67 https://oeis.org/history?seq=A214570 -> gate_history.html
- 2026-11-03T22:23:34Z 200 c0ee7a9b9258e37391d0a0cdcde3535a2f34a8bca8dc373dfe5070c0e1b00435 https://oeis.org/search?q=1,1,1,2,3,4,6,12,24,40,60,120,240,420,840,1680,3360&fmt=text -> gate_vs_fullprefix.txt
- 2026-11-03T22:23:34Z 200 b3fbd15cadb8d5ef88043d306ce5358c78676228e65434f4a9919479f131f23c https://oeis.org/search?q=1680,3360&fmt=text -> gate_vs_1680,3360.txt
- 2026-11-03T22:23:34Z 200 b8d6cad90fa38bfb40b3d809250d11213891bcb2d8fd85aaa5535fd8e26d0a16 https://oeis.org/search?q=420,840,1680,3360&fmt=text -> gate_vs_420,840,1680,3360.txt
- 2026-11-03T22:23:34Z 200 5cc11a046f0fa1b9784c9a74d524ac0ccc01e7247a618e11cd7ff503ce024e9f https://oeis.org/search?q=id:A214569&fmt=text -> gate_A214569_text.txt
- Entry text (fmt=text) byte-identical to the scout fetch 21:28:05Z and pre-claim fetch 21:36:40Z (sha256 01439a4f...): %I #29 May 28 2015, %S ends 840,1680 (a(16)), %K nonn,hard,more, %O 1,4, %E only "a(12)-a(16) from Alois P. Heinz, Sep 06 2012". "3360" occurs 0 times in entry text, entry page, b-file and history.
- b-file byte-identical to the pre-claim fetch (1990f878..., synthesized, ends "16 1680"). n = 17 is the first missing index.
- History: revisions up to #29 (Alois P. Heinz, May 28 2015, proposed -> approved) as newest; no revision > #29, no pending/editing draft; tag-stripped text identical to the pre-claim fetch except the site footer ("Last modified ... / Contains N sequences").
- Value searches: full prefix a(1..17) "No results." (byte-identical to claim time); 1680,3360 "Showing 1-10 of 22" (byte-identical to claim time; all unrelated: multinomial/Lah triangles, divisor records, etc.); 420,840,1680,3360 (HTTP 000 at claim time, 200 now): 4 hits A085988, A361937, A363692, A378630, all unrelated (prime signatures / divisor records), same set the novelty skeptic found. A214569 text byte-identical to claim time (b-file rows 1..16).

## PREREG timing (file mtimes, box clock America/New_York)
- PREREG.md "frozen 2026-11-03T21:28:38Z"; mtime 16:28:38 EST (= 21:28:38Z).
- Earliest program: attempts/search-engineer/code/progB.c 16:31:59 EST, attempts/exact-eval-first/code/progA.c 16:32:29; first n = 17 outputs 16:32:02 (B) / 16:36:00 (A); claim/object/VALUE.txt 16:38:58. All claim/ files are later than PREREG.
- PREREG thresholds (A and B reproduce DATA a(1..16) and agree on a(17); negative fixture differs from DATA; value search no hit holding it as this count with context search a(16),a(17); entry/b-file/history unchanged with no pending draft): all met.
- null_test: not needed because (exact deterministic count).

## Independent recomputation at the gate
- Fresh copy of claim/ in a temp folder: gcc -O2 programs/pA_c/progA.c and programs/pB_c/progB.c; ./pB 17 -> gate/pB_17.gate.out; nice ./pA 17 -> gate/pA_17.gate.out (about 50 s on this box).
  Both byte-identical to the stored programs/pA_c/progA_17.out and programs/pB_c/progB_17.out. Column 2 for n = 1..16 = 1,1,1,2,3,4,6,12,24,40,60,120,240,420,840,1680 = DATA; n = 17: 3360 in both; ordered = sum = 35357670 = Catalan(16); classes = trees = 634847 = A000081(17); argmax = 1 in both.
  table/brute_fixtures.py rerun: third method matches DATA for n <= 12; no-multiplicity negative fixture differs.

## Downgrade audit (statuses only go down)
- Hedging panelist: none. All three end 'pass: true' without conditions; CRITERION states full, not partial.
- Reproduction mismatch: none. Program A (C brute force over all Dyck words, hash-interned class counting, no formula), Program B (C Beyer-Hedetniemi level sequences with c(t) = prod deg!/prod mult!), the reproduce skeptic's own Python checker (definition brute force n <= 11 and multiset enumeration n <= 17), the criterion skeptic's re-run and this gate agree: a(17) = 3360, unique maximizer.
- Value not new: absent from DATA, b-file, %C/%F/%e/%p/%t/%E, history and drafts; companion triangles A214569/A214571 stop at row 16; full-prefix search No results; 2-term and 4-term context searches hit only unrelated sequences; bare "3360" (1069 hits) is uninformative and disclosed. Under the bank wording ("no hit holding it as this count") this passes.
- Stretched criterion / hidden quantifier: no. Criterion asks for at least one new value at the first missing index; a(17) = 3360 is that value. Both programs written in C, but with different algorithms (bank: "different algorithms or languages"); both from this run (disclosed).
- Scope wider than reproduced: no. Scope = a(17) only; B's by-products a(18..21) are not claimed.
- Sample as complete / capped search / probable prime: n/a (exhaustive over all 634847 rooted trees and all 35357670 ordered trees).
- Table value by evasion: no. Plain GETs, HTTP 200.
- Several objects bundled: no. One cell, one value.
- Bank exclusion: "A214570"/"A214569" absent from repo/bank/targets.json, bank/proposed, TROPHY_CASE.md and known-knowns (panel novelty/criterion); not in the excluded list; not repdigit/repunit.
- Benchmark baseline: n/a.

## Decision
Full success criterion met for the whole scoped statement. status: CONFIRMED_SOLUTION, standing only if kit/check_run.py prints
CHECK_RUN: PASS for the package and the run; otherwise PROMISING.
