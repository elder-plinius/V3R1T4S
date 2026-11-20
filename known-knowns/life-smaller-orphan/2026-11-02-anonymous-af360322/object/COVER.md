# Cover argument
For h = 5 the target column 4 (0-based) has 5 cells, so it takes one of 2^5 = 32 values. Cube v fixes that column to
value v with 5 unit clauses on the column's target variables and leaves everything else as in the unsplit formula.
Every 5 x 8 target lies in exactly one cube, so "all 32 cubes UNSAT" equals "the unsplit formula is UNSAT", that is,
no 5 x 8 target lacks a predecessor. The same holds for 5 x 7 (column 4), 5 x 6 (column 3) and 5 x 4 (column 2).
certificate.tsv lists one row per cube; encoders/ holds the encoder sources that generate each cube.
