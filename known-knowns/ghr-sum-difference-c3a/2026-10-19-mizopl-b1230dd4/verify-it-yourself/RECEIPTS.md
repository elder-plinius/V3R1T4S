# Verification Receipts (`verify-it-yourself/RECEIPTS.md`)

Command executed:
```sh
sh verify-it-yourself/run_checks.sh
```

Output:
```text
== running check_c3a.py on object/ files ==
[PASS] Toy finite-depth brute-force verification (B=2, q=3, N=3): exact GHR inequalities verified.
[PASS] Kleinwaks baseline reproduction (B=17032, Q=34065, N=10000000000000): |M|=3121, |S|=18730, |D_+|=16184, n_0=14962802398, L=51500691976683641, theta_mp60 >= 1.19102809427254087548, theta_int >= 1.19102809424738956213 (published: 1.19102809)
[PASS] Primary new certificate (B=17086, q=27995, N=10000000000000): |M|=3153, |S|=18835, |D_+|=13997 (27,995/27,995 residues), n_0=17074745018, L=50031092045455301, theta_mp60 >= 1.19230254070568368329, theta_int >= 1.19230254068351294895 (8dp: 1.19230254, margin over 1.19102809 = +0.00127445 >= 1e-7)
[PASS] Secondary new certificate on Kleinwaks mask (B=17032, q=27995, N=10000000000000): |M|=3121, |S|=18730, |D_+|=13997 (27,995/27,995 residues), n_0=17075622128, L=50029864065809249, theta_mp60 >= 1.19229904840497896133, theta_int >= 1.19229904838280822699 (8dp: 1.19229904, margin over 1.19102809 = +0.00127096 >= 1e-7)
ALL CHECKS PASSED.
== negative control: a corrupted copy must FAIL ==
negative control rejected as expected (AssertionError)
ALL CHECKS PASS
```
