contributor text, unverified

# How we found it

The brief was Henry Cohn's table of spherical codes (https://spherical-codes.org/): beat a row's 12-decimal cosine by at least 1e-10, on a row that the table does not mark as proven optimal and, for a full claim, does not flag "needs more optimization".

The search agent (an AI, Gemini) wrote a preregistration first (`how-we-built-it/PREREG.md`) with three goals: A, full wins on unflagged rows; B, a batch of at least 20 improvements in one dimension on flagged rows (partial win p2); C, exact algebraic certificates (not attempted in this package). It then wrote a small C solver, `sc_opt.c`: Riemannian L-BFGS on the log-sum-exp smoothing of the largest inner product, sharpened step by step, with random tangential kicks to hop between basins. Rows were chosen where the posted code looked loosely converged, mostly high dimensions (27 to 31) with small N, and dimension 7 for the batch. Candidate codes were normalised and polished to 30 significant digits by a separate 50-digit script, then each was compared with the table's cosine.

What worked: sharpening the smoothing to very large beta and polishing gave gains from 3e-9 to 1.4e-4 on rows whose posted codes had not fully converged. What was not recorded: the seeds, restart counts and exact commands per row (see `how-we-built-it/README.md`).

The object was then checked by the orchestrator's own checker and by the three-skeptic panel (`panel/`); the checker in `verify-it-yourself/` was written from the definition and does not use the search code.
