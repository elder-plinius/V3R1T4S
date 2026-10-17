context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty check, [[185,3]] qubit upper bound

## What I did and real output

1. Read CLAIM.md and REPRODUCE.md. Claim: no [[185,3,61]] exists, so the upper bound is at most 60. The claim records a live upper bound of 63 and a lower bound of 36.

2. Table fetch, exactly once, after `sleep 110`:
   `curl -s -A "V3R1T4S-verexxi" -o novelty_fetch.html -w '%{http_code}' https://codetables.de/QECC.php?q=4&n=185&k=3`
   - HTTP status: 200
   - UTC time (date -u): Sat Oct 17 05:45:19 UTC 2026
   - sha256 of novelty_fetch.html: b63791604a45d3cf7bd4ada4ab322fdf8888038bb1b4eaaabaa258bf551694e2 (identical to the claim-time copy data/QECC_q4_n185_k3_claimtime.html)
   - Page text: "Bounds on [[185,3]] 2 lower bound: 36 upper bound: 63", construction of a [[185,3,36]] code; "Last change: 10.06.2024". No challenge page. The table value is unchanged and the claimed bound 60 is strictly below 63.

3. TROPHY_CASE.md of github.com/elder-plinius/V3R1T4S (raw, main): HTTP 200, 30936 bytes. A grep for "185" and "codetables" gave no matches, so there is no entry for this cell. The pinned copy in the claim folder (data/TROPHY_CASE_pinned_9b1d444.md) has no 185 entry either.

4. Open pull requests: one request to https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit returned HTTP 200 (page 1 of 25 titles; page header counts 33 open, 1 closed). Because the listing is paginated I also fetched page=2 of the same listing (HTTP 200, 9 more titles). The 34 titles are of the form "[claim] codetables-qubit-upper-bounds-n101-256: [[N,K]] upper bound lowered from X to Y". The only titles with n near 185 are [[183,1]] (61 to 59). No title mentions [[185,3]] or any k=3 cell at n=185. A `git ls-remote ... 'refs/pull/*/head'` call counted 307 PR heads in total, but titles are not available that way, so only the codetables-qubit search listing was inspected.

5. Literature: web searches (arXiv, last 24 months) for upper-bound, LP/shadow and SDP nonexistence results for [[185,3]] or n in 101..256 found only general papers (SDP bounds on quantum codes, arXiv 2408.10323, which targets small n). Nothing found that gives an upper bound below 63 for [[185,3]]. The search is not exhaustive, but nothing contradicts novelty.

6. Propagation: CLAIM.md/REPRODUCE.md state that the closure of all live cells at (185,3) is 61 (check/propagation_check.txt), so 60 is not implied by neighbouring cells. I did not re-run that script (it is the numerical skeptic's task); I only checked that it is stated.

## Reasoning

The live table says 63. The claimed result (at most 60) is a strict improvement. No known literature result, TROPHY_CASE entry or open PR for this exact cell was found. Correctness of the certificate is outside the novelty scope. The novelty condition (strictly beats everything known) holds on the evidence I could gather.

pass: true
