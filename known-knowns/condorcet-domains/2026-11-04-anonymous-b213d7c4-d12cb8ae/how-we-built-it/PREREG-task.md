# Binary DAG search
Frozen before output; task starts after exact marginal audit passes. Source SHA
be05fe9ea7f4f6f33777cdf17e1c97d5d6869419838005b0ca949adca6fc2483.
Alternatives SHA5f710c7fab5f7340d71365d52bc625e1474c6d09d71610c34fb4fc32f87cfc79.
Family: exactly the1566 old rows selected by loss<=1000000, each original or
first highest-single-score alternative from old marginal-alternatives.csv;
all other rows original. No claim about other choices or global maximality.

Build one root relaxed prefix DAG; each edge names choices it violates. At every
node exact forward/backward losses give both child bounds simultaneously. If a
choice removes zero currently possible complete orders, fixing that choice keeps
the parent's complete path set, hence dominates the opposite choice. If either
choice's loss is greater than bound-best, it cannot beat best; force the opposite.
Otherwise branch maximizing min(loss0,loss1), then sum. Better-bound child first.
All arithmetic guarded; complete status assignments saved for independent count.
Checkpoint entire pending DFS frontier every100 nodes and at exit, allowing resume.

Nodecap1000000, CPU/wall300s, single CPU NI>=10, full C++ allocations<=512MiB;
run clipped before01:30:44Z. CAPPED/UNKNOWN pending remains OPEN. A clean DONE is
only a single-code operational negative for this selected binary family.
null_test: not needed because results are explicit assignments and exact counts.
