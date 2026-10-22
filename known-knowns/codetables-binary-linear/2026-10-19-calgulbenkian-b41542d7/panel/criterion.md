context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report: lpub-q5-n66-k11-d44

Cell: [66,11] over GF(5), claimed new upper bound 44 (certificate excludes d = 45, the live upper bound). Target id named by README.md: codetables-binary-linear. Win claimed: p2. The contributor's hash list checked from inside the package folder: all files OK.

## Target coverage 

Bank statement (verbatim from the target's success criterion): "For given [n,k] over GF(q), codetables.de (Grassl) records the best known lower and upper bounds on the maximum minimum distance d. A linear code with d larger than the tabulated lower bound is a new record. Binary tables cover n <= 256." The success criterion reads "a k x n generator matrix over GF(q)" and "the live http://www.codetables.de/ cell for (q,n,k)"; the p2 text reads "no [n,k,d] code over GF(q) exists". Only the target id (codetables-binary-linear), the sentence "Binary tables cover n <= 256" and the bank's verification method (Gaussian elimination over GF(2), 2^k) are binary-specific. So the literal criterion text covers q = 4, 5, 7, 8, 9; the id and the verification method suggest the maintainers had q = 2 in mind. All three merged claims for this target in the pull-request list (#142, #158, #163) are q = 2; the q = 4 filings (#90 to #101) were closed unmerged in the bulk close, so there is no maintainer precedent either way for q other than 2. The live table does hold q = 4, 5, 7, 8, 9 cells (the pages below were fetched and parse), and the same live table page family is the status source.

## The named partial win p2, clause by clause

p2 text (verbatim from the target's success criterion): "An improved upper bound: a re-checkable certificate (exact rational LP dual certificate, or an exhaustive non-existence classification with code the skeptic re-runs) proving that no [n,k,d] code over GF(q) exists for d equal to the live codetables.de upper bound, thereby lowering it."

My own check (a checker written from the Delsarte definition, not shipped in this package; I did not read or run the author's verifier scripts or receipts for this cell). Definition used: for a code of size M and minimum distance at least d in the Hamming scheme H(n,q), if f(x) = f_0 + sum_(j=1..deg) f_j K_j(x) with f_0 = 1, every f_j at least 0 and f(i) at most 0 for all integers i from d to n, then M is at most f(0) (K_j the q-ary Krawtchouk polynomial, K_j(x) = sum_s (-1)^s (q-1)^(j-s) C(x,s) C(n-x,j-s)). The object's y_multipliers_rational are f_1 to f_deg. With exact Fractions I got:

lpub-q5-n66-k11-d44
q,n,k,deg,excluded d 5 66 11 7 45
f(0)= 780563323041959590575285019658599/18052872647294449094322360 43237624.1882447  q^k= 48828125  claim P0: 780563323041959590575285019658599/18052872647294449094322360
matches claimed P0: True
max_{d<=i<=n} f(i) = -215005848724218069709240936097/430012301591482311884182722641920 -0.0004999992975281824  <=0: True  matches claimed: True
f(0) < q^k: True
CERT VALID (code of size q^k and distance >=d impossible): True
claim fields: {'d_lo_codetables': 38, 'd_ub_codetables': 45, 'd_ub_ruled_out': 45, 'd_ub_new': 44}

- Certificate exact and dual-feasible: met. All multipliers are positive rationals, f(i) is negative at every integer i from 45 to 66 (the maximum is the small negative value printed above), and f(0) is below q^k, so no code with q^k words and distance at least 45 exists in H(66,5); a linear [66,11,45] code would have exactly q^k words. The values f(0) and max f printed match those in the object.
- Excluded distance equals the live upper bound: met. Live cell fetched once by me: http://www.codetables.de/BKLC/BKLC.php?q=5&n=66&k=11 at 2026-10-19T05:21:46Z, HTTP 200, page sha256 1e895e2039327b4e5f7f937354d6b46af141ba8499f01bdb196837148077ca97; it reads lower bound 38, upper bound 45; the object's recorded live bounds (38, 45) agree.
- Lowers it (new bound 44 strictly below everything implied by the live table and merged/open pull requests): met on the evidence I could gather. One-step propagation from the live neighbours I fetched: shorten (n-1,k-1): live upper 45, implied 45; puncture (n-1,k) + 1: live upper 44, implied 45; subcode (n,k-1): live upper 45, implied 45; pad (n+1,k): live upper 45, implied 45; none is below 45. Multi-step closure over every cell I fetched around the cell (n-2..n+2, k-1..k+1; own script, not shipped in this package) leaves the upper bound at 45. The neighbour pages (all HTTP 200): (5,65,10) 2026-10-19T05:21:40Z sha b1bd181cdf5e; (5,65,11) 2026-10-19T05:21:41Z sha 36e1e2aa80b8; (5,66,10) 2026-10-19T05:21:44Z sha bb2df87369b4; (5,67,11) 2026-10-19T05:21:50Z sha fd8d8f08f311. Pull requests: I searched titles in a snapshot of all V3R1T4S pull requests (473 pull requests, fetched 2026-10-19T04:30:31Z) for upper-bound or q = 5 claims on this cell or its neighbours and found none; the merged binary-linear claims (#142, #158, #163) are lower-bound codes at other cells and imply no upper bound here. Multi-step propagation reaching beyond the cells I fetched cannot be excluded from my data; the live page's own derivation chain for this cell cites a Griesmer chain (cell excerpt in the folder), not a stronger argument.
- Plain Delsarte LP is a legitimate certificate: yes, the criterion names "exact rational LP dual certificate" without further restriction (Open question 1). Whether the table's value was left at 45 because nobody ran the LP rather than a stronger argument excluding d = 45: a stronger argument would have lowered the bound already, and my LP certificate is a proof by itself, so the point does not affect validity.
- Open question 2 (other propagation rules): none I know of beyond the four one-step rules and their closure, which I tested. Open question 3 (second Krawtchouk implementation): done; my f was built with my own integer-binomial Krawtchouk code and matches the object exactly.



Fetch note: I fetched each page below once (curl with the honest user agent, no retry); times are UTC from the machine clock, status 200 for all.

confirmed_scope: Exact-rational Delsarte LP dual certificate (degree 7) that no (unrestricted or linear) code of length 66, size 5^11 and minimum distance at least 45 exists over an alphabet of size 5, so U(5,66,11) is at most 44 against the live table value 45; not implied by one-step propagation from the live neighbours I fetched; the target-scope reading for q = 5 follows the literal GF(q) text of the criterion (the target id and merged precedent are binary).

pass: true
