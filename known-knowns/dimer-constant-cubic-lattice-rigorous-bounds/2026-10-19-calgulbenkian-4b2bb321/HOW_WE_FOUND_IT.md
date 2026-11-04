contributor text, unverified

# How it was found

The first step of the work was to reproduce He's Table 2 independently, to be sure the implementation matched his definitions before pushing it further. The contributor's team wrote an exact-integer C solver and then the package builder wrote a second, standalone Python checker plus a C section checker written from the definition. All 12 entries, (2,2) to (6,3) at p = 4 and (5,5) at p = 2, come out equal to He's published values after rounding up to six decimals. The author's results note had two wrong ten-digit figures, for (5,4) and (6,3); they were found during checking and do not change the six-decimal values.
