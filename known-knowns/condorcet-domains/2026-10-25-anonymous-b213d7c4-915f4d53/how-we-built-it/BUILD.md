# Construct or search the explicit object

Source input (public third-party assignment, not bundled):
https://github.com/psmoros/V3R1T4S/blob/abc5220fd79f75651d5faadb71df365566201121/known-knowns/condorcet-domains/2026-10-18-psmoros-bfb22498/object/n24_assignment.txt

Input SHA256: bfb224984f1f45bf52635b80f73a5cd237736940c0d9a0804f029988df6ccc2e. Obtain that public file as SOURCE24.txt and verify its hash. From this package root:

    python3 how-we-built-it/generate.py SOURCE24.txt how-we-built-it/completion.txt regenerated.txt 24 11

The result must have SHA256 915f4d534bc6a8557649f3b02bf4ed21d8782ce01a450c2c39c53c25751d508b and equal object/assignment.txt byte-for-byte. This reconstruction performs no search.

The native deterministic search can be rebuilt with a C++17 compiler:

    c++ -O3 -std=c++17 how-we-built-it/code/pairsearch.cpp -o pairsearch
    mkdir search-output
    nice -n 10 ./pairsearch 24 SOURCE24.txt 10 search-output 240 180248340

The search argument 10 is zero-based clone alternative 11. The initial threshold 180248340 is a prior same-run carrier; the search needs only a strict improvement and has a 240-second cap. A cap is not an exclusion certificate. Exact object verification is independent of search reproduction. Native counts use unsigned128, sufficient for 25!, and the object verifier uses Python arbitrary integers.
