# PREREG.v2

frozen_at: Fri Oct 23 13:30:28 UTC 2026
replaces: the object rule of PREREG.md only. Criterion, statistic, thresholds and null design are unchanged. The LogSumExp file is scored in mpmath only after this stamp.

target: spherical-codes-cohn-table
cell: (25, 650) only.

criterion verbatim:
Success means N vectors in R^d for a (d, N) row present in the live https://spherical-codes.org/plain, coordinates given to >= 20 digits, such that after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal cosine for (d, N) re-fetched live immediately before claiming, by at least 1e-10, AND on the live HTML index https://spherical-codes.org/ the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs more optimization' (improving an entry the table itself flags as unconverged is partial win p2, never a claim), AND the row is not superseded by a newer arXiv result for the same (d, N) (search arXiv for 'spherical code' / 'Tammes' and N), AND the result is not a kissing-number configuration (if 9 <= d <= 23 and c* <= 0.5 the claim belongs to the bank target kissing-number-low-dim and is not counted here). Uploading to /upload-code is an external submission and is never done without explicit permission from the human; the claim is for the verified code.

statistic: c* is the maximum of the N(N-1)/2 pairwise inner products after each vector is divided by its Euclidean norm in mpmath at mp.dps = 50. Direction is down. The table cosine is the third comma-separated field of the live /plain row d=25, N=650, recorded at Fri, 23 Oct 2026 13:25:03 GMT as 0.242872702057. delta = c_table - c*.

thresholds:
- delta >= 1e-10
- every coordinate token has at least 20 significant digits
- HTML cell for href="/data/25/650" contains no '&ast;' and its reference cell does not contain 'needs more optimization'
- d=25 is outside 9..23, so the kissing-number handoff does not apply
- a tie (delta < 1e-10) is not a record

object rule: the LP minimax polish of PREREG.md was stopped after about 15 minutes without one accepted step, so output/polished_650.txt does not exist. output/lse_650.txt, a LogSumExp ladder (code/lse_650.py, betas 3e5 to 3e8, 20-minute cap) started from output/650_deleted.txt, replaces the deletion file only if its mpmath c* is strictly smaller and it passes the same checker. Otherwise output/650_deleted.txt is the object.

null design: none. The accept/reject rule is the deterministic inequality above.

null_test: not needed because an explicit point set is accepted or rejected by a deterministic mpmath checker against the fetched table cosine, not by a search statistic
