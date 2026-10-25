# How we found it

contributor text, unverified

This is a short account by the contributor. It is contributor text, unverified.
The checks that can be re-run are in `verify-it-yourself/`. The saved full
counts are quoted in `panel/`.

A396618 asks how many n-digit squares have no proper decimal suffix that is
itself a square. The published b-file stopped at a(21). Two counters were
used. One walks every k in the n-digit range and tests suffixes with an exact
integer square root. The other, used from a(24) on and checked on the earlier
terms, replaces most suffix tests by the condition that a square root of the
suffix is congruent to plus or minus k modulo 5^d. They share the definition
and not the code.

a(22) and a(23) came from the table counter and were repeated with the
square-root counter. a(24) and a(25) came from the 5-adic counter and were
repeated with the square-root counter. A bug that stopped the 5-adic integer
square root at 40 bits showed up because a trial a(25)/a(24) was near 1.75
instead of near the square root of 10; the corrected counter was the one
whose parts add to the value in the object. The research rule was that a
term is kept only when a verifier exits 0, or, for the long split runs, when
the saved part-totals add to the claimed value.
