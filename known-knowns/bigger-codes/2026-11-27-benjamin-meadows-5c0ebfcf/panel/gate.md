# Honesty gate: constant-weight-codes A(29,10,8)

gate_by: packaging run, after reading reproduce.md, novelty.md and criterion.md for this claim
gate_time_utc: 2026-11-27T18:59Z

status: CONFIRMED_SOLUTION
panel: reproduce pass: true; novelty pass: true; criterion pass: true
confirmed_scope: The file object/A-29-10-8-98words.txt (sha256 5c0ebfcf...) is a list of 98 distinct binary words of length 29, each of weight 8, with minimum Hamming distance 10 (so also A(29,10,21) at least 98 by complement), which exceeds the lower bound 96 and does not exceed the upper bound 203 of the A(29,10,8) cell as recorded in RECORD.md from the table fetched at 2026-11-27T18:39:11Z.
conditions: all three reviewers re-fetched the table and found the page byte-identical to the claimant's fetch at 2026-11-27T18:39:11Z; the REPRODUCE reviewer rebuilt the object byte for byte with how-we-built-it/rebuild.sh under Apple clang on arm64 (the claimant's replay ran on Linux x86-64 with g++); the reviewers found no value at or above the claimed size in arXiv:2608.13906, arXiv:2607.19550, newer 2026 arXiv papers or this repository. After the panel, README.md's construction paragraph was reworded at the CRITERION reviewers' note ("keeps the seed words" became "starts from the seed words", with the number of seed words the final code shares) and HOW_WE_FOUND_IT.md now explains why fewer than 20 seeds ran at some sizes; the scope sentence is unchanged. The code is to be sent to A. E. Brouwer after this claim is filed and is not yet in his table. The NOVELTY reviewer's Semantic Scholar (429) and Echols repository tree (403) lookups were refused and not retried.
