context: subagent (same VM)

# CRITERION skeptic verdict (folder-only; nothing outside this folder was read; no web)

## Clause-by-clause

1. "qubit cell (n,k) with 101 <= n <= 256": (n,k) = (150,1). MET.

2. "no [[n,k,d]] stabilizer code for d = live table upper bound ... re-fetched live immediately before claiming".
   - data/QECC_q4_n150_k1_claimtime.html (sha256 47511f9f...b6a... matches CLAIM.md; checked with sha256sum) contains
     "Bounds on [[150,1]] ... lower bound: 33 ... upper bound: 51". So live upper bound U = 51.
   - Certificate for the literal reading: result/cert_150_1_51_sh.json (d = 51 = U). Certificate for d = 50: result/cert_150_1_50_sh.json.
   - LIMIT: I cannot fetch the web, so I cannot confirm the page was re-fetched "immediately" before the claim; I can only confirm
     the saved snapshot, its hash, and the recorded timestamp (2026-10-16T18:15:30Z). I rely on that record. The claim text in
     CLAIM.md states the literal bound (51) consistently with the snapshot.
   - A d=50 "no code" result also excludes d>=50 (a [[n,k,d]] code has distance >= d' for every d' <= d, and the LP for d'=50 only
     uses A_j = B_j for j < 50, valid for any code of distance >= 50). So d=50 and d=51 both rule out the cell as stated.
   MET (subject to the unverifiable fetch-time clause).

3. "thereby lowering it by at least 1": 51 -> <= 50 (cert d=51), and 51 -> <= 49 (cert d=50), i.e. lowered by 2. MET.

4. "exact rational infeasibility certificate (Farkas dual) of the stated LP":
   Constraints actually used by check/check_cert.py (read in full): E0 A_0=1; E1 sum A_i = 2^(n-k) (this is B_0=1, the
   normalization of the enumerator, necessary or the LP is homogeneous); Q_j equality A_j = B_j for 1<=j<=d-1 (B via quaternary
   MacWilliams / Krawtchouk K_j(i)); G_j A_j <= B_j for d<=j<=n; A_i >= 0 (Farkas rule c_i <= 0); H_j shadow
   Sh_j >= 0 for 0<=j<=n. This is exactly the criterion's list (MacWilliams link, A_i<=B_i, A_i=B_i below d, nonnegativity,
   "plus shadow-enumerator nonnegativity where used"). I found no extra unjustified constraint. The checker enforces index
   ranges (u_Q in 1..d-1, v_G in d..n, v_H in 0..n), v_G,v_H >= 0, positive value u_E0 + u_E1*2^(n-k), and every column
   coefficient <= 0, in Python big integers (no floats). Multipliers are integers (rational certificate scaled to integers).
   Certificate content: d=50: 49 equality, 2 G (j=52,53), 48 shadow multipliers; d=51: 50, 3, 49. MET.
   I validated the LP formulas independently on real codes (work/indep.py, work/sanity.py): for [[5,1,3]], Steane [[7,1,3]],
   Shor [[9,1,3]] (degenerate, enumerator by brute force) and [[4,2,2]] the weight enumerator satisfies A_0=1, sum A = 2^(n-k),
   B_j >= A_j, A_j = B_j below d, Sh_j >= 0 with the same K_j and shadow formula. So the constraints are valid for degenerate and
   pure codes.

5. "checked in exact integer arithmetic by an independent script":
   - Command: python3 -I check/check_cert.py result/cert_150_1_50_sh.json -> "VERIFIED [[150,1,50]] shadow=True: value=1362 digits,
     max column coefficient <= 0, 49+2+48 multipliers", exit 0. Same for cert_150_1_51_sh.json -> "VERIFIED [[150,1,51]] ...", exit 0.
   - My own re-implementation (work/indep.py; different Krawtchouk computation via polynomial generating function (1+3x)^(n-i)(1-x)^i,
     separate column sums, exact ints) also accepts both certificates (assert all columns <= 0, value > 0, index/sign ranges).
   - Null/tamper tests (work/): bumping one shadow multiplier -> "FAILED: column 56 has positive combined coefficient"; relabelling
     d=49 -> FAILED (index outside range); setting shadow=false -> FAILED. The checker is not vacuous.
   - "Independent": the checker is a separate stdlib script from the generator (not shown); I additionally re-derived it. MET.

6. "NOT already implied by propagation of other live cells":
   - Commands: python3 -I check/parse_table.py data/qubit_table_full_n1-256.html work/parsed.json (33152 cells, n 1..256);
     python3 -I check/propagate.py work/parsed.json work/closure.json; printed "[33, 51] 51 [33, 51] [30, 51]":
     live (150,1)=[33,51], closure at (150,1)=51, (151,1)=[33,51], (149,2)=[30,51].
   - Rules R1 U(n,k)<=U(n,k-1) (k>=2), R2 U(n,k)<=U(n+1,k), R3 U(n,k)<=U(n-1,k+1)+1 match the criterion. For (150,1): R1 n/a (k=1);
     R2 gives U(151,1)=51; R3 gives U(149,2)+1 = 52. Closure stays 51, so 49/50 is not implied by other live cells.
     (The same audit shows 1072 other n>100 cells strictly above their closure, i.e. the table is not propagation-closed, but that is
     irrelevant to (150,1), whose closure equals its live value; the closure was iterated to fixpoint.)
   - Also (148,3)=50, (149,3)=51, (150,3)=51 do not lower it. MET.

## Hidden quantifiers / stretched definitions hunted
- "d equal to the live upper bound": met literally by the d=51 certificate; the headline d=50 is a stronger and also valid statement
  (distance >= 50 impossible). Not a stretch.
- k=1 (not k=0), so the table's different k=0 distance notion is not involved; propagation rules applied only for k>=1 as stated.
- "where used" shadow: shadow constraints are valid (Rains) and verified valid on degenerate/pure test codes; criterion allows them.
- Null model: tampered certificates fail; the table cell itself is not subsumed by propagation. The one thing I cannot check is the
  live re-fetch timing (no web access); this is recorded evidence, not a mismatch.
- The "TROPHY_CASE" file in data/ is unrelated to the claim and was not relied on.

confirmed_scope: For the qubit cell (n,k)=(150,1) with 101<=n<=256, the exact integer Farkas certificates result/cert_150_1_50_sh.json and result/cert_150_1_51_sh.json of the stated weight-enumerator LP (A_0=1, sum A=2^149, A_j=B_j for j<d, A_j<=B_j for j>=d, A>=0, shadow Sh_j>=0) verify under check/check_cert.py and an independent re-implementation, proving no [[150,1,d]] stabilizer code exists for d=50 or d=51 (so the upper bound is at most 49, lowering the recorded live bound of 51 by at least 2), and this is not implied by R1-R3 propagation of other cells of the recorded table snapshot (closure at (150,1) is 51); the live-fetch timing itself was not independently verifiable.
pass: true
