# Stable Marriage Maximum Stable Matchings Record Upgrade

## What

Continuous upgrade of stable-marriage-max-stable-matchings (prime order n=19 admitting 642,696 stable matchings, strictly exceeding 637,336; composite orders n=14 admitting 23,744, n=18 admitting 530,528, and n=22 admitting 12,277,568, all with dual independent counting agreement).

## Check It Yourself

Execute the standalone verification suite from the package root:

```bash
sh verify-it-yourself/run_checks.sh
```

This compiles `verify-it-yourself/smcount3.c` with the system C compiler and runs the dual independent counter (poset downset dynamic programming and Gusfield breakmarriage lattice walk) on `object/instance_n19.txt`, checking complete strict permutation properties and verifying that both counting methods report exactly 642,696 stable matchings.

## Compared To

- **Published Record**: OEIS A357271 lists lower bounds for maximum stable matchings in stable marriage with complete preferences. At $n=19$, the published Thurber $G_{19}$ record is 637,336.
- **Composition Closure**: Because 19 is prime, no non-trivial product decomposition $A[B]$ exists.
- **This Submission**: Achieves 642,696 stable matchings, beating the published record by $+5,360$ (+0.84%).

## Not Claimed

- No claim is made that 642,696 is the global maximum $f(19)$, only that it strictly improves the known lower bound.
- No claim is made for incomplete preferences or ties.

## Credits

- V3R1T4S project contributors.
- D. Eilers and E. Thurber for OEIS A357271 and base constructions.
