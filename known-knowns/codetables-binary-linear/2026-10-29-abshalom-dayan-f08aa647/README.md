# Linear code `[31, 17, 11]` over GF(9) (table: lower bound `10`)

## What

The 17 x 31 matrix in object/code_q9_n31_k17_d11.json, read over GF(9) = GF(3)[w]/(w^2 - w - 1), has rank 17 and exact minimum distance 11 (three agreeing exact methods plus an in-span weight-11 witness), which is strictly above the lower bound 10 and within the upper bound 13 of the codetables.de cell (q,n,k) = (9,31,17) as fetched at 2026-10-29T01:24:04Z.

Note: the paragraph above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`).
Path note: the panel files name the panel's claim/ folder. In this package claim/object/code_q9_n31_k17_d11.json is
object/code_q9_n31_k17_d11.json (same sha256); claim/checkers/m3_mindist.c is verify-it-yourself/m3_mindist.c;
claim/checkers/hdep.c and claim/rebuild/ (build_code.py, build_tail.py, to_json.py, hermitian.py, gf9lib.py) are in
how-we-built-it/ (all byte-identical); claim/REPRODUCE.md is adapted as RUN_IT_YOURSELF.md (its live-cell step is in
the-record-we-beat/README.md) and claim/CLAIM.md's claim is this README.
Not shipped: claim/checkers/witness_check.py and json_to_code.py (verify-it-yourself/check_code.py re-checks the witness
and RUN_IT_YOURSELF.md has the conversion one-liner), claim/table/bklc_q9_n31_k17.html and its .headers, .result and
.time files (third-party page and fetch metadata; URL, fetch times, HTTP status and sha256 are in
the-record-we-beat/README.md), claim/table/RECORD.md (the scout's record of that page; its content is in
the-record-we-beat/README.md), any Python byte-code caches, and the skeptics' working folders (mine/, live/, fetched/, scripts/, author_run/).
Also see "Named but not shipped" in RUN_IT_YOURSELF.md.

The object's full SHA-256 is `f08aa6475f164ffa1ed1f41f5c63eb0f5516b74c34c1b198da8c83ae1a7da5dd`. The cell was read
again just before packaging, at 2026-10-29T01:36:33Z: same page hash, same bounds (`the-record-we-beat/README.md`).

The code is a Construction X on the Hermitian curve `y^3 + y = x^4` over GF(9). Rows 1 to 14 are the one-point code
`C(D,16P)` on the 27 affine points (a `[27,14,11]` code), followed by four zero columns. Rows 15 to 17 are the
functions of pole order 17 to 19 (`x^3 y^2`, `x^6`, `x^5 y`); their four tail entries are the columns (0,0,1),
(0,1,0), (0,1,1), (1,0,3), read as points of PG(2,9) in the a + 3b encoding. On the affine part all 17 rows span
`C(D,19P)`, a `[27,17,8]` code. The textbook Construction X bound with a Reed-Solomon (MDS) tail of length 4 gives
only `min(11, 8 + 2) = 10`; the distance 11 comes from this specific tail, found by an exact search over 4-column
tails for this nested pair (it stops at the first valid tail), and rests on exact computation (two exact methods by
the author, both shipped: m3_mindist and hdep; the panel files in `panel/` record the REPRODUCE and CRITERION skeptics'
own computations). Its number of weight-11 codewords is A_11 = 48,648 (6,081 supports, counted by both of the REPRODUCE skeptic's methods, times 8 nonzero scalars).

This is a GF(9) result. The bank target is named `codetables-binary-linear`, but its success criterion is stated for
GF(q); this code is not a binary code.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 17 seconds on one core (17.30 s measured, see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It checks the rank, then examines every set of at most 10 of the 31 coordinates (all 44,352,165 10-subsets) exactly
over GF(9) and finds no nonzero codeword supported inside any of them, then prints a codeword of weight 11 and checks
that it lies in the row space. Expected output, the rebuild and a second independent check (the smallest set of
dependent parity-check columns) are in `RUN_IT_YOURSELF.md`.

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of linear codes (codetables.de) | `q=9, n=31, k=17` | lower bound 10, upper bound 13 (`[31,17,10]`, a shortened puncture of a `[37,21,12]` subcode of a punctured Reed-Solomon code over GF(81), last modified 2001-12-17) | `[31,17,11]` (`d = 11`) | https://codetables.de/BKLC/BKLC.php?q=9&n=31&k=17 | 2026-10-29T01:36:33Z |

Details, HTTP headers, page hash and the neighboring cells are in `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; the table's upper bound is 13.
- Only cell `(q, n, k) = (9, 31, 17)` is claimed (one cell per package). Codes derived from it only tie the table:
  shortened `[30,16,11]` (table 11-13), punctured `[30,17,10]` (table 10-12), subcode `[31,16,11]` (table 11-14),
  `[32,17,11]` by a zero column (table 11-14).
- No quantum or entanglement-assisted code is claimed here.
- Not yet submitted to or listed by the table maintainer (codetables.de).
- Not peer reviewed. The panel files (`panel/`) and the standalone checker in `verify-it-yourself/` are shipped so
  that anyone can check the claim.
- The panel's NOVELTY skeptic read abstracts and PR titles and bodies, not full texts or PR file contents, and did not
  query MinT; see `panel/novelty.md`. The live codetables.de cell is the bar in this target's criterion.
- The docstring of how-we-built-it/hermitian.py says the curve is the one "codetables.de uses for its [23..28, 9..14]
  codes"; that statement is unverified (the file is byte-identical to the panel's copy and was left unedited).

## Credits

- **Markus Grassl**, maintainer of the code tables at https://codetables.de/, whose cell this improves; the upper
  bound there comes from **Andries E. Brouwer**'s tables (https://aeb.win.tue.nl/) via a result of **Stefano Marcugini, Alfredo Milani and Fernanda Pambianco** (https://doi.org/10.1109/18.992802), and the [37,21,12] code behind the lower bound, which
  codetables.de attributes (Lb(37,21) = 12, "XL") to **Chaoping Xing and San Ling**
  (https://doi.org/10.1109/18.868488, https://doi.org/10.1109/18.850687).
- **N. J. A. Sloane, S. M. Reddy and C.-L. Chen**, "New binary codes", IEEE Transactions on Information Theory 18
  (1972), 503-510, https://doi.org/10.1109/TIT.1972.1054833: Construction X.
- **V. D. Goppa**, "Algebraico-geometric codes", Math. USSR-Izv. 21 (1983) 75-91,
  https://doi.org/10.1070/IM1983v021n01ABEH001641 (algebraic-geometry codes), and **Henning Stichtenoth**, "A note on
  Hermitian codes over GF(q^2)", IEEE Trans. Inform. Theory 34 (1988) 1345-1348, https://doi.org/10.1109/18.21267
  (Hermitian codes), whose one-point codes on the Hermitian curve are the nested codes used here.
- LinCodeEvolve (Amal Seddas, Vladyslav Shashkov, Maryna Viazovska, Emmanuel Abbe; arXiv:2609.37056, https://arxiv.org/abs/2609.37056): compared against; its seven codes are binary.
- Contributor credit: Abshalom Dayan, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
