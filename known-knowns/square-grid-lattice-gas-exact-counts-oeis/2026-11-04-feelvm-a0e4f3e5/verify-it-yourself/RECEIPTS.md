== 1. object files present
== 2. full verification (CRT certificates, ladder evidence, growth checks)
ok: object value has 43 digits - digits=43
ok: claimed value is NOT a published term (genuinely the next index)
ok: run1: 14 distinct primes, all prime and 1 (mod 15)
ok: run1: every residue matches the claimed value
ok: run1: CRT reconstruction equals the claimed value
ok: run1: recorded modulus equals the prime product
ok: run1: CRT modulus exceeds the rigorous bound 2^15*||T||_inf^15 - modulus 2^209.5 vs bound 2^168.8
ok: run2: 14 distinct primes, all prime and 1 (mod 15)
ok: run2: every residue matches the claimed value
ok: run2: CRT reconstruction equals the claimed value
ok: run2: recorded modulus equals the prime product
ok: run2: CRT modulus exceeds the rigorous bound 2^15*||T||_inf^15 - modulus 2^208.6 vs bound 2^168.8
ok: prime sets disjoint (two-run rule)
ok: run1: ladder reproduces a(1)..a(14) (program output vs published terms)
ok: run2: ladder reproduces a(1)..a(14) (program output vs published terms)
ok: entropy per site decreases toward Lieb's constant (ln a15/225 < ln a14/196) - 0.436309 < 0.437020
ok: finite-size consistency: n^2*(ln a/n^2 - lnW) ~ 1.08 as in every published term - n^2*delta = 1.0769 (published a(14): 1.0774)
ok: digit count matches the entropy-constant estimate
PASS
== 3. corruption self-test (the checker must reject a broken object)
corrupted object -> FAIL (5 failed checks: run1: every residue matches the claimed value; run1: CRT reconstruction equals the claimed value; run2: every residue matches the claimed value; run2: CRT reconstruction equals the claimed value; finite-size consistency: n^2*(ln a/n^2 - lnW) ~ 1.08 as in every published term)
corruption correctly rejected
== 4. live OEIS cross-check (informational; skipped silently when offline)
live b-file: matches the extracted cells: True; claimed a(15) still absent: True
PASS
