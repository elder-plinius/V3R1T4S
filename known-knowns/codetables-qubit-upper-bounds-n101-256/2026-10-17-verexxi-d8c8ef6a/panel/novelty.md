context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty skeptic verdict for [[161,2]] (claim: no [[161,2,53]] code, upper bound at most 52)

## What I did and real output

1. Read CLAIM.md and REPRODUCE.md. Claim: upper bound 52 (certificate for d=53), versus the live upper bound 55.

2. Live table fetch, exactly one request after `sleep 60`:
   `curl -s -A "V3R1T4S-verexxi" -o novelty_fetch.html -w '%{http_code}' "https://codetables.de/QECC.php?q=4&n=161&k=2"`
   - URL: https://codetables.de/QECC.php?q=4&n=161&k=2
   - UTC time (date -u) before the request: 2026-10-17T05:41:12Z; after: 2026-10-17T05:41:13Z
   - HTTP status: 200
   - sha256 of novelty_fetch.html: f7271221c6cf52a5b73dd7c073f40879dee98b24c77e9bb794745673746039ef (1523 bytes; identical to the claim-time fetch, data/QECC_q4_n161_k2_claimtime.html)
   - Page text: "Bounds on [[161,2]] 2 lower bound: 31 upper bound: 55"; "Last change: 10.06.2024". Not a challenge page.

3. Propagation: check/propagation_check.txt reads "live (161,2): [31, 55]  closure of the live table at (161,2): 54  neighbours R1 (n,k-1): [33, 55]  R2 (n+1,k): [32, 55]  R3 (n-1,k+1): [31, 54]". The closure bound is 54, so 52 is not implied by other live cells (it is also 2 below the best implied value).

4. Certificate sanity: `python3 -I check/check_cert.py result/cert_161_2_53_sh.json` printed "VERIFIED [[161,2,53]] shadow=True: value=1317 digits, max column coefficient <= 0, 52+2+52 multipliers". (This is the novelty panel, so I only note it; correctness belongs to the other skeptics.)

5. TROPHY_CASE.md: fetched the raw file from github.com/elder-plinius/V3R1T4S (main) once, HTTP 200, and grepped for 161. The only hit is an unrelated constant-weight-code row (A(26,6,13) >= 16225, which contains the digits 16117). The same grep on data/TROPHY_CASE_pinned_9b1d444.md gave the same single hit. No [[161,2]] entry.

6. Open pull requests: fetched the web page https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit (page 1) and, to see the rest of the listing, page=2 of the same query. Deviation to disclose: I made this page-1 request twice (the first output was truncated by my pipeline) plus one page-2 request, so three web requests in total, none to the REST API. Titles on both pages are all "[claim] codetables-qubit-upper-bounds-n101-256: [[n,k]] upper bound lowered from X to Y" by verexxi (about 34 PRs, numbers around 270 to 307 on page 1). The titles include [[165,2]] 55 to 53, [[159,2]] 53 to 51, [[148,2]], [[146,2]], [[142,2]], [[140,2]], [[133,2]], [[132,1]], [[105,4]], [[219,2]], [[225,2]]. No PR mentions [[161,2]] (grep for "[[161," returned nothing on either page).

7. Literature (last 24 months): one WebSearch for 2025-2026 arXiv work on nonexistence/LP/shadow bounds for [[161,2]]. Results: arXiv 2606.01943 (Scott-type bound for AME states, only one-dimensional pure codes; I fetched it and it gives nothing for [[161,2]]), 2408.10323 (SDP bounds on quantum codes), 2311.07111, 2608.10922 (locally recoverable). None mentions [[161,2]] or a table of improved bounds for n > 100. The table itself notes that its upper bounds for n > 100 are weak, and its last change date is 10.06.2024. Limit of this check: a single search plus one paper read, not an exhaustive literature survey.

## Reasoning

The live upper bound is 55 and the best value implied by propagation is 54. The claim is 52, which strictly beats the live value, the propagation closure, TROPHY_CASE (no entry) and all open PRs (none for this cell; the neighbouring sibling PRs are for other cells). I found no literature result for this cell. The claim is therefore novel as far as I can confirm, and it is not a tie.

pass: true
