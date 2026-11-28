# Receipts: real output of `sh verify-it-yourself/run_checks.sh` (2026-11-27, one laptop-class core, ~15 s)

```
ok:   sha256 of object/controls/NEG_dual_a45_T95_rho66.txt.gz
ok:   sha256 of object/controls/NEG_pol_a45_T250_rho67045.pol.gz
ok:   sha256 of object/controls/NEG_pol_a45_T250_rho67045.txt.gz
ok:   sha256 of object/controls/NEG_tampered_a45_T250_rho67078.txt.gz
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part00
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part01
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part02
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part03
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part04
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part05
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part06
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part07
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part08
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part09
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part10
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part11
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part12
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part13
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part14
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part15
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part16
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part17
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part18
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part19
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part20
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part21
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part22
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part23
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part24
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part25
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part26
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part27
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part28
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part29
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part30
ok:   sha256 of object/parts/upper_a45_T2000_rho67005787.txt.gz.part31
ok:   sha256 of object/upper_a45_T250_rho67078.txt.gz
ok:   joined T=2000 certificate has sha256 1c95c8f035bc8fb8f68e5a86fb8bf9fc3db6b6eed8383881ca63db959aec2f0f
cert upper_a45_T2000_rho67005787.txt.gz alpha 9/20 rho 67005787/100000000 T 2000 scale 2^40
variant printed   pairs 32010003  max residual g = -29177/5497558138880  (~-5.307265383e-09) at (1648, 1661, 0, 'wait')  CERT_OK
variant corrected pairs 32010003  max residual g = -29177/5497558138880  (~-5.307265383e-09) at (1648, 1661, 0, 'wait')  CERT_OK
CERT_OK
ok:   headline T=2000 certificate CERT_OK, printed and corrected
cert object/upper_a45_T250_rho67078.txt.gz alpha 9/20 rho 33539/50000 T 250 scale 2^40
variant printed   pairs 501253  max residual g = -82708181/21990232555520  (~-3.761132621e-06) at (56, 27, 0, 'wait')  CERT_OK
variant corrected pairs 501253  max residual g = -82708181/21990232555520  (~-3.761132621e-06) at (56, 27, 0, 'wait')  CERT_OK
CERT_OK
ok:   T=250 certificate CERT_OK, printed and corrected
ok:   header alpha 9/20, rho 67005787/10^8, T 2000
ok:   g = -29177/5497558138880 < 0 and rho <= 0.70099 (exact)
cert object/controls/NEG_dual_a45_T95_rho66.txt.gz alpha 9/20 rho 33/50 T 95 scale 2^40
variant printed   pairs 72678  max residual g = 74968222589/5497558138880  (~1.363664025e-02) at (5, 1, 0, 'wait')  CERT_FAIL
variant corrected pairs 72678  max residual g = 74968222589/5497558138880  (~1.363664025e-02) at (5, 1, 0, 'wait')  CERT_FAIL
CERT_FAIL
ok:   negative control NEG_dual_a45_T95_rho66.txt.gz is rejected
cert object/controls/NEG_tampered_a45_T250_rho67078.txt.gz alpha 9/20 rho 33539/50000 T 250 scale 2^40
variant printed   pairs 501253  max residual g = 21392128277/21990232555520  (~9.728013664e-04) at (10, 10, 0, 'wait')  CERT_FAIL
variant corrected pairs 501253  max residual g = 21392128277/21990232555520  (~9.728013664e-04) at (10, 10, 0, 'wait')  CERT_FAIL
CERT_FAIL
ok:   negative control NEG_tampered_a45_T250_rho67078.txt.gz is rejected
policy cert object/controls/NEG_pol_a45_T250_rho67045.txt.gz variant corrected alpha 9/20 rho 13409/20000 T 250 states 189003
exact min residual g_lo = 4247038573/21990232555520 (~1.931329540e-04) at (193, 73, 'w')
POLICY_GAIN_POSITIVE
ok:   old claim point rho=0.67045, T=250: exact positive-gain policy in corrected N (no certificate possible)
PASS
```
