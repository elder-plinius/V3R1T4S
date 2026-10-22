# Receipts (real output of sh verify-it-yourself/run_checks.sh, run from the package folder)

```
== object files already checked against SHA256SUMS by the integrity guard above
== shannon_check.py: separation property of every table and code used, exact recomputation of M, exact comparison with the live records
== claim C19 (d=12112: u_{k+1}=S3f(u_k,w,w) extended from u15 to u23; K4b on four copies of u23), key new_record_best
-- 1. separation relation
  [ok]   label separation relation equals Definition 4 of the paper (22 ordered pairs)
  [ok]   separation relation is symmetric
-- 2. admissibility of every table and terminal code used: ['S3d', 'S3f', 'S3g'] ; ['K4b']
  [ok]   table S3d (arity 3, 46 words): Definition 6 (i) and (ii), 0 violations
  [ok]   table S3f (arity 3, 47 words): Definition 6 (i) and (ii), 0 violations
  [ok]   table S3g (arity 3, 47 words): Definition 6 (i) and (ii), 0 violations
  [ok]   terminal code K4b (arity 4, 57 words): pairwise separated, 0 violations
-- 3. recompute M along the schedule
  base seven-family cardinality vector (B,N,A,D,O,H,V) in C_19^(box 4): [7664, 7661, 3, 2, 2, 2, 2]
  [ok]   all node exponents positive
  M computed: 11763 digits, degree d = 3028 x 4 = 12112
  [ok]   known-answer: BPZ Lean schedule (16 nodes) recomputes the Lean integer exactly (d=11856, 11514 digits)
-- 4. M and degree against the contributor's claim
  [ok]   recomputed M equals the contributor's M (11763 digits)
  [ok]   recomputed degree d = 12112 equals the contributor's degree
  the set lives in C_19^(box 12112)
-- 5. bound and exact comparison with every record
  bound M^(1/d) with d=12112: 9.35720032041060779697123677074196799338966554384597 (floor at 50 digits, certified by exact integer powers)
  [ok]   bound equals the contributor's 50-digit value
  record bpz_lean                           d=11856 bound 9.35720003000079613738523309560909791509163729383504  margin +0.00000029040981165958600367513287007829802825001093
  [ok]   bound strictly greater than BPZ Lean repository CertC19.lean at aa21eeb12b75 (d=11856) (exact integer test)
  [ok]   bound strictly greater than 9a.md comment, BPZ C19 = 9.357192705918 (even after rounding the displayed decimal up one unit in its last place)
  record 9a_bpz_comment                     decimal 9.357192705918  margin over the displayed decimal 0.00000761449260779697123677074196799338966554384597

RESULT C19 d=12112 M_digits=11763 bound=9.35720032041060779697123677074196799338966554384597 headline_margin_vs_bpz_lean=+0.00000029040981165958600367513287007829802825001093 all_records_beaten=True time=1.3s
== negative control 1: one duplicated word in a substitution table must be rejected
negative control 1 rejected as expected
== negative control 2: one input changed by 1 (a certificate, or the base vector) must change M and be rejected
negative control 2 rejected as expected
RESULT C19 d=12112 M_digits=11763 bound=9.35720032041060779697123677074196799338966554384597 headline_margin_vs_bpz_lean=+0.00000029040981165958600367513287007829802825001093 all_records_beaten=True time=1.3s
ALL CHECKS PASS
```
