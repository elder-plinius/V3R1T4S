# Linear code `[29, 19, 8]` over GF(9) (table: lower bound `7`)

## What

The 19 x 29 matrix in object/code_q9_n29_k19_d8.json (sha256 912c80c8...f9e7), read over GF(9) = GF(3)[w]/(w^2 - w - 1), has rank 19 and exact minimum distance 8 (A_8 = 12456), which is strictly above the lower bound 7 and within the upper bound 9 of the codetables.de [29,19] GF(9) cell as fetched at 2026-10-27T02:09:43Z, and it is not a LinCodeEvolve (binary) code nor derived from one.

Note: the paragraph above is quoted word for word from `panel/gate.md` (the CRITERION skeptic's `confirmed_scope`).
Path note: the panel files name the panel's claim/ folder. In this package claim/object/code_q9_n29_k19_d8.json is
object/code_q9_n29_k19_d8.json (same sha256); claim/checkers/m3_mindist.c is verify-it-yourself/m3_mindist.c;
claim/checkers/hdep.c, dualenum.c and macwilliams.py, and claim/rebuild/ (build_code.py, hermitian.py, gf9lib.py), are in
how-we-built-it/ (all byte-identical); claim/REPRODUCE.md is adapted as RUN_IT_YOURSELF.md (its live-cell step is in
the-record-we-beat/README.md) and claim/CLAIM.md's claim is this README.
Not shipped: claim/checkers/witness_check.py and json_to_code.py (verify-it-yourself/check_code.py re-checks the witness
and RUN_IT_YOURSELF.md has the conversion one-liner), claim/table/bklc_q9_n29_k19.html (third-party page; URL, fetch
times, HTTP status and sha256 are in the-record-we-beat/README.md), and the skeptics' working folders (mine/, author/,
fetched/, scripts/, run_author/, live/).
Also see "Named but not shipped" in RUN_IT_YOURSELF.md.

The object's full SHA-256 is `912c80c8ee946bc6021522350a436fb9510b39e1565175a0a0fc380d0216f9e7`. The cell was read
again just before packaging, at 2026-10-27T02:21:50Z: same page hash, same bounds (`the-record-we-beat/README.md`).

The code is a Construction X on the Hermitian curve `y^3 + y = x^4` over GF(9). Rows 1 to 17 are the one-point code
`C(D,19P)` on the 27 affine points (a `[27,17,8]` code), followed by two zero columns. Row 18 is the function
`x^4 y^2` (pole order 20) with tail `(0, 1)`, and row 19 is `x^7` (pole order 21) with tail `(1, 1)`. On the affine
part all 19 rows span `C(D,21P)`, a `[27,19,6]` code. The textbook Construction X bound with a 2-column tail gives
only `min(8, 6 + 1) = 7`; the true distance 8 comes from the specific tail, found by an exact search over 2-column tails
for this nested pair, which stops at the first valid tail (the object's construction field says "exhaustive search over
all 2-column tails"; read it the same way), and rests on exact computation (four exact methods by the author, three of
them shipped: m3_mindist, hdep, and dualenum with MacWilliams; the panel files in `panel/` record the skeptics' own
computations).

This is a GF(9) result. The bank target is named `codetables-binary-linear`, but its success criterion is stated for
GF(q); this code is not a binary code.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements:** `python3` (standard library only) and a C compiler (`cc`).
- **Rough laptop time:** about 1 second on one core (0.95 s measured, see `verify-it-yourself/RECEIPTS.md`).
- **Expected last line:** `PASS`

It checks the rank, then examines every set of at most 7 of the 29 coordinates (all 1,560,780 7-subsets) exactly
over GF(9) and finds no nonzero codeword supported inside any of them, then prints a codeword of weight 8 and checks
that it lies in the row space. Expected output, the rebuild and a second independent check (the full weight
distribution from all 9^10 dual codewords) are in `RUN_IT_YOURSELF.md`.

## Compared to

| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Grassl, Bounds on the minimum distance of linear codes (codetables.de) | `q=9, n=29, k=19` | lower bound 7, upper bound 9 (`[29,19,7]`, a subcode of a shortened `[37,28,7]` code from Xing and Ling, last modified 2001-12-17) | `[29,19,8]` (`d = 8`) | https://codetables.de/BKLC/BKLC.php?q=9&n=29&k=19 | 2026-10-27T02:21:50Z |

Details, HTTP headers, page hash and the neighboring cells are in `the-record-we-beat/README.md`.

## Not claimed

- Optimality is not claimed; the table's upper bound is 9.
- Only cell `(q, n, k) = (9, 29, 19)` is claimed (one cell per package). Codes derived from it only tie the table and
  are not claimed: shortened `[28,18,8]` (table 8-9), punctured `[28,19,7]` (table 7-9), subcode `[29,18,8]` (table
  8-10), `[30,19,8]` by a zero column (table 8-10).
- No quantum or entanglement-assisted code is claimed here.
- Not yet submitted to or listed by the table maintainer (codetables.de).
- Not peer reviewed. The panel files (`panel/`) and the standalone checker in `verify-it-yourself/` are shipped so
  that anyone can check the claim.
- The panel's NOVELTY skeptic could not read three sources (arXiv's export API returned 429 and 503, MinT had no
  connection, Yves Edel's GF(9) tables gave a TLS name mismatch); it did not retry. See `panel/novelty.md`.
  The arXiv API was read again on 2026-10-27 (20:29:24Z): no [29,19,>=8] code over GF(9) among the 60 newest
  GF(9)/Hermitian linear-code abstracts. MinT and Yves Edel's GF(9) tables still could not be read on 2026-10-27 (20:35Z to 20:40Z): MinT refused connections on ports 80 and 443, and Edel's pages gave a TLS name mismatch on mathi.uni-heidelberg.de and HTTP 404 on www.mathi.uni-heidelberg.de. Neither is a bar in this target's criterion; the live codetables.de cell is.
- The docstring of how-we-built-it/hermitian.py says the curve is the one "codetables.de uses for its [23..28, 9..14]
  codes"; that statement is unverified (the file is byte-identical to the panel's copy and was left unedited).

## Credits

- **Markus Grassl**, maintainer of the code tables at https://codetables.de/, whose cell this improves; the upper
  bound there comes from **Andries E. Brouwer**'s tables, and the previous entry from **Chaoping Xing and San Ling**.
- **N. J. A. Sloane, S. M. Reddy and C.-L. Chen**, "New binary codes", IEEE Transactions on Information Theory 18
  (1972), 503-510, https://doi.org/10.1109/TIT.1972.1054833: Construction X.
- **V. D. Goppa**, "Algebraico-geometric codes", Math. USSR-Izv. 21 (1983) 75-91,
  https://doi.org/10.1070/IM1983v021n01ABEH001641 (algebraic-geometry codes), and **Henning Stichtenoth**, "A note on
  Hermitian codes over GF(q^2)", IEEE Trans. Inform. Theory 34 (1988) 1345-1348, https://doi.org/10.1109/18.21267
  (Hermitian codes), whose one-point codes on the Hermitian curve are the nested codes used here.
- **F. J. MacWilliams**, "A theorem on the distribution of weights in a systematic code", Bell Syst. Tech. J. 42 (1963)
  79-94, https://doi.org/10.1002/j.1538-7305.1963.tb04003.x: the MacWilliams identities used in the dual-side check.
- **Chaoping Xing and San Ling**, the two papers the cell page cites for the previous entry:
  https://doi.org/10.1109/18.868488 and https://doi.org/10.1109/18.850687.
- **Andries E. Brouwer**'s tables of bounds, https://aeb.win.tue.nl/ (source of the table's upper bound).
- LinCodeEvolve (arXiv:2609.37056, https://arxiv.org/abs/2609.37056): compared against; its seven codes are binary.
- Contributor credit: Abshalom Dayan, using the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
