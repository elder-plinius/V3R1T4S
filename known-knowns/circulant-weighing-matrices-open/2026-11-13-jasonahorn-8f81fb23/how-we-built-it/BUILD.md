# C search build and controls

Run from the package root. Use a scratch path for binaries; the verifier does this automatically. Example standalone build:

    work=$(mktemp -d)
    cc -std=c11 -O3 -Wall -Wextra -Werror -o "$work/liftjoin" how-we-built-it/liftjoin.c
    "$work/liftjoin" --contractions
    "$work/liftjoin" --selftest
    "$work/liftjoin" all 180

The contraction mode prints exactly 25 integer rows. The self-test mode checks successful and rejected joins and autocorrelations. Synthetic join controls are tests of the algorithm, not witnesses to the nonexistent CW(208,81). The positive autocorrelation control is an inflated weight-4 row, also not a weight-81 witness.

The full run must exit successfully and finish with hits=0, capped=0, targets=25, completed=25, nodes=43196762 and matches=5519232. A single-target debug run is not sufficient evidence. The shipped Python verifier enforces these requirements and separately reproduces the search.

Undefined-behavior and address sanitizer build (compiler support required):

    cc -std=c11 -O1 -g -Wall -Wextra -Werror -fsanitize=address,undefined -fno-sanitize-recover=all -o "$work/liftjoin-san" how-we-built-it/liftjoin.c
    "$work/liftjoin-san" --selftest
    "$work/liftjoin-san" all 180

If sanitizer instrumentation is too slow for a complete run, report it as incomplete rather than substituting the noninstrumented result. See the receipts for instrumentation actually exercised on this revision.

PREREG.md is the original preregistration; its frozen claim and scope are retained. The 2026-11-14 verification repair is documented in README.md and does not rewrite that historical record.
