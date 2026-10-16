# How we found it (contributor text, unverified)

Brief: the fleet's night run (2026-10-14) swept every posted scu<N>.txt in scu_coords.tar.gz against radius.txt (bank partial win p3) with mpmath at 50 digits. About a third of the rows miss by 1e-14 to 1.5e-12, consistent with 12-digit coordinates; we ignore those. N = 83 (-7.19e-7) and N = 507 (-3.76e-6) were the two outliers at the 1e-6 level. The day run (2026-10-15) then polished the posted files with an SLP compressor; the polish stalls about 7.17e-7 (N = 83) and 3.63e-6 (N = 507) below the cell, so the gap is not under-convergence of the posted file.
What failed: the day hunt (1228 trials over 166 N) found no record anywhere.
