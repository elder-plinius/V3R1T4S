# HOW WE FOUND IT (contributor text, unverified)

The brief: beat one cell of Packomania's circles-in-a-circle table with a construction a
stranger's computer can check. A charter seeded at random (categories number-hunts and
packings-physics) had picked this table as its top quarry; the previous night's run had shown
that rotated triangular-lattice windows lose to the three largest rows it tried (N = 2000, 4495,
5000) by 1.6e-5 to 6.5e-5 — those rows are genuinely optimized.

What worked: reading that result as "some rows are optimized, but are they ALL?" The table has
135 sparse "gap value" rows above N = 2600. One cheap sweep — twelve windows per row
(4 orientations x 3 offsets, spacing fixed in closed form by scale invariance, s* = 2/(1+2
rho_N)) — took two seconds to price every row. 128 of them were optimized like their famous
neighbours. Two were not: N = 3307 (+4.4e-6) and N = 4141 (+7.7e-6) sat BELOW the best plain
lattice window — raw-seed rows that nobody had circled back to. A full 601-orientation x
36-offset grid confirmed both, and exact 60-digit evaluation of the saved coordinates (and,
later, two independent panel checkers reproducing it through 80 digits) settled the margin six
orders above the claim threshold.

What failed on the way: phyllotaxis spirals (2-3e-3 below the table everywhere), and five
families of local and structural search on the jammed N = 2000 row — the big optimized rows do
not fall to grind, only the neglected cells do. The 2026-10-15 run had already spent its whole
budget learning that; this run spent two seconds of the same machinery on the cells nobody had
priced.

The claim is one cell (N = 4141, the larger margin); N = 3307 is documented in the run record
for its own claim. The verification chain: closed-form estimate -> exact r* from the submitted
strings (decimal 60) -> three-skeptic panel (mpmath and big-integer-exact independent
reproductions, live-table re-fetch, clause-by-clause criterion audit) -> this package.
