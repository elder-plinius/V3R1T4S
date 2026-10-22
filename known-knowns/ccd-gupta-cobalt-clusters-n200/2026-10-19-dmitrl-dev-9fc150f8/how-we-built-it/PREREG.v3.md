# PREREG.v3 (changed plan during part B; PREREG.md and PREREG.v2.md unchanged)

Reason: lens 1 (neighbour seeding from E_best(N+-1)) found no gain for N = 83..200; lens 2 (monotonic basin hopping,
250 steps per size, N = 200..182) accepted 0 moves at every size and was stopped. Common-neighbour analysis shows that
7 of the 10 Co.zip improvements (95, 101, 113, 121, 122, 196, 198) replace a table structure with ~37% 422 pairs and
~6% 555 pairs by a decahedral one (33-45% 421 pairs, ~1% 555). Lens 1 seeds only from E_best(N+-1), which is a
non-decahedral table structure for most N, so it never propagates the decahedral family more than one atom.
Lens 3 (written before it runs): decahedral family propagation. From each decahedral Co.zip structure
(95, 101, 113, 121, 122, 196, 198; and the decahedral table/Co.zip 197, 200), grow greedily (+1 atom per step: every
surface hollow site above a triangle of mutually bonded surface atoms, quick relax, keep the lowest) and etch greedily
(-1 atom per step: every atom with coordination < 10), up to 6 steps each way, without crossing into another seed's
size. Each family member is compared with E_best(N); any gain > 1e-5 eV is saved and goes to part C. Same potential,
same budget rule (part B total <= 2 h wall from 04:02Z, <= 2 processes, stop if free memory < 15%).
null_test: not needed because the claim is an explicit object (coordinates) checked by a deterministic checker against a table value
FROZEN 2026-10-19T04:28:24Z
