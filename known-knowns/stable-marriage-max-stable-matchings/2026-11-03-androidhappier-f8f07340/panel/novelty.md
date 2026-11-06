# Panel: NOVELTY skeptic: stable-marriage-max-stable-matchings, n = 9
context: subagent (executor NOVELTY)
inputs: a read-only copy of claim/ (CLAIM.md, TABLE.md, REPRODUCE.md, instance_n9.prefs, data/, programs/, closure_probe/) plus the live fetches below. I did not read attempts/, NOTES, REPORT or the other panel files.

## Claim under test
claim/instance_n9.prefs (sha256 f8f0734081c8c613267257d617d9393d5ad591782b802beaa72c8b1639f35de1, re-hashed by me and matching) has 412 stable matchings at n = 9. CLAIM.md says it is not a composition: it was found by local search seeded from the Z2^3 Latin order-8 instance (268 stable matchings) plus one pair.
My recount on a scratch copy gave `./allperm instance_n9.prefs` -> 412 and `count_stable.py --brute` -> lattice 412, brute 412, agree.

## Primary status fetches (one honest fetch each, all at 2026-11-03T17:35:48Z = 12:35:48 PM EST, no retries)
| URL | HTTP | sha256 | n = 9 value |
|---|---|---|---|
| https://oeis.org/A357271 | 200 | 3e3019ee8dc2cdcc211e3266b8bf3dae280029ca58fc0f1c4d41d2b1925987a9 (HTML; dynamic page, data line unchanged) | 330 (data line `...,268,330,1000,...`) |
| https://oeis.org/search?q=id:A357271&fmt=text | 200 | fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143 | 330; %C says "Improved lower bounds for n=7, 9, 11, 13, 15 are shown in linked Ong et al. (2025) file" |
| https://oeis.org/A357271/a357271_1.txt | 200 | 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47 (byte-identical to claim/data/a357271_1.txt) | "lb(9)=365 (previously 330)", "order 9 example with 365 SM" |
| https://oeis.org/search?q=id:A357269&fmt=text | 200 | 21f555dbd8d899ff... | exact only to n=5 (1,2,3,10,16) |
| https://oeis.org/search?q=id:A371810&fmt=text | 200 | fb71c17c72ac94a4... | 288 |
| https://oeis.org/search?q=id:A069156&fmt=text | 200 | a0b564cfb51317f9... | 330 |
| https://zenodo.org/api/records/23329599 (+ F7_MANUSCRIPT.pdf, sha256 bf9dddd8...) | 200 / 200 | | M. Jo, "A computer-assisted proof that the maximum number of stable matchings of order seven is 85" (2026-10-13): order 7 only, with no order-8/9 value in the text |

Recounts I ran on published bars with the claim's programs: Ong n=9 (data/ong_n9.prefs) is 365, Ong n=7 is 81, Jo n=7 (data/jo_n7.prefs) is 85, and Z2^3 Latin n=8 is 268.

## Literature and code (last 24 months)
- WebSearch (2026-11-03): searched for order-9 maximum stable matchings, arXiv lower bounds and GitHub n=9 instances. The only n=9 value I found was Ong et al. 365 (OEIS file / IFoRE 2024 poster). Nothing reports 366 or more at n=9. The arXiv API query (export.arxiv.org) returned HTTP 500 once and I did not retry it. Web search showed no recent arXiv paper with an order-9 instance.
- Repo (`known-knowns/`, HEAD 9a0d19a1, same as origin after a fetch): `known-knowns/stable-marriage-max-stable-matchings/` holds only n=15 (two packages) and n=13 entries. The only n=9 mentions are recounts of Ong's 365. TROPHY_CASE.md has no stable-marriage row.
- PRs (public GitHub search API, 2026-11-03T17:36Z = 12:36 PM EST): "stable-marriage" and "A357271" each return 14 PRs, open and closed, for n = 13, 14, 15, 17, 18, 19, 21, 22, 23 and 28 only. None is an n=9 instance. PR #147 (closed, unmerged) is K2 doubling of Ong's 365 at n=18 and is not an n=9 object. A third query ("stable matchings") hit the rate limit. `gh` is not authenticated.

## Composition closure at n = 9 (could a composition of published parts reach 412 or more?)
Published parts by order: 1:1, 2:2, 3:3, 4:10, 5:16, 6:48, 7:85 (Jo; Ong 81), 8:268.
- Disjoint unions: the best is 8+1 = 268. Others: 7+2 = 170, 5+4 = 160, 6+3 = 144.
- Lexicographic product 3x3: Z3xZ3 Latin gives 93. 1500 random pairs drawn from all 1092 order-3 instances with 3 stable matchings gave at most 111.
- Thurber compositions: A357271(9) and A069156(9) = 330.
- Block sums with each published block's internal order frozen and only the cross-block placements hill-climbed (claim/closure_probe/blocksum.py). I ran this myself: Z2^3(8)+K1 with 8 seeds (150-420 s each) gave at most **378** (two seeds; I recounted 378 with allperm). Jo7+K2 gave at most 252, Ong7+K2 at most 248, lat6+C3 at most 240, and f5+K4 at most 333. The claim's own saved probe bs_8_1.prefs counts 366.
So the strongest closure-style bar I could build or verify is 378. That already beats Ong's 365, so 365 alone is not the real bar. 412 still beats 378 by 34.

## Trivial-edit test
The object is not a relabelling of Ong's instance (365 versus 412). It is also not reachable as a frozen-block placement around the 268 seed: that search tops out at 378 in my runs. CLAIM.md says 5 of the 16 old lists changed their internal order, which is a real edit of the seed and not a trivial one.

## Caveats
Hill climbing only gives lower bounds, so the "composition closure" here is the best I found and not a proven maximum over all compositions. The PR search was partial: two queries succeeded and the third was rate-limited.

## Verdict
novelty: 412 strictly beats every n=9 value I could find. Published values: Ong 365, A357271 / A069156 330, A371810 288. Repo / PRs: none at n=9. Compositions: at most 378 from frozen-block block sums, 268 from disjoint unions, about 111 from 3x3 products and 330 from Thurber. The result is not a tie.
pass: true
