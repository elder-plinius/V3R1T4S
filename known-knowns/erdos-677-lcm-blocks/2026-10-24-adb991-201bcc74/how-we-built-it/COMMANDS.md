# How the object was built

Files here:
- `PREREG.md`: the run's pre-registration (criterion, planned claim C-R2 and judge, frozen 2026-10-24T08:24:04Z
  before any attack program of the run started). No null test: the claim is an exhaustive deterministic verification
  judged by exact arithmetic, with no search statistic.
- `claim/`: the claim as the panel saw it: `CLAIM.md` (the claim, the certificate, things a skeptic should know, the
  scout's status record, the success criterion quoted verbatim) and `REPRODUCE.md`; `claim/checker/spec_677.lean` is
  the formal statement frozen verbatim from google-deepmind/formal-conjectures (`Erdos677.erdos_677` with the
  definition `lcmInterval`), and `spec_677_negation.lean` its negation. The claim's exact judge `checker/check677.py`
  is `verify-it-yourself/check677.py` here (same bytes). The claim's copies of third-party files (`claim/source/`:
  the formal-conjectures Lean file, the problem page text, the scout's fetch log) are not included; their URLs, fetch
  times and sha256 are in `claim/CLAIM.md` and `the-record-we-beat/STATUS_RECORD.md`.
- `lens-reports/extender-r2_report.md` and `lens-reports/rigor-margin_report.md`: the two lens reports of the run
  (`attempts/extender-r2/report.md`, `attempts/rigor-margin/report.md`), copied unchanged. File names in them (`out/…`,
  `code/…`, `NOTES.md`) refer to the lens folders in the contributor's workspace, which are not shipped; the outputs
  that the claim uses are in `object/out/`.
- `PATCH_NOTE.md` and `deep_rig_patch.diff`: the pre-filter patch made to `deep_rig.py` during the run.

The code that found the object is the object itself (`object/`): `search677b.c` (C) and `verify_cands.py` for the
small-X search, `deep_cf.py` (the ratio sets and continued fractions) and `deep_rig.py` for the enumeration,
`taskA_ratio_audit.py` for the ratio-set audit, `rig_margin.py` and `rig_margin_exact.py` for the margin. Python 3
with gmpy2, mpmath and numpy (the run used Python 3.13.16, gmpy2 2.3.2, mpmath 1.3.0, numpy 2.5.4); `verify_cands.py` needs only the standard
library, and every script that imports `deep_cf.py` needs all three modules. `deep_rig.py`,
`deep_cf.py`, `search677b.c` and `verify_cands.py` are byte-identical to the extender-r2 lens copies; in the three
rigor-margin scripts only the import path of `deep_cf.py` was changed to the script's own folder (`claim/CLAIM.md`).

Commands the lenses ran (from the lens logs and `claim/REPRODUCE.md`; `PY` was the workspace's Python with gmpy2,
mpmath and numpy, always with `-I`; QMAX = 10^495 is printed in every saved TOTAL line):

```sh
# extender-r2 (code/ = the lens's copy of object/), 2026-10-24
gcc -O2 -march=native -o search677b search677b.c -lm  # compile line as in claim/REPRODUCE.md
./search677b 1100000 4242 out/search_N1.1e6.txt               # 08:24:57, "# COMPLETE kmin=3 kmax=147 total_candidates=2 elapsed=4s"
PY -I verify_cands.py out/search_N1.1e6.txt > out/verify_N1.1e6.txt
QEXP=495 PY -I code/deep_rig.py 3 18 1040 0.001 1000000      # final (patched) runs launched 09:06:59
QEXP=495 PY -I code/deep_rig.py 19 22 1040 0.001 1000000
QEXP=495 PY -I code/deep_rig.py 23 23 1040 0.001 1000000
QEXP=495 PY -I code/deep_rig.py 24 24 1040 0.001 1000000
QEXP=495 PY -I code/deep_rig.py 25 25 1040 0.001 1000000
# rigor-margin
PY -I taskA_ratio_audit.py 3000                              # started 08:29:24
PY -I rig_margin.py 3 25 1000000 1 1000                      # started 08:31:15
PY -I rig_margin_exact.py 3 25 1000000 1 1000                # started 08:36:50, finished by 09:34
```

The per-k times of the final enumeration runs are the `t=` fields of `object/out/deep_rig_final_*.txt` (cumulative
within each run; for example k = 24 alone took 4762 s and k = 25 alone 3161 s, with five runs sharing four cores).
The same commands, from the claim folder, are `claim/REPRODUCE.md`; the package's own check is
`verify-it-yourself/run_checks.sh`.
