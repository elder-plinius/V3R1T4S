# Reproduce Skeptic Report — `bilateral-trade-best-offer-vs-second-best`

context: subagent (fresh invocation)
target_id: bilateral-trade-best-offer-vs-second-best
review_utc: 2026-10-28T22:27:00Z

## Reproduction Audit

1. **Mandatory Benchmark Calibrations**:
   - **BDK 2x2 Calibration (`arXiv:2111.07790`, Section 3)**:
     - Seller support $S = [0, 1]$, $p_S = [1/2, 1/2]$.
     - Buyer support $B = [1, 2]$, $p_B = [1/2, 1/2]$.
     - Posted price $p=1$ achieves $\text{GFT}_M = 1$.
     - Evaluated offers under GFT-favourable tie-breaking: $\text{SO} = 1, \text{BO} = 1 \implies \max(\text{SO}, \text{BO}) / \text{GFT}_M = 1 / 1 = 1$.
     - Evaluated offers under BDK adversarial tie-breaking: $\text{SO} = 3/4, \text{BO} = 3/4 \implies \max(\text{SO}, \text{BO}) / \text{GFT}_M = (3/4) / 1 = 3/4$.
     - Both calibration values match verbatim with zero error.
   - **AlphaEvolve Calibration (`arXiv:2603.08679`, Appendix Code)**:
     - Evaluated modulated power law with $H = 20000$.
     - $\text{FB} = 1.232226$ (paper target $\approx 1.2322$).
     - $\text{SO} = 0.331178$ (paper target $\approx 0.3312$).
     - $\text{BO} = 0.856511$ (paper target $\approx 0.8565$).
     - $\text{RO} = 0.593845$, $\text{FB}/\text{RO} = 2.0750$ (paper target $\approx 2.0749$).
     - All values match printed numbers within one unit of the last printed digit.

2. **Verification of the Discovered Instance**:
   - Discrete distributions given in `claim/instance.json`:
     - Seller support: $S = [1, 2, 7, 14]$
     - Seller probabilities: $p_S = [53/100, 3/100, 21/50, 1/50] = [53/100, 3/100, 42/100, 2/100]$ (sums to 1).
     - Buyer support: $B = [4, 8, 10, 14]$
     - Buyer probabilities: $p_B = [1/100, 19/100, 6/25, 14/25] = [1/100, 19/100, 24/100, 56/100]$ (sums to 1).
   - **Seller-Offering Audit (Every Type)**:
     - $s=1$: offers $p \in \{4, 8, 10, 14\}$ yield profits $3.0000, 6.9300, 7.2000, 7.2800$ respectively. Maximum profit $7.2800 = 182/25$ is achieved uniquely at $p^* = 14$ (GFT = $182/25$).
     - $s=2$: offers $p \in \{4, 8, 10, 14\}$ yield profits $2.0000, 5.9400, 6.4000, 6.7200$. Maximum profit $6.7200 = 168/25$ is achieved uniquely at $p^* = 14$ (GFT = $168/25$).
     - $s=7$: offers $p \in \{8, 10, 14\}$ yield profits $0.9900, 2.4000, 3.9200$. Maximum profit $3.9200 = 98/25$ is achieved uniquely at $p^* = 14$ (GFT = $98/25$).
     - $s=14$: offer $p = 14$ yields profit $0$, uniquely optimal.
     - Total $\text{GFT}_{SO} = \frac{53}{100}\frac{182}{25} + \frac{3}{100}\frac{168}{25} + \frac{42}{100}\frac{98}{25} + 0 = \frac{7133}{1250} = 5.7064$.
   - **Buyer-Offering Audit (Every Type)**:
     - $b=4$: offers $p \in \{1, 2\}$ yield profits $1.5900, 1.1200$. Maximum profit $1.5900 = 159/100$ is achieved uniquely at $p^* = 1$ (GFT = $159/100$).
     - $b=8$: offers $p \in \{1, 2, 7\}$ yield profits $3.7100, 3.3600, 0.9800$. Maximum profit $3.7100 = 371/100$ is achieved uniquely at $p^* = 1$ (GFT = $371/100$).
     - $b=10$: offers $p \in \{1, 2, 7\}$ yield profits $4.7700, 4.4800, 2.9400$. Maximum profit $4.7700 = 477/100$ is achieved uniquely at $p^* = 1$ (GFT = $477/100$).
     - $b=14$: offers $p \in \{1, 2, 7, 14\}$ yield profits $6.8900, 6.7200, 6.8600, 0.0000$. Maximum profit $6.8900 = 689/100$ is achieved uniquely at $p^* = 1$ (GFT = $689/100$).
     - Total $\text{GFT}_{BO} = \frac{1}{100}\frac{159}{100} + \frac{19}{100}\frac{371}{100} + \frac{24}{100}\frac{477}{100} + \frac{56}{100}\frac{689}{100} = \frac{1431}{250} = 5.7240$.
   - **Mechanism Feasibility and Surplus**:
     - Mechanism $M$ is a posted price $p = 8$ (trade occurs iff $s \le 8 \le b$).
     - By construction, a posted price mechanism is dominant-strategy incentive compatible, interim individually rational, and budget balanced (each transaction is settled at $p=8$, so seller receipt equals buyer payment).
     - Trade occurs for $s \in \{1, 2, 7\}$ (cumulative probability $98/100$) and $b \in \{8, 10, 14\}$ (cumulative probability $99/100$).
     - Expected GFT: $\text{GFT}_M = \frac{80301}{10000} = 8.0301$.
   - **Ratio Comparison**:
     - $\max(\text{GFT}_{SO}, \text{GFT}_{BO}) = \text{GFT}_{BO} = \frac{1431}{250} = 5.7240$.
     - Ratio: $\frac{\max(\text{GFT}_{SO}, \text{GFT}_{BO})}{\text{GFT}_M} = \frac{1431/250}{80301/10000} = \frac{19080}{26767} \approx 0.71281802$.
     - Target bar: $\frac{3}{4} = 0.75000000$.
     - Ratio is strictly below $3/4$ by margin $\frac{3}{4} - \frac{19080}{26767} = \frac{3981}{107068} \approx 0.03718198 > 0$.
   - **Strict Offer Uniqueness (Tie-Breaking Invariance)**:
     - Because every seller type and every buyer type possesses a unique optimal offer, the claim holds unconditionally under every tie-breaking rule (favourable, adversarial, or arbitrary).
   - Verified independently with `claim/verify.py` and exact rational arithmetic: PASS.

pass: true
