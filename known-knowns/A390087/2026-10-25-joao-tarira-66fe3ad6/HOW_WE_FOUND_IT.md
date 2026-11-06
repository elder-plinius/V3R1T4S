# How we found it

contributor text, unverified

This is a short account by the contributor. It is contributor text, unverified.

A390087(n) is the first odd interval, of half-width n in the index, whose longest irreducible odd zero-sum subset has length 2n. The published data stopped at n = 7, k = 30. The even and odd upper bounds n(n+2)/2 - 1 and (n-1)(n+3)/2 gave 39 and 48 as targets, and both were achieved.

The search walks odd magnitudes downward and assigns each one to the positive side, the negative side, or neither, with the subset-sum intersection kept trivial until the last element. Three separate programs (a C search, a C bitset search with sign symmetry, and a C++ bitset search without that symmetry) were compared on overlapping ranges, including equal node counts where the ranges matched. The witnesses themselves were also checked by listing every subset, which does not use the subset-sum pruning.

a(8) = 39 was kept when the length-16 search returned NONE through magnitude 75 and FOUND at 77, and the longer lengths through 38 were NONE for magnitudes up to 77. a(9) = 48 was kept when length 18 was NONE through magnitude 93 and FOUND at 95, and lengths 20 through 48 were NONE through magnitude 95. That is what forces A390085 to stay at 7, then 8, then 9 on the indices in the object.
