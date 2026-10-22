# Run it yourself (cell LA)

## Verify the object (standard library only)
    sh verify-it-yourself/run_checks.sh      # last line PASS
Real output: verify-it-yourself/RECEIPTS.md.

## Rebuild the object
1. Get the pinned data: `git clone https://github.com/sigtyp/ST2022` and check out 03094435cba4293ce0eea383036cab78499ad50d. At proportion P the system may read only data-surprise/FAM/training-P.tsv, the
   masked data-surprise/FAM/test-P.tsv, and the development families' data/FAM/training-0.10.tsv and test-0.10.tsv. Lay them out as data/view/surprise/FAM/ and data/view/dev/FAM/ next to a tools/ folder holding how-we-built-it/tools/ (q15h.py finds data/view relative to the folder above tools/; edit its RUN line if needed).
2. Environments: how-we-built-it/requirements-systems.txt (system) and requirements-scorer.txt (scorer).
3. Retrain and predict at each P (each P from training-P alone), then write the object file(s); each must equal object/predictions-P.tsv byte for byte (verify-it-yourself/frozen_result_sha256.txt lists the result files):
       python3 -I tools/q15h.py run --code how-we-built-it/entries/classifier/PRIMARY/code --mode test --out OUT/0.10 --props 0.10 --workers 2
       python3 tools/make_object.py OUT/0.10/test/0.10 0.10 object-0.10.tsv
       python3 -I tools/q15h.py run --code how-we-built-it/entries/classifier/PRIMARY/code --mode test --out OUT/0.20 --props 0.20 --workers 2
       python3 tools/make_object.py OUT/0.20/test/0.20 0.20 object-0.20.tsv
       python3 -I tools/q15h.py run --code how-we-built-it/entries/classifier/PRIMARY/code --mode test --out OUT/0.30 --props 0.30 --workers 2
       python3 tools/make_object.py OUT/0.30/test/0.30 0.30 object-0.30.tsv
       python3 -I tools/q15h.py run --code how-we-built-it/entries/classifier/PRIMARY/code --mode test --out OUT/0.40 --props 0.40 --workers 2
       python3 tools/make_object.py OUT/0.40/test/0.40 0.40 object-0.40.tsv
       python3 -I tools/q15h.py run --code how-we-built-it/entries/classifier/PRIMARY/code --mode test --out OUT/0.50 --props 0.50 --workers 2
       python3 tools/make_object.py OUT/0.50/test/0.50 0.50 object-0.50.tsv
