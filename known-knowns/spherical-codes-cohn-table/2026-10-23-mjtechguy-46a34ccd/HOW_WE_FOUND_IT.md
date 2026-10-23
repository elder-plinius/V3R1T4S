contributor text, unverified

The (25, 651) code of package 2026-10-23-mjtechguy-23ad10a0 has maximum cosine 0.242691253763, which is already below the live (25, 650) cosine 0.242872702057. Deleting any one of its points therefore gives a 650-point code that beats the (25, 650) row.

derive_650.py tried every endpoint of the 20 largest pairs of the 651 code. Deleting row 554 (one-based; zero-based 553), one end of the single worst pair, gave the smallest maximum, 0.24269125172535584491 at 50 digits, a gain of only about 2e-9 over the 651 code.

A short active-set LP minimax polish (polish_650.py) was started from that file and stopped after about 15 minutes without one accepted step. A LogSumExp ladder (lse_650.py, L-BFGS-B at inverse temperatures 3e5 up to 3e8, a few minutes) started from the same file lowered the float64 maximum by 1.558e-4, to 0.2425354041061758. mpmath at 50 digits then reported 0.24253540410617579968405548728311276930607147141846, and the standard-library checker printed PASS.

The result has a single worst pair and about 1960 pairs within 1e-8 of it, so further polishing may lower it a little more.
