context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty panel: [[146,2]] qubit upper bound 49 -> 47

## Table fetch (once, no retry)
- URL: https://codetables.de/QECC.php?q=4&n=146&k=2
- Fetched after `sleep 20`: start 2026-10-16T21:05:00Z (date -u), finished 2026-10-16T21:05:01Z
- HTTP status: 200, 87120 bytes, file novelty_fetch.html
- sha256 (real output): e767c28e676aecd16c0ce703b8a38796dd935f742602a9912db4846cad96e627
- Value quoted from the page: "Bounds on [[146,2]] ... lower bound: 30 upper bound: 49"
- The hash is identical to the claimant's claim-time capture (data/QECC_q4_n146_k2_claimtime.html), so the live table still shows 49 and was unchanged by anyone in the interval.

## Claim vs. record
- Claim: no [[146,2,48]] code exists, so the upper bound is at most 47. That is strictly below the live 49 (improvement of 2), not a tie.
- I re-ran check/check_cert.py on both certificates (standard library, integer arithmetic):
  - VERIFIED [[146,2,48]] shadow=True: value=1143 digits, max column coefficient <= 0, 47+2+47 multipliers
  - VERIFIED [[146,2,49]] shadow=True: value=999 digits, max column coefficient <= 0, 48+2+48 multipliers
- Propagation: REPRODUCE.md and check/propagation_check.txt state the closure of the live cells at (146,2) is 49, so 47 is not implied by other cells. I did not re-run parse_table.py or propagate.py; I relied on the claimant's recorded output (a limitation of this check).

## Prior art search
- Open pull requests of elder-plinius/V3R1T4S (list fetched read-only via the GitHub API, 100 per page): the codetables-qubit-upper-bounds-n101-256 claims open are [[132,1]], [[139,1]], [[145,1]], [[150,1]], [[152,1]], [[154,1]], [[158,1]], [[164,1]] (#257-#262, #266, #267). None concerns [[146,2]] or k=2.
- TROPHY_CASE.md (current main, and the pinned copy data/TROPHY_CASE_pinned_9b1d444.md): no mention of 146, codetables or quantum codes.
- arXiv searches (export API, last 24 months): "146,2" with quantum code gave no hits. Quantum weight enumerator / LP bound queries returned only older general LP-bound papers (2020, 2021), and the recent hits (e.g. "Quantizing Delsarte Theory", 2026-10-07; "Theory of low-weight quantum codes", 2026-01; "Check-weight-constrained quantum codes", 2026-01) are not seen to state an upper bound for [[146,2]]. I read only titles and dates, not full texts, so a result buried inside a paper is not excluded.
- No evidence found of any source (table, PR, paper) that already gives d <= 47 or lower for [[146,2]].

## Verdict
The claimed bound (<= 47) strictly beats the live table value (49), is certified by an exact certificate that checked out in my run, and I found no prior or competing claim. Caveats: propagation was taken from the claimant's output, and the literature check was by title and date only.

pass: true
