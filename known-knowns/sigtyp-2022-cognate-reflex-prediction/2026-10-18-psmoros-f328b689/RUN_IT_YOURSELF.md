# Run it yourself (cell C10, proportion 0.10)

## Verify the object (standard library only)
    sh verify-it-yourself/run_checks.sh      # last line PASS
Real output: verify-it-yourself/RECEIPTS.md.

## Rebuild the object
1. Get the pinned data: `git clone https://github.com/sigtyp/ST2022` and check out 03094435cba4293ce0eea383036cab78499ad50d. The systems may read only data-surprise/<fam>/training-0.10.tsv, the
   masked data-surprise/<fam>/test-0.10.tsv, and the development families' data/<fam>/training-0.10.tsv and test-0.10.tsv. Lay them out as data/view/surprise/<fam>/ and data/view/dev/<fam>/ next to a tools/ folder holding how-we-built-it/tools/ (q15h.py finds data/view relative to the folder above tools/; edit its RUN line if needed).
2. Environments: how-we-built-it/requirements-systems.txt (components) and requirements-scorer.txt (scorer, stage 2).
3. Retrain and predict each stage-2 entry (how-we-built-it/README.md lists them):
       python3 -I tools/q15h.py run --code how-we-built-it/entries/LENS/ROLE/code --mode test --out OUT/LENS/ROLE --props 0.10 --workers 2
   Every entry is bit-deterministic (the REPRODUCE skeptic retrained all of them byte for byte, panel/reproduce.md). r1806-correspondence/PRIMARY sets HOME in line 16 of its system.py; point it at a folder of your own and warm lingpy's cache with one run first (a cold cache can change one family slightly).
4. Validation splits for the weights: `python3 -I tools/q15h.py build-val` (the organisers' split rule at ratio 0.15 on training-0.10), then the same `run` with `--mode val`.
5. Combine: `STUB_MPL=1 <scorer python> -I tools/stage2.py --entries E.json --val-test-root shared/val --gold-map G.json --test-root data/view --props 0.10 --out COMB` (E.json lists the entries in the order of how-we-built-it/combiner/entries.json; G.json maps "0.10" to the folder holding <P>/<fam>/solutions.tsv of the validation split). The weights must come out as [3, 3, 1, 2, 1, 0, 1] and COMB/test/0.10 must equal the frozen files (verify-it-yourself/frozen_result_sha256.txt).
6. `python3 tools/make_object.py COMB/test/0.10 0.10 object.tsv` writes the object.
