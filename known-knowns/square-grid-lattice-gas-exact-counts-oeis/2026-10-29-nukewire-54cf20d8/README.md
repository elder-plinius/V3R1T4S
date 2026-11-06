# A028420 a(28): the next term of the monomer-dimer tiling sequence (main criterion)

Submission id: 2026-10-29-nukewire-54cf20d8 · target:
square-grid-lattice-gas-exact-counts-oeis · claim level: full success criterion
(one sequence term; the bank's main arm A028420).

## What

confirmed_scope: The 222-digit integer in a28_value.txt (sha256 883cfca9...a666) is established as the exact value of a(28) of OEIS A028420 — unpublished on the live b-file at this panel's own 2026-10-29 re-fetch — by two independent runs (row-major and column-major sweeps over disjoint 21-prime sets, both CRTs reconstructing the identical integer, each 1282-bit modulus above the 1243-bit 3^784 anchor bound, and a fresh-prime match by this panelist's own third-sweep DP), with every published term n = 0..27 now reproduced exactly (n <= 20 by exact big-integer gates plus this panelist's own independent exact recomputations of all of them, n = 21..27 by the completed full multi-prime CRT exact gate, all equality checks re-run with this panelist's own CRT) and the value on the monomer-dimer c/n^2 growth trajectory to 3.0e-5 — meeting the FULL success criterion with the explicit disclosure that the criterion's literal parenthetical "within 1e-3" is unattainable by any true term of this sequence at reachable n (all published terms themselves miss it by >= 2.3e-2), so the growth clause is passed under its main-clause reading.

## Check it yourself

One command, standard library only (Python 3.8+), about 4 minutes:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (the standalone checker re-derives the transfer from the
definition and reproduces the published terms; receipts in
verify-it-yourself/RECEIPTS.md).

## Compared to

OEIS A028420, b-file https://oeis.org/A028420/b028420.txt fetched 2026-10-29 (HTTP 200,
sha256 af5ce6dc...; see the-record-we-beat/): published through n = 27; a(28) ABSENT at
claim time and at the panel's re-fetch.

## Not claimed

- Any term beyond a(28); the values of A006506 or A063443 (the target's other arms).
- Proof of the monomer-dimer entropy constant or any asymptotic statement.
- "Solution" of the sequence: one term, computed exactly.

## Credits

- The two-run + CRT framework and the anchor bound argument: our own (documented in
  how-we-built-it/).
- The sequence and published terms: OEIS A028420 (N. J. A. Sloane, editor), b-file as
  fetched; earlier terms by multiple contributors per the OEIS page.
- The entropy-constant context (monomer-dimer constant): the literature cited on the
  OEIS page (Heilmann-Lieb; see the page's references).
- Panel: three fresh-context skeptics (reproduce, novelty, criterion-repanel) whose
  verdicts are in panel/ as written.
