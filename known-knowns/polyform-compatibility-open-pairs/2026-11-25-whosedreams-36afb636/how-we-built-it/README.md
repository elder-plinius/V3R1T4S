# How we built it

- code/ is the contributor's run kit (heptiamond-compat-package; tarball sha256
  a8c88bdde9d97175096c5e6d70fd43a92979537da095d7168cc5147a893bc403), copied unchanged except that
  third_party/ (CaDiCaL 3.0.1 and drat-trim sources), bin/ and record/ are left out:
  - py/sat_compat.py: board_for_k and build_joint_cnf (the encoding), run_cadical, verify_drat
  - py/cnfutil.py: DIMACS writer and Sinz sequential-counter cardinality constraints
  - py/shapes.py, py/grid.py: the triangular lattice, D6 aspects, placements; data/heptiamonds.json: the 24 pieces
  - py/solve_pair.py, py/worker.py, run.sh, scripts/: the driver (solve without proof; on UNSAT re-solve with a
    DRAT proof and check it with drat-trim; label the result)
  - build.sh builds CaDiCaL and drat-trim from third_party/; docs/METHOD.md describes the model.
- Solver: CaDiCaL 3.0.1 (third_party/cadical VERSION 3.0.1; upstream tag rel-3.0.1).
  Checker: drat-trim, from the kit's third_party/drat-trim (drat-trim.c sha256 d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee). Packaging-machine builds: cadical sha256 24df77380aabb71c9afc397352452de9237d8979f7b0a3f41ae48b0938afaab5, drat-trim sha256 73e315b40f3f4a3b1021be5afdb530127b16a562f5e6397b0833915a92b42689 (compiler-dependent; not expected to match other builds).
- PC runs (contributor's PC, AMD Ryzen 9 9900X, WSL2 Ubuntu): `KMIN=2 KMAX=8 ./run.sh` into work/run_unrestricted
  (all 21 unrestricted '?' pairs), then a rerun with `KMIN=9 KMAX=20` into work/run_k9_20. The exact TIMEOUT and
  worker settings of the k = 9..20 run were not kept in the send-back. pc-results/ holds the two M-X summary.json
  files exactly as sent back (their per-k "seconds" include both solves and the drat-trim check).
- Encoding in one paragraph: board = all cells (r, c), 0 <= r < R, 0 <= c < C with R = max(6, ceil(2*sqrt(7k))) + 2
  and C = R + 2; variables f_cell (cell in F), one variable per placement of M and per placement of X inside the
  board (all 12 symmetries, deduplicated); exactly 7k f_cell true, exactly k M-placements and k X-placements;
  a placement implies its cells are in F; each cell in F is covered by at least one and at most one chosen
  M-placement, and likewise for X. UNSAT therefore excludes every figure of area 7k inside the board, connected or
  not, with or without holes.
- PREREG.md: written at packaging time, after the search (see its first line).
- box-reproduction/: the packaging machine's re-run (CNF regeneration k = 2..20, and CaDiCaL plus drat-trim
  for k = 2..20), with the scripts used.
