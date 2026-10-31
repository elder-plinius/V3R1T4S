# How We Built It (`how-we-built-it/`)

- `PREREG.md`: Frozen pre-registration rule for `lychrel-new-base-proof` (with a dated note recording the split of this package to base 50 in #517, while #723, #724, and #725 hold the companion packages).
- `search_engines.py`: Outside-in 4-carry BFS solver for the Period-2 Outer Engine $(L_0, R_0)$ in bases $b \equiv 2 \pmod{3}$.
- `search_inner.py`: Outside-in 4-carry BFS solver for the Period-4 Inner Core $M_0$ in bases $b \equiv 2 \pmod{8}$.
- `generate_certificates.py`: Historical builder script from the multi-base run that generated `object/lychrel_base50_certificate.json` (the sole certificate included in this base-50 package; the companion certificates for bases 98 and 146 and the Kuitché 2023 audit are in #723, #724, and #725).
- `author_checker_lychrel_check.py`: Historical author checker from the initial multi-base run; for the standalone base-50 verifier used by this package, see `verify-it-yourself/check_lychrel.py`.
