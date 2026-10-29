contributor text, unverified

# How we found it

The brief was Henry Cohn's table of spherical codes (https://spherical-codes.org/): beat a row's 12-decimal cosine by at least 1e-10, on a row that the table does not mark as proven optimal and, for a full claim, does not flag "needs more optimization".

The search agent (an AI, Gemini) wrote a preregistration first (`how-we-built-it/PREREG.md`) with three goals: A, full wins on unflagged rows; B, a batch of at least 20 improvements in one dimension on flagged rows (partial win p2); C, exact algebraic certificates (not attempted in this package). It then wrote a small C solver, `sc_opt.c`: Riemannian L-BFGS on the log-sum-exp smoothing of the largest inner product, sharpened step by step, with random tangential kicks to hop between basins. Rows were chosen where the posted code looked loosely converged, mostly high dimensions (27 to 31) with small N, and dimension 7 for the batch. Candidate codes were normalised by a separate 50-digit script and their coordinates written to 30 significant digits (the active contacts agree only to about 1e-10), then each was compared with the table's cosine.

What worked: sharpening the smoothing to very large beta and polishing gave gains from 3e-9 to 1.4e-4 on rows whose posted codes had not fully converged. What was not recorded: the seeds, restart counts and exact commands per row (see `how-we-built-it/README.md`).

The object is a re-optimisation of Ilmari Vahteristo's posted code at https://spherical-codes.org/data/30/62, which was its seed: it keeps the same point order, and each point (after normalising) moved by 0.010 to 0.020 in Euclidean distance (posted file fetched 2026-10-27T13:29:42Z, sha256 d73e88783048800f1c59819a11a853eabd08cf9d10d7ca854554942d684d2cfd).

The object was then checked by the three-skeptic panel (`panel/`); the checker in `verify-it-yourself/` was written from the definition and does not use the search code.
