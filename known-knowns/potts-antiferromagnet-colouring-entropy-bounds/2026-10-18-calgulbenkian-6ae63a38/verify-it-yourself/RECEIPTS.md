# Receipts

Output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18T19:33:38Z (UTC), Python 3.9.6 on Darwin arm64, system python3 without numpy, exit status 0.

```
== 1. reassemble the parts and check every sha256 (parts and whole file)
PASS: 33 parts reassemble to q4_cyl_18_cert.bin (28923460 bytes), sha256 6ae63a3870e719d855663cc81e6517880c282a8bcb773dc2f26a7d32cd8bdf01
== 1b. sha256 of the other object files
PASS: 6 object files match their recorded sha256
== 2. parse the certificate, check positivity, compute the bound from the exact integer ratios
PASS: file length = 4 + 64 n (n=451929, bytes=28923460)
PASS: every v entry is positive (strictly) (min v bit length 221, max 224)
PASS: every y entry is positive 
min ratio y/v = 4292523.0342056223587157719556590059728848958444345531926449169512095534786966407 (index 0)
max ratio y/v = 4292523.0342056223587157719556590059728848958444345557997455299301653250815235065 (index 330432)
relative spread (max-min)/min = 6.0735856096842770528748239502531407751105228218533365204714591835573933045290893E-52
C_hi^(1/18) = 2.3360602265554583581403491124455588569045969966701811662234277002027667886952281
C_lo^(1/18) = 2.3360602265554583581403491124455588569045969966701810873997511704081893911093672
PASS: claimed 20-decimal value agrees with the computed bound to within 1e-20 (claimed 2.33606022655545835815)
published bound 2.33606820555777 minus computed bound = 0.0000079790023116418596508875544411430954030033298188337765722997972332113047719
PASS: computed bound is below the published bound by at least 1e-9 
PASS: stated value is a rigorous upper bound: stated^18 >= C_hi, exact integers 
PASS: stated value is the upward rounding at 20 decimals: (stated - 1 ulp)^18 < C_hi 
CERT PARSE AND BOUND OK
== 3. exact check that y = (orbit-quotient matrix) v on the three small certificates (validates the file format)
orbits found: 9, file has 9
ORBIT CHECK OK: y = C v holds exactly for all 9 orbits
orbits found: 34, file has 34
ORBIT CHECK OK: y = C v holds exactly for all 34 orbits
orbits found: 57, file has 57
ORBIT CHECK OK: y = C v holds exactly for all 57 orbits
== 4. independent small-width eigenvalues (double precision) against the table
PASS q=4 cycle m=5: computed 67.015148038438, table 67.015148038438, relative diff 3.39e-15
PASS q=4 cycle m=6: computed 165.600822094454, table 165.600822094456, relative diff 7.55e-15
PASS q=4 cycle m=7: computed 375.480400415275, table 375.480400415289, relative diff 3.71e-14
SMALL-WIDTH CHECK OK (9 comparisons)
== 5. negative controls (each must be rejected)
negative control (corrupted y entry) rejected as expected
negative control (corrupted small certificate) rejected as expected
ALL CHECKS PASS
```

The optional full check (verify-it-yourself/full-check/) was not run by the packager; the panel's own run of it is quoted in panel/reproduce.md.
