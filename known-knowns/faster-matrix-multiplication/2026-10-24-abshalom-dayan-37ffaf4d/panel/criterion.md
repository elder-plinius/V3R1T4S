# CRITERION skeptic: fmm-catalogue-small-format-rank, claimed partial win p1, <18,18,19> rank 3225

context: subagent (Claude Opus 5.5, fresh context, given only a copy of claim/)

Sources for the criterion: the bank entry `fmm-catalogue-small-format-rank` in bank/targets.json and its
known-unknowns page (read directly, not taken from the claim; the claim's quotation in CLAIM.md matches them word
for word), kit/RULES.md and the "Fast matrix multiplication" section of kit/POLICY.md.

## Which level is claimed

The main criterion requires "a format <n,m,p> with max(n,m,p) <= 16". max(18,18,19) = 19, so the main criterion
cannot be met, and the claim does not say it is. CLAIM.md asks only for partial win p1. Only p1 is judged here.

## p1, clause by clause (bank text quoted)

| p1 clause (verbatim) | finding |
|---|---|
| "A new rank for a format with 17 <= max(n,m,p) <= 32" | max = 19, which is inside 17..32. The format is <18,18,19> (A 18x18, B 18x19, C 18x19), already sorted. "New rank" can only mean a new upper bound (a scheme). The claim says that ("Not the tensor rank ... 3225 is an upper bound"). Met. |
| "(outside Perminov's 16x16x16 table but inside the Lille catalogue)" | fmm_sota.json has the entry `{"format": [18, 18, 19], "rank": 3355}`, and the Lille index has the row ⟨18×18×19:3355⟩. Both were re-fetched by me (see below), so the format is inside the Lille catalogue. Perminov's table stops at 16, so the format is outside it. Met. |
| "an exactly verified scheme" | I verified it myself in exact arithmetic (see "Own checks"): all 37,896,336 Brent equations hold over Q, and an exact Fraction evaluation on a random pair agrees. Met. |
| "whose rank is strictly below the live fmm_sota.json entry ... for that format" | fmm_sota.json, re-fetched live by me: 3355 for [18,18,19]. 3225 < 3355, a margin of 130. Met. |
| "and the live Lille per-format page for that format" | The claim records https://fmm.univ-lille.fr/18x18x19.html at 3524 (HTTP 200, sha256 0bae8537..., 2026-10-24T19:05:59Z, in the-record-we-beat/RECORD.md). I did not re-fetch the per-format page, because my mandate allowed one fetch each of the index and fmm_sota.json. The index I fetched (same sha256 as the claim's fetch, so unchanged) gives 3355 for the cell. 3225 < 3524 and 3225 < 3355. Met on the record, with my own live confirmation of the index and the digest. |
| "and not a plain composition already listed in the Lille 'construction' column" | The Lille index row for 18x18x19 lists exactly one construction: ⟨18×18×1:324⟩ + ⟨18×18×18:3031⟩ = 3355. 3225 is not that value. The object is also not a plain composition. It comes from LITA's published <19,19,19> rank-3633 scheme through two non-coordinate one-slice restrictions, each followed by an exact 2-reduction (the claim's provenance, how-we-built-it/COMMANDS.md). My null model below shows that no composition of listed values gets below 3355. Met. |

### Clauses of the main criterion that carry over to p1 (counting, ring, scope)

- Counting convention. The bank says "r must be the number of rank-one terms after removing zero terms and merging
  duplicates". I find 3225 terms, 0 with an empty factor or a zero coefficient, and 0 pairs of terms with
  proportional factors in any two of U, V, W, so no merge is possible. r = 3225 under the bank's convention. The
  count is multiplications (rank), not additions, so the fmm-additive-complexity-records scope is not touched.
- Commutative vs non-commutative. Each product is m_k = (linear form in A)·(linear form in B), with A on the left
  and B on the right. The Brent equations I checked are the non-commutative identity, so the scheme is a bilinear
  (non-commutative) scheme as the bank requires.
- Ring. The coefficients are rationals with denominators {2, 4, 5, 7, 10, 12, 14, 25, 28, 50, 84, 300, 600, 1200}.
  The scheme is claimed and verified over Q only, so the GF(2) clause and the ternary/integer scope split do not
  apply. Because it is a characteristic-0 scheme, it compares directly with the characteristic-0 catalogue values.
- Derived from a published scheme. The criterion excludes only a composition, padding or block split "if the
  resulting rank equals a value already listed". Restricting LITA 19^3 and then reducing gives a value (3225) that is
  listed nowhere I checked, so the derivation does not disqualify the claim. The LITA authors are credited
  (Khoruzhii, Serafin, Gelss, Pokutta).
- One cell per claim (RULES.md rule 4). Only <18,18,19> is claimed. The sibling <18,19,19> rank 3424 is excluded
  explicitly (PR #708).
- Object format. u.txt, v.txt (= v.part1.txt + v.part2.txt) and w.txt are explicit sparse rational factor lists, an
  "equivalent list of rank-one terms" in the bank's wording. The bank sets no further format or verifier
  requirement.

## Own checks (my own code, nice -n 10)

1. Exact Brent check, written independently (python3 -I, numpy 2.5.3). Each factor matrix is parsed as Fractions
   and scaled to integers by its least common denominator (U 8400, V 84, W 84; scale 59,270,400). The full tensor
   sum_k u_k ⊗ v_k ⊗ w_k is then compared with S·δ(i=i')δ(j=j')δ(l=l') for every index triple. This used float64
   BLAS, with a proof of exactness: the maximum of sum_k |u||v||w| over all triples is 25,416,373,860,864 < 2^53, so
   every partial sum is an exactly representable integer. Output:
   - sha256 u 37ffaf4d...5eca, v (joined parts) 5d15717b...c5be, w 0f0a3d5c...d93a: identical to CLAIM.md
   - headers `# format 18 18 19`, `# rank 3225` in all three files; 3225 terms each
   - terms with an empty factor or a zero coefficient: 0; mergeable (proportional) pairs in UV, UW, VW: 0, 0, 0
   - Brent equations checked 37,896,336, wrong 0
   - exact Fraction evaluation, random integer A, B (seed 7): 0 of 342 entries of C differ from AB
   - 4.2 s, peak memory 189 MB
2. Live table fetch: one plain GET each, User-Agent naming V3R1T4S, no retries.
   - https://fmm.univ-lille.fr/ at 2026-10-24T19:34:28Z: HTTP 200, sha256 57e936b6...06a9 (identical to the
     claim's 19:05:59Z fetch). The row is ⟨18×18×19:3355⟩, construction ⟨18×18×1:324⟩ + ⟨18×18×18:3031⟩. There is no
     row for 18x19x18 or 19x18x18. No ⟨...:3225⟩ entry anywhere; the string "3225" occurs only inside unrelated
     numbers, for example the maintainer's ORCID and complexity exponents.
   - fmm_sota.json at 2026-10-24T19:34:29Z: HTTP 200, sha256 2a653515...cbae (identical to the claim's fetch),
     createdAt 2026-10-19T20:46:33, 5456 entries, [18,18,19] -> 3355.
3. Null model, meaning what can be obtained trivially from the table. Computed over fmm_sota.json:
   - restriction from any listed format that contains (18,18,19): best 3355; the next containing formats are
     (18,18,20) 3526 and (18,19,19)/(19,19,19) 3633
   - recursive block sums along every axis, plus Kronecker factorizations, from table values: best 3355
     (18+1 split on p). Every other split is at least 3524; for example 9+9 gives 1762+1762.

   No trivially derived bound reaches 3225. The claim's own accounting gives more null baselines, which I have not
   recomputed, because the LITA source file is not in claim/: coordinate restriction of LITA 19^3 gives 3557, and
   coordinate restriction of the sibling 3424 gives 3395. Both are above 3355.
4. Subsumption by the sibling <18,19,19> 3424 (PR #708, open, not in any table). If it were merged, restricting it
   by deleting a column gives 3395 by the claim's figure (and at least 3355 in any case per the null model above).
   The sibling therefore does not subsume 3225, and it is a different cell, so the same-cell priority rule (POLICY
   rule 5) does not apply.

## Notes for the gate (not criterion failures)

- PR #708's body states the value 3225 for this cell without a scheme. It was opened 2026-10-24T18:58:23Z by the
  same contributor. POLICY rules 2 and 3 date credit by the filing of the claimed object, and a bare number is not an
  object under RULES.md rule 1. This is a novelty or dating question, not a failure of a p1 clause. I mention it so
  the gate sees it.
- The per-format page value (3524) rests on the claim's recorded fetch, not on a fetch of my own. The index and the
  digest, which I did re-fetch, give 3355, and both lie above 3225.
- p1 does not require beating Perminov's or MerlijnW70's tables. Per the claim's record, neither covers dimension 19
  in any case.

confirmed_scope: object/u.txt, object/v.txt (object/v.part1.txt followed by object/v.part2.txt) and object/w.txt form an exactly verified bilinear scheme over Q for <18,18,19> with 3225 rank-one terms (no zero or mergeable terms), which is strictly below the rank 3355 for [18,18,19] in fmm_sota.json and in the Lille catalogue index (both re-fetched 2026-10-24T19:34Z) and below the 3524 on the Lille per-format page as recorded in the-record-we-beat/RECORD.md; this meets partial win p1 of fmm-catalogue-small-format-rank, not the main criterion.

pass: true
