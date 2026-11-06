# Verify the fixed object

From this package folder:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected: AEP 1543800.4664981714 MWh (printed to double precision), maximum radius 2999.999900000135 m, minimum spacing 307.51364081707464 m, recomputed participant 12 1526474.8025 and PR #938 1539447.1174 MWh, margin over the posted record 17325.66 MWh. Last line: PASS. The checker verifies the frozen-object hash, strict geometry, energy, the posted-record margin, and that the object exceeds both hash-pinned comparators.

Offline: place the two exact reference files (URLs and SHA256 in the REFERENCES mapping of check_layout.py) as reference-files/iea37-par12-opt64.yaml and reference-files/pr938-opt64.yaml, then run
```sh
python3 verify-it-yourself/check_layout.py --reference-dir reference-files
```
Fifteen hubs lie within 1e-3 m of the 3000 m boundary: keep full double precision; rounding can make the layout infeasible.

# How the object was built (provenance, not a replay guarantee)
how-we-built-it/ holds the search code (quadruple_vacancies.py with insertion.py and engine_search.py: four-hub vacancy, exact marginal beam reinsertion, SLSQP polish), pinned requirements, the run's PREREG.md, the own starting layout (starting-own-64.json, 1538890.7191 MWh; local path fields removed, original sha256 recorded in it) and the search record of this object (search-artifact-metadata.json: trial 53, polish 317, seed 2026110422). Five seeds ran in parallel sharing their own best layouts through files, so an exact replay is not deterministic; the frozen object is authoritative. Note: insertion.py and quadruple_vacancies.py expect the folder layout attempts/optimizer64/code and attempts/coordinate64/code of the original run.
