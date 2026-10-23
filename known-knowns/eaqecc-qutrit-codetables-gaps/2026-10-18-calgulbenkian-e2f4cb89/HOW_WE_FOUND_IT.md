contributor text, unverified

An AI search agent (Gemini, called Argon) worked for the contributor calgulbenkian on the target "entanglement-assisted qutrit code tables with gaps". Its preregistration chose the approach: start from a classical code over GF(9) with a Hermitian hull of controlled size, scale its columns by units of GF(9) to tune the hull, and read off an entanglement-assisted code over GF(3) (the Brun-Devetak-Hsieh reduction). For this cell the code is Elliptic-curve AG code C_L(D, 8 P_inf) on y^3 + y = x^2 over GF(9), a [16, 8, 8]_9 code, with column scaling for Hermitian hull h = 4.

Note: the curve y^3 + y = x^2 has only 15 affine points over GF(9) (y^3 + y takes values in GF(3), and x^2 lies in GF(3) for 5 values of x, each giving 3 values of y), so C_L(D, 8 P_inf) on it has length at most 15, not 16. The construction description above is therefore wrong as written. The object file is unchanged, and its parameters are established by the checks in verify-it-yourself/, not by this description.

Parameters of the result: n = 16, k = 4, c = 4, s = 16 generators, minimum distance d = 8. The agent's verifier enumerated every vector of the symplectic dual; the panel's skeptics checked it again with their own programs.

What failed, what else was tried and how many candidates were scanned are not recorded in the snapshot; the construction script is missing from it (see `how-we-built-it/README.md`). Nothing here is a claim about how long the search took.
