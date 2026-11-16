# How We Found It

_Note: contributor text, unverified._

1. **Symmetric split barrier (`flip-graph-rank25`)**: Every symmetric `32`-AND Karatsuba-Schoolbook split on `GF(2^7)` modulo `x^7 + x^4 + 1` suffers heavy post-reduction column density (`>= 87` gates), explaining why symmetric polynomial-split pipelines stalled above CMT's `84`-gate `40`-AND circuit.
2. **Non-symmetric, field-reduced `34`-AND bilinear decomposition (`algebraic-bilinear-slp`)**: Optimizing directly over the reduced field tensor modulo `x^7 + x^4 + 1` (`gf2m_deep_hunter.cpp`) discovered a non-symmetric `34`-AND basis (`6` A-input XORs + `7` B-input XORs, spanning `10` of the `13` unreduced degree slots) whose `7 x 34` reconstruction matrix has `55` ones (`8` multi-bit columns) and synthesizes at its exact layered floor **`82` gates** (`34 AND + 48 XOR`, depth `6`).
