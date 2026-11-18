# CRITERION verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (4, 28)

context: fresh reviewer (new context started for the CRITERION role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:30:28Z

## Value computed here
- mu = 0.5771170599259038745234526030227877722929 (40 significant digits shown, computed at mp.dps = 50), attained at vector pair (2, 17) (0-based).
- README: https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md fetched 2026-11-18T00:26:12Z, HTTP 200, sha256 699dbe7157363e568d11e019a0ea98178ec9f52f8834e900587c162801b0502d. Row: `<tr><td>4</td><td>28</td><td>0.57711826</td><td>0.54772256</td><td>jrr</td><td><a href="CurrentBestPackings/4x28_jrr.txt">File</a></td><td></td></tr>`
- Posted file: https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/4x28_jrr.txt (HTTP 200), sha256 8b821d9d9ca0965f8f0f584b906e88c09d57af40ead16b16db41079171d60e41, 224 numbers, recomputed coherence 0.57711826421638707682; the object is 1.2042904832e-6 below it.
- CLAIM.md's own statement about open pull requests (1e-7 bar) is outside this role and was not checked.

## Clauses checked
- d in 3..7: PASS (d = 4)
- (d, n) is a row of the live README table: PASS (1 row found for (4, 28))
- mu in mpmath at >= 40 digits, normalised, all pairs, stated layout: PASS (mp.dps = 50, 378 pairs, vectors[j] = re[j*d:(j+1)*d] + i*im[j*d:(j+1)*d] with re = first 112 numbers, im = last 112)
- mu strictly lower than Best Coherence by >= 1e-8: PASS (0.57711826 - mu = 1.20007409612548e-6)
- row not marked provably optimal (&#9675;): PASS (Notes cell is '' (no &#9675;; no &#9651; conjectured mark either))
- mu >= listed Lower Bound: PASS (mu - 0.54772256 = 0.0293944999259039)
- >= 16 significant digits per coordinate, as written: PASS (minimum 17 significant digits over 224 numbers, 0 below 16, no zero entries)
- file in repository format: 2dn numbers, one per line, nothing else: PASS (224 lines = 2*4*28; 0 non-numeric lines, 0 lines with stray whitespace, ASCII, final newline; object/ holds only 4x28_bmea.txt; sha256 0b126eb16a321d7691a921464458ceed7b9113cc00660376208dfee443df7c72 matches CLAIM.md)
- convention check: posted file reproduces the table value to ~1e-8: PASS (recomputed 0.57711826421638707682 vs table 0.57711826 (difference 4.21639e-9))
- CLAIM.md quotes criterion, p1 and verification method verbatim: PASS (byte-identical to success_criterion, partial_wins[p1].statement and verification_method in bank/targets.json read from https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json (HTTP 200, sha256 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2; the `gh api` read of the same path hung and was stopped, so the raw URL of the main branch was used))
- steering text in CLAIM.md or object: PASS (none found: CLAIM.md matches the other 24 claim files except the title, object/sha256 and value lines; the object holds only numbers)

## Decision
The object's coherence 0.57711705992590 is 1.20007409612548e-6 below the listed Best Coherence 0.57711826 (jrr), above the Lower Bound 0.54772256, on a row not marked provably optimal, and the posted file confirms the convention. Every clause holds, so this cell is a full win.

pass: true
