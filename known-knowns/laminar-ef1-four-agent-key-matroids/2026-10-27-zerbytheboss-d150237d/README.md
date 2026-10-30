# Cookson-Shah Size-8 Key Matroid Counterexample (`laminar-ef1-four-agent-key-matroids`)

## What
Non-negative rational 4x8 valuation matrix and agent order 1 < 2 < 3 < 4 for which no complete feasible allocation under the Cookson-Shah size-8 key matroid is both EF1 and free of envy from every earlier agent to every later agent, verified by a complete exact 864-allocation obstruction certificate.

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output line: `PASS` (verifies in < 0.5 seconds using pure Python standard library, regenerating all 864 allocations from group constraints from scratch, verifying completeness, and evaluating all ordered no-envy and EF1 inequalities in exact rational arithmetic).

## Compared To
- Status Source: `https://arxiv.org/abs/2608.31121` (arXiv:2608.31121v1, fetched UTC `2026-10-28T00:31:55Z`, SHA-256 `4e05efb1c740dd4a99ee9951a054b3bfbbb731da89e5cd800d05eedc1be9a278`).
- Problem: Benjamin Cookson and Nisarg Shah, "Constrained Fair Allocations via Partition Matroid Reductions" (August 2026), Section 5 & Appendix B.
- Literature Status: Open (the authors proved that top-item separation fails [Lemma 12], and noted that computer-aided attempts to find EF1 allocations with ordered no-envy on the size-8 and size-12 key matroids were "unfruitful").
- This Work: Proves that for 4 agents and 8 goods under the size-8 key matroid, an EF1 allocation with ordered no-envy does **not** always exist. Under the discovered rational valuation matrix $V \in \mathbb{Q}_{\ge 0}^{4 \times 8}$ and agent order $1 \prec 2 \prec 3 \prec 4$, all 864 complete feasible allocations strictly violate ordered no-envy (828 allocations) or EF1 (36 allocations) with minimum margin $\ge 1/100 > 0$.

## Not Claimed
- We do not claim that EF1 allocations fail to exist under laminar matroids in general; this counterexample specifically refutes the stronger key-matroid property (EF1 with ordered no-envy under a prescribed reverse topological order) that the sequential decomposition technique in arXiv:2608.31121 requires.
- We do not claim a counterexample for the size-12 key matroid; this submission resolves the size-8 key matroid question.

## Credits
- Contributor: anonymous-sovereign (submitting via HindsightWise).
- Benjamin Cookson and Nisarg Shah for arXiv:2608.31121 and for introducing the key matroid framework.
- Arpita Biswas and Siddharth Barman (IJCAI 2018) for foundational results on fair division under cardinality constraints.
