# How the object was built (the contributor's search code)

Everything in this folder is copied from the contributor's own snapshot (taken 2026-10-19), with absolute local paths replaced by {WORKDIR}. No other change was made.

- `qlp.py`: a phase-1 simplex for the qubit stabilizer-code linear program (stabilizer and normalizer enumerators linked by the quaternary MacWilliams identity, with optional shadow rows) in python-flint ball arithmetic. When the program is infeasible, the row duals are rationalised, repaired exactly and re-verified in Python integers, and returned as a Farkas certificate. It produced `object/cert_117_3_39_sh.json`.
- `check_cert.py`, `check2_recurrence.py`: the contributor's two integer checkers (direct Krawtchouk sums, and the three-term recurrence). They are the contributor's own; the checker in `verify-it-yourself/` was written separately from the LP definition.
- `run_qubit_campaign.py`: the campaign script that chose cells and called `qlp.solve_phase1(n, k, d, True, prec=1536, window=8)` for the excluded distance d. Its reference to a private local git repository (used to list cells already claimed) is replaced by {WORKDIR}/cg_repo.git and will not run without that repository.
- `scan.py`, `parse_table.py`, `propagate.py`: batch scanning, table parsing and propagation-closure helpers.

Requirements: python3 and python-flint; the snapshot does not record versions.

Commands: the campaign was run as `python3 run_qubit_campaign.py` from the contributor's workspace (with `ref/` and a parsed copy of the live table in `data/`). The parsed table is third-party data and is not copied here; the live values are in `the-record-we-beat/`. The exact command line used for this one certificate is not separately recorded.

PREREG.md: there is none. The snapshot holds no pre-registration. The claim is a certificate, and a certificate is checked by its own definition.
