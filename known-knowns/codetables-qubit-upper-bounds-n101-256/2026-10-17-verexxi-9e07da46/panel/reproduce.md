# REPRODUCE report: no [[165,6,53]] qubit stabilizer code (bank entry codetables-qubit-upper-bounds-n101-256)

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)

## Verdict in brief

The Farkas certificate result/cert_165_6_53_sh.json verifies in exact integer arithmetic with a checker I wrote myself from the LP definition before opening check/, and also with the shipped check/check_cert.py (output byte-identical to check/checker_output.txt). The live codetables.de page for [[165,6]] still shows lower bound 31 and upper bound 53 (byte-identical to the claim-time page). The propagation closure of all live cells at (165,6) is 53, so the new bound 52 is not implied. Both checkers and the propagation scripts were each run at least twice with identical output (deterministic). I found no mismatch.

## 0. Scope and package integrity

- I used only the claim package (CLAIM.md, REPRODUCE.md, result/, check/, data/) plus plain public GET requests to codetables.de. My scratch files are in the sibling folder work/ (mycheck.py, explore1.py, explore2.py, mycheck2.py, controls.py, myprop.py, trace.py and the live downloads).
- Python 3.14.4 (`python --version`; python and python3 both resolve to it here). Start of session, `date -u`: Sat Oct 17 05:25:54 UTC 2026.
- `sha256sum` of the claim files at start (the three hashes CLAIM.md states match): result/cert_165_6_53_sh.json 9e07da46bfb2114321ecb503f02a06c0546dd5f018b0e30f1973c8c4cf2135f4; data/qubit_table_full_n1-256.html 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6; data/QECC_q4_n165_k6_claimtime.html 2ab973981689cd1731fa749a17b6cc4d48c6eb1e956fbc0658ef732dcdc33bb2; check/check_cert.py 3c4e89d40124f80751290db7b9190387cdbd6590d4fd48f25ac9c7e996cf3fe4.
- At 05:37:01 UTC `sha256sum -c` over all 11 files of claim/ reported OK for every file, so nothing in the package was altered by my runs.
- The certificate JSON has exactly the keys n, k, d, shadow, u_E0, u_E1, u_Q, v_G, v_H; n,k,d = 165, 6, 53; shadow true. No duplicate JSON keys (checked with a duplicate-rejecting parser) and every multiplier is a plain ASCII decimal integer string (checked by regex).

## 1. My own checker (written before reading check/)

The definition I worked from, quoted from REPRODUCE.md item 2 (and the same LP is in the success criterion of CLAIM.md). The ASCII comparison signs are transcribed as the Unicode symbols ≤ and ≥, and the strict one as the words less than, so that this report contains no angle-bracket characters; the wording is otherwise verbatim:

```
variables A_0..A_n ≥ 0, the weight distribution of the stabilizer S of an [[n,k,d]] code
(|S| = 2^(n-k)); B_j = 2^-(n-k) sum_i K_j(i) A_i is the weight distribution of the normalizer
(quaternary MacWilliams identity) and Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i that of the shadow
(Rains); K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s). Every [[n,k,d]] code satisfies A_0 = 1,
sum A_i = 2^(n-k), A_j = B_j for 1 ≤ j (less than) d, A_j ≤ B_j for j ≥ d, Sh_j ≥ 0. The certificate gives integer
multipliers (sign-free on equalities, nonnegative on inequalities) whose combination has every column
coefficient ≤ 0 and a positive right-hand side, which no nonnegative A can satisfy (Farkas' lemma). The
certificate's rows are the LP rows multiplied by 2^(n-k) (integer coefficients).
```

My rows (T = 2^(n-k) = 2^159, all coefficients integers, columns i = 0..165):
- E0: A_0 = 1 (multiplier u_E0, any sign)
- E1: sum_i A_i = T (u_E1, any sign)
- Q_j for 1 ≤ j ≤ 52: sum_i K_j(i) A_i - T A_j = 0, that is T(B_j - A_j) = 0 (u_Q, any sign)
- G_j for 55 and 56 (both at least d = 53): sum_i K_j(i) A_i - T A_j ≥ 0, that is T(B_j - A_j) ≥ 0 (v_G, must be ≥ 0)
- H_j for j in 0..51, 56, 57: sum_i (-1)^i K_j(i) A_i ≥ 0, that is T Sh_j ≥ 0 (v_H, must be ≥ 0)
- Combination c_i = sum over rows of multiplier times row coefficient at column i; right-hand side R = u_E0 * 1 + u_E1 * T. Certificate condition: c_i ≤ 0 for every i and R positive.

What had to be inferred, stated honestly: CLAIM.md and REPRODUCE.md do not say which row each key means or how the equality rows are oriented (equality multipliers are sign-free, so the orientation is part of the certificate format). I took E0, E1 as the two normalisations, u_Q as the equalities j = 1..d-1 (the key range is exactly 1..52), v_G as A_j ≤ B_j rows (keys 55, 56 are at least d), v_H as shadow rows. My first attempt (work/mycheck.py, run 05:29:03 UTC, exit 1) used T A_j - sum K_j(i) A_i for Q and failed for all four scalings of E0/E1 (113, 3, 113, 3 positive columns). I then tried all 8 sign patterns of the three equality-row groups times the 4 scalings (32 combinations, work/explore2.py). Exactly one combination has no positive column and a positive right-hand side: E0 unscaled, E1 unscaled, Q oriented as sum_i K_j(i) A_i - T A_j. The G and H rows were never sign-searched: they are used only in their true orientation (B_j - A_j ≥ 0, Sh_j ≥ 0) with the given multipliers, all of which are positive. Flipping the sign of an equality row is a legitimate rewrite of the same constraint. After this I opened check/check_cert.py and its docstring states exactly this convention.

Final checker, `python -I work/mycheck2.py result/cert_165_6_53_sh.json`, run at 05:31:16 UTC, twice, exit 0 both times, identical output (sha256 25365264c71212d785331c59bf684096c7c26e22c0bb555810bccce089e77a36). Output lines:
- selftests OK (K_0, K_1, orthogonality, symmetry, MacWilliams/shadow on [[5,1,3]] and Steane [[7,1,3]])
- rows: E0, E1, Q_1..Q_52 (52), G_j for j in [55, 56], H_j for 54 j-values (0..51 and [56, 57])
- multiplier signs: u_E0 +, u_E1 -, all u_Q negative, all v_G positive, no v_H equal to zero, all v_H ≥ 0
- Krawtchouk table K_j(i), j = 0..57, i = 0..165: binomial formula equals a binomial-free polynomial product (cross-check OK)
- columns i = 0..165: no column with c_i positive, 1 column with c_i = 0 (i = 63), 165 columns with c_i negative
- RHS R = u_E0 * 1 + u_E1 * 2^159: sign +, bit length 4830 (1454 decimal digits, computed separately at 05:37:01 UTC)
- RESULT: VERIFIED, every column coefficient ≤ 0 and RHS positive, so the LP is infeasible, so no [[165,6,53]] stabilizer code

The check is exhaustive over all 166 columns and all 108 inequality and equality multipliers plus E0 and E1, not a sample.

## 2. The LP definitions checked against real codes (brute force)

work/controls.py enumerates, for three genuine stabilizer codes, the stabilizer group, the full normalizer (all 4^n Paulis commuting with the generators) and the shadow set (all Paulis u with symplectic product with each generator g equal to the weight of g mod 2), and compares with the formulas above:
- [[5,1,3]], Steane [[7,1,3]], Shor [[9,1,3]] (impure): brute-force normalizer enumerator equals MacWilliams B_j (True), brute-force shadow-set enumerator equals Rains Sh_j (True), A_j ≤ B_j for all j (True), A_j = B_j for j below 3 (True) for all three. So the (-1)^i sign convention, the 2^-(n-k) factors and the impure case behave as the LP assumes.

## 3. Negative controls (the checker is not vacuous)

Same arithmetic, modified certificate (work/controls.py):
- baseline: PASS
- all shadow rows removed: FAIL (54 positive columns)
- the two A_j ≤ B_j rows removed: FAIL (53 positive columns)
- u_Q[1] raised by 1: FAIL (1 positive column, necessarily the tight column 63 because every other column has thousands of bits of slack); lowered by 1: still PASS (expected, slack on that side)
- u_E0 negated: FAIL (RHS not positive)
- u_E1 raised by 2^4830: FAIL (161 positive columns)
- v_H[56] sign-flipped (illegal): FAIL (55 positive columns)

So the certificate genuinely needs both the shadow rows and the G rows, and it is exact (one column is tight).

## 4. Shipped checker

`python -I check/check_cert.py result/cert_165_6_53_sh.json`, run at 05:32:00 UTC, twice (0.71 s and 0.68 s), exit 0 both times. Output:

VERIFIED [[165,6,53]] shadow=True: value=1454 digits, max column coefficient ≤ 0, 52+2+54 multipliers

(the file prints the ASCII form of ≤.) sha256 of both outputs 514b3913957a1dd222efb8a68d1d4f64b687245be1399b8bde8d3d47dea9a705, equal to the sha256 of check/checker_output.txt; `diff` reported them identical. The `python3` spelling and a run from inside claim/ exactly as REPRODUCE.md step 1 (exit 0, same line) also agree. The shipped checker uses the same rows and the same Farkas rule as mine (reading it after the fact, it matches my independent implementation row for row; the 1454 digits it reports equal the digit count of my R).

## 5. Propagation check (is 52 implied by other live cells?)

Shipped scripts, run in work/ on the saved table at 05:32:55 UTC:
- `python -I check/parse_table.py data/qubit_table_full_n1-256.html parsed.json` printed: cells 33152 n-range 1 256 (that is exactly the triangle 1 ≤ n ≤ 256, 0 ≤ k ≤ n).
- `python -I check/propagate.py parsed.json closure.json` printed: cells k≥1: 32896, live above implied: 1075, of which n over 100: 1072, n at most 100: 3.
- the one-liner from REPRODUCE.md printed `[31, 53] 53` as expected. parsed.json sha256 1f6b123968ef827e93f9e33c8dbfb87da4e28e2e418b821005857fd0cb16a78b, closure.json sha256 a1310128645030ed4a72f86a8d87570140e392d7655cfe842f922607791b5e3b; a second run gave identical hashes.
- check/propagation_check.txt (live (165,6) = [31, 53], closure 53, neighbours R1 [31, 55], R2 [31, 53], R3 [31, 53]) agrees with what I get.

Independent version (work/myprop.py: my own parser built on html.parser, my own fixed-point loop for the three rules R1 U(n,k) ≤ U(n,k-1) for k ≥ 2, R2 U(n,k) ≤ U(n+1,k), R3 U(n,k) ≤ U(n-1,k+1)+1, k ≥ 1 cells only): same 33152 cells, own parse equals shipped parsed.json for every cell, own closure equals shipped closure.json for every k ≥ 1 cell, and two reruns give identical output. Values at (165,6): live upper 53, lower 31, closure 53. Route candidates from the closure values: R1 via (165,5) live 55, closure 54; R2 via (166,6) 53; R3 via (164,7) live 53 so 54, but its closure is 52 (via (163,8) plus 1), so the candidate is 53. With the (165,6) cell's own value removed (other live cells only) the closure at (165,6) is still 53. Implied bound ≤ 52? False. So the claimed 52 beats everything the three standard rules give from the live table by exactly one.

## 6. Live status (re-fetched today, plain GET with curl -s, 60 s limit for the cell pages and 120 s for the table)

- 2026-10-17T05:33:27Z, GET https://codetables.de/QECC.php?q=4&n=165&k=6 : HTTP 200, 1523 bytes, sha256 2ab973981689cd1731fa749a17b6cc4d48c6eb1e956fbc0658ef732dcdc33bb2 (byte-identical to data/QECC_q4_n165_k6_claimtime.html), parsed: lower 31, upper 53.
- 05:33:29Z, same URL with n=165&k=5 : HTTP 200, sha256 9e2ecbfb2bb127c3d30bae7c7fddacc1801e3c452b8a838a76fae445faa737a0, lower 31 upper 55.
- 05:33:31Z, n=166&k=6 : HTTP 200, sha256 52286358a9a40b03b4e9c3306930b68d5d1d3734244099df7633bcb0e8c43fab, lower 31 upper 53.
- 05:33:33Z, n=164&k=7 : HTTP 200, sha256 e1e5fe295ba3808b5775406e5f3d2594f111ed1ba63e1974aafebafb600748db, lower 31 upper 53.
- 2026-10-17T05:33:47Z, GET https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256 : HTTP 200, 5547032 bytes, sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, and `cmp` says it is byte-identical to data/qubit_table_full_n1-256.html. So nothing in the table changed between the claim-time fetch and now, and 53 is still the live upper bound.
- The saved cell page itself says upper bounds for n above 100 are weak and not necessarily monotone in k, which is why the closure (not just the cell) was computed.

## 7. Re-derivation of the proof steps

1. Setup: a [[165,6,d≥53]] stabilizer code gives an additive self-orthogonal S over GF(4), length 165, |S| = 2^159, normalizer S-perp of size 2^171. A_i counts weight-i elements of S.
2. E0 and E1: A_0 = 1 and sum A_i = |S| = 2^159.
3. MacWilliams: B(x,y) = A(x+3y, x-y)/|S| gives B_j = sum_i K_j(i) A_i / 2^159, and B counts S-perp. Verified by brute force on three codes (section 2).
4. S is contained in S-perp, so A_j ≤ B_j for all j (G rows, used at j = 55, 56).
5. Distance at least 53 means S-perp minus S has no element of weight below 53, so A_j = B_j for 1 ≤ j ≤ 52 (Q rows). The rows used only need distance at least 53, so the conclusion excludes every d ≥ 53, not just d = 53.
6. Shadow: weight is additive mod 2 on S because wt(v+w) = wt(v) + wt(w) + (symplectic product of v and w) mod 2 coordinatewise and S is self-orthogonal; hence the set of u whose symplectic product with v equals wt(v) mod 2 for all v in S is defined by linear conditions, and counting it by character sums gives exactly Sh_j = sum_i (-1)^i K_j(i) A_i / |S| as the number of its weight-j elements, so Sh_j ≥ 0 (H rows; brute-force matched in section 2).
7. Farkas: for any feasible A ≥ 0, sum_i c_i A_i equals R plus a nonnegative combination of the G and H row values, so it is at least R, which is positive; but c_i ≤ 0 and A_i ≥ 0 force sum_i c_i A_i ≤ 0. Contradiction, so the real-valued relaxation (and a fortiori any code) is infeasible. The inequalities c_i ≤ 0 (all 166) and R positive were verified in exact integers by two independent programs.
8. Therefore no qubit stabilizer code [[165,6,d]] with d ≥ 53 exists, so the upper bound is at most 52, one below the live 53, and by section 5 this is not implied by the three propagation rules from other live cells.

Success criterion of CLAIM.md, item by item:
- cell inside 101 ≤ n ≤ 256: n = 165, yes.
- d equals the live table upper bound, re-fetched live right now: 53 at 05:33:27Z, HTTP 200, yes.
- lowers the bound by at least 1: 53 to at most 52, yes.
- exact integer infeasibility certificate (Farkas dual) of the weight-enumerator LP with MacWilliams link, A_j ≤ B_j, A_j = B_j below d, nonnegativity and shadow rows: sections 1 and 4, yes.
- checked by an independent script: my own mycheck2.py (refined from my first attempt; both were written from the definition before I opened check/) and the shipped check_cert.py, yes.
- not implied by R1, R2, R3 applied to other live cells: closure 53, yes (section 5).

## 8. What I did not or could not check

- I cannot re-observe the claim-time timestamps and HTTP statuses stated in CLAIM.md; I can only say the saved files match their stated sha256 values and that today's live pages are byte-identical to them.
- Novelty against the literature beyond the live table is outside this reproduce step. The pinned trophy case in data/ has no match for 165, codetables, qubit, quantum or the bracket notation, so it neither helps nor contradicts.
- The bound is for stabilizer (additive) codes, which is what the success criterion asks for.

pass: true
