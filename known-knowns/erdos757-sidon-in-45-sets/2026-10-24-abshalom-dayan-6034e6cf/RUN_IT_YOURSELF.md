# Run it yourself

From this folder, in a fresh shell (python3, standard library only, no network):

    sh verify-it-yourself/run_checks.sh

Expected output (see verify-it-yourself/RECEIPTS.md for a real run): a calibration line for the A.P.-hypergraph of the
paper's 14-point set A_base (n 14, m 12, every property True, alpha 8, OK), then for object/H.json n 101, m 99 and every
property True (three_uniform, edges_distinct, linear, middles_distinct, middles_not_first_or_last, m_at_most_n_minus_2,
f7_free), then `alpha 56 claimed 56 ratio 56/101 below 5/9: True below 4/7: True at least 9/17: True`, and a last line
`PASS`. Under a second on a laptop.

A second, solver-based check (CP-SAT optimum, a SAT solver's UNSAT answer for an independent set of size 57 (no certificate is saved), a
comparison with the alpha_dp value stored in H.json, and F7 by two searches; needs the pinned packages in how-we-built-it/requirements.txt):

    python3 -m venv .v && .v/bin/pip install -r how-we-built-it/requirements.txt
    .v/bin/python how-we-built-it/code/check_p2.py object/H.json        # last line P2_CHECK: PASS

To rebuild the object from the 13-vertex block in object/construction.json (gluing 9 copies on 2 vertices each):

    mkdir -p out
    .v/bin/python how-we-built-it/code/chain_build.py "$(python3 -c 'import json;print(json.dumps(json.load(open("object/construction.json"))["block_edges"]))')" 13 6 8 8

It prints n, m and alpha for K = 0..8 (n = 13 + 11K, alpha = 8 + 6K) and writes out/chain_K8.json, whose n and edges
equal object/H.json. To rerun the search that found the block (CEGAR in CP-SAT, 15 to 80 seconds):

    .v/bin/python how-we-built-it/code/cegar.py 13 6 1 6 8 280

Its last line is `RESULT FOUND ... g 6 ratio 6/11 edges [...]`. CP-SAT runs multi-threaded, so the block it returns
can differ from run to run. A rerun on 2026-10-24 returned a different 13-vertex block with the same transfer matrix;
its 9-copy chain also has n = 101 and alpha = 56 (check_p2.py: CP-SAT OPTIMAL 56, SAT UNSAT at 57, P2_CHECK: PASS).
The standalone checker's alpha DP uses a greedy vertex order, which is fast on object/H.json but did not finish in
90 seconds on that other chain, so use check_p2.py for blocks other than the one in object/.
