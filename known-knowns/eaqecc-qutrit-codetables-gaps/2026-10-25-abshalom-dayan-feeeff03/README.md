# Entanglement-assisted qutrit code `[[24, 4, 13; 10]]_3` (the table lists `[[24,4,12-19;10]]_3`)

## What

The 30 x 48 GF(3) stabilizer matrix S in claim/object/eaqecc_24_4_13_10.json (sha256 feeeff03749ecfd57a5b84b8778a2ffe2111723da17f31a3f197d02d048c1794) has s = 30 independent rows and rank(S J S^T) = 20, so c = 10 and k = 4, and an exhaustive enumeration of all 3^18 - 1 nonzero vectors of span(S)^perp gives exactly 13 as the minimum symplectic weight outside span(S) ∩ span(S)^perp, so it is a non-catalytic EAQECC [[24,4,13;10]]_3 whose d = 13 is strictly greater than d_lower 12 and at most d_upper 19 of the listed cell [[24,4,12-19;10]]_3 of https://eaqecc.codetables.de/qutrit.php as re-fetched 2026-10-25T11:22:04Z (sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c), a value the page's six propagation rules applied to its listed non-teleportation cells do not reach (they give 12 there).

Note: the sentence above is quoted word for word from `panel/gate.md` (`confirmed_scope`, from the CRITERION skeptic's
verdict); `claim/` in it is this package's root. The object's full SHA-256 is
`feeeff03749ecfd57a5b84b8778a2ffe2111723da17f31a3f197d02d048c1794`.

Path note: the panel files (including `panel/claim.sha256`, which lists the claim folder's files) and
`how-we-built-it/PREREG.md` refer to the run's claim folder. There, `claim/object/eaqecc_24_4_13_10.json` is
`object/eaqecc_24_4_13_10.json`, `CLAIM.md` is `README.md` (with `HOW_WE_FOUND_IT.md`), `REPRODUCE.md` is
`RUN_IT_YOURSELF.md`, `checkers/` is `verify-it-yourself/`, `rebuild/` is `how-we-built-it/` and `table/` is
`the-record-we-beat/` (the page and the row files themselves are not shipped; the record and the listed rows are in
`the-record-we-beat/README.md`). Work files and folders named there (`self_break/`, `runs/`, `tests/`,
`panel/attempt1-novelty-stopped-at-run-end`, `panel/work-*/` and the skeptics' `mine/`,
`author_run/` and `fetched/`) are not shipped. Dated run and folder names ("run", "folder" or "run folder" followed
by a date and time, or by a four-digit time alone) name runs of the contributor's workspace, which are not shipped
either.

This is the bank's full success criterion at the listed cell `(n=24, k=4, c=10)`: exact `d = 13`, strictly above the
cell's `d_lower = 12` and at most its `d_upper = 19`.

The code comes from the extended one-point algebraic-geometry code `E_11` of the Hermitian curve `y^3 + y = x^4`
over GF(9): the 9 monomials `x^i y^j` (`j <= 2`, pole order `3i + 4j <= 11`) evaluated at the 27 affine points, plus a
28th coordinate holding the `x y^2` coefficient (the point at infinity). It is a `[28, 9, 17]_9` code. Deleting the
four affine points `(x, y) = (0, 0), (1, 2), (2, 2), (3, 6)` (in the encoding `a + 3b` of GF(9)) gives a
`[24, 9, >= 13]_9` code, and multiplying 12 of its columns by `w` (an element of norm `-1`) raises its Hermitian hull
from 1 to 5 without changing any weight. That gives `[[24, 9 - 5, 13; 24 - 9 - 5]]_3 = [[24, 4, 13; 10]]_3`. Entanglement is needed because the GF(9) code
behind `S`, the `[24,15]` Hermitian dual of the `[24,9]_9` code, is not Hermitian self-orthogonal: its hull has
dimension 5, so rank(S J S^T) = 2(15 - 5) = 20 and the code uses 10 shared pairs; without entanglement the table's best at `n = 24, k = 4` is 8-10. The object
holds the GF(9) generator `G9`, its Hermitian dual `D9`, and the stabilizer matrix `S = phi(D9)` over GF(3).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 2 seconds on one core (2.2 s measured, see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It computes `s`, `c` and `k` from `S`, checks the object's GF(9) description against `S`, examines every one of the
2,704,156 sets of 12 positions with an exact GF(3) rank test (none supports a vector of `span(S)^perp` outside the
isotropic part, so `d >= 13`), and checks an explicit weight-13 vector of `span(S)^perp` outside `span(S)` (so
`d <= 13`). It then proves `d >= 13` a second way without any codeword search (`punct_check.py`: `span(S)^perp` is
exactly `phi(E')` for `E'` = `E_11` with the four points above deleted and the given columns scaled; a nonzero
function with at most 11 poles at infinity has at most 11 affine zeros, so `d(E_11) >= 17`, and each deleted
coordinate lowers a weight by at most one), with a weight-13 codeword of `E'`. `RUN_IT_YOURSELF.md` has the expected
output and more independent exact checks (a GF(9) information-set test over all 2,704,156 sets of 12 columns, a
Brouwer-Zimmermann distance computation, and a full enumeration of all 3^18 - 1 vectors of `span(S)^perp`).

## Compared to

| table | cell | listed | our code | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of entanglement-assisted qutrit quantum codes (`Last change: 10.07.2025`) | `(n=24, k=4, c=10)` | `[[24,4,12-19;10]]_3` ("subcode of [[24,6,12;10]] from arXiv:2207.05647") | `[[24, 4, 13; 10]]_3` | https://eaqecc.codetables.de/qutrit.php | 2026-10-25T11:22:04Z (CRITERION skeptic; the same page at 09:45:36Z before the claim and at 11:05:08Z for the NOVELTY skeptic) |

Details, HTTP headers, page hash and the listed `(24, 4)` row are in `the-record-we-beat/README.md`.

The closure of the table under its own propagation rules (teleportation cells excluded, as the page does), of the
codes named in this repository and its open pull requests, of this workspace's other codes and of the literature the
NOVELTY skeptic found gives at most 12 at `(24, 4, 10)` (`panel/novelty.md`). The row first lists `d_lower = 13` at
`c = 11`.

## Disclosures

- **How the panel was run.** The run ended at 10:43:58Z before its panel finished (its background skeptics were
  stopped by the headless background-wait limit). Its one unfinished NOVELTY attempt is not used. The supervising
  session then ran the run's three skeptics (REPRODUCE, NOVELTY, CRITERION) as fresh subagents, each given only its
  own copy of the claim folder, one after another. So the panel was run after the
  run, by the supervising session, and not by the run itself (`panel/gate.md` has the times).
- **Draft PR #739 now exists.** The claim's text says no open pull request names a code of length 23, 24 or 25. Since
  11:02Z draft PR #739 (same contributor) names `[[25,5,12;8]]_3` and codes derived from it. It does not reach this
  cell: none of the page's rules raises `d`, and the NOVELTY and CRITERION skeptics each found that adding it still
  gives 12 at `(24, 4, 10)`. The claim's sentence is out of date; the criterion is judged against the live table only.
- **Teleportation cells.** The page lists `(24,3,3)` as `[[24,3,13-19;3]]` and `(24,4,4)` as `[[24,4,11-17;4]]`, both
  "using teleportation". If teleportation cells were valid sources for the page's rules, `[[24,3,13;3]]` would give 13
  at `(24,4,4)` (where the page lists 11) and so 13 at `(24,4,10)`; the CRITERION skeptic found 57 teleportation cells
  that would each give 13 here. They are not valid sources: see the next section.

## Not claimed

- Only the code `[[24, 4, 13; 10]]_3` and the cell `(24, 4, 10)` are claimed (one object per package). Codes that
  follow from it by the table's propagation rules (for example `[[25,4,13;10]]` by lengthening or `[[24,4,13;11]]` by
  adding a pair) are not claimed here.
- Optimality is not claimed: the table's upper bound at this cell is 19.
- This is not a new technique: the Hermitian construction, one-point Hermitian codes and puncturing are published.
  The classical parameters are not new either: codetables.de lists `[24,9]_9` at 13-14. What is new is a
  `[24,9,13]_9` code with Hermitian hull 5, not found in the table or the literature checked.
- Teleportation cells: the page never applies its propagation rules to such cells. Teleportation codes are stabilizer
  codes too, but the page's rules that need pure codes (increasing dimension, quantum shortening) or a full isotropic
  cover (length reduction) do not apply to them, because a teleportation code's isotropic part is Z-only. Propagating
  them anyway breaks the page's own upper bounds: quantum shortening of the listed `[[8,1,6;1]]` would give
  `[[7,2,5;1]]`, above that cell's upper bound 4; increasing dimension three times on the listed teleportation
  `[[24,1,18-23;1]]` would give `[[24,4,18;4]]`, above the upper bound 17 of `(24,4,4)`; and seeding all teleportation
  cells into the rules puts 2569 listed cells (NOVELTY skeptic's closure) or 2700 (CRITERION skeptic's) above their
  own upper bounds. So teleportation cells are not used as sources here (`panel/novelty.md`, `panel/criterion.md`).
  The panel's own wording that teleportation codes are "impure" is right for the Z-only isotropic part but should not
  be read as "not stabilizer codes".
- Literature not read in full: journal papers without an arXiv version (Cao, Li and Zhu, IEEE TIT 71 (2025); Li, Li,
  Guan and Song, IJTP 63 (2024); Liu, Li and Shi, AMC 19; Li and Zhu, "Galois hulls of arbitrary dimensions") were
  judged only through the comparison columns of arXiv:2607.02170, which list no qutrit code with `n >= 23` at
  `k = 4`; arXiv:2605.05613 and the other recent hits of the NOVELTY skeptic's arXiv queries were read as abstracts.
  The file lists of the 14 pull requests other than #739 were not fetched; their bodies were read in full and every
  code they name is in the closure (`panel/novelty.md`, section 6).
- Closest ideas that are not known codes: a hypothetical Hermitian-hull-8 equivalent of the one-point code `C_13`
  would tie at 13 here, and the k = 1 rule of PR #363 reaches 14 only through impure codes (`panel/novelty.md`,
  section 5).
- Not yet submitted to or listed by the table maintainer (`eaqecc.codetables.de`).
- Not peer reviewed. The panel files (`panel/`) and the standalone checker in `verify-it-yourself/` are shipped so
  that anyone can check the claim.

## Credits

- **Markus Grassl**, maintainer of the online EAQECC bounds tables (https://eaqecc.codetables.de/ and
  https://eaqecc.codetables.de/qutrit.php) and `codetables.de` (https://codetables.de/).
- **Gaojun Luo, Martianus Frederic Ezerman, Markus Grassl, and San Ling**, "Constructing quantum error-correcting
  codes that require a variable amount of entanglement", *Quantum Information Processing* 23, 4 (2024),
  https://doi.org/10.1007/s11128-023-04211-x (preprint https://arxiv.org/abs/2207.05647, titled "How Much Entanglement
  Does a Quantum Code Need?" on arXiv), whose Hermitian
  construction (Proposition 1) turns a GF(9) code with a given Hermitian hull into the qutrit EA code, and whose
  propagation rules the table uses; the listed cell's code comes from this paper.
- **Markus Grassl**, "Entanglement-assisted quantum communication beating the quantum Singleton bound", *Phys. Rev. A*
  103, L020601 (2021), https://doi.org/10.1103/PhysRevA.103.L020601 (preprint https://arxiv.org/abs/2007.01249): the
  source of the table's "using teleportation" cells discussed above.
- **Todd A. Brun, Igor Devetak, and Min-Hsiu Hsieh**, "Correcting quantum errors with entanglement", *Science* 314,
  436-439 (2006), https://doi.org/10.1126/science.1131563 (preprint https://arxiv.org/abs/quant-ph/0610092).
- **Carlos Galindo, Fernando Hernando, Ryutaroh Matsumoto, and Diego Ruano**, "Entanglement-assisted quantum
  error-correcting codes over arbitrary finite fields", *Quantum Information Processing* 18, 116 (2019),
  https://doi.org/10.1007/s11128-019-2234-5 (preprint https://arxiv.org/abs/1812.05312).
- **V. D. Goppa** (algebraic-geometry codes, https://en.wikipedia.org/wiki/Algebraic_geometry_code) and **Henning
  Stichtenoth**, "A note on Hermitian codes over GF(q^2)", *IEEE Transactions on Information Theory* 34 (1988)
  1345-1348, https://doi.org/10.1109/18.21267 (one-point Hermitian codes and their distance bound).
- **René Bødker Christensen, Carlos Munuera, Francisco Revson F. Pereira, and Diego Ruano**, "An Algorithmic
  Approach to Entanglement-Assisted Quantum Error-Correcting Codes from the Hermitian Curve",
  https://arxiv.org/abs/2105.02166 (one-point Hermitian EA codes and their hulls).
- **Yang Li, Martianus Frederic Ezerman, Shitao Li, San Ling, and Zhonghua Sun**, "Generalized Extended Codes with
  Applications in Entanglement-Assisted Qubit and Qutrit Codes", https://arxiv.org/abs/2607.02170 (its Table V and
  Table VII of qutrit EA codes were compared against; none reaches this cell).
- **Andries Brouwer and Karl-Heinz Zimmermann**, whose minimum-distance algorithm the bz64 distance check uses (as
  described by Hernando, Igual and Quintana-Orti, https://arxiv.org/abs/1603.06757).
- Contributor credit: Abshalom Dayan, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
