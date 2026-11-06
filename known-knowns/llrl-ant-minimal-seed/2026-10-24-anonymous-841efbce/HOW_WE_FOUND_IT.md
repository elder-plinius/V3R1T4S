# How we found it (contributor text, unverified)
GLR's paper gives the LLRL period-384 highway and a rounded blank onset, but no seeds. We searched over the ant's first
reads with an exact "on the highway at time t" test against the 384 blank-highway phases (hsearch), and re-proved every
value with a second search written separately (a fixed-depth light-cone DFS, lcb/lcb_fast, with its own blank word and
certificate). k = 5 was the hard case: the first run hit a CPU cap; this run split the search into disjoint subtrees,
and sped the second checker up about 5-8x with a trie prefilter over the 384 rotations (exact; same leaf counts).
A third simulator re-checks every minimiser with an exact translate certificate. Three fresh reviewers (criterion,
novelty, reproduce) reviewed the claim; their reports are in panel/.
