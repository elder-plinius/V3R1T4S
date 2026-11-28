# Selfish mining (gamma = 0) at alpha = 0.45: certified upper bound on the optimal revenue, max REV < 0.67005787

## What

For SSZ's gamma = 0 model at alpha = 9/20, the rational certificate certs/upper_a45_T2000_rho67005787.txt.gz is an exactly verified average-reward dual certificate with gain -29177/5497558138880 < 0 for N_rho^T at T = 2000, rho = 67005787/10^8, both as printed (eq. (7) and the following display) and with the corrected Lemma 13 / eq. (28) compensation, which by the corrected Prop. 3 argument gives max REV < 0.67005787 <= 0.70099 within SSZ's policy class.

Plain words: an exactly checked rational certificate (about 32 million state-action inequalities, all verified in integer/Fraction arithmetic) shows that no policy in SSZ's model earns relative revenue 0.67005787 or more at alpha = 0.45, gamma = 0. The bank bar is 0.70099 and SSZ's printed Table 2 upper bound is 0.70109. Along the way the work found two errors in SSZ's proof appendix (Lemma 13 / eq. (22) and eq. (28)); both make the over-paying MDP N_rho^T as printed under-compensate, and both are derived and checked in how-we-built-it/CLAIM.md. The certificate passes for N_rho^T as printed (the literal bank wording) and for the corrected N_rho^T (the version we argue over-pays).

## Check it yourself

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS`. About 15 seconds and under 200 MB RAM on one laptop core (measured: 14.7 s, peak 172 MB for the largest child process); needs only `python3` (standard library). The checker joins the 32 parts of the 31 MB headline certificate (object/parts/), verifies its sha256, then runs the exact checker on it (printed and corrected compensation), on a T = 250 certificate, and on the negative controls. Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Sapirshtein, Sompolinsky, Zohar, arXiv:1507.06183 (PDF), Table 2 (gamma = 0, T = 95) | alpha = 0.45, upper bound | 0.70109 | https://arxiv.org/abs/1507.06183 | 2026-11-27T02:39:24Z |
| Bank bar (bank/targets.json, bitcoin-selfish-mining-revenue-bounds) | alpha = 0.45 | 0.70099 | n/a | n/a |

Snapshot details and SHA-256 digests: the-record-we-beat/README.md.

## Not claimed

- Not alpha = 0.475 (a separate, unpanelled attempt gave a T = 2000 certificate at 0.8083; not part of this package).
- Not that SSZ's Table 2 numbers or their Proposition 3 as printed for N_rho^T are wrong or right: the soundness argument relies on SSZ's Proposition 3 (parts I and II) with the corrected compensation rewards; those parts were checked by the panel, not re-proved from scratch (the panel's REPRODUCE caveat says Lemma 8 and its admissibility conditions were not re-proved).
- Not a value for the optimum: the lower side (an exact policy certificate REV > 0.67005786 at T = 1500) is recorded in how-we-built-it/LARGE_FILES.md by hash and regeneration recipe only; it is not in this package and not part of the claim.
- Not the exact-rational policy value of the bank's partial win p1.
- The T = 2000 certificate is shipped in 32 parts of at most 990000 bytes because of the 1 MB per file limit; the T = 2000 negative controls and the lower certificate are not shipped (50 MB limit), only listed by sha256 with a deterministic rebuild recipe.

## Credits

- **Ayelet Sapirshtein, Yonatan Sompolinsky, Aviv Zohar** (arXiv:1507.06183, FC 2016): the model, Tables 1-2, the over-paying MDP and Proposition 3 this work builds on and corrects.
- **Bar-Zur, Eyal and Tamar** (arXiv:2007.05614): the follow-up methods the bank entry cites.
- **numpy** (https://numpy.org/): the float solver that produced the bias vectors (the checker is standard library only).
