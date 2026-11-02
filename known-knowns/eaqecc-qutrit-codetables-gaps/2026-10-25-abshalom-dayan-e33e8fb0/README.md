# Entanglement-assisted qutrit code `[[25, 5, 12; 8]]_3` (the table lists `[[25,5,11-18;8]]_3`)

## What

The 28 x 50 GF(3) matrix S in claim/object/eaqecc_25_5_12_8.json (sha256 e33e8fb04dc70d4d703e033310b6efafb1825109a93d649ecef183451ee09ec3), with 28 independent rows and rank(S J S^T) = 16, is a non-catalytic [[25,5,12;8]]_3 EAQECC whose exact distance 12 (no nonzero vector of span(S)^perp of symplectic weight <= 11 over all 4457400 11-position sets, and explicit weight-12 vectors of span(S)^perp outside span(S)) is strictly above the d_lower 11 and at most the d_upper 18 of the listed cell [[25,5,11-18;8]]_3 of https://eaqecc.codetables.de/qutrit.php as fetched at 2026-10-25T10:14:24Z (HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c) and is not reached at (25,5,8) by the page's six propagation rules applied to its listed non-teleportation cells (which give 11).

Note: the sentence above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`); `claim/` in it is this package's root.
The object's full SHA-256 is `e33e8fb04dc70d4d703e033310b6efafb1825109a93d649ecef183451ee09ec3`.

Path note: the panel files and `how-we-built-it/PREREG.md` refer to the run's claim folder. There,
`claim/object/eaqecc_25_5_12_8.json` is `object/eaqecc_25_5_12_8.json`, `CLAIM.md` is `README.md`, `REPRODUCE.md` is
`RUN_IT_YOURSELF.md`, `checkers/` is `verify-it-yourself/` and `rebuild/` is `how-we-built-it/`. Work files and
folders named there (`panel/claim.sha256`, `self_break/`, `attempts/`, `runs/`, `tests/`, and the skeptics' `mine/`,
`run/`, `fetched/` and `scripts/`) are not shipped. Dated run and folder names ("run", "folder" or "run folder"
followed by a date and time, or by a four-digit time alone) name runs of the contributor's workspace, which are not
shipped either.

This is the bank's full success criterion at the listed cell `(n=25, k=5, c=8)`: exact `d = 12`, strictly above the
cell's `d_lower = 11` and at most its `d_upper = 18`.

The code comes from the extended one-point algebraic-geometry code `E_13` of the Hermitian curve `y^3 + y = x^4`
over GF(9): the 11 monomials `x^i y^j` (`j <= 2`, pole order `3i + 4j <= 13`) evaluated at the 27 affine points,
plus a 28th coordinate holding the `x^3 y` coefficient (the point at infinity). It is a `[28, 11, 15]_9` code.
Deleting the three affine points of the line `x = 0` gives a `[25, 11, >= 12]_9` code, and multiplying 13 of its
columns by `w` (an element of norm `-1`) raises its Hermitian hull from 4 to 6 without changing any weight. That
gives `[[25, 11 - 6, 12; 25 - 11 - 6]]_3 = [[25, 5, 12; 8]]_3`. The object holds the GF(9) generator `G9`, its
Hermitian dual `D9`, and the stabilizer matrix `S = phi(D9)` over GF(3).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 6 seconds on one core (6.30 s measured, see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It computes `s`, `c` and `k` from `S`, checks the object's GF(9) description against `S`, examines every one of
the 4,457,400 sets of 11 positions with an exact GF(3) rank test (none supports a vector of `span(S)^perp` outside
the isotropic part, so `d >= 12`), and checks an explicit weight-12 vector of `span(S)^perp` outside `span(S)` (so
`d <= 12`). It then proves `d >= 12` a second way without any codeword search (`punct_check.py`: `span(S)^perp` is
exactly `phi(E')` for `E'` = `E_13` with the three points of `x = 0` deleted and the given columns scaled; a nonzero
function with at most 13 poles at infinity has at most 13 affine zeros, so `d(E_13) >= 15`, and each deleted
coordinate lowers a weight by at most one), with a weight-12 codeword of `E'`. `RUN_IT_YOURSELF.md` has the expected
output and more independent exact checks (a GF(9) information-set test over all 4,457,400 sets of 14 columns and a
Brouwer-Zimmermann distance computation).

## Compared to

| table | cell | listed | our code | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of entanglement-assisted qutrit quantum codes (`Last change: 10.07.2025`) | `(n=25, k=5, c=8)` | `[[25,5,11-18;8]]_3` ("lengthening of [[24,5,11;8]] subcode of [[24,6,11;8]] from arXiv:2207.05647") | `[[25, 5, 12; 8]]_3` | https://eaqecc.codetables.de/qutrit.php | 2026-10-25T10:14:24Z (CRITERION skeptic; the same page at 08:57:05Z, 09:17:02Z and 09:35:47Z) |

Details, HTTP headers, page hash and the listed `(25, 5)` row are in `the-record-we-beat/README.md`.

The closure of the table under its own propagation rules (teleportation cells excluded, as the page does), of the
codes named in this repository and its open pull requests, of this workspace's other codes and of the literature the
NOVELTY skeptic found gives at most 11 at `(25, 5, 8)` (`panel/novelty.md`). The row first lists `d_lower = 12` at
`c = 10`.

## Not claimed

- Only the code `[[25, 5, 12; 8]]_3` and the cell `(25, 5, 8)` are claimed (one object per package). Codes that
  follow from it by the table's propagation rules (for example `[[26,5,12;8]]` by lengthening or `[[25,4,12;8]]` by
  subcode) are not claimed here.
- Optimality is not claimed: the table's upper bound at this cell is 18.
- This is not a new technique: the Hermitian construction, one-point Hermitian codes and puncturing are published.
  The classical parameters are not new either: codetables.de lists `[25,11]_9` at 12-13. What is new is a
  `[25,11,12]_9` code with Hermitian hull 6, not found in the table or the literature checked.
- Teleportation cells: the page lists `(25,4,4)` as `[[25,4,12-18;4]]` and `(25,5,5)` as `[[25,5,10-16;5]]`, both
  "using teleportation", and never applies its propagation rules to such cells (increasing dimension of
  `[[25,4,12;4]]` would give 12 at `(25,5,5)`, where the page lists 10). Teleportation codes are stabilizer codes too,
  but the length-reduction rule needs the isotropic part to cover the deleted coordinate in both X and Z, and a
  teleportation code's isotropic part is Z-only, so the rule does not hold for them: applied anyway, it would turn
  the listed `[[8,1,6-7;1]]` into `[[5,1,6;4]]`, which is impossible since d <= n, and it would put 144 listed
  cells above their own upper bounds. So teleportation cells are not used as sources here (the closure is in
  `panel/novelty.md`).
- Literature the NOVELTY skeptic could not read in full: the NOVELTY skeptic read arXiv:2207.05647 (the table's source), arXiv:2607.02170 (Table V, qutrit
  codes up to length 25), arXiv:2105.02166, arXiv:2501.04921 (https://arxiv.org/abs/2501.04921), arXiv:2206.09782 (https://arxiv.org/abs/2206.09782) and the codetables.de entries for
  `[25,11]_9`, `[25,12]_9` and `[25,8]_3`; three journal papers (Cao, Li and Zhu, IEEE TIT 2025; Li, Li, Guan and
  Song, IJTP 2024; arXiv:2512.17128 beyond its summary) were judged from the codes arXiv:2607.02170 cites from them,
  and journal papers without an arXiv version may be missed. The GitHub API refused the NOVELTY skeptic's requests
  for the pull requests' file lists (rate limit); the codes named in those files had been extracted by an earlier
  skeptic about an hour before and were included in the closure.
- Not yet submitted to or listed by the table maintainer (`eaqecc.codetables.de`).
- Not peer reviewed. The panel files (`panel/`) and the standalone checker in `verify-it-yourself/` are shipped so
  that anyone can check the claim.

Corrections to the panel text:
- `panel/novelty.md` says teleportation codes are "not stabilizer codes", and `panel/criterion.md` that "a
  teleportation protocol has no stabilizer matrix with c = k". They are stabilizer codes; the reason the page's propagation rules are not applied to them is the one given above (the length-reduction
  rule needs the isotropic part to cover the deleted coordinate in both X and Z, and a teleportation code's isotropic
  part is Z-only).

## Credits

- **Markus Grassl**, maintainer of the online EAQECC bounds tables (https://eaqecc.codetables.de/ and
  https://eaqecc.codetables.de/qutrit.php) and `codetables.de` (https://codetables.de/).
- **Gaojun Luo, Martianus Frederic Ezerman, Markus Grassl, and San Ling**, "Constructing quantum error-correcting
  codes that require a variable amount of entanglement", *Quantum Information Processing* 23, 4 (2024),
  https://doi.org/10.1007/s11128-023-04211-x (preprint https://arxiv.org/abs/2207.05647), whose Hermitian
  construction (Proposition 1) turns a GF(9) code with a given Hermitian hull into the qutrit EA code, and whose
  propagation rules the table uses; the listed cell's code comes from this paper.
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
  Applications in Entanglement-Assisted Qubit and Qutrit Codes", https://arxiv.org/abs/2607.02170 (its Table V of
  qutrit EA codes was compared against; none reaches this cell).
- **Andries Brouwer and Karl-Heinz Zimmermann**, whose minimum-distance algorithm the bz64 distance check uses (as
  described by Hernando, Igual and Quintana-Orti, https://arxiv.org/abs/1603.06757).
- Contributor credit: Abshalom Dayan, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
