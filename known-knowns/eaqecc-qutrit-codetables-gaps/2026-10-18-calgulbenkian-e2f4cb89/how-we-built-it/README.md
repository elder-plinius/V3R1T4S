# How the code was built

What is here, copied from the contributor's search snapshot (read-only, taken 2026-10-18T13:45:35Z):

- `PREREG.md`: the preregistration of the whole target (all three codes of this target came from this one plan). It is frozen before the codes existed and describes the plan, not this one code.
- `verify_eaqecc.py`: the contributor's own exhaustive verifier. It enumerates the whole symplectic dual (3^(2n-s) - 1 nonzero vectors). It needs the saved table page `data/qutrit.php.html`, which is a third-party page and is not copied here (fetch it from https://eaqecc.codetables.de/qutrit.php; its sha256 is in `the-record-we-beat/README.md`). Usage: `python3 verify_eaqecc.py CERT.json data/qutrit.php.html`.
- `eaqecc_16_4_8_4.receipt.json`: the verifier's receipt for this code: s = 16, 43046720 vectors enumerated, 22.20 seconds on the contributor's machine.

What is NOT here: the scripts that constructed the code. `PREREG.md` names a search program `eaqecc_search.c` and the object's own `construction` field says how this code was made (elliptic curve AG code), but no construction script and no log of commands is in the snapshot. So the exact commands that produced `object/eaqecc_16_4_8_4.json` are not recorded, and this package cannot rebuild it from scratch. What the package does let you do is check the finished code from the definition (`verify-it-yourself/`).

The construction in the contributor's words (unverified): Elliptic-curve AG code C_L(D, 8 P_inf) on y^3 + y = x^2 over GF(9), a [16, 8, 8]_9 code, with column scaling for Hermitian hull h = 4. The 0/1/2 matrix is the GF(3) image of that code under the Hermitian-hull reduction in `PREREG.md`, section 2.

Note: the curve y^3 + y = x^2 has only 15 affine points over GF(9) (y^3 + y takes values in GF(3), and x^2 lies in GF(3) for 5 values of x, each giving 3 values of y), so C_L(D, 8 P_inf) on it has length at most 15, not 16. The construction description above is therefore wrong as written. The object file is unchanged, and its parameters are established by the checks in verify-it-yourself/, not by this description.
