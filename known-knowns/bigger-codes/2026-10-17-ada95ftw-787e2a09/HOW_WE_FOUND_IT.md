# How we found it (contributor text, unverified)
Brief: the 2026-10-17 08:02 UTC V3R1T4S run on constant-weight-codes (light effort, about 1 h on 8 CPU cores) tried two lenses.
- What failed: unions of AGL(1,p)-subgroup orbits solved exactly with CP-SAT stayed far below the table's lower bounds (the best was a tie at A(31,10,7) = 62).
- What worked: an exact LP sweep over the inner distribution (Delsarte rows plus per-distance rows a_x <= C(w,x)A(n-w,d,x) with numeric inputs from the live table) over 1305 cells. Floats located optima, and each candidate was then certified in exact rational arithmetic. 14 cells dropped. With a conservative rule against single-value inputs 11 survived; 8 of those were plain Johnson refreshes of stale printed bounds and are not claimed. This cell was one of the 4 genuine LP improvements.
- Three fresh-context subagent skeptics (REPRODUCE, NOVELTY, CRITERION) each passed it; see panel/.
