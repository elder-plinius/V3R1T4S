# PREREG (frozen 2026-10-25T07:37:10Z, from date -u)

## Honesty note: the value existed before this prereg

This prereg does NOT precede the object, and it does not precede this run's comparator fetches. The <30,31,31> rank-12906 scheme was built by the band run from LITA's 31x31x31 scheme: conversion 2026-10-24T23:11:06Z to 2026-10-24T23:11:08Z, first rebuild 2026-10-24T23:11:08Z to 2026-10-25T00:37:15Z (N = 31 was rebuilt once only; no second rebuild was run, so determinism is NOT confirmed for this N); the band run's numpy checker (check_exact_np.py, the version of that run, which has an assertion that every single term contribution is below 2^53) aborted on this cell with that assertion after the line for slab 400 had printed (cells/N31/30x31x31/check.log: AssertionError, FAIL; a limit of that checker, not a failed equation: 0 wrong so far); the pure-integer standard-library checker (check_brent_stdlib.py of the 18x18x19 package, cells/N31/check_stdlib_integer.log) passed with 0 wrong; the check_exact_np.py shipped in this claim has an exact Python-integer path for such terms, was written after that run and is first run in this run's own receipts. The prediction of the rank from the closed-form kill counts ((N^2+3N)/2 removed by slice 1 with its 2-reduction, (N^2+2N-1)/2 by slice 2) was made in the earlier 18x18x19 work; no timestamped prediction file for this N was saved, so nothing is claimed about when it was made; it is not part of any evidence here. The comparator pages in data/ were fetched 2026-10-24T22:35:43Z to 2026-10-25T07:25:52Z (fetch_log.txt), before this file was written. What this prereg freezes is the judging rule below, which is the bank's text verbatim and was fixed by the assignment of this run before any fetch, and the list of checks and the drop rule, before this run's own checks, negative controls and receipts produce any output.

## Criterion (verbatim, partial win p1 of the bank entry)
p1: A new rank for a format with 17 <= max(n,m,p) <= 32 (outside Perminov's 16x16x16 table but inside the Lille catalogue): an exactly verified scheme whose rank is strictly below the live fmm_sota.json entry and the live Lille per-format page for that format, and not a plain composition already listed in the Lille 'construction' column.

(The main criterion needs max(n,m,p) <= 16; <30,31,31> has max 31, so only p1 is in play.)

## Object and statistic
- Object: u.txt, v.txt, w.txt (rational coefficients as exact strings) for the format <30,31,31> (A 30x31, B 31x31, C 30x31); each file may be stored as parts of under 1 MB.
- r = number of terms whose three factors are all nonzero, counted by the checkers; every term must have three nonzero factors (a term with a zero factor is a defect, not a free term).
- Checks that must all pass:
  1. the sha256 of the joined u, v, w equals the values recorded in CLAIM.md and run_checks.sh;
  2. a standard-library-only exact checker (check_brent_stdlib.py, the 18x18x19 package's checker, unchanged): every Brent equation sum_k u_k[i,j] v_k[j',l] w_k[i',l'] = [j=j'][i=i'][l=l'] over Q after an explicit integer scaling, for all 831168900 index triples (stored and zero);
  3. three random exact evaluations C = AB (in that checker and in the second one);
  4. a second exact checker (check_exact_np.py, numpy; the version shipped here has an exact Python-integer path for terms too large for float64, tested against the <18,18,19> negative controls, see RECEIPTS.md) agreeing with the first;
  5. negative controls: both checkers must reject a copy with one term deleted and a copy with one coefficient changed;
  6. rebuild from LITA's published 31x31x31_r13433.npz with the pipeline in how-we-built-it/ and a comparison with object/ (the only rebuild of the band run; the claim's rebuild step is a first reproduction).
- Any failure or disagreement kills the object.

## Bar and threshold
- bar = the minimum, over the format <30,31,31> AND its permutations, of: the fmm_sota.json rank (sedoglavic/fmm_digest), the Lille index row and the Lille per-format pages, matmulcatalog docs/catalog.json (every scheme listed for the format) and generated/COVERAGE.md, Perminov's docs/ranks.md (and docs/additions.md, README and the repository tree), MerlijnW70 fmm-schemes, khoruzhii/lita's scheme listing, every pull request of elder-plinius/V3R1T4S (open and closed) and every merged known-knowns entry that gives a rank for this cell, and the two arXiv API queries of the sibling claim. Each source fetched once, live, timestamped UTC.
- Threshold: r <= bar - 1 (strict). r == bar is a tie and not a win. Per kit/POLICY.md, an equal or better value public before filing means not new.
- For p1 literally: r must be strictly below the live fmm_sota.json entry and the live Lille per-format page, and not a plain composition already listed in the Lille 'construction' column.
- Drop rule: if any source lists a rank at or below r for this cell, or the Lille construction column lists r itself as a plain composition, this cell is not built into a claim and is reported instead.
- One cell per claim: <30,31,31> only. The sibling cells of the band are not part of this claim.

## Null design
null_test: not needed because the claim is an explicit object checked by deterministic exact checkers against a table value (no search statistic, no chance baseline).
