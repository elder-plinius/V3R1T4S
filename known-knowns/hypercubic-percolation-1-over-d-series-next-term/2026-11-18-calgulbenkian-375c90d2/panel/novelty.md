context: Claude Code subagent, fresh context [Sonnet 5.5]

# Novelty report, SID 375c90d2 (claimed partial win p2, binom(d, e-3) coefficient of D_e(q))

## Fetch log (one attempt each, no retries)
- 2026-11-18T17:31:13Z https://en.wikipedia.org/wiki/Percolation_threshold HTTP 200 sha256 7ef9dedef4104f8fbd1860542dbd47204ddb362444acccbcf5d7f8ab49c88193
  Value: hypercubic series still end at 119077/96 sigma^-6 (site) and 4855/12 sigma^-6 (bond), both O(sigma^-7). No sigma^-7 term, no mention of a binom(d, e-3) formula. The page text has no "perimeter polynomial" hit.
- 2026-11-18T17:31:14Z https://arxiv.org/abs/1805.02701 HTTP 200 sha256 90f03436a0fffd90851c8fbe9f4b4ee045c396950f20c23c696defa532119d16 (J. Phys. A 51 (2018) 475001; submitted 7 May 2018).
- 2026-11-18T17:31:20Z https://arxiv.org/e-print/1805.02701 HTTP 200 sha256 c2277e76b34fa4cab645e15c949eadae6adfb8aabbd3b68c017eb07c4492a2cf (matches the hash in the-record-we-beat/README.md).
- 2026-11-18T17:31:34Z https://arxiv.org/pdf/2102.09682 (Hu and Charbonneau 2021, D_n lattices) HTTP 200 sha256 3849fa4f62e9f50a5132a90342ce1b06f3976af53c3d802264ad2befd9aa4d74
- 2026-11-18T17:31:35Z https://www-e.ovgu.de/mertens/research/animals : failed, DNS could not resolve host (curl 6, no HTTP code). Not retried. Its content was only seen in a search snippet (data files and code for perimeter polynomials at fixed size).

## Findings
- Mertens and Moore's source proves closed forms only for binom(d,e), binom(d,e-1), binom(d,e-2) (Theorems 4-6; G^(e), G^(e-1), G^(e-2)). Its abstract says it discusses "what it would take to compute the next ones"; a commented-out passage states D_e(q) for e=12,13,14 would be needed for sigma^-7 "in the absence of some new technique". So the binom(d,e-3) family was an open task in the source paper.
- The 2021 Hu-Charbonneau paper only uses perimeter polynomials of low size for D_n lattices. It has no closed e-3 family.
- Web searches (standard and extended) for "perimeter polynomial", "lattice animals high dimension", "1/d expansion percolation", and 2019-2026 work by Luther, Mertens, Gaunt, Ruskin, Graham found no paper with a binom(d,e-3) formula and no published sigma^-7 coefficient. Related items found: Luther and Mertens arXiv 1106.1078 (site animals up to n=11 by explicit formulas; not the bond e-3 family); Heydenreich-Matzke (first three site terms, lace expansion); arXiv 1912.04584.
- This repository's open and closed pull requests (first 300 listed, filtered by title for hypercubic, perimeter, percolation-1-over, 1805.02701; and gh search for the SID and target id): no other submission for this target.
- Not implied by an older closed form: older sources (Gaunt-Sykes-Ruskin 1976, Gaunt-Ruskin 1978) give only series coefficients and low-order polynomials. The package's own checks (verify-it-yourself/RECEIPTS.md) reproduce Mertens-Moore Theorems 5, 6 and their Appendix A D_11(q) and [binom(d,9)] D_12(1), which is a consistency check and also shows the formula is a genuine extension.
- Restriction/trivial-edit test: the formula is a new coefficient family, not a deletion, relabelling or propagation of a published object.

## Limits
- I could not reach Mertens' animals data page, and could not do citation-graph search (Google Scholar, INSPIRE). A later paper or a data file listing e-3 formulas cannot be fully excluded. I did not rerun the package's checks (that is the reproduce and criterion roles).
- The sigma^-7 term itself is not claimed and was not tested; p2 only requires removing a Table 9 task, which the claim states for (9,12) and (11,14).

pass: true
