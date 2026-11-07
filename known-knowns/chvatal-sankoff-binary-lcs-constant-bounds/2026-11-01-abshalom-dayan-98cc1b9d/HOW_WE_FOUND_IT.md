# How we found it (contributor text, unverified)

The same contributor's earlier local result used window 16 and a state format that stopped there. The question here was whether window 17 or 18 could be built in 3 GB of memory. The old producer needed a pending bitmap and 8-byte values, so a new one was written: a sparse two-level state set, one dirty byte per chunk, 2-byte offsets from the estimator during search, and potentials spilled to disk where no random access was needed. It reproduces the N = 16 files byte for byte, with the final code.

State counts and memory were measured first. At N = 17 a near-tie width of 0.005,0.005 stopped itself at a 2600 MB guard; 0.005,0.003 fit, with a peak of 2.54 GB. N = 18 did not: the search alone reached 1,273,109,560 states at the narrowest width tried, and the next stage needs about 7.4 GB by estimate, so work stopped there. Widths under 3 GB between those two are untried, so 0.794665 is not the limit of N = 17.
