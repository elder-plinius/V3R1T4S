context: subagent
skeptic: reproduce
target_id: eaqecc-qutrit-codetables-gaps

# Reproduce Skeptic Report: `[[14, 3, 8; 5]]_3` (`claim/object/qutrit_14_3_8_5.json`)

## 1. Quoted Mathematical Definition (from `claim/CLAIM.md`)

> "Success means an explicit EAQECC with parameters [[n,k,d;c]]_3, c >= 1, given by an exact generator matrix over GF(3) (symplectic form, 2n columns) or over GF(9) (trace-Hermitian form), for a cell of the live qutrit table (https://eaqecc.codetables.de/qutrit.php, re-fetched live immediately before claiming), such that: with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded (they belong to the qudit table entry)."

## 2. Independent Checker Written Before Reading Author Code

Before reading `claim/check_eaqecc.py` or `claim/REPRODUCE.md`, an independent Python verifier (`my_reproduce_check.py`) was written directly from the mathematical definition quoted in `claim/CLAIM.md` and executed against `claim/object/qutrit_14_3_8_5.json` and `claim/data/qutrit.php`.

### Real Output of Independent Checker (`my_reproduce_check.py`)

```text
=== 1. File Integrity & Hash Verification ===
claim/object/qutrit_14_3_8_5.json sha256: 7b890c6f3a1b318ef4267bcaec58ec60823b19e6962e7d6f5c721dd3009186e5
claim/data/qutrit.php sha256:             37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c

=== 2. Generator Matrix S over GF(3) & Symplectic Commutation Matrix ===
Shape of S: (16, 28), rank_GF3(S) = 16
rank_GF3(S J S^T) = 10 => c = 5, k = n - s + c = 14 - 16 + 5 = 3

=== 3. Symplectic Dual span(S)^perp and Isotropic Subspace I = span(S) cap span(S)^perp ===
dim_GF3(span(S)^perp) = 12 (3^12 = 531441 vectors)
dim_GF3(I) = dim_GF3(span(S) cap span(S)^perp) = 6 (3^6 = 729 vectors)

=== 4. Exhaustive Symplectic Weight Enumeration of span(S)^perp (531,441 vectors) ===
Number of vectors in I via symplectic orthogonality to span(S)^perp: 729
Minimum symplectic weight on span(S)^perp \ I (530,712 vectors): d = 8
Minimum symplectic weight on I \ {0} (728 vectors):             d_iso = 8
Minimum symplectic weight on span(S)^perp \ {0} (531,440 vectors): d_pure = 8
Weight distribution of span(S)^perp (total 531441): {0: 1, 8: 1736, 9: 5600, 10: 26040, 11: 70112, 12: 148344, 13: 177072, 14: 102536}
Weight distribution of I = span(S) cap span(S)^perp (total 729): {0: 1, 8: 104, 9: 128, 10: 312, 11: 184}
Weight distribution of span(S)^perp \ I (total 530712): {8: 1632, 9: 5472, 10: 25728, 11: 69928, 12: 148344, 13: 177072, 14: 102536}

=== 5. Independent Verification of GF(9) Dual Matrix H9 ===
Verified: GF(3)-span of H9 (via u = x + w*z <-> (x|z)) equals span(S)^perp (dimension 12).
Symplectic rank on H9_gf3 = span(S)^perp: rank_GF3(H9_gf3 J H9_gf3^T) = 6 (nullity = 6 = dim_GF3(I))
Verified: H9_self_orthogonal_seed is Hermitian self-orthogonal (H0 * H0^dagger = 0) and scaling columns [0, 1, 2] by 4 in GF(9) yields H9 exactly.

=== 6. Verification of Saved Table Snapshot claim/data/qutrit.php ===
Matched table cell in claim/data/qutrit.php: ['<TD NOWRAP bgcolor="#00ccff" class="EAQECC" title="reducing length of [[19,3,7;0]] from codetables.de">[[14,3,7-10;5]]<sub>3</sub></TD>']

ALL INDEPENDENT CHECKS PASSED.
```

## 3. Step-by-Step Verification Summary

1. **File Hashes**:
   - `claim/object/qutrit_14_3_8_5.json` has SHA-256 `7b890c6f3a1b318ef4267bcaec58ec60823b19e6962e7d6f5c721dd3009186e5` (matches `claim/CLAIM.md`).
   - `claim/data/qutrit.php` has SHA-256 `37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c` (matches `claim/CLAIM.md`).
2. **Generator Matrix Rank and Parameters**:
   - `S` in `claim/object/qutrit_14_3_8_5.json` has dimensions `16 x 28` (`2n = 28` for `n = 14`), all entries in `{0, 1, 2}`, and exact row rank `s = 16` over `GF(3)`.
   - The `16 x 16` symplectic commutation matrix `M = S J S^T (mod 3)` with `J = [[0, I_14], [2 I_14, 0]] (mod 3)` is skew-symmetric and has rank `10` over `GF(3)`, confirming `c = rank(M)/2 = 5 >= 1` and `k = n - s + c = 14 - 16 + 5 = 3`.
3. **Symplectic Dual and Isotropic Subspace**:
   - The symplectic dual `span(S)^perp = {v in GF(3)^28 : S J v^T = 0 (mod 3)}` has `GF(3)`-dimension `2n - s = 12` (`3^12 = 531,441` vectors).
   - The isotropic subspace `I = span(S) ∩ span(S)^perp` has `GF(3)`-dimension `s - 2c = 6` (`3^6 = 729` vectors), verified both via `ker(M)` on `S` and via direct row-space reduction of all `531,441` dual vectors against `RREF(S)` and `RREF(I)`.
4. **Exhaustive Symplectic Weight Distribution**:
   - Across all `530,712` vectors in `span(S)^perp \ I`, the exact minimum symplectic weight is `d = 8` (attained by `1,632` vectors).
   - Across all `728` nonzero vectors in `I \ {0}`, the exact minimum symplectic weight is `d_iso = 8` (attained by `104` vectors).
   - Across all `531,440` nonzero vectors in `span(S)^perp \ {0}`, the exact minimum symplectic weight is `8` (attained by `1,736` vectors), confirming the code is pure (`[[14, 3, 8; 5]]_3`).
   - Exact symplectic weight enumerators:
     - `span(S)^perp`: `A_0 = 1, A_8 = 1736, A_9 = 5600, A_10 = 26040, A_11 = 70112, A_12 = 148344, A_13 = 177072, A_14 = 102536` (sum = `531,441`).
     - `I = span(S) ∩ span(S)^perp`: `A_0 = 1, A_8 = 104, A_9 = 128, A_10 = 312, A_11 = 184` (sum = `729`).
     - `span(S)^perp \ I`: `A_8 = 1632, A_9 = 5472, A_10 = 25728, A_11 = 69928, A_12 = 148344, A_13 = 177072, A_14 = 102536` (sum = `530,712`).
5. **`GF(9)` Dual Matrix `H9` & Seed Verification**:
   - Under the standard `GF(9) = GF(3)[w]/(w^2 + 1)` isomorphism `x + w z <-> (x | z)`, the `12` `GF(3)`-rows generated by `H9` and `w H9` have `GF(3)`-rank `12` and span the exact same `12`-dimensional subspace as `span(S)^perp`.
   - `H9_self_orthogonal_seed` is verified to be strictly Hermitian self-orthogonal over `GF(9)` (`H_0 H_0^\dagger = 0`), and scaling its first three columns (`[0, 1, 2]`) by `4 = 1 + w in GF(9)` reproduces `H9` entry-for-entry.
6. **Table Bound Check**:
   - In `claim/data/qutrit.php`, cell `(n=14, k=3, c=5)` is `[[14,3,7-10;5]]_3` (`d_lower = 7, d_upper = 10`). The verified distance `d = 8` satisfies `7 < 8 <= 10`.

## 4. Author's Reproduction Command (`claim/REPRODUCE.md`)

Running `python3 check_eaqecc.py object/qutrit_14_3_8_5.json` and `python3 check_eaqecc.py --selftest` inside `claim/` produced:

```text
VALID [[14, 3, 8; 5]]_3 (s=16, dim_dual=12, dim_iso=6, non_iso_vecs=530712)
PASS
SELF_TEST POSITIVE: VALID [[3, 1, 3; 2]]_3 (s=4, dim_dual=2, dim_iso=0, non_iso_vecs=8)
SELF_TEST NEGATIVE 1 (tie rejected): Computed d=3 is not strictly greater than d_lower=3
SELF_TEST NEGATIVE 2 (rank-deficient rejected): Generator matrix S is not full rank: rank=3 != s=4
```

pass: true