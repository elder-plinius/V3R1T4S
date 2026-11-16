context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report

Verdict on the criterion: the main criterion (exact distance of [[360]] or [[756]]) is NOT met and is not claimed. Enumerated partial win p1 is literally met for the [[504,12,<=30]] code.

## Checks against p1, word by word
- Which code: l=42, m=6, A=x^27+y+y^2, B=y^3+x^37+x^38, n=504. These match the p1 text for [[504,12,<=30]] and the Symons-Rajput-Browne entry. p1 allows this code explicitly.
- Rank/k: my own independent Python-int script (not shipped in this package, run with -I, no shared code with the package verifier) gets k=12, rank HX = rank HZ = 246, and HX*HZ^T = 0.
- Weight strictly below the published bound: the witness (object/bb504_logical_wt28.txt) has 28 distinct indices, below 30. Strict inequality holds.
- Nontrivial and exact: it is in ker of one check matrix and outside the row space of the other (rank +1 test), so it is a logical, not a stabilizer. Verified by exact GF(2) arithmetic, not a heuristic or time-limited run.
- Convention: the package verifier builds the checks with the shifts negated (it uses the transposes, row r-d rather than r+d). My raw run with the standard [A|B], [B^T|A^T] and the file's indices as given FAILS the syndrome test. After the index map (x,y) -> (-x,-y) on both blocks, the witness passes under the standard convention (HX v = 0, not in rowspace HZ), weight 28. That map is a pure relabeling that sends the transposed-convention code to the standard one, so it is the same code up to isomorphism. The package's verifier also checks this inversion. So the claim is sound, but the file's indices are literally in the negated labeling, which the README does not say plainly.
- Dual claim: I also found a weight-28 vector in ker HZ, outside rowspace(HX), by swapping the two blocks of the relabeled witness (negswap/swapneg tests passed). So the "dual X-logical of weight 28" statement holds.
- Not overclaimed: README says d <= 28 only, no lower bound, no claim on 360/432/756. That is the correct scope. The pre-registration is consistent.

## Limits and what I could not settle
- Novelty/subsumption: I did not search the literature. A fetch of the Rowshan-Devitt README (200) shows no entry for n=504 (only the 288 table row mentions 455,504,708, a node count). The arXiv abs page for 2511.13560 was fetched but is only the abstract page; I could not confirm Table 1 or v3 details from it, and I did not check for any newer value at or below 28 for this code. The NOVELTY skeptic must settle that. Repository rule: a tie or better upstream counts against it.
- The result is only an upper bound (d <= 28). The true d may be lower. It is a modest p1 win (BP-OSD style bound of 30 beaten by 2), not an exact distance.
- The unverified part of the package is the 360 control log (not shipped in this package) cited in RECEIPTS.md; it is not in the folder, so I did not check it. It is not needed for p1.

confirmed_scope: An explicit weight-28 nontrivial logical operator (index-negated labeling of the standard convention, equivalent by relabeling) exists for the [[504,12]] covering BB code with l=42, m=6, A=x^27+y+y^2, B=y^3+x^37+x^38, verified exactly over GF(2), so its minimum distance is at most 28, below the published bound of 30; no lower bound, no exact distance, and no claim on the 360, 432 or 756 codes.

pass: true
