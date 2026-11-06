# Portable exact construction replay

This package reconstructs the recorded integer-polynomial search jobs that supplied the generated factors of the one final product in `claim/candidate.json`. The prior products and dual measures included here are construction inputs. The separate continuum certificates establish the final upper bound.

From this directory, install the pinned dependency in a virtual environment, then run:

```sh
python -m pip install -r requirements.txt
python runs/2026-11-05-2230/attempts/factor_search/reproduce_all_provenance.py --input provenance_final.json --out replay_result.json
python runs/2026-11-05-2230/attempts/factor_search/check_known_origins.py
```

The replay uses only Python standard-library modules and python-flint. The original search drivers are also included byte-for-byte; regenerating the short-vector ranking additionally requires NumPy, while the recorded exact combination replay does not. The replay checks exact factor recovery and emits its actual runtime and peak RSS. The second command checks original coefficient matches and exact lower-library symmetry transport. Its checkpoint may be monitored while it runs.

The directory structure deliberately mirrors the original relative paths. Run the command from this package root. Manifest SHA256 entries cover the final product, construction inputs, normalized provenance, and unchanged source files. Source files were copied without modification; provenance path strings were normalized to portable relative references, with coefficients and construction parameters unchanged.

Starting factor data and prior-library credit: David Niedbala Giraudin, *New bounds for the integer Chebyshev constant of [0,1]*, arXiv:2610.00386, https://arxiv.org/abs/2610.00386. The paper in turn credits Hare and Hodges, Hare, and Flammang for much of its starting library. No author ancillary solver or verifier script is included or used here.
