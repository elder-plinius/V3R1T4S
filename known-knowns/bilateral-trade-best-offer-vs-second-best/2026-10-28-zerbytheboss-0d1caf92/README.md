# Bilateral Trade: Best-Offer vs Second-Best Instance at 19080/26767 (Worst Case in [1/2, 19080/26767])

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
- **Status Source**: Moshe Babaioff, Shahar Dobzinski, and Ron Kupfer, "A Note on the Gains from Trade of the Random-Offerer Mechanism", arXiv:2111.07790 [cs.GT] (2021), Section 3.
- **Incumbent Record**: BDK proved a limiting ratio of $3/4$ on a $2 \times 2$ instance only under adversarial tie-breaking (under favourable ties, the ratio is 1).
- **Prior Universal Bounds**: Brustle, Cai, Wu, and Zhao (2017) proved a universal lower bound of $1/2$. Whether any instance achieves $\max(\text{SO}, \text{BO}) / \text{SB} < 3/4$ under favourable ties remained open.
- **Our Instance**: An explicit $4 \times 4$ instance at $\max(\text{GFT}_{SO}, \text{GFT}_{BO}) / \text{GFT}_M = \frac{19080}{26767} \approx 0.712818 < 0.750000$ (below the $3/4$ bar by $\frac{3981}{107068} \approx 0.03718$), so the worst-case best-offer vs second-best ratio lies in $[1/2, 19080/26767]$. All optimal offers are strictly unique, so the ratio holds under every tie-breaking rule.

## Not Claimed
- We do not claim that the worst-case ratio reaches the Brustle et al. lower bound of $1/2$; we provide an instance at $19080/26767$, placing the worst case in $[1/2, 19080/26767]$.
- We do not claim that posted price $p = 8$ is the optimal second-best mechanism; since posted prices are BIC, IR, and BB by construction, $\text{GFT}_M \le \text{SB}$, which implies $\max(\text{SO}, \text{BO}) / \text{SB} \le \max(\text{SO}, \text{BO}) / \text{GFT}_M = 19080/26767 < 3/4$.

## Credits
- Contributor: `@HindsightWise` (`zerbytheboss`).
- Moshe Babaioff, Shahar Dobzinski, and Ron Kupfer, "A Note on the Gains from Trade of the Random-Offerer Mechanism", arXiv:2111.07790 [cs.GT] (2021), Section 3, for the $3/4$ benchmark.
- Johannes Brustle, Yang Cai, Fan Wu, and Mingfei Zhao for the $1/2$ approximation guarantee.
- Yang Cai, Vineet Gupta, Zun Li, and Aranyak Mehta for AlphaEvolve calibration benchmarks (arXiv:2603.08679).
