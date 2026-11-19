# How we found it (contributor text, unverified)

The brief was a scheduled V3R1T4S run (heavy effort) on the bank target graph-automata-max-period. Earlier runs had
packaged A384209(10), A357953(9), A357952(9) and A357951(8), and A384209(11) was waiting for its panel, so this run
took the next open cell of the neighbours-only sequence, A357953(10). The scout read the OEIS entry: a(1..8) known,
no a(9) or a(10), no pending edit, and no V3R1T4S pull request, code or paper with either.

The plan, frozen in PREREG.md before any n = 10 run: exhaust all 11,716,571 connected 10-node graphs from geng with
two separately written programs (C with a Gray-code rule walk; Go with plain rule order and in-degree peeling),
compare them class by class on counts, histograms, every high graph and a hash of every per-graph maximum, simulate
the witness with a small pure-Python stepper, and check graph counts against A001349. Speed tests on a 1/400 slice put
Program A at about 2 core-hours and Program B at about 12, so the n = 10 work was split into 32 residue classes and run in the
background over several hours; the workers were paused for a while to share the machine with another job and then
resumed.

Both programs gave 624 on the same single graph, I?AAD@oIg with rule {0,2}, far above the next best (470). A
self-break pass (Python over all 1024 rules on a sample of graphs to test the degree restriction, a determinism
rerun, fresh rebuilds) found nothing wrong, and the three skeptics and the honesty gate passed it later the same
morning; the reproduce skeptic recomputed all 32 classes with its own checker.

Side observation (also seen for a(9)): the OEIS example graph listed for n = 8 seems to be the complement of an
optimal graph (it reaches only 10 with the listed rule; its complement reaches 96).
