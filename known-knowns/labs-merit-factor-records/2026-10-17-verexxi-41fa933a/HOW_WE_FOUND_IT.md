# How we found it (contributor text, unverified)

The June 2026 record paper (arXiv:2607.09688) improved lengths 450 to 527 partly by taking published sequences of a
neighbouring length and adding or removing one element at an end. Published tables between 121 and 449 are thin, so
we asked whether the same simple edits beat them there too.

We collected every published sequence and value we could read from ten sources, recomputed every energy exactly,
and took the lowest published value per length as the baseline. Then we tried every small end edit (adding,
removing or trimming one to three elements) of the published sequences of nearby lengths, and kept the edits whose
exact energy is below the baseline. Each kept edit was rechecked with a second energy implementation, rebuilt from the
quoted source line, and then reviewed by three fresh reviewers.

What did not work: memetic tabu search seeded from these sequences found nothing below its seeds, and searches from
random starts stayed far above the published values.
