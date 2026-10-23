# Replay the recorded construction

From this directory run `python3 rebuild.py`. Expected last line: REBUILD PASS. It uses the Python standard library, no network or solver.

This replays the selected constructive decisions with the unchanged discovery Circuit/materialize/prune code. It produces an exactly verified 182-addition circuit for2x4x8 with 51 products. It does not rerun the original optimization or guarantee the same serialized circuit bytes.

The original search command was `python3 milp_search.py --format 2x4x8 --map v --seed 101 --limit 180 --mag 2 --seconds 90`. Discovery logs, observed dependency versions, pinned public-source metadata, selected-operation certificate and own predecessor circuits are retained. Full original dictionaries and runtime model-script hashes were not recorded, so exact whole-search replay is unavailable. Archived model files are labelled post-discovery snapshots. NumPy 1.24.3 and SciPy 1.11.4 were observed for search; the logged HiGHS version was 1.2.0. requirements-search.txt pins the Python search dependencies, but certificate replay and verification require none.

The constructive replay was actually executed and produced REBUILD PASS. Reference data and downloaded pages are not distributed.
