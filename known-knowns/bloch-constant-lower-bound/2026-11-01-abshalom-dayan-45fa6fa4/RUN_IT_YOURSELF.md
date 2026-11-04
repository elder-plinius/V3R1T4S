# Run it yourself

From this folder: `sh verify-it-yourself/run_checks.sh`. It rebuilds trig.bin and the certificates from object/parts (hashes in object/parts/MANIFEST.txt) in a temporary .work/ folder, compiles check.c, and on all seven pieces runs check (C, directed-rounding balls) and cover_check.py (exact integers). Last line PASS or FAIL. Needs clang and python3; under a minute.

With `FLINT_PY=<a Python with python-flint>` it also runs check_arb.py on all seven pieces and check_pts.py on eta 0.2 to 0.7 (Arb, 128 bits). About 4 minutes.

Second precision: set ctx.prec to 256 in a copy of check_arb.py and check_pts.py and rerun.

Rebuilding the libraries from raw multipliers: fetch Wikstrom's archive from doi:10.5281/zenodo.21975862 (not shipped), run `python3 -I export_arrays.py <src> arrays.json`, `$FLINT_PY -I make_library.py arrays.json <dir>`, `$FLINT_PY -I code/make_strip_lib.py 0 0.2 lib strips/s0_0.2/lib --verify` (same for 0.2 0.3, 0.3 0.4, 0.4 0.5, 0.5 0.6, 0.6 0.7), and compare with object/. Run make_strip_lib.py from .work/away-primal, after `KEEP_WORK=1 sh verify-it-yourself/run_checks.sh`, because --verify reads ../near-lift/certs relative to the working directory and run_checks.sh otherwise deletes .work.

File formats: c_*.leaves: 20-byte records <4B4I = la,lr,lu,kind,ia,ir,iu,w, with A in [ia,ia+1]/2^la, rho in rho0+4[ir,ir+1]/2^lr, u in [iu,iu+1]/2^lu. c_*.wits: 88-byte records of 11 doubles (the affine centre of a kind-0 box, as read by check.c).

How the object was built: how-we-built-it/search.c and strip_search.sh make the covers; nlp.py, cp.py and build.py make the near-radius multipliers. These are float searches and untrusted; every output is re-verified by the checkers above.

Known defect: how-we-built-it/build.py can write duplicate radial nodes into a pts file. The duplicates were removed from the JSON afterwards and build.py was not fixed. check_pts.py reads the stored file, so this does not affect the check.

Versions used: python-flint 0.9.0 on Python 3.12.13, Apple clang version 21.0.0. export_arrays.py and how-we-built-it/ also need numpy.
