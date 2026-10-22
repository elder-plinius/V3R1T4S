# An exact certificate for the Angel–Holmes all-in conjecture

## What

For every real x,y,z>0 with x<y in the all-in game defined in the source paper, f(x,y,z)-f(y,y,z) is at least 379/1813985280>0.

PROVED-HERE: this computer-assisted proof has three exact region certificates covering one theorem. It checks all 9,839 nodes and 6,561 leaves, including every admissible equality stratum.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Requires Python 3 and a C++17 compiler supporting signed 128-bit integers. No solver, network or third-party Python package is required. Expected last line: `PASS`. A complete prior replay took 38.23 seconds on the run machine; speed depends on the machine.

## Compared to

Conjecture 9 in [He–Holmes, arXiv:2410.15329](https://arxiv.org/abs/2410.15329), Section 5.3, was left open after their finite-depth computation became too slow. The primary status page returned HTTP 200 at 2026-10-15T16:12:59.555801+00:00 and lists only v1. The full independent novelty assessment is in panel/novelty.md.

## Not claimed

This is not a Lean/Coq/Isabelle formalization, an optimal quantitative gap, general monotonicity in the first stack, the unit-step gambler's ruin game, or an independently peer-reviewed publication. The claimed full theorem is the inequality stated above.

## Credits

Omer Angel and Mark Holmes posed the conjecture, as attributed by Angel Y. He and Mark Holmes in [All In: Give me your money!](https://arxiv.org/abs/2410.15329). Their [MeshItUp implementation](https://github.com/7angel4/betting-game-proof) inspired region partitioning. The supplied adaptive prover and separate verifiers were newly written during this research; none imports their solver code. The original candidate and subsequent fresh independent reviews are credited in how-we-built-it/PROVENANCE.md.
