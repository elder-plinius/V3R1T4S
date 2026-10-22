# Run it yourself (cell B50, proportion 0.50, mean BCFS)

## Verify the object (standard library only)
    sh verify-it-yourself/run_checks.sh      # last line PASS
Real output: verify-it-yourself/RECEIPTS.md.

## Rebuild the object
1. Get the pinned data: `git clone https://github.com/sigtyp/ST2022` and check out 03094435cba4293ce0eea383036cab78499ad50d. The systems may read only data-surprise/FAM/training-0.50.tsv, the
   masked data-surprise/FAM/test-0.50.tsv, and the development families' data/FAM/training-0.10.tsv and test-0.10.tsv. Lay them out as data/view/surprise/FAM/ and data/view/dev/FAM/ next to a tools/ folder holding how-we-built-it/tools/ (q15h.py finds data/view relative to the folder above tools/; edit its RUN line if needed).
2. Environments: how-we-built-it/requirements-systems.txt (components) and requirements-scorer.txt (scorer, stage 2).
3. Retrain and predict each entry (how-we-built-it/README.md lists them):
       python3 -I tools/q15h.py run --code how-we-built-it/entries/LENS/ROLE/code --mode test --out OUT/LENS/ROLE --props 0.50 --workers 2
4. Validation split for the weights: `python3 -I tools/q15h.py build-val` (the organisers' split rule at ratio 0.15 on training-0.50), then the same `run` with `--mode val`.
5. Combine: `STUB_MPL=1 SCO -I tools/stage2.py --entries E.json --val-test-root shared/val --gold-map G.json --test-root data/view --props 0.50 --out COMB` (E.json lists the entries in the order of how-we-built-it/combiner/entries.json; G.json maps "0.50" to the folder holding P/FAM/solutions.tsv of the validation split). The weights must come out as [1, 2, 3, 2, 2, 1, 0, 2] and COMB/test/0.50 must equal the frozen files (verify-it-yourself/frozen_result_sha256.txt).
6. `python3 tools/make_object.py COMB/test/0.50 0.50 object.tsv` writes the object.
