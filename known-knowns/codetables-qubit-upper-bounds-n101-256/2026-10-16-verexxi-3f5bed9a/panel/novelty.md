# Novelty verdict

context: subagent (same VM)

## Primary status fetch (single plain request, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=139&k=1
- UTC fetch time: 2026-10-16T19:49:03Z (from `date -u`, saved in fetch_time.txt)
- HTTP status: 200 (no block, no challenge page)
- Value read: "Bounds on [[139,1]] ... lower bound: 29, upper bound: 47"
- Saved page: live_QECC_q4_n139_k1.html (79780 bytes)
- sha256: 22fe191aa3c3310d48d62cbf7e88640b2110cce4e0842998fb73e796bf75ba2e
  (identical to the claim-time sha256 recorded in CLAIM.md, so the cell is unchanged since the claim was made)
- The page itself states: "For n>100, the upper bounds on qubit codes are weak (and not necessarily monotone in k)."
- Claimed bound: upper bound <= 45 (no [[139,1,46]] code). 45 < 47 strictly. Neighbour cells in check/propagation_check.txt: (140,1) = [30,47], (138,2) = [28,47], so no table propagation gives <= 46 (I only read that file, I did not recompute it).

## Searches (last 24 months, web / arXiv via WebSearch)
1. "upper bound qubit stabilizer codes n=139 k=1 linear programming shadow enumerator minimum distance": only generic LP/shadow literature (Rains shadow enumerators, entanglement-assisted LP 1602.00413, SDP bounds); no n=139 value, no n>100 shadow-LP run.
2. "arXiv 2025 improved upper bounds quantum codes linear programming shadow constraints n > 100 codetables.de qubit": hits were SDP bounds on quantum codes (2408.10323, small n only), EA-CWS SDP (2311.07111, small n), pure quantum LRC bounds (2512.07256), GV-bound improvement (2601.18590); nothing at n>100 for qubit stabilizer codes, nothing giving a [[139,1]] bound.
3. "[[139,1" quantum code nonexistence distance 46 OR 47 stabilizer: nothing addressing [[139,1]]; only old Rains [[n,1,d]] LP work and small-n nonexistence results. One hit was a GitHub repository (brandonlign/quantum-code-bounds); per instruction I did not open it or use any GitHub tool, so it is unexamined.
4. "Grassl 2025 2026 new upper bounds additive quantum codes length 101-256 linear programming bound": no 2025-2026 result giving new upper bounds in this range.
5. Pinned TROPHY_CASE (data/TROPHY_CASE_pinned_9b1d444.md, 100 lines): grep for qubit / codetables / QECC / stabilizer / quantum found no match; only classical rows (degree-diameter, constant-weight, Lehmer). No prior claim on this cell.
6. Open pull requests of elder-plinius/V3R1T4S: web search "elder-plinius V3R1T4S pull request codetables qubit upper bound certificate" returned nothing for V3R1T4S (its pulls page did not appear; only other repos by that owner). No evidence of a competing PR, but the PR list itself was not seen (no GitHub tools allowed), so this is an absence of evidence.

## Assessment
The live table value is 47; the claim (<= 45) is strictly below it. No literature, trophy-case row or findable pull request gives an upper bound at or below 45 (or 46) for [[139,1]], and none reports a qubit shadow-LP run for n > 100. Caveats: web search is shallow, and the PR list was not directly inspected; this is a novelty check only (the certificate correctness and propagation rules are for the other skeptics).

pass: true
