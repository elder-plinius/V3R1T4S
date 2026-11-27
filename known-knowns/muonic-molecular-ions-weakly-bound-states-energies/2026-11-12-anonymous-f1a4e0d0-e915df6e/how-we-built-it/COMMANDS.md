# How the object was built

Requirements: Python 3 with sympy; a C++17 compiler; GMP with its C++ interface (gmpxx). macOS (the engine uses
Grand Central Dispatch for threads).

    python3 gen.py 1 && python3 gen.py 2            # writes elems_L1.h and elems_L2.h (closed-form matrix elements)
    c++ -O2 -std=c++17 engine.cpp -lgmpxx -lgmp -o engine
    python3 opt.py start.json 1 SIGMA 150 0.15 3     # greedy search over the exponent-box bounds at 240 functions
    python3 scale.py boxes.json 1 SIGMA 2 1 512 out  # doubles every box (480 functions), writes out.txt and out.vec

boxes.json is the optimised box specification that scale.py turned into object/basis.txt; SIGMA is a shift just
below the expected lowest root (roots_below_sigma must print 0). opt.py and scale.py expect the engine in
../../evaluator-first/code relative to themselves (edit ENG in opt.py). The exponents are Korobov-style
pseudo-random numbers inside each box (mkbasis.py). object/vector.txt is the inverse-iteration eigenvector printed
by the engine. PREREG.md is the run's frozen success rule. No null test was required (explicit object, deterministic
checker).
