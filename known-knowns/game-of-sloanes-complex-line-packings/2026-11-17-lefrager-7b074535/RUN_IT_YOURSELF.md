# Run It Yourself

## 1. Verify the Submitted Packing (`< 1 second`, Python 3 standard library only)

From the root of this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

What this checks at 60-digit decimal precision (computed with `decimal.getcontext().prec = 80` guard digits, results rounded to 60 significant digits):
1. Exact token count `204 = 2 * 3 * 34` in `GameofSloanes` layout (`102` real parts vector-by-vector, then `102` imaginary parts), finite floats, and `>= 16` significant digits per coordinate (`>= 20` actual).
2. Normalizes every complex vector and computes `mu = max_{j<k} |<phi_j, phi_k>| = 0.756494798182271705164224601239675096749550724764985832115081`.
3. Compares `mu` against both the live `GameofSloanes` table record (`0.75683480`) and the recorded 60-digit value (`0.756834797253628206097823785778147954374744559786819000003660`) of upstream [`CurrentBestPackings/3x34_jrr.txt`](https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/3x34_jrr.txt) (`SHA-256: 159cb51fdd209252b1b4c2a190b8fccefed7415e5254a3226160d4218082cf1e`), confirming strict improvement `+0.0003400018...` (`>= 1e-8`) and compliance with the lower bound `0.67202151`. You may optionally pass a locally downloaded copy of `3x34_jrr.txt` as a second CLI argument to `verify-it-yourself/check_submission.py` to verify it directly from disk.
4. Verifies SHA-256 integrity of `object/3x34_new.txt`.

## 2. Rediscover and Polish From Random Seeds (`~10 seconds` on an 8-core CPU)

Requires `g++` with C++17 and OpenMP:

```sh
sh how-we-built-it/reproduce.sh
```

This compiles `fast_rrr_turbo.cpp`, `gram_alm.cpp`, and `fine_alm_ld.cpp`, runs 2,400 multi-start $O(d n^2)$ Subspace-Iteration Gram RRR + LSE trajectories (`seed_offset = 100`) to find the `0.7565178377501368` basin, and polishes it via Augmented Lagrangian $(\Phi, t)$ L-BFGS (`double` then 80-bit `long double`) to `<= 0.7564948091`.
