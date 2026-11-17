Prerequisites: POSIX sh, python3 (>= 3.9, standard library only), and g++ (with C++17 and -fopenmp support).
Command: sh verify-it-yourself/run_checks.sh
Expected output: PASS (on the final line, exit code 0).
Expected runtime: ~38 seconds wall clock (~122 MB peak RSS; runs check_table.py, a frontier mutation check, and both independent C++ solvers from scratch).
Failure mode: Any discrepancy in row count, formatting, analytical vertex/edge DP identities, literal BFS game evaluation, published Table A1 / OEIS benchmarks, frontier winner values, or fresh recomputation by either C++ solver prints a diagnostic error followed by FAIL on the last line and exits with non-zero status.
