contributor text, unverified

The live table listed (25, 651) at cosine 0.245484258816, attributed to Azmi C. Özgen, 2026, with no proven-optimal mark and no needs-more-optimization label. The posted coordinate file reproduces that cosine to about 9e-13 and has only 14 digits, so it is not itself an improvement.

A LogSumExp polish of those posted points, already checked on 2026-10-22, had mpmath maximum 0.24269127947873630083715492763900551603445684936698. This run continued that file at inverse temperatures 1e7, 3e7 and 1e8. The first two steps raised the float64 maximum. The beta 1e8 step lowered it by 2.571617e-8. mpmath at 50 digits then reported 0.24269125376256213554570755018269336149252422485568, which is 0.00279300505343786445429 below the printed cosine. A Decimal check at precision 50 printed the same 50 digits.

A tangent push of the worst pair, a replacement by the negative neighbor sum, and thirty random replacements of that point all failed to lower the maximum. The code is not antipodal, not a tight frame, and 0.0464 above the Welch floor. No algebraic match to the table cosine was available, because the gap is 0.002793, not 1e-12.

The same day's refetch of the index and the plain file left the cell unchanged.
