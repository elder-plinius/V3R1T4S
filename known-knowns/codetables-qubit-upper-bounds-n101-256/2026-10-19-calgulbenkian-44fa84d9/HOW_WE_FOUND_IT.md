contributor text, unverified

# How we found it

Found on 2026-10-18 by the contributor's team (an AI search agent, Gemini "Argon"). For cells just above n = 100 whose live upper bound equals the propagation closure, the program in `how-we-built-it/` ran a phase-1 simplex for the quantum weight-enumerator LP with shadow rows at the excluded distance, took the row duals when it was infeasible, rationalised and repaired them exactly, and kept the cell only if its own integer checkers accepted the certificate and the LP was feasible at the live lower bound. The snapshot holds no pre-registration.
