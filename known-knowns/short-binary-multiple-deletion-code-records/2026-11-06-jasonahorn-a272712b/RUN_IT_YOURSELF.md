From this folder, in a fresh shell:

sh verify-it-yourself/run_checks.sh

Expected last line: PASS
Expected earlier lines: size=43 and max_lcs=12

The object is object/code.txt, 43 lines, each 16 characters of 0 and 1.
sha256 a272712b10be2718ba8ef2024f38207d4aa2d66ed36c29f56db9a2e2185499bb

To rebuild the check, use only the Python standard library. Pairwise longest common subsequence must be at most 12. A one-character change that creates a shared length-13 subsequence must fail.
