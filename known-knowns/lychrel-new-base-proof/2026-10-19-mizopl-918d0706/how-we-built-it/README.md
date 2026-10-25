# How We Built It (`how-we-built-it/`)

- `PREREG.md`: Frozen pre-registration rule for `lychrel-new-base-proof`.
- `search_engines.py`: Outside-in 4-carry BFS solver for the Period-2 Outer Engine $(L_0, R_0)$ in bases $b \equiv 2 \pmod{3}$.
- `search_inner.py`: Outside-in 4-carry BFS solver for the Period-4 Inner Core $M_0$ in bases $b \equiv 2 \pmod{8}$.
- `generate_certificates.py`: Generates `lychrel_base50_certificate.json`, `lychrel_base98_certificate.json`, `lychrel_base146_certificate.json`, `seal_base26_baseline_certificate.json`, and `kuitche_2023_audit.json`.
- `author_checker_lychrel_check.py`: Full symbolic carry-transducer, non-palindromicity, brute-force ($1 \le m \le 500$), 100,000-step regex orbit, and Kuitche (2023) audit verifier.
