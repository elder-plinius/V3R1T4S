# How we built it

Contributor material, unverified. Copied from the contributor's snapshot (taken 2026-10-19T02:53:48Z) and sanitised: every absolute local path is replaced by {WORKDIR}, and usernames, emails and hostnames are removed. Compiled binaries and the contributor's own verifier scripts are not copied. Third-party datasets are not copied.

Files here:

- `PREREG.md`
- `RESULTS.md`
- `tools/fast_maxdet_search.c`
- `tools/os_3norm_search.c`
- `tools/search_williamson_all.py`
- `tools/run_williamson_and_audit.py`
- `tools/verify_hadamard_maxdet.py`

`PREREG.md` is the run's pre-registration. `RESULTS.md` is the contributor's results log for all orders of the run; only the row for order 109 belongs to this package.

## Commands

The snapshot documents tool usage in the source headers and in RESULTS.md, not a command log. Usage lines from the sources:

- `os_3norm_search`: `os_3norm_search N paley1|paley2|hadamard_file OUT_MATRIX_FILE THREADS`, compiled with `clang -O3 -march=native -pthread tools/os_3norm_search.c -o tools/os_3norm_search -lm`.
- `fast_maxdet_search`: `fast_maxdet_search N TOTAL_RESTARTS KICKS paley1|paley2|hadamard_file OUT_MATRIX_FILE THREADS`.
- Williamson Hadamard cores come from `search_williamson_all.py` (which imports `run_williamson_and_audit.py`).

The exact arguments of the run that produced this object (restart counts, seeds, thread counts) are NOT recorded in the snapshot. RESULTS.md records the construction: Orrick-Solomon style 3-normalized construction (tools/os_3norm_search.c) on the Paley class I Hadamard matrix of order 108 (p = 107), at the row triple (0, 1, 2).
