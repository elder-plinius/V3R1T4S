# REPRODUCE skeptic: claim p4 (bzyzz K2 sum over all zeros below 1.3e6)

context: fresh-context knowledgeWork skeptic, sandbox panel-0045-reproduce

Written 2026-11-25 07:59 UTC (date -u). I saw only the claim package (claim/) and RULES.md. The private folder, credentials and the network were not used for verification; the only download was python-flint 0.9.0 from pip into a venv in the sandbox.

## Definition checked (quoted from claim/CLAIM.md)
"rho = 1/2 + i gamma (gamma > 0), K2(v) = 2 * sum_{0<gamma<T0} exp(-k gamma^2) * Re( exp(i gamma v) / (rho zeta'(rho)) ),
k = 1.5e-10, T0 = 1.3e6, v as above", where v = 3484971332733132396.5383341489440461.

## Method (NUMERICAL: rigorous ball arithmetic, assuming FLINT/Arb is correct)
- I wrote my own checker (mine/k2mine.py, mine/aggregate_mine.py) from the definition above **before** I read the author's code.
- Zeros: `acb.zeta_zeros(n, cnt)` (FLINT/Arb, certified isolation by index) for every n = 1 .. 2,325,573, in 4,652 chunks of 500 zeros (the last chunk has 73).
  zeta'(rho) comes from a certified order-1 series expansion (`acb_series([rho,1]).zeta()`).
- k and v are exact rationals (fmpq: 15/10^11 and 34849713327331323965383341489440461/10^16), so v carries no representation error.
- Working precision: 160 bits for n <= 600,000, 128 bits for 600,000 < n <= 1,200,000, and 96 bits above that. Chunk sums were added at 256 bits.
- A term is included only if its certified gamma ball is strictly below T0. The code stops with an error if a ball straddles T0.
- Run: nice 10, 6 workers, nohup, resumable atomic chunk files. The host rebooted partway through (about 23:52 CST). The run resumed with the same command and recomputed every chunk file that was missing.
  A duplicate run (started by mistake) lived about 9 s around 00:19 CST. I recomputed all 35 chunk files written from 00:17:30 to 00:20:00 CST, including m_00875001_0500.json. All 35 matched the saved files exactly.
- No chunk was sampled or skipped: all 2,325,573 zeros and all 2,325,572 terms were computed by my code.

## Zero count and boundary zeros
- Terms summed: 2,325,572. The only computed zero at or above T0 is n = 2,325,573, and it is excluded.
- Independent count: `arb(1300000).zeta_nzeros()` = 2325572.0000000000000 (exact).
- gamma_2,325,572 = [1299999.53632749461783640283430 +/- 2.78e-25] < 1.3e6
- gamma_2,325,573 = [1300000.18286524889819717690167 +/- 2.12e-24] > 1.3e6. Its excluded half-term is [3.336e-118 +/- 6.3e-139].

## My K2 ball (mine/final_aggregate.json)
- K2_head (n <= 600,000) = [1.00030525038649901205876 +/- 3.60e-24]
- K2_tail (600,000 < n <= 2,325,572) = [1.2853109500e-14 +/- 4.34e-25]
- **K2 = [1.00030525038651186516826 +/- 3.73e-24]**
- K2_lower - 1 - E (E = 2.391e-11) = 3.052503626e-4 > 0

## Comparisons
| reference | value | my ball overlaps | my ball contained |
|---|---|---|---|
| author K2 (result/aggregate_claim.json) | [1.00030525038651 +/- 5.07e-15] | yes | yes |
| author K2_head (128-bit) | [1.00030525038650 +/- 4.03e-15] | yes | yes |
| author K2_tail | [1.3e-14 +/- 9.56e-16] | yes | yes |
| certificate K2 (inputs/bzyzz_k2_certificate.json) | [1.0003052504 +/- 2.30e-11] | yes | yes |
| certificate K2_main_(n<=600000) | [1.000305250386499012059 +/- 3.21e-22] | yes (my head) | yes |
| certificate K2_tail_ball | [+/- 9.43e-12] | yes (my tail) | yes |

- Per-block comparison: I summed my chunks and the author's saved chunks (chunks_head128 + chunks_tail) over the same 1,163 blocks of 2,000 zeros. In the last block I removed the author's n = 2,325,573 term. **0 of the 1,163 blocks fail to overlap** (mine/final_checks.json).
- Author's checker: `python code/aggregate_claim.py` was run 3 times, and every run matched result/aggregate_claim.json exactly. The run on `chunks_head` matched result/aggregate_claim_head96.json exactly.
  Both report complete = true and boundary_ok = true. The author's checker subtracts the n = 2,325,573 term explicitly, so that zero is excluded from the claimed sum.
- SHA256SUMS.txt: every file verifies, and no file is unlisted.
- Determinism:
  - Chunks n0 = 1, 600001, 1200001 and 2325501 were each recomputed twice, and both runs matched the saved file exactly.
  - The 35 chunks written around the duplicate run were all identical on recompute.
  - My aggregate gave identical output on rerun.

## Discrepancies and notes (none affect the claim)
- The author's code builds v as arb(v) at the working precision (96 or 128 bits). The radius of v (about 2^(62-prec)) times gamma therefore dominates the phase error.
  This explains their loose ball (+/- 5e-15 at 128 bits, +/- 1.7e-5 at 96 bits). The balls are still rigorous, and my exact-rational v gives a radius 1e9 times smaller.
- The author's aggregator computes the excluded n = 2,325,573 term with v at the default 53-bit precision. That is harmless, because the term is about 1e-118 and the ball stays rigorous.
- I found no gap, no overlapping or duplicate chunk, no non-overlapping ball and no non-determinism.

Hashes: mine/k2mine.py 5372d40b...e651; mine/final_aggregate.json 43a13b7a...670f; all my chunk files concatenated ca43cc11...96b2.

Scope confirmed (one sentence): the K2 sum of the bzyzz certificate at the stated v and k, over all 2,325,572 zeros with 0 < gamma < 1.3e6, lies in [1.00030525038651186516826 +/- 3.73e-24]. That ball sits inside both the author's ball and the certificate's, so K2 > 1 + E. Nothing beyond the K2 sum is checked here (not J1..J6, not the 1/zeta bound, and the bound itself has not been reviewed).

pass: true
