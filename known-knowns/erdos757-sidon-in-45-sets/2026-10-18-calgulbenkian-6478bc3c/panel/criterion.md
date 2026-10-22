# Criterion skeptic report: e757-n21 (partial win p1 only)
context: Claude Code subagent, fresh context

Target: erdos757-sidon-in-45-sets. Claimed: partial win p1 only (not the full criterion). Object: object/witness_n21_s12.json, 21 integers. Hashes in the contributor's hash list were checked from inside the package folder: all OK.

## My own checks (output not shipped in this package)
Own script, definitions written from the criterion text:
- distinct integers: 21 distinct, all integers.
- (4,5)-property: all C(21,4) = 5985 four-subsets have at least 5 distinct absolute differences: True.
- s(A), method 1: my own depth-first branch and bound over subsets with a pairwise-distinct-differences test (a 3-AP is a repeated difference, so a = b sums are covered): 12.
- s(A), method 2: my own ILP (pulp with CBC) with one constraint per pair of equal differences (19 constraints, status Optimal): 12.
- Ratio with fractions.Fraction: 12/21 = 4/7. Below 4/7: False. Equal to 4/7: True. At least 9/17: True. 21 mod 14 = 7, so |A| is not a multiple of 14.
- Calibration on the Ma-Tang 14-set (verify-it-yourself/calibration_ma_tang.json): (4,5) True, s = 8 by both of my methods (item 6).
- Extra structural test: the set contains the exact image 10 x (Ma-Tang 14-set) (scale 10, offset 0), plus 7 further points 9815, 11223, 11264, 11305, 12631, 13957, 16650. Those 7 points alone form a (4,5)-set with s = 5, so s = 12 = 8 + 4 is not a simple sum of the parts.

## Numbered items of the criterion
1. Every 4-subset has at least 5 distinct differences, exhaustively: met.
2. Exact s(A) certified by two independent exact methods (bitmask branch and bound; ILP forbidding every a+b = c+d including a = b): met. The folder ships a bitmask branch and bound plus a full 2^21 enumeration, and an ILP (verify-it-yourself/ilp_sidon.py) that was added by the orchestrator on 2026-10-18; I reproduced s = 12 with my own two different methods. The author's JSON fields s_method1 and s_method2 are the author's reports and I did not rely on them.
3. s/|A| strictly smaller than the best upper bound shown at verification time: NOT MET for the full criterion (the ratio equals 4/7; the criterion says an equal ratio is not a success). The claim does not assert it; p1 replaces this item with equality. Live check: I fetched the erdosproblems.com page for problem 757 once at 2026-10-18T14:25Z (HTTP 200): it still reads 9/17 <= c <= 4/7 (Ma and Tang). I fetched the EinsteinArena page sidon-45-set once (HTTP 200, sha256 identical to the claim record 8aa7ed03...2044): leaderboard best 0.571428571 (Ma-Tang, Previous SOTA). Not decided here: whether a newer arXiv paper has lowered the bound (not searched; novelty skeptic's job). If one had, equality with 4/7 would no longer be 'equal to the live best'.
4. s/|A| >= 9/17: met (4/7 > 9/17).
5. Verify in arXiv:2602.23282 the lemma that a finite witness bounds c* (blow-up lemma or inf-formula): not needed for p1 and not checked. p1 makes no claim about c*, since a ratio equal to 4/7 does not improve the bound, so no lemma is invoked. It would be needed for any claim that a finite witness lowers the upper bound on c*. The folder contains no check of it.
6. Calibration, Ma-Tang 14-set gives s = 8: met.

## p1 text, literally
p1: 'a (4,5)-set A with |A| NOT a multiple of 14 (e.g. |A| = 21 with s = 12) whose certified exact maximum Sidon subset gives s/|A| exactly equal to the live best ratio (4/7 ...), verified by the same two-method pipeline.'
- (4,5)-set: met. |A| = 21, not a multiple of 14: met. s = 12, certified exactly: met (two methods, agree). Ratio exactly 4/7, equal to the live best (erdosproblems.com/757 and the arena leaderboard as fetched today): met. Same two-method pipeline as item 2: met.
- 'Disjoint unions of dilated copies of the Ma-Tang 14-set only reach multiples of 14, so this is a structurally new extremal example': true as far as the union construction goes, but it is the author's gloss, not a criterion clause. This set is not independent of Ma-Tang: it contains a dilated copy of the 14-set and adds 7 points. Whether the Ma-Tang paper or others already list other sizes at 4/7 cannot be decided from the folder.
- Other notes: the arena problem restricts to at most 18 integers, so the object is not arena-eligible (the folder says so). This is a refile of the author's earlier closed PR with the same set (stated in the claim; the author's own earlier filing, not a competing value). p1 is a tie, so it is a partial win only; the full criterion is not met.

confirmed_scope: The set A in object/witness_n21_s12.json (21 distinct integers, 21 not a multiple of 14) is a (4,5)-set whose exact maximum Sidon subset has size 12 (agreed by two independent exact methods run here), giving s/|A| = 4/7, exactly equal to, not below, the 4/7 shown at erdosproblems.com/757 and on the EinsteinArena leaderboard on 2026-10-18; this meets only the p1 partial win, not the full criterion, and says nothing about the lemma in arXiv:2602.23282.

pass: true
