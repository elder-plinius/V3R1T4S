# Run it yourself

From this folder, in a fresh shell (needs `sh`, `curl`, `sha256sum` and Python 3 with the ability to create a venv and install packages):

```sh
sh verify-it-yourself/run_checks.sh
```

What it does:

1. Downloads https://www.minlplib.org/gms/pricing050.gms once into `verify-it-yourself/_instance/` (about 15 KB; third-party data is not copied into this package) and checks sha256 `192dd92d69cdcd131462d40c137df73dc101afef0739cc7ba98c130a79313715`.
2. Creates `verify-it-yourself/_venv/` if needed and installs pinned `python-flint==0.9.0`.
3. Runs `verify-it-yourself/check_dual_certificate.py` on `object/lambda.txt` and `object/cert_arb_leaves.json`: parses the posted model, checks that each variable's 1958 leaves cover `[0,10]` with no gaps, proves every leaf lower bound with Arb ball arithmetic (natural + mean-value enclosure, adaptive bisection if needed), reassembles the Lagrangian dual, and checks that the resulting upper bound U on max objvar satisfies both `U <= -1813.829075713452` and `U <= -1813.829078 + 1e-6*1813.829078`.

Expected output ends with:

```
dual certificate: max objvar <= -1813.829075713452 (<= bar -1813.827264170922); leaves 1958 verified
PASS
```

First run: about one minute (mostly the venv install). Later runs: a few seconds. Real output: `verify-it-yourself/RECEIPTS.md`.

To rebuild the leaf log (same bytes at fixed flint precision), follow `how-we-built-it/COMMANDS.md`.
