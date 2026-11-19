# How We Found It

*Contributor text, unverified.*

## Why Naive Truncations Fail

Kunisky's recursive lift `phi` doubles the column count (`4 -> 8 -> 16`), reaching `2.06066` on `T_4` (`16` columns), while row/column deletion or row-merging to `15` columns with uniform column normalization drops the discrepancy to `1.49578 < 2.0`, and 15-leaf binary tree SOCPs reach `2.04653`.

## What Worked

Applying a 7-row partial lift (`7 * 2 + 1 = 15` columns) to `phi(Ex. 2.2)` (`8x8`) breaks full row symmetry into three structural orbits (`12` split main rows, `2` split partner rows, and `1` unsplit row). Solving the coupled 2-orbit Weiszfeld second-order cone scaling program and rationalizing inward to denominator `10^{12}` yielded exact discrepancy `2.05956508661 > 2.006`.
