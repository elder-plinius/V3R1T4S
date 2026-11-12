# How we found it (contributor text, unverified)

The field review of 2026-10-21 left a fast CUDA all-pairs relaxation engine (one configuration per thread block,
FP32 Barzilai-Borwein descent, FP64 energies). Run 2026-10-21-2021 seeded three greedy basin-hopping chains with the
posted CCD Riesz s=1 N = 743 file: each iteration perturbed it 3,360 ways (relocate a few points at random, jitter the
rest) and relaxed every copy on the GPU, about 16 seconds per iteration. All three chains went below the merged #125
value within 3 to 8 iterations, each into a different basin; chain C (larger jitter) found the lowest. A 30-digit
mpmath judge written from the bank definition (tangent Newton, Hessian with rotations projected out) certified it.

The first panel failed it on one misreported number: the claim sentence quoted the gradient norm at an in-memory point
(4.47554e-24) instead of the saved file (about 4.48e-24). Run 2026-10-22-0154 re-fetched every table (byte-identical),
re-ran the judge on the saved file, corrected the sentence and ran a fresh three-skeptic panel.

What failed: greedy acceptance stalls (30 more iterations from the best basin found nothing lower); random starts are
far above the table.
