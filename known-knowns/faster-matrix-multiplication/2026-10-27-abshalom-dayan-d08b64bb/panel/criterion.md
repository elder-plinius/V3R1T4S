# Criterion skeptic: fmm-catalogue-small-format-rank, claimed main success criterion (rank 1270 for <12,13,13> over Q)

context: subagent (fresh Claude Code Agent context, Opus 5.5, saw only claim/; clean re-run 2026-10-28)

## Method

I read claim/CLAIM.md, claim/TABLE_RECORD.md and claim/REPRODUCE.md, hashed the object files, and wrote my own exact checker (mine/mycheck.py, standard-library Python, run with `python3 -I` under `nice -n 10`). It parses claim/object/u.txt, v.txt and w.txt as rationals, scales each factor type to integers, expands every one of the 1270 rank-one terms into the full 156 x 169 x 156 tensor and compares it with the matrix multiplication tensor of <12,13,13> under the stated convention (C[i][l] = sum_k w_k[i*13+l] m_k). Result: 4,112,784 coefficients, 2028 nonzero entries equal to the 2028 target ones, 0 mismatches; no term has a zero factor; two random exact rational evaluations against AB gave 0 differing entries. I also ran claim/verify-it-yourself/run_checks.sh from a copy (mine/claim_copy): PASS (common denominator 59904, 4112784 Brent equations, 0 wrong; 3 random trials 0 differences). I then made exactly one plain GET per source the criterion names (curl, User-Agent "V3R1T4S-panel criterion skeptic (curl)", no cookies, no retries), saved the bodies in mine/fetched/ and parsed them with scripts. No guard, classifier block, 401, 403 or 429 occurred.

## Clauses

| clause (verbatim fragment) | finding | verdict |
|---|---|---|
| "an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms)" | claim/object/u.txt (sha256 d08b64bb...), v.txt (a1c14244...), w.txt (8180074e...): 1270 data lines each, sparse index:coefficient lists; every term has three nonzero factors | met |
| "for a format <n,m,p> with max(n,m,p) <= 16" | format <12,13,13> (A 12x13, B 13x13); max = 13 | met |
| "sorted(n,m,p) not in {(3,3,3),(4,4,4)}" | sorted (12,13,13) | met |
| "number of rank-one terms r" | r = 1270 (counted lines; no zero or empty term, so 1270 multiplications) | met |
| "the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json" | fetched 2026-10-28T05:44:19Z, HTTP 200, sha256 2a653515..., 343774 bytes; createdAt 2026-10-19T20:46:33; the only entry whose sorted format is [12,13,13] is {"format": [12, 13, 13], "rank": 1274}; 1270 < 1274 | met |
| "the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html" | https://fmm.univ-lille.fr/12x13x13.html fetched 2026-10-28T05:44:19Z, HTTP 200, sha256 1f1af49d..., 143643 bytes; heading "&lang;12&times;13&times;13:1274&rang;"; 1274 is the only number in 1000..1400 on the page; 1270 < 1274 | met |
| "the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md" | fetched 2026-10-28T05:44:20Z, HTTP 200, sha256 e71786dd..., 52950 bytes; single row for the format (line 659): "`12x13x13` \| 1298 (?) \| 1298 (?) \| 1274"; no row for 13x12x13 or 13x13x12; minimum 1274; 1270 < 1274 | met |
| "the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes" | fetched 2026-10-28T05:44:20Z, HTTP 200, sha256 c0d29fe3..., 276758 bytes; the README tables list 30 formats (10 "below the best known rank", 20 "new ZT records"), none of them 12x13x13 or a permutation in any spelling (x, ×, comma, underscore, hyphen: 0 hits); the README states schemes/ holds one file per scheme; no rank listed for this format, so no bar below 1274 | met (see caveat 1) |
| "every one re-fetched live immediately before claiming; the scheme beats the minimum over all four" | the claim's record shows fetches at 2026-10-27T22:01Z and 22:05Z; my panel re-fetch at 05:44:19Z to 05:44:20Z returns byte-identical bodies (same sha256) for the three sources the claim fetched at the same URLs; minimum over all four = 1274; 1270 is 4 below it | met |
| "verified in exact arithmetic (integers/fractions ...) over the ring it claims" | ring Q; denominators 2, 3, 4, 6, 8, 12, 13, 16, 24, 32, 39, 96, 117; my independent integer-scaled full-tensor check and the claim's checker both give 0 wrong out of 4,112,784 | met |
| "a scheme valid only over GF(2) counts here ONLY if ..." | not applicable: the scheme is over Q (fractional coefficients with even denominators, so it is not a GF(2) scheme) | n/a |
| "obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed" | stated provenance is a one-slice restriction of LITA's 13x13x13 rank-1379 scheme plus 25 exact term absorptions, not a composition, padding or block split; in any case 1270 is not a value listed by any of the four sources (all list 1274 or no value) | met |
| "Ternary/integer re-derivations of a rank already attained over Q are NOT this target" | not a re-derivation: 1270 is below the best Q rank (1274) | met |
| "fewer additions at an existing rank is NOT this target" | the rank itself is new (1270 < 1274) | met |

## Caveats

1. For MerlijnW70/fmm-schemes I made the one GET of the named repository page. It lists the top-level entries (schemes/ is a directory) and the rendered README, but not the file names inside schemes/. My finding that the repository holds no <12,13,13> scheme rests on the README tables, which enumerate every scheme, and on the README's "one file per scheme" statement. The claim's own record of the full git tree (39 paths, none for this format) agrees, but I did not re-fetch that tree because the rule allows one GET per named source.
2. Perminov's ZT and Z entries for this format carry "(?)". This does not matter here because the Q entry 1274 is the minimum.
3. I did not run the rebuild from LITA's npz file. Provenance only matters for the composition clause, and that clause cannot exclude this result because 1270 appears in none of the sources.
4. I checked only the four named sources (plus the claim's own record). A lower rank published somewhere else would not change the literal criterion, but this verdict says nothing about it.
5. Null model: any of the four sources could have listed a permutation of the format with a different rank. fmm_sota.json has one entry for the sorted format, ranks.md has one row, and the Lille per-format page is the one for 12x13x13. None of them lists a value below 1274.

confirmed_scope: The files claim/object/u.txt (sha256 d08b64bb), claim/object/v.txt (sha256 a1c14244) and claim/object/w.txt (sha256 8180074e) define a bilinear scheme with 1270 rank-one terms (each with three nonzero factors) for <12,13,13> over Q that satisfies all 4,112,784 Brent equations exactly (0 mismatches in my independent integer-scaled full-tensor check and in the claim's own checker), and 1270 is strictly below every bar the criterion names as I fetched them: fmm_sota.json rank 1274 (2026-10-28T05:44:19Z, HTTP 200, sha256 2a653515), https://fmm.univ-lille.fr/12x13x13.html rank 1274 (2026-10-28T05:44:19Z, HTTP 200, sha256 1f1af49d), Perminov docs/ranks.md minimum over ZT 1298 (?), Z 1298 (?) and Q 1274, which is 1274 (2026-10-28T05:44:20Z, HTTP 200, sha256 e71786dd), and https://github.com/MerlijnW70/fmm-schemes, whose README lists no <12,13,13> scheme or permutation (2026-10-28T05:44:20Z, HTTP 200, sha256 c0d29fe3).
pass: true
