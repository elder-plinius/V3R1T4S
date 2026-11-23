# CRITERION panel: OEIS A054961 a(16) >= 102 (claim_a054961_16_102)
context: independent fresh-context CRITERION panelist (a knowledgeWork subagent with no prior conversation), working only from the claim folder, the run's saved OEIS copy that claim/TABLE_RECORD.md cites, and one web search
reviewed: 2026-10-22T19:29:25Z
verdict: SURVIVES
criterion_met: partial win (enumerated run partial win: explicit family of m distinct binary vectors of length n with all C(m,2) pairwise ORs distinct, m > B(n), not VOID; here n=16, m=102 > B(16)=92)
confirmed_scope: The file claim/A054961_n16_m102.txt (sha256 de9e6522...e381) is a family of 102 distinct binary vectors of length 16 whose 5151 pairwise ORs of distinct vectors are all distinct, so under the OEIS A054961 definition a(16) >= 102, which exceeds the best value found in the cited public sources (91, Zhao Hui Du 2018; emath poisonall.txt; wolfy-out.txt) and is not a trivial extension of any of them; a(16) itself is not determined.

## (a) Definition reading
- The OEIS A054961 title says "the unions (or bitwise ORs) of any 2 distinct vectors are all distinct". In the saved 2026-10-22 OEIS copy (the one claim/TABLE_RECORD.md cites), the EXAMPLE for n=4 is {0000 0001 0010 0100 1000}, and n=5 is 00000 plus the 5 unit vectors. These pass only reading A (unions of 2 distinct vectors). Under reading B (singletons counted, bar-2-separable), 0000|0001 = 0001 is the same as the singleton 0001. So the sequence literally uses reading A. The comment "concatenation of these vectors produces a 2-separable matrix" (exactly-2 separability) agrees with this.
- The claim says it is made under reading A and openly reports that reading B FAILS (26 containments). That is the right reading. My own check gives the same result: there are 26 pairwise ORs that equal a family member, all from the weight-1 vector 0000010000000000 sitting inside 26 weight-4 vectors.
- Wording flags (they don't affect the verdict, but the claim text should be tightened before packaging):
  1. In claim/CLAIM.md, "16 tests that identify any 2 defective items" should say "exactly 2". The family cannot tell 1 defective apart from 2.
  2. "union-free / '2-cancellative' families in the sense of Erdős-Frankl-Füredi" stretches the source. EFF 1982 is about cover-free families ("no set covered by the union of two others"), and this family is badly NOT 2-cover-free. The correct name is union-free in the Frankl-Füredi sense (all pairwise unions distinct). The family is also not cancellative if A=B is allowed (v|e = v|v). Suggested replacement: "union-free family (all unions of two distinct members distinct); not 2-cover-free, not bar-2-separable".

## (b) Trivial extension / VOID clause (my own script in a scratch directory)
```
sha256 de9e6522f190dbddc1bf2db69e8e1dcf9cb8995e8adc7f5b9a61093b95ffe381
m 102 distinct True
pairs 5151 distinct ORs 5151 max mult 1
ORs equal to a member vector: 26
weights [(1, 1), (4, 101)]
weight1 0000010000000000 contained in 26
vanish per coord [75, 77, 81, 78, 78, 75, 76, 77, 77, 79, 76, 76, 77, 74, 74, 77] max 81
max vanishing on any 2 coords 62
intersections among weight-4 [(0, 1401), (1, 2376), (2, 1273)]
max 4-sets through a 3-set 1
```
- Zero-pad of an n=15 family plus at most 1 vector: this would need at least 101 vectors vanishing on one coordinate, but the maximum is 81. A pad by 2 coordinates would need at least 100 vanishing on 2 coordinates, but the maximum is 62. Neither is possible. (Any n=15 sub-family would also be at most 81, which is still above the published 79 at n=15. That is a side fact only and is not claimed.)
- Published family plus at most 2 vectors, or a union/restriction of published objects: both published 91-families have weight profile {0:1, 4:7, 5:49, 6:34}. This family has no weight-0, 5 or 6 vectors. Coordinate permutations are the only OR-automorphisms and they preserve weight, so no copy of either published family can be contained here (claim/compare_published.py shows the same, with 0 shared vectors). The family is a genuinely different object.
- Own unpanelled 92 (run 1345): 6 shared vectors, and the 92's weight-0 and weight-5 vectors are missing. This is not an "own-92 + augment".
- Structure note: the 101 weight-4 vectors form a packing (every 3-set lies in at most one block), so they are a sub-family of a partial SQS(16) (A(16,4,4) = 140). That explains why a weight-4 search finds it easily, but no published A054961 object contains it. Not VOID.

## (c) Partial win vs full criterion
- The charter criterion is "extend or improve the best known values" for A054961 / A290492 / A361928. The result improves the best known lower bound for a(16) by an explicit object. It does not determine a term, does not extend the DATA (which stops at a(9)), and touches only one of the three sequences. So I score it as the enumerated partial win from claim/PREREG.md and claim/target.md (explicit family, m > B(n), not VOID), not the full criterion.
- B(16) = max(91, 91, 91, own 92) = 92, and the candidate threshold was m >= 93. Since 102 > 92, the enumerated partial win is met literally. The threshold B(n) was frozen in PREREG at 2026-10-19T17:47:37Z, before the find at 19:27:44Z (claim/provenance/ladder_W16.log), and the find is inside the budget (end 20:47:37Z).

## (d) Scope vs evidence
- The claim is stated as a lower bound only (a(16) >= 102). CLAIM.md does not claim a(16) is determined, and it keeps the reading-B failure and the "side fact" 101 bar-2-separable family out of the claim. The upper bound C(m,2) <= 2^16 (m <= 362) gives no contradiction.
- "Best published 91": the cited OEIS copy (2026-10-22) shows Du's Apr 19 2018 list with 91 at n=16 (the Mar 30 2018 list had 90). No later comment raises it. My single web search (separable codes / union-free / constant-weight tables) found no n=16 binary value above 91. Neither I nor the claim checked Du-Hwang's book tables or unarchived emath forum pages, so "best known" means "best found in the cited public sources" (as my confirmed_scope says). The NOVELTY panelist should own that question.
- Null model: claim/provenance/ladder_W16.log shows a weight-4 random-start search reaching 93..100 within about 20 minutes. So the published 91 was simply weak (the published families are weight-5/6 heavy). That is not a reason to reject: the criterion is to improve the best known value, and the object is explicit and exhaustively checked. It does mean the margin (+11) reflects a stale table more than a hard search, and the claim text should not suggest more than that.

## Conclusion
I verified the object with my own checker (5151/5151 distinct ORs, 102 distinct length-16 rows). It uses the literal OEIS reading, it is not VOID, and it beats the frozen B(16)=92. It meets the enumerated partial win, not the full criterion. Two wording fixes are recommended in CLAIM.md ("exactly 2 defectives", and replacing the EFF "2-cancellative" phrasing with "union-free; not 2-cover-free"), but neither changes the scope.
pass: true
