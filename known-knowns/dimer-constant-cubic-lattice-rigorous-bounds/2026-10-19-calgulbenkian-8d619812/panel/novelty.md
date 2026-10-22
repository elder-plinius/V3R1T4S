context: Claude Code subagent, fresh context [claude-sonnet-5-5]

role: novelty. Cell: cubic-dimer-l3-ub-55. Target: dimer-constant-cubic-lattice-rigorous-bounds.

## Sources fetched (every attempt was logged; the logs are not shipped in this package)
Retries were allowed by the operator (2026-10-19); the arXiv export API answered 429 several times and succeeded on later tries (all attempts logged). Times are UTC, 2026-10-19, about 07:12 to 07:28.
- the trophy-case file on the main branch of the V3R1T4S repository (fetched from raw.githubusercontent.com), 200, sha256 b946f68eb0a6...; no dimer, cubic-lattice or matching-constant row (only a degree-diameter row matched my keyword search).
- known-knowns listing, api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns, 200, sha256 8a2927f79954...; 20 folders, none on dimers or lattice constants.
- Pull requests: not fetched from api.github.com; I used a snapshot of all V3R1T4S pull requests (titles and bodies; fetched 2026-10-19T04:30:31Z, 473 PRs). Keyword scan (dimer, cubic, matching, collatz, lundow, monomer, z^3, z^4) found no dimer-constant PR; the only hits are unrelated (Potts colouring bounds #460, #461, #483; stable-marriage; Hadamard; a percolation Z^3 bound #481).
- He, arXiv 2607.28810: abstract pages v1 (sha256 64dc633a6aa8...) and v2 (sha256 9d7fdac30892...), both 200. v1 submitted 30 Jul 2026, v2 11 Aug 2026 (16 KB). Abstract: "bounded above by 0.452130, improving the previous best upper bound of 0.457547 obtained by Lundow (2001)". The listing of arXiv search for the phrase "dimer constant" (arxiv.org/search, 200, sha256 eef85a8c8fa1...) returns 7 results; the only post-2015 dimer-constant paper is He (latest version 10 August 2026). The search "dimer cubic lattice upper bound" returns only He.
- arXiv export API, all:"dimer" AND all:"cubic lattice", newest first (200, sha256 50e6503d7179...): newest relevant item is He; nothing newer on bounds (the only 2026 neighbour is a physics paper on cubic dimer dynamics, 2605.15730).
- arXiv export API monomer-dimer AND entropy (200, sha256 6c82b7a2ef95...): newest rigorous-bound items are 1502.06734 (2015) and math/0603001; nothing in the last 24 months on rigorous monomer-dimer or hypercubic dimer bounds.
- Citations of 2607.28810: Semantic Scholar graph API, 200, sha256 b890c0f15f5c..., returned an empty citation list (offset 0, data empty); OpenAlex title search did not find the paper at all. These sources do not index the paper yet, so the empty list is weak evidence. The arXiv listing searches above are the real check. No citing paper found.
- Csikvari lower bound: Butera, Federbush, Pernici arXiv 1305.7028 abs page (200); its table text is not shipped in this package.
- Friedland and Peled arXiv math/0402009 and Friedland, Krop, Lundow, Markstrom arXiv math/0603001 (v3): abs pages and PDFs fetched (200; PDF sha256 1af5cabb56db... and c2aff70b2dca...), converted to text and read at the relevant lines. Also 1502.06734 (PDF sha256 e96a9c6643c4...).
unresolved: Google Scholar or journal-side citation lists for He's paper were not reachable (no browser); Lundow 2001 and Federbush-Friedland 2011 journal texts were not read; the Friedland-Peled entry of Table in math/0402009 was read, not the Journal version. A very new (days old) preprint not yet in the arXiv indexes could still exist.

## Comparator and value read
- Best published rigorous upper bound on l3: He, arXiv 2607.28810 v2, Theorem 1.1: l3 <= 0.452130 (Table 2 entry (5,5), p = 2, rounded up; abstract page fetched as above). Prior: Lundow 0.457547. Claim: l3 <= 0.4520095976 (rounded up: 0.452010), margin 1.2e-4 against 0.452130, far above the 1e-6 the criterion requires.
- Quoted from He's Section 4 (third-party text, not shipped): "using p=4 except for (m,n)=(5,5), for which p=2 was used to reduce the computation time ... approximately 16.5 hours". And from his abstract: a "monotone sequence of upper bounds converging to the true spectral radius". So 0.452130 is the p = 2 member of a sequence; the claim reports a later, converged member at the same cross-section.
- Other competing values: none. No dimer or cubic-lattice pull request in the snapshot; the trophy-case file and known-knowns hold nothing for this target. No later paper than He found (see sources). Closed bulk-close PRs: none for this target.

## Propagation test (PR #350 rule)
Does the claimed value follow from table values or merged claims by a standard rule? Table 2 lists only (5,5) at p = 2 (0.452130), (6,3) at 0.454618 and smaller cross-sections; every entry is an upper bound and the bound for (5,5) cannot be improved by combining entries (monotonicity in cross-section is not shown by He for the values in his table; the (6,3) and (5,4) entries are larger). The only way to reach 0.4520096 is to run more Collatz-Wielandt iterations at (5,5), which is new computation, not an implication. Conclusion: not implied by any published or pending value.

## Open questions for the panel answered here
Q1 (is a deeper iterate at the same cross-section a new result, when it is method-identical to He's Corollary): for novelty, the test is strictly beats everything known. It does, by 1.2e-4, and He's own text says the p = 2 value was a running-time choice, so the sharper value is not published in v1 or v2. Whether a "same method" improvement counts as a record is a criterion question; the bank text asks only for a strictly better rigorous bound with certificate, and I see no clause excluding a deeper iterate. As a novelty matter it is a record against the live table.
Q2 (adequate search): done here: arXiv search by phrase and by topic, the Semantic Scholar and OpenAlex citation routes, the three primary papers. No newer or citing bound found; the citation indexes do not yet cover the paper, which is a stated limit.

## Caveat
A newer He version (v3) or a successor preprint could change the comparator within days; my check is as of the fetch time above.

verdict: the value strictly beats the only live published bound (0.452130) by 1.2e-4, is not implied by any table entry, and no competing PR or later paper was found.

pass: true
