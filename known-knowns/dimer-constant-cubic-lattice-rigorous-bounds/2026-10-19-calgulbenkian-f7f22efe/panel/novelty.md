context: Claude Code subagent, fresh context [claude-sonnet-5-5]

role: novelty. Cell: cubic-dimer-z4-ub-332. Target: dimer-constant-cubic-lattice-rigorous-bounds.

## Sources fetched (every attempt was logged; the logs are not shipped in this package)
Retries were allowed by the operator (2026-10-19); the arXiv export API answered 429 several times and succeeded on later tries (all attempts logged). Times are UTC, 2026-10-19, about 07:12 to 07:28.
- the trophy-case file on the main branch of the V3R1T4S repository (fetched from raw.githubusercontent.com), 200, sha256 b946f68eb0a6...; no dimer, cubic-lattice or matching-constant row (only a degree-diameter row matched my keyword search).
- known-knowns listing, api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns, 200, sha256 8a2927f79954...; 20 folders, none on dimers or lattice constants.
- Pull requests: not fetched from api.github.com; I used a snapshot of all V3R1T4S pull requests (titles and bodies; fetched 2026-10-19T04:30:31Z, 473 PRs). Keyword scan (dimer, cubic, matching, collatz, lundow, monomer, z^3, z^4) found no dimer-constant PR; the only hits are unrelated (Potts colouring bounds #460, #461, #483; stable-marriage; Hadamard; a percolation Z^3 bound #481).
- He, arXiv 2607.28810: abstract pages v1 (sha256 64dc633a6aa8...) and v2 (sha256 9d7fdac30892...), both 200. v1 submitted 30 Jul 2026, v2 11 Aug 2026 (16 KB). Abstract: "bounded above by 0.452130, improving the previous best upper bound of 0.457547 obtained by Lundow (2001)". The listing of arXiv search for the phrase "dimer constant" (arxiv.org/search, 200, sha256 eef85a8c8fa1...) returns 7 results; the only post-2015 dimer-constant paper is He (latest version 10 August 2026). The search "dimer cubic lattice upper bound" returns only He.
- arXiv export API, all:"dimer" AND all:"cubic lattice", newest first (200, sha256 50e6503d7179...): newest relevant item is He; nothing newer on bounds (the only 2026 neighbour is a physics paper on cubic dimer dynamics, 2605.15730).
- arXiv export API monomer-dimer AND entropy (200, sha256 6c82b7a2ef95...): newest rigorous-bound items are 1502.06734 (2015) and math/0603001; nothing in the last 24 months on rigorous monomer-dimer or hypercubic dimer bounds.
- Citations of 2607.28810: Semantic Scholar graph API, 200, sha256 b890c0f15f5c..., returned an empty citation list (offset 0, data empty); OpenAlex title search did not find the paper at all. These sources do not index the paper yet, so the empty list is weak evidence. The arXiv listing searches above are the real check. No citing paper found.
- Csikvari lower bound and Z^4 table: Butera, Federbush, Pernici arXiv 1305.7028 abs page (200); the Z^4 table row is quoted in the-record-we-beat/README.md.
- Friedland and Peled arXiv math/0402009 and Friedland, Krop, Lundow, Markstrom arXiv math/0603001 (v3): abs pages and PDFs fetched (200; PDF sha256 1af5cabb56db... and c2aff70b2dca...), converted to text and read at the relevant lines. Also 1502.06734 (PDF sha256 e96a9c6643c4...).
unresolved: Google Scholar or journal-side citation lists for He's paper were not reachable (no browser); Lundow 2001 and Federbush-Friedland 2011 journal texts were not read; the Friedland-Peled entry of Table in math/0402009 was read, not the Journal version. A very new (days old) preprint not yet in the arXiv indexes could still exist.

## Comparator and value read
- Published Z^4 upper bound: Butera, Federbush, Pernici, arXiv 1305.7028, table of known rigorous bounds (row quoted in the-record-we-beat/README.md; abstract page fetched 200 above): "known rigorous lower and upper bounds [13] defined by (1/2) ln(2d) - 1/2 <= lambda_d(1) <= ln((2d)!)/4d", with the row lambda_4(1): lower 0.53972077, upper 0.66278769. I recomputed ln(8!)/16 = 0.6627876814, which matches. The claim's comparator is correct; the Brégman-type bound is the best rigorous Z^4 bound that this table lists.
- Claimed: l4 <= 0.5840147694 (six places 0.584015), below the comparator by 0.0788.
- Better published Z^4 upper bound? Searched: arXiv phrase and topic searches (monomer-dimer, hypercubic, perfect matchings), the Federbush-Friedland author search (seven papers on expansions, none an upper-bound table for Z^4), the 1502.06734 text (rigorous bounds only for finite regular graphs through the Heilmann-Lieb route, no Z^4 constant), and FKLM v3 and Friedland-Peled (rigorous tori work is for d = 3; I found no Z^4 upper-bound value). None found. No Z^4 PR in the snapshot, nothing in the trophy-case file or known-knowns. He's paper says only that the method generalises; I found no paper that carries it out.
- The bank's p3 requires a citable comparator (DOI/arXiv + page): arXiv 1305.7028, its table of rigorous bounds, is citable.

## Propagation test
A lower-dimensional bound does not propagate to Z^4 by a standard rule (no embedding gives an upper bound for the larger lattice from Z^3 values), and the Brégman bound is the only table value for d = 4. Not implied.

## Open questions answered here
Q2 (comparator right and best citable): confirmed for 1305.7028 as above; I found nothing better in the searches listed. Q3 (Argon's mis-sourced lower bound 0.55808612 vs BFP 0.53972077): confirmed that the BFP table row for d = 4 gives 0.53972077; the lower bound plays no role in the claim. Q1 (is the extension proved) and Q5 (single cross-section) are for the criterion and reproduce roles.

## Caveat
The upper bound in the BFP table is a decade-old general bound; a better Z^4 bound might sit in an unindexed or paywalled source. Coverage is arXiv, the primary papers and citation indexes only.

verdict: strictly below the only citable Z^4 upper bound (0.66278769) by 0.0788, which I confirmed numerically; no better published value or competing PR found.

pass: true
