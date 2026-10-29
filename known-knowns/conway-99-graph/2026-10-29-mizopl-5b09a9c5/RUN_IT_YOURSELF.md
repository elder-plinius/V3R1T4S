# Run It Yourself — `conway-99-graph` (`2026-10-26-mizopl-bcf57871`)

## Requirements
- Python 3.8+ (standard library only; zero external dependencies).

## One-Command Verification
From the package root directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Or directly via Python:

```sh
python3 -B verify-it-yourself/verify.py
```

## What `verify.py` Checks
1. **Positive Non-Vacuity Control (`srg(9, 4, 1, 2) = K_3 box K_3`):**
   Builds the unblocked forced-structure CNF on $\mathrm{srg}(9, 4, 1, 2)$ ($k = 4, M = 4$) under both Encoding A (Sinz 2005 Sequential Counter, $200$ clauses) and Encoding B (Bailleux & Boufkhad 2003 Binary Tree Totalizer, $146$ clauses), seeds the $6$ outer-edge variables with the unique outer $4$-cycle assignment of $K_3 \square K_3$, and verifies via deterministic unit propagation that every clause in both encodings is satisfied.
2. **Fresh CNF Re-Generation & Exact Core Clause Membership (54 Proofs across 27 Theorems):**
   Re-generates all $54$ full CNF clause sets from scratch (`5` Track `p2` propositions + `22` Track `p1` automorphism exclusions—including the open prime order $p = 7$ case `p7_fix1` and 18 of 19 involution profiles—across Encoding A and Encoding B) and checks that every clause in each `object/proofs/*_core.cnf` file is an exact member of the freshly generated CNF from its encoder.
3. **Pure-Python LRAT RUP Proof Verification (`92,259` RUP Lemmas, `0` RAT Lemmas):**
   Verifies all $54$ LRAT proofs in `object/proofs/*.lrat` (`55,589` RUP steps in Encoding A + `36,670` RUP steps in Encoding B = `92,259` RUP steps total) using a self-contained pure-Python LRAT Reverse Unit Propagation checker, confirming that `0` RAT lemmas are used and that every proof derives the empty clause `0`.
4. **Cryptographic Digest & Invariant Audit:**
   Verifies all SHA-256 digests (`142` proof files, each `< 750 KB`), variable/clause counts, and permutation cycle-structure invariants against `object/certificate.json`, terminating with `VERIFY: PASS`.
