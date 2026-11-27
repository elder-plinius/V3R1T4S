# Brun's constant under GRH: B < 2.1257395 (previous conditional record 2.1594, Dunn)

This is a **conditional** result: it assumes the Generalized Riemann Hypothesis for Dirichlet L-functions (including RH). It is not
unconditional, it is not the bank's main win, and it says nothing about whether GRH holds.
Submission id: `2026-11-24-blocksavvy-ece6008a`. Bank target: `brun-constant-unconditional-upper-bound`, partial win p1.

**Supersedes** the same contributor's submission `2026-11-24-blocksavvy-e6b84d42` (B < 2.126988, PR #1232) for the same cell. It reuses that
proof verbatim and changes one step (how-we-built-it/PROOF_DELTA.md). This is a separate, new submission; nothing in #1232 or #1231 was changed.

## What

Assuming GRH for Dirichlet L-functions, the package's proof (Dunn's Theorem 3.1 framework with the inherited e6b84d42 changes, plus the per-modulus combination of the Selberg remainder in the 22 intervals with z_i <= 20000) and its arb/exact-integer certificate give B <= 2.1257393973... < 2.1257395, strictly below Dunn's 2.1594, which is partial win p1 and not the unconditional main win, contingent on the inherited e6b84d42 base being correct.

In short: in Dunn's framework the Selberg sieve remainder is sum_{d1,d2} lambda_d1 lambda_d2 R_[d1,d2]. The e6b84d42 proof bounded it by
(sum |lambda_d|)^2 max|R_q|. Here the weight products are first combined per modulus q = [d1,d2] (the standard upper-bound-sieve form, e.g.
Tao, 254A Notes 4, eq. (28)): the factor becomes Sigma(z) = sum_q |rho_q|, about 0.645 (sum|lambda_d|)^2, used in the 22 intervals with
z_i <= 20000. Sigma is bounded with exact rational weights (rounded to multiples of 2^-40 with the rounding bounded exactly) and exact 128-bit
integer sums. Certified: B <= 2.1257393973040676877 (standalone checker, 128 and 256 bits), about 1.0e-7 below the stated 2.1257395.
Control: with the change switched off the same program gives 2.1269872000642055706, the e6b84d42 value.

## Check it yourself

From this folder (python3 >= 3.9, a C compiler with __int128 such as gcc, and pip access once to install python-flint==0.9.0 into
verify-it-yourself/.venv unless python3 already has it):

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough time: 2-3 minutes for both precisions (the V/W sieve uses up to 8 threads; pin with taskset to limit).
It recomputes V(n), M(n), W(n) with its own sieve, every one of the 9906 interval terms in arb, and for the 22 intervals marked "rho" it
computes the Selberg weights itself in ball arithmetic, certifies their rounding, sums them per modulus exactly with its own sort-based
program (verify-it-yourself/rhocount.c), checks lambda_1 = 1, sum|lambda| <= W/V and sum_q P_q = (sum L)^2, and checks the total < 2.1257395.
Optional: `python3 verify-it-yourself/tamper_tests.py` builds five corrupted certificates and requires each to FAIL.

## Compared to

| table | cell | our value | table value | source | fetched (UTC) | HTTP | sha256 of fetched page |
|---|---|---|---|---|---|---|---|
| Tao et al., optimizationproblems | constant 81a (Brun's constant), upper bound under GRH | 2.1257395 | 2.1594 (Dunn 2025) | https://teorth.github.io/optimizationproblems/constants/81a.html | 2026-11-24T08:46:42Z (pre-package re-fetch; NOVELTY 08:20:13Z; scout 07:29:34Z) | 200 | f8344f6ab5e7162878949de7b362dcbe4e5a54a48df35185e564e1901d4e0cc9 |

The unconditional row (2.288513) is not affected. Re-fetch the page immediately before submitting.

## Not claimed

- Not unconditional; not the main win.
- Not a new sieve method: the per-modulus combination is the standard upper-bound-sieve form of Selberg's sieve (Tao, 254A Notes 4,
  eq. (28); Vaughan's notes keep the signed remainder). Applied numerically to Brun's constant here for the first time as far as the panel's
  search found. Residual novelty risk: Halberstam-Richert, Opera de Cribro, Greaves, Montgomery-Vaughan not opened (paywalled).
- The result is contingent on the inherited e6b84d42 base proof (object/proof.md after the "base proof" line), which had its own three-skeptic
  panel; this panel re-checked only the new step.
- The change is used only for z_i <= 20000; five intervals sit at that cap. A larger cap gives more (not part of this submission).
- Thin margin: the certified value is about 1.0e-7 below 2.1257395 (rigorous, outward rounded).

## Credits

- **Contributor:** [BlockSavvy](https://github.com/BlockSavvy). Found with a V3R1T4S agent run, checked by a three-skeptic panel of fresh subagent contexts.
- **Lachlan Dunn**: the GRH bound 2.1594 and the framework. Bull. Aust. Math. Soc. 113 (2026) 293-303; https://arxiv.org/abs/2504.15658
- **Dominic Klyve**: PhD thesis (Dartmouth 2007), the explicit Selberg sieve and its weights (doi:10.1349/ddlp.153).
- **Atle Selberg**: the Lambda^2 sieve. **Terence Tao**: 254A Notes 4, https://terrytao.wordpress.com/2015/01/21/254a-notes-4-some-sieve-theory/
  **Robert C. Vaughan**: notes on Selberg's sieve, https://personal.science.psu.edu/rcv4/Selberg.pdf
- **Loïc Grenié and Giuseppe Molteni**: explicit Chebotarev under GRH, https://arxiv.org/abs/1709.07609
- **Dave Platt and Tim Trudgian**: B(4e18) and the unconditional record, https://arxiv.org/abs/1803.01925
- **Jonathan Bayless, Dominic Klyve and Tomás Oliveira e Silva**: pi_2(4e18), Integers 13 (2013) #A43.
- **J. Barkley Rosser and Lowell Schoenfeld**: pi(x) bounds (1962).
- **Terence Tao and contributors**: the optimizationproblems constants table. **FLINT/Arb** and python-flint.
