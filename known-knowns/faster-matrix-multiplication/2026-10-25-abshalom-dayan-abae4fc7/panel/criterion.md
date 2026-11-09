context: subagent (Claude Opus 5.5, fresh context, given only a copy of claim/)

# Criterion skeptic: <14,14,15> rank 1709 over Q (target fmm-catalogue-small-format-rank, main criterion)

## Clause-by-clause reading of the success criterion

| clause (verbatim fragment) | reading | met? |
|---|---|---|
| "an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms)" | object/u.txt, v.txt, w.txt: one line per term with the nonzero entries of each factor; 1709 lines each, no empty factor. That is an explicit list of rank-one terms. | yes |
| "for a format <n,m,p> with max(n,m,p) <= 16" | headers of all three files say `# format 14 14 15`; max = 15. | yes |
| "sorted(n,m,p) not in {(3,3,3),(4,4,4)}" | sorted (14,14,15). | yes |
| "number of rank-one terms r is STRICTLY LESS ... than ALL of" four sources | r = 1709 (counted by me). Live values below: 1789, 1798, min(1798,1798,1790)=1790, none. 1709 < 1789 <= every listed value. | yes |
| "the rank listed for the sorted format in .../fmm_sota.json" | entry {"format": [14, 14, 15], "rank": 1789}; createdAt 2026-10-19T20:46:33. | 1709 < 1789 |
| "the rank on https://fmm.univ-lille.fr/{n}x{m}x{p}.html" | fetched https://fmm.univ-lille.fr/14x14x15.html (the criterion's template filled with the claimed orientation, which is already the sorted one): heading "<14x14x15:1798>", algorithm taken from Perminov's repository. | 1709 < 1798 |
| "the minimum over the ZT/Z/Q columns ... in .../docs/ranks.md" | row `14x14x15` under header Format / ZT / Z / Q / omega: ZT 1798, Z 1798, Q 1790 (bracketed previous-best values 1813 are not column values; counting them would not change the minimum). No row for 14x15x14 or 15x14x14. Minimum 1790. | 1709 < 1790 |
| "the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes" | the repository page README tables list no 14x14x15 (or permutation) entry; the full tree (API, not truncated, 39 paths, 31 scheme files) has none either. No value exists, so the clause has nothing to beat. Hidden quantifier noted: "beats the minimum over all four" is then the minimum over the three sources that list the format, 1789. | yes (vacuous for this source) |
| "every one re-fetched live immediately before claiming" | I re-fetched all four just now (table below): three bodies are byte-identical to the claim's 07:03-07:05Z fetches; the github.com HTML page differs in bytes (dynamic HTML) but still lists no <14,14,15>. Values unchanged. The filing step must still re-fetch right before it files; my fetches are ~3 h after the claim's. | yes, as of 10:13Z |
| "verified in exact arithmetic ... over the ring it claims" | claimed ring Q; all coefficients are integers or p/q fractions. I verified exactly (see Checks): all Brent equations via a CRT proof over four primes, plus exact Fraction evaluation. | yes |
| GF(2) clause | does not apply: the scheme claims Q, not GF(2)-only; it has denominators 2, 4, 8, ... so it is not even defined mod 2. | n/a |
| "composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed" | the exclusion is conditional on the rank equalling a listed value. 1709 is listed in none of the four sources (nor in matmulcatalog per the claim's record, nor in any V3R1T4S pull request). So the exclusion cannot apply whatever the derivation is called. The derivation (one-slice restrictions of LITA's public <15,15,15> rank-1977 scheme plus exact linear-dependency term elimination) is in any case not a composition, padding or block-splitting. | not excluded |
| "Ternary/integer re-derivations of a rank already attained over Q are NOT this target" | 1709 is a new rank, not a ring upgrade of an attained rank. | not excluded |
| "fewer additions at an existing rank is NOT this target" | the rank itself is new. | not excluded |

Partial wins: p1 needs 17 <= max <= 32, so it does not apply (max = 15); p2 is GF(2)-only and does not apply. The claim is for the main criterion only.

## Live fetches (one plain GET each, curl, User-Agent "V3R1T4S-criterion-skeptic (single GET)", no cookies, no retries)

| UTC | HTTP | URL | sha256 of body | value for <14,14,15> |
|---|---|---|---|---|
| 2026-10-25T10:13:20Z | 200 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae (same as claim) | 1789 |
| 2026-10-25T10:13:20Z | 200 | https://fmm.univ-lille.fr/14x14x15.html (Last-Modified Wed, 10 Jun 2026 10:22:10 GMT) | 63ce18bf1085d0f315839876c397d7ff9bfe725fa5fd998883f382a14e6b907a (same as claim) | 1798 |
| 2026-10-25T10:13:20Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a (same as claim) | ZT 1798, Z 1798, Q 1790; min 1790 |
| 2026-10-25T10:13:20Z | 200 | https://github.com/MerlijnW70/fmm-schemes | 703ab8974c6d8b4b5e505df8bbb489c4a865bb025871da26f18a49818c281af8 | no <14,14,15> in any orientation |
| 2026-10-25T10:13:50Z | 200 | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | e6866337cf18c6f4bb9d2b950240341d901260e28b560a301853202c03b1a5fc (same as claim) | truncated false, 39 paths, no 14x14x15 / 14x15x14 / 15x14x14 |

No source blocked; no 401/403/429 or bot check. Live bar = min(1789, 1798, 1790, none) = 1789.

Repository check (read-only GitHub API, elder-plinius/V3R1T4S):
- all pull requests, state=all, 8 pages of 100 (10:13:50Z-10:14:08Z, all HTTP 200, 711 PRs): scanned titles and bodies for 14x14x15, 14x15x14, 15x14x14 (separators x, ×, comma, spaces). Hits: #6 "(14, 14, 15) rank 1715 over Q", closed, not merged; #399 a bank update quoting the 1790 -> 1789 bar. No PR title or body contains the number 1709 at all. No open or closed PR has <14,14,15> at rank <= 1709 in any orientation.
- search https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:pr+14x14x15&per_page=100 (10:13:51Z, 200, sha256 0d5a7f52...cf5520, same as claim): 1 result, #6.
- search ...+fmm-catalogue-small-format-rank (10:13:52Z, 200, sha256 61185fc1...e0ca7, same as claim).
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md (10:14:17Z, 200, sha256 b946f68e...1a1, same as claim): entry 47 "<14,14,15> rank 1716 over Q", merged known-knowns. 1709 is 7 below it.

## Checks on the object (my own scripts, Python -I, stdlib + local numpy)

- sha256 of object/u.txt, v.txt, w.txt match CLAIM.md/REPRODUCE.md exactly (abae4fc7..., a05bcf35..., 041992e8...).
- 1709 data lines in each file, headers `# format 14 14 15`, `# rank 1709`; every coefficient matches `-?\d+(/\d+)?` and is nonzero; indices in range, no duplicates; no empty factor. All coefficients rational, so the scheme is over Q. Denominators exactly the 35 listed in CLAIM.md; lcm 212160. (check_scheme.py prints "common denominator 2121600": that is its lcm of per-term denominator products, a different quantity, not an inconsistency.)
- Exact evaluation: 3 random integer pairs (entries in [-50,50]) evaluated with fractions.Fraction: 0 of 210 entries of C differ from AB in each. 10 random pairs mod 2^61-1: 0 mismatches.
- Full Brent check (all 196*210*210 = 8,643,600 equations), my own method: the integer tensor X = L^3 (T_scheme - T_true), L = 212160, has |entries| < 2^71 (bound sum_k max|Lu_k| max|Lv_k| max|Lw_k| + L^3); I computed X mod four primes 1048573, 1048571, 1048559, 1048549 (product > 2*bound) with exact float64 matmuls (r*p^2 < 2^53): 0 nonzero entries mod each prime, hence X = 0 and the scheme is exact over Q. Sanity: the same checker on a copy with one w coefficient changed 1 -> 2 reports 10136 nonzero entries.
- Not done: I did not run the rebuild/ chain (it needs python-flint; installing is out of scope). The LITA parent copy in rebuild/ has the sha256 the claim states (94515288...a102a33). Provenance does not affect the criterion here because the composition exclusion is keyed to a listed rank, and 1709 is not listed.

## Null model / subsumption

- Trivial constructions from listed schemes give 1789 (the listed "naive-14x14x1 +p 14x14x14" = 1593 + 196), 1798, 1790, or a raw restriction of <15,15,15> 1977 (>= 1977 terms before any vanishing). None gives 1709. The claim's own chain shows the two slices alone reach 1731 (not a listed value either) and the elimination steps remove 22 more; 1709 is not a value listed anywhere I checked.
- Not subsumed by anything in the repository: the merged 1716 and the closed, unmerged PR #6 at 1715 are both above 1709; no PR at <= 1709.

## Worries

- This repository already holds a merged win for this very format (<14,14,15> rank 1716, TROPHY_CASE #47). The criterion's bar is only the four external sources, so the claim meets it literally; whether the bank counts a further 7-term improvement on the repository's own record as a new win is a maintainer judgement (precedent: #197, 1762 vs merged 1763, was merged).
- MerlijnW70 has no entry for the format, so that clause holds vacuously.
- The Lille per-format page (1798) is higher than fmm_sota.json (1789); the binding bar is fmm_sota.json.
- The re-fetch must be repeated immediately before filing; my fetches are from 10:13-10:14Z.

confirmed_scope: The three files in claim/object/ (sha256 abae4fc7..., a05bcf35..., 041992e8...) define a bilinear scheme with exactly 1709 rank-one terms over Q for <14,14,15> that satisfies all 8,643,600 Brent equations exactly, and 1709 is strictly below the minimum 1789 of the four named sources as fetched live at 2026-10-25T10:13:20Z (fmm_sota.json 1789, Lille 14x14x15.html 1798, Perminov ranks.md min 1790, MerlijnW70 no entry), with no V3R1T4S pull request at rank <= 1709 for this format.

pass: true
