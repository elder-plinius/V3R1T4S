# Honesty gate — runs/2026-11-03-1435-dnaedit93
context: main session (Alpha), step 7 honesty gate
date: 2026-11-03 ~15:48 America/New_York (EST)

panel files read:
- reproduce.md — pass: true (own C + Python checkers VALID 1042; author checkers VALID; same-seed regen byte-identical at it=8159505)
- novelty.md — pass: true (live Table 7.1 row 9 = 939g at 20:25Z; no published >=1042 found; residuals named)
- criterion.md — pass: true

downgrade checks (none triggered):
- no hedging panelist
- no reproduction mismatch (regen cmp identical)
- value strictly better than live table (1042 > 939g)
- criterion not stretched; one cell, one object
- scope no wider than evidence
- panel table fetch age < 6 h (novelty 20:25Z; gate ~20:48Z)
- no bundled cells

residuals carried (do not block CONFIRMED_SOLUTION under kit rules; disclosed):
- Congr. Numer. 204 journal version of thesis unopened
- Orth & Houghten CIBCB 2011 full text unopened
- Ashlock/Houghten CIBCB / BioSystems full texts unopened
- Banerjee ISIT 2025 full text paywalled

status: CONFIRMED_SOLUTION
confirmed_scope: The 1042-word list in claim/object/code_n9_d3_k1042.txt (sha256 b51b30e3082648bc6cb0511bd156b71ae51c967f7281a83010d2c0e844e4a93a) is a code of length 9 over {A,C,G,T} with every word of GC weight 4 and Levenshtein distance at least 3 between any two distinct words and between any word and the reverse complement of any word including itself, which is strictly larger than the lower bound 939 (not marked exact) given for cell (n,d)=(9,3) in Table 7.1 of J. Sun's 2009 Brock M.Sc. thesis under that thesis's own constraint set; whether it also beats every later published value is left to the NOVELTY check.
