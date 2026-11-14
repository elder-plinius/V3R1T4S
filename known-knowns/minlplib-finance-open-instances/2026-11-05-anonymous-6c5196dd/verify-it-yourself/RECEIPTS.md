# Receipts

Command (from the package folder, wall clock 2026-11-05T20:09:50Z UTC):

```sh
sh verify-it-yourself/run_checks.sh
```

Real output:

```
instance sha256 ok 192dd92d69cdcd131462d40c137df73dc101afef0739cc7ba98c130a79313715
gms sha256 192dd92d69cdcd131462d40c137df73dc101afef0739cc7ba98c130a79313715
parsed e2: 50 terms
parsed e3: 50 terms
parsed e4: 50 terms
parsed e5: 49 terms
parsed e6: 50 terms
total NL terms 249 nonzero c 46
n_leaves 1958 n_ok 1958
const 4535.60102720
LB from verified leaf claims 1813.82907571345236477629728158768968
U -1813.82907571345236477629728158768968
claimed_U -1813.829075713452
bar -1813.827264170922
U <= claimed_U True
U <= bar True
dual certificate: max objvar <= -1813.829075713452 (<= bar -1813.827264170922); leaves 1958 verified
PASS
```

First run also creates `verify-it-yourself/_venv/` (python-flint 0.9.0) and downloads `verify-it-yourself/_instance/pricing050.gms`; those directories are local artifacts and are not part of the published package.
