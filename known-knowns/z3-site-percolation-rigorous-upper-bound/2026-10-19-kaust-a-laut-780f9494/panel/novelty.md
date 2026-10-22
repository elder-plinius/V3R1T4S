# Novelty skeptic verdict: p_c^site(Z^3) <= 4427/10000

context: subagent (fresh, claim/ copy only)

Claim under test: p_c^site(Z^3) <= 4427/10000 = 0.4427, a rigorous upper bound for site percolation on the simple
cubic lattice (target id z3-site-percolation-rigorous-upper-bound). Novelty question: does 0.4427 strictly beat
every explicit rigorous upper bound known? A tie would not count, and confidence intervals and Monte Carlo
estimates are not bounds.

## 1. Status source (fetched once, one plain request, no retries)

- URL: https://arxiv.org/pdf/2106.10388v2
- Request: curl, User-Agent "V3R1T4S-novelty-skeptic/1.0 (one-shot status check)".
- Result: `HTTP 200 application/pdf 465855 bytes https://arxiv.org/pdf/2106.10388v2`
- UTC time (`date -u` immediately before / after): 2026-10-19T00:12:39Z / 2026-10-19T00:12:43Z
- sha256 of the PDF: 1710a31565adaf160bc9607748ca32de839c1717255ff99c838b05dd9f894d74 (identical to the hash in
  the claim's table/literature_record.md, so the document has not changed since the claimant's fetch).
- PDF header: "arXiv:2106.10388v2 [math.PR] 13 Mar 2026 ... Applied Probability Trust (17 March 2026)".
- Value read: Table 1 ("Numerical bounds up to dimension 9"), row d = 3, column ps_c(d): **0,5000 (*)**.
  Footnote (*): "The bound for non-oriented site percolation in dimension d = 3, ps_c(3) < 1/2, was given in [3]",
  where [3] = Campanino, M., and Russo, L. (1985), Ann. Prob. 13 (2), 478-491.
  The introduction: "we believe that most of them are the best rigorous upper bounds in the literature."
  (For contrast, the same row gives bond 0,3473, oriented bond 0,5680, oriented site 0,6422.)
- Abstract page, also fetched once: https://arxiv.org/abs/2106.10388, `HTTP 200`, at 2026-10-19T00:12:50Z.
  It shows "[Submitted on 18 Jun 2021 (v1), last revised 13 Mar 2026 (this version, v2)]", Comments "Accepted for
  publication in the Journal of Applied Probability. First view available", related DOI
  https://doi.org/10.1017/jpr.2025.10041.

Status-table record for site percolation, d = 3: 0.5000 (Campanino-Russo, p_c < 1/2; the strict inequality comes
with no explicit epsilon).

## 2. Literature search (what was searched, what was found)

The question was whether any rigorous, deterministic upper bound on p_c^site(Z^3) at or below 0.4427 has been
published, or any explicit epsilon extracted from Campanino-Russo. I found none. Details:

### arXiv API (export.arxiv.org/api/query, sorted by submission date, newest first)
- `abs:"site percolation" AND abs:cubic AND abs:"upper bound"`: 0 results.
- `abs:"site percolation" AND abs:"three-dimensional" AND abs:bound`: 1 result (2409.11841, super-tree random
  measures; not relevant).
- `abs:percolation AND abs:"cubic lattice" AND abs:rigorous`: 4 results. The only relevant one is
  1312.0961 (Ball, a confidence interval; see below).
- `all:"site percolation" AND all:"upper bound"`: 19 results. None is a Z^3 site threshold bound. The last 24 months
  give 2601.09950 (Z. Li, supercritical disconnection probabilities, no p_c value) and 2509.10160 (triangulations).
- `all:"critical probability" AND all:"upper bound" AND all:percolation`: 16 results. Relevant ones are
  2106.10388 (the status source), 2107.14173 (range-R bond percolation, 2D/3D, bond only) and 2206.12335
  (1-independent percolation on Z^n, not a Bernoulli site bound).
- `all:Campanino AND all:percolation`, `all:"growth process" AND all:percolation AND all:bound`,
  `all:percolation AND all:"interval arithmetic"`, `all:percolation AND all:"computer-assisted"`: nothing on Z^3
  site thresholds. 2609.20764 (Blanc-Renaudie, Sep 2026) treats d > 6 only and states no numerical bound.

### Citation graph
- OpenAlex, works citing Campanino-Russo 1985 (W2090678138, 64 citers): the titles were screened. Apart from the
  status source itself, no citer states a numerical site bound for Z^3 below 1/2. The most recent are 2026 Gomes-Pereira-Sanchis (the status
  source), 2025 papers on the uniform even subgraph / Ising and on Gaussian excursion sets, and older coexistence
  and Gaussian-free-field papers. https://api.openalex.org/works?filter=cites:W2090678138
- OpenAlex, works citing Yu-Wierman 2021 (bond, cubic): 1 citer, the status source.
- OpenAlex, works citing Gomes-Pereira-Sanchis (W3173546782): 0 citers.
- Semantic Scholar, citations of DOI 10.1214/aop/1176993004 (68 entries). Two citers that OpenAlex had missed were
  opened and checked:
  - Jiang and Lang, "Coexistence of infinite clusters for percolation and Ising model on Z^d", arXiv:2609.29806
    (24 Sep 2026), https://arxiv.org/abs/2609.29806. Its Section 4 proves rigorous upper bounds for critical
    probabilities by a second-moment method, but only for d >= 4 ("We fix d >= 4"). Table 2 starts at d = 4
    (site 0.4719, weaker than the status table's 0.4344 for d = 4). Its only d = 3 site figure is the numerical
    estimate 0.31160768(15), not a bound. So it gives no d = 3 site bound.
  - Jiang and Lang, arXiv:2503.21147 (2025), https://arxiv.org/abs/2503.21147: Ising on triangular-type 3D
    lattices; no site threshold bound for Z^3.
- Semantic Scholar keyword search (2022-2026) "site percolation cubic lattice upper bound critical probability":
  15 hits, none a Z^3 site bound. Among them, 2610.11872 (Amit, Oct 2026) concerns 1D long-range percolation:
  https://arxiv.org/abs/2610.11872

### Surveys and growth-process / substitution work (Wierman, Yu)
- Grimmett, "The work of Lucio Russo on percolation", arXiv:1604.04849v2, Section 6
  (https://arxiv.org/abs/1604.04849): "Theorem 6.2 may still be the best rigorous upper bound that is currently known
  for pc. By examining its proof, one may calculate a small epsilon > 0 such that pc < 1/2 - epsilon." No such
  epsilon has been published in anything this search found.
- Yu and Wierman, J. Appl. Probab. 58(3) (2021) 677-692, doi 10.1017/jpr.2020.111: **bond** percolation on the
  cubic lattice, 0.447792 to 0.347297. This is a different model.
  https://www.cambridge.org/core/journals/journal-of-applied-probability/article/abs/an-upper-bound-for-the-bond-percolation-threshold-of-the-cubic-lattice-by-a-growth-process-approach/C1FB01EDD1DB4B08DA84153F79FF2B20
- Wierman and Yu conference abstracts (FAU combinatorics conference, 2024 PDFs): stacked triangular and stacked
  hexagonal **bond** thresholds are at most 0.27455 and 0.45213; the FCC **bond** threshold is at most 0.19170. These
  are not site results and not Z^3. https://www.math.fau.edu/combinatorics/abstracts/wierman55.pdf ,
  https://www.math.fau.edu/combinatorics/abstracts/wierman.pdf
- Yu's JHU dissertation, "Rigorous Bounds for Bond Percolation Thresholds of Three-dimensional Lattices"
  (https://jscholarship.library.jhu.edu/items/bb440f1c-8547-48ad-9d27-53fe32302778): the page returned HTTP 403
  and was not retried. The title and search snippets say it covers bond thresholds only.
- Wierman and Oberly's site bounds by the substitution method and self-matching lattices are for the **square**
  lattice (2D). They are not relevant to Z^3.

### Not bounds (excluded on purpose)
- Ball, arXiv:1312.0961, https://arxiv.org/abs/1312.0961: a 99.9999% confidence interval [0.3110, 0.3118] for
  Z^3 site, in the Balister-Bollobas-Walters style. This is a confidence interval, not a deterministic bound.
- Monte Carlo estimates of p_c^site(Z^3), about 0.3116 (for example the d = 3 entry quoted in 2609.29806).

### Web searches (general engines)
The queries were: "rigorous upper bound site percolation threshold cubic lattice below 1/2"; "site percolation"
"cubic lattice" upper bound growth process Wierman Yu; Campanino Russo 1985 improved explicit epsilon; "p_c" site
percolation Z^3 rigorous upper bound 2025 arXiv computer-assisted; Wierman "site percolation threshold" "simple
cubic"; the same with explicit constants 0.44-0.49; van den Berg Ermakov growth process site percolation three
dimensions; survey "best known upper bound" simple cubic site; slab / bilayer / 1-independent cubic site. They
surfaced only the items above: Campanino-Russo (1/2), Gomes-Pereira-Sanchis (0.5000), bond results, confidence
intervals, and Damron-Newman-Sidoravicius on Z^2 x {0,1} (absence of percolation at criticality, no numerical
bound; https://arxiv.org/abs/1211.4138).

## 3. This repository's records

- TROPHY_CASE.md: no entry mentions percolation (0 matches for "percolat"). The only trophy rows concern other
  problems.
- Upstream pull requests, `gh pr list -R elder-plinius/V3R1T4S --state all --limit 500`, listed at
  2026-10-19T00:17:12Z: 470 PRs (173 open, 155 closed, 142 merged). Titles matching percolation, site, cubic, Z^3,
  lattice, Campanino or growth: #239 and #391 (site-percolation-2-uniform-lattices-thresholds, 2D Monte Carlo
  thresholds), #458 (square-site-percolation-rigorous-bounds, a **lower** bound on Z^2). The other matches are
  sphere packing in a cube, lattice gas and poker. No PR claims anything for Z^3 site percolation.

## 4. Decision

- Best explicit rigorous upper bound known for p_c^site(Z^3): 1/2 = 0.5000 (Campanino-Russo 1985; recorded as
  0,5000 in Gomes-Pereira-Sanchis Table 1, arXiv v2 of 13 Mar 2026 / J. Appl. Probab.). Their strict inequality
  has no published explicit epsilon, and none was found in the citing literature through Oct 2026.
- Claimed bound: 0.4427. That is 0.0573 below the record: a strict improvement, not a tie. No published rigorous
  bound at or below 0.4427 was found for the site model on Z^3.
- Scope and limits: this verdict is about novelty only. It is conditional on the proof and certificates being
  correct, which the other skeptics check. The search did not cover paywalled full texts or MathSciNet. Campanino-Russo
  (1985) itself was not opened. Its abstract and every secondary source state p_c < 1/2 without a numerical epsilon.
- Observation outside the novelty remit, for the other skeptics: claim/outputs/chainA_summary.txt ends with
  "[exited with code 1]" even though every link line reads "CERTIFICATE: PASS". The verification skeptic should
  explain this.

pass: true
