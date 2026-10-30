# REPRODUCE skeptic report

context: subagent (fresh context, Agent tool, model claude-sonnet-5-5; saw only claim/)

Scope: claim/CLAIM.md says `object/u.txt`, `v.txt`, `w.txt` are an exact bilinear scheme over Q with 3424 products for
<18,19,19>. I read CLAIM.md, REPRODUCE.md, TABLE_RECORD.md and `object/`, wrote my own checker, and only then opened
`verify-it-yourself/` and `rebuild/`. No file in claim/ contains instructions addressed to a reviewer. claim/ was
never modified: its three object sha256 values were re-checked against REPRODUCE.md at the end (all OK). All my files are
in `panel_work/reproduce/`; the claim copy used for the author's scripts is `panel_work/reproduce/claim_copy/`.

## 1. Definition implemented (quoted)

"rank r for <n1,n2,n3> means r products m_k = (sum u_k[i*n2+j] A[i][j]) * (sum v_k[j*n3+l] B[j][l]) with
C[i][l] = sum_k w_k[i*n3+l] m_k equal to (AB)[i][l] for all A, B over Q, i.e. every Brent equation holds exactly."

Expanding C[i'][l'] and comparing the coefficient of A[i][j] B[j'][l] with (AB)[i'][l'] gives, for every
(i,j,j',l,i',l'): `sum_k u_k[i*n2+j] * v_k[j'*n3+l] * w_k[i'*n3+l'] = [i=i'] [j=j'] [l=l']`. For <18,19,19> that is
342 * 361 * 342 = 42224004 equations, which is the count the author also reports.

## 2. My checker (`parse_lib.py`, `my_check.py`, `stats.py`; outputs `stats_output.txt`, `my_check_output.txt`)

- Parser (`parse_lib.py`): strict. It rejects bad tokens, out-of-range or repeated indices, listed zero
  coefficients, non-canonical (unreduced) fractions, carriage returns, a missing trailing newline, and comment lines
  that are not at the top. Result for u, v and w: 5 comment lines, 3424 term lines, 0 parse problems.
- Headers (checked in `my_check.py`): `# format 18 19 19` and `# rank 3424` present exactly once in each file, rank
  equals the number of term lines.
- Exactness: Fractions only. Each file's coefficients are scaled by that file's denominator lcm (u 8400, v 84, w 84;
  product 59270400) to python integers. D[a,b,c] = sum_k U[k,a] V[k,b] W[k,c] - 59270400 * delta must be 0 for all
  (a,b,c). It is computed modulo five primes below 2^20 (1048573, 1048571, 1048559, 1048549, 1048517). float64 BLAS only
  carries integers asserted below 2^53. The bound |D| <= B = 17319104239248 (about 2^44) is computed with python ints,
  and the prime product (about 2^100) is asserted greater than 2B. So D = 0 mod all five primes implies D = 0
  exactly (Chinese remainder theorem). This is an exhaustive check of all equations, not a sample.
- Independent second route: 3 exact Fraction evaluations on random rational A, B (seeded) against AB (a sample, not the
  basis of the verdict).

Output of `my_check.py` on `object/` (copied from `my_check_output.txt`):

```
format <18,19,19>, term lines u/v/w = 3424/3424/3424, terms with three nonzero factors = 3424
per-file denominators lcm: u 8400, v 84, w 84; product 59270400
bound B on |D| = 17319104239248 (about 2^44); primes [1048573, 1048571, 1048559, 1048549, 1048517], product about 2^100
prime 1048573: equations checked 42224004, nonzero residues 0
prime 1048571: equations checked 42224004, nonzero residues 0
prime 1048559: equations checked 42224004, nonzero residues 0
prime 1048549: equations checked 42224004, nonzero residues 0
prime 1048517: equations checked 42224004, nonzero residues 0
BRENT: 42224004 equations checked exhaustively, residues nonzero for (per prime) [0, 0, 0, 0, 0]
random exact trial 1: 0 of 342 entries of C differ from AB
random exact trial 2: 0 of 342 entries of C differ from AB
random exact trial 3: 0 of 342 entries of C differ from AB
elapsed 3.2s
MY CHECKER: PASS (rank 3424, three-nonzero terms 3424, equations 42224004)
```

Other facts from `stats_output.txt`: nonzero entries per factor file u 147881, v 73004, w 65543; denominators occurring
in the files (excluding 1) are 2, 4, 5, 7, 10, 12, 14, 25, 28, 50, 84, 300, 600, 1200, which is exactly the list in
CLAIM.md. Every term has all three factors nonempty: 3424 of 3424, equal to the header rank.

Rerun (`my_check_output_run2.txt`, on `claim_copy/object`): output identical to the first run apart from the elapsed
time (diff printed "MY CHECKER OUTPUT IDENTICAL ON RERUN (excluding elapsed time)").

## 3. sha256 of the object files against REPRODUCE.md

`shasum -a 256 -c` with the three lines copied from REPRODUCE.md (`sha_expected.txt`): `object/u.txt: OK`,
`object/v.txt: OK`, `object/w.txt: OK`. Values: u 47419363a41b203879fe8ae93035fe231852f01eb3081ad15c306a91d1e3298a,
v dbf5c154ad97f11abdefd3d7d9ff1fda723a49710e881124bc547299308a93fa,
w 797187bb905b8ee0dd22f321b802a1009938e2b4905517c1ffa7c576749bfacb. Re-checked on the original `claim/object/` at the
end of the session: all three OK (so the originals were not touched).

## 4. Negative and positive controls (`make_controls.py`, `controls/`, `controls_output.txt`)

Same checker, run on altered copies of `object/`. Each negative control must FAIL and the positive control must PASS.

| control | change | nonzero residues per prime | random exact trial 1 | verdict |
|---|---|---|---|---|
| `neg1_w_coef_plus_1_84` | one coefficient of w, term 1000, plus 1/84 | 2911 (all 5 primes) | 1 of 342 entries differ | FAIL |
| `neg2_u_sign_flip` | one coefficient of u, term 2000, negated | 48 | 6 of 342 differ | FAIL |
| `neg3_drop_last_term` | last term removed everywhere, rank header set to 3423 | 37544 | 2 of 342 differ | FAIL |
| `neg4_swap_two_v_entries` | two coefficients swapped in v, term 500 | 672 | 6 of 342 differ | FAIL |
| `neg5_header_rank_lie` | header says rank 3000, body unchanged | 0 (body still valid) | 0 differ | FAIL (header check: "header says ['3000'], body has 3424 lines") |
| `neg6_duplicate_term` | term 78 replaced by a copy of term 77 | 3128 | 9 of 342 differ | FAIL |
| `pos1_equivalent_rescale` | u_123 x3 with v_123 x1/3, and u_456 and w_456 both x(-1) (products unchanged) | 0 | 0 differ | PASS |

The checker therefore catches a one-coefficient change of size 1/84, structural damage, and a lying header, and does not
reject a valid but differently normalised scheme.

## 5. The author's checks, run from a copy (`author_checks_output.txt`)

`cd claim_copy && sh verify-it-yourself/run_checks.sh`, exit status 0, 39.34 s total. Output:

```
== exact Brent-equation check (check_scheme.py)
format <18,19,19>, 3424 terms, every term with three nonzero factors, common denominator 352800, 42224004 Brent equations checked, 0 wrong
rank 3424 scheme for <18,19,19> over Q verified exactly
PASS
== random exact evaluation against AB (check_random_eval.py)
trial 1: 0 of 342 entries of C differ from AB
trial 2: 0 of 342 entries of C differ from AB
trial 3: 0 of 342 entries of C differ from AB
PASS
PASS
```

A `diff` of this output against the "Expected output" block in REPRODUCE.md printed "AUTHOR OUTPUT MATCHES REPRODUCE.md
EXPECTED BLOCK" (`expected_out.txt` vs `actual_out.txt`). After reading `verify-it-yourself/check_scheme.py` I found
it to be an exact pure-Fraction/integer sparse expansion that also counts missing (never produced) equations as wrong;
it agrees with mine on all counts (3424 terms, 42224004 equations, 0 wrong).

## 6. Rebuild (REPRODUCE.md section 2), run twice (`rebuild_run1.log`, `rebuild_run2.log`)

Done in `claim_copy/` with the venv python (numpy 2.5.4, python-flint 0.9.0), the two runs in parallel.
- `shasum -a 256 rebuild/19x19x19_r3633.npz` = 72633df65c1da7195d1a3284845cf82bf70c5e11c969895a33b7167bd978889b
  (expected value in REPRODUCE.md identical); git blob sha1 computed locally =
  397b9f9d6e99d3105b1464e5f4f0a04679d71fee (equals the value stated in REPRODUCE.md).
- The npz metadata (read by me): tensor [19, 19, 19], rank 3633, coefficient field Q,
  is_complete_matrix_multiplication_scheme True.
- Both runs printed `slice axis 0 -> (18, 19, 19) rank 3425`, `absorbed 1 -> rank 3424`, `wrote 3424 terms`. Each took
  about 76 s CPU. 3633 - 3425 = 208, matching the "208 terms vanish, 3425 remain" statement in CLAIM.md.
- `cmp` of rebuilt (run 1), rebuilt (run 2) and `object/` for u, v, w: all byte-identical; the loop printed `SAME`.
  sha256 of both rebuilt sets equals the object sha256 values above. Deterministic across two runs.

## 7. Not covered by this report

The comparison with 3633 (fmm_sota.json) and 3816 (Lille page) rests on web fetches recorded in TABLE_RECORD.md. I had no
network and did not re-fetch them; that is for another skeptic. What I did confirm is that the object is an exact
rank 3424 scheme and that 3424 < 3633 and 3424 < 3816 as numbers. I also did not judge the p1 classification or the
"composition" clause (the object is a one-slice restriction plus one 2-reduction of the published 19x19x19 r3633
scheme; the rebuild reproduces it, which is what REPRODUCE.md promises).

## Verdict

Every property was confirmed from the saved files by my own exhaustive exact checker: headers, format, three nonzero
factors in all 3424 terms, all 42224004 Brent equations exactly, sha256 values, controls behaving as required, the
author's script output identical to the expected block, and the rebuild reproducing the object byte for byte twice.
No mismatch, missing object or non-determinism found.

pass: true
