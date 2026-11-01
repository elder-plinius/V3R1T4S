# Commands (code is in ../object/code; hashes in ../verify-it-yourself/object.sha256)
python object/code/test_small.py                 # sieve vs primesieve and depths vs numpy on a 2^22-odd window near 1.5e15
python object/code/run_range.py --out OUT        # the whole run (resumable); about 5.1 h with a shared GPU, about 3 h idle
python object/code/verify_counts.py OUT 500 2    # primecount comparison at every 500th window and the last: "windows checked 95 mismatches 0"
python object/code/build_claim.py OUT claim      # summaries, histogram, sample blocks, RESULT.json
