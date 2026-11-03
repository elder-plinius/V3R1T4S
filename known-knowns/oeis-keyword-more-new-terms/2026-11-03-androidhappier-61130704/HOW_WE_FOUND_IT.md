# How we found it (contributor text, unverified)

A V3R1T4S run took the bank target oeis-keyword-more-new-terms and looked for a cheap cell outside the families
other runs were working on. OEIS A361864 (Gus Wiseman, 2023) counts set partitions of {1..n} whose block medians
have an integer median. It had a(1..11), keyword "more", and no edits since April 2023. Bell(12) = 4,213,597
partitions is small enough for a direct count.

The plan was frozen in PREREG.md before any program was written. It called for a C program over restricted growth
strings with doubled integer medians, a separate Go program that builds each partition from the block holding
the lowest unused element and uses exact rationals, and a Python Fraction brute force as a check on the definition.
All three reproduced the published terms, and C and Go agreed on a(12) = 2092816 within a minute. A self-break lens
tried the wrong median convention as a negative fixture. It failed to reproduce DATA, which shows the checks can
tell the conventions apart. The by-product terms a(13) and a(14) are not claimed.
