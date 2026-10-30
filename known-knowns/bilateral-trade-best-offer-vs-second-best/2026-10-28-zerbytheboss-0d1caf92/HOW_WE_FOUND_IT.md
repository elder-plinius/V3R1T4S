# How We Found It — `bilateral-trade-best-offer-vs-second-best`

*contributor text, unverified*

## Background & Problem
In bilateral trade with independent private values, Babaioff, Dobzinski, and Kupfer (arXiv:2111.07790, Section 3) showed that on a 2x2 instance, the better of seller-offering (SO) and buyer-offering (BO) gains from trade can be at most 3/4 of the second-best (SB) gains from trade under adverse tie-breaking. However, under favourable tie-breaking, that ratio is 1. Brustle et al. (2017) proved a universal lower bound of 1/2. The open problem was whether there exists any bilateral trade instance where max(SO, BO) / SB < 3/4 under GFT-favourable tie-breaking.

## What Failed
1. Testing published hard instances for Random-Offerer (RO) vs First-Best (FB): The AlphaEvolve modulated power law instance (arXiv:2603.08679) gives max(SO, BO) / SB approx 0.8227 > 0.75, failing to beat the 3/4 bar against second-best.
2. The BDK Section 2 family for H = 3..20 has max(SO, BO) / SB monotonically increasing towards 1 as H grows.
3. Continuous power law and uniform distributions generally satisfy max(SO, BO) >= 0.82 * SB.

## What Worked
1. **Adversarial Rational Search Formulation**:
   - We formulated a discrete support search over asymmetric distributions where both seller and buyer have skewed pricing incentives.
   - To make max(SO, BO) low relative to a posted price mechanism M, we designed the valuations such that:
     - Seller types are tempted to make aggressive high offers (aiming for the high buyer value), sacrificing trade volume with intermediate buyer types.
     - Buyer types are tempted to make aggressive low offers (aiming for the low seller value), sacrificing trade volume with intermediate seller types.
     - A simple posted price p = 8 clears the vast majority of mutually beneficial trades without the informational rent extracted by the single-offerer mechanisms.
2. **Discovery of 4x4 Counterexample**:
   - Discrete grid optimization isolated support sets $S = [1, 2, 7, 14]$ and $B = [4, 8, 10, 14]$.
   - Rational probability vectors $p_S = [53/100, 3/100, 42/100, 2/100]$ and $p_B = [1/100, 19/100, 24/100, 56/100]$.
   - Crucially, every seller type has a strictly unique profit-maximising offer ($p = 14$), and every buyer type has a strictly unique profit-maximising offer ($p = 1$). Therefore, tie-breaking rules have zero effect!
   - Under this instance:
     - $\text{GFT}_{SO} = 7133/1250 = 5.7064$
     - $\text{GFT}_{BO} = 1431/250 = 5.7240$
     - Posted price $p = 8$ yields $\text{GFT}_M = 80301/10000 = 8.0301$
     - Exact ratio: $\max(\text{SO}, \text{BO}) / \text{GFT}_M = 19080/26767 \approx 0.712818 < 3/4 = 0.75$ with strict margin $0.03718$.
