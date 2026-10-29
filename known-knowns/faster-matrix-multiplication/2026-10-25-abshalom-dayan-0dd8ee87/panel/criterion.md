context: subagent (Claude Opus 5.5, fresh context, given only a copy of claim/)

# Criterion skeptic: <24,25,25> rank 7157 (claimed level: partial win p1 of fmm-catalogue-small-format-rank)

Local material read: CLAIM.md, README.md, REPRODUCE.md, STATEMENT.txt, the-record-we-beat/RECORD.md and FETCH_LOG.txt, object/ (all parts). I did not run the claim's own checkers; every check below is my own code.

## Clause-by-clause reading

Main success criterion: requires max(n,m,p) <= 16. Here max = 25 > 16, so the main criterion is not met (and the claim does not claim it). Its other clauses (Perminov ranks.md, MerlijnW70) therefore do not apply.

Partial win p2: is about a GF(2)-only improvement for a format whose characteristic-0 rank is already at or below the new GF(2) rank. This scheme is over Q (rational coefficients, denominators up to 5994) and its rank is below every characteristic-0 value read, so p2 does not apply.

Partial win p1, phrase by phrase:
- "A new rank for a format with 17 <= max(n,m,p) <= 32": max = 25, inside 17..32. Met. "(outside Perminov's 16x16x16 table but inside the Lille catalogue)": the Lille index has a row for 24x25x25 (value 7507). Met.
- "an exactly verified scheme": I checked all Brent equations exactly myself (below). Met.
- "whose rank is strictly below the live fmm_sota.json entry": live entry for [24,25,25] is 7507; 7157 < 7507. Met.
- "and the live Lille per-format page for that format": live page https://fmm.univ-lille.fr/24x25x25.html shows 8176; 7157 < 8176. Met. (The Lille index row shows 7507; also above 7157.)
- "and not a plain composition already listed in the Lille 'construction' column": the index row's construction is "Proj([[25, 0], [0]], ⟨25×25×25:7507⟩ )" at rank 7507, the per-format page's decomposition is at rank 8176. The value 7157 is not listed anywhere in the index or the page for this format in any axis order, and the object is not a plain block sum, product or coordinate projection of listed schemes (the lowest such value in the tables and in matmulcatalog's projections is 7457, see the null model). Met.
- Hidden quantifiers: "live" is satisfied by my own fetch today (below), byte-identical to the claim's fetch. Ring: Q, exactly as claimed (the scheme is checked over Q). Counting convention: r = number of rank-one terms = 7157 lines in each of u, v, w, header rank 7157, no term has a zero factor (0), so r is the number of multiplications. Orientation: A is 24x25, B is 25x25, C = AB is 24x25, matching the file convention (m_k = (u_k.A)(v_k.B), C = sum w_k m_k); rank is invariant under permuting the format, and both tables index the sorted format [24,25,25].

Level met: p1.

## Live fetches (one plain GET each, curl, no retries, no cookies; times UTC)

| URL | UTC | HTTP | sha256 | value for 24x25x25 |
|---|---|---|---|---|
| https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (shared, as linked from claim/the-record-we-beat/RECORD.md) | 2026-10-25T09:09:45Z | 200 | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | 7507 |
| https://fmm.univ-lille.fr/ (shared) | 2026-10-25T09:09:46Z | 200 | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row 24x25x25: 7507 |
| https://fmm.univ-lille.fr/24x25x25.html | 2026-10-25T09:09:47Z | 200 | 84e2014de74b8ec465c7f47904fdfad2f143d2ddaa4ddd73672e2799f8a86fe1 | 8176 |
| https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json (shared) | 2026-10-25T09:09:56Z | 200 | 5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b | lowest 7457; no scheme listed at or below 7157 |
| https://api.github.com/repos/khoruzhii/lita/contents/schemes (shared) | 2026-10-25T09:18:10Z | 200 | 5d82d0309fc9e324dc3b49cfc6c45822b3e6482500983eb9f86c38666ac93b5d | 20 square schemes 13^3..32^3, no rectangular scheme |
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1..8 (shared, read-only) | 2026-10-25T09:16:24Z to 2026-10-25T09:16:30Z | all 200 | per page in my log | 705 pull requests (#1..#729): none names 24x25x25 in any axis order or notation; the number 7157 appears in none |

fmm_sota.json, the Lille index and the per-format page are byte-identical (same sha256) to the claim's own fetches in FETCH_LOG.txt, so the tables did not change since the claim was made. No fetch was blocked.

## Checks of the object

- Joined files (parts joined in numeric part order, my own code): sha256 u.txt 0dd8ee872815374dbea1c5ad46d2fa3d66b5513d5daf7e3deb924a7d11e146dc, v.txt 2fa3c110aee729212f67c643abcb3ea16e7ace02aa005b5ea9078c9ebc8455dd, w.txt 23207f290da58bb771cd3a713cf030e3916bb262c1fbd5db863eb04af2b7f42c; all three equal the values in CLAIM.md. Parts: u u.part1.txt+u.part2.txt+u.part3.txt; v v.part1.txt+v.part2.txt; w w.part1.txt+w.part2.txt; no other files in object/.
- Terms: r = 7157 (each factor file has 7157 term lines; header format 24 25 25, rank 7157); nonzeros u 398652, v 167772, w 152419; all indices in range; denominators occurring [1, 2, 4, 5, 9, 10, 18, 20, 37, 45, 180, 333, 666, 2997, 5994].
- Full Brent check, my own code (not the claim's checkers): all 225000000 equations ((n*m)*(m*p)*(n*p) = 225000000) checked exactly, 0 wrong. Method: each factor matrix scaled to integers by its least common denominator (U 59940, V 180, W 180; D = 1942056000), slabs over the sparsest factor (w), float64 products used only because a per-slab absolute bound (max 2106776870915760) proves every partial sum is an integer below 2^53; every slab compared with D times the matrix-multiplication tensor.
- Exact spot evaluation with Python Fractions on 2 random integer matrix pairs (entries uniform in [-10^6, 10^6], seed 7301): wrong entries of C [0, 0].
- Negative control of my checkers (on a scratch copy of the <20,20,21> object with one coefficient of one w term changed by 1): the direct and the modular Brent checks both reported 1032 wrong equations and the spot evaluation reported a wrong entry in both trials, so the checkers do detect a corrupted scheme.

## Null model and subsumption

- Block sums and products of listed schemes: a multi-step closure over the live fmm_sota.json (all 5456 entries, every format up to 32, additive splits along any axis, tensor products over all factorizations, restriction from any componentwise-larger listed format) gives 7507 for 24x25x25, equal to the table value (best single block sum or product alone: 7664, [24, 1, 25]+[24, 24, 25]=600+7064); the closure improves no fmm_sota entry anywhere, so the table already is its own closure. 7157 is 350 below it.
- Restriction of listed larger formats: the lowest fmm_sota entry for a format containing 24x25x25 componentwise is 7507 ([25, 25, 25]), above 7157. Plain coordinate projections of LITA's square schemes are what matmulcatalog lists (its lowest here: 7457), above 7157.
- How 7157 arises (the claim's provenance statement; I did not re-derive it, since LITA's .npz is not in claim/): one non-coordinate one-slice restriction of LITA's published <25,25,25> rank 7507 scheme, each followed by one exact 2-reduction. That is not a plain composition, block sum or coordinate projection, and in any case 7157 is not a listed value. The claim says the same method was used in V3R1T4S PRs #130, #164, #172 and #197, which my listing shows as merged (all for max dimension <= 16).
- Other listed formats or pull requests: no V3R1T4S pull request (open or closed) names this format; the closest are #708 and #714 (19-family, different formats). The sibling cell 24x24x25 of this batch is a different format and a separate claim; it is not a listed or published value, so it cannot subsume this cell.
- One object, one claim: the object defines one scheme for one format; nothing is bundled.
- Not covered by my checks: I did not re-fetch Perminov's or MerlijnW70's repositories (p1 does not name them; the claim reports both stop at dimension 16) and did no literature search beyond what the claim reports; "new" is therefore relative to the sources read.

confirmed_scope: The joined object files (sha256 u 0dd8ee872815..., v 2fa3c110aee7..., w 23207f290da5...) define a bilinear scheme over Q with exactly 7157 rank-one terms for <24,25,25> whose 225000000 Brent equations I verified exactly, and 7157 is strictly below both the live fmm_sota.json entry (7507) and the live Lille per-format page (8176) fetched 2026-10-25, is not a listed Lille construction, and is below every value for this format I found in those tables, the Lille index, matmulcatalog and the V3R1T4S pull requests, so it meets partial win p1 (not the main criterion).
pass: true
