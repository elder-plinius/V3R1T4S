# How we found it (contributor text, unverified)

Brief: Henry Cohn's table of spherical codes was being converged quickly in 2026 (5,637 rows still labelled "needs
more optimization" on 2026-10-16; 4,777 converged rows held Ilmari Vahteristo's 60-second annealing codes). The run
looked for rows where a fresh local search could beat a converged entry.

What failed: polishing converged posted codes in place (they sit at local optima); long random-start anneals within a
night's CPU share; lattice root-system starts; adding a point to an (N-1)-point code; exact-angle (PSLQ) certificates
under a frozen height bound; reconstructions of old Ericson-Zinoviev constructions.

What worked: starting from a NEIGHBOURING row's code. The table's own unconverged (6,527) code, with one point
deleted and the remaining 526 points re-polished (LogSumExp + L-BFGS, then a penalty polish), dropped below the
converged (6,526) entry by 2.06e-4.

Second step (run 2026-10-16-0758): the first code was re-polished in place, starting from the uploaded file, with a smooth-max (LogSumExp) pass followed by a sequential linear-programming polish of the near-contact pairs. That moved c* from 0.786430618545 to 0.786427532330 (a further 3.09e-6). The live table's value for (6,526), 0.786427532331, equals this version's c* rounded up at 12 decimals.
