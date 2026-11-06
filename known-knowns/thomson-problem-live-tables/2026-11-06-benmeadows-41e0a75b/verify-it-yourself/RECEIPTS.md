# Receipts

Output of `sh verify-it-yourself/run_checks.sh` on 2026-11-06 (Python 3.14.7, numpy 2.5.4):

```
sha256 41e0a75b4b6d5bbb4a7c8f3d951ab712da44e958b69641eb2ac2c2da3967f979
points: 436  fewest significant digits in a coordinate: 30
E* = 90020.681268073011826514460478379715290371348019301
claimed E* = 90020.68126807301182651446  difference = 4.78379715290371348019301E-22
table minimum - E* = 0.034817546988173485539521620284709628651980699
float64 tangent gradient norm: 1.902e-12
tangent Hessian: 869 positive (need 869), 3 zero (rotations, expect 3), 0 negative; lowest ['-0.000000', '-0.000000', '0.000000', '0.511236', '2.241729', '2.241729']
PASS
```
