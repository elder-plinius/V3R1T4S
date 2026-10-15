# CRITERION skeptic verdict: risk-or-safety-exact-optimal-play, run 2026-10-15-0312

What I looked at: only the claim package (every file named below is relative to claim/), plus arXiv:2603.01002. I fetched the abs page and the PDF once each, and both returned HTTP 200. The paper is v1 of 1 Mar 2026, 12 pages; the PDF sha256 is 88978bcfbe6bc5af5ca9456de471d53b5b4a4478985e2952b8490bf5d652aa91. I ran every regeneration step outside claim/, so claim/ was not modified. All the checks I wrote myself use only the Python 3 standard library.

## Success criterion (verbatim, as quoted in claim.md)

> Exact reduced rationals A387261(n)/A387262(n) - the starting player's win probability from (0 open, 0 banked, 0 banked) under optimal play by both players - for EVERY n from 16 through 30 (direction: new terms), each with a certificate: the claimed value P(a, b, c) for every position (a open and b banked points of the player to move, c banked by the opponent) and the claimed action, satisfying exactly P(a, b, c) = max(continue, stop) for a >= 1 and the forced toss for a = 0, where continue = (1/2)(1 - P(0, c, b)) + (1/2) P(a + 1, b, c) and stop = 1 - P(0, c, a + b), with P = 1 when a + b >= n (equations of Sections 3-4 of arXiv:2603.01002), all checked in exact arithmetic. The same code must reproduce the published terms for n <= 15 (or certify a correction, see p1).

Partial wins (verbatim): "p1: A certified correction: an exact Bellman certificate showing that a published value (A387261/A387262, n <= 15) or a published optimal action (paper Table 1 / A394776, n <= 20) is not optimal. p2: Certified exact terms for n = 16..20 only (the range where the paper gives strategies but no exact probabilities)."

## Checklist

| # | Requirement | Result |
|---|---|---|
| i | Exact reduced rationals for EVERY n = 16..30 (15 terms) | PASS. values.txt and the claim.md table both have exactly n = 16..30 (values.txt also has 1..15). Each value is reduced (gcd = 1), lies strictly in (0,1), equals the P000 field and the (0,0,0) row of object/nK.json with K = n, and is identical in claim.md. |
| ii | The value is "the starting player's win probability from (0,0,0) under optimal play by both" | PASS. The paper's position triple is (open, saved of the player to move, saved of the opponent) (Sec. 3), and it calls P(0,0,0) "a winning probability of 6/11 (54.54 %) for the player who starts" (n = 3). The equations have a unique solution (the argument is checked below), so a table that satisfies them is the game value. A Monte Carlo of the prose rules agrees with P(0,0,0) and rules out the reversed convention. |
| iii | Certificate lists P(a,b,c) and an action for EVERY position | PASS. For every n the row set equals exactly {0<=b<n, 0<=c<n, 0<=a<n-b}, with no duplicates and no extras. The row counts are n^2(n+1)/2 = 2176, 2601, 3078, 3610, 4200, 4851, 5566, 6348, 7200, 8125, 9126, 10206, 11368, 12615, 13950. Every row has an action in {toss, stop}. Terminal positions (a+b >= n) are never listed: they are fixed at P = 1 by the rule. |
| iv | Equations hold exactly: forced toss at a = 0, max(continue, stop) at a >= 1, P = 1 when a+b >= n | PASS at every position of all 15 certificates, with the claimed action attaining the max everywhere. There are 0 exact ties in any certificate. The smallest gap \|continue - stop\| is 1.469e-06 at n = 16 and 5.151e-10 at n = 30. |
| v | All checked in exact arithmetic | PASS. checker/ros_cert_check.py uses fractions.Fraction only, with no floats on the check path. solver/my_verify.py uses integer cross-multiplication. My own checker uses fractions.Fraction with strict parsing and covered all 30 certificates, not just n = 16 and 30. All three pass. |
| vi | The same code reproduces the published terms for n <= 15 | PASS. One invocation of solver/solver.py regenerates calibration/n1..n15, object/n16..n30 and values.txt byte-for-byte (31/31 identical). The output is also identical when the OEIS b-files are not supplied, so they are not an input. P(0,0,0) for n = 1..15 equals the numerator in data/b387261.txt and the denominator in data/b387262.txt, term by term (15/15). n = 1..6 also match the values printed in the paper. |

### Real output of the package's own steps (run by me)

- `shasum -a 256 -c SHA256SUMS`: 38 of 38 lines `OK`.
- `checker/ros_cert_check.py object/n16.json ... object/n30.json`: 15 lines ending ` PASS`, then `ALL_PASS`, exit 0. Each `positions_checked=` equals n^2(n+1)/2 and each P000 equals values.txt. The first line in full:
  `n16.json: n=16 positions_checked=2176 P000=1599710761252635467097849938052769718961535662524/3090007892803332518177914010771390705108642578125 PASS`
- `checker/ros_cert_check.py --oeis data calibration/n1.json ... n15.json`: 15 lines with `oeis_match=yes PASS`, then `ALL_PASS`, exit 0.
- `solver/my_verify.py --oeis data calibration/n*.json object/n*.json`: `my_verify summary: 30 passed, 0 failed, of 30 certificates`. All 30 lines show `exact_ties=0`, and the 15 calibration lines show `OEIS-MATCH`.
- `solver/solver.py 30 SCRATCH 1 30 SCRATCH/values.txt --b-dir data`: printed `exact ties (cont == stop) found: 0` and `OEIS comparison n<=15: ALL MATCH`. `cmp` then reported calibration n1..n15, object n16..n30 and values.txt all identical (31/31). Re-running without `--b-dir` gave the same: `identical without b-files: 30 of 30` and `values.txt identical without b-files`.

### Real output of my own exact checker (stdlib fractions; written from the criterion text)

My checker enforces the following:

- **Structure:** top-level keys exactly {n, P000, table}; the file name agrees with n.
- **Rows:** integer coordinates; values as canonical reduced "p/q" in [0,1].
- **Completeness:** the row set equals the full position set.
- **Equations:** the forced-toss equation and toss action at a = 0; the max equation at a >= 1, with the claimed action attaining it; P = 1 for a+b >= n.
- **Consistency:** P000 equals the table, and values.txt and claim.md agree with the certificates.

```
PASS object/n16.json    n=16 rows= 2176 (=n^2(n+1)/2= 2176) equations_checked= 2176 stop= 1655 toss(a>=1)=  265 exact_ties=0 min|cont-stop|=1.469e-06 P000=0.517704425603049
PASS object/n17.json    n=17 rows= 2601 (=n^2(n+1)/2= 2601) equations_checked= 2601 stop= 2010 toss(a>=1)=  302 exact_ties=0 min|cont-stop|=1.469e-06 P000=0.517242617083992
PASS object/n18.json    n=18 rows= 3078 (=n^2(n+1)/2= 3078) equations_checked= 3078 stop= 2413 toss(a>=1)=  341 exact_ties=0 min|cont-stop|=1.469e-06 P000=0.516681859313322
PASS object/n19.json    n=19 rows= 3610 (=n^2(n+1)/2= 3610) equations_checked= 3610 stop= 2867 toss(a>=1)=  382 exact_ties=0 min|cont-stop|=1.210e-06 P000=0.516292651289050
PASS object/n20.json    n=20 rows= 4200 (=n^2(n+1)/2= 4200) equations_checked= 4200 stop= 3375 toss(a>=1)=  425 exact_ties=0 min|cont-stop|=9.537e-07 P000=0.515818532255379
PASS object/n21.json    n=21 rows= 4851 (=n^2(n+1)/2= 4851) equations_checked= 4851 stop= 3939 toss(a>=1)=  471 exact_ties=0 min|cont-stop|=4.063e-07 P000=0.515484661790567
PASS object/n22.json    n=22 rows= 5566 (=n^2(n+1)/2= 5566) equations_checked= 5566 stop= 4562 toss(a>=1)=  520 exact_ties=0 min|cont-stop|=1.270e-07 P000=0.515076930847961
PASS object/n23.json    n=23 rows= 6348 (=n^2(n+1)/2= 6348) equations_checked= 6348 stop= 5247 toss(a>=1)=  572 exact_ties=0 min|cont-stop|=4.228e-08 P000=0.514786395838939
PASS object/n24.json    n=24 rows= 7200 (=n^2(n+1)/2= 7200) equations_checked= 7200 stop= 5998 toss(a>=1)=  626 exact_ties=0 min|cont-stop|=4.228e-08 P000=0.514430866458121
PASS object/n25.json    n=25 rows= 8125 (=n^2(n+1)/2= 8125) equations_checked= 8125 stop= 6817 toss(a>=1)=  683 exact_ties=0 min|cont-stop|=4.278e-09 P000=0.514175024603996
PASS object/n26.json    n=26 rows= 9126 (=n^2(n+1)/2= 9126) equations_checked= 9126 stop= 7708 toss(a>=1)=  742 exact_ties=0 min|cont-stop|=4.278e-09 P000=0.513861422906692
PASS object/n27.json    n=27 rows=10206 (=n^2(n+1)/2=10206) equations_checked=10206 stop= 8673 toss(a>=1)=  804 exact_ties=0 min|cont-stop|=4.278e-09 P000=0.513633869914842
PASS object/n28.json    n=28 rows=11368 (=n^2(n+1)/2=11368) equations_checked=11368 stop= 9716 toss(a>=1)=  868 exact_ties=0 min|cont-stop|=5.151e-10 P000=0.513354548066449
PASS object/n29.json    n=29 rows=12615 (=n^2(n+1)/2=12615) equations_checked=12615 stop=10840 toss(a>=1)=  934 exact_ties=0 min|cont-stop|=5.151e-10 P000=0.513150422843286
PASS object/n30.json    n=30 rows=13950 (=n^2(n+1)/2=13950) equations_checked=13950 stop=12048 toss(a>=1)= 1002 exact_ties=0 min|cont-stop|=5.151e-10 P000=0.512899554429881
values.txt n=16: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=49 den=49
values.txt n=17: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=55 den=55
values.txt n=18: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=62 den=62
values.txt n=19: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=66 den=67
values.txt n=20: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=74 den=75
values.txt n=21: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=81 den=81
values.txt n=22: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=89 den=90
values.txt n=23: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=95 den=95
values.txt n=24: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=104 den=105
values.txt n=25: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=111 den=111
values.txt n=26: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=121 den=121
values.txt n=27: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=125 den=125
values.txt n=28: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=138 den=138
values.txt n=29: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=146 den=146
values.txt n=30: reduced=yes in(0,1)=True equals_cert_P000=True equals_claim_md=True digits num=151 den=152
values.txt n=1..15 equal calibration P000: True
MY_CHECK: ALL_PASS
```

The same run also passed all 15 calibration certificates; their lines are omitted here. A strict JSON scan, which rejects duplicate keys and NaN/Infinity, gave: `strict JSON scan: 30 files, no duplicate keys, no NaN/Infinity`.

### Independent replication (my code; does not use the solver)

I ran float value iteration from P = 0 on the paper's Sec. 4 equations, in the original (a,b,c) coordinates. I took the policy (stop iff stop > continue) from that, then computed the policy's exact values with Fractions. I compared every value and action with the certificate.

```
n=16 float_sweeps=  3863 min_float_gap=1.469e-06 max|float-exact|=4.86e-16 positions=2176 value_mismatches=0 action_mismatches=0 exact_P000_equals_cert=True REPLICATED
n=17 ... n=29: all REPLICATED, 0 value and 0 action mismatches
n=30 float_sweeps=  7227 min_float_gap=5.151e-10 max|float-exact|=1.11e-15 positions=13950 value_mismatches=0 action_mismatches=0 exact_P000_equals_cert=True REPLICATED
REPLICATION: ALL_REPLICATED
```

The float error (about 1e-15) is about six orders of magnitude below the smallest action gap (5e-10), so the float-derived policy is reliable.

## Hidden quantifiers and stretched definitions

1. **"Optimal play by both players" needs more than satisfying the equations.** It also needs the solution to be unique, so that it is THE value. The proof note's argument is sound:
   - |max(x1,x2) - max(y1,y2)| <= max_i |x_i - y_i|, and the 1 - P terms preserve differences. So |P-Q|(s) <= max over actions of E|P-Q|(successor).
   - Stops are isolated: a stop leads to a = 0, where a toss is forced. So any 2n consecutive steps contain at least n tosses.
   - With probability at least 2^-n, whatever the strategies, the first n of those tosses are all heads. Then the first tosser either reaches n or banks at least 1.
   - The banked total stays at most 2n-2. Hence r_K <= 1 - 2^(-n(2n-1)) < 1 for K = 2n(2n-1), so D <= D r_K, which forces D = 0.
   - A unique solution of these Bellman equations is the minimax value, and the argmax stationary strategies are optimal for both players. This is the standard optional-stopping argument, valid because play ends with probability 1. That also means there are no draws, so 1 - P is the opponent's win probability.
   - The paper's Sec. 2 asserts the same uniqueness, citing Theorem 2 of Glenn et al. and Shapley.
2. **Ties.** There are none in any of the 30 certificates; all three checkers agree. So every claimed action is the unique optimal action, and no tie convention is involved.
3. **Terminal rule.** "P = 1 when a + b >= n" is the paper's rule:
   - Sec. 2, n = 3, at (0,2,0): "If player 1 tosses heads they win"; and stopping "after 3. throw" gives y2 = 7/8 x2.
   - Sec. 4: "if a+b=n, then Pmin(a, b, c) := Pmax(a, b, c) := 1".
4. **The equations are the paper's.**
   - The forced toss is the paper's rule: Sec. 1, "A player whose turn it is tosses a coin"; Sec. 4, "For any b and c, we have P(0, b, c) = 1/2 (1-P(0, c, b)) + 1/2 P(1, b, c)".
   - Sec. 4 gives the continue and stop equations exactly in the criterion's form.
5. **Same game as the paper.**
   - P(0,0,0) matches the paper's printed values for n = 1..6.
   - The other values printed in the paper also match: for n = 2, P(0,1,1) = 2/3 and P(0,0,1) = 2/5; for n = 3, the values 8/9, 8/11, 4/11, 2/9, 4/5, 2/3, 4/7, 2/5.
   - Table 1 (the number of coins for i, j = 2..20) matches the first-stop count in object/n20.json in 361 of 361 entries, and object/n16..n19 match it on every entry with i, j <= n.
   - The prose strategies in Sec. 3.2/3.3 (n = 3, 4) list fewer stops than the certificates. The extra stops are at positions those strategies never reach from (0,0,0). For n = 4, two of them, (1,1,0) and (2,0,1), are what the paper's own Table 1 prescribes. Evaluated exactly, the n = 4 prose strategy also gives 2236/4165. This is not a conflict.
6. **Nothing in the claim is wider than the certificates.**
   - claim.md says nothing about n > 30, and it says nothing about strategies beyond the action column.
   - Its process statements ("written independently", "written before any solver ran") cannot be checked from the package. They don't affect the verdict, because my checker and replication are independent of the package code.
   - checker/ros_cert_check.py does not itself test that table entries are reduced, because Fraction normalises them. The criterion requires only the final terms to be reduced, and my checker and solver/my_verify.py confirm that every entry is reduced anyway.

## Null models

No statistical null model is needed. The claim is a deterministic exact identity check on an explicit object, with no sampling or inference. What does need testing is whether the checkers can reject wrong objects, and whether the semantics are right. Both were done.

Mutation tests. All 10 mutants were rejected by all three checkers. M7 and M8 are "null" certificates: they satisfy every forced-toss equation and every equation for the claimed action exactly, but follow a suboptimal policy.

```
--- n = 16 ---
M1   value at (1, 8, 5) perturbed by +1e-60                         mine=FAIL(forced toss fails at (0, 8, 5)) | ros_cert_check=FAIL | my_verify=FAIL
M2   action at (1, 1, 0) flipped stop->toss                         mine=FAIL(claimed action does not attain max at (1, 1, 0)) | ros_cert_check=FAIL | my_verify=FAIL
M3   row (3,2,5) deleted                                            mine=FAIL(position set differs: missing 1, extra 0) | ros_cert_check=FAIL | my_verify=FAIL
M4   row (3,2,5) relabelled as duplicate (3,2,6)                    mine=FAIL(duplicate (3, 2, 6)) | ros_cert_check=FAIL | my_verify=FAIL
M5   P000 field changed to 1/2                                      mine=FAIL(P000 field != table (0,0,0)) | ros_cert_check=FAIL | my_verify=FAIL
M6   a=0 row (0,4,4) action set to stop                             mine=FAIL(a=0 not toss at (0, 4, 4)) | ros_cert_check=FAIL | my_verify=FAIL
M7   NULL exact values of policy w/ (2, 0, 0) stop->toss (P000 0.512928229188 vs 0.517704425603) mine=FAIL(max equation fails at (1, 0, 0)) | ros_cert_check=FAIL | my_verify=FAIL
M8   NULL min-gap (3, 1, 14) (gap 1.47e-06) flipped, 151 values change mine=FAIL(max equation fails at (3, 1, 14)) | ros_cert_check=FAIL | my_verify=FAIL
--- n = 30 ---
M1   value at (1, 15, 10) perturbed by +1e-60                       mine=FAIL(forced toss fails at (0, 15, 10)) | ros_cert_check=FAIL | my_verify=FAIL
M8   NULL min-gap (4, 2, 28) (gap 5.15e-10) flipped, 811 values change mine=FAIL(max equation fails at (4, 2, 28)) | ros_cert_check=FAIL | my_verify=FAIL
MUTATION_TESTS: ALL_REJECTED_BY_ALL_THREE_CHECKERS
```

Semantic check, independent of the equations. I simulated the paper's prose rules with both players following object/n16.json, with the first mover as player A:

```
n=16 games=400000 first-mover wins=0.51819 (SE 0.00079); certificate P(0,0,0)=0.51770; z=0.61; z vs 1-P(0,0,0)=45.4
```

## Partial wins and subsumption

- **Partial wins.** The result meets the full criterion: all 15 terms n = 16..30, with certificates and calibration. This includes and supersedes p2 (n = 16..20). p1 is not claimed, and none of my checks found a correction: the n <= 15 values match the data/ snapshot 15/15, and Table 1 matches 361/361.
- **Subsumption.**
  - Neither claim.md nor the paper publishes an exact value for any n >= 16.
  - The paper says the (0,0,0) probabilities are in A387261/A387262 "for n up to 15". It prints exact values only for n <= 6, and its Table 1 gives coin counts, not probabilities.
  - claim.md's status record says OEIS lists n = 1..15 only.
- **Two dependencies outside my remit.** Checking the live OEIS page belongs to the NOVELTY skeptic. The calibration match is against the package's OEIS snapshot (data/b387261.txt, data/b387262.txt; header "b-file synthesized from sequence entry", hash listed in claim.md). The paper independently confirms n = 1..6 of it.

confirmed_scope: For each n = 16, ..., 30, the reduced fraction given for n in values.txt and claim.md is P(0,0,0) of object/nK.json with K = n, which lists a value and an action at every one of the n^2(n+1)/2 non-terminal positions and satisfies the criterion's equations exactly in rational arithmetic (P = 1 when a + b >= n, forced toss at a = 0, P = max(continue, stop) for a >= 1 with the listed action attaining the max and no exact ties), so by the proof note's uniqueness argument (checked sound) it is the starting player's win probability from (0, 0, 0) under optimal play in the game of Sections 1-4 of arXiv:2603.01002, and the same solver, re-run, regenerates all 30 certificates byte-for-byte with its n = 1..15 values equal to the A387261/A387262 terms in the package's OEIS snapshot (data/), n = 1..6 also equal to the values printed in the paper.

context: subagent

pass: true
