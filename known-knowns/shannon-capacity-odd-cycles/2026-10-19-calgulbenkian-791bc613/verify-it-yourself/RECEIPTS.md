# Receipts (real output of sh verify-it-yourself/run_checks.sh, run from the package folder)

```
== object files already checked against SHA256SUMS by the integrity guard above
== shannon_check.py: separation property of every table and code used, exact recomputation of M, exact comparison with the live records
== claim C23 (d=2928: n183=S3h(S3a(n27,n9,n9), n81, S3a(n27,n3,n27)); K4a on four copies), key new_record_best
-- 1. separation relation
  [ok]   label separation relation equals Definition 4 of the paper (22 ordered pairs)
  [ok]   separation relation is symmetric
-- 2. admissibility of every table and terminal code used: ['S2a', 'S3a', 'S3h'] ; ['K4a']
  [ok]   table S2a (arity 2, 20 words): Definition 6 (i) and (ii), 0 violations
  [ok]   table S3a (arity 3, 58 words): Definition 6 (i) and (ii), 0 violations
  [ok]   table S3h (arity 3, 45 words): Definition 6 (i) and (ii), 0 violations
  [ok]   terminal code K4a (arity 4, 49 words): pairwise separated, 0 violations
-- 3. recompute M along the schedule
  base seven-family cardinality vector (B,N,A,D,O,H,V) in C_23^(box 4): [16451, 16279, 76, 146, 50, 50, 50]
  [ok]   all node exponents positive
  M computed: 3088 digits, degree d = 732 x 4 = 2928
  [ok]   known-answer: BPZ Lean schedule (7 nodes) recomputes the Lean integer exactly (d=3040, 3206 digits)
-- 4. M and degree against the contributor's claim
  [ok]   recomputed M equals the contributor's M (3088 digits)
  [ok]   recomputed degree d = 2928 equals the contributor's degree
  the set lives in C_23^(box 2928)
-- 5. bound and exact comparison with every record
  bound M^(1/d) with d=2928: 11.33455800536622830135329115399285797338312702840016 (floor at 50 digits, certified by exact integer powers)
  [ok]   bound equals the contributor's 50-digit value
  record bpz_lean                           d=3040  bound 11.33455792275451814963309014607990805631803694025507  margin +0.00000008261171015172020100791294991706509008814509  direct M^d_rec > M_rec^d: True
  [ok]   bound strictly greater than BPZ Lean repository CertC23.lean at aa21eeb12b75 (d=3040) (exact integer test)
  [ok]   bound strictly greater than 9a.md comment, BPZ C23 = 11.328224257774 (even after rounding the displayed decimal up one unit in its last place)
  record 9a_bpz_comment                     decimal 11.328224257774  margin over the displayed decimal 0.00633374759222830135329115399285797338312702840016

RESULT C23 d=2928 M_digits=3088 bound=11.33455800536622830135329115399285797338312702840016 headline_margin_vs_bpz_lean=+0.00000008261171015172020100791294991706509008814509 all_records_beaten=True time=18.6s
== negative control 1: one duplicated word in a substitution table must be rejected
negative control 1 rejected as expected
== negative control 2: one input changed by 1 (a certificate, or the base vector) must change M and be rejected
negative control 2 rejected as expected
RESULT C23 d=2928 M_digits=3088 bound=11.33455800536622830135329115399285797338312702840016 headline_margin_vs_bpz_lean=+0.00000008261171015172020100791294991706509008814509 all_records_beaten=True time=18.6s
ALL CHECKS PASS
```
