context: subagent (Claude Opus 5.5, fresh context, given only a copy of claim/)

# Criterion skeptic: <26,26,27> rank 8437 (claimed level: partial win p1 of fmm-catalogue-small-format-rank)

Local material read: CLAIM.md, README.md, REPRODUCE.md, STATEMENT.txt, the-record-we-beat/RECORD.md and FETCH_LOG.txt, object/ (all parts). I did not run the claim's own checkers; every check below is my own code.

## Clause-by-clause reading

Main success criterion: requires max(n,m,p) <= 16. Here max = 27 > 16, so the main criterion is not met (and the claim does not claim it). Its other clauses (Perminov ranks.md, MerlijnW70) therefore do not apply.

Partial win p2: is about a GF(2)-only improvement for a format whose characteristic-0 rank is already at or below the new GF(2) rank. This scheme is over Q (rational coefficients, denominators up to 16400) and its rank is below every characteristic-0 value read, so p2 does not apply.

Partial win p1, phrase by phrase:
- "A new rank for a format with 17 <= max(n,m,p) <= 32": max = 27, inside 17..32. Met. "(outside Perminov's 16x16x16 table but inside the Lille catalogue)": the Lille index has a row for 26x26x27 (value 8727). Met.
- "an exactly verified scheme": I checked all Brent equations exactly myself (below). Met.
- "whose rank is strictly below the live fmm_sota.json entry": live entry for [26,26,27] is 8727; 8437 < 8727. Met.
- "and the live Lille per-format page for that format": live page https://fmm.univ-lille.fr/26x26x27.html shows 9334; 8437 < 9334. Met. (The Lille index row shows 8727; also above 8437.)
- "and not a plain composition already listed in the Lille 'construction' column": the index row's construction is "⟨26×26×1:676⟩ + ⟨26×26×26:8051⟩" at rank 8727, the per-format page's decomposition is at rank 9334. The value 8437 is not listed anywhere in the index or the page for this format in any axis order, and the object is not a plain block sum, product or coordinate projection of listed schemes (the lowest such value in the tables and in matmulcatalog's projections is 8727, see the null model). Met.
- Hidden quantifiers: "live" is satisfied by my own fetch today (below), byte-identical to the claim's fetch. Ring: Q, exactly as claimed (the scheme is checked over Q). Counting convention: r = number of rank-one terms = 8437 lines in each of u, v, w, header rank 8437, no term has a zero factor (0), so r is the number of multiplications. Orientation: A is 26x26, B is 26x27, C = AB is 26x27, matching the file convention (m_k = (u_k.A)(v_k.B), C = sum w_k m_k); rank is invariant under permuting the format, and both tables index the sorted format [26,26,27].

Level met: p1.

## Live fetches (one plain GET each, curl, no retries, no cookies; times UTC)

| URL | UTC | HTTP | sha256 | value for 26x26x27 |
|---|---|---|---|---|
| https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (shared, as linked from claim/the-record-we-beat/RECORD.md) | 2026-10-25T09:09:45Z | 200 | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | 8727 |
| https://fmm.univ-lille.fr/ (shared) | 2026-10-25T09:09:46Z | 200 | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row 26x26x27: 8727 |
| https://fmm.univ-lille.fr/26x26x27.html | 2026-10-25T09:09:48Z | 200 | 8b91ca55699d8495eb5ab9bbdf30f061fa4d7c1606fd1f32d41fd01ec984c724 | 9334 |
| https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json (shared) | 2026-10-25T09:09:56Z | 200 | 5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b | lowest 8727; no scheme listed at or below 8437 |
| https://api.github.com/repos/khoruzhii/lita/contents/schemes (shared) | 2026-10-25T09:18:10Z | 200 | 5d82d0309fc9e324dc3b49cfc6c45822b3e6482500983eb9f86c38666ac93b5d | 20 square schemes 13^3..32^3, no rectangular scheme |
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1..8 (shared, read-only) | 2026-10-25T09:16:24Z to 2026-10-25T09:16:30Z | all 200 | per page in my log | 705 pull requests (#1..#729): none names 26x26x27 in any axis order or notation; the number 8437 appears in none |

fmm_sota.json, the Lille index and the per-format page are byte-identical (same sha256) to the claim's own fetches in FETCH_LOG.txt, so the tables did not change since the claim was made. No fetch was blocked.

## Checks of the object

- Joined files (parts joined in numeric part order, my own code): sha256 u.txt 1d6c9f89e17717b7236f9bbbf46d6903e95f66a3965445cd8194bc23bd065d58, v.txt bdcfa626ff98644b132c75ac00deebb2b9cb922116b7b44e00e63d2238f5da5a, w.txt 9192310639d1141ba525574fac6735b5ce0507711ac0c8989a1f049b221aa48e; all three equal the values in CLAIM.md. Parts: u u.part1.txt+u.part2.txt+u.part3.txt; v v.part1.txt+v.part2.txt+v.part3.txt+v.part4.txt; w w.part1.txt+w.part2.txt; no other files in object/.
- Terms: r = 8437 (each factor file has 8437 term lines; header format 26 26 27, rank 8437); nonzeros u 352891, v 522808, w 190241; all indices in range; denominators occurring [1, 2, 4, 11, 20, 22, 41, 44, 82, 220, 820, 1640, 16400].
- Full Brent check, my own code (not the claim's checkers): all 333135504 equations ((n*m)*(m*p)*(n*p) = 333135504) checked exactly, 0 wrong. The direct float64-exact route did not apply (per-slab absolute bound above 2^53), so I checked every equation modulo four primes near 2^20 (1048573, 1048571, 1048559, 1048549; each slab sum stays below 2^53, so each modular product is exact) and used the absolute bound (max |entry| <= 38083981230416000, plus D = 8731360000) being below half the product of the primes, so agreement modulo all four primes implies equality over Z, hence over Q after dividing by D. LCDs U 180400, V 220, W 220.
- Exact spot evaluation with Python Fractions on 2 random integer matrix pairs (entries uniform in [-10^6, 10^6], seed 7301): wrong entries of C [0, 0].
- Negative control of my checkers (on a scratch copy of the <20,20,21> object with one coefficient of one w term changed by 1): the direct and the modular Brent checks both reported 1032 wrong equations and the spot evaluation reported a wrong entry in both trials, so the checkers do detect a corrupted scheme.

## Null model and subsumption

- Block sums and products of listed schemes: a multi-step closure over the live fmm_sota.json (all 5456 entries, every format up to 32, additive splits along any axis, tensor products over all factorizations, restriction from any componentwise-larger listed format) gives 8727 for 26x26x27, equal to the table value (best single block sum or product alone: 8727, [26, 26, 1]+[26, 26, 26]=676+8051); the closure improves no fmm_sota entry anywhere, so the table already is its own closure. 8437 is 290 below it.
- Restriction of listed larger formats: the lowest fmm_sota entry for a format containing 26x26x27 componentwise is 9078 ([26, 26, 28]), above 8437. Plain coordinate projections of LITA's square schemes are what matmulcatalog lists (its lowest here: 8727), above 8437.
- How 8437 arises (the claim's provenance statement; I did not re-derive it, since LITA's .npz is not in claim/): two non-coordinate one-slice restrictions of LITA's published <27,27,27> rank 9233 scheme, each followed by one exact 2-reduction. That is not a plain composition, block sum or coordinate projection, and in any case 8437 is not a listed value. The claim says the same method was used in V3R1T4S PRs #130, #164, #172 and #197, which my listing shows as merged (all for max dimension <= 16).
- Other listed formats or pull requests: no V3R1T4S pull request (open or closed) names this format; the closest are #708 and #714 (19-family, different formats). The sibling cell 26x27x27 of this batch is a different format and a separate claim; it is not a listed or published value, so it cannot subsume this cell, and this cell is a further restriction of it: my own count over every single-coordinate deletion of the sibling object (both size-27 axes) gives at best 8775 terms, above 8437 (the README says 8787; my lower 8775 comes from deleting a column of B and C, and either way it is above 8437).
- One object, one claim: the object defines one scheme for one format; nothing is bundled.
- Not covered by my checks: I did not re-fetch Perminov's or MerlijnW70's repositories (p1 does not name them; the claim reports both stop at dimension 16) and did no literature search beyond what the claim reports; "new" is therefore relative to the sources read.

confirmed_scope: The joined object files (sha256 u 1d6c9f89e177..., v bdcfa626ff98..., w 9192310639d1...) define a bilinear scheme over Q with exactly 8437 rank-one terms for <26,26,27> whose 333135504 Brent equations I verified exactly, and 8437 is strictly below both the live fmm_sota.json entry (8727) and the live Lille per-format page (9334) fetched 2026-10-25, is not a listed Lille construction, and is below every value for this format I found in those tables, the Lille index, matmulcatalog and the V3R1T4S pull requests, so it meets partial win p1 (not the main criterion).
pass: true
