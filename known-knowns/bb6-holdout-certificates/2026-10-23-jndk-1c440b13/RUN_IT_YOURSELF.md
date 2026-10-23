# Run it yourself

## Requirements

- CPython **3.12.15**, invoked as `python3`.
- SymPy **1.14.0**, installed in that Python environment before checking.
- A POSIX shell and standard `mkdir`/`rm` commands.
- A C11 compiler invoked as **`cc`**, such as GCC or Clang. The verifier compiles its bundled naive replay program in the same check.

The check itself makes no network requests and installs no packages.

## Verify the complete package

From the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final line: `PASS`. Allow a few minutes on a laptop as a rough estimate; no laptop benchmark is claimed. A prior clean queued-server check took 41 seconds.

The script verifies every packaged file hash, reconstructs the compressed proof packet safely, and runs its complete verifier. Temporary files are removed by the shell script.

## Optionally reconstruct and inspect the proof judgments

From a fresh package root, use output directories outside the package so generated files do not alter its declared file set:

```sh
python3 verify-it-yourself/check_bundle.py ../bb6-proof-expanded
python3 ../bb6-proof-expanded/claim/verify.py --out ../bb6-proof-verification
```

The first command reconstructs the supplied mathematical proof object from `object/proof_bundle.part-*`; its final line is `BUNDLE_INTEGRITY_PASS`. The second freshly regenerates and checks its source-bound proof judgments and ends in `PASS`. The custom trusted boundary is explicit in `object/PROOF.md` and the expanded packet.
