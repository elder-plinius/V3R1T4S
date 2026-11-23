# How we found it (contributor text, unverified)

An evening agent run audited both CCD glue tables (2026-11-21) and noticed that deleting atoms from some posted lead
minima gives structures below the rows for N = 119 and 120. Those deletions are trivial edits, so they were not claimed.
On 2026-11-22, 120 s of basin hopping from every posted Pb file lowered N = 121 by 0.0296 eV (a two-atom relocation,
so not new either). 300 s more basin hopping from that structure (seed 11) dropped to -198.47902916627 eV. Seven atoms
moved more than 0.5 A from the posted 121; three of them by 4.6-7.4 A.

What failed: an Al N = 146 candidate the day before turned out to be a single-atom relocation of the posted structure,
so this time we computed blind bars first (random 2- and 3-atom relocations of posted 121, all deletions of posted
122 and pairs of posted 123, additions to posted 120: 55,625 relaxations; none came within 0.228 eV of the object).
The NOVELTY panelist ran 129,675 relaxations of its own with the same outcome. Basin hopping from the same motif at
N = 124..126 ended above the table, so the motif's advantage seems confined to roughly N = 118..123.
