# Novelty verdict (claim q132-1: no [[132,1,44]] qubit stabilizer code, bound <= 43)

context: subagent (same VM)

## Primary status page (fetched once, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=132&k=1
- UTC fetch time: 2026-10-16T19:46:15Z (from `date -u`, saved in fetch_time.txt)
- HTTP status: 200 (one plain curl request, user agent "V3R1T4S-panel (honest single request)"; no challenge page)
- Saved page: status_page_live.html (72072 bytes)
- sha256 (sha256sum): 61399b24e3e415e90dd5ea5a3eeb0897c628605dbaef73de052b897140b2bd11
- Value read: "Bounds on [[132,1]]_2  lower bound: 27  upper bound: 45". The page footer says: "For n>100, the upper bounds on qubit codes are weak (and not necessarily monotone in k)."
- The hash equals the claim-time hash in CLAIM.md, so the live table is unchanged since the claim was made.
- Claimed bound 43 < live value 45, so it is strictly below the table (by 2, not a tie).
- check/propagation_check.txt: neighbouring live cells give (132,1)=45, (133,1)=45, (131,2)=45; propagation does not imply 43.
- check/checker_output.txt reports VERIFIED for both certificates (44 and 45). Correctness of the proof is outside my novelty scope.

## TROPHY_CASE.md (data/TROPHY_CASE_pinned_9b1d444.md, 100 lines)
- Searched for qubit, stabilizer, quantum, codetables, QECC, 132, shadow: no matching entry. It covers graphs, constant-weight codes (classical Delsarte LP), VNN-COMP and others. Nothing on quantum code bounds, so no prior record for this cell there.

## Literature and web searches (last 24 months, Oct 2024 to Oct 2026)
1. "upper bound qubit stabilizer codes [[132,1]] linear programming shadow enumerator Rains": only classic works (Rains quant-ph/9611001, 9709049, CRSS 9608006), entanglement-assisted LP for n<=20 (1602.00413), SDP for EA codeword-stabilized codes (2311.07111). Nothing for [[132,1]].
2. "arXiv 2025 new upper bounds ... linear programming n > 100 qubit shadow constraints": no hit reporting shadow-constrained LP for n>100. arXiv 2601.15446 (check-weight-constrained quantum codes) does LP bounds for constrained-weight codes; WebFetch of its abstract mentions neither shadow constraints, n>100 nor [[132,1]]. This is a different problem (weight-constrained) and does not bound unconstrained [[132,1]].
3. "[[132,1" quantum code upper bound distance: only Monte-Carlo/BP distance-estimation papers (2402.06481, 2603.22532), which give no upper bound on d(132,1). The only analytic reference is Rains's [[n,1,d]] LP/shadow bound, whose closed-form value for n=132 is 45, the same as the table.
4. "improved upper bounds additive quantum codes length 100 to 256 ... Grassl table 2025": no paper improving upper bounds in n=101..256.
5. Open pull requests of elder-plinius/V3R1T4S (web search only, no GitHub tools): "elder-plinius V3R1T4S pull request codetables QECC qubit upper bound [[132,1]]" and "V3R1T4S github elder-plinius pull requests quantum stabilizer code bound Farkas certificate". Both returned no PR touching quantum codes or codetables. Search could not list the PR tab, so absence of a competing PR is not conclusive. A social post said the repo received nearly 200 PRs in its first 2 days.

## Assessment
- The live table (fetched now) says 45 and the claim says 43. No source found gives an upper bound at or below 43 for [[132,1]], and no source found runs the qubit LP with shadow constraints for n>100.
- Caveats: (a) the open-PR check is web-search-only and limited; (b) Rains's analytic bound is 45 for this n, so a 43 would be a sharper-than-analytic LP result; its soundness is for the other skeptics (the exact checker reports VERIFIED).
- Under the novelty rule (strictly beats table and everything I could find), the result passes.

pass: true
