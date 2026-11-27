# Run it yourself

All commands are run from this package folder in a fresh shell.

## 1. Quick check (seconds, no download)
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS` (output as in verify-it-yourself/RECEIPTS.md). Set `KMAX=5` in the environment to
extend the board-free search to k = 5 (a few minutes, a few hundred MB of RAM).

## 2. Check every proof (needs the archive, about 175 MB download, 2.7 GB unpacked)
1. Download `heptiamond-MX-k2-20-proofs.tar.xz` from https://doi.org/10.5281/zenodo.24518087 into this folder.
   (Published 2026-11-25T00:44:38Z; direct file URL https://zenodo.org/api/records/24518087/files/heptiamond-MX-k2-20-proofs.tar.xz/content )
2. Build drat-trim: `git clone https://github.com/marijnheule/drat-trim && make -C drat-trim`
3. `DRAT_TRIM=./drat-trim/drat-trim sh verify-it-yourself/verify_archive.sh`
   It checks the archive sha256, unpacks it into mx-proofs/, checks the 38 file sha256s, and runs drat-trim on
   each k. Expected: 19 lines `k=.. s VERIFIED`, then `PASS`. On the packaging machine drat-trim took between
   0.2 s (k=2) and about 25 s (k=20) per proof, using up to about 1.4 GB of RAM.

## 3. Rebuild the CNFs and proofs from scratch
The encoder is in how-we-built-it/code/ (Python 3.8+, standard library). You need CaDiCaL 3.0.1
(`git clone https://github.com/arminbiere/cadical && cd cadical && git checkout rel-3.0.1 && ./configure && make`).
```sh
mkdir -p rebuild && cd rebuild
cp -r ../how-we-built-it/code/py ../how-we-built-it/code/data . && mkdir -p bin
cp /path/to/cadical/build/cadical /path/to/drat-trim/drat-trim bin/
python3 -c "from py.sat_compat import build_joint_cnf, board_for_k; c,m=build_joint_cnf('M','X',5,board=board_for_k(5)); c.write('k5.cnf')"
sha256sum k5.cnf      # equals the k5 problem.cnf line of ../object/SHA256SUMS-files.txt
bin/cadical k5.cnf k5.drat ; sha256sum k5.drat ; bin/drat-trim k5.cnf k5.drat
```
CaDiCaL is deterministic: on the packaging machine every regenerated CNF (k = 2..20) and every regenerated proof
matched the contributor's sha256s exactly (how-we-built-it/box-reproduction/). The full original run used
`KMIN=2 KMAX=8 ./run.sh` (work/run_unrestricted) and a second run with `KMIN=9 KMAX=20` into work/run_k9_20; see
how-we-built-it/README.md.
