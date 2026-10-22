# Receipts (real output of sh verify-it-yourself/run_checks.sh, run from the package folder)

```
== object files already checked against SHA256SUMS by the integrity guard above
== shannon_check.py: separation property of every table and code used, exact recomputation of M, exact comparison with the live records
== claim C13 (d=522: c12'=S3c(a3,a6,b3), x34=S3c(a9,b13,c12'), x36=S3c(a7,b17,c12'), K3a(x34,x36,b17)), key new_record_best
-- 1. separation relation
  [ok]   label separation relation equals Definition 4 of the paper (22 ordered pairs)
  [ok]   separation relation is symmetric
-- 2. admissibility of every table and terminal code used: ['S2b', 'S3c'] ; ['K3a']
  [ok]   table S2b (arity 2, 17 words): Definition 6 (i) and (ii), 0 violations
  [ok]   table S3c (arity 3, 48 words): Definition 6 (i) and (ii), 0 violations
  [ok]   terminal code K3a (arity 3, 19 words): pairwise separated, 0 violations
-- 3. recompute M along the schedule
  base seven-family cardinality vector (B,N,A,D,O,H,V) in C_13^(box 6): [61516, 60502, 1014, 1014, 1014, 1014, 1014]
  [ok]   all node exponents positive
  M computed: 418 digits, degree d = 87 x 6 = 522
  [ok]   known-answer: BPZ Lean schedule (26 nodes) recomputes the Lean integer exactly (d=522, 418 digits)
-- 4. M and degree against the contributor's claim
  [ok]   recomputed M equals the contributor's M (418 digits)
  [ok]   recomputed degree d = 522 equals the contributor's degree
  the set lives in C_13^(box 522)
-- 5. bound and exact comparison with every record
  bound M^(1/d) with d=522: 6.30292681655233559742720157075414399233513701535409 (floor at 50 digits, certified by exact integer powers)
  [ok]   bound equals the contributor's 50-digit value
  record bpz_lean                           d=522   bound 6.30292672931010853494960279947052989703296258437934  margin +0.00000008724222706247759877128361409530217443097475  direct M^d_rec > M_rec^d: True
  [ok]   bound strictly greater than BPZ Lean repository CertC13.lean at aa21eeb12b75 (d=522) (exact integer test)
  [ok]   bound strictly greater than 9a.md comment, BPZ C13 = 6.302455083464 (even after rounding the displayed decimal up one unit in its last place)
  record 9a_bpz_comment                     decimal 6.302455083464  margin over the displayed decimal 0.00047173308833559742720157075414399233513701535409

RESULT C13 d=522 M_digits=418 bound=6.30292681655233559742720157075414399233513701535409 headline_margin_vs_bpz_lean=+0.00000008724222706247759877128361409530217443097475 all_records_beaten=True time=0.1s
== negative control 1: one duplicated word in a substitution table must be rejected
negative control 1 rejected as expected
== negative control 2: one input changed by 1 (a certificate, or the base vector) must change M and be rejected
negative control 2 rejected as expected
RESULT C13 d=522 M_digits=418 bound=6.30292681655233559742720157075414399233513701535409 headline_margin_vs_bpz_lean=+0.00000008724222706247759877128361409530217443097475 all_records_beaten=True time=0.1s
ALL CHECKS PASS
```
