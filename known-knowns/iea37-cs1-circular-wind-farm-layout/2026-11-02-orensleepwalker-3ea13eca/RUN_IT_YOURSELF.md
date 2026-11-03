# Verify the fixed object

From this package folder, run:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected: AEP 869713.9496471485 MWh (printed to double precision), maximum radius 1999.9999000019018 m, minimum spacing 260.25900134524915 m, and 36 assigned distances strictly above 50 m to participant 12 (total 12736.71572395246 m, with a primal-dual certificate). Last output line: PASS. The checker first checks the frozen-object hash, then strict geometry and energy, then the hash-pinned reference assignment.

The first run downloads one public reference file (URL and SHA256 are in the REFERENCES mapping of check_layout.py); it never retries a denied request or executes fetched data. Offline: place that exact file as reference-files/iea37-par12-opt36.yaml and run
```sh
python3 verify-it-yourself/check_layout.py --reference-dir reference-files
```
Two hubs lie within 1e-4 m of the 2000 m boundary: keep full double precision; any rounding can make the layout infeasible.

# How the object was built (provenance, not a replay guarantee)
how-we-built-it/ holds the generator code (search36.py engine; search36_rings.py fresh ring starts, seed 20261137; search36_ruin.py ruin-and-recreate from the own ring result, seed 20261138), pinned requirements, the search pre-registration (SEARCH_PREREG.v5.md), this verification run's PREREG.md and a log excerpt. The ruin search started from how-we-built-it/starting-own-best.json (ring restart 117, 859452.796573924 MWh) and logged this object at restart 3287 at 2026-11-01T17:34:57Z, under a wall-clock deadline. Both searches were deadline-bounded and the ruin proposals read the evolving best file, so an exact replay was not attempted; the frozen object is authoritative. Run from how-we-built-it/ with the requirements installed, e.g.:
```sh
python3 search36_ruin.py --output generated --own-seed starting-own-best.json --deadline 2099-01-01T00:00:00+00:00 --seed 20261138 --max-restarts 3288
```
