# Novelty panel: [[200,2]] qubit upper bound

context: subagent (Claude Code headless on the owner's PC, fresh context)

## Primary table fetch (one fetch, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=200&k=2
- Command: curl -s -A "V3R1T4S-verexxi" -o novelty_fetch.html (after sleep 15)
- Fetched (date -u): 2026-10-16T21:12:15Z
- HTTP status: 200 (no challenge page; 1523-byte plain HTML)
- sha256 (novelty_fetch.html): 83407f406126a7bb6b725add67b0ec7128d170f6fd189103a79b419875fd60b8
- Value quoted from page: "Bounds on [[200,2]]: lower bound: 39, upper bound: 67". Page footer: "Last change: 10.06.2024". Page note: for n>100 the upper bounds are weak and not necessarily monotone in k.
- The sha256 is identical to the claimant's earlier fetch (claim time 21:01:52Z), so the live value is unchanged: 67.

## Open pull requests (one API call)
- URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=1 , HTTP 200, saved as pulls.json. 78 open PRs (fewer than 100, so this is the full list).
- Searched titles and bodies for "200,2", "[[200", "codetables", "QECC", the target id, "quantum", "stabilizer". Matches are only PRs 257, 258, 259, 260, 261, 262, 266, 267 for codetables-qubit-upper-bounds-n101-256. They cover cells [[132,1]], [[139,1]], [[145,1]], [[150,1]], [[152,1]], [[154,1]], [[158,1]], [[164,1]], all k=1. None names (200,2), and none claims any d <= 66 at (200,2).
- Propagation: those k=1 cells cannot lower (200,2) under d(n,k) <= d(n,k-1), d(n+1,k), d(n-1,k+1)+1 (k=1 cells are on the wrong side of the k and n rules; the claim's check/propagation_check.txt reports live neighbours R1 [39,67], R2 [39,67], R3 [38,67]). I did not recompute the propagation closure.

## TROPHY_CASE.md
- Source: raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, HTTP 200, saved as trophy.md (30936 bytes).
- It has no quantum-code, QECC or codetables entry. Rows are degree-diameter, Lehmer and similar.

## Literature, last 24 months (arXiv API, one query plus redirect follow, saved as arxiv.xml)
- Closest paper: arXiv 2603.19901 (Mar 2026), "SDP bounds on quantum codes: rational certificates". It improves 18 upper bounds for n-qubit codes with 6 <= n <= 19. It covers n up to 19 only, far below n = 200.
- arXiv 2502.14165 (Feb 2025), thesis on quantum Delsarte LP bounds in general quantum metric spaces. It gives no table entries at n = 200.
- arXiv 2306.00048 (May 2023, slightly older than 24 months): Hamming-like bound for degenerate stabilizer codes. It is not a specific n = 200 result.
- arXiv 2610.18130 (Oct 2026): neural distance prediction for BB codes. It is not an upper-bound result.
- I found no paper in the window that gives a bound for [[200,2]] or any n in 101..256 that is tighter than the table.

## Verdict
- Best known upper bound for [[200,2]] is 67 (live table). No open PR, no TROPHY_CASE entry and no paper found gives 66 or lower. The claim (no [[200,2,66]] and no [[200,2,67]], so d <= 65) strictly beats it. It is a strict improvement, not a tie.
- Limits: the table was fetched once, and the literature search was a single arXiv API query and abstract reading, not exhaustive. Certificate correctness is outside this role.

pass: true
