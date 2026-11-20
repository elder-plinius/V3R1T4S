# How the object was built (the contributor's search code)

Everything in this folder is copied from the contributor's own snapshot (taken 2026-10-19), with absolute local paths replaced by {WORKDIR}. No other change was made.

- `lp_upper_bound.py`: builds an exact rational Delsarte (Krawtchouk) linear-programming dual certificate for a chosen cell and verifies it with `fractions.Fraction` and `sympy.Rational`. It produced `object/lp_cert_q7_n55_k10_dub40.json`.

Requirements: python3, numpy, scipy, sympy. The snapshot does not record the versions used.

Command: the snapshot's own record says the script was run as a plain `python3 lp_upper_bound.py` from the contributor's workspace, which reads the live-bounds table the contributor had parsed earlier and writes one certificate file per cell. The exact command line and the parsed table are not in the snapshot. That table is third-party data and is not copied here; the live values are in `the-record-we-beat/`.

PREREG.md: there is none. The snapshot holds no pre-registration. The claim is a certificate, and a certificate is checked by its own definition: the checker in `verify-it-yourself/` takes the excluded distance from the command line and evaluates the polynomial in exact fractions.
