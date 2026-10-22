# p_c^site(Z^3) <= 0.4427: an explicit upper bound for site percolation on the cubic lattice

## What

Conditional on the released code reproducing the logged 3x3x3 certificates (outputs/chainB_log.txt links 1-3 and outputs/chainA_log.txt links 4-7), PROOF.md together with those exhaustive outward-rounded and exact-integer checks rigorously proves p_c^site(Z^3) <= 4427/10000 from Campanino-Russo's p_c^site(Z^3) <= 1/2, a bound strictly below the best published bound named in the claim's record (Campanino-Russo's non-explicit p_c < 1/2, tabulated as 0.5000).

In words: the critical probability of site percolation on the simple cubic lattice is at most 4427/10000. The best
published rigorous upper bound was Campanino and Russo's p_c < 1/2 (1985), with no explicit constant.

The proof (object/PROOF.md) tiles Z^3 by 3x3x3 blocks, follows a block growth process in the style of van den Berg
and Ermakov (1996), and reduces "each step dominates Bernoulli(q)" to 6 x 511 laws checked against all 7579
nontrivial up-sets of {0,1}^5 (Strassen's criterion) over all 2^27 block states, in outward-rounded interval
arithmetic with an exact integer comparison. A chain of seven such certificates goes from theta(0.501) > 0 (by
Campanino-Russo's p_c <= 1/2) down to p = 0.4427.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (under a second): object integrity, the exact census of block states, the chain logic and
every link's root condition in exact rationals. The full exhaustive certificate (Go >= 1.21 and Python 3 with numpy;
about 12 minutes on 6 cores, ~2 GB):

    PYTHON=python3 FULL=1 sh verify-it-yourself/run_checks.sh

Expected last line: `PASS (full: counts reproduced byte for byte, 7 of 7 links certified)`. Receipts of both:
verify-it-yourself/RECEIPTS.md. Details: RUN_IT_YOURSELF.md.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| Gomes, Pereira, Sanchis, J. Appl. Probab. (arXiv:2106.10388v2, 13 March 2026), Table 1 | non-oriented site percolation, d = 3 | 0,5000 (*), i.e. Campanino-Russo's p_c < 1/2 | https://arxiv.org/abs/2106.10388 | 2026-10-19T00:12:39Z (panel), 2026-10-18T21:31:19Z (run) |

Snapshot: the-record-we-beat/TABLE_RECORD.md. Monte Carlo puts p_c near 0.3116; that is an estimate, not a bound.

## Not claimed

- Not the value of p_c, and not a bound below 0.4427. This block and rule have a fixed point near 0.4426.
- Nothing about bond percolation (its cubic-lattice bound 0.347297, Yu and Wierman 2021, is a different model).
- Confidence intervals (Ball 2013) are not compared: they are not bounds.
- The run also certified a variant chain starting from q = 0.68, which needs only p_c^site(Z^2) <= 0.679492
  (Wierman 1995) and Z^2 inside Z^3 instead of Campanino-Russo (how-we-built-it/outputs/chainW_summary_unpanelled.txt).
  That variant was done after the panel and is not part of the panelled claim.
- No statement about higher dimensions, although bounds derived from the Z^3 value (Gomes-Pereira-Sanchis,
  Theorem 2.3) would move.

## Credits

- M. Campanino and L. Russo, An upper bound on the critical percolation probability for the three-dimensional
  cubic lattice, Ann. Probab. 13 (1985) 478-491 (the base input p_c <= 1/2).
- J. van den Berg and A. Ermakov, A new lower bound for the critical probability of site percolation on the square
  lattice, Random Structures Algorithms 8 (1996) 199-212 (the growth-process and Strassen-coupling method).
- V. Strassen, The existence of probability measures with given marginals, Ann. Math. Statist. 36 (1965) 423-439.
- P. A. Gomes, A. Pereira and R. Sanchis, Upper bounds for critical probabilities in Bernoulli percolation models,
  J. Appl. Probab. (arXiv:2106.10388) (the table compared against).
- G. R. Grimmett, The work of Lucio Russo on percolation, arXiv:1604.04849 (the record's status).
- J. C. Wierman, Substitution method critical probability bounds for the square lattice site percolation model,
  Combin. Probab. Comput. 4 (1995) 181-188 (the 2D bound used by the unpanelled variant; quoted as 0.679492 in
  N. Ball, arXiv:1312.0961).
- Found by Kaust-a-laut with Claude Code (Anthropic) running claude-opus-5-5, in the V3R1T4S kit
  (https://github.com/elder-plinius/V3R1T4S).
