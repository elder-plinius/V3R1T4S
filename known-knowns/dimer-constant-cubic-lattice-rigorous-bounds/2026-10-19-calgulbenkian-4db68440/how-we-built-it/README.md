# How the object was built

Contributor material, copied from the contributor's snapshot of its working folder for the whole target (all cells of the target share one folder). Absolute local paths were replaced by {WORKDIR}; C include lines were rewritten from angle brackets to quotes (so `#include "stdio.h"` stands for the standard header). Compiled binaries, the other programs and certificates in the snapshot, and the downloaded third-party source archives (arXiv sources of He, Friedland-Peled, FKLM and Butera et al.) are not copied; the papers are named and linked in README.md.

## Files

- `cubic_md_h3.c`: exact permanent plus subset-zeta solver and certificate generator for the monomer-dimer entropy h3. Its main function runs several cross-sections; the call solve_md(5, 4, 50, "results/cert_md_h3_54.txt") writes the certificate of this package.
- `verify_cubic_dimer.py`: the author's own standalone verifier (kept for completeness; it is not the package checker, which is in verify-it-yourself/).
- `PREREG.md`: the contributor's pre-registration for the whole target (all four win paths).
- `RESULTS.md`: the contributor's results note for the whole target. It covers all four win paths and several figures that are NOT part of this package's claim. Read README.md section Not claimed first.

## Commands

The snapshot documents no command lines: the C programs take no arguments (their cross-sections and iteration counts are fixed in the source) and the compiler flags are not recorded. A plausible build is `cc -O2 -o NAME NAME.c -lpthread -lm`; this is a guess, not a recorded command. The standalone Python verifier runs as `python3 -I verify_cubic_dimer.py`. The package checker that the panel used is separate and lives in verify-it-yourself/.
