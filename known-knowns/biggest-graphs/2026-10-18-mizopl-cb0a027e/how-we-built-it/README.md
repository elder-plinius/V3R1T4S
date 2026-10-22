# How we built it

- `sa2_opt.c`: Native C bit-parallel BFS evaluator and simulated annealing optimizer with new-vertex screen inclusion and multi-temperature polish rounds (`cc -O3 -o sa2_opt sa2_opt.c -lm`).
- `PREREG.md`: Pre-registration of the target cell `(Delta, D) = (14, 3)` and spare-degree vertex insertion + bit-parallel BFS simulated annealing method prior to running the search.
