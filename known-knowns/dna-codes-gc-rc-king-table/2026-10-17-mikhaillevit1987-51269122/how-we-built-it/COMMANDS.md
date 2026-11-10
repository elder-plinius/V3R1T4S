# How the object was produced

Python 3.12, numpy. `engine.py` and `projective_search.py` sit in a folder `code/` inside a lens folder
`attempts/linear_codes/` of a run folder that also holds `data/table.json` (the parsed King table; `engine.py`
reads it only to label improvements). Command, from the lens folder:

    python code/projective_search.py

Construction: the 21 points of PG(2,4) as columns of a [21,3] GF(4) evaluation code (64 codewords); a
transvection (x,y,z) -> (x+y,y,z) fixing the line y=0 pairs the columns; one fixed point is dropped and the
remaining 20 columns are ordered so that the column pairing becomes the reversal; a coordinate offset (XOR)
moves to a coset; codewords with GC count 10 are kept; a maximum clique of the RC/Hamming compatibility graph
is taken (time-capped branch and bound). Letters 0,1,2,3 = A,T,C,G; complement = XOR 1.

The search is random and time-capped (seeded with `random.seed(13791)` in `engine.py`, but numpy offsets in
the puncturing branch and wall-clock caps make reruns not bit-identical); rerunning need not rediscover the
identical list. The frozen object is the evidence. The line of the captured output where the size first
reached 16 at (n,d) = (20,15):

    {"n": 20, "d": 15, "size": 16, "table": 15, "method": "projective_transvection_coset", "utc": "2026-10-17T14:01:02.814892+00:00", "trial": 44173, "seconds": 11.384828090667725}

`verify.py` is the author's original object check (it uses `assert`, so do not run it with `python -O`);
`verify-it-yourself/check_dna_code.py` is the standalone checker.
