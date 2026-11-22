# How we built it (exact commands)

Inputs: the three files of https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/ (cobalt.html, points.tgz, Co.zip), fetched
once each on 2026-10-19 (sha256 in ../the-record-we-beat/README.md), in a folder DATA_DIR. Python 3.11 with the
versions in requirements.txt.

    python3 code/audit_ccd_cobalt.py DATA_DIR audit_merged_table.csv   # the audit, with a printed summary
    python3 code/build_p1_object.py DATA_DIR ccd_cobalt_audit.csv      # the object in ../object/

The search for lower minima (exploratory, no improvement found; logs in logs/) ran from a folder holding the code and a
subfolder net/ with points.tgz and Co.zip:

    python3 code/search_seed.py 5400          # lens 1: one-atom growth (hull facets) and etching from E_best(N+-1)
    python3 code/search_mbh.py 3300 250 200 150   # lens 2: monotonic basin hopping (stopped at N = 180)
    python3 code/search_deca.py 2700          # lens 3: decahedral family from the Co.zip seeds
    python3 code/search_deca3b.py 1400        # lens 3b: the same growth chains with 3- and 4-fold sites
    python3 code/search_grow1b.py 4500        # lens 1b: growth from E_best(N-1) with 3- and 4-fold sites, N = 200..101

code/check_claim.py is the separate certifier written for any candidate (mpmath 30-digit gradient, Hessian spectrum,
distinct-basin test); it was only exercised on the known Co.zip 197 structure, because no candidate was found.
Known defects of code/check_claim.py (noted 2026-11-13, after the maintainer's review of 2026-11-03; no result in this
package depends on the file): (1) negative control 2 cannot fail: it tests len(xc[:-3]) != 3N, which holds for every
input, and its outcome does not enter the verdict; (2) the seeded calibration on ten table files that the docstring
describes never runs: the ten sizes are drawn (random.Random(20261019)) but never used, because the posted table
energies are not in DATA_DIR. The calibration on all 199 table files is done by code/audit_ccd_cobalt.py and checked
by verify-it-yourself/check_p1.py.
PREREG.md was frozen before any download; PREREG.v2.md to PREREG.v5.md record each later change of plan, with times.
