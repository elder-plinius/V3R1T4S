# Honesty gate: constant-weight-codes A(30,12,9)

gate_by: packaging run, after reading reproduce.md, novelty.md and criterion.md for this claim
gate_time_utc: 2026-11-26T20:27Z

status: CONFIRMED_SOLUTION
panel: reproduce pass: true; novelty pass: true; criterion pass: true
confirmed_scope: The file object/A-30-12-9-45words.txt (sha256 806649f7...) is a list of 45 distinct binary words of length 30, each of weight 9, with minimum Hamming distance 12 (so also A(30,12,21) at least 45 by complement), which exceeds the lower bound 44 and does not exceed the upper bound 74 of the A(30,12,9) cell as recorded in RECORD.md from the table fetched at 2026-11-26T20:13:38Z.
conditions: the novelty reviewer's table fetch (20:17:35Z) and the reproduce reviewer's (20:17:46Z) were byte-identical to the claimant's (20:13:38Z); the novelty reviewer found no value of 45 or more for this cell in arXiv:2608.13906, arXiv:2607.19550, newer arXiv papers or this repository; the 215-word A(32,12,11) code file returned 404, so its best two-coordinate shortening (about 24 words on average) was not computed; the code is to be sent to A. E. Brouwer after this claim is filed and is not yet in his table. A first CRITERION review (verdict 2026-11-26T20:18:20Z, pass: true, same conclusions) wrote file-name patterns in angle brackets, which kit/check_run.py rejects as unfilled placeholders; since panel files are not edited, a second fresh CRITERION reviewer was started with the same instruction plus that formatting rule, and its file is panel/criterion.md. The first file is not included.
