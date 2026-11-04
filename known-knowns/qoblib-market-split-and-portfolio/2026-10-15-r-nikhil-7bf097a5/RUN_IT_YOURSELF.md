# Verification in a fresh shell

From this package directory run:

```sh
sh verify-it-yourself/run_checks.sh
```

Python 3.9 or newer and HTTPS access to the two public GitHub input files are sufficient. No third-party package, credentials, login or account is needed. SOURCES.json pins each public input by commit, byte count and SHA256. A failed request or wrong hash stops verification without a retry. The public covariance input is larger than the package file cap, so it is fetched rather than redistributed.

To reuse previously downloaded public inputs, set `V3R1T4S_QOBLIB_CACHE` to their directory; both files must have the exact source names and hashes. If that variable is absent, a temporary download directory is used. The two independent checkers must agree on every objective component and the total -1696664. Expected last line: `PASS`.

Search code, dependency version, a concrete rerun and the limitation on exact heuristic rediscovery are in how-we-built-it/METHOD.md. The certificate itself is the complete canonical portfolio file; it can be copied or reconstructed directly from its period/symbol/long/short rows.
