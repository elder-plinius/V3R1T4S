# Run It Yourself

Exact commands from this package folder in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Calibration 1 (BDK 2x2): Favourable ratio = 1, Adversarial ratio = 3/4 -> PASS
Calibration 2 (AlphaEvolve H=20000): FB=1.2322 (target ~1.2322), SO=0.3312 (target ~0.3312), BO=0.8565 (target ~0.8565) -> PASS
  Seller s= 1: optimal offer(s)=[Fraction(14, 1)], profit=7.2800, unique=True
  Seller s= 2: optimal offer(s)=[Fraction(14, 1)], profit=6.7200, unique=True
  Seller s= 7: optimal offer(s)=[Fraction(14, 1)], profit=3.9200, unique=True
  Seller s=14: optimal offer(s)=[Fraction(14, 1)], profit=0.0000, unique=True
  Buyer  b= 4: optimal offer(s)=[Fraction(1, 1)], profit=1.5900, unique=True
  Buyer  b= 8: optimal offer(s)=[Fraction(1, 1)], profit=3.7100, unique=True
  Buyer  b=10: optimal offer(s)=[Fraction(1, 1)], profit=4.7700, unique=True
  Buyer  b=14: optimal offer(s)=[Fraction(1, 1)], profit=6.8900, unique=True

=== EXACT RATIONAL VERIFICATION SUMMARY ===
Seller distribution: S = [Fraction(1, 1), Fraction(2, 1), Fraction(7, 1), Fraction(14, 1)], p_S = [Fraction(53, 100), Fraction(3, 100), Fraction(21, 50), Fraction(1, 50)]
Buyer distribution:  B = [Fraction(4, 1), Fraction(8, 1), Fraction(10, 1), Fraction(14, 1)], p_B = [Fraction(1, 100), Fraction(19, 100), Fraction(6, 25), Fraction(14, 25)]
Mechanism M: Posted Price p = 8
GFT_SO (exact): 7133/1250 = 5.70640000
GFT_BO (exact): 1431/250 = 5.72400000
max(GFT_SO, GFT_BO): 1431/250 = 5.72400000
GFT_M (exact):  80301/10000 = 8.03010000
Certified Ratio max(SO, BO) / GFT_M: 19080/26767 = 0.71281802
Target Bar: 3/4 = 3/4 = 0.75000000
Strict Margin below 3/4: 3981/107068 = 0.03718198

SUCCESS: max(GFT_SO, GFT_BO) < (3/4) * GFT_M CONFIRMED UNDER FAVOURABLE TIES!
PASS
```

To re-run the discovery scripts from `how-we-built-it/`:
```sh
python3 how-we-built-it/calibrate.py
python3 how-we-built-it/solve_alphaevolve_sb.py
python3 how-we-built-it/solve_bdk_sb.py
python3 how-we-built-it/verify_solution.py
```
