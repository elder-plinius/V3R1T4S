# Run it yourself

Requirements: CPython 3.12.15, SymPy 1.14.0, a POSIX shell, and `tar`. There is no network access or package installation in the check.

From the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS`. The script verifies the package file hashes, reconstructs the compressed proof packet, checks its safe contents, and runs the packet verifier. The proof packet is the object archive in `object/proof_bundle.part-*`.
