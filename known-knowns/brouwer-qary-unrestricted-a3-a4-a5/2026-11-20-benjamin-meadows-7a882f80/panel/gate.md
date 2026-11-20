# Honesty gate: brouwer-qary-unrestricted-a3-a4-a5 A4(12,7)

gate_by: packaging run, after reading reproduce.md, novelty.md and criterion.md for this claim
gate_time_utc: 2026-11-20T14:10Z

status: CONFIRMED_SOLUTION
panel: reproduce pass: true; novelty pass: true; criterion pass: true
confirmed_scope: `object/A4-12-7-320words.txt` (sha256 7a882f80...) lists 320 distinct words of length n = 12 over q = 4 symbols with minimum Hamming distance 7 over all pairs, which is strictly above the lower bound 256 (ub 1167, not `=`) for A4(12,7) as extracted in RECORD.md from the quaternary table fetched 2026-11-20T14:01:15Z; page fidelity and the literature search are left to the other reviewers.
conditions: the code was sent to A. E. Brouwer on 2026-11-20 and is not yet in his table; the novelty reviewer's table fetch (14:05:43Z) was byte-identical to the claimant's (14:01:15Z); its one arXiv API request was rate-limited (HTTP 429) and not retried, and web searches covered arXiv instead.
