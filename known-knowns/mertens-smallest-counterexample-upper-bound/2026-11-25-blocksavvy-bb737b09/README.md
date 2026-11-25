# Mertens conjecture: independent K_2 check of the bzyzz exp(3.485e18) certificate (partial win p4)

## What

With separately written python-flint/Arb ball-arithmetic code, the K_2 sum of the bzyzz/mertens_bound certificate at v = 3484971332733132396.5383341489440461, k = 1.5e-10, over all 2,325,572 zeta zeros with 0 < gamma < 1.3e6 (zeros from Arb's acb_dirichlet_zeta_zeros, which the certificate also uses) is enclosed in [1.00030525038651 +- 5.07e-15]; this ball lies inside the certificate's K2 ball [1.0003052504 +- 2.30e-11] and exceeds 1 + E by 3.0525e-4 at the certificate's own, here unchecked, E = 2.391e-11, which confirms the certificate's K_2 inequality and finds no error in it, while Pintz Theorem A/Corollary A as used, Pintz Lemmas 4-5, J1..J6 (hence E) and the 1/zeta constant M remain unchecked.

Note: the sentence above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`). Status label: NUMERICAL.
Here K2(v) = 2 * sum over 0 < gamma < T0 of exp(-k gamma^2) Re(e^{i gamma v} / (rho zeta'(rho))), rho = 1/2 + i gamma, T0 = 1.3e6.
The REPRODUCE skeptic recomputed every zero and term itself and got [1.00030525038651186516826 +- 3.73e-24], inside our ball, with
its own count arb(1300000).zeta_nzeros() = 2325572 (`panel/reproduce.md`). Caveat: the zeros come from the same Arb routine the
certificate uses, so this is a separately written computation, not an independent source of zeros.
Object: `object/k2_result.json` (sha256 `bb737b0962247c8e68f7a128f8e3bfe55ffcde781e4fdcd3383e86d966675a51`), with the per-chunk ball sums in `object/chunks_*.jsonl`.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only). Optional: `pip install python-flint==0.9.0` and `FLINT=1` to also recompute four chunks from the zeros.
- **Rough laptop time:** a few seconds; about 30 s with `FLINT=1` (`verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It checks the hashes of the chunk files, that the 5,814 chunks cover n = 1..2,325,573 with no gap and increasing gamma, the
boundary gamma_2325572 < 1.3e6 < gamma_2325573, and re-sums every chunk ball exactly in Decimal (minus the excluded n = 2,325,573
term). The result must equal the stored ball digit for digit, lie inside the certificate's K2 ball and exceed 1 + E. The full
recomputation of all 2,325,572 terms (about 4-6 CPU-hours) is step 2 of `RUN_IT_YOURSELF.md`.

## Compared to

| source | cell | listed value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Wikipedia, Mertens conjecture (status source) | smallest counterexample upper bound | exp(1.96e19) (Kim-Nguyen); no independent check of the 3.485e18 claims | K_2 inequality of the bzyzz exp(3.485e18) certificate confirmed at its stated E | https://en.wikipedia.org/wiki/Mertens_conjecture | 2026-11-25T00:47:07Z (panel: 04:39:06Z) |
| bzyzz/mertens_bound certificate | K2 | [1.0003052504 +/- 2.30e-11] (tail only bounded) | [1.00030525038651 +/- 5.07e-15] (all zeros summed) | https://github.com/bzyzz/mertens_bound/blob/a0b267c2c7ff32a917732cf16ee860d705ca4a08/certification/k2_certificate.json | 2026-11-25T00:47Z |

Details in `the-record-we-beat/README.md`.

## Not claimed

- No new or smaller bound. Not a check of the rest of the bzyzz proof: Pintz Theorem A / Corollary A as used, Lemmas 4-5, J1..J6
  (hence E) and the 1/zeta constant M are unchecked.
- Not an independent source of zeros (same Arb routine as the certificate).
- Nothing about Gallego's bound (also about exp(3.485e18), at different k, y and T0; his exponent is 36,813.58 lower) or about Kim-Nguyen's tables (that is PR #1234, p1).
- Not peer reviewed; the panel reports are in `panel/`.

## Credits

- **Bi and Hou**, the certificate https://github.com/bzyzz/mertens_bound (commit a0b267c2) and preprint https://hal.science/hal-05838582.
- **Seungki Kim and Phong Q. Nguyen**, https://arxiv.org/abs/2502.21021 (Mertens counterexample bound exp(1.96e19), lattice method).
- **J. Pintz**, "An effective disproof of the Mertens conjecture", Asterisque 147-148 (1987) 325-333, https://www.numdam.org/item/AST_1987__147-148__325_0/.
- **Y. Saouter and H. te Riele**, Math. Comp. 83 (2014) 421-433, https://doi.org/10.1090/S0025-5718-2013-02716-0.
- **Gallego**, https://doi.org/10.5281/zenodo.23700211.
- FLINT/Arb (https://flintlib.org) and python-flint (https://github.com/flintlib/python-flint).
- Contributor credit: BlockSavvy, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
