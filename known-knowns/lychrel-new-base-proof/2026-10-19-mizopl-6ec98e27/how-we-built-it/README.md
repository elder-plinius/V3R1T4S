# How We Built It (`how-we-built-it/`)

- `PREREG.md`: Pre-registration record for this base-98 package (split from the initial multi-base evaluation in [PR #517](https://github.com/elder-plinius/V3R1T4S/pull/517) so that `object/lychrel_base98_certificate.json` is packaged as a single standalone object).
- `search_engines.py`: Outside-in 4-carry BFS solver for the Period-2 Outer Engine $(L_0, R_0)$ in our $b \equiv 2 \pmod{3}$ search family.
- `search_inner.py`: Outside-in 4-carry BFS solver for the Period-4 Inner Core $M_0$ in our $b \equiv 2 \pmod{8}$ search family.
- `generate_certificates.py`: Historical builder script from the initial multi-base search run that produced `object/lychrel_base98_certificate.json` (the sole certificate shipped in this base-98 package).
- `author_checker_lychrel_check.py`: Historical multi-base author checker from the initial run; for the standalone base-98 verifier executed by `verify-it-yourself/run_checks.sh` in this package, see `verify-it-yourself/check_lychrel.py`.
