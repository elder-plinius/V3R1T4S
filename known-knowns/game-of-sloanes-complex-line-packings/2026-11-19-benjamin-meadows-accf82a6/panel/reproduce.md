# REPRODUCE verdict: game-of-sloanes-complex-line-packings, cell (d, n) = (7, 31)

context: fresh reviewer (new context started for the REPRODUCE role only; saw only CLAIM.md, object/ and public pages; no access to the search code or the claimant's checker)
verdict_utc: 2026-11-19T05:12:46Z

## Value computed here
- Definition used (bank criterion, quoted from CLAIM.md):

> Success means n unit vectors in C^d, 3 <= d <= 7, for a (d,n) row of the live leaderboard (https://github.com/gnikylime/GameofSloanes README table, re-fetched live immediately before claiming) whose coherence mu = max_{j<k} |<phi_j,phi_k>|, computed in mpmath at 40 digits after normalising each vector, is STRICTLY LOWER (direction: min) than the listed 'Best Coherence' by at least 1e-8 (the table's resolution and the maintainers' stated acceptance threshold), the row is not marked provably optimal, mu is at least the listed lower bound (a value below it means a bug), and the vectors are given to >= 16 significant digits in the repository's file format (real parts of all vectors vector-by-vector, then imaginary parts).

- Verification method (quoted from CLAIM.md):

> Download the claimed .txt (2dn numbers), reshape as vectors[j] = re[j*d:(j+1)*d] + i*im[j*d:(j+1)*d] (this layout reproduces the posted coherences, checked on 3x13_dgm and 4x9_hlc on 2026-10-15), normalise in mpmath, compute all n(n-1)/2 overlaps, take the max. Parse the live README table row for (d,n) and compare. Also recompute the posted file for that row to make sure the comparison uses the same convention. Under a minute for n <= 49.

- Own checker written from that definition: file object/7x31_bmea.txt split on whitespace; vector j (0-based) = re[j*d:(j+1)*d] + i*im[j*d:(j+1)*d] with re = first d*n numbers, im = last d*n; each vector normalised; all 465 pairs j<k evaluated (no sampling).
- Method 1, mpmath at 50 digits: mu = 0.3485093138521599189322310158935112513346
- Method 2, exact rational arithmetic on the decimal strings (|<a,b>|^2 / (|a|^2 |b|^2) as exact fractions, max taken exactly, square root taken at the end to 55 digits): mu = 0.3485093138521599189322310158935112513346
- Attaining pair (1-based vector indices): [6, 29] (both methods). Second-largest overlap 0.3485093138521124221189122 at pair [13, 19]; gap 4.74968e-14. 325 of 465 overlaps lie within 1e-9 of mu (an equalised packing, as expected for a polished optimum).
- Claimed value in CLAIM.md: 0.34850931385215; leaderboard value quoted in CLAIM.md: 0.34941560.
- Live README: GET https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md at 2026-11-19T05:10:57Z, HTTP 200, sha256 699dbe7157363e568d11e019a0ea98178ec9f52f8834e900587c162801b0502d. Row: d=7, n=31, Best Coherence 0.34941560, Lower Bound 0.33806170, Creator jrr, Notes empty. These match the leaderboard value quoted in CLAIM.md; CLAIM.md quotes no lower bound, so the README value is used.
- Posted file: GET https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x31_jrr.txt at 2026-11-19T05:11:10Z, HTTP 200, sha256 7d0e57f131750209b9f9d41994093a37c9783f182b9e1eeda2d9c811272b8d84, 434 numbers; recomputed with the same layout in mpmath at 50 digits: 0.3494156040666677327699605400868924456455, which rounds to the table's 0.34941560.
- Margins: Best Coherence - mu = 9.062861e-4; mu - Lower Bound = 1.044761e-2.

## Clauses checked
- object sha256 matches CLAIM.md: PASS (computed accf82a6ee2089b168a50f6100f78a3b3a7edf28ca8af3bf01ed8e0386c01d5c)
- count of numbers = 2*d*n: PASS (434 numbers, 2*7*31 = 434; one per line)
- every token parses as a decimal number: PASS (0 unparsable tokens)
- >= 16 significant digits per coordinate: PASS (minimum 21 significant digits over all 434 tokens)
- no zero vector: PASS (0 zero vectors (exact squared norms); stored norms in [0.99999999999999992048, 1.0000000000000002437])
- mpmath (50 digits) and exact rational agree: PASS (|difference| = 6.6819e-52, same attaining pair)
- deterministic: PASS (two separate mpmath runs gave identical top-3 overlaps to 45 digits)
- mu matches claimed value: PASS (mu - claimed = 9.92e-15 (claimed given to 14 decimals))
- layout convention reproduces posted table value: PASS (posted CurrentBestPackings/7x31_jrr.txt recomputes to 0.349415604066, table 0.34941560)
- row not marked provably optimal: PASS (Notes column of the live row is empty (no open-circle mark))
- mu strictly below Best Coherence by >= 1e-8: PASS (0.34941560 - mu = 9.062861e-4)
- mu >= listed lower bound: PASS (mu - 0.33806170 = 1.044761e-2)
- 3 <= d <= 7: PASS (d = 7)

## Decision
The saved object has the required format and, computed independently in mpmath at 50 digits and in exact rational arithmetic, has coherence 0.3485093138521599, which is 9.063e-4 below the live Best Coherence 0.34941560 for (7, 31) and above the listed lower bound 0.33806170. The same layout convention reproduces the posted leaderboard file's value, and the row carries no provably-optimal mark. Every clause of the bank criterion is met.

pass: true
