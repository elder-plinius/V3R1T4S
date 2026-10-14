A proposed A(34,8,7) ≥ 603 certificate passes exhaustive mathematical checks and three separate fresh-context reviews (REPRODUCE, NOVELTY, CRITERION). Its SHA-256 is 18b44fac5d5ff1d4895fd9de1240669eb71543b3e15599f7f864e090aa1491ad.

The primary table was fetched once on 2026-10-14 at 03:17:23 UTC, HTTP 200. Its cell remains 601–1175. Raw response evidence and exact hashes are preserved.

Two matters need maintainer review:

1. `kit/check_run.py` flags standard C++ `#include <unordered_map>` and `#include <unordered_set>` as unfilled placeholders. The attached proposed patch exempts only recognized standard-header operands in actual C++ include directives while preserving placeholder checks elsewhere and all leak checks. It passes 25 independently frozen regression cases, both acceptance-enlargement witnesses, the reproduced digit-separator regression, and the repository's 39 original tests.
2. The construction was produced under a preserved JSON contract fixing the code parameters, minimum 603 words and exact checker. Archive metadata supports its pre-result ordering. A complete original dated `PREREG.md` with the required null declaration is not available. The retrospective explanation is labeled explicitly. Please determine whether this original external-construction contract is acceptable provenance for this deterministic existence certificate.

No retroactive preregistration or upstream checker adoption is claimed. The proposed package remains PROMISING until these matters are resolved.
