context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report: lpub-q4-n148-k7-d106

Cell: [148,7] over GF(4), claimed new upper bound 106 (certificate excludes d = 107, the live upper bound). Target id named by README.md: codetables-binary-linear. Win claimed: p2. The contributor's hash list checked from inside the package folder: all files OK.

## Target coverage 

Bank statement (verbatim from the target's success criterion): "For given [n,k] over GF(q), codetables.de (Grassl) records the best known lower and upper bounds on the maximum minimum distance d. A linear code with d larger than the tabulated lower bound is a new record. Binary tables cover n <= 256." The success criterion reads "a k x n generator matrix over GF(q)" and "the live http://www.codetables.de/ cell for (q,n,k)"; the p2 text reads "no [n,k,d] code over GF(q) exists". Only the target id (codetables-binary-linear), the sentence "Binary tables cover n <= 256" and the bank's verification method (Gaussian elimination over GF(2), 2^k) are binary-specific. So the literal criterion text covers q = 4, 5, 7, 8, 9; the id and the verification method suggest the maintainers had q = 2 in mind. All three merged claims for this target in the pull-request list (#142, #158, #163) are q = 2; the q = 4 filings (#90 to #101) were closed unmerged in the bulk close, so there is no maintainer precedent either way for q other than 2. The live table does hold q = 4, 5, 7, 8, 9 cells (the pages below were fetched and parse), and the same live table page family is the status source.

## The named partial win p2, clause by clause

p2 text (verbatim from the target's success criterion): "An improved upper bound: a re-checkable certificate (exact rational LP dual certificate, or an exhaustive non-existence classification with code the skeptic re-runs) proving that no [n,k,d] code over GF(q) exists for d equal to the live codetables.de upper bound, thereby lowering it."

My own check (a checker written from the Delsarte definition, not shipped in this package; I did not read or run the author's verifier scripts or receipts for this cell). Definition used: for a code of size M and minimum distance at least d in the Hamming scheme H(n,q), if f(x) = f_0 + sum_(j=1..deg) f_j K_j(x) with f_0 = 1, every f_j at least 0 and f(i) at most 0 for all integers i from d to n, then M is at most f(0) (K_j the q-ary Krawtchouk polynomial, K_j(x) = sum_s (-1)^s (q-1)^(j-s) C(x,s) C(n-x,j-s)). The object's y_multipliers_rational are f_1 to f_deg. With exact Fractions I got:

lpub-q4-n148-k7-d106
q,n,k,deg,excluded d 4 148 7 3 107
f(0)= 258051632794969/16695880740 15456.005994144936  q^k= 16384  claim P0: 258051632794969/16695880740
matches claimed P0: True
max_{d<=i<=n} f(i) = -3314519539249/6629049360174780 -0.0004999992244983992  <=0: True  matches claimed: True
f(0) < q^k: True
CERT VALID (code of size q^k and distance >=d impossible): True
claim fields: {'d_lo_codetables': 103, 'd_ub_codetables': 107, 'd_ub_ruled_out': 107, 'd_ub_new': 106}

- Certificate exact and dual-feasible: met. All multipliers are positive rationals, f(i) is negative at every integer i from 107 to 148 (the maximum is the small negative value printed above), and f(0) is below q^k, so no code with q^k words and distance at least 107 exists in H(148,4); a linear [148,7,107] code would have exactly q^k words. The values f(0) and max f printed match those in the object.
- Excluded distance equals the live upper bound: met. Live cell fetched once by me: http://www.codetables.de/BKLC/BKLC.php?q=4&n=148&k=7 at 2026-10-19T05:20:01Z, HTTP 200, page sha256 fe717030bf07d85ba648d9cdaee69d419745f2d3b65c4f24c93413be36c95254; it reads lower bound 103, upper bound 107; the object's recorded live bounds (103, 107) agree.
- Lowers it (new bound 106 strictly below everything implied by the live table and merged/open pull requests): met on the evidence I could gather. One-step propagation from the live neighbours I fetched: shorten (n-1,k-1): live upper 108, implied 108; puncture (n-1,k) + 1: live upper 106, implied 107; subcode (n,k-1): live upper 108, implied 108; pad (n+1,k): live upper 107, implied 107; none is below 107. Multi-step closure over every cell I fetched around the cell (n-2..n+2, k-1..k+1; own script, not shipped in this package) leaves the upper bound at 107. The neighbour pages (all HTTP 200): (4,147,6) 2026-10-19T05:19:55Z sha 24d7d8ac0c4e; (4,147,7) 2026-10-19T05:19:56Z sha c3ba1cabb085; (4,148,6) 2026-10-19T05:19:59Z sha b5f0e08a333e; (4,149,7) 2026-10-19T05:20:05Z sha fb9cff310e78. Pull requests: I searched titles in a snapshot of all V3R1T4S pull requests (473 pull requests, fetched 2026-10-19T04:30:31Z) for upper-bound or q = 4 claims on this cell or its neighbours and found none; the merged binary-linear claims (#142, #158, #163) are lower-bound codes at other cells and imply no upper bound here. Multi-step propagation reaching beyond the cells I fetched cannot be excluded from my data; the live page's own derivation chain for this cell cites a Griesmer chain (cell excerpt in the folder), not a stronger argument.
- Plain Delsarte LP is a legitimate certificate: yes, the criterion names "exact rational LP dual certificate" without further restriction (Open question 1). Whether the table's value was left at 107 because nobody ran the LP rather than a stronger argument excluding d = 107: a stronger argument would have lowered the bound already, and my LP certificate is a proof by itself, so the point does not affect validity.
- Open question 2 (other propagation rules): none I know of beyond the four one-step rules and their closure, which I tested. Open question 3 (second Krawtchouk implementation): done; my f was built with my own integer-binomial Krawtchouk code and matches the object exactly.



Fetch note: I fetched each page below once (curl with the honest user agent, no retry); times are UTC from the machine clock, status 200 for all.

confirmed_scope: Exact-rational Delsarte LP dual certificate (degree 3) that no (unrestricted or linear) code of length 148, size 4^7 and minimum distance at least 107 exists over an alphabet of size 4, so U(4,148,7) is at most 106 against the live table value 107; not implied by one-step propagation from the live neighbours I fetched; the target-scope reading for q = 4 follows the literal GF(q) text of the criterion (the target id and merged precedent are binary).

pass: true
