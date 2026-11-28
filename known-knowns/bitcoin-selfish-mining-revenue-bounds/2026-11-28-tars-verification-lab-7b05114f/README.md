# max REV < 169/250 at alpha = 9/20, gamma = 0 (SSZ model)

## What

In the SSZ model of arXiv:1507.06183 at alpha = 9/20 and gamma = 0, an exact-rational average-reward dual with g = -51696398727/351843720888320 < 0 holds for every state and every allowed action of the over-paying MDP N_{169/250}^{95} (Table 1 transitions, adopt-only at max(a,h) = 95, eq. (7) read as (1-rho)*E[last(a,h)] per eqs. (26)-(27)), so by SSZ Proposition 3 the maximum relative revenue over SSZ's admissible policies is below 169/250 = 0.676 <= 0.70099, which meets the full alpha = 0.45 success criterion.

## Check it yourself

Python 3 (standard library only; no third-party packages):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. The exact dual over 72678 inequalities takes about one second. Receipts are in verify-it-yourself/RECEIPTS.md. RUN_IT_YOURSELF.md also describes the optional Table 2 calibration (needs numpy, several minutes) and the supplementary h=T recertification.

## Compared to

The published SSZ Table 2 upper bound at alpha = 0.45 is 0.70109 (arXiv:1507.06183, PDF page 13, T=95, eps=1e-5). The bank bar is 0.70099, set 1e-4 below that published value; they are not the same number. The honesty-gate refetch of the status page https://arxiv.org/abs/1507.06183 at 2026-11-28T10:34:04Z returned HTTP 200 and sha256 17034454c06d20f055d997a07fbfc9beed99e36376db3c3425e0f1cf51d99d99, identical to the 2026-11-26T19:39:44Z fetch; the paper is v2, 23 Jul 2015, not withdrawn. The object U = 169/250 = 0.676 is strictly below both 0.70109 and 0.70099. The novelty review (2026-11-26) also compared PTO 2020 lower digits 0.66894 and open PR 814's claimed 0.70099; this object is a strict improvement, not a tie, and does not close the interval down to the published lower bound. Snapshot metadata is in the-record-we-beat/.

## Not claimed

No bound at alpha = 0.475. No claim that the literal typesetting of equation (7) (where (1-rho) multiplies only the first term) is a valid certificate; that reading yields a positive dual residual and is not used. No claim that the interval is closed, that Proposition 3's printed h=T display is gap-free without the supplementary conservative recertification, or that selfish mining is unprofitable at this alpha (the bound is still above the fair share 0.45). No Ethereum / p3 result. Maintainer listing in TROPHY_CASE.md remains separate.

## Credits

The model, Table 1, equation (7), Proposition 3, Algorithm 1 and Table 2 are due to Ayelet Sapirshtein, Yonatan Sompolinsky and Aviv Zohar, "Optimal Selfish Mining Strategies in Bitcoin", Financial Cryptography 2016, arXiv:1507.06183. Lower-bound digits compared at this cell include Bar-Zur, Eyal and Tamar, "Efficient MDP Analysis for Selfish-Mining in Blockchains", AFT 2020, arXiv:2007.05614. Submission credit: Tars-verification-lab. Independent review and packaging used the V3R1T4S protocol at https://github.com/elder-plinius/V3R1T4S, pinned to commit 738e7124ee00b996b511ec42ed1e81ad3c8c58b8.
