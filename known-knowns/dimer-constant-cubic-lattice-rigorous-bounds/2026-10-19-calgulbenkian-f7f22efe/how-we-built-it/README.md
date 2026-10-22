# How the object was built

Contributor material, copied from the contributor's snapshot of its working folder for the whole target (all four cells of the target share one folder). Absolute local paths were replaced by {WORKDIR}; C include lines were rewritten from angle brackets to quotes (so `#include "stdio.h"` stands for the standard header). Compiled binaries and the downloaded third-party source archives (arXiv sources of He, Friedland-Peled, FKLM and Butera et al.) are not copied; the papers are named and linked in README.md.

## Files

- `hypercubic_d4.c`: exact solver and certificate generator for the four-dimensional dimer constant.
- `verify_cubic_dimer.py`: the author's own standalone verifier (kept for completeness; it is not the package checker, which is in verify-it-yourself/).
- `PREREG.md`: the contributor's pre-registration for the whole target (all four win paths).
- `RESULTS.md`: the contributor's results note for the whole target. It covers all four win paths and several figures that are NOT part of this package's claim; it also contains the author's unrounded-down figure issues described in README.md. Read README.md section Not claimed first.

## Commands

The snapshot documents no command lines: the C programs take no arguments (their cross-sections and iteration counts are fixed in the source) and the compiler flags are not recorded. A plausible build is `cc -O2 -o NAME NAME.c -lpthread -lm`; this is a guess, not a recorded command. The standalone Python verifier runs as `python3 -I verify_cubic_dimer.py`. The package checker that the panel used is separate and lives in verify-it-yourself/.
