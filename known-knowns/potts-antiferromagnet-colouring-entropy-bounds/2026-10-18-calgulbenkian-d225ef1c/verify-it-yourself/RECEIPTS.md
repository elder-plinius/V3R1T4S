# Receipts

Output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18T19:33:50Z (UTC), Python 3.9.6 on Darwin arm64, system python3 without numpy, exit status 0.

```
== 1. reassemble the parts and check every sha256 (parts and whole file)
PASS: 6 parts reassemble to q5_cyl_14_cert.bin (5211716 bytes), sha256 d225ef1cf4f8f3c335620d5c7e37c5d96afa60cdc47b228acce51b66065a91e1
== 1b. sha256 of the other object files
PASS: 6 object files match their recorded sha256
== 2. parse the certificate, check positivity, compute the bound from the exact integer ratios
PASS: file length = 4 + 64 n (n=81433, bytes=5211716)
PASS: every v entry is positive (strictly) (min v bit length 223, max 224)
PASS: every y entry is positive 
min ratio y/v = 14693493.610319124799256859942479451395923620979315217076931537724788606943159667 (index 74525)
max ratio y/v = 14693493.610319124799256859942479451395923620979315217076931537724790250056301256 (index 80146)
relative spread (max-min)/min = 1.1182589962369838211886420686473053115816860116254255189158851317437935785240808E-67
C_hi^(1/14) = 3.2504052058785496850598045891913500783900376703054435295026057020945567302399930
C_lo^(1/14) = 3.2504052058785496850598045891913500783900376703054435295026057020945307674195439
PASS: claimed 20-decimal value agrees with the computed bound to within 1e-20 (claimed 3.25040520587854968506)
published bound 3.250407145038276 minus computed bound = 0.0000019391597263149401954108086499216099623296945564704973942979054432697600070
PASS: computed bound is below the published bound by at least 1e-9 
PASS: stated value is a rigorous upper bound: stated^14 >= C_hi, exact integers 
PASS: stated value is the upward rounding at 20 decimals: (stated - 1 ulp)^14 < C_hi 
CERT PARSE AND BOUND OK
== 3. exact check that y = (orbit-quotient matrix) v on the three small certificates (validates the file format)
orbits found: 11, file has 11
ORBIT CHECK OK: y = C v holds exactly for all 11 orbits
orbits found: 17, file has 17
ORBIT CHECK OK: y = C v holds exactly for all 17 orbits
orbits found: 62, file has 62
ORBIT CHECK OK: y = C v holds exactly for all 62 orbits
== 4. independent small-width eigenvalues (double precision) against the table
PASS q=5 cycle m=4: computed 114.167960646926, table 114.167960646926, relative diff 1.87e-15
PASS q=5 cycle m=5: computed 359.909325150343, table 359.909325150345, relative diff 4.26e-15
PASS q=5 cycle m=6: computed 1182.693461888315, table 1182.693461888315, relative diff 5.77e-16
SMALL-WIDTH CHECK OK (9 comparisons)
== 5. negative controls (each must be rejected)
negative control (corrupted y entry) rejected as expected
negative control (corrupted small certificate) rejected as expected
ALL CHECKS PASS
```

The optional full check (verify-it-yourself/full-check/) was not run by the packager; the panel's own run of it is quoted in panel/reproduce.md.
