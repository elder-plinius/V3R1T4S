# Novelty skeptic: p_c^site(Z^3) >= 0.263376

context: subagent (fresh, claim/ copy only, web)

Claim under test: p_c^site(Z^3) >= 263376/10^6 = 0.263376, a rigorous lower bound for site percolation on the
simple cubic lattice. Criterion: the bound must be strictly above every explicit rigorous lower bound that is
published, or directly implied by published results, at verification time (2026-10-19).

## Verdict in one paragraph

The author's record is wrong about what the previous record is. It names 0.21103 (1/4.7387, Ponitz-Tittmann
2000). The best published rigorous lower bound is in fact **p_c^site(Z^3) > 0.2522**, from Georgakopoulos and
Panagiotis, Combinatorics, Probability and Computing 32 (2023) 912-955 (Theorem 7.1), first posted as
arXiv:1908.03426 in August 2019. The paper itself calls it "the best rigorous lower bound known". 0.263376 still
strictly beats it, by 0.011176 (about 4.4 %). I found nothing published or posted, in the last 24 months or
earlier, that is at or above 0.263376. That includes any proof of Torquato-Jiao's 5/19 (= 0.263158); the claim is
above 5/19 anyway, by 0.000218. Novelty holds, but the record named in CLAIM.md, table/literature_record.md and
result/bound.json must be corrected to 0.2522 (Georgakopoulos-Panagiotis), and that paper must be credited.

## Status sources named in CLAIM.md (one request each, no retries)

| source | URL | fetched (UTC) | HTTP | bytes | sha256 | value read |
|---|---|---|---|---|---|---|
| Ponitz-Tittmann, EJC 7 R21 (landing page, as named) | https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r21 | 2026-10-19T09:08:09Z | 200 | 16771 | 5b2f29d794f2852152925ddc13a3ae0f2de98697eb7d81f9f523d1a898875a06 | abstract: "The upper bound in dimension two is 2.679192495." (the d = 3 value is not on the landing page) |
| Ponitz-Tittmann, EJC 7 R21 (PDF) | https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r21/pdf | 2026-10-19T09:08:54Z | 200 | 112294 | ccd467b28d9d371d12a3e8187dfba8ea35acc0a724e4b490e45c324fdc6d224f (same as the author's record) | "In this paper, we improve these bounds to 2.6792 and 4.7387, respectively"; table row "14 2.7014 4.7387 6.8040"; 1/4.7387 = 0.21103 |
| Torquato-Jiao, arXiv:1302.0332 (abstract, as named) | https://arxiv.org/abs/1302.0332 | 2026-10-19T09:08:11Z | 200 | 44418 | 5311ed8ff281ca1119bc53e896d2e1c06ec3f75533b18d6e6edd760699d9ce61 (same as the author's record) | "These results lead to certain lower bounds on the percolation threshold p_c ..." (no number in the abstract) |
| Torquato-Jiao, arXiv:1302.0332 (PDF) | https://arxiv.org/pdf/1302.0332 | 2026-10-19T09:14:46Z | 200 | 461234 | b71fb7eaacb2a804c5460c1c41b9f68d05522c410f96aeff2fb5c470500aaf16 (same as the author's record) | Table III, site, d = 3: "3  0.3116004  0.2631578947...  0.2000000000...  0.1666666666..." (columns: Eq. (43) [2,1] Pade, Eq. (37) [1,1], Eq. (29) [0,1]); "While the [0,1] estimate of pc was proven to be a lower bound here, rigorous proofs of that the [1,1] and [2,1] estimates are indeed lower bounds will be reserved for a future publication." |

All status sources could be read; there was no block. One correction to the record: Torquato-Jiao's proven bound
(Eq. (29), p_c >= 1/z) is **1/6** for site Z^3, not 1/5 as CLAIM.md says. The value 1/5 = 1/(2d-1) is their
unproven [1,1] value, and it also follows from the classical non-backtracking-walk bound. This changes nothing
here, because both values are far below the record.

## The actual record (found in this check; missing from the author's record)

- A. Georgakopoulos and C. Panagiotis, "On the exponential growth rates of lattice animals and interfaces",
  Combin. Probab. Comput. 32 (2023) 912-955, https://doi.org/10.1017/S0963548323000214. Preprints:
  arXiv:1908.03426 (v1 9 Aug 2019, v2 13 Jul 2021) and arXiv:2107.06272 (13 Jul 2021).
  - Fetched: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/96D87E5F67E90E4E781BDE8108513657/S0963548323000214a.pdf/on-the-exponential-growth-rates-of-lattice-animals-and-interfaces.pdf,
    2026-10-19 at about 09:10Z (web-fetch tool, between the timestamped requests at 09:08:54Z and 09:14:46Z),
    HTTP 200, 878014 bytes, sha256 f474eb138f13fd22073b49a7f7e21a4d9297db7144ae417caa5c2b3892be38d2. The arXiv
    abstracts https://arxiv.org/abs/2107.06272 and https://arxiv.org/abs/1908.03426v1 were also read; both state 0.2522.
  - Quotes: abstract, "We obtain the rigorous lower bound pc(Z3) > 0.2522 for 3-dimensional site percolation.";
    Section 1, "In dimension 3, the same paper proves a(Z3) < 9.3835. Plugging this into (2), we deduce
    pc(Z3) > 0.2522, which is the best rigorous lower bound known."; Theorem 7.1, "We have pc(Z3) > 0.2522."
    The paper also says the previous best was "about pc(Z3) > 0.21225", the inverse of a connective-constant
    bound.
  - What is directly implied: the formula a >= (1/p)(1-p)^{-(1-p)/p} at p = p_c, with the Barequet-Shalah
    bound a(Z^3) < 9.3835 (Algorithmica 2022, arXiv:1906.11447), gives p_c > 0.252265. To reach 0.263376 by
    this route, someone would need a(Z^3) <= 8.9272. No published polycube growth-constant upper bound below
    9.3835 was found. An arXiv listing of "polycubes" and "lattice animals" + "growth constant", sorted by date
    up to Oct 2026, shows no improvement.
- Margin: 0.263376 - 0.2522 = 0.011176 (0.263376 - 0.252265 = 0.011111).

## Other candidates checked (none reaches 0.263376)

- Torquato-Jiao 5/19 = 0.263158: I searched for a proof or a follow-up ("future publication") and found none.
  The claim is above 5/19 regardless, by 0.000218.
- N. Ball, arXiv:1312.0961 (J. Stat. Phys.): site [0.3110, 0.3118] "with 99.9999% confidence". This is a Monte
  Carlo confidence interval, not a proof, so it is not counted as a rigorous bound. Open PR #481 in this repo
  takes the same position.
- Self-avoiding-walk connective constant: no rigorous upper bound below 4.7387 found (Alm 1993 4.756,
  Goulden-Jackson 4.7476, Ponitz-Tittmann 4.7387). This route cannot defeat the claim in any case: even the
  numerical value mu ~ 4.684 gives 1/mu ~ 0.2135.
- Bond percolation lower bounds: these bound p_c^bond, whose numerical value is about 0.2488. The Yu-Wierman
  JHU thesis (3D bond bounds) says the bond lower bound is only 1/mu. These cannot reach 0.263376.
- Heydenreich-Matzke (lace expansion for the site p_c of Z^d): asymptotic in d with an O(1/d^4) error; no
  explicit bound for d = 3.
- M. Puljic, arXiv:1307.2827: claims an infinite open path for p >= 1/d. That is an upper-bound-type claim,
  and it is false at d = 2 (it contradicts p_c^site(Z^2) >= 0.556). It is irrelevant to lower bounds.
- Searches run: arXiv API queries sorted by date, through 2026-10, for "percolation threshold" + "lower bound";
  "site percolation" + cubic / Z^3 / three-dimensional; "critical probability" + cubic lattice; percolation +
  rigorous + bound; "lattice animals" + percolation; polycubes / lattice-animal growth constants. Also web
  searches (rigorous lower bound for site Z^3, neighbour-avoiding walks, 5/19, Torquato-Jiao follow-ups, Wierman
  3D work, computer-assisted Duminil-Copin-Tassion criterion, GitHub/Zenodo) and GitHub repository searches.
  None of these found anything from the last 24 months (2024-10 to 2026-10) giving a rigorous lower bound for
  p_c^site(Z^3) or p_c^bond(Z^3), or an improved d = 3 animal or walk bound.

## This repository

- TROPHY_CASE.md: no percolation entries. Its families are degree-diameter graphs, constant-weight codes,
  matrix multiplication, Lehmer, VNN-COMP, RobustBench, and the cipher commitments.
- Open pull requests of elder-plinius/V3R1T4S (`gh pr list -R elder-plinius/V3R1T4S --state open --limit 300`,
  242 open, queried 2026-10-19 between 09:06:04Z, the creation time of the newest PR, and 09:08:09Z). Titles and
  bodies were searched for percolation, Z^3, p_c, neighbour-avoiding, 5/19, Torquato and Ponitz. The
  percolation-related PRs are #481 (Z^3 site *upper* bound 0.4427), #458 (Z^2 site lower bound 0.5567), #391
  and #239 (2-uniform lattice threshold estimates) and #534 (2D connective constant). **None claims a lower bound
  for p_c^site(Z^3) or p_c^bond(Z^3).**

## Method (information only, not a pass/fail criterion)

I found no published use of exactly this method. Its pieces are: a canonical breadth-first-search parent tree
with smallest-direction tie-breaking; forcing "shortcut" sites and lexicographically earlier "turn corners" to be
closed; and the inequality theta <= K_N(p) theta summed over 20-step neighbour-avoiding walks. Its relatives are:
- Hammersley's self-avoiding-walk argument (p_c >= 1/mu).
- The fact that shortest open paths in site percolation are induced (neighbour-avoiding) paths. Plain counting
  of these paths only reaches about 1/4.08, roughly 0.245; by the claim's own counts, a_20/a_18 = 16.66.
- Hammersley/Simon-Lieb-type renewal inequalities.
- 2D site lower bounds by different or unverified methods: Toth 1985 (0.503, "elementary combinatorial
  considerations"; full text not accessed), Zuev, Menshikov-Pelikh, van den Berg-Ermakov (0.556).
- Georgakopoulos-Panagiotis, who use lattice-animal/interface counting, a different method.

This method search was not exhaustive.

## Required before any release (does not change the novelty verdict)

1. Replace "previous record 0.21103" in CLAIM.md, table/literature_record.md and result/bound.json with
   p_c^site(Z^3) > 0.2522 (Georgakopoulos-Panagiotis, CPC 32 (2023) 912-955, Theorem 7.1; arXiv:1908.03426),
   and credit it. The improvement is +0.0112, not +0.0523.
2. Correct the Torquato-Jiao summary: their proven bound is 1/z = 1/6 for site Z^3. The values 1/5 ([1,1]) and
   5/19 ([2,1]) are not proven there.

novelty: CONFIRMED. 0.263376 strictly exceeds the best known rigorous lower bound, 0.2522 (Georgakopoulos-Panagiotis 2023); no bound >= 0.263376 found.
pass: true
