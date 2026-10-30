contributor text; every step below was rerun on 2026-10-25 and reproduces the object exactly

# How we found it

The rank-1547 ternary scheme is the composition from #410 plus two further steps: one mechanical, and one search step that saves one term.

1. **Block substitution (the composition in #410).** Start from Perminov's published rational scheme `11x14x16_m1520_Q`, rank 1520. The agent found 20 runs of 63 consecutive terms in it, each a <3,4,7> block of rank 63. It replaced each with Perminov's published `3x4x7_m64_ZT` of rank 64, carried through the exact linear maps of that block. That gives 1520 + 20 = 1540. A flip pass did not lower it. The maps leave 8 of the 1540 terms with a coefficient of 2, so this scheme is in class Z, not ZT. It is `how-we-built-it/start/11x14x16_m1540_Z.json`, the same file as the object of #410 (sha256 `66011ac1f5e75b0684243a5546c3a163f98eb01e79ead74b30785c07829f0f66`). This step is a composition of published instances and is not claimed.
2. **Ternary split (mechanical).** A vector with entries of size 2 is the sum of two ternary vectors. Each of the 8 terms that have a coefficient of 2 therefore splits into two ternary terms. That gives a valid ternary scheme of rank 1548. This step is not claimed either.
3. **Ternary flip-graph reduction (the search step).** `how-we-built-it/tools/zt_flip_reduce.c`, run for 100,000 steps with seed 1337 and coefficients kept in {-1, 0, 1}, takes 1548 to 1547. The flips also rewrite many terms without changing the rank, so only 1230 of the 1547 terms match the #410 scheme exactly.

So composition plus splitting gives 1548, and the search saves one more term. The live ZT value is 1550. Perminov published his own rank-1540 integer scheme for this format on 25/10/2026; 13 of its terms have a coefficient of 2, so the same split of it gives 1553.

## Reproduce it

The agent's run log was not kept. Instead, `how-we-built-it/rebuild.sh` reruns steps 2 and 3 from the shipped start file:

```sh
sh how-we-built-it/rebuild.sh            # needs python3 and a C compiler; writes to ./rebuild-out
```

On 2026-10-25 it printed:

```
input rank 1540; terms with a coefficient of absolute value 2 or more: 8; rank after the ternary split: 1548
PASS format=11x14x16 rank=1548
C_OPT(max=1): R 1548 -> 1547 | bad_triads 0 -> 0 | bad_entries 0 -> 0
PASS format=11x14x16 rank=1547
SAME: n=[11, 14, 16] m=1547, 857038 entries compared, 0 differ
```

The rebuilt dense file has sha256 `2a7d22e9c0e1881aeedfe29f53a8d2423673ca7dbf827f4eece7a598d2a93da7`. That is the same as the original dense object the panel checked, byte for byte. Step 1 is the composition the maintainer has already reproduced for #410. The parent, base schemes and script for it are named and hashed in `how-we-built-it/README.md`.
