# Commands that built the objects
Requires Python 3 with OR-Tools (tested with ortools 9.15) and fjsspw_check.py from verify-it-yourself/ next to the solver.

    python3 solve_hier.py <instance>.fjs <UB> 30 4 <instance>.json     # 30 s, 4 search workers

solve_hier.py: one interval per operation, an optional interval per eligible machine and per eligible (machine, worker)
pair, no-overlap per machine and per worker, job precedence, a redundant cumulative of capacity min(machines, workers),
minimise makespan. CP-SAT is multi-threaded, so a rerun can give a different schedule of similar makespan.
solve_flat.py is the first, weaker formulation (makespan capped at UB - 1), kept for the record.
