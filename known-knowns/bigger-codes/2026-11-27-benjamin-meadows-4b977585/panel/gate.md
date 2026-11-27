# Honesty gate: constant-weight-codes A(27,8,12)

gate_by: packaging run, after reading reproduce.md, novelty.md and criterion.md for this claim
gate_time_utc: 2026-11-27T18:59Z

status: CONFIRMED_SOLUTION
panel: reproduce pass: true; novelty pass: true; criterion pass: true
confirmed_scope: The file object/A-27-8-12-3387words.txt (sha256 4b977585...) is a list of 3387 distinct binary words of length 27, each of weight 12, with minimum Hamming distance 8 (so also A(27,8,15) at least 3387 by complement), which exceeds the lower bound 3374 and does not exceed the upper bound 10460 of the A(27,8,12) cell as recorded in RECORD.md from the table fetched at 2026-11-27T18:39:11Z.
conditions: all three reviewers re-fetched the table and found the page byte-identical to the claimant's fetch at 2026-11-27T18:39:11Z; the REPRODUCE reviewer rebuilt the object byte for byte with how-we-built-it/rebuild.sh under Apple clang on arm64 (the claimant's replay ran on Linux x86-64 with g++); the reviewers found no value at or above the claimed size in arXiv:2608.13906, arXiv:2607.19550, newer 2026 arXiv papers or this repository. After the panel, README.md's construction paragraph was reworded at the CRITERION reviewers' note ("keeps the seed words" became "starts from the seed words", with the number of seed words the final code shares) and HOW_WE_FOUND_IT.md now explains why fewer than 20 seeds ran at some sizes; the scope sentence is unchanged. The code is to be sent to A. E. Brouwer after this claim is filed and is not yet in his table. The NOVELTY reviewer hit the unauthenticated GitHub API rate limit (HTTP 403) on two pull request pages and ran the pull request check as authenticated read-only searches; nothing was found.
