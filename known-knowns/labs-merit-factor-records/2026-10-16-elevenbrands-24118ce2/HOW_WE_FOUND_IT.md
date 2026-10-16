# How we found it (contributor text, unverified)
The first real run on this target assembled the baseline from Table 3 of arXiv:2607.09688v1 (35 hex-encoded records,
all re-decoded and matched to their printed merit factors), then treated the records as specimens. Neighbouring records
turned out to be end extensions of one another, so an exhaustive scan applied every small end extension, interior
insertion and deletion to every record. At 33 of 35 lengths the best result only tied the published record; at
L = 463 the L = 461 record with one symbol added at each end gave E = 14047 against the published 14439 (and at L = 464,
a separate unclaimed cell, 14396 against 14436). A warm-started tabu search ran alongside on 8 lengths.
