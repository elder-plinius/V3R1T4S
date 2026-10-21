# Receipts (real output of sh verify-it-yourself/run_checks.sh, run from the package folder)

```
== object files already checked against SHA256SUMS by the integrity guard above
== shannon_check.py: separation property of every table and code used, exact recomputation of M, exact comparison with the live records
== claim C11 (d=210: p10=S3c(g3,h5,b2), x27=S3c(h7,p10,h10), x29=S3c(h6,b13,p10), K3a(x27,x29,b14)), key new_record_best
-- 1. separation relation
  [ok]   label separation relation equals Definition 4 of the paper (22 ordered pairs)
  [ok]   separation relation is symmetric
-- 2. admissibility of every table and terminal code used: ['S2b', 'S3c'] ; ['K3a']
  [ok]   table S2b (arity 2, 17 words): Definition 6 (i) and (ii), 0 violations
  [ok]   table S3c (arity 3, 48 words): Definition 6 (i) and (ii), 0 violations
  [ok]   terminal code K3a (arity 3, 19 words): pairwise separated, 0 violations
-- 3. recompute M along the schedule
  base seven-family cardinality vector (B,N,A,D,O,H,V) in C_11^(box 3): [145, 142, 3, 3, 3, 3, 3]
  [ok]   all node exponents positive
  M computed: 153 digits, degree d = 70 x 3 = 210
  [ok]   known-answer: BPZ Lean schedule (22 nodes) recomputes the Lean integer exactly (d=207, 150 digits)
-- 4. M and degree against the contributor's claim
  [ok]   recomputed M equals the contributor's M (153 digits)
  [ok]   recomputed degree d = 210 equals the contributor's degree
  the set lives in C_11^(box 210)
-- 5. bound and exact comparison with every record
  bound M^(1/d) with d=210: 5.29549275705422970542530964715933628230581897086303 (floor at 50 digits, certified by exact integer powers)
  [ok]   bound equals the contributor's 50-digit value
  record bpz_lean                           d=207   bound 5.29549231578462014255077898586171222761333914484062  margin +0.00000044126960956287453066129762405469247982602241  direct M^d_rec > M_rec^d: True
  [ok]   bound strictly greater than BPZ Lean repository CertC11.lean at aa21eeb12b75 (d=207) (exact integer test)
  [ok]   bound strictly greater than 9a.md comment, BPZ C11 = 5.294502522149 (even after rounding the displayed decimal up one unit in its last place)
  record 9a_bpz_comment                     decimal 5.294502522149  margin over the displayed decimal 0.00099023490522970542530964715933628230581897086303

RESULT C11 d=210 M_digits=153 bound=5.29549275705422970542530964715933628230581897086303 headline_margin_vs_bpz_lean=+0.00000044126960956287453066129762405469247982602241 all_records_beaten=True time=0.0s
== negative control 1: one duplicated word in a substitution table must be rejected
negative control 1 rejected as expected
== negative control 2: one input changed by 1 (a certificate, or the base vector) must change M and be rejected
negative control 2 rejected as expected
RESULT C11 d=210 M_digits=153 bound=5.29549275705422970542530964715933628230581897086303 headline_margin_vs_bpz_lean=+0.00000044126960956287453066129762405469247982602241 all_records_beaten=True time=0.0s
ALL CHECKS PASS
```
