context: Claude Code subagent, fresh context [Sonnet 5.5]

ROLE novelty, cell potts-wsq5-ub. Target: potts-antiferromagnet-colouring-entropy-bounds, cell W_sq(5) upper bound (C_14 cylinder).

## Sources fetched (one plain request each, curl with the honest user agent; saved files are not shipped in this package)
- Primary status page, Cambridge Core article page of Lundow and Markstrom: UTC 2026-10-18T18:23:02Z, HTTP 200, sha256 9983a7438a6acb1bc51f99c9d980ae59dab4f55fa00d27e674ca781e9f4260cf. Abstract quoted: "As applications of this method we give currently best known bounds for the number of 4- and 5-colourings of the square grid". Published LMS J. Comput. Math. 11 (2008) pp. 1-14, DOI 10.1112/S1461157000000498.
- Full paper PDF (link on that page, served openly): UTC 2026-10-18T18:23:42Z, HTTP 200, sha256 63dfff930c191cae7ac0d17d0217d97dc0ed1425d5c4ef88f12cc0741c9c9f86 (the saved copy is not shipped in this package). It confirms the bank text exactly: eq. (8) "3.2504049231640764 <= lambda_s(5) <= 3.250407145038276"; the paper's remark "To our knowledge these are currently the best rigorous bounds" follows its printed bounds (stated there for q=4).
- The inequality used (eq. (6) of the paper): theta_1(k+1)/theta_1(k) <= lambda_s(q) <= theta_2(2k)^(1/2k), with theta_2 the maximum eigenvalue of the cycle (C_k) transfer matrix. So the claim's inequality W <= theta_1(C_m)^(1/m) for even m is the paper's own upper bound.
- Table 3 (5 colourings) of the paper stops at C_12 = 1390763.1270219. I recomputed 1390763.1270219^(1/12) = 3.25040714503827, so the published upper bound is exactly the widest cycle in the table, and the claim's C_14 cylinder is one even width beyond the paper (the paper has no C_14 eigenvalue).
- Margin against the published value: 3.250407145038276 - 3.250405205878550 = 1.939e-6 (above the 1e-9 required). (This role does not judge whether the claimed value is itself correct; that is the reproduce role.)
- the trophy-case file: UTC 2026-10-18T18:23:03Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1. No mention of Potts, colouring or Lundow.
- Pull requests pages 1 to 5 (state=all, 100 per page; all HTTP 200, times 18:23:03Z to 18:23:11Z, sha256 b5eb38dd..., 6fb3f2b2..., 38689418..., db2001e7..., ca276d1a...): I scanned titles and the first 3000 characters of every body for potts, colouring, antiferro, entropy, W_sq, lundow, transfer. No PR on this target. (Unrelated hits only, e.g. #401 erdos-617 balanced colouring, a bank PR by the same contributor.)
- known-knowns directory listing: UTC 2026-10-18T18:23:12Z, HTTP 200, sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011. 20 folders; none is a Potts/colouring target, so there is no merged folder for this target.
- The author's own earlier filings: the claim record (not shipped) says this is a new claim, not a refile; no closed PR named.
- Primary table is a journal paper, not a GitHub repository, so no repository PR/issue/commit fetch applies.

## Literature (arXiv export API, four queries; plus two web searches)
1. all:"transfer matrices" AND Potts AND antiferromagnet AND entropy: 0 results.
2. au:Lundow AND au:Markstrom: 12 results, all Ising/random-cluster/permanent/3-SAT/channel-capacity papers; none on colouring bounds after 2008 (the 2008 paper itself did not appear in the API).
3. "graph homomorphisms" AND "transfer matrices": 0 results.
4. zero-temperature Potts antiferromagnet square, newest first: 30 results; newest is 2512.06762 (a machine-learning study of the 2D antiferromagnetic q-state Potts model), the rest 2010 and earlier (Jacobsen-Salas-Sokal, Chang-Shrock, Salas-Sokal, Biggs-type bounds, 1502.07254 lower bounds). None gives a rigorous upper bound for W_sq(5) from a cycle wider than C_12.
Web searches (2 queries) for later rigorous bounds, cylinder widths beyond C_12, and 2025-2026 work found no improvement over eq. (8).
unresolved: Google Scholar was not queried (no browser); arXiv coverage is limited to four queries; the bank's own "no later improvement" search (2026-10-15) is not independently re-run beyond this. A later bound in a journal not indexed by arXiv or by the web search cannot be excluded, though none is signalled and the target's bank text and the later cited papers (1502.07254, 1806.06751) are listed as sources by the bank without a better upper bound.

## Verdict
The published rigorous upper bound is confirmed from the paper itself, and the claimed value is strictly smaller by far more than 1e-9; it is not a tie, no competing PR or trophy exists, and no later bound was found. Caveat: the claim extends the paper's own method to wider cylinders, so its novelty rests on the new width, not on a new idea.
novelty: new strict improvement over eq. (8) found no competing value
pass: true
