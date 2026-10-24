# How we found it (contributor text, unverified)
The bank criterion (beat the best ten-fold mean MCC by 0.02) was already met publicly (GENERator 2025), so the run pivoted to an audit. An exact
paired sign-flip test over the 10 per-fold MCC values in benchmark.csv showed that on 6 of the 10 histone tasks the top entry is not distinguishable
from the second. A first script crashed on HyenaDNA rows with 9-14 folds; a preregistered v2 excluded them. A small deterministic CNN was used to
estimate test-sampling noise; the panel did not confirm that part. A k-mer audit found the released splits clean.
