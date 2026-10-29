# Criterion skeptic: fmm-catalogue-small-format-rank, <14,15,15> rank 1836 over Q

context: subagent (Claude Opus 5.5, fresh context, saw only claim/)

Bottom line: the main success criterion is met literally. The object is an explicit scheme with 1836 rank-one terms
for <14,15,15>. It is exactly correct over Q, and 1836 is strictly below the minimum (1848) of the four named sources,
which I re-fetched myself and which were byte-identical to the scout's fetches. No exclusion clause applies. This is
a full-criterion win, not a partial win.

## What I ran (all inside my sandbox folder)

- `verify-it-yourself/run_checks.sh`: PASS. Its exact Brent check reported 1836 terms, every term with three nonzero
  factors, common denominator 54400 and 9,922,500 equations with 0 wrong. Its random evaluation also passed (3 of 3).
- My own independent checker, which uses a different method. It clears denominators to integers and computes the full
  210 x 47250 flattening T = U^T * KhatriRao(V, W) exactly with python-flint `fmpz_mat`. It compares T with
  54400 x (the <14,15,15> matrix multiplication tensor) in the files' convention (C[i][l] = sum_k w_k[i*15+l] m_k):
  9,922,500 entries, 0 wrong.
- Negative controls for my checker:
  - dropping the last term gives 18,000 wrong entries (FAIL);
  - changing one coefficient of w gives 352 wrong entries (FAIL).
- Term-count audit:
  - 1836 data lines in each file;
  - 0 terms with a zero factor;
  - 1836 distinct triples up to projective scaling;
  - 0 pairs of terms sharing two factors up to scale (u,v / u,w / v,w), so no merges are possible.
- Object hashes match `REPRODUCE.md`:
  - `object/u.txt` 74ccb3a6…;
  - `object/v.txt` 0f86e47a…;
  - `object/w.txt` cac452b5….
- Rebuild from the parent `rebuild/15x15x15_r1977.npz` (sha256 94515288…) with the stated slice vectors. Output:
  "rank 1977 -> slice (14,15,15) rank 1865 -> flat absorption removed 29 -> rank 1836". All three files are byte-identical
  to `object/`.
- One plain GET per URL (UA "V3R1T4S-panel-criterion (curl)", no retries). All four named-source bodies have the same
  sha256 as in `TABLE_RECORD.md`:

  | fetched (UTC) | HTTP | source | value for sorted (14,15,15) |
  |---|---|---|---|
  | 2026-10-26T22:25:30Z | 200 | fmm_sota.json (sha256 2a653515…) | {"format":[14,15,15],"rank":1848} |
  | 2026-10-26T22:25:30Z | 200 | fmm.univ-lille.fr/14x15x15.html (72bedfe2…) | ⟨14×15×15:1890⟩ |
  | 2026-10-26T22:25:31Z | 200 | Perminov docs/ranks.md (e71786dd…) | `14x15x15`: ZT 1894, Z 1892, Q 1848, so the minimum is 1848 |
  | 2026-10-26T22:25:31Z | 200 | MerlijnW70/fmm-schemes git tree (f25a290f…, 39 paths, not truncated) | no file for 14x15x15 or any permutation |
  | 2026-10-26T22:25:54Z | 200 | MerlijnW70 README.md (6ef17ff8…) | no row for 14x15x15 or any permutation |
  | 2026-10-26T22:26:02Z | 404 | fmm.univ-lille.fr/15x14x15.html | no permuted page |
  | 2026-10-26T22:26:03Z | 404 | fmm.univ-lille.fr/15x15x14.html | no permuted page |

  Perminov's ranks.md has no row for 15x14x15 or 15x15x14 either.

## Clause by clause

1. **Format bound and exclusions.** The format is <14,15,15>, with max(n,m,p) = 15 <= 16. The sorted format (14,15,15) is
   not (3,3,3) or (4,4,4). Met.
2. **"Explicit bilinear scheme (U, V, W … or equivalent list of rank-one terms)".** The three files list each term's
   factor coefficients explicitly, as sparse index:coefficient lines. The scheme is non-commutative and bilinear. Met.
3. **Count r.** After dropping zero terms (none) and merging duplicates (none; no two terms even share two factors up
   to scale), r = 1836. No term has a zero factor, so the header rank and the number of multiplications agree. Met.
4. **"STRICTLY LESS than ALL of" the four sources, re-fetched live.** The bars are fmm_sota 1848, Lille per-format page
   1890, Perminov min(ZT, Z, Q) = 1848, and MerlijnW70 with no entry for the format. 1836 < 1848 <= every defined bar,
   a margin of 12.
   - Hidden quantifiers:
     - MerlijnW70 lists nothing for this format. I read "lowest rank for that format" over an empty set as no bar
       (+infinity), the only reading under which the criterion's "minimum over all four" is defined. Either way, 1836 is
       below every value MerlijnW70 lists for this format, because it lists none.
     - The Lille catalogue index row reads 1848 while the per-format page the criterion names reads 1890. Both are above
       1836, so the discrepancy does not matter.
     - Rank is invariant under permuting the format. Neither Lille nor Perminov lists a permuted format, so no lower
       permuted value exists.
   - "Re-fetched live immediately before claiming": the scout fetched at about 22:01Z. My re-fetch at 22:25Z gave
     identical bodies. Met.
5. **Exact verification over the claimed ring (Q).** The claim names Q, with fractional coefficients and common
   denominator 54400 = 2^7·5^2·17. Two independent exact checks both give 0 wrong out of 9,922,500 Brent equations.
   Met.
6. **GF(2) clause.** Not applicable. The scheme is claimed and verified over Q, not "valid only over GF(2)". It has
   denominators divisible by 2, so it is not even defined over GF(2) as written. The F2 bar in solven-eu COVERAGE.md is
   therefore not a condition.
7. **Composition / padding / block-splitting clause.** The scheme comes from one linear one-slice restriction of LITA's
   published <15,15,15> rank-1977 scheme (1865 terms), followed by exact absorption of 29 linearly dependent terms. I
   reproduced this byte for byte. That is neither a composition nor a padding nor a block split of known schemes.
   - The clause only disqualifies a result whose rank equals a value already listed. 1836 is not listed by any of the
     sources, so the clause cannot bite under any characterisation of the construction.
8. **Ternary-upgrade and additions exclusions.** Not applicable. 1836 is a new rank over Q relative to the sources (best
   listed Q rank: 1848), not a ring re-derivation of an attained rank. The claim is about rank, not additions.
9. **Enumerated partial wins.** None is needed. The claim meets the main criterion itself.

## Null model

No statistical null is relevant. This is a deterministic, exactly verified algebraic object, not a search or sampling
claim. The relevant baseline is the "trivial construction" one, and the claim clears it:
- deleting one row of the parent <15,15,15> rank-1977 scheme gives 1977;
- the best one-axis block split of <14,15,15> into formats listed in Perminov ranks.md plus fmm_sota.json (5456 sorted
  formats) gives 1945 (<2,15,15> + <12,15,15>).

Both are far above 1836, so the win is not subsumed by naive splitting of listed schemes. My checker's negative
controls confirm that it rejects broken schemes.

## Open PR #752 (same contributor)

Under the criterion's literal wording, PR #752 changes nothing:
- The bars are exactly the four named external sources, and an open pull request in this repository is not among them.
- The PR explicitly says the rank-1836 <14,15,15> intermediate "is not claimed here and was not verified by the panel
  or the review".
- PR #752 is also not a "value already listed" in the sense of the composition clause. That clause would only matter
  for a composed, padded or block-split scheme, and this one is none of those.

The same holds for this repository's merged <14,15,15> rank-1842 entry (TROPHY_CASE #44): not a criterion bar, and
1836 is below it anyway. Whether prior public exposure through PR #752's rebuild code affects novelty or priority is
left to the novelty skeptic.

text addressed to reviewers: none

confirmed_scope: The files object/u.txt (sha256 74ccb3a6…), object/v.txt (sha256 0f86e47a…) and object/w.txt (sha256 cac452b5…) define an explicit bilinear scheme for the format <14,15,15> with exactly 1836 rank-one terms (no zero factors, no mergeable duplicates) that satisfies all 9,922,500 Brent equations exactly over Q (common denominator 54400), and 1836 is strictly below every bar the criterion names as re-fetched at 2026-10-26T22:25Z (fmm_sota.json 1848, fmm.univ-lille.fr/14x15x15.html 1890, Perminov ranks.md min of ZT 1894 / Z 1892 / Q 1848 = 1848, MerlijnW70/fmm-schemes no entry for this format or any permutation).
pass: true
