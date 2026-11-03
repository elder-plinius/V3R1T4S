contributor text, unverified

An AI search agent (Gemini, called Argon) worked for the contributor calgulbenkian on the target "entanglement-assisted qutrit code tables with gaps". Its preregistration chose the approach: start from a classical code over GF(9) with a Hermitian hull of controlled size, scale its columns by units of GF(9) to tune the hull, and read off an entanglement-assisted code over GF(3) (the Brun-Devetak-Hsieh reduction). For this cell the code is Punctured Xing-Ling quadratic norm-trace code [33, 6, 23]_9 over GF(9), with column scaling for Hermitian hull h = 3.

Parameters of the result: n = 33, k = 3, c = 24, s = 54 generators, minimum distance d = 23. The agent's verifier enumerated every vector of the symplectic dual; the panel's skeptics checked it again with their own programs.

What failed, what else was tried and how many candidates were scanned are not recorded in the snapshot; the construction script is missing from it (see `how-we-built-it/README.md`). Added 2026-11-03, not contributor text: the structure recovered from the shipped object is a column-scaled evaluation of conics at 33 points of PG(2,9), which does not confirm the "norm-trace" description above; `how-we-built-it/rebuild_eaqecc_33_3_23_24.py` rebuilds the code from that recovered description. Nothing here is a claim about how long the search took.
