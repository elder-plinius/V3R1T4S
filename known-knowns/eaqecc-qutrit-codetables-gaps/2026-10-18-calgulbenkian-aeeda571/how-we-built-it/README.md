# How the code was built

What is here, copied from the contributor's search snapshot (read-only, taken 2026-10-18T13:45:35Z):

- `PREREG.md`: the preregistration of the whole target (all three codes of this target came from this one plan). It is frozen before the codes existed and describes the plan, not this one code.
- `verify_eaqecc.py`: the contributor's own exhaustive verifier. It enumerates the whole symplectic dual (3^(2n-s) - 1 nonzero vectors). It needs the saved table page `data/qutrit.php.html`, which is a third-party page and is not copied here (fetch it from https://eaqecc.codetables.de/qutrit.php; its sha256 is in `the-record-we-beat/README.md`). Usage: `python3 verify_eaqecc.py CERT.json data/qutrit.php.html`.
- `eaqecc_33_3_23_24.receipt.json`: the verifier's receipt for this code: s = 54, 531440 vectors enumerated, 0.38 seconds on the contributor's machine.

What is NOT here: the scripts that constructed the code. `PREREG.md` names a search program `eaqecc_search.c` and the object's own `construction` field says how this code was made (punctured norm-trace), but no construction script and no log of commands is in the snapshot. So the exact commands that produced `object/eaqecc_33_3_23_24.json` are not recorded, and the contributor's search cannot be re-run from this package.

The construction in the contributor's words (unverified): Punctured Xing-Ling quadratic norm-trace code [33, 6, 23]_9 over GF(9), with column scaling for Hermitian hull h = 3. The 0/1/2 matrix is the GF(3) image of that code under the Hermitian-hull reduction in `PREREG.md`, section 2.

## Rebuild from recovered data (added 2026-11-03)

Added after review: `rebuild_eaqecc_33_3_23_24.py` (Python 3 standard library only) and its real output `rebuild_output.txt`. The description it uses was recovered from the shipped object, not taken from the contributor:

- The GF(3) symplectic dual of the shipped generators is a GF(9)-linear code under c = x + i z (i^2 = -1). That GF(9) code D is a [33,6,23]_9 code with Hermitian hull of dimension 3 (minimum weight and hull computed over all 9^6 words).
- Up to a column scaling, D is the evaluation of all six quadratic monomials in three variables (all conics) at 33 points of PG(2,9). That is, D is a scaled puncturing of the order-2 projective Reed-Muller code [91,6]_9.
- The 33-point set has trivial stabiliser in PGL(3,9) (Frobenius included), lies on no curve of degree 2 to 6, and has at most 20 of its points on any one Hermitian curve. The object therefore does not confirm the contributor's label "Xing-Ling norm-trace"; that label stays unverified.
- The Hermitian hull of dimension 3 needs the column scaling. Without it (points in normalised coordinates) the hull is 0. Among 20000 random Hermitian-type scalings the hull was 0, 1 or 2 and never 3.

The script embeds the recovered 33 points and 33 scalings, rebuilds D, applies the Hermitian-hull reduction, and checks that the GF(3) row space equals the shipped one (the shipped matrix is not in reduced row echelon form in any column order tried, so equality is of row spaces, not of bytes). It then recomputes s, c, k and the exact distance.
