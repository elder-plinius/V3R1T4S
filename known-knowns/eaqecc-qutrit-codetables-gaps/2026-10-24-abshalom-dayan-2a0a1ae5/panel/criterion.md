# Criterion skeptic verdict

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

**Bottom line: PASS.** The full success criterion is met as written. This is not a partial win (p1 or p2). The
stabilizer matrix S has (n,k,c) = (28,9,7) with c = 7 >= 1. Its exact distance is d = 11 under the stated EAQECC
definition (min weight on span(S)^perp outside span(S) ∩ span(S)^perp). I checked it with my own exhaustive code and
an explicit witness. The live page I fetched lists the cell [[28,9,10-14;7]]_3, so 10 < 11 <= 14. I found no hidden
quantifier, no stretched definition, no catalytic reading, no sampling and no cell mismatch.

## Clause by clause

| # | Clause | What I checked (my own code in mine/) | Result |
|---|--------|----------------------------------------|--------|
| 1 | Exact generator matrix over GF(3), 2n columns | `S` in claim/object/eaqecc_28_9_11_7.json: 26 rows x 56 columns, every entry in {0,1,2}, rows (x\|z). sha256 of the JSON is 2a0a1ae5e178dcc0264b6a9f40ee1935991f28e65199a0712aecffe879b6c7d0, as stated. The author's rebuild (`rebuild/build_obj.py 17`, run in mine/author_run/) reproduces it byte for byte. | met |
| 2 | s independent generators on Alice's n qutrits | mine/params.py: rank over GF(3) = 26 = number of rows, n = 28 (no Bob columns) | s = 26 |
| 3 | c = rank(S J S^T)/2, c >= 1 | Commutation matrix from <(x\|z),(x'\|z')> = x.z' - z.x'. It is antisymmetric (asserted) with rank 14. | c = 7 |
| 4 | k = n - s + c | 28 - 26 + 7 | k = 9. This matches the claim's JSON fields and the cell (28,9,7). It is a different (n,k,c) from no cell. |
| 5 | d exact: min symplectic weight on span(S)^perp \ (span(S) ∩ span(S)^perp) | dim span(S)^perp = 30. The isotropic part has dim 12 (two ways: from the left kernel of the commutation matrix, and as s + 30 - dim(span S + dual)). **Lower bound:** mine/subset.c (my own bit-sliced GF(3) code) runs over all 13,123,110 = C(28,10) position sets T. For each T it computes dim(dual_T) = 2\|T\| - rank(S restricted to the columns of T), and if that is nonzero, compares it with dim(iso_T). Result: no nonzero vector of span(S)^perp lies on <= 10 positions (mine/W10.out). So d >= 11, and the pure distance is also >= 11, so the isotropic exclusion cannot hide a lighter vector. **Upper bound:** mine/mywitness.py builds a vector supported on T = {0,1,2,3,4,5,6,11,18,26,27}. It has symplectic weight 11, is orthogonal to all 26 rows, and is not in span(S), so it is not isotropic (mine/witness.out). | d = 11 exactly |
| 5a | Not sampled or capped | Enumeration counts equal C(28,10) and C(28,11), checked with math.comb. At W = 11 my code finds 5211 sets, each with dim(dual_T) = 2 and dim(iso_T) = 0 (mine/W11.out). This matches the author's 5211 from both of their methods. | exhaustive |
| 5b | Validation of my checker | mine/control.py ran 2 x 40 random small EA codes (n = 4..6), including planted low-weight isotropic generators. Brute force over all dual vectors (both pure distance and distance excluding isotropic vectors) agreed with subset.c 40/40 both times (mine/control.out). In 28 of those trials the isotropic exclusion changed the answer, so that branch was exercised. mine/spot.py redid 3000 random 10-subsets and 3000 random 11-subsets of the real S in plain Python. It found no deficiency and dim 2 on the three printed weight-11 sets. | checker sound |
| 6 | Cell of the live table, re-fetched | My single GET of https://eaqecc.codetables.de/qutrit.php ran from 2026-10-24T17:42:49Z to 17:42:50Z (UTC) and returned HTTP 200, 628039 bytes, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. That is byte-identical to the author's claim/table/qutrit.php, fetched 16:42:29Z, about 17 min before the claim files were written at 16:59:39Z. Saved in fetched/ (headers, times, status, sha256.txt, cell.txt). The cell is listed verbatim: `<TD NOWRAP bgcolor="#0099ff" class="EAQECC" title="increasing dimension of [[28,2,10;0]] from codetables.de">[[28,9,10-14;7]]<sub>3</sub></TD>`. It is the only ranged cell for (28,9,7), and no other cell on the page gives d_lower >= 11 for (28,9,7). Footer: "Last change: 10.07.2025". | listed. d_lower = 10, d_upper = 14 |
| 7 | d > d_lower strictly, d <= d_upper | 11 > 10, and 11 <= 14 | met |
| 8 | c = 0 excluded | c = 7 | met |
| 9 | Non-catalytic | k is the standard k = n - s + c from s = 26 generators acting on Alice's 28 qutrits. There is no k - c or k + c reinterpretation and no entanglement regenerated from logical qudits. The table's own derivations use the same convention (e.g. "increasing dimension of [[28,6,9;0]]" giving [[28,9,9;3]]). | met |

## Null-model and subsumption checks

- **Do the table's own rules already reach 11?** No. The (28,9,7) bound of 10 comes from "increasing dimension of
  [[28,2,10;0]]" (k+1, c+1, same d). The cells that could feed it all have d_lower <= 10:
  - (28,9-j,7-j), via increasing dimension.
  - (27,9,6..7) and (27,8,7), via lengthening.
  - (28,10,7), via subcode; its inherited bound is 9-12.

  Cells with d_lower >= 11 nearby are (28,7,7), (28,8,8), (28,9,9) and (28,10,9). They have equal or larger c with
  equal or smaller k, and no standard rule lowers c at fixed n and k. So the result is not implied by a listed entry.
- **Partial-win subsumption:** this is a full-criterion claim (a new code above d_lower). It is neither the p1
  (upper bound) nor the p2 (fewer ebits) partial win.
- **Construction:** an extended one-point Hermitian code [28,15,11]_9 with Hermitian hull dimension 6. This is a
  standard construction, but the criterion asks only for improvement over the live table's d_lower, and the table
  does not list it. Whether it appears elsewhere in the literature is outside this criterion.
- **Other checks:** the author's commands, rerun in mine/author_run/, give the same numbers as REPRODUCE.md:
  - Method A, m = 18: 0 deficient over 13,123,110 subsets.
  - Method A, m = 17: 3396 + 1335 + 480 deficient.
  - Method B, W = 10: 0 sets with a vector outside the isotropic part.
  - Method B, W = 11: 1735 + 1745 + 1731 such sets.
  - Both witness tools: weight 11, not isotropic.

  injection_suspected: none. The fetched page and the claim files contained no instructions aimed at the reader.

## Caveats (do not change the verdict)

- The "immediately before claiming" fetch by the author came about 17 min before the claim files were written. My
  own live fetch is identical byte for byte, so the cell was unchanged at verdict time.
- Newly fetched cells derived from this one ([[29,9,10-14;7]] and [[30,9,10-15;7]], by lengthening [[28,9,10;7]])
  may also be affected. They are not claimed and I did not verify them.

confirmed_scope: The 26 x 56 GF(3) matrix S in object/eaqecc_28_9_11_7.json defines a [[28,9,11;7]]_3 EAQECC: it has 26 independent rows, rank(S J S^T) = 14 (c = 7) and k = 9, and its distance is exactly 11 as the minimum symplectic weight on span(S)^perp outside span(S) ∩ span(S)^perp (exhaustive over all 10-position subsets plus an explicit weight-11 non-isotropic witness), which is strictly above the d_lower = 10 and within the d_upper = 14 of the listed cell [[28,9,10-14;7]]_3 on https://eaqecc.codetables.de/qutrit.php as fetched 2026-10-24T17:42:49Z (sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c).

pass: true
