context: subagent (Claude Opus 5.5, fresh context, given only a copy of claim/)

# Criterion skeptic: <30,31,31> rank 12906 (claimed level: partial win p1 of fmm-catalogue-small-format-rank)

Local material read: CLAIM.md, README.md, REPRODUCE.md, STATEMENT.txt, the-record-we-beat/RECORD.md and FETCH_LOG.txt, object/ (all parts). I did not run the claim's own checkers; every check below is my own code.

## Clause-by-clause reading

Main success criterion: requires max(n,m,p) <= 16. Here max = 31 > 16, so the main criterion is not met (and the claim does not claim it). Its other clauses (Perminov ranks.md, MerlijnW70) therefore do not apply.

Partial win p2: is about a GF(2)-only improvement for a format whose characteristic-0 rank is already at or below the new GF(2) rank. This scheme is over Q (rational coefficients, denominators up to 28224) and its rank is below every characteristic-0 value read, so p2 does not apply.

Partial win p1, phrase by phrase:
- "A new rank for a format with 17 <= max(n,m,p) <= 32": max = 31, inside 17..32. Met. "(outside Perminov's 16x16x16 table but inside the Lille catalogue)": the Lille index has a row for 30x31x31 (value 13433). Met.
- "an exactly verified scheme": I checked all Brent equations exactly myself (below). Met.
- "whose rank is strictly below the live fmm_sota.json entry": live entry for [30,31,31] is 13433; 12906 < 13433. Met.
- "and the live Lille per-format page for that format": live page https://fmm.univ-lille.fr/30x31x31.html shows 14540; 12906 < 14540. Met. (The Lille index row shows 13433; also above 12906.)
- "and not a plain composition already listed in the Lille 'construction' column": the index row's construction is "Proj([[31, 0], [0]], ⟨31×31×31:13433⟩ )" at rank 13433, the per-format page's decomposition is at rank 14540. The value 12906 is not listed anywhere in the index or the page for this format in any axis order, and the object is not a plain block sum, product or coordinate projection of listed schemes (the lowest such value in the tables and in matmulcatalog's projections is 13371, see the null model). Met.
- Hidden quantifiers: "live" is satisfied by my own fetch today (below), byte-identical to the claim's fetch. Ring: Q, exactly as claimed (the scheme is checked over Q). Counting convention: r = number of rank-one terms = 12906 lines in each of u, v, w, header rank 12906, no term has a zero factor (0), so r is the number of multiplications. Orientation: A is 30x31, B is 31x31, C = AB is 30x31, matching the file convention (m_k = (u_k.A)(v_k.B), C = sum w_k m_k); rank is invariant under permuting the format, and both tables index the sorted format [30,31,31].

Level met: p1.

## Live fetches (one plain GET each, curl, no retries, no cookies; times UTC)

| URL | UTC | HTTP | sha256 | value for 30x31x31 |
|---|---|---|---|---|
| https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (shared, as linked from claim/the-record-we-beat/RECORD.md) | 2026-10-25T09:09:45Z | 200 | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | 13433 |
| https://fmm.univ-lille.fr/ (shared) | 2026-10-25T09:09:46Z | 200 | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row 30x31x31: 13433 |
| https://fmm.univ-lille.fr/30x31x31.html | 2026-10-25T09:09:49Z | 200 | 4f3c4514c3af46f2504abab2b1143d5f325a4a5de48dbb40c903267c363ebe75 | 14540 |
| https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json (shared) | 2026-10-25T09:09:56Z | 200 | 5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b | lowest 13371; no scheme listed at or below 12906 |
| https://api.github.com/repos/khoruzhii/lita/contents/schemes (shared) | 2026-10-25T09:18:10Z | 200 | 5d82d0309fc9e324dc3b49cfc6c45822b3e6482500983eb9f86c38666ac93b5d | 20 square schemes 13^3..32^3, no rectangular scheme |
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1..8 (shared, read-only) | 2026-10-25T09:16:24Z to 2026-10-25T09:16:30Z | all 200 | per page in my log | 705 pull requests (#1..#729): none names 30x31x31 in any axis order or notation; the number 12906 appears in none |

fmm_sota.json, the Lille index and the per-format page are byte-identical (same sha256) to the claim's own fetches in FETCH_LOG.txt, so the tables did not change since the claim was made. No fetch was blocked.

## Checks of the object

- Joined files (parts joined in numeric part order, my own code): sha256 u.txt 1570401161925e32961aa2ad3cb58ac6c66b38b3e804fac3e9d7a195405da245, v.txt ccae23a2fc6350bf299bfbf6b5df8ebab898741535a56a983e2285f681efcb3d, w.txt cfb52c03a37acf0d7c85b66db919ec6dcd32ef47203ac183c59a577426eabb42; all three equal the values in CLAIM.md. Parts: u u.part1.txt+u.part2.txt+u.part3.txt+u.part4.txt+u.part5.txt+u.part6.txt+u.part7.txt; v v.part1.txt+v.part2.txt+v.part3.txt; w w.part1.txt+w.part2.txt+w.part3.txt; no other files in object/.
- Terms: r = 12906 (each factor file has 12906 term lines; header format 30 31 31, rank 12906); nonzeros u 877795, v 321688, w 294303; all indices in range; denominators occurring [1, 2, 4, 7, 13, 14, 24, 26, 49, 52, 98, 312, 1176, 2352, 28224].
- Full Brent check, my own code (not the claim's checkers): all 831168900 equations ((n*m)*(m*p)*(n*p) = 831168900) checked exactly, 0 wrong. The direct float64-exact route did not apply (per-slab absolute bound above 2^53), so I checked every equation modulo four primes near 2^20 (1048573, 1048571, 1048559, 1048549; each slab sum stays below 2^53, so each modular product is exact) and used the absolute bound (max |entry| <= 113620384482628608, plus D = 35716681728) being below half the product of the primes, so agreement modulo all four primes implies equality over Z, hence over Q after dividing by D. LCDs U 366912, V 312, W 312.
- Exact spot evaluation with Python Fractions on 2 random integer matrix pairs (entries uniform in [-10^6, 10^6], seed 7301): wrong entries of C [0, 0].
- Negative control of my checkers (on a scratch copy of the <20,20,21> object with one coefficient of one w term changed by 1): the direct and the modular Brent checks both reported 1032 wrong equations and the spot evaluation reported a wrong entry in both trials, so the checkers do detect a corrupted scheme.

## Null model and subsumption

- Block sums and products of listed schemes: a multi-step closure over the live fmm_sota.json (all 5456 entries, every format up to 32, additive splits along any axis, tensor products over all factorizations, restriction from any componentwise-larger listed format) gives 13433 for 30x31x31, equal to the table value (best single block sum or product alone: 13719, [30, 1, 31]+[30, 30, 31]=930+12789); the closure improves no fmm_sota entry anywhere, so the table already is its own closure. 12906 is 527 below it.
- Restriction of listed larger formats: the lowest fmm_sota entry for a format containing 30x31x31 componentwise is 13433 ([31, 31, 31]), above 12906. Plain coordinate projections of LITA's square schemes are what matmulcatalog lists (its lowest here: 13371), above 12906.
- How 12906 arises (the claim's provenance statement; I did not re-derive it, since LITA's .npz is not in claim/): one non-coordinate one-slice restriction of LITA's published <31,31,31> rank 13433 scheme, each followed by one exact 2-reduction. That is not a plain composition, block sum or coordinate projection, and in any case 12906 is not a listed value. The claim says the same method was used in V3R1T4S PRs #130, #164, #172 and #197, which my listing shows as merged (all for max dimension <= 16).
- Other listed formats or pull requests: no V3R1T4S pull request (open or closed) names this format; the closest are #708 and #714 (19-family, different formats). The sibling cell 30x30x31 of this batch is a different format and a separate claim; it is not a listed or published value, so it cannot subsume this cell.
- One object, one claim: the object defines one scheme for one format; nothing is bundled.
- Not covered by my checks: I did not re-fetch Perminov's or MerlijnW70's repositories (p1 does not name them; the claim reports both stop at dimension 16) and did no literature search beyond what the claim reports; "new" is therefore relative to the sources read.

confirmed_scope: The joined object files (sha256 u 157040116192..., v ccae23a2fc63..., w cfb52c03a37a...) define a bilinear scheme over Q with exactly 12906 rank-one terms for <30,31,31> whose 831168900 Brent equations I verified exactly, and 12906 is strictly below both the live fmm_sota.json entry (13433) and the live Lille per-format page (14540) fetched 2026-10-25, is not a listed Lille construction, and is below every value for this format I found in those tables, the Lille index, matmulcatalog and the V3R1T4S pull requests, so it meets partial win p1 (not the main criterion).
pass: true
