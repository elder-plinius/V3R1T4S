context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report: lpub-q2-n163-k18-d71

Cell: [163,18] over GF(2), claimed new upper bound 71 (certificate excludes d = 72, the live upper bound). Target id named by the claim record (not shipped): codetables-binary-linear. Win claimed: p2. The the contributor's hash list was checked from inside the package folder: all files OK.

## Target coverage

Binary cell (q = 2): the target id codetables-binary-linear applies without any scope doubt. Bank statement (verbatim): "For given [n,k] over GF(q), codetables.de (Grassl) records the best known lower and upper bounds on the maximum minimum distance d. A linear code with d larger than the tabulated lower bound is a new record. Binary tables cover n <= 256." 

## The named partial win p2, clause by clause

p2 text (verbatim, the target's success criterion): "An improved upper bound: a re-checkable certificate (exact rational LP dual certificate, or an exhaustive non-existence classification with code the skeptic re-runs) proving that no [n,k,d] code over GF(q) exists for d equal to the live codetables.de upper bound, thereby lowering it."

My own check (a program of my own, not shipped in this package, written from the Delsarte definition; I did not read or run the author's verifier scripts or receipts for this cell). Definition used: for a code of size M and minimum distance at least d in the Hamming scheme H(n,q), if f(x) = f_0 + sum_(j=1..deg) f_j K_j(x) with f_0 = 1, every f_j at least 0 and f(i) at most 0 for all integers i from d to n, then M is at most f(0) (K_j the q-ary Krawtchouk polynomial, K_j(x) = sum_s (-1)^s (q-1)^(j-s) C(x,s) C(n-x,j-s)). The object's y_multipliers_rational are f_1 to f_deg. With exact Fractions I got:

lpub-q2-n163-k18-d71
q,n,k,deg,excluded d 2 163 18 5 72
f(0)= 138327920185042536516573/621000958767257068 222749.9301444493  q^k= 262144  claim P0: 138327920185042536516573/621000958767257068
matches claimed P0: True
max_{d<=i<=n} f(i) = -731566217158668677/1463134713488272857396 -0.000499999221134283  <=0: True  matches claimed: True
f(0) < q^k: True
CERT VALID (code of size q^k and distance >=d impossible): True
claim fields: {'d_lo_codetables': 64, 'd_ub_codetables': 72, 'd_ub_ruled_out': 72, 'd_ub_new': 71}

- Certificate exact and dual-feasible: met. All multipliers are positive rationals, f(i) is negative at every integer i from 72 to 163 (the maximum is the small negative value printed above), and f(0) is below q^k, so no code with q^k words and distance at least 72 exists in H(163,2); a linear [163,18,72] code would have exactly q^k words. The values f(0) and max f printed match those in the object.
- Excluded distance equals the live upper bound: met. Live cell fetched once by me: http://www.codetables.de/BKLC/BKLC.php?q=2&n=163&k=18 at 2026-10-19T05:19:38Z, HTTP 200, page sha256 b747a81b223550784bf9fe377782c47d03c2f1ccbb98f4f8c71f5f8ae744e02a; it reads lower bound 64, upper bound 72; the object's recorded live bounds (64, 72) agree.
- Lowers it (new bound 71 strictly below everything implied by the live table and merged/open pull requests): met on the evidence I could gather. One-step propagation from the live neighbours I fetched: shorten (n-1,k-1): live upper 72, implied 72; puncture (n-1,k) + 1: live upper 72, implied 73; subcode (n,k-1): live upper 72, implied 72; pad (n+1,k): live upper 72, implied 72; none is below 72. Multi-step closure over every cell I fetched around the cell (n-2..n+2, k-1..k+1; own script, not shipped in this package) leaves the upper bound at 72. The neighbour pages (all HTTP 200): (2,162,17) 2026-10-19T05:19:30Z sha 04fbb498b838; (2,162,18) 2026-10-19T05:19:32Z sha cb72b55187a0; (2,163,17) 2026-10-19T05:19:37Z sha 65652289a445; (2,164,18) 2026-10-19T05:19:43Z sha 52294d46e3a9. Pull requests: I searched titles in a snapshot of all V3R1T4S pull requests (473 pull requests, fetched 2026-10-19T04:30:31Z) for upper-bound or q = 2 claims on this cell or its neighbours and found none; the merged binary-linear claims (#142, #158, #163) are lower-bound codes at other cells and imply no upper bound here. Multi-step propagation reaching beyond the cells I fetched cannot be excluded from my data; the live page's own derivation chain for this cell cites a Griesmer chain (cell excerpt in the folder), not a stronger argument.
- Plain Delsarte LP is a legitimate certificate: yes, the criterion names "exact rational LP dual certificate" without further restriction (Open question 1). Whether the table's value was left at 72 because nobody ran the LP rather than a stronger argument excluding d = 72: a stronger argument would have lowered the bound already, and my LP certificate is a proof by itself, so the point does not affect validity.
- Open question 2 (other propagation rules): none I know of beyond the four one-step rules and their closure, which I tested. Open question 3 (second Krawtchouk implementation): done; my f was built with my own integer-binomial Krawtchouk code and matches the object exactly.
- Open question 4 (parity, binary cells): the new bound 71 is odd. A hypothetical [163,18,71] code would give an even-distance code of length 164 with distance 72, consistent with the live upper bound 72 of the next length; the live chain for this cell is a Griesmer chain, not a parity argument, so nothing interacts.

Fetch note: I fetched each page below once (curl with the honest user agent, no retry); times are UTC from the machine clock, status 200 for all.

confirmed_scope: Exact-rational Delsarte LP dual certificate (degree 5) that no (unrestricted or linear) code of length 163, size 2^18 and minimum distance at least 72 exists over an alphabet of size 2, so U(2,163,18) is at most 71 against the live table value 72; not implied by one-step propagation from the live neighbours I fetched; the target-scope reading for q = 2 follows the literal GF(q) text of the criterion.

pass: true
