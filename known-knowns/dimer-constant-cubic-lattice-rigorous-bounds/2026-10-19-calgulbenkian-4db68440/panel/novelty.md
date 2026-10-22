context: Claude Code subagent, fresh context [claude-sonnet-5-5]

role: novelty. Cell: cubic-dimer-h3-ub-54 (p2 upgrade). Target: dimer-constant-cubic-lattice-rigorous-bounds.

Package hashes: all listed files verified OK (run from inside the package folder, where the list's relative paths resolve; run from elsewhere it reports "could not be read", which is a path issue only).

## Sources (every fetch attempt was logged with UTC time, status and sha256; the log is not shipped)
Date of fetches: 2026-10-19, about 12:51 to 12:53 UTC (system clock). All first tries succeeded except one Semantic Scholar 429 (retried after 20 s, 200).
- He, arXiv 2607.28810 via the arXiv export API (id_list v1,v2): 200, sha256 52233a67...; v1 published 2026-07-30T20:13:33Z, v2 updated 2026-08-11T02:35:27Z; nothing later. Abstract: "bounded above by 0.452130" for the dimer constant of Z^3; no monomer-dimer statement.
- arXiv search listing for 2607.28810 (200): resolves to the paper's own abstract page (sha256 9d7fdac3..., identical to the earlier group fetch); arXiv has no citing-papers list.
- arXiv search "dimer entropy upper bound cubic", newest first (200): "produced no results".
- arXiv export API, monomer-dimer AND three-dimensional, newest first (200, sha256 be488446...): newest items are 2026-01-06 (frustrated Heisenberg, unrelated), 2024-06-09 and 2022-05-24 (monopole-dimer model, a different model), 2017, 2014, 2007 (Approximating the monomer-dimer constants through matrix permanent, an estimate) and 2006 (Generalized Friedland-Tverberg). No rigorous h3 upper bound in 2024 to 2026.
- arXiv author searches (200): Friedland, Lundow, Markstrom lists "Validations of the Asymptotic Matching Conjectures" and "The 1-vertex transfer matrix and accurate estimation of channel capacity" (not h3 bounds); Friedland, Peled lists the SOFT pressure paper, "On the First Eigenvalue of Bipartite Graphs", "The Polytope of Dual Degree Partitions" and "Theory of Computation of Multidimensional Entropy with an Application to the Monomer-Dimer Problem" (this last is math/0402009, the source of the comparator). Nothing newer.
- Semantic Scholar citations of FKLM math/0603001 (200, sha256 df505db3...): 100 citing items, newest 2020 ("A proof of the upper matching conjecture for large graphs", "Errata and Addenda to Mathematical Constants"); none states an h3 upper bound. Citations of He 2607.28810 (200, sha256 b890c0f1...): empty list; this index does not know the paper yet, so the empty list is weak evidence. Citing papers of He are therefore not enumerable from any source I could reach; the arXiv searches above are the working check.
- The repository trophy-case listing (200, sha256 b946f68e...): the only dimer/matching keyword hit is a degree-diameter row; nothing on dimers. Known-knowns listing (200, sha256 8a2927f7...): no dimer or lattice-constant folder.
- V3R1T4S pull requests: I used a snapshot of all V3R1T4S pull requests (titles and bodies; 473 PRs, fetched 2026-10-19T04:30:31Z, highest number 483) rather than the api.github.com pulls pages. No dimer, monomer-dimer or h3 PR in it. The snapshot predates the author's own filings, so I made one single GET of PR 537 itself (api.github.com pulls/537, 200): "[claim] dimer-constant-cubic-lattice-rigorous-bounds: monomer-dimer entropy h3 at most 0.7860441 at (3,3)", state open, not merged, by calgulbenkian (the claimant), created 2026-10-19T08:34:25Z. This is the author's own filing, not a competing value; this claim replaces it in place. I did not enumerate PRs newer than 483 beyond #537 (no list call made), so a third-party h3 PR filed after the snapshot cannot be excluded from this evidence.
- Earlier work reused read-only: the Friedland-Peled math/0402009 and FKLM math/0603001 v3 PDFs.

## Comparator, confirmed at source
FKLM (math/0603001 v3), introduction: "The numerical computations in [12] yield the best known upper bound h_3 <= 0.7862023450." Friedland-Peled (math/0402009) text: "the best upper bound for h3 from our data is log beta(4,4)/16 = 0.7862023450" and "0.7652789557 <= h3 <= 0.7862023450 (8.2)". No later rigorous h3 upper bound found anywhere reached (arXiv searches, FKLM citers to 2020, Friedland, Lundow, Markstrom and Peled author lists, 2024 to 2026 monomer-dimer listings). The Butera-Federbush-Pernici h3 values are non-rigorous estimates.

## Is 0.7859681 a record?
Margin below the comparator: 0.7862023450 - 0.7859681 = 2.34e-4 (the claim's own exact unrounded value 0.785968076808... gives 2.34e-4 too). It is strictly below the only known rigorous upper bound, by far more than the target's 1e-6 threshold. It is also below #537's 0.7860441 by 7.6e-5, so it supersedes it; ties are not an issue.

## Propagation test (PR #350 rule)
- Table propagation: the FP table entries at other cross-sections are either larger upper bounds or non-bounding (rectangular entries; FP use only the square (4,4) for the upper bound). Nothing in any table gives a value below 0.7862 by monotonicity.
- Cross-quantity propagation: an upper bound on the dimer entropy l3 (He's 0.452130 or the main-win 0.4520095976) does not bound h3 from above, since h3 >= dimer entropy at p = 1 (h3 is a sup over densities). No standard rule maps the dimer bounds to h3.
- Merged or pending values: none on this quantity in the pull-request snapshot or the repository trophy-case listing.
- Same-claim propagation: (5,4) vs #537's (3,3) is the same theorem with a larger matrix. Under the #350 rule a larger-matrix bound of one's own method is the improvement itself, not a derived value; the (3,3) bound does not imply the (5,4) bound (it is the weaker one). So only the (5,4) value should stand as the record.
- Method-as-propagation worry: the extension (monomer-dimer version of He's argument) is unpublished and the author's own, so there is no published value it could be implied by.

## Open questions concerning novelty
- Q3 (is there a newer rigorous upper bound on h3; was the comparator's credit to Friedland-Peled right): comparator credit confirmed at the primary text (FP (4,4) entry, FKLM quote above). No newer rigorous bound found in the sources listed; the builder's three queries and my own additional ones agree.
- Q2, Q1, Q4, Q5 (proof of the extension, sup-versus-limit definition of h3, orbit expansion, independence of the C program) are mathematical/reproduction questions, outside novelty; I do not judge them. Novelty-side note for Q2: the comparator and the claim use the same quantity h3 = sup over p of h3(p) as defined in FKLM, so the comparison is like-for-like.

## unresolved
- Citations of He's paper beyond arXiv's own search: Google Scholar/journal-side lists unreachable; Semantic Scholar and OpenAlex do not index it. A very recent (days old) preprint could exist.
- PRs filed after the 2026-10-19T04:30Z snapshot other than #537 were not listed.
- Lundow 2001 and Federbush-Friedland (J. Stat. Phys. 2011) journal texts not read; FKLM v3 (2008) would have cited any better h3 bound of that era, and FKLM's citers to 2020 show none.

verdict: 0.7859681 is strictly below the only known rigorous h3 upper bound (0.7862023450, Friedland-Peled via FKLM) by 2.34e-4, is not implied by any table or merged/pending value under the PR #350 rule, and properly supersedes the claimant's own open #537 (0.7860441); no competing paper or PR found.

pass: true
