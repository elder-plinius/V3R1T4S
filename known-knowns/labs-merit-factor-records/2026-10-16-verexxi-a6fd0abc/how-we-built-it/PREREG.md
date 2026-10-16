# PREREG (frozen 2026-10-16T17:09:18Z, before any seeded-search output was scored)

criterion (verbatim): Success means an explicit +-1 sequence of length L with 67 <= L <= 600 whose exactly computed integer energy E = sum_{k>=1} C_k^2 is STRICTLY SMALLER (direction: min) than the best published energy for that L at verification time, taken as the minimum over the tables in arXiv:2607.09688, arXiv:2504.00987, the Boskovic et al. LABS records repository cited there, and any newer arXiv result. Compare integer energies, never rounded merit factors. For L <= 66 the optimum is proven; lower energy there means a bug.

Claim unit: one length L per claim, panelled separately.

Statistic: E = sum_{k=1}^{L-1} C_k^2 with C_k = sum_{i=0}^{L-1-k} s_i s_{i+k}, computed exactly as integers by
tools/labs_energy.py (pure Python ints) and by a second independent implementation (numpy int64 np.correlate),
which must agree.

Baseline for L: baseline_E(L) = the minimum over (a) every printed energy, (b) the smallest integer energy consistent
with every printed merit factor (rounding at its printed precision), and (c) the recomputed energy of every printed
sequence, over all sources assembled in baseline/rows.tsv (Knauer 2004 via git_labs; arXiv 1406.5301, 1512.02475,
2011.00068, 2206.12070 incl. its "old MF" column, 2210.15962, 2409.07222 incl. its previous-F column, 2504.00987 incl.
previous E, 2607.09688 incl. previous F), plus any further published value found by the settled-check lens or the
NOVELTY skeptic. Lengths whose baseline depends on a source I could not read are not claimable.

Threshold: a claim for L needs E < baseline_E(L) strictly (integer comparison). A tie is not a record.
Also required: length exactly L, alphabet {+1,-1} (written 0/1 with 0 -> +1, 1 -> -1; E is invariant under negation).
Partial win p1 is a fallback only (skew-symmetric odd L >= 121, below the best published skew energy).

null_test: not needed because each claim is an explicit sequence whose energy is computed by a deterministic exact
checker and compared with a published table value; no statistical or "beats chance" inference is made.
