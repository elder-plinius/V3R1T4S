# How we found it (contributor text, unverified)

The plan (PREREG v1, frozen 2026-11-04 before any row-29 output was scored):
two independent broken-profile DP runs — left-to-right row sweeps over 22
proven primes > 2^61 + 3e6, right-to-left sweeps over 22 disjoint primes >
2^61 + 103e6 — with the rigorous anchor T(29,k) <= 3^(29k) (each scanned
cell has at most 3 continuation choices), full reproduction of the 378
published cells as a gate, a fresh-prime spot check, and the frozen growth
test on the rows-26/27 fit. The two runs finished on 2026-11-08 after a
week of RAM-window scheduling (width-28 sweeps need ~3 GB and the machine
idles at 92-94% load; a sliced two-half layout and a one-worker-at-a-time
supervisor carried the arc through).

The honest story of this package is its THREE panel rounds. Round 1 (claim:
all 28 row-29 cells): reproduction and criterion passed; novelty FAILED —
five cells (k=1,2,3,4,7) were already published as terms of the column
sequences the A210662 entry itself cross-references, which the row-28 arc's
earlier novelty check had under-examined (its column fetches were
Cloudflare-challenged HTML pages that looked like data). Round 2 (claim:
the 23 remaining cells): novelty FAILED again, deeper — the entry's FORMULA
line maps columns 8-11 to A033511..A033514 (their b-files contain the (29)
terms), and columns 5-6 follow mechanically from published generating
functions. Round 3 (claim: the 17 cells k=12..28, "beyond the published
columns"): all three panelists passed — novelty with a structural proof
that no width-12+ column sequence exists (all 16 OEIS sequences referencing
A210662 enumerated; the sequences that would have to hold these cells do
not exist). Each narrowing is documented in PREREG.v2/.v3 (no threshold
moved; the two-run gates always verified all 28 computed cells).

The same finding reaches our open PR #960 (row 28): its cells k=1..11 are
published-or-derivable the same way. That disclosure is being made to the
maintainer separately.

What worked: the panel system doing exactly its job (three fresh contexts
beat one tired author's blind spot, twice); frozen formulas copied
symbol-for-symbol (a re-derived growth fit silently gave a different
constant); per-cell CRT coverage checks (file-level moduli lie about
partially-swept widths); and the published column values matching our
computed cells — eleven free external confirmations of the arithmetic.
