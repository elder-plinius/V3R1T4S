# Honesty gate: oeis-keyword-more-new-terms / A131449 flattened index 66 (row 6, m = 2) = 360 (run 2026-11-03-2153-orglabel)

status: CONFIRMED_SOLUTION
confirmed_scope: A131449 flattened index 66 (row 6, m=2) = 360, the first index missing from DATA/b-file, computed and agreed by two independent programs that reproduce all 66 existing terms; full row 6 = claim/object/ROW6.txt as the non-increasing listing (the convention every existing row follows). Criterion verdict for the panel: CONFIRMED (not partial) -- no criterion element fails and the order assumption does not affect the claimed term.

Gate session: executor gate session, separate from the three panel sessions; it wrote no panel vote.
Read: panel/reproduce.md (context: subagent (reproduce), pass: true), panel/novelty.md (context: subagent (novelty), pass: true),
panel/criterion.md (context: subagent (criterion), pass: true, "Criterion verdict for the panel: CONFIRMED (not partial)").
3/3 pass. The three files differ. The confirmed_scope line above is the criterion panelist's confirmed_scope sentence, copied exactly.
Gate time: 2026-11-03T22:01Z (17:01 EST).

## Live re-fetch at the gate (one plain curl GET each, User-Agent "V3R1T4S research", no retries; gate/gate_fetchlog.txt)
- 2026-11-03T22:01:20Z 200 a528ccf340058109f060ce2c4638e4ca6f60519a85c1a6a2d3123bec7e20d363 https://oeis.org/search?q=id:A131449&fmt=text -> gate_A131449_text.txt
- 2026-11-03T22:01:21Z 200 ea4dd988d3b042b00f9a699cccaa16af729d9a6c2d4572d28b13b3cf428c55d1 https://oeis.org/A131449 -> gate_A131449.html
- 2026-11-03T22:01:21Z 200 cabf2cc627ebbd35c4f5386667d07eb726c901567cd173782f04737509e66d49 https://oeis.org/A131449/b131449.txt -> gate_b131449.txt
- 2026-11-03T22:01:21Z 200 a5b3897615982772f0c19a892322c18bd07fa35eae103a84a70734a931e21e49 https://oeis.org/history?seq=A131449 -> gate_history.html
- 2026-11-03T22:01:21Z 200 d362dac2fe6b90660c7ad981d47ba7d36e29acd7894c077eaba44ecc95ea5647 https://oeis.org/search?q=2,1,720,360,360,360,360,360,240&fmt=text -> gate_vs_datatail_row6.txt
- 2026-11-03T22:01:21Z 200 b55e1092fe2856e19ec3ce2e91cb9655169a94ef8c4e3727c9da797aaccee316 https://oeis.org/search?q=720,360,360,360,360,360,240,240,240,240,180&fmt=text -> gate_vs_row6_head.txt
- 2026-11-03T22:01:21Z 200 281b37e113451b930dbe71e4de46fba0113b7327c1646cc783e35740b600f44c https://oeis.org/search?q=720,360,360,360,360,360,240&fmt=text -> gate_vs_row6_short.txt
- Entry text (fmt=text) byte-identical to the scout fetch 21:53:52Z (sha256 a528ccf3...); b-file byte-identical to scout and pre-claim fetches (cabf2cc6..., ends "65 720").
- Entry: %I #12 Aug 29 2019; %K nonn,more,tabf; %O 0,3; DATA ends ...,3,3,2,1,720 (indices 0..65). "360" occurs 0 times in entry text and entry page.
- History: revisions #12 (newest, approved) down to #1; tag-stripped text (scripts removed) identical to the pre-claim fetch 21:54:53Z; no pending/proposed draft; "360" occurs 0 times.
- Value searches: 2,1,720,360,360,360,360,360,240 / 720,360,360,360,360,360,240,240,240,240,180 (byte-identical to claim time) / 720,360,360,360,360,360,240: all "No results."

## PREREG timing (file mtimes, box clock America/New_York)
- PREREG.md "frozen: 2026-11-03T21:54:14Z"; mtime 16:54:14 EST (= 21:54:14Z).
- Earliest program: attempts/*/code/progA.py, progB.c 16:54:30 EST; fixtures.py 16:54:42; claim/object/ROW6.txt 16:54:50; VALUE.txt 16:55:24.
  Only data/ fetches (16:53:52 EST) precede PREREG. PREREG precedes every program, computed value and the claim.
- PREREG thresholds (A and B reproduce DATA 0..65; row 6 has 132 entries summing to 10395 = A001147(6) in both; A and B agree on sorted row 6;
  negative fixture differs from DATA; value searches no hit; entry/b-file/history unchanged with no pending draft; ordering convention disclosed): all met.
- null_test: not needed because (exact deterministic count).

## Independent recomputation at the gate
- Fresh copy of claim/ in a temp folder: python3 programs/pA_py/progA.py 7 -> gate/pA_7.gate.out; gcc -O2 progB.c; ./pB 7 -> gate/pB_7.gate.out.
  The two are byte-identical and identical to the stored progA_7.out; indices 0..65 == b-file; index 66 = 360; indices 65..196 == claim/object/ROW6.txt.
  table/fixtures.py: Lang row-5 bars 1,4,3,3,2,1,3,2,4,3,2,2,2,1,1,2,2,2,1,1 reproduced; both negative fixtures differ from DATA.

## Downgrade audit (statuses only go down)
- Hedging panelist: none. All three end 'pass: true' without conditions; CRITERION states CONFIRMED (not partial).
- Reproduction mismatch: none. Program A (Python hook formula), Program B (C removal-order DP, no hook formula), the reproduce skeptic's brute-force
  permutation checker, the criterion skeptic's re-run and this gate agree on rows 0..6 (A and B through row 7).
- Value not new: index 66 absent from DATA, b-file, %C/%H/%e/%E, history and drafts; Lang's linked files stop at row 5 (row-5 figure only);
  three contextual value searches "No results." (360 alone is uninformative; disclosed by CRITERION).
- Stretched criterion / hidden quantifier: no. Criterion asks for at least one new value at the first missing index; T(6,2) = 360 is that value.
- Ordering convention: %N does not define within-row order. T(6,2) = 360 is robust to any order consistent with rows 0..5 (720 unique max; 360 is
  the second value, multiplicity 5). The rest of row 6 is stated as the non-increasing listing, explicitly scoped so in confirmed_scope. Disclosure, not a scope cut.
- Scope wider than reproduced: no. Scope = index 66 plus row 6 as non-increasing listing; reproduced by 3 independent codes. Row 7 is a by-product, not claimed.
- Sample as complete / capped search / probable prime: n/a (exhaustive over all 132 ordered trees).
- Table value by evasion: no. Plain GETs, HTTP 200.
- Several objects bundled: no. One object (row 6 of one triangle, starting at the first missing cell, index 66).
- Bank exclusion: "131449" absent from repo/bank/targets.json, bank/proposed, TROPHY_CASE.md and outbox/; not in the criterion's excluded list; not repdigit/repunit.
- Benchmark baseline: n/a.

## Decision
Full success criterion met for the whole scoped statement. status: CONFIRMED_SOLUTION, standing only if kit/check_run.py prints
CHECK_RUN: PASS for the package and the run; otherwise PROMISING.
