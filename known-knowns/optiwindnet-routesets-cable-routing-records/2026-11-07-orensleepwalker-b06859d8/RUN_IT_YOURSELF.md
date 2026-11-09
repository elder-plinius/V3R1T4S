# Verify
From this folder: `sh verify-it-yourself/run_checks.sh` (last line PASS). It checks the frozen object hashes, downloads the release once (pinned sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a), reads the nodeset and stored route sets with sqlite3, and checks: total Euclidean length 449188.8203 m; every turbine connected exactly once (a forest rooted at the substations); every feeder subtree at most 6 turbines (branching allowed); feeders per substation not above the shortest stored set's; no proper crossings; every segment inside the closed border and outside every obstacle interior; strictly shorter (> 1e-6 relative) than every stored route set of the instance, of any topology.
Offline: put the release file in a folder and run `python3 verify-it-yourself/check_route.py --reference-dir <folder>`.
Official validator (optional, needs optiwindnet 0.3.2 and its dependencies; see how-we-built-it/requirements-optiwindnet-env.txt): rebuild the route-set graph from object/routeset-packed.json with optiwindnet's storage functions (as G_from_routeset does for database rows) and run optiwindnet.validating.validate_routeset(G); expect [].

# How the object was produced (provenance, not a replay guarantee)
how-we-built-it/lns_branched.py: starting from a stored route set, repeatedly pick a random turbine, keep a window of its 22-34 nearest turbines free, pin every other turbine's outgoing link, and re-solve with optiwindnet's OR-Tools CP-SAT model (branched, segmented feeders, feeder cap = the shortest stored set's, 30 s per window, warm start from the incumbent, 1 worker, selected seed 9); accept only shorter route sets that pass validate_routeset and how-we-built-it/checks.py (border and obstacles). Frozen plan: how-we-built-it/PREREG.md. Solver timing makes replays differ; the frozen object is authoritative.

The exact executed source is lns_branched_original.py. The portable lns_branched.py differs only in finding checks.py beside itself rather than in the run's common directory; algorithm and parameters are unchanged. Original neighborhood implementation: Claude Code, 2026-11-06; this run: Codex.

From a fresh shell in this package, a prospective single-worker rerun is:
```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r how-we-built-it/requirements-optiwindnet-env.txt
sh verify-it-yourself/run_checks.sh
mkdir -p data replay
python3 - <<'PY'
import lzma, pathlib, tempfile
p = pathlib.Path(tempfile.gettempdir()) / 'own-routesets-cache' / 'c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a'
pathlib.Path('data/work.sqlite').write_bytes(lzma.decompress(p.read_bytes()))
PY
RUN_DEADLINE=$(python3 -c 'from datetime import datetime,timedelta,timezone; print((datetime.now(timezone.utc)+timedelta(minutes=37)).isoformat())')
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 nice -n 10 timeout 2700 .venv/bin/python how-we-built-it/lns_branched.py --name 'Hornsea One.1_OSS' --cap 6 --seed 9 --k 28 --sub-time 30 --start-from-shortest --deadline "$RUN_DEADLINE" --out replay > replay/log.jsonl 2>&1
```
The original run used all five declared workers and selected per capacity; these commands rerun only this package's selected seed. A timing-dependent rerun need not reproduce the same trajectory or final object.
