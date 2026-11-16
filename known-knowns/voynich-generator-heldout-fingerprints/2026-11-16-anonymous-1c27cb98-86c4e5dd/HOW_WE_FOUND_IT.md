# How we found it (contributor text, unverified)

The target's outcome (B) asks for a pre-registered falsification of the Naibbe cipher on a
statistic NOT among the known Naibbe failure statistics (edge-glyph coupling, singleton/hapax
rate, the 2604.19762 four signatures, Greshko-2025 limitations). We pre-registered the edit-1
adjacency-similarity ratio H1 (arXiv 2608.17096 Table 4 "Edit-1") as the falsifying statistic,
with a 4000-resample quire-bootstrap 99.9% Voynich envelope as the null. The unmodified Naibbe
procedure (re-implemented token-identical to the pinned driver, 0/90,939 token mismatches) was
run on 20 plaintexts x 10 seeds (10 A-mode + 10 B-mode). The pooled H1 (A 0.7981, B 0.7917)
fell below the 99.9% envelope on all four (dialect x transliteration) cells and below the
minimum of all 16,000 Voynich quire-bootstrap controls. The sign of the effect (Naibbe H1 lower
than Voynich) was already known from 2608.17096's single-corpus 0.82-vs-1.12; the new object is
the pooled, both-dialect, both-transliteration, 99.9%-envelope, 16,000-control falsification.
(The generator outcome (A) and the p1/p2/p3 partial wins were probed separately and came back
negative; see the run's attempts/generator/.)
