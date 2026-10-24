# Environment variables the Level 2-4 scripts expect

The scripts in this directory were written against one machine and have been rewritten to take their
locations from the environment, so nothing is hardcoded to the author's filesystem. Set these before
running anything beyond Level 1 of `../RUN_IT_YOURSELF.md` (Level 1 needs none of them):

| variable | meaning |
|---|---|
| `PKG` | this package's root directory (the folder containing `object/` and `how-we-built-it/`) |
| `DATA` | the unpacked pinned dataset: the directory containing `CTRPv2/` and `meta/` from Zenodo record 17343165 |
| `RESULTS` | a writable directory for drevalpy's run outputs |
| `ENV` | the Python environment with `drevalpy==1.3.5` installed (its `bin/python` is used) |
| `NCI60` | the directory holding `GI50.csv`, `nsc_smiles.csv` and `nsc_sid_cid.csv` from NCI DTP |

For example:

```sh
export PKG="$PWD" DATA=/path/to/dreval-data RESULTS=/path/to/results \
       ENV=/path/to/venv NCI60=/path/to/nci60
```

`${...}` placeholders appear inside some script bodies where a literal path was replaced; substitute them,
or set the variable and run the script through a shell that expands it, as `RUN_IT_YOURSELF.md` shows.
These scripts are the record of what was run, not a turnkey pipeline — Level 1 is the turnkey verification.
