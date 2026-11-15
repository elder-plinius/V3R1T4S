# Run the repaired verification package

Prerequisites: Python 3 with NumPy, a C11 compiler named cc, and a POSIX shell. Development environment: Python 3.14.9, NumPy 2.5.4, GCC 13.3.0 on Linux. No network access occurs during verification and no dependency is installed automatically. The independent checker uses NumPy integer arrays; it does not use floating-point rejection.

If NumPy is absent, install the tested dependency in your own isolated environment before running checks:

    python3 -m venv .venv
    . .venv/bin/activate
    python3 -m pip install -r verify-it-yourself/requirements.txt

Keep the environment outside the package when comparing file hashes.

From the package root:

    sha256sum -c SHA256SUMS
    sh verify-it-yourself/run_checks.sh

Expected final line: PASS. A nonzero process status, FAIL, or timeout is not a successful verification.

The entry point performs:

1. Fast Python verifier regression tests (bad summaries, incomplete runs, process failures and corrupt objects).
2. Exact enumeration of the 25 contractions and comparison to object/contractions.txt.
3. C compilation from source with warnings as errors into a temporary directory, then comparison of the C contraction set to the object and Python result.
4. C positive/negative join and autocorrelation self-tests.
5. The complete C search with a 180-second internal cap and 210-second subprocess timeout. The final END record must have nodes=43196762, matches=5519232, hits=0, capped=0, targets=25 and completed=25. Substring matches are not accepted as evidence.
6. Separately implemented enumeration, checking 48 solutions at n=91, zero at n=104 and zero at n=208. The target covers both signs and all 50 contractions. Expected target join matches: 1499136. This stage has a 180-second subprocess timeout.

The C search originally took about 31 seconds on the development machine; sanitized builds are slower. Slow machines may hit the configured cap: that is an incomplete check, never a proof. Do not remove completion checks to obtain PASS.

The entry point builds only a temporary executable and suppresses Python bytecode writes. There is no trusted prebuilt executable. TMPDIR may be set to a writable directory with sufficient space.

For an independent rerun only:

    python3 -B verify-it-yourself/independent.py --verify

For fast regression tests only:

    python3 -B verify-it-yourself/test_verifier.py

See how-we-built-it/BUILD.md for standalone C and sanitizer commands, PROOF.md for coverage, and verify-it-yourself/RECEIPTS.md for the revision's actual outputs.
