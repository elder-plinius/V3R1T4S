# How we found it (contributor text, unverified)

Brief: the V3R1T4S bank target "site-percolation-2-uniform-lattices-thresholds" asks for site thresholds of the 20
two-uniform lattices in Wikipedia's "Percolation threshold" table, beyond the 4-digit values of Neher, Mecke and
Wagner. Its partial win p2 asks for an independent 7-digit determination of a "citation needed" bond value in the
same table. Row #22's bond value, 0.44528611(40), carries that tag. The run froze its reading of the criterion
(PREREG.md, 2026-10-16T03:03:58Z) before computing anything: p2 needs a stated sigma of at most 5e-8.

What worked: each row of the table that is a strip tiling can be written as a word of gaps between rows (T = a strip
of triangles, S = a strip of squares); the word TSS gives exactly row #22's vertex fractions and z-bar. Two separately
written transfer-matrix programs (a C++ slot/operation code and a C code that takes any torus graph) solve the
eigenvalue form of the Jacobsen-Scullard critical polynomial on W x infinity cylinders. The C++ code reproduces the
exactly known cases (square bond 1/2, triangular bond 2 sin(pi/18), triangular site 1/2) at every W tested; both
reproduce Scullard and Jacobsen's kagome roots to a few times 1e-15 and, through the same extrapolation, the
elongated triangular bond threshold to 3.9e-9. The two programs agree on the TSS roots to 2e-15 for W = 2..10. A
three-point power-law fit on W = 8, 9, 10 gives 0.445287065459697.

What failed or limited it: the frozen rule-4 error bar turned out to under-cover on lattices with known answers (by
up to 2.87 times on square site), so PREREG.v2, written after the results existed, widened it (only upwards) to
2.093e-8. A second orientation of the cylinder reached only three sizes, so it is a diagnostic, not part of the value.
On the neighbouring row #23 (word TSSS) the root sequence turns around near W = 7 and the rule-4 fallback applies;
row #22's last four roots are monotone with shrinking steps. After the panel, a leaner code reached W = 11 and moved
the estimate by -5.5e-9 (gate.md), well inside the bar; that value is not part of this package.
