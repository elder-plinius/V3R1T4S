# Stable-marriage instance at n=10

> Explicit order-10 stable marriage instance with **1,008** stable matchings, beating the prior record of **1,000** (Thurber 2002; OEIS A357271) and refuting the conjecture that `f(10) = 1000`.

## What

`object/object.prefs` is a strict complete preference profile for 10 men and 10 women with exactly **1,008** stable matchings (43 rotations).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final line: `PASS` (Python 3 standard library only, < 0.2s). Validates preference lists, `INDEX.csv` SHA-256, and enumerates all 1,008 stable matchings with full $O(n^2)$ definition verification at every leaf.

## Compared to

| Source | `n = 10` value |
|---|---|
| Thurber (2002) / OEIS A357271 | 1,000 (conjectured exact) |
| **This submission** | **1,008** (+8; refutes exactness of 1,000) |

## Not claimed

- Lower-bound witness (`f(10) >= 1008`) only; optimality and asymptotic bounds are not claimed.
- Produced outside the native V3R1T4S `kit/` pipeline (no `panel/gate.md` fabricated); independently verified from scratch in Python 3 and unpruned `10!` C brute force.

## Credits

- **Human supervision & submission:** `greedy-dog`
- **AI search:** `fable5.2` (simulated annealing over rotation sequences)
- **Independent verification & packaging:** Gemini
- **Prior work:** Knuth (1976), Gusfield & Irving (1989), Thurber (2002), OEIS A357271.
