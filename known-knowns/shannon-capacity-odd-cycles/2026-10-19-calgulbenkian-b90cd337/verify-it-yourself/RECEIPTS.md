# Receipts (real output of sh verify-it-yourself/run_checks.sh, run from the package folder)

```
== object files already checked against SHA256SUMS by the integrity guard above
== shannon_check.py: separation property of every table and code used, exact recomputation of M, exact comparison with the live records
== claim C15 (d=3792: tail exponents (255,219,219,255); K4b applied to (end of 14-step S3f tail on v9, v13, v13, end of 14-step tail on v19)), key new_record_best
-- 1. separation relation
  [ok]   label separation relation equals Definition 4 of the paper (22 ordered pairs)
  [ok]   separation relation is symmetric
-- 2. admissibility of every table and terminal code used: ['S3e', 'S3f', 'S3g'] ; ['K4b']
  [ok]   table S3e (arity 3, 53 words): Definition 6 (i) and (ii), 0 violations
  [ok]   table S3f (arity 3, 47 words): Definition 6 (i) and (ii), 0 violations
  [ok]   table S3g (arity 3, 47 words): Definition 6 (i) and (ii), 0 violations
  [ok]   terminal code K4b (arity 4, 57 words): pairwise separated, 0 violations
-- 3. recompute M along the schedule
  base seven-family cardinality vector (B,N,A,D,O,H,V) in C_15^(box 4): [2839, 2833, 6, 3, 3, 3, 3]
  [ok]   all node exponents positive
  M computed: 3275 digits, degree d = 948 x 4 = 3792
  [ok]   known-answer: BPZ Lean schedule (23 nodes) recomputes the Lean integer exactly (d=3664, 3164 digits)
-- 4. M and degree against the contributor's claim
  [ok]   recomputed M equals the contributor's M (3275 digits)
  [ok]   recomputed degree d = 3792 equals the contributor's degree
  the set lives in C_15^(box 3792)
-- 5. bound and exact comparison with every record
  bound M^(1/d) with d=3792: 7.30162938512617882481015737977863418478091882027714 (floor at 50 digits, certified by exact integer powers)
  [ok]   bound equals the contributor's 50-digit value
  record bpz_lean                           d=3664  bound 7.30162869593010394346043700214115255027612333587610  margin +0.00000068919607488134972037763748163450479548440104  direct M^d_rec > M_rec^d: True
  [ok]   bound strictly greater than BPZ Lean repository CertC15.lean at aa21eeb12b75 (d=3664) (exact integer test)
  [ok]   bound strictly greater than 9a.md comment, BPZ C15 = 7.301600534487 (even after rounding the displayed decimal up one unit in its last place)
  record 9a_bpz_comment                     decimal 7.301600534487  margin over the displayed decimal 0.00002885063917882481015737977863418478091882027714

RESULT C15 d=3792 M_digits=3275 bound=7.30162938512617882481015737977863418478091882027714 headline_margin_vs_bpz_lean=+0.00000068919607488134972037763748163450479548440104 all_records_beaten=True time=24.1s
== negative control 1: one duplicated word in a substitution table must be rejected
negative control 1 rejected as expected
== negative control 2: one input changed by 1 (a certificate, or the base vector) must change M and be rejected
negative control 2 rejected as expected
RESULT C15 d=3792 M_digits=3275 bound=7.30162938512617882481015737977863418478091882027714 headline_margin_vs_bpz_lean=+0.00000068919607488134972037763748163450479548440104 all_records_beaten=True time=24.1s
ALL CHECKS PASS
```
