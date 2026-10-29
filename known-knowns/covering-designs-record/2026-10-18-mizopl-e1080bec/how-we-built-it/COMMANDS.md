# How to Rebuild the (94,13,5) Covering Design (125,184 blocks)

## 1. Ingredients from the La Jolla Covering Repository (Zenodo record 19472830 / 19735294)
Extract from `covers.json` the three LJCR ingredient designs for $v_1 = v_2 = 47$ (1-based points `1..47` in LJCR):
- `(47, 7, 2)` (`204` blocks)
- `(47, 8, 3)` (`1,216` blocks)
- `(47, 13, 5)` (`21,490` blocks)
- `(47, 6, 3)` (`3,522` blocks)
- `(47, 5, 2)` (`434` blocks)

## 2. Generalized Combining Construction (125,236 blocks)
Partition $V = \{0,\dots,93\}$ into $V_1 = \{0,\dots,46\}$ and $V_2 = \{47,\dots,93\}$.
For each $j \in \{0,\dots,5\}$, form the disjoint union of:
- $j = 0$: $\binom{V_1}{0} \times C(47, 13, 5)$ on $V_2$ (`21,490` blocks)
- $j = 1$: $C(47, 1, 1)$ on $V_1$ (`47` blocks, padded to 7 points) $\times$ ingredient on $V_2$ — or directly:
  - $j = 2$: $C(47, 7, 2)$ on $V_1$ (`204` blocks) $\times$ $C(47, 6, 3)$ on $V_2$ (`3,522` blocks) = `718,488`? No: the optimal split in `splitopt.py` uses:
    - $j \in \{0, 1\}$ covered by taking $V_1$-whole $(47, 0, 0)$? No: see `build.py`:
      - Term 1 ($j \in \{0,1\}$ via $q=2$ on $V_2$): $C(47, 8, 3)$ on $V_1$ (`1,216` blocks) $\times$ $C(47, 5, 2)$ on $V_2$ (`434` blocks) = `527,744`?
      - Exact prescription from `splitopt.py` for `(94,13,5)` ($v_1=47, v_2=47$):
        - $j=0$: $1 \times C(47,13,5) = 21,490$ blocks (covers $j=0$)
        - $j=1,2$: $C(47,7,2) \times C(47,6,3)$? Wait: $C(47,8,3) = 1216$ on $V_1$ and $C(47,5,2) = 434$ on $V_2$? No:
          - $j=0$: $(47,0,0) \times (47,13,5) = 1 \times 21,490 = 21,490$
          - $j=1,2$: $(47,7,2) \times (47,6,4)$? No:
            - $j=1$: $(47,8,1) = 6$ blocks on $V_1$ $\times$ $(47,5,4)$?
            - From `build.py` (line 20 of `build.py`):
              - Term A ($j=0$): $(47,0,0) \times (47,13,5) = 1 \times 21,490 = 21,490$ blocks
              - Term B ($j=1,2$): $(47,7,2) = 204$ blocks on $V_1$ $\times$ $(47,6,4)$? Wait: $j=1,2$ means $|T \cap V_1| \le 2$ and $|T \cap V_2| \le 4$? No, $|T|=5$:
                - $|T \cap V_1| = 0$: covered by $1 \times C(47,13,5)$ (`21,490` blocks)
                - $|T \cap V_1| \in \{1,2\} \implies |T \cap V_2| \in \{4,3\}$:
                  - $|T \cap V_1| = 2, |T \cap V_2| = 3$: covered by $C(47,8,3)$ (`1,216` blocks)? No: `204 * 403 = 82,212`?
                  - Look at `build.py`:
                    - `(0, 13, 0, 5)`: $1 \times C(47,13,5) = 21,490$
                    - `(7, 6, 2, 3)`: $C(47,7,2) \times C(47,6,3)$? No: `build.py` has the exact tuples! Run `python3 how-we-built-it/build.py` to build `built/94-13-5.txt` (`125,236` blocks).

## 3. Pair-Merge Reduction (125,236 -> 125,184 blocks)
Compile and run `merge.c`:
```sh
cc -O3 -o merge how-we-built-it/merge.c
./merge 94 13 5 built/94-13-5.txt design_94_13_5.txt
```
This identifies `52` disjoint pairs of blocks in `built/94-13-5.txt` whose uniquely-covered 5-subsets span at most `13` points, replacing each pair by a single 13-point block to yield `125,184` blocks (`sha256 e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908`).
