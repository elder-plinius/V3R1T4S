# How we found it (contributor text, unverified)

The table's notes say its upper bounds above 100 qubits are weak. We asked a simple question: had anyone run the
standard linear-programming bound with Rains' shadow constraints at those sizes?

We built an exact pipeline. A high-precision simplex solver (1536-bit arithmetic with python-flint) runs the program.
When the program has no solution, its dual values become a certificate; we round them to exact fractions, repair them
exactly, and check the result in integer arithmetic. Two separately written checkers confirm each certificate.

Before trusting it, we compared it with the table on 30 random cells between 20 and 100 qubits, where the table's
upper bounds come from the same kind of program, and it reproduced the table every time. Brute-force checks on small
random codes and on well-known codes confirmed the underlying formulas.

What made it work: the shadow constraints, and keeping only the conditions that matter near the distance being
tested (a certificate built from part of the conditions still proves the whole system has no solution), which made
scans up to 256 qubits run in hours.
