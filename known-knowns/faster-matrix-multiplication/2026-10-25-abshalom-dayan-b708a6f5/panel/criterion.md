context: subagent (Claude Opus 5.5, fresh context, given only a copy of claim/)

# Criterion skeptic: <28,28,29> rank 10290 (claimed level: partial win p1 of fmm-catalogue-small-format-rank)

Local material read: CLAIM.md, README.md, REPRODUCE.md, STATEMENT.txt, the-record-we-beat/RECORD.md and FETCH_LOG.txt, object/ (all parts). I did not run the claim's own checkers; every check below is my own code.

## Clause-by-clause reading

Main success criterion: requires max(n,m,p) <= 16. Here max = 29 > 16, so the main criterion is not met (and the claim does not claim it). Its other clauses (Perminov ranks.md, MerlijnW70) therefore do not apply.

Partial win p2: is about a GF(2)-only improvement for a format whose characteristic-0 rank is already at or below the new GF(2) rank. This scheme is over Q (rational coefficients, denominators up to 1815) and its rank is below every characteristic-0 value read, so p2 does not apply.

Partial win p1, phrase by phrase:
- "A new rank for a format with 17 <= max(n,m,p) <= 32": max = 29, inside 17..32. Met. "(outside Perminov's 16x16x16 table but inside the Lille catalogue)": the Lille index has a row for 28x28x29 (value 10630). Met.
- "an exactly verified scheme": I checked all Brent equations exactly myself (below). Met.
- "whose rank is strictly below the live fmm_sota.json entry": live entry for [28,28,29] is 10630; 10290 < 10630. Met.
- "and the live Lille per-format page for that format": live page https://fmm.univ-lille.fr/28x28x29.html shows 11340; 10290 < 11340. Met. (The Lille index row shows 10630; also above 10290.)
- "and not a plain composition already listed in the Lille 'construction' column": the index row's construction is "⟨28×28×1:784⟩ + ⟨28×28×28:9846⟩" at rank 10630, the per-format page's decomposition is at rank 11340. The value 10290 is not listed anywhere in the index or the page for this format in any axis order, and the object is not a plain block sum, product or coordinate projection of listed schemes (the lowest such value in the tables and in matmulcatalog's projections is 10630, see the null model). Met.
- Hidden quantifiers: "live" is satisfied by my own fetch today (below), byte-identical to the claim's fetch. Ring: Q, exactly as claimed (the scheme is checked over Q). Counting convention: r = number of rank-one terms = 10290 lines in each of u, v, w, header rank 10290, no term has a zero factor (0), so r is the number of multiplications. Orientation: A is 28x28, B is 28x29, C = AB is 28x29, matching the file convention (m_k = (u_k.A)(v_k.B), C = sum w_k m_k); rank is invariant under permuting the format, and both tables index the sorted format [28,28,29].

Level met: p1.

## Live fetches (one plain GET each, curl, no retries, no cookies; times UTC)

| URL | UTC | HTTP | sha256 | value for 28x28x29 |
|---|---|---|---|---|
| https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (shared, as linked from claim/the-record-we-beat/RECORD.md) | 2026-10-25T09:09:45Z | 200 | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | 10630 |
| https://fmm.univ-lille.fr/ (shared) | 2026-10-25T09:09:46Z | 200 | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row 28x28x29: 10630 |
| https://fmm.univ-lille.fr/28x28x29.html | 2026-10-25T09:09:48Z | 200 | 26cf02b4423bad2284a683b1397d45c79114c89cbb3cf69bbe14c7926c11ee89 | 11340 |
| https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json (shared) | 2026-10-25T09:09:56Z | 200 | 5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b | lowest 10630; no scheme listed at or below 10290 |
| https://api.github.com/repos/khoruzhii/lita/contents/schemes (shared) | 2026-10-25T09:18:10Z | 200 | 5d82d0309fc9e324dc3b49cfc6c45822b3e6482500983eb9f86c38666ac93b5d | 20 square schemes 13^3..32^3, no rectangular scheme |
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1..8 (shared, read-only) | 2026-10-25T09:16:24Z to 2026-10-25T09:16:30Z | all 200 | per page in my log | 705 pull requests (#1..#729): none names 28x28x29 in any axis order or notation; the number 10290 appears in none |

fmm_sota.json, the Lille index and the per-format page are byte-identical (same sha256) to the claim's own fetches in FETCH_LOG.txt, so the tables did not change since the claim was made. No fetch was blocked.

## Checks of the object

- Joined files (parts joined in numeric part order, my own code): sha256 u.txt b708a6f57581908dc2930065758f6beaa1d52eb9fb3cde062330fb964ea2c278, v.txt b84fdd470305ab0ba69f5d01b3488646517344b4f47e47028d32658e8d3c8037, w.txt 27aa43deb60a92f30aa99ed4c0d205a40d84cabace9c910141a6894dfee397c4; all three equal the values in CLAIM.md. Parts: u u.part1.txt+u.part2.txt+u.part3.txt+u.part4.txt; v v.part1.txt+v.part2.txt+v.part3.txt+v.part4.txt+v.part5.txt+v.part6.txt; w w.part1.txt+w.part2.txt; no other files in object/.
- Terms: r = 10290 (each factor file has 10290 term lines; header format 28 28 29, rank 10290); nonzeros u 454709, v 680338, w 236938; all indices in range; denominators occurring [1, 2, 3, 4, 5, 6, 8, 11, 12, 15, 22, 24, 44, 55, 66, 132, 165, 264, 605, 1815].
- Full Brent check, my own code (not the claim's checkers): all 516925696 equations ((n*m)*(m*p)*(n*p) = 516925696) checked exactly, 0 wrong. Method: each factor matrix scaled to integers by its least common denominator (U 14520, V 264, W 264; D = 1011985920), slabs over the sparsest factor (w), float64 products used only because a per-slab absolute bound (max 6770098982903344) proves every partial sum is an integer below 2^53; every slab compared with D times the matrix-multiplication tensor.
- Exact spot evaluation with Python Fractions on 2 random integer matrix pairs (entries uniform in [-10^6, 10^6], seed 7301): wrong entries of C [0, 0].
- Negative control of my checkers (on a scratch copy of the <20,20,21> object with one coefficient of one w term changed by 1): the direct and the modular Brent checks both reported 1032 wrong equations and the spot evaluation reported a wrong entry in both trials, so the checkers do detect a corrupted scheme.

## Null model and subsumption

- Block sums and products of listed schemes: a multi-step closure over the live fmm_sota.json (all 5456 entries, every format up to 32, additive splits along any axis, tensor products over all factorizations, restriction from any componentwise-larger listed format) gives 10630 for 28x28x29, equal to the table value (best single block sum or product alone: 10630, [28, 28, 1]+[28, 28, 28]=784+9846); the closure improves no fmm_sota entry anywhere, so the table already is its own closure. 10290 is 340 below it.
- Restriction of listed larger formats: the lowest fmm_sota entry for a format containing 28x28x29 componentwise is 11036 ([28, 28, 30]), above 10290. Plain coordinate projections of LITA's square schemes are what matmulcatalog lists (its lowest here: 10630), above 10290.
- How 10290 arises (the claim's provenance statement; I did not re-derive it, since LITA's .npz is not in claim/): two non-coordinate one-slice restrictions of LITA's published <29,29,29> rank 11203 scheme, each followed by one exact 2-reduction. That is not a plain composition, block sum or coordinate projection, and in any case 10290 is not a listed value. The claim says the same method was used in V3R1T4S PRs #130, #164, #172 and #197, which my listing shows as merged (all for max dimension <= 16).
- Other listed formats or pull requests: no V3R1T4S pull request (open or closed) names this format; the closest are #708 and #714 (19-family, different formats). The sibling cell 28x29x29 of this batch is a different format and a separate claim; it is not a listed or published value, so it cannot subsume this cell, and this cell is a further restriction of it: my own count over every single-coordinate deletion of the sibling object (both size-29 axes) gives at best 10682 terms, above 10290 (the README says 10695; my lower 10682 comes from deleting a column of B and C, and either way it is above 10290).
- One object, one claim: the object defines one scheme for one format; nothing is bundled.
- Not covered by my checks: I did not re-fetch Perminov's or MerlijnW70's repositories (p1 does not name them; the claim reports both stop at dimension 16) and did no literature search beyond what the claim reports; "new" is therefore relative to the sources read.

confirmed_scope: The joined object files (sha256 u b708a6f57581..., v b84fdd470305..., w 27aa43deb60a...) define a bilinear scheme over Q with exactly 10290 rank-one terms for <28,28,29> whose 516925696 Brent equations I verified exactly, and 10290 is strictly below both the live fmm_sota.json entry (10630) and the live Lille per-format page (11340) fetched 2026-10-25, is not a listed Lille construction, and is below every value for this format I found in those tables, the Lille index, matmulcatalog and the V3R1T4S pull requests, so it meets partial win p1 (not the main criterion).
pass: true
