# Bloch's constant: B >= sqrt(3)/4 + 0.0155

## What
B >= sqrt(3)/4 + 0.0155 = 0.44851270189... has a computer-assisted, unrefereed proof in claim/PROOF.md with its programs, rerun by independent automated checkers at 128 and 256 bits with the cover independently checked, taking as cited inputs Bonk's positivity theorem (Proc. AMS 110, 1990), Landau's reduction (Math. Z. 30, 1929) and Wikstrom's arXiv 2608.17660v1 (lemmas re-derived, stored multipliers re-verified in Arb), and it strictly exceeds 0.0153 against the sources recorded in table/ (status page, open pull requests, arXiv title query, fetched 2026-11-01T02:18-02:19Z), where preprints.org manuscript 202610.1936 is recorded as unread (HTTP 403).

Path note: claim/PROOF.md = object/PROOF.md; claim/REPRODUCE.md = RUN_IT_YOURSELF.md; claim/CLAIM.md = this README.md; claim/away-primal/cover and strips = object/cover and object/strips; claim/near-lift/certs and each trig.bin are rebuilt from object/parts by verify-it-yourself/run_checks.sh; claim/away-primal/code = verify-it-yourself; table/ = the-record-we-beat/. Not shipped: panel_work/, attempts/, data/ (Wikstrom's arrays, from doi:10.5281/zenodo.21975862), the search-time logs.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (needs clang; last line PASS; under a minute). PASS checks file hashes and the cover inequalities; it does not rederive the library inputs (the Step 5 cuts, the Step 6 bound on |a3|, the E(s) table), and SHA256SUMS only shows they are the files shipped. Rederiving them needs Wikstrom's archive, see RUN_IT_YOURSELF.md. With `FLINT_PY=<a Python with python-flint>` it also replays all covers and positivity certificates in Arb.

## Compared to
| table | cell | value | margin |
|---|---|---|---|
| https://teorth.github.io/optimizationproblems/constants/57a.html, 2026-11-01T02:18:50Z | lower bound of B | sqrt(3)/4 + 2e-4 | |
| The bar, highest public lower bound found: Wikstrom, arXiv 2608.17660 v1 Theorem 1.1 (PR #223) | lower bound of B | sqrt(3)/4 + 0.0153 = 0.44831270189 | +0.0002 |

## Not claimed
No value above sqrt(3)/4 + 0.0155. Not refereed. The originals of Bonk's and Landau's papers were not read; their statements are taken as given in Wikstrom's paper. preprints.org manuscript 202610.1936 is unread; open pull request #245 cites it for constant 57c, an upper bound on the univalent constant. The upper side is untouched.

## Credits
F. Wikstrom, arXiv 2608.17660, https://arxiv.org/abs/2608.17660, and archive doi:10.5281/zenodo.21975862: the linear certificate frame (Theorem 3.2, 3.5), inequality (20), the coefficient-dependent radius idea, the 47 cuts of the top piece and the |a3| multipliers. M. Bonk, Proc. AMS 110 (1990) 889-894: positivity on |z| < 1/sqrt 3. E. Landau, Math. Z. 30 (1929): reduction. H. Chen and P. Gauthier, J. Anal. Math. 69 (1996); C. Xiong (1998): earlier bounds. F. Johansson: Arb. New here: explicit primal centre witnesses in place of the moment and Sion steps, the cuts of pieces 1 to 6, the positivity certificates at the larger radii, and the case split of seven pieces.
