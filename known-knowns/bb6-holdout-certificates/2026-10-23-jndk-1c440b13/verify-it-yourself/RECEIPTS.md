# Captured verification output

Command, run from the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Runtime: CPython 3.12.15, SymPy 1.14.0, POSIX shell and a C11 compiler available as `cc`. The check makes no network requests and installs no packages.

## Clean package

Captured during replacement preparation beginning 2026-10-23T15:21:25+00:00. Actual standard output (exit 0):

```text
BUNDLE_INTEGRITY_PASS
macro exit 0 last ['RELATIVE_TCB_SOURCE_SPECIFIC_BLANK_IFF_DERIVED_NO_HALTING_DECISION']
logic exit 0 last ['LIFTING_LOGIC PASS (conditional, source obligations OPEN)']
naive exit 0 last ['SOURCE_REPLAY PASS']
synthetic exit 0 last ['SYNTHETIC_REPLAY PASS']
PASS
PASS
```

Measured checker elapsed time on the queued server: 41.85 seconds. This is not a laptop benchmark; the README's laptop allowance is an estimate.

The `logic` line describes the conditional generic lifting component. The preceding `macro` line reports the source-specific derivation that supplies its premises; the complete entry point checks their composition. The substantial custom TCB remains explicit in `object/PROOF.md`.

## Corrupted object control

One numeric digit in `object/DEFINITION.md` was changed in a separate copy, leaving its declared checksum unchanged. Actual output (exit 1):

```text
FAIL: SHA256SUMS mismatch: object/DEFINITION.md
FAIL
```

This demonstrates rejection of the corrupted packaged object, not a proof of the mathematical kernel's soundness. Scientific reproduction and source/novelty reviews are recorded in `panel/`.

## Receipt and manifest consistency

The receipt is itself hashed by `SHA256SUMS`. After this captured output is inserted and the manifest regenerated, the frozen package is checked again before publication; its clean output is compared byte-for-byte with the capture above. No mathematical object or frozen panel report is changed.
