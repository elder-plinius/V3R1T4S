context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report: lpub-q4-n153-k7-d110

Cell: [153,7] over GF(4), claimed new upper bound 110 (certificate excludes d = 111, the live upper bound). Target id named by README.md: codetables-binary-linear. Win claimed: p2. The contributor's hash list checked from inside the package folder: all files OK.

## Target coverage 

Bank statement (verbatim from the target's success criterion): "For given [n,k] over GF(q), codetables.de (Grassl) records the best known lower and upper bounds on the maximum minimum distance d. A linear code with d larger than the tabulated lower bound is a new record. Binary tables cover n <= 256." The success criterion reads "a k x n generator matrix over GF(q)" and "the live http://www.codetables.de/ cell for (q,n,k)"; the p2 text reads "no [n,k,d] code over GF(q) exists". Only the target id (codetables-binary-linear), the sentence "Binary tables cover n <= 256" and the bank's verification method (Gaussian elimination over GF(2), 2^k) are binary-specific. So the literal criterion text covers q = 4, 5, 7, 8, 9; the id and the verification method suggest the maintainers had q = 2 in mind. All three merged claims for this target in the pull-request list (#142, #158, #163) are q = 2; the q = 4 filings (#90 to #101) were closed unmerged in the bulk close, so there is no maintainer precedent either way for q other than 2. The live table does hold q = 4, 5, 7, 8, 9 cells (the pages below were fetched and parse), and the same live table page family is the status source.

## The named partial win p2, clause by clause

p2 text (verbatim from the target's success criterion): "An improved upper bound: a re-checkable certificate (exact rational LP dual certificate, or an exhaustive non-existence classification with code the skeptic re-runs) proving that no [n,k,d] code over GF(q) exists for d equal to the live codetables.de upper bound, thereby lowering it."

My own check (a checker written from the Delsarte definition, not shipped in this package; I did not read or run the author's verifier scripts or receipts for this cell). Definition used: for a code of size M and minimum distance at least d in the Hamming scheme H(n,q), if f(x) = f_0 + sum_(j=1..deg) f_j K_j(x) with f_0 = 1, every f_j at least 0 and f(i) at most 0 for all integers i from d to n, then M is at most f(0) (K_j the q-ary Krawtchouk polynomial, K_j(x) = sum_s (-1)^s (q-1)^(j-s) C(x,s) C(n-x,j-s)). The object's y_multipliers_rational are f_1 to f_deg. With exact Fractions I got:

lpub-q4-n153-k7-d110
q,n,k,deg,excluded d 4 153 7 3 111
f(0)= 4553875121138905/347381819532 13109.134862826098  q^k= 16384  claim P0: 4553875121138905/347381819532
matches claimed P0: True
max_{d<=i<=n} f(i) = -228728499114701/457457044068924372 -0.0004999999498974571  <=0: True  matches claimed: True
f(0) < q^k: True
CERT VALID (code of size q^k and distance >=d impossible): True
claim fields: {'d_lo_codetables': 107, 'd_ub_codetables': 111, 'd_ub_ruled_out': 111, 'd_ub_new': 110}

- Certificate exact and dual-feasible: met. All multipliers are positive rationals, f(i) is negative at every integer i from 111 to 153 (the maximum is the small negative value printed above), and f(0) is below q^k, so no code with q^k words and distance at least 111 exists in H(153,4); a linear [153,7,111] code would have exactly q^k words. The values f(0) and max f printed match those in the object.
- Excluded distance equals the live upper bound: met. Live cell fetched once by me: http://www.codetables.de/BKLC/BKLC.php?q=4&n=153&k=7 at 2026-10-19T05:20:23Z, HTTP 200, page sha256 71f001d419d57ec63a8fb4c51b7c7d9a5fa891abd59bc50c841e896c614c7ccb; it reads lower bound 107, upper bound 111; the object's recorded live bounds (107, 111) agree.
- Lowers it (new bound 110 strictly below everything implied by the live table and merged/open pull requests): met on the evidence I could gather. One-step propagation from the live neighbours I fetched: shorten (n-1,k-1): live upper 112, implied 112; puncture (n-1,k) + 1: live upper 110, implied 111; subcode (n,k-1): live upper 112, implied 112; pad (n+1,k): live upper 111, implied 111; none is below 111. Multi-step closure over every cell I fetched around the cell (n-2..n+2, k-1..k+1; own script, not shipped in this package) leaves the upper bound at 111. The neighbour pages (all HTTP 200): (4,152,6) 2026-10-19T05:20:17Z sha 0708fb8fc43a; (4,152,7) 2026-10-19T05:20:18Z sha 26c89db75b34; (4,153,6) 2026-10-19T05:20:21Z sha bb924e2ae6a8; (4,154,7) 2026-10-19T05:20:27Z sha 8a490a1c4191. Pull requests: I searched titles in a snapshot of all V3R1T4S pull requests (473 pull requests, fetched 2026-10-19T04:30:31Z) for upper-bound or q = 4 claims on this cell or its neighbours and found none; the merged binary-linear claims (#142, #158, #163) are lower-bound codes at other cells and imply no upper bound here. Multi-step propagation reaching beyond the cells I fetched cannot be excluded from my data; the live page's own derivation chain for this cell cites a Griesmer chain (cell excerpt in the folder), not a stronger argument.
- Plain Delsarte LP is a legitimate certificate: yes, the criterion names "exact rational LP dual certificate" without further restriction (Open question 1). Whether the table's value was left at 111 because nobody ran the LP rather than a stronger argument excluding d = 111: a stronger argument would have lowered the bound already, and my LP certificate is a proof by itself, so the point does not affect validity.
- Open question 2 (other propagation rules): none I know of beyond the four one-step rules and their closure, which I tested. Open question 3 (second Krawtchouk implementation): done; my f was built with my own integer-binomial Krawtchouk code and matches the object exactly.



Fetch note: I fetched each page below once (curl with the honest user agent, no retry); times are UTC from the machine clock, status 200 for all.

confirmed_scope: Exact-rational Delsarte LP dual certificate (degree 3) that no (unrestricted or linear) code of length 153, size 4^7 and minimum distance at least 111 exists over an alphabet of size 4, so U(4,153,7) is at most 110 against the live table value 111; not implied by one-step propagation from the live neighbours I fetched; the target-scope reading for q = 4 follows the literal GF(q) text of the criterion (the target id and merged precedent are binary).

pass: true
