# Entanglement-assisted qutrit code `[[23, 4, 12; 9]]_3` (the table lists `[[23,4,11-18;9]]_3`)

## What

The GF(3) stabilizer matrix S in claim/object/eaqecc_23_4_12_9.json defines a non-catalytic EAQECC [[23,4,12;9]]_3 (s = 28, rank(SJS^T) = 18, exact minimum distance 12 by full enumeration of span(S)^perp), which exceeds the d_lower 11 and is within the d_upper 18 of the listed cell [[23,4,11-18;9]]_3 on https://eaqecc.codetables.de/qutrit.php as fetched 2026-10-25T13:58:02Z (sha256 37bbf731...936c), and is not obtained by the page's propagation rules applied to its non-teleportation cells.

Note: the sentence above is quoted word for word from `panel/gate.md` (`confirmed_scope`, from the CRITERION skeptic's
verdict); `claim/` in it is this package's root. The object's full SHA-256 is
`c64bdf57a5280892b8d4e085ea565c865d5584de5198baa9763cb516318f06f4`.

Path note: the panel files (including `panel/claim.sha256`, which lists the claim folder's files) and
`how-we-built-it/PREREG.md` refer to the run's claim folder. There, `claim/object/eaqecc_23_4_12_9.json` is
`object/eaqecc_23_4_12_9.json`, `CLAIM.md` is `README.md` (with `HOW_WE_FOUND_IT.md`), `REPRODUCE.md` is
`RUN_IT_YOURSELF.md`, `checkers/` is `verify-it-yourself/`, `rebuild/` is `how-we-built-it/` and `table/` is
`the-record-we-beat/` (the page itself is not shipped). Work files and folders named there (`self_break/`, `runs/`,
`tests/`, `panel/work-*/` and the skeptics' `mine/`, `author_run/`, `fetched/` and `scripts/`)
are not shipped. Dated run and folder names ("run", "folder" or "run folder" followed by a date and time, or by a
four-digit time alone) name runs of the contributor's workspace, which are not shipped either.

This is the bank's full success criterion at the listed cell `(n=23, k=4, c=9)`: exact `d = 12`, strictly above
the cell's `d_lower = 11` and at most its `d_upper = 18`.

The code comes from the extended one-point algebraic-geometry code `E_11` of the Hermitian curve `y^3 + y = x^4`
over GF(9): the 9 monomials `x^i y^j` (`j <= 2`, pole order `3i + 4j <= 11`) evaluated at the 27 affine points,
plus a 28th coordinate holding the `x y^2` coefficient (the point at infinity). It is a `[28, 9, 17]_9` code.
Deleting the five affine points at coordinates 0, 3, 11, 12, 16 (the points (0, 0), (1, 2), (3, 6), (4, 2), (5, 5) as
encoded (x, y), in the encoding `a + 3b` of GF(9)) gives a `[23, 9, >= 12]_9` code, and multiplying 12 of its columns by
`w` (an element of norm `-1`) raises its Hermitian hull from 2 to 5 without changing any weight. That gives
`[[23, 9 - 5, 12; 23 - 9 - 5]]_3 = [[23, 4, 12; 9]]_3`. Entanglement is needed because the GF(9) code behind
S, the `[23,14]` Hermitian dual of the `[23,9]_9` code, is not Hermitian self-orthogonal: its hull has dimension 5, so
rank(S J S^T) = 2(14 - 5) = 18 and the code uses 9 shared pairs;
without entanglement the table's best at `n = 23, k = 4` is 7-9. The object holds the GF(9) generator `G9`, its
Hermitian dual `D9`, and the stabilizer matrix `S = phi(D9)` over GF(3).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 2 seconds on one core (1.5 s measured, see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It computes `s`, `c` and `k` from `S`, checks the object's GF(9) description against `S`, examines every one of
the 1,352,078 sets of 11 positions with an exact GF(3) rank test (none supports a vector of `span(S)^perp` outside
the isotropic part, so `d >= 12`), and checks an explicit weight-12 vector of `span(S)^perp` outside `span(S)` (so
`d <= 12`). It then proves `d >= 12` a second way without any codeword search (`punct_check.py`: `span(S)^perp` is
exactly `phi(E')` for `E'` = `E_11` with the five points above deleted and the given columns scaled; a nonzero
function with at most 11 poles at infinity has at most 11 affine zeros, so `d(E_11) >= 17`, and each deleted
coordinate lowers a weight by at most one), with a weight-12 codeword of `E'`. `RUN_IT_YOURSELF.md` has the expected
output and more independent exact checks (a GF(9) information-set test over all 1,352,078 sets of 12 columns, a
Brouwer-Zimmermann distance computation, and a full enumeration of all 3^18 - 1 vectors of `span(S)^perp`).

## Compared to

| table | cell | listed | our code | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of entanglement-assisted qutrit quantum codes (`Last change: 10.07.2025`) | `(n=23, k=4, c=9)` | `[[23,4,11-18;9]]_3` ("lengthening of [[19,4,11;9]] quantum shortening of [[20,3,12;9]] from arXiv:2207.05647") | `[[23, 4, 12; 9]]_3` | https://eaqecc.codetables.de/qutrit.php | 2026-10-25T13:58:02Z (CRITERION skeptic; the same page, byte for byte, at 09:53:51Z before the claim and at 11:27:14Z for the NOVELTY skeptic) |

Details, HTTP headers, page hash and the listed `(23, 4)` row are in `the-record-we-beat/README.md`.

The closure of the table under its own propagation rules (teleportation cells excluded, as the page does), of the
codes named in this repository and its open pull requests, of this workspace's other codes and of the literature the
NOVELTY skeptic found gives at most 11 at `(23, 4, 9)` (`panel/novelty.md`). The row first lists
`d_lower = 12` at `c = 10`.

## Disclosures

- **How the panel was run.** The run ended before its panel ran. The supervising session then ran the run's three
  skeptics (REPRODUCE, NOVELTY, CRITERION) as fresh subagents, each given only its own copy of the claim folder, one
  after another. So the panel was run after the run, by the supervising session, and not
  by the run itself. The CRITERION skeptic was held back between 11:50Z and 13:58Z by a usage pause and then run
  unchanged (`panel/gate.md` has the times).
- **Teleportation cells.** The page lists `(23,3,3)` as `[[23,3,12-18;3]]` and `(23,4,4)` as `[[23,4,10-16;4]]`, both
  "using teleportation". The only route to 12 at `(23,4,9)` that the CRITERION skeptic found starts from the
  teleportation cell `(23,3,3)` and applies "increasing dimension"; it is not valid (see "Not claimed"). If
  teleportation cells were valid sources for the page's rules, `[[23,3,12;3]]` would give 12 at `(23,4,4)` (where the
  page lists 10) and so 12 here. There is a second such route: the teleportation cell `(24,3,3)` (`[[24,3,13;3]]`) by
  quantum shortening would give `[[23,4,12;3]]` and so 12 here; it is excluded for the same reason.
- **Order relative to draft PR #758.** The NOVELTY skeptic ran at 11:27Z, before draft PR #758 (`[[24,4,13;10]]_3`,
  same contributor, same construction family) was filed at 13:06Z, so the panel did not see it. Checked on
  2026-10-25, after the panel and before filing: none of the page's propagation rules lowers `c`, so #758's code (`c = 10`) gives
  nothing at `c <= 9`, and the closure of the listed non-teleportation cells together with the codes of all 17 pull
  requests for this target (#758 included) still gives 11 at `(23,4,9)`. The only steps that lower `c` are the page's
  catalytic note, which the page excludes (see "Not claimed"), and Theorem 18 of arXiv:2207.05647, which adds a
  position and guarantees no distance. #758 deletes a different point set ((0,0), (1,2), (2,2), (3,6)), so this code is
  not a puncturing of it.

## Not claimed

- Only the code `[[23, 4, 12; 9]]_3` and the cell `(23, 4, 9)` are claimed (one object per package). Codes that
  follow from it by the table's propagation rules (for example `[[24,4,12;9]]` by lengthening or `[[23,3,12;9]]` by
  subcode) are not claimed here.
- Optimality is not claimed: the table's upper bound at this cell is 18.
- Catalytic codes: the page excludes them. If its catalytic note were applied, the listed `[[24,6,12;10]]` would
  already give 12 at `(23,4,9)` (catalytic step, length reduction, catalytic step). The claim is for the non-catalytic
  setting, which is the page's and the bank's.
- This is not a new technique: the Hermitian construction, one-point Hermitian codes and puncturing are published.
  The classical parameters are not new either: codetables.de lists `[23,9]_9` at 12-13. What is new is a
  `[23,9,12]_9` code with Hermitian hull 5, not found in the table or the literature checked.
- Teleportation cells: the page never applies its propagation rules to such cells. Teleportation codes are stabilizer
  codes too, but the page's rules that need pure codes (increasing dimension, quantum shortening) do not apply to
  them, because a teleportation code's isotropic part is Z-only. Propagating
  them anyway breaks the page's own upper bounds: increasing dimension of the listed teleportation `[[8,1,6;1]]`
  would give `[[8,3,6;3]]`, above the upper bound 5 of `(8,3,3)`; increasing dimension alone applied to the page's
  teleportation cells puts 626 listed cells above their own upper bounds, and all six rules together put 2700 there
  (CRITERION skeptic; the NOVELTY skeptic also found 2700). So teleportation cells are not used as sources here
  (`panel/novelty.md`, `panel/criterion.md`). The CRITERION skeptic's conclusion that the teleportation route is
  not valid propagation rests on the page's bounds; it did not settle from first principles whether
  increasing dimension could hold for the one cell `(23,3,3)`.
- Literature not read in full: the NOVELTY skeptic read the recent arXiv papers it found (140 from the last 24
  months) as abstracts only, and did not search journal papers without an arXiv version. It fetched the file list of
  PR #739 only; for the other pull requests it used their bodies, and every exact code in them is in the closure
  (`panel/novelty.md`, section 5).
- Closest known codes: the listed `(23,4,10)` value is 12 (`d_lower`), so 12 is reached at `c = 10` but not at
  `c = 9`; PR #739's `[[25,5,12;8]]` reaches `[[23,4,12;10]]`, also `c = 10`.
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
