"""Run the competition's own validator, unmodified, on one VNN-LIB 2.0 witness.

  python -I official_validate_run.py SCORING_DIR BENCHMARK_VERSION_DIR NETWORK_FIELD PROPERTY_FIELD WITNESS_V2

Calls SCORING/counterexamples_v2.py validate_vnnlib2_counterexample with abs_tol 1e-4 (the competition's
COUNTEREXAMPLE_ATOL) and with 0. Only the result-type names are supplied here.
"""
import sys
from pathlib import Path

scoring, bench, net, prop, ce = sys.argv[1:6]
sys.path.insert(0, scoring)
import counterexamples_v2 as cv2  # noqa: E402


class ResultType:
    CORRECT = "correct"
    CORRECT_UP_TO_TOLERANCE = "correct_up_to_tolerance"
    SPEC_NOT_VIOLATED = "spec_not_violated"
    NO_CE = "no_ce"
    MALFORMED_CE = "malformed_ce"
    UNSUPPORTED = "unsupported"


for tol in (1e-4, 0.0):
    r = cv2.validate_vnnlib2_counterexample(Path(bench), net, prop, ce, tol, 0.0, ResultType)
    print("abs_tol=%g: %s | %s" % (tol, r[0], r[1][:300]))
