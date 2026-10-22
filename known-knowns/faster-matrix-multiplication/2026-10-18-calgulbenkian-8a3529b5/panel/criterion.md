# Criterion report: ring-11x14x16-ZT-r1547

context: Claude Code subagent, fresh context
role: criterion skeptic. Judged only this cell (target fmm-ternary-integer-ring-upgrade).

Live values: one fetch each (curl, honest client, no retries) at 2026-10-18T14:21Z, HTTP 200 for all four. Their sha256 equal the ones recorded in the claim folder's the-record-we-beat/README.md (Perminov README 7b0761ec..., Perminov tree 71f2669d..., MerlijnW70 tree f25a290f..., fmm_sota.json d0da2c36...), so the folder values are the current live values. The claim folder hashes were checked against the contributor's hash list: all files OK.

## Object
- File object/11x14x16_m1547_ZT.json; n = [11, 14, 16]; stored m = 1547; terms = 1547; terms with all three factors nonzero = 1547.
- All entries are Python ints (no fractions/strings): True. Largest absolute coefficient: 1. Actual class: ZT. Claimed class: ZT. Label correct: True.
- Format range: max dimension 16 <= 16: True; sorted dimensions (11, 14, 16) != (4,4,4): True.

## Live README row (header ZT rank | Z rank | Q rank), cells as printed
`11x14x16`: ZT cell "1550 (?)", Z cell "1550 (?)", Q cell "1520 (1571)" -> ZT 1550, Z 1550, Q 1520. fmm_sota.json rank(s) for the sorted format: [1520].

## Clauses
- Clause (1), r strictly below the listed ZT rank: 1547 < 1550: MET. The comparison is made with the ZT column as the criterion words it (ZT claim vs ZT column, Z claim vs Z column).
  Note: another column is lower than r (the Q column (1520)). The criterion text does not compare with other columns in clause (1); clause (2) only requires r >= the minimum, which holds, so the wording still makes it a win literally. It is a win in its own class only; a scheme in a wider class is already at or below r.
- Clause (2), r >= min over ZT/Z/Q columns and fmm_sota.json: min(1550,1550,1520,[1520]) = 1520; 1547 >= 1520: MET.
- Clause (3), no scheme of rank <= 1547 in the same class: Perminov schemes/results (sorted dimensions, any permutation): ZT dir rank 1550 (schemes/results/ZT/11x14x16_m1550_ZT.json), Z dir no file, Q dir rank 1520 (schemes/results/Q/11x14x16_m1520_Q.json). MerlijnW70/fmm-schemes: ZT no file, Z no file, other no file. Minimum same-class file rank in Perminov is 1550, above 1547: MET; MerlijnW70 repository has nothing at rank <= 1547: MET.
- Clause (4), exact Brent equations over Z: shipped checker output (python -I, expect-rank 1547, expect-class ZT):
    coefficient class: ZT (max |coefficient| = 1; ZT means all coefficients in {-1, 0, 1})
    exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 11 bits, slot width 13 bits, 34496 blocks of 176 slots compared
    PASS format=11x14x16 rank=1547
  Own independent spot check (separate code, exact Python-int arithmetic, no modular reduction): evaluated sum over t of w_t[l*n1+i] * (u_t . A) * (v_t . B) on 5 random integer matrix pairs with entries in [-9,9] and 1 pair with entries up to 10^6 in absolute value, comparing with the true product A.B: all equal = True. Negative control (one coefficient of u[0] negated, tested on up to 5 further random pairs) is detected as wrong on at least one pair: True. This is a randomized identity test of the cubic Brent identity (failure probability negligible), complementing the shipped checker, which is deterministic and exhaustive. Clause (4): MET.

## Hidden quantifiers and null models
- The comparison set is the live README as re-fetched now; the README row (a rank of the form "N (?)" means no earlier value recorded) is the listed value. The format range and the (4,4,4) exclusion hold. Index permutations: the same sorted format is used for the table, Perminov files and MerlijnW70 files.
- Clause (3) was tested from file names in the repository trees (ranks in names), not by downloading the competing files; names carry the rank, so this is sufficient for "rank <= r exists".
- Null model: a scheme with the trivial or the best known lower rank cannot pass clause (1) and (2) together; this one sits strictly between the class value and the overall best.
- Not decided here: reproducibility beyond the exact check, and novelty against open pull requests or literature (other skeptics).

confirmed_scope: The file object/11x14x16_m1547_ZT.json is an exact integer (class ZT, largest absolute coefficient 1) bilinear scheme of rank 1547 for the 11x14x16 format whose Brent equations hold over Z, and rank 1547 is strictly below the ZT rank 1550 in the live Perminov README table, not below the overall best rank 1520 and not matched by any ZT-class scheme file in the two named repositories at the fetch time.

pass: true
