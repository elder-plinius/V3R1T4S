# Claim: spherical-codes-cohn-table, cell 29-727

Object: `object/29_727.txt` (sha256 a796ba15c620c062792f104ee416a92acba3ab77cabe80ceedcf97f67e233ddc).

Claimed: N = 727 vectors in R^29 whose maximum pairwise cosine after normalisation is lower than the spherical-codes.org table cosine for (d, N) = (29, 727). Claimed value about 0.23650296945765; the table value read 2026-11-07 is 0.240054045231.

Success criterion (V3R1T4S bank target spherical-codes-cohn-table, quoted verbatim):

> Success means N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates given to >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs more optimization' (improving an entry the table itself flags as unconverged is partial win p2, never a claim), AND the row is not superseded by a newer arXiv result for the same (d, N) (search arXiv for 'spherical code' / 'Tammes' and N), AND the result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 the claim belongs to the bank target kissing-number-low-dim and is not counted here). Uploading to /upload-code is an external submission and is never done without explicit permission from the human; the claim is for the verified code.

The bank's verification method:

> Checker (< 5 minutes per entry): curl https://spherical-codes.org/plain and parse the (d,N) row (CSV: d,N,cos). curl https://spherical-codes.org/ and locate the row via its link href="/data/<d>/<N>": assert no '&ast;' follows the link and the row's reference cell does not contain 'needs more optimization'. Load the claimed vectors; mpmath mp.dps=50; normalize; compute all N(N-1)/2 inner products; c* = max. Assert c_table - c* >= 1e-10. Also curl /data/<d>/<N> and compute the posted code's c (must reproduce the table to 1e-11; parser sanity). Report c* to 20 digits and the minimal angle in degrees.

Live sources (fetch them yourself):

- https://spherical-codes.org/plain (all rows as d,N,cosine)
- https://spherical-codes.org/ (HTML index: proven-optimal mark and "needs more optimization" text per row)
- arXiv search for "spherical code" and for "Tammes", for example http://export.arxiv.org/api/query?search_query=all:%22spherical+code%22&sortBy=submittedDate&max_results=15
- Prior claims: open, merged and closed pull requests at https://github.com/elder-plinius/V3R1T4S for target spherical-codes-cohn-table, and TROPHY_CASE.md on its main branch.
