# How we found it (contributor text, unverified)

The brief was the bank entry: beat Figure 7's bars (show f(2,5) <= 13 or f(3,6) <= 12 with explicit tournaments), or settle
a cell exactly. Searches for three tournaments on 12 vertices with S_6 found none, so the work turned to proving there is
none to find.

What failed: a single formula for the whole question was too slow to solve with a proof, and some cubes of the first split
were still too slow, so they had to be split again.

What worked: a normal form (fix a vertex of largest out-degree and count its neighbours in each tournament), then three
levels of cubes, refining only the cubes that were slow, and a cover lemma for every split, so that "the cubes cover the
parent" is itself a checked UNSAT proof rather than an argument in prose. All 2,871 formulas were then solved with DRAT
proofs and checked by cake_lpr, about 27 CPU-hours over 10 hours on 3 cores (2026-10-28). One independent review read the
encoder line by line; a three-skeptic panel reviewed the claim; and after the first panel a second full run regenerated
every proof and matched every hash (2026-10-30).

We learned on the way that cake_lpr exits 0 even when it rejects a proof, so every script here reads its output line.
