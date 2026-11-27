# Criterion skeptic

Criterion (claim/CLAIM.md): new exact term of A006821 (listed) at first order beyond live b-file, two independent methods agreeing exactly, same code reproducing the published terms of the sequence and its disconnected version via inverse Euler.

## Clause 1: new term beyond the b-file
- claim/data/b006821.txt last line: `14 322040154704144697047052726990` (N=28); fetch record: HTTP 200, refetched 2026-11-24. Claimed term is n=15 (N=30): 1690586697346784893842479211750187. A006821 is an enumerated sequence, and n=15 is the first order past the b-file. MET. (Novelty search of the web was not redone by me; the human's check is in data/HUMAN_NOVELTY_CHECK.md.)

## Clause 2: two independent methods agree exactly
- Rerun in a scratch copy: `python3 -I methodD/dsumcheck.py 30 methodA/A_terms_d5.txt results/Dd5_N30_lane0.txt results/Dd5_N30_lane1.txt` printed `N=30 types=5604 U_D=1690586697369281612308192667831589 U_A=1690586697369281612308192667831589 AGREE`. 5604 = p(30), so every cycle type is covered.
- Spot check (REPRODUCE check 3), pure-Python and C short part: 156656509541307 twice, matching the saved row.
- Independence: A (methodA/cubic.c, engine.py, driver.py) is a histogram elimination recurrence in C, with CRT over word-size primes. D (methodD/D.py, Dd.py, Ddsym*.py, Svdp.py/svdp.c) is a vertex DP for the fixed points and 2-cycles plus a count-vector DP for the longer cycles, mod 2^521-1. The imports show no D module importing A code. Only runDd.py imports engine, for the optional F_A column, and the final N=30 rows were run with --noA. The agreement is on the sum U(30), not per cycle type, for the final rows. The two methods share the Burnside/cycle-type framework (U = sum F/z over partitions) and the 5-regular simple-graph definition. Those are the same mathematics, but the code on the computed path is separate. A shared conceptual bug in that framework would be caught only by the small-N and b-file agreement, which is clause 3. Some N=30 rows were ERR (memory cap) in lane files and retried. dsumcheck uses the valid row for each type, and 5604 types are present. Results/Dsum_check_d5.txt has a stale INCOMPLETE line for N=28, and the allterms check still passes for it.
- Nothing is sampled. The computation is deterministic exact integer arithmetic. The only cap is the memory/time cap on individual types, which was retried. Null model not applicable. MET, with the shared Burnside framework noted.

## Clause 3: reproduces published terms (A006821 and A165626)
- `python3 -I check/allterms.py 5 results/Dsum_check_d5.txt results data/b165626.txt data/b006821.txt half` printed:
  `all-graphs b-file b165626.txt: checked=15 MISMATCH 0`
  `connected b-file b006821.txt: checked=14 (n=1..14) MISMATCH 0`
  `beyond b-file: n=15 N=30 U_D=1690586697369281612308192667831589 C_D=1690586697346784893842479211750187`
- `python3 -I methodD/dbfcheck.py 5 30 data/b006821.txt --half results/Dsum_check_d5.txt` printed `C_D(N=30)=1690586697346784893842479211750187 bfile_checked=14 MISMATCH 0`.
- The MISMATCH lines at the end of methodA/A_terms_d5.txt are an index artifact. They read `idx=13 N=13 bfile=... ours=0`, so driver.py compared b-file index n with N, which is a misalignment. I compared the file's connected column at N=2n with the b-file for n=1..12 (the rows present up to N=24 with a b-file entry): 12 checked, 0 bad. The U column is not touched. The file's N=30 row, and the C_D values from method D, match the b-file through n=14.
- The claim says "method-D code" reproduces the terms. Verified for D through allterms and dbfcheck. Method A's connected column also matches at N=2n.

## Hidden quantifiers and stretched definitions
- The criterion says "the same code" reproduces all published terms. The N<=28 rows come from the same runDd pipeline, but they were produced in separate runs and some in an earlier "ok" mode. There is no single end-to-end run. This is a procedural point, not a value risk.
- The disconnected check: A165626 n=0..14 (15 terms) match. A005638-type "disconnected version" is satisfied by A165626 as named in data/A006821.txt.
- No part of the claim is wider than one new term (A006821(15)), plus its disconnected companion U_5(30), which is a by-product and not itself a separately listed criterion term.

confirmed_scope: A006821(15) = 1690586697346784893842479211750187 (with U_5(30) = 1690586697369281612308192667831589) is computed by two separately coded exact methods that agree on U_5(30), and method D reproduces all b-file terms of A006821 (n=1..14) and A165626 (n=0..14) through the inverse Euler transform.
context: subagent (fresh context, saw only claim/)
pass: true
