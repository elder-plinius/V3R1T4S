context: subagent
panel_role: criterion
target_id: eaqecc-qutrit-codetables-gaps
confirmed_scope: The artifact `claim/object/qutrit_14_3_8_5.json` (`sha256: 7b890c6f3a1b318ef4267bcaec58ec60823b19e6962e7d6f5c721dd3009186e5`) gives an explicit, pure, non-catalytic qutrit entanglement-assisted quantum error-correcting code `[[14, 3, 8; 5]]_3` via a `16 x 28` symplectic generator matrix `S` over `GF(3)` (and its `6 x 14` dual generator matrix `H9` over `GF(9)`) whose exact minimum symplectic distance `d = 8` on `span(S)^perp \ (span(S) ∩ span(S)^perp)` (and on `span(S)^perp \ {0}`) strictly improves the lower bound `d_lower = 7` in `[[14, 3, 7-10; 5]]_3` for `(n=14, k=3, c=5)` on `https://eaqecc.codetables.de/qutrit.php` (`claim/data/qutrit.php`, `sha256: 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c`).

## Clause-by-Clause Verification of Verbatim Success Criterion

1. **Explicit EAQECC with parameters `[[n,k,d;c]]_3` and `c >= 1` (`c = 0` excluded):**
   - Verified in `claim/object/qutrit_14_3_8_5.json`: `q = 3` (qutrit), `n = 14`, `k = 3`, `d = 8`, `c = 5 >= 1` (`c != 0`).

2. **Exact generator matrix over `GF(3)` (symplectic form, `2n` columns) or over `GF(9)`:**
   - `claim/object/qutrit_14_3_8_5.json` provides both:
     - `S`: an explicit `16 x 28` matrix over `GF(3) = {0, 1, 2}` with `2n = 28` columns under the standard symplectic form `J = [[0, I_14], [2 I_14, 0]] (mod 3)`.
     - `H9`: the corresponding `6 x 14` generator matrix over `GF(9) = GF(3)[w]/(w^2 + 1)` whose `GF(3)`-expansion spans the `12`-dimensional symplectic dual `span(S)^perp` (`S J R_28^T = 0 mod 3`, `rank_GF3(R_28) = 12`).

3. **Number of independent generators `s`, entangled pairs `c`, and logical qutrits `k`:**
   - Independent row rank over `GF(3)`: `s = rank_GF3(S) = 16` on Alice's `n = 14` qutrits.
   - Symplectic commutation matrix `Omega = S J S^T mod 3` (`16 x 16` skew-symmetric over `GF(3)`) has `rank_GF3(S J S^T) = 10`, so `c = rank_GF3(S J S^T) / 2 = 5`.
   - Logical qutrits: `k = n - s + c = 14 - 16 + 5 = 3`.
   - This is a direct stabilizer specification in the non-catalytic setting (not a catalytic reduction from a code with larger `k` and `c`).

4. **Exact minimum distance `d` on `span(S)^perp \ (span(S) ∩ span(S)^perp)`:**
   - Exhaustive enumeration of all `3^{28 - 16} = 3^{12} = 531,441` vectors in `span(S)^perp = { v in GF(3)^{28} : S J v^T = 0 mod 3 }` confirms:
     - `|span(S) ∩ span(S)^perp| = 3^{16 - 10} = 729` (the isotropic subgroup has dimension `s - 2c = 6`).
     - On `span(S)^perp \ (span(S) ∩ span(S)^perp)` (`530,712` vectors), the minimum symplectic weight is `d = 8` (attained by `1,632` vectors), with weight distribution `{8: 1632, 9: 5472, 10: 25728, 11: 69928, 12: 148344, 13: 177072, 14: 102536}`.
     - On `(span(S) ∩ span(S)^perp) \ {0}` (`728` nonzero isotropic vectors), the minimum symplectic weight is also `8` (attained by `104` vectors), with weight distribution `{8: 104, 9: 128, 10: 312, 11: 184}`.
     - Consequently, the code is pure (`min_{v in span(S)^perp \ {0}} wt_symp(v) = 8`) and satisfies `d = 8` under both the standard EAQECC definition (`span(S)^perp \ (span(S) ∩ span(S)^perp)`) and the pure distance definition (`span(S)^perp \ {0}`).

5. **Comparison against the live table `https://eaqecc.codetables.de/qutrit.php` (`claim/data/qutrit.php`):**
   - In `claim/data/qutrit.php` (`sha256: 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c`), the cell `(n=14, k=3)` lists the entries `[[14,3,5-6;0]]_3`, `[[14,3,6-7;1]]_3`, `[[14,3,7-10;5]]_3`, `[[14,3,8-11;6]]_3`, `[[14,3,9-11;7]]_3`, `[[14,3,10-11;10]]_3`, and `[[14,3,11-12;11]]_3`.
   - Specifically, for `(n=14, k=3, c=5)`, the table entry is `<TD NOWRAP bgcolor="#00ccff" class="EAQECC" title="reducing length of [[19,3,7;0]] from codetables.de">[[14,3,7-10;5]]<sub>3</sub></TD>`, giving `d_lower = 7` and `d_upper = 10`.
   - Our verified minimum distance `d = 8` satisfies `d = 8 > d_lower = 7` (strict improvement) and `d = 8 <= d_upper = 10`.
   - Moreover, it is not subsumed by any entry with fewer entangled pairs (`c = 0` has `d_lower = 5`, `c = 1` has `d_lower = 6`, and no entry for `c in {2, 3, 4}` has `d_lower >= 8`), and it improves upon the `c = 6` entry `[[14,3,8-11;6]]_3` by achieving `d = 8` with `c = 5` entangled pairs.

pass: true
