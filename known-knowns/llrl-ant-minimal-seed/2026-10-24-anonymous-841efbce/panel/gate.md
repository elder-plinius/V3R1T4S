# Honesty gate: run 2026-10-24-1605, llrl-ant-minimal-seed (local target), partial win p1
gate written: 2026-10-24T17:42Z (date -u) by the run's orchestrating session, after reading all four panel files in full.
status: CONFIRMED_PARTIAL
confirmed_scope: For LLRL in the fixed frame (origin, facing north, y down), g(0)=256241 on the blank grid; g(1)=555, g(2)=318, g(3)=245, g(4)=195, g(5)=174, each with exactly one minimiser modulo never-read cells, namely (1,0,1), (1,0,2)+(1,-1,1), that pair plus (0,2,3), (-1,0,2)+(0,-1,2)+(0,2,1)+(1,-2,1), and (0,1,3)+(2,1,3)+(0,2,2)+(1,2,3)+(3,0,1); K0=12 with exactly the 10 onset-0 seeds in data/minimisers.txt, and no 11-cell seed has onset 0 on H384.
partial win: p1 (g(k) for k = 1..5 and g(0) = blank onset, conditions (i) and (ii) for those k, K0 = 12 as in (iii)). The full success criterion (all k up to K0-1 = 11) and p2 (k = 6) are not met. The target is user-added (targets-local/llrl-ant-minimal-seed.md), not a pinned-bank target.

## Panel record (plain)
Each reviewer was a fresh headless Grok Build CLI session (grok --prompt-file, no prior conversation), started in its own copy of claim/, nice -n 19. The three main reviewers ran in parallel from 2026-10-24T17:07:15Z (1500 s timeout, 1 worker each).
- CRITERION (criterion.md): pass. Read both checkers, the certificate and the logs; own simulator re-certified every minimiser and the blank onset (cert true at onset, false at onset-1, word = rotation of H384). Rebuilt A and B and re-ran k=1..3, the planted k=2 positive, the RL control and the T=0 searches (match the logs digit for digit). Audited (did not re-run) k=4 and k=5. Wrote the confirmed_scope above. It noted the 40-piece A pass was incomplete at its snapshot; it has since finished (40/40, min 174, same seed; claim/data/this-run/A/q_k5_T174/NOTE.txt).
- NOVELTY (novelty.md): pass. OEIS (several subsequences, both conventions, "LLRL"): no match. GLR 2409.10124 / Natural Computing 2025: only the rounded blank onset 256100. Lutfalla arXiv 2506.10482 (LLLR, different rule) and 2505.05426; Lutfalla simulator: a 13-cell onset-0 H384 snapshot (no minimality, not below 12). New find: a 2026-10-15 YouTube video gives the exact blank onset 256,241 (g(0) is therefore not claimed as new). Caveat: Springer PDF paywalled; Semantic Scholar rate-limited.
- REPRODUCE (reproduce.md): pass. Own simulator before reading code: blank 256241/P=384, every minimiser; own exhaustive k=1 and k=2 (no onset below 555 / 318). Rebuilt A and B for k=1..3, K0 and two k=5 B pieces; no mismatch. Caveat: did not re-run full k=4/k=5.
- REPRODUCE-EXHAUSTIVE (reproduce2.md, supplementary, started 2026-10-24T17:29:05Z with a narrow prompt to close the REPRODUCE caveat; 4 workers allowed): pass. Re-executed checker B fully for k=4 (27,257,864 leaves) and all 40 k=5 pieces (542,179,718 leaves, viol=0, one MIN at 174), every output byte-identical to the stored logs; re-ran A queue pieces 3, 7, 10, 35 (piece 10 gives the 174 seed), byte-identical.
- Gate-side checks: repo/TROPHY_CASE.md (kit pin 04fdfba) has no LLRL entry; GitHub open PRs of elder-plinius/V3R1T4S searched for "LLRL" at 2026-10-24T17:42Z: none.
- File sha256 at gate time: criterion.md 5c985326..., novelty.md 4b5d815f..., reproduce.md 0294ce8e..., reproduce2.md dd7c4fbb..., 

## Downgrade check (kit/RUN.md step 7)
- Hedging panelist: no. All four pass outright and state their caveats.
- Reproduction mismatch: none. Every re-run output matches the stored logs.
- Table value: no record table exists. Known single points (GLR's rounded 256100; the exact 256241 in a video; a 13-cell onset-0 snapshot) are consistent and disclosed. The GLR fetch is from 2026-10-24T16:05:56Z (under 6 h old).
- Stretched criterion or hidden quantifier: fixed frame, "modulo never-read cells", the onset convention and the H384 word (not other highways) are named in the scope sentence or in criterion.md; the certificate is a sufficient condition stated in CERT.md.
- Scope wider than reproduced: no. k=1..3 and K0 re-run by two reviewers; k=4 and k=5 re-run in full with checker B by a fresh reviewer, and k=5 A pieces spot-matched; A's complete k=5 runs (two splits) are in the logs. Every minimiser re-certified by two independent simulators.
- Capped search used as an exclusion: no. T is the onset bound being proved, not a search cap; both checkers are uncapped otherwise.
- Sample presented as complete: no. Several objects bundled: one table with its minimiser list, as p1 asks.
Result: no downgrade. Final status CONFIRMED_PARTIAL (p1), subject to CHECK_RUN: PASS.
