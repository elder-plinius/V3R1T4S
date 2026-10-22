# PREREG: spherical-codes-cohn-table (run 2026-10-16-0024)

frozen_at: 2026-10-16T00:45:04Z (date -u, before any lens output exists)

## Criterion (verbatim from bank/targets.json)
Success means N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates given to >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs more optimization' (improving an entry the table itself flags as unconverged is partial win p2, never a claim), AND the row is not superseded by a newer arXiv result for the same (d, N) (search arXiv for 'spherical code' / 'Tammes' and N), AND the result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 the claim belongs to the bank target kissing-number-low-dim and is not counted here). Uploading to /upload-code is an external submission and is never done without explicit permission from the human; the claim is for the verified code.

## Partial wins (verbatim)
- p1: A certified improvement (same rule, margin 1e-10, no star, no 'needs more optimization' label) in dimension 3 (Tammes problem) for an N listed in /plain; 3D entries carry no 'needs more optimization' label, so this is the hardest sub-case.
- p2: A batch of at least 20 certified improvements (margin 1e-10 each) to rows labeled 'needs more optimization' in one dimension d in 4..32, delivered as one file set with the largest improvement reported; these rows are flagged unconverged by the table, so the batch is a partial win, never a claim.
- p3: An exact-angle certificate for an unstarred, unlabeled row that has no minimal polynomial listed: a configuration whose minimal-angle cosine is shown (mpmath findpoly/PSLQ at 60 digits, confirmed at 100 digits) to be an algebraic number matching the table value to 1e-12, with the contact structure verified rigid; adds a polynomial the table lacks.

null_test: not needed because every claim here is an explicit coordinate file whose maximum pairwise cosine is computed deterministically (mpmath, 50 digits, all N(N-1)/2 pairs) and compared with a re-fetched table value; there is no search statistic, period, language or "beats chance" claim.

## Exact statistic and checker
- c* := max over i<j of <x_i/|x_i|, x_j/|x_j|> computed in mpmath at mp.dps = 50 from the decimal strings of the
  submitted file (every coordinate written with >= 20 significant digits). Any screen used to find the maximal pairs
  must be provably safe (float64 screen margin >= 1e-7 below the float maximum; all pairs inside it recomputed in
  mpmath). Checker of record: code/sc_check.py (tests in BRIEF.md); every lens also writes its own; the panel writes a
  third.
- gain := c_table - c*, where c_table is the 12-decimal cosine of row (d, N) in https://spherical-codes.org/plain
  re-fetched by the main session at gate time (and the HTML index re-fetched at the same time for stars/labels).

## Thresholds (frozen)
- Full criterion (one row = one claim): gain >= 1e-10; row present in the live /plain; on the live HTML index the row
  has no star and no "needs more optimization" text; (d, N) not in the taken list {(29,114), (30,74), (29,72),
  (28,70), (30,117), (29,145), (26,232), (27,68)}; not (9 <= d <= 23 and c* <= 0.5); c* also below the cosine of
  every public archive found for the row (Vahteristo combined.json at least) by >= 1e-10; no arXiv result for (d,N)
  newer than the table entry with a lower cosine; NOVELTY skeptic finds nothing better.
- p2: >= 20 distinct rows, all in ONE dimension d in 4..32, each labelled "needs more optimization" on the live HTML
  index at gate time, each with gain >= 1e-10 against the live /plain at gate time (rows missing from /plain are
  compared with the index cosine and listed separately; they count only if the CRITERION skeptic accepts the index
  value as the table's), each also below the Vahteristo cosine by >= 1e-10; delivered as one file set with the
  largest improvement reported. Rows that lost the label by gate time but are still beaten are reported separately
  (they would fall under the full criterion and are judged under its rules, one row per claim).
- p3: an unstarred, unlabelled row with no minimal polynomial on the index or in /plain; a polynomial P with integer
  coefficients found by PSLQ/findpoly at 60 digits with (deg P + 1) * log10(max |coeff|) <= 45, P vanishing at the
  100-digit value of the cosine to below 1e-95 (relative), the 100-digit cosine matching the table to 1e-12, and the
  contact graph (pairs within 1e-30 of c* at 100 digits) infinitesimally rigid: the Jacobian of the system
  {|x_i|^2 = 1, <x_i, x_j> = c for contact pairs} in the unknowns (x, c) has rank dN + 1 - d(d-1)/2 at the polished
  point (no rattlers; rattlers make it not rigid and the row is rejected).

## Optimizer sanity control (required before any claim; not a null test)
Every optimizer configuration that produces a claimed code is run with the same settings on starred rows (proven
optimal; 30 on the 2026-10-16 index, use every starred row with d >= 4 and N <= 1024 it can handle, at least 8). A
starred row "beaten" by >= 1e-10 means a checker or optimizer bug: stop and report it; no claim from that
configuration stands.

## What is never done
Uploading to spherical-codes.org/upload-code, contacting anyone, or claiming a row whose comparison came from a blocked
or failed fetch (that comparison is PENDING TABLE CHECK).
