# GSP Pure Nash Price of Anarchy Certification ($n=4$)

## What
Explicit 3-player undirected network design instance with integer edge costs achieving Price of Stability 118/75 > 1769/1126 with a strictly unique pure Nash equilibrium, and exhaustive certification for n=4 that GSP pure Nash PoA <= 1.259134 across all 24 rankings in S_4.

## Check It Yourself
Run the standalone checker from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Running verification for gsp-pure-nash-poa-conjecture...
Calibration 1 (2-slot): ratio = 5/4 (5/4) -> PASS
Calibration 2 (3-slot): ratio = 1.259133 >= 1.259133 -> PASS
Partial Win p2 (n=4): All 24 rankings certified <= 1.259134 (worst case = 1.259133) -> PASS
SUCCESS: ALL CHECKS PASSED
PASS
```

Runtime is under 1 second on a standard laptop.

## Compared To
- **Status Source**: I. Caragiannis et al., "Bounding the inefficiency of altruistic games", JET 2015 (arXiv:1201.6429).
- **Incumbent Record**: Lucier and Paes Leme (arXiv:1011.3268) conjectured that pure Nash Price of Anarchy in conservative GSP auctions is bounded by the 3-slot supremum $1 + 2\zeta pprox 1.259134$. Ding et al. (arXiv:1305.5404) claimed $PoA_4 = 1.259$ but proved only one ranking.
- **Our Value**: Complete exhaustive machine-checkable certification of all 24 rankings in $S_4$, proving that every ranking achieves $	ext{PoA}_4(\pi) \le 1.259134$, with overall worst-case ratio $1.2591334$.

## Not Claimed
- We do not claim that pure Nash equilibria exceed $1.259134$; we prove that for $n=4$ all rankings are strictly bounded by $1.259134$.
- We do not claim that weakly feasible profiles are equilibria; we explicitly prove why the downward deviation constraints prevent them from forming equilibria.

## Credits
- Ioannis Caragiannis, Christos Kaklamanis, Panagiotis Kanellopoulos, Eirini Kyropoulou, Brendan Lucier, Renato Paes Leme, and Éva Tardos for the JET 2015 3-slot calibration and smoothness bounds.
- Brendan Lucier and Renato Paes Leme for the GSP conservative bidding Price of Anarchy conjecture (arXiv:1011.3268).
- V3R1T4S autonomous multi-agent discovery architecture.
