# Novelty Skeptic Report — `bilateral-trade-best-offer-vs-second-best`

context: subagent (fresh invocation)
target_id: bilateral-trade-best-offer-vs-second-best
review_utc: 2026-10-28T22:27:00Z

## Novelty & Prior Art Audit

1. **Status Source and Literature Benchmark**:
   - Status Source: `https://export.arxiv.org/api/query?search_query=abs:%22bilateral%20trade%22&sortBy=submittedDate&sortOrder=descending&max_results=50`
   - Primary reference: Moshe Babaioff, Shahar Dobzinski, and Ron Kupfer, "A Note on the Gains from Trade of the Random-Offerer Mechanism", arXiv:2111.07790 (Section 3).
     - BDK exhibited a $2 \times 2$ instance where the best-offer mechanism achieves at most $3/4$ of the second-best gains from trade, but noted that this bound relies entirely on adversarial tie-breaking. Under GFT-favourable tie-breaking, the ratio collapses to 1.
   - Universal guarantee: Brustle, Cai, Wu, and Zhao (2017) established that the random-offerer mechanism achieves at least $1/2$ of the second-best GFT, which implies $\max(\text{SO}, \text{BO}) \ge \frac{1}{2} \text{SB}$.
   - The open problem in the literature was whether an instance exists achieving a ratio strictly below $3/4$ that survives favourable tie-breaking (or strictly unique optimal offers).

2. **Literature Survey (2024–2026)**:
   - Recent 2026 papers on bilateral trade:
     - arXiv:2603.08679 (AlphaEvolve): focuses on the Random Offerer (RO) vs First-Best (FB) ratio, reporting $\text{FB}/\text{RO} \approx 2.0749$. It does not evaluate Second-Best (SB) or compare best-offer to second-best. (Our audit in Lens 1 demonstrates that AlphaEvolve has $\text{BO}/\text{SB} \approx 0.8206 > 3/4$).
     - arXiv:2607.13959 (M. Jo), arXiv:2609.37997 (Bei et al.), arXiv:2610.06547 (Shang and Chen): establish bounds for RO versus First-Best (FB), pushing $\text{FB}/\text{RO}$ towards $2.2886$.
     - arXiv:2606.03849, 2609.18724, 2609.30702, 2609.37366: investigate second-best efficiency in matching markets or versus first-best.
   - As confirmed by the bank problem description (checked 2026-10-25) and our fresh arXiv status check (2026-10-28T22:15:43Z), no prior work has established a best-offer vs second-best ratio below $3/4$ under favourable ties.

3. **Comparison Against Known Records**:
   - Incumbent published bound: $3/4 = 0.750000$ (BDK 2021, valid only under adversarial tie-breaking).
   - Favourable tie-breaking incumbent: $1.000000$ (on BDK $2 \times 2$).
   - Current discovery: $\frac{19080}{26767} \approx 0.71281802$, strictly beating $3/4$ by a margin of $+0.03718198$.
   - Because all optimal offers are strictly unique, the result holds identically under all tie-breaking rules.
   - Zero competing claims in `TROPHY_CASE.md` and zero open pull requests on `elder-plinius/V3R1T4S`.

pass: true
