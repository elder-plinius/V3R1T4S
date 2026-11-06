# Recompute the rigorous bound

From the package root, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The expected last line is exactly `PASS`, with exit status zero. Any validation failure or incomplete proof ends with `FAIL` and a positive exit status. The runner uses system Python 3.9 or later on Unix, a POSIX shell, and standard-library modules only. No package installation or network access is required.

The runner reads `config.json`, checks the object's expected SHA256 before expensive work, and checks the frozen portable checker's SHA256. It copies the authenticated bytes into a temporary directory and invokes the checker with `python3 -S` and `PYTHONOPTIMIZE=0`. It recomputes the complete continuum certificate from the integer factors. A successful digest check alone can never produce `PASS`: completion, exact degree normalization, the requested rational threshold, a complete cover and strict integer separation must also be reported by the checker.

All intermediate partitions, logs and receipts are temporary. Cleanup finishes before `PASS` is printed, so a clean-copy execution does not modify any packaged file or invalidate the package's manifest. A corrupted object is rejected before the continuum computation begins. Runtime output includes hashes and numerical results, but no local workspace path or process identifier.

The runner is a launcher for the included portable checker, not a second independent mathematical verifier. `METHOD.md` gives its self-contained mathematical argument. `RECEIPTS.md` records the scaffold's actual validation, including the provisional v6 object; it is not a claim about whichever final object is later configured.

The numerical threshold and object identity are deliberately configuration data. Before freezing a final package, bind `object_path`, `object_sha256` and `threshold` to the final reviewed bytes and exact bound. Preserve `checker_sha256` unless the reviewed checker itself changes. Keep the internal time budget below its process timeout and the process timeout below the package check's external limit. Rerun the final package and record its actual receipt before regenerating the final package manifest.
