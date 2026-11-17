# How the object was built

Files here:
- `PREREG.md`: the run's pre-registration (criterion and judge, frozen 2026-10-15T07:28:24Z before any attack
  program was run). No null test: the claim is an exact statement judged by exact arithmetic, with no search
  statistic.
- `claim/`: the claim as the panel saw it: `CLAIM.md` (the claim, object hashes, the scout's status record, the
  success criterion quoted verbatim) and `REPRODUCE.md`; `claim/checker/spec_677.lean` is the formal statement frozen
  verbatim from google-deepmind/formal-conjectures (`Erdos677.erdos_677` with the definition `lcmInterval`), and
  `spec_677_negation.lean` its negation. The claim's exact judge `checker/check677.py` is
  `verify-it-yourself/check677.py` here (same bytes). The claim's copies of the third-party source files
  (formal-conjectures Lean files, the catalog entry) are not included; their URLs, fetch times and sha256 are in
  `claim/CLAIM.md`.

The code that found the object is the object itself: `object/range_nCk.py` (Python 3, standard library only). The
proof that makes its enumeration complete is `object/PROOF.md`. Commands, from the claim folder
(`claim/REPRODUCE.md`):

```sh
python3 -I object/range_nCk.py 5871 > my_range_nCk_C5871.txt
cmp my_range_nCk_C5871.txt object/out/range_nCk_C5871.txt && echo IDENTICAL
tail -n 1 my_range_nCk_C5871.txt                 # RESULT: no counterexample with n <= 5871 k
python3 -I checker/check677.py n m k             # exact judge for one triple (arguments in the order n, m, k)
```

In the run, the lens that wrote the program ran it as `python -I code/range_nCk.py 5871` (lens REPRODUCE.md: "3 min";
the C = 5871 run finished at 08:07 on 2026-10-15). The panel reran it twice, 133.8 s (REPRODUCE) and 134 s
(CRITERION), both byte-identical to `object/out/range_nCk_C5871.txt`; this package's check reran it in 142 s
(`verify-it-yourself/RECEIPTS.md`).
