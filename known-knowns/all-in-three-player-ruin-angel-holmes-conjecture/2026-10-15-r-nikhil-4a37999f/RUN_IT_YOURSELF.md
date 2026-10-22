From the package root, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The command builds the supplied memoized integer kernel in a temporary directory, checks exact rational geometry, recomputes all four bounds on every leaf, checks positive separation, and compares complete transcript hashes. It checks the complete real domain; it does not sample it. It exits nonzero on any mismatch and ends with PASS only after every certificate has passed. Generated files are removed automatically.

Scientific claim paths named by panelists map to object/ in this package. Supplied portable checker paths map to verify-it-yourself/. Source snapshots cited by reviewers remain in the research archive; public URLs and extracted status are supplied in the-record-we-beat/. No third-party page or dataset is needed to run the proof check.

For rebuilding the search, see how-we-built-it/REBUILD.md. The verifier does not depend on the generator or on reproducing its heuristic search history.
