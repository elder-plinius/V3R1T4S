# How we found it (contributor text, unverified)
We wrote an ITC-2007 exam evaluator from the track specification and checked it against OptHub: it reproduces the
posted best of 19 of the 20 instances on the page (set4's posted file was replaced in storage, V3R1T4S issue #1092).
A simulated annealing over feasible timetables (single-exam moves, Kempe chains between two periods, whole-period
swaps, exact incremental penalties) started from each posted best moved only set4 and set5. On set5 it went from
2,327 to 2,325 in 20 s, 2,312 in two minutes and 2,305 in a further hour at a cool temperature; hotter restarts from
the posted file did nothing. An exact CP-SAT model proved two Yeditepe values optimal and moved none of the others.
