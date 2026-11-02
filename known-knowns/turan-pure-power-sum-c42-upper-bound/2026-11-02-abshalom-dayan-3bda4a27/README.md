# C_42 >= 501/1000: an explicit lower bound for Turan's pure power sum constant

## What

For every positive integer n and all complex z_1,...,z_n with max|z_i| = 1, max_{1<=k<=n}|z_1^k+...+z_n^k| > 501/1000, so Turan's pure power sum constant C_42, as defined at https://teorth.github.io/optimizationproblems/constants/42a.html, satisfies C_42 >= 501/1000, strictly above the explicit lower bound 1/2 listed there when fetched at 2026-10-31T22:02:55Z; this rests on an unrefereed written proof whose finite hypotheses on a binary64 table were machine-checked (Arb for LATE, GAP, TERM and INIT, and outward-rounded binary64 intervals on all 4,022,400 table cells for HJB, taking Apple libm as accurate to 4 ulps, which is assumed and not proved), and 501/1000 has not been compared with Biro's constant c from Indag. Math. 11 (2000) 343-358, whose explicit value appears neither on that page nor in the open pull requests fetched at 2026-10-31T22:02:56Z.

Path note: claim/ of the run maps to this folder; CLAIM.md = README.md; REPRODUCE.md = RUN_IT_YOURSELF.md; claim/code/ = verify-it-yourself/ and how-we-built-it/; claim/table/ = the-record-we-beat/. V_b.npy (32199440 bytes, sha256 b1712e642ea9a80c1731556369451bb7afb4dcfab14fa71a218c3351440def0c) ships split at 900 KB in object/V_b_parts/; RUN_IT_YOURSELF.md joins it. Not shipped: panel/claim.sha256, attempts/, data/gate_fetch/, logs/ (final lines and a coverage count are in verify-it-yourself/RECEIPTS.md), code/negctl.py. checker2.c, named in a comment of check2.c, is check2.c.

The proof is object/PROOF.md. It reduces the bound to finite inequalities on a table V, a function on a grid of 1601 x 2514 nodes. object/CERT.md says how they are checked.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. About 2 minutes on a laptop. This checks exact small cases and a few rows only. The check of all rows takes about 40 minutes on two cores and is in RUN_IT_YOURSELF.md.

## Compared to

Table: https://teorth.github.io/optimizationproblems/constants/42a.html, lower bound of C_42, fetched 2026-10-31T22:02:55Z. Best explicit value there: 1/2 (Biro 1994). The next line, ">1/2" (Biro 2000), is a computable constant with no value stated. Bar: 1/2, margin 1/1000. See the-record-we-beat/record.md.

## Not claimed

No value of Biro's constant is computed here, so there is no comparison with it. No optimality. No formal verification. The upper bound is not touched. The plan in how-we-built-it/PREREG.md asked for two independent interval checkers; the value-function step has one (check2.c), plus a float checker with a pad and a sampled Arb check. The target's criterion asks only for interval certification. The id in INDEX.csv says upper-bound because that one target covers both directions.

## Credits

G. Biro, Indag. Math. 11 (2000) 343-358 (https://users.renyi.hu/~biroand/pdfs/Turan1.pdf): formula (14) is (F2) in the proof, and the barrier at rho = 1/sqrt2 is the geometry of that paper. Not found in what we searched: the test functional with fixed beta and gamma at each time, and the value function with its certificate. The ray lemma is an elementary concavity remark. Page of record: optimization constants table, entry 42a, https://teorth.github.io/optimizationproblems/constants/42a.html. Credit for this package: Abshalom Dayan.
