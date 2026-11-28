# Honesty gate: run 2026-10-27-2252, llrl-ant-minimal-seed (local target), partial win p2
gate written: 2026-10-27T23:57Z (date -u) by the run's orchestrating session, after reading all four panel files in full.
status: CONFIRMED_PARTIAL
confirmed_scope: For LLRL in the fixed frame (origin, facing north, y down), g(6)=139 with exactly one minimiser modulo never-read cells, namely (0,1,3)+(0,2,2)+(1,2,3)+(1,4,3)+(2,1,3)+(3,0,1); completeness for at-most-6 cells (no onset <139) holds by two independent exhaustive checkers (hsearch A, full 40/40 pieces combining box TMAX=174 and home TMAX=140 sub-pieces; lcb_fast B at T=139, 400/400 pieces, 5011329083 leaves, viol=0, one MIN); the minimiser is re-confirmed by independent simulation with a translate certificate (onset 139 cert true, 138 false).
partial win: p2 (g(k) for k=1..6 with conditions (i) and (ii) for those k). g(0..5) and K0=12 remain as CONFIRMED_PARTIAL p1 (run 2026-10-24-1605 / draft PR #709) and are not re-opened here. The full success criterion (all k up to K0-1=11) is not met. The target is user-added (targets-local/llrl-ant-minimal-seed.md), not a pinned-bank target.

## Panel record (plain)
Each reviewer was a fresh headless Grok Build CLI session (grok --prompt-file, no prior conversation), started in its own copy of claim/, nice -n 19.
- CRITERION (criterion.md): pass. Read both checkers; own/indep sim certified the k=6 seed (onset 139, H384 word, cert at 139 not 138); rebuilt A/B; re-merged all shipped pieces; re-ran cheap controls (k=3, one A sub-piece, one B piece). confirmed_scope matches above for k=6. Caveat: full 84 A / 400 B not re-executed in that session.
- NOVELTY (novelty.md): pass. OEIS (including ±1 onset conventions), GLR 2409.10124 and Semantic Scholar citations, Lutfalla 2506.10482/2505.05426 and lutfalla.fr/ant, GitHub, LifeWiki, MO/MSE, Reddit, YouTube, X: no published g(6)=139 or this 6-cell minimiser. In-project p1 (#709) is disclosed background.
- REPRODUCE (reproduce.md): pass. Own simulator before reading code: blank 256241, k=5=174, k=6=139 (cert true at 139 / false at 138). Rebuilt A/B; re-merged all shipped outputs; re-ran k=1..3; replayed one home A sub-piece and B pieces 0 and 159. Caveat: full k=6 A/B not re-run end-to-end.
- REPRODUCE-EXHAUSTIVE (reproduce2.md, supplementary): pass. Prior same-directory session re-executed all 400 checker-B pieces at T=139 (LCB_SPLITD=60); closing session verified every bout file byte-identical to shipped done files (leaves=5011329083, viol=0, mins=1, flags=0, unique MIN matching the claim) and spot-re-ran pieces 0, 159, 399 with matching DONE/MIN lines; B-results-digest cbd7913df3b309c1 reproduced. A: p16 matched; one home sub-piece incomplete RESULT only.
- Gate-side checks: coverage audit data/audit/COVERAGE_AUDIT.md (A 84/84 digest bc8fc1f6719817ee; B 400/400 digest cbd7913df3b309c1); independent sim attempts/indep-sim; box TMAX=174 NONE pieces exclude onset 139; charter quarry llrl-ant-minimal-seed.
- File sha256 at gate time (first 16 hex): see panel/SHA256SUMS.

## Downgrade check (kit/RUN.md step 7)
- Hedging panelist: no. All four pass outright and state their caveats.
- Reproduction mismatch: none. Full B re-execution matched shipped logs digit for digit; spot A/B matches.
- Table value: no published g(6)=139; GLR rounded blank onset and YouTube exact blank onset are consistent and disclosed; g(1..5) is prior p1.
- Stretched criterion or hidden quantifier: fixed frame, modulo never-read cells, onset convention, H384 identity named in confirmed_scope / criterion.md.
- Scope wider than reproduced: no. k=6 B re-run in full by a fresh reviewer; k=6 seed re-certified by two independent simulators; A coverage audited + merges recomputed + spot re-runs; k=1..5 left as p1 background as claimed.
- Capped search used as an exclusion: no. B at T=139 is the onset bound being proved; A TMAX=174 on finished pieces excludes every onset ≤174 in those pieces.
- Sample presented as complete: no. One value g(6)=139 with its unique minimiser, as p2 asks.
Result: no downgrade. Final status CONFIRMED_PARTIAL (p2), subject to CHECK_RUN: PASS.
