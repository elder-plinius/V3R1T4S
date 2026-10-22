context: Claude Code subagent, fresh context [claude-sonnet-5-5]

role: novelty. Cell: cubic-dimer-he-table2. Target: dimer-constant-cubic-lattice-rigorous-bounds.

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

## Re-judgement against the p1 text (coordinator follow-up)
p1 text: "Independent reimplementation that reproduces He's 0.452130 at (m, n) = (5, 5) and every smaller entry of his Table 2 to six decimals (rounded upward) with exact arithmetic; reproduction only". For this win, matching the published values is the requirement, so a tie with He's table is not a disqualifier. The novelty question becomes: is this the first independent reproduction? This is a second run of the method: He's own Java computation is the first. It is not a second independent reproduction if none other exists.

## Search for an existing independent reproduction
- V3R1T4S pull requests: the snapshot of all pull requests (fetched 2026-10-19T04:30:31Z, 473 PRs) has no PR on this target; keyword scan (dimer, cubic, matching, collatz, lundow, monomer) found only unrelated PRs. The trophy-case file and the known-knowns listing hold nothing on it.
- Papers: arXiv phrase searches for "dimer constant" and "dimer cubic lattice upper bound" return only He (latest version 10 August 2026) among post-2015 items; the export API listing shows nothing newer; Semantic Scholar citations of 2607.28810 are empty (the paper is not indexed, so this is weak evidence). No paper citing or reproducing He found.
- Repositories: GitHub repository search (api.github.com/search/repositories, 200 at 2026-10-19T07:28:39Z, sha256 08c082fdf7ca...) for "dimer constant cubic lattice Collatz-Wielandt" returns total_count 0. He's paper says its code is a Java implementation; I found no published code or reproduction.
- Result: no published or filed independent reproduction found. The entries claimed are He's published values: (2,2) 0.486478 ... (5,5) 0.452130 (Table 2, as listed in the-record-we-beat/README.md).

## Other points
- Open question 3 (is a reproduction a record in its own right): for novelty, p1 is first-of-its-kind only in the sense above; the bank text itself says it is "reproduction only". Whether the claimant's own team (same Argon team) counts as independent of He is clear: it is a different author and different code.
- Limits: as in the common section above (citation indexes do not cover the paper; no browser; very new preprints or private repositories could exist).

verdict: no earlier independent reproduction of He's Table 2 found anywhere searched; this would be the first, and a second run of the method after He's own. The comparator is matched by design, as p1 requires.

pass: true
