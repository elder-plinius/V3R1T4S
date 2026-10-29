# How we found it (contributor text, unverified)

The previous run generalised Construction X tails on nested one-point Hermitian codes over GF(9): a tail of l
columns is any l linear functionals on C(D,bP)/C(D,aP), i.e. points of a small projective space, and the code reaches
distance D iff every hyperplane holds few enough of them, with the bound for each hyperplane read off an exact table
of coset minimum weights. That search printed a valid 5-column tail for C(D,17P) ⊂ C(D,21P) at D = 10, but the run
ended before the code was built.

This run built that code from the printed solution and computed its minimum distance exactly with two independent
programs (a subset test on the generator side and the smallest dependent set of parity-check columns): d = 10, one
above the table's 9. An independent rebuild from the construction text gave the same matrix. It then went to a
three-skeptic panel, one skeptic at a time, each of which wrote its own checker first. The cell and all pull requests
were re-checked just before packaging.

What failed in the same family this run: no 5-column tail exists for C(D,17P) ⊂ C(D,22P) at D = 10 (no [32,20,10] from
that pair; exhaustive), and 18 other low-distance nested pairs gave nothing new beyond a [30,20,8] lead.
