# Run it yourself (cell L30, proportion 0.30, mean BLEU)

## Verify the object (standard library only)
    sh verify-it-yourself/run_checks.sh      # last line PASS
Real output: verify-it-yourself/RECEIPTS.md.

## Rebuild the object
1. Get the pinned data: `git clone https://github.com/sigtyp/ST2022` and check out 03094435cba4293ce0eea383036cab78499ad50d.
   The systems may read only data-surprise/FAMILY/training-0.30.tsv, the masked data-surprise/FAMILY/test-0.30.tsv, and the
   development families' data/FAMILY/training-0.10.tsv and test-0.10.tsv. Lay them out as data/view/surprise/FAMILY/ and
   data/view/dev/FAMILY/ next to a tools/ folder holding how-we-built-it/tools/ (q15h.py finds data/view relative to the
   folder above tools/; edit its RUN line if needed).
2. Environments: how-we-built-it/requirements-systems.txt (entries) and requirements-scorer.txt (scorer, stage 2).
3. Retrain and predict each entry (how-we-built-it/README.md lists them):
       python3 -I tools/q15h.py run --code how-we-built-it/entries/LENS/ROLE/code --mode test --out OUT/LENS/ROLE --props 0.30 --workers 2
   Every entry is bit-deterministic (the REPRODUCE skeptic retrained all of them byte for byte twice, panel/reproduce.md).
4. Validation split for the weights: `python3 -I tools/q15h.py build-val` (the organisers' split rule at ratio 0.15 on
   training-0.30), then the same `run` with `--mode val`.
5. Combine: `STUB_MPL=1 SCORER_PYTHON -I tools/stage2_bleu.py --entries E.json --props 0.30 --val-test-root shared/val
   --gold-root shared/val --test-root data/view --out COMB` (E.json lists the entries in the order of
   how-we-built-it/combiner/entries.json). The weights must come out as [2, 2, 1, 3, 1, 3] and COMB/test/0.30 must equal the
   frozen files (verify-it-yourself/frozen_result_sha256.txt).
6. `python3 tools/make_object.py COMB/test/0.30 0.30 object.tsv` writes the object.
