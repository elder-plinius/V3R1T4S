The shipped object is object/650.txt. The checker does not need a rebuild. Python 3 with numpy, scipy and mpmath; set OMP_NUM_THREADS to a small number.

1. Start from object/651.txt of package 2026-10-23-mjtechguy-23ad10a0 (sha256 23ad10a0d1210f45733dcd33ef9b2c85455ed24dbbb9f11325d8d58f3fedee84).
2. python3 derive_650.py 651.txt 650_deleted.txt
   Deletes the best single point among the endpoints of the 20 largest pairs. Result: zero-based row 553 removed, mpmath maximum 0.24269125172535584491267820485902099189671082015171. The kept lines are byte-for-byte copies.
3. python3 polish_650.py 650_deleted.txt out 1500 (tried; stopped after about 15 minutes with no accepted LP step; no file written).
4. python3 lse_650.py 650_deleted.txt out 1200
   Uses kernel.py. Betas 3e5, 1e6, 3e6, 1e7, 3e7, 1e8, 3e8. Float64 maxima per step: 0.24258984756665181, 0.24255340102389419, 0.24253934342551869, 0.24253642485666338, 0.24253562175328458, 0.24253544968409857, 0.24253540410617583. The best is written as out/lse_650.txt at 20 digits in scientific notation; that file is object/650.txt.
5. python3 score.py object/650.txt
   mpmath 50 digits over every pair: c* = 0.24253540410617579968405548728311276930607147141846, worst pair zero-based (623, 633).
6. The accept rule was frozen in PREREG.md, and the object rule was replaced by PREREG.v2.md before the LogSumExp file was scored.
