# CRITERION verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (7, 20)

context: fresh reviewer (new context started for the CRITERION role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-18T00:30:28Z

## Value computed here
- mu = 0.3130761407816107813719867874416059543644 (40 significant digits shown, computed at mp.dps = 50), attained at vector pair (7, 12) (0-based).
- README: https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md fetched 2026-11-18T00:26:12Z, HTTP 200, sha256 699dbe7157363e568d11e019a0ea98178ec9f52f8834e900587c162801b0502d. Row: `<tr><td>7</td><td>20</td><td>0.31334596</td><td>0.31264095</td><td>hlc</td><td><a href="CurrentBestPackings/7x20_hlc.txt">File</a></td><td></td></tr>`
- Posted file: https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x20_hlc.txt (HTTP 200), sha256 f65f17e763674648ab065ae8cc699a6b0bc2ca512fea3c9db348cff876720a85, 280 numbers, recomputed coherence 0.31334595651199423906; the object is 0.000269815730383 below it.
- CLAIM.md's own statement about open pull requests (1e-7 bar) is outside this role and was not checked.

## Clauses checked
- d in 3..7: PASS (d = 7)
- (d, n) is a row of the live README table: PASS (1 row found for (7, 20))
- mu in mpmath at >= 40 digits, normalised, all pairs, stated layout: PASS (mp.dps = 50, 190 pairs, vectors[j] = re[j*d:(j+1)*d] + i*im[j*d:(j+1)*d] with re = first 140 numbers, im = last 140)
- mu strictly lower than Best Coherence by >= 1e-8: PASS (0.31334596 - mu = 0.000269819218389219)
- row not marked provably optimal (&#9675;): PASS (Notes cell is '' (no &#9675;; no &#9651; conjectured mark either))
- mu >= listed Lower Bound: PASS (mu - 0.31264095 = 0.000435190781610781)
- >= 16 significant digits per coordinate, as written: PASS (minimum 18 significant digits over 280 numbers, 0 below 16, no zero entries)
- file in repository format: 2dn numbers, one per line, nothing else: PASS (280 lines = 2*7*20; 0 non-numeric lines, 0 lines with stray whitespace, ASCII, final newline; object/ holds only 7x20_bmea.txt; sha256 bfca650c9a2fa6b2df28ba36c2ff0607705e5b28f8287beb04f3d209b9d51c6d matches CLAIM.md)
- convention check: posted file reproduces the table value to ~1e-8: PASS (recomputed 0.31334595651199423906 vs table 0.31334596 (difference -3.48801e-9))
- CLAIM.md quotes criterion, p1 and verification method verbatim: PASS (byte-identical to success_criterion, partial_wins[p1].statement and verification_method in bank/targets.json read from https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json (HTTP 200, sha256 7c3942f228807b3bd1eae1b636f557aca64344161137e8bda5566081a6b846a2; the `gh api` read of the same path hung and was stopped, so the raw URL of the main branch was used))
- steering text in CLAIM.md or object: PASS (none found: CLAIM.md matches the other 24 claim files except the title, object/sha256 and value lines; the object holds only numbers)

## Decision
The object's coherence 0.31307614078161 is 0.000269819218389219 below the listed Best Coherence 0.31334596 (hlc), above the Lower Bound 0.31264095, on a row not marked provably optimal, and the posted file confirms the convention. Every clause holds, so this cell is a full win.

pass: true
