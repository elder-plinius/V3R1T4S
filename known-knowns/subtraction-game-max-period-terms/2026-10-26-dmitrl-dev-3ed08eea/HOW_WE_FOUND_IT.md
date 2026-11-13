# How we found it (contributor text, unverified)

AI-assisted work for DmitrL-dev (run 2026-10-26-0708). The bank target subtraction-game-max-period-terms asks for the next
unknown terms of A389689 and A389690, which had not been extended since October 2025. The terms are pure computation:
for every move set S with max S = n, iterate the Sprague-Grundy values until a window of n values repeats.

We first wrote a standard-library reference from the OEIS definition and checked it against the listed terms for small n,
then two faster programs that share no code: a C program with the window in machine words and Brent's cycle detection,
and a Rust program that follows the definition literally (first repeat of the window in a hash map). Both reproduced every
listed term with identical period histograms, so we froze the rule (PREREG.md) and ran n = 23: 3570, attained by
the single set S = {2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23} (the next largest period is 2232). The OEIS entry's own Python program gives the same period for
that set, and a third full pass with the slow standard-library reference over all 4194304 sets gave the identical histogram.
Nothing failed along the way; the computation takes seconds.
