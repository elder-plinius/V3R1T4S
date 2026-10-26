# How we found it (contributor text, unverified)
The run looked for symmetric codes. Fix a group G of coordinate permutations (here Z_5 rotating each of the two halves of
a length-10 word simultaneously), list every GC-content-5 word, keep one representative of every G-orbit whose words are
pairwise at distance >= 7, join two orbits when all their words are compatible, and search for a maximum-weight clique
(weight = orbit size). For (10,7) there are 36,648 such orbits and 136,278,580 compatible pairs; a 600 s branch and bound
found a clique of 12 orbits (four of size 1, eight of size 5) = 44 words. What failed: random orbit sampling and plain
local search in earlier runs stayed below the table; exact cyclic codes of two orbits at (17,13) do not exist.
