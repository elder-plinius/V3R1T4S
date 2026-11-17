# How the object was built

Two independently written exhaustive programs over all 4194304 sets S with max S = 23 (bit i-1 of the mask = move i):

- A/subper_a.c (C): the last n values packed in machine words (5 bits per value), the first n positions computed
  directly, then Brent's cycle detection on the window sequence from the first full window. A/run_a.py splits the mask
  range over processes and merges maxima (first maximiser in mask order) and histograms.
- B/src/main.rs (Rust, standard library only): values from the value array, oldest-first packed window keys, the period
  is p - q at the first repeat of a window (hash map), threads split the range.

```sh
cc -O2 -o A/subper_a A/subper_a.c
python3 A/run_a.py sg 23 4 out_A.txt       # about 4 s with 4 processes
(cd B && cargo build --release)
B/target/release/subper_b sg 23 4 > out_B.txt  # about 6 s with 4 threads
python3 A/compare.py out_A.txt out_B.txt   # max_equal, set_equal and hist_equal must all be true
```

object/A389690_23.txt is A's output rewritten with a short header (value, maximising set, number of sets, number of
histogram lines) followed by the same "period count" lines. PREREG.md is the run's frozen rule.
