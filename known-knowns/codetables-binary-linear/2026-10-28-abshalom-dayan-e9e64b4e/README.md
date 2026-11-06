# Linear code `[32, 19, 10]` over GF(9) (table: lower bound `9`)

## What

The 19 x 32 matrix G in object/code_q9_n32_k19_d10.json (sha256 e9e64b4eef94a2fc783bf8e027b849d0d931a3641607aa98121561a77cb77965), read in the stated GF(9) = GF(3)[w]/(w^2 - w - 1) encoding, has rank 19 and generates a linear [32,19,10] code over GF(9), whose minimum distance 10 is strictly above the lower bound 9 and at most the upper bound 12 of the codetables.de cell (q,n,k) = (9,32,19) as fetched at 2026-10-28T01:39:29Z.

Note: the paragraph above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`).
Path note: the panel files name the panel's claim/ folder. In this package claim/object/code_q9_n32_k19_d10.json is
object/code_q9_n32_k19_d10.json (same sha256); claim/checkers/m3_mindist.c is verify-it-yourself/m3_mindist.c;
claim/checkers/hdep.c and claim/rebuild/ (build_code.py, build_tail.py, to_json.py, hermitian.py, gf9lib.py) are in
how-we-built-it/ (all byte-identical); claim/REPRODUCE.md is adapted as RUN_IT_YOURSELF.md (its live-cell step is in
the-record-we-beat/README.md) and claim/CLAIM.md's claim is this README.
Not shipped: claim/checkers/witness_check.py and json_to_code.py (verify-it-yourself/check_code.py re-checks the witness
and RUN_IT_YOURSELF.md has the conversion one-liner), claim/table/bklc_q9_n32_k19.html (third-party page; URL, fetch
times, HTTP status and sha256 are in the-record-we-beat/README.md), claim/table/RECORD.md (the scout's record of that page, named in
panel/reproduce.md; its content is in the-record-we-beat/README.md), claim/rebuild/__pycache__/ (Python byte-code caches
named in panel/reproduce.md), and the skeptics' working folders (mine/).
Also see "Named but not shipped" in RUN_IT_YOURSELF.md.

The object's full SHA-256 is `e9e64b4eef94a2fc783bf8e027b849d0d931a3641607aa98121561a77cb77965`. The cell was read
again just before packaging, at 2026-10-28T01:50:06Z: same page hash, same bounds (`the-record-we-beat/README.md`).

The code is a Construction X on the Hermitian curve `y^3 + y = x^4` over GF(9). Rows 1 to 15 are the one-point code
`C(D,17P)` on the 27 affine points (a `[27,15,10]` code), followed by five zero columns. Rows 16 to 19 are the
functions of pole order 18 to 21 (`x^6`, `x^5 y`, `x^4 y^2`, `x^7`); their five tail entries are the columns
(0,0,0,1), (0,0,1,1), (0,1,0,1), (0,1,1,3), (1,6,1,2), read as points of PG(3,9) in the a + 3b encoding. On the affine
part all 19 rows span `C(D,21P)`, a `[27,19,6]` code. The textbook Construction X bound with a Reed-Solomon tail of
length 5 gives only `min(10, 6 + 2) = 8`; the distance 10 comes from this specific tail, found by an exact search
over 5-column tails for this nested pair (it stops at the first valid tail), and rests on exact computation (two exact
methods by the author, both shipped: m3_mindist and hdep; the panel files in `panel/` record the REPRODUCE and
CRITERION skeptics' own computations).
Its number of weight-10 codewords is A_10 = 35,456 (4,432 supports, the CRITERION skeptic's count of deficient 10-subsets,
times 8 nonzero scalars).

This is a GF(9) result. The bank target is named `codetables-binary-linear`, but its success criterion is stated for
GF(q); this code is not a binary code.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 8 seconds on one core (8.06 s measured, see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It checks the rank, then examines every set of at most 9 of the 32 coordinates (all 28,048,800 9-subsets) exactly
over GF(9) and finds no nonzero codeword supported inside any of them, then prints a codeword of weight 10 and checks
that it lies in the row space. Expected output, the rebuild and a second independent check (the smallest set of
dependent parity-check columns) are in `RUN_IT_YOURSELF.md`.

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of linear codes (codetables.de) | `q=9, n=32, k=19` | lower bound 9, upper bound 12 (`[32,19,9]`, a shortened subcode of a `[41,29,9]` BCH code, last modified 2001-12-17) | `[32,19,10]` (`d = 10`) | https://codetables.de/BKLC/BKLC.php?q=9&n=32&k=19 | 2026-10-28T01:50:06Z |

Details, HTTP headers, page hash and the neighboring cells are in `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; the table's upper bound is 12.
- Only cell `(q, n, k) = (9, 32, 19)` is claimed (one cell per package). Codes derived from it only tie the table or
  an earlier V3R1T4S result and are not claimed: punctured `[31,19,9]` (table 9-11), subcode `[32,18,10]` (table
  10-13), shortened `[31,18,10]` (table 9-12, already our merged #644), `[33,19,10]` by a zero column (table 10-13).
- No quantum or entanglement-assisted code is claimed here.
- Not yet submitted to or listed by the table maintainer (codetables.de).
- Not peer reviewed. The panel files (`panel/`) and the standalone checker in `verify-it-yourself/` are shipped so
  that anyone can check the claim.
- The panel's NOVELTY skeptic could not read two sources (MinT had no connection; Yves Edel's tables page gave HTTP
  404); it did not retry. See `panel/novelty.md`. Neither is a bar in this target's criterion; the live codetables.de
  cell is.
- The docstring of how-we-built-it/hermitian.py says the curve is the one "codetables.de uses for its [23..28, 9..14]
  codes"; that statement is unverified (the file is byte-identical to the panel's copy and was left unedited).

## Credits

- **Markus Grassl**, maintainer of the code tables at https://codetables.de/, whose cell this improves; the upper
  bound there comes from **Andries E. Brouwer**'s tables (https://aeb.win.tue.nl/) via a result of **Stefano
  Marcugini, Alfredo Milani and Fernanda Pambianco** (https://doi.org/10.1109/18.992802), and the [41,28,9] code behind the lower bound, which codetables.de attributes (Lb(41,28) = 9, "XL") to **Chaoping Xing and San Ling**
  (https://doi.org/10.1109/18.868488, https://doi.org/10.1109/18.850687) (codetables.de builds it as a subcode of a
  [41,29,9] BCH code).
- **N. J. A. Sloane, S. M. Reddy and C.-L. Chen**, "New binary codes", IEEE Transactions on Information Theory 18
  (1972), 503-510, https://doi.org/10.1109/TIT.1972.1054833: Construction X.
- **V. D. Goppa**, "Algebraico-geometric codes", Math. USSR-Izv. 21 (1983) 75-91,
  https://doi.org/10.1070/IM1983v021n01ABEH001641 (algebraic-geometry codes), and **Henning Stichtenoth**, "A note on
  Hermitian codes over GF(q^2)", IEEE Trans. Inform. Theory 34 (1988) 1345-1348, https://doi.org/10.1109/18.21267
  (Hermitian codes), whose one-point codes on the Hermitian curve are the nested codes used here.
- LinCodeEvolve (Amal Seddas, Vladyslav Shashkov, Maryna Viazovska, Emmanuel Abbe; arXiv:2609.37056, https://arxiv.org/abs/2609.37056): compared against; its seven codes are binary.
- Contributor credit: Abshalom Dayan, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
