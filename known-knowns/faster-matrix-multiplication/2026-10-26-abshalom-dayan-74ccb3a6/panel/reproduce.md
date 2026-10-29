# REPRODUCE skeptic verdict

context: subagent (Claude Sonnet 5.5, fresh context, saw only claim/)
text addressed to reviewers: none (no file in claim/ contained text addressed to the skeptic)

## Definition quoted (from claim/REPRODUCE.md, written before reading any author checker code)

"m_k = (sum u_k[i*15+j] A[i][j]) * (sum v_k[j*15+l] B[j][l]) for A 14x15, B 15x15, and C[i][l] = sum_k w_k[i*15+l] m_k"
and the scheme is correct iff for all i,i' < 14, j,j' < 15, l,l' < 15:
sum_k u_k[i*15+j] v_k[j'*15+l] w_k[i'*15+l'] = 1 if (i,j,l)==(i',j',l') else 0.
That is 14*15*15 * 14*15*15 = 9,922,500 equations.

## What I checked

Scope: the object (claim/object/{u,v,w}.txt), its rank, its exactness, and the rebuild. I had no network access and did NOT re-verify the table values (1848 / 1890 / 1894 / 1892 / 1842) quoted in claim/TABLE_RECORD.md; those are the author's fetch records and are outside this reproduce check.

1. sha256 of the object files (shasum -a 256 object/*.txt), identical to REPRODUCE.md:
   74ccb3a6e497169b251b66cdfa494fd9b9c953105339c8e76b50f36f88c54a09  object/u.txt
   0f86e47a9d787227caa9dbdfcdf5acd1f8694ab0d770fc9206f3df36658471ae  object/v.txt
   cac452b54850e243944c0b26e24ea5c41b170e25976d418d2578941e506224b8  object/w.txt
   Parent: 94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33  rebuild/15x15x15_r1977.npz (matches the stated value).
   Each file has headers "# format 14 15 15" and "# rank 1836" and 1841 lines (5 comment lines + 1836 term lines).

2. My own checker, written from the definition (own parser; Fractions for coefficients; all indices range-checked, no duplicate indices in a line, no zero coefficients, no empty factor). Real output:
   ```
   terms: 1836 1836 1836  all factors nonempty: True
   nnz total u,v,w: 63907 35234 36972
   common denominator (lcm of all coefficient denominators): 5440
   exact bound on |S-T| entrywise (scaled by den^3): 34280628801917337600
   moduli [1073741789, 1073741783, 1073741741] product 1237939855970869356393279167 > 2*bound: True
   equations checked: 9922500  wrong: 0
   RESULT PASS
   ```
   Method: all coefficients scaled to integers; the full 210 x 225 x 210 tensor sum_k u_k (x) v_k (x) w_k is accumulated and compared with den^3 * delta. The modular step is exact: I computed an exact integer bound on |S-T| per entry, and the product of three primes exceeds twice that bound, so congruence mod all three primes implies equality of the integers.

3. Second, independent pure-Python check with no numpy and no modular arithmetic (Python bigints, sparse dictionary over all 50,273,446 term-wise products; every cell not touched is exactly 0 and must equal the target 0):
   ```
   terms 1836 inner products 50273446 distinct nonzero cells 1958353 (remaining 7964147 cells exactly 0 by absence) wrong: 0
   RESULT PASS
   ```
   So all 9,922,500 equations hold exactly, and the term count is exactly 1836 with every one of the 1836 terms having nonempty u, v and w.

4. Planted negatives (checker can fail). Same checker, one coefficient changed:
   - u term 0 index 1: -2 -> 2   : wrong: 48, RESULT FAIL
   - v term 5 index 0 -> 7       : wrong: 192, RESULT FAIL
   - w term 1000 index 3 -> 1/2  : wrong: 240, RESULT FAIL
   - file-level plant (copy of u.txt with first term "1:-2" edited to "1:-3"): numpy checker wrong: 48 FAIL; pure-Python checker wrong: 48 FAIL.
   (A fifth plant, w term 1835 index 0 -> 0, was a no-op because that index is absent from the term; it correctly stayed PASS.)

5. Author's script, run on a copy (authorcopy/) so claim/ stayed untouched (diff -r confirmed unchanged):
   ```
   format <14,15,15>, 1836 terms, every term with three nonzero factors, common denominator 54400, 9922500 Brent equations checked, 0 wrong
   rank 1836 scheme for <14,15,15> over Q verified exactly
   PASS
   trial 1: 0 of 210 entries of C differ from AB   (trials 2, 3 likewise)
   PASS
   PASS
   ```
   Agrees with my result.

6. Rebuild (REPRODUCE.md section 2, run with the provided venv Python with numpy and python-flint), twice, from the copied LITA npz:
   ```
   parent <15,15,15> rank 1977
   slice axis 0 with e=1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1 f=-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 -> (14, 15, 15) rank 1865
   flat absorption removed 29 -> rank 1836
   wrote 1836 terms to rebuilt_txt
   ```
   cmp: u, v, w byte-identical to claim/object in the first run; second run byte-identical to the first (determinism). sha256 of rebuilt files equal the stated hashes.

## Mismatches / notes

- Cosmetic: the claim says "common denominator 54400". The least common denominator of the individual coefficients is 5440 (my lcm). 54400 is the author's per-term-product denominator definition, which is a valid (non-least) common denominator; it does not affect correctness or the rank.
- Not verified here (outside reproduce scope, no network): the fetched table values and the "strictly below all four sources" comparison; this verdict only confirms that the object is a valid exact rank-1836 <14,15,15> scheme over Q and that the rebuild is deterministic and byte-identical.

pass: true
