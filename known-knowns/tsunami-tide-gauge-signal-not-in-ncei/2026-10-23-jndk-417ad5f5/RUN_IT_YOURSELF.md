# Run it yourself

From this folder, in a fresh shell (Python 3.8+, internet):

```sh
sh verify-it-yourself/run_checks.sh
```
Expected output: one line per series (luga/prs R 8.445, lifo/prs R 5.238, lifo2/rad R 5.228, all checks True), then
`stations passing: ['Lifou', 'Luganville']` and `PASS` (verify-it-yourself/RECEIPTS.md).

Rebuild the object (numpy, scipy, matplotlib: how-we-built-it/requirements.txt; internet for IOC, NCEI, ETOPO1):

```sh
cd how-we-built-it
python3 sweep.py p1            # all NCEI earthquake events since 2024; writes results.jsonl and candidates.json
python3 null.py candidates.json  # 400 random origin times for each candidate
python3 check_p1.py RAW_DIR    # re-score luga/lifo/lifo2 from saved raw IOC JSON (RAW_DIR holds the three files)
```
The frozen rules are in how-we-built-it/PREREG.md (tsu.py sha256 61bccc50777e893634ff2e199a836fa79c8a30e50a13aa796de0f0f6e6f85a54).
