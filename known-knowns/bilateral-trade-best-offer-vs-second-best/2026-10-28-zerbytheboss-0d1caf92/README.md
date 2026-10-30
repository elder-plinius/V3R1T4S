# Bilateral Trade: Best-Offer vs Second-Best Strict 3/4 Bound Refutation

## What
An explicit finite-support bilateral trade instance (|S|=4, |B|=4) with exact rational probabilities and posted price mechanism M=8 certifying max(GFT_SO, GFT_BO) / GFT_M = 19080/26767 approx 0.712818 strictly below the 3/4 bar under GFT-favourable tie-breaking with strictly unique optimal offers for all types.

## Check It Yourself
Run the standalone checker from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
SUCCESS: max(GFT_SO, GFT_BO) < (3/4) * GFT_M CONFIRMED UNDER FAVOURABLE TIES!
PASS
```

Runtime is sub-second (< 0.1s) in standard Python 3.

## Compared To
- **Status Source**: M. Babaioff, S. Dobzinski, and N. Kupfer, "The Best-of-Both-Worlds in Bilateral Trade", arXiv:2111.07790 Section 3; FOCS 2021.
- **Incumbent Record**: BDK proved a limiting ratio of $3/4$ on a $2 \times 2$ instance only under adversarial tie-breaking (under favourable ties, the ratio is 1).
- **Prior Universal Bounds**: Brustle, Cai, Wu, and Zhao (2017) proved a universal lower bound of $1/2$. Whether any instance achieves $\max(\text{SO}, \text{BO}) / \text{SB} < 3/4$ under favourable ties remained open.
- **Our Value**: Certified $\max(\text{GFT}_{SO}, \text{GFT}_{BO}) / \text{GFT}_M = \frac{19080}{26767} \approx 0.712818 < 0.750000$ strictly below the $3/4$ bar by a strict margin of $0.03718$. All optimal offers are strictly unique, so the bound holds under every tie-breaking rule.

## Not Claimed
- We do not claim that the worst-case ratio reaches the Brustle et al. lower bound of $1/2$; we claim only a certified instance strictly below $3/4$ surviving favourable ties.
- We do not claim that posted price $p = 8$ is the optimal second-best mechanism; since posted prices are BIC, IR, and BB by construction, $\text{GFT}_M \le \text{SB}$, which rigorously implies $\max(\text{SO}, \text{BO}) / \text{SB} \le \max(\text{SO}, \text{BO}) / \text{GFT}_M < 3/4$.

## Credits
- Moshe Babaioff, Shahar Dobzinski, and Noam Kupfer for the formulation of best-of-both-worlds bilateral trade and the $3/4$ benchmark (arXiv:2111.07790).
- Johannes Brustle, Yang Cai, Fan Wu, and Mingfei Zhao for the $1/2$ approximation guarantee.
- Yang Cai, Vineet Gupta, Zun Li, and Aranyak Mehta for AlphaEvolve calibration benchmarks (arXiv:2603.08679).
- V3R1T4S multi-agent discovery architecture.
