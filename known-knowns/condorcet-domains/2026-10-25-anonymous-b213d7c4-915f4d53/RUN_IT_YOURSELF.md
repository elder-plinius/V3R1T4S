# Reproduce from a fresh shell

From this folder run:

    sh verify-it-yourself/run_checks.sh

Python 3 standard library only. Expected exact count is 180870896, assignment SHA256 915f4d534bc6a8557649f3b02bf4ed21d8782ce01a450c2c39c53c25751d508b, and final output PASS. The checker requires every one of the 2300 distinct sorted triples and uses exact integer arithmetic; Fishburn n = 9 and n = 20 and a complete first-nine permutation check calibrate conventions.

The complete object is shipped, so verification needs no download. Reconstructing its construction optionally uses the public source described in how-we-built-it/BUILD.md; that third-party input is not included here.

The independent suffix checker is also run by run_checks.sh. Original panel paths refer to the claim layout; object and supplied-checker mappings are explained in README.md. Reproduction work files referenced by panel/reproduce.md are preserved under panel/reproduce-work/.
