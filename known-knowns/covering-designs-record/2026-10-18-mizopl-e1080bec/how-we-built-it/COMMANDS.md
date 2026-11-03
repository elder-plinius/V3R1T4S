# Commands Used to Build `object/design_94_13_5_part1.txt .. part5.txt`

## 1. Compile the Search & Post-Processing Tools

```sh
cc -O3 -march=native -pthread how-we-built-it/merge.c -o merge
cc -O3 -march=native -pthread how-we-built-it/prune.c -o prune
```

## 2. Exact Six Ingredient Terms ($94 = 47 + 47$) and Baseline Construction (`125,236` Blocks)

Partition the $v = 94$ points $\{0,\dots,93\}$ into $V_1 = \{0,\dots,46\}$ ($v_1 = 47$) and $V_2 = \{47,\dots,93\}$ ($v_2 = 47$). Every 5-subset $T \subset V$ satisfies $j = |T \cap V_1| \in \{0, 1, 2, 3, 4, 5\}$ and $|T \cap V_2| = 5 - j$. Taking the disjoint union of the Cartesian products $\mathcal{D}_1^{(j)} 	imes (\mathcal{D}_2^{(j)} + 47)$ across $j = 0, \dots, 5$ with the block-size splits $(k_1, k_2) \in \{(0,13), (2,11), (5,8), (8,5), (11,2), (13,0)\}$ ($k_1 + k_2 = 13$) covers every 5-subset of $\{0,\dots,93\}$ in `125,236` blocks:

| $j = |T \cap V_1|$ | Left half $V_1$ ($0\dots 46$) | Right half $V_2$ ($47\dots 93$) | Block product $b_1 	imes b_2$ | Ingredient source URL & contributor credit | 0-based `.txt` `sha256` (`built/47-k-t.txt`) | 1-based `.txt` `sha256` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| $j = 0$ | $(47, 0, 0)$ (`1` empty block) | $C(47, 13, 5) \le 2,849$ | $1 	imes 2,849 = 2,849$ | https://ljcr.dmgordon.org/show_cover.php?v=47&k=13&t=5 and Zenodo LJCR v1.2 (`19735294`, `2026-04-24`); **Jan de Heer & Steve Muir** (`2026-02-28 23:37:09`) | `47-0-0.txt`: `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b` (`1` B)<br>`47-13-5.txt`: `af0df98e87b41ad88537bd7f6ba9e26b65b0a337aa4d28d554b46ad471807835` (`103,484` B) | `a5529708d2d4325f2cda450042ad08a3b10aa98e03179cbff460c889206bbf9c` (`104,265` B) |
| $j = 1$ | $C(47, 2, 1) \le 24$ (`{0,1},..,{44,45},{45,46}`) | $C(47, 11, 4) \le 866$ | $24 	imes 866 = 20,784$ | https://ljcr.dmgordon.org/show_cover.php?v=47&k=11&t=4 and Zenodo LJCR v1.2 (`19735294`, `2026-04-24`); **Jan de Heer & Steve Muir** (`2026-02-28 23:37:09`) | `47-2-1.txt`: `d5400aee5352427736a090d297a7dcd2a4fa97377654515928e7c715845310ef` (`134` B)<br>`47-11-4.txt`: `fe4b4cd936fa50ae0ca273b22bbcd1dfce55b808b56e5afbca0aaad28afdab06` (`26,337` B) | `f279047c161675718e00bafaba8a4724f08cd3821b0e17387d8e9387ab6b9172` (`135` B)<br>`76c5a427113e3ed9879d6814f4a75e7d6ee985c0ca3147fe411a37b4f4c2542a` (`26,556` B) |
| $j = 2$ | $C(47, 5, 2) \le 113$ | $C(47, 8, 3) \le 345$ | $113 	imes 345 = 38,985$ | $C(47,5,2)$: https://ljcr.dmgordon.org/show_cover.php?v=47&k=5&t=2 (**Michael Dambmann**, `2008-11-22 20:38:48`, `covers.json` bytes `1141952..1144005`, slice `sha256: 88545b5c01bbfcf4eb336bbe02209f93ea493aebc69cb0469f20a58dae0cd5fd`);<br>$C(47,8,3)$: https://ljcr.dmgordon.org/show_cover.php?v=47&k=8&t=3 (**Jan de Heer & Steve Muir**, `2009-07-02 00:39:14`, `covers.json` bytes `34804083..34813235`, slice `sha256: aa1f1e0f0c5d86d9b58a2a3424cd8c6a306a43e0680f2f6ef6d8c7a7e343b9ce`) | `47-5-2.txt`: `abcf309f0123d234d71ba3d1fff6943922e6f0c90da338947d6a47dcabacca05` (`1,575` B)<br>`47-8-3.txt`: `d9401d479f3b7a6abadcc8d45b6692f42e7995dfac46e2c8e1ce5499191419b7` (`7,695` B) | `5a460feb3e80e19411b35dd2f813175f1c3c9b377911ec169d75fc92cee6e230` (`1,587` B)<br>`169b3393fa4a95a677a5f25dbafb62277f2b7b6f09873408646c4707391560c6` (`7,758` B) |
| $j = 3$ | $C(47, 8, 3) \le 345$ | $C(47, 5, 2) \le 113$ | $345 	imes 113 = 38,985$ | Same ingredients as $j = 2$ with $V_1 \leftrightarrow V_2$ (**Jan de Heer & Steve Muir**; **Michael Dambmann**) | `47-8-3.txt`: `d9401d479f3b7a6abadcc8d45b6692f42e7995dfac46e2c8e1ce5499191419b7`<br>`47-5-2.txt`: `abcf309f0123d234d71ba3d1fff6943922e6f0c90da338947d6a47dcabacca05` | Same as $j = 2$ |
| $j = 4$ | $C(47, 11, 4) \le 866$ | $C(47, 2, 1) \le 24$ | $866 	imes 24 = 20,784$ | Same ingredients as $j = 1$ with $V_1 \leftrightarrow V_2$ (**Jan de Heer & Steve Muir**; trivial pairs) | `47-11-4.txt`: `fe4b4cd936fa50ae0ca273b22bbcd1dfce55b808b56e5afbca0aaad28afdab06`<br>`47-2-1.txt`: `d5400aee5352427736a090d297a7dcd2a4fa97377654515928e7c715845310ef` | Same as $j = 1$ |
| $j = 5$ | $C(47, 13, 5) \le 2,849$ | $(47, 0, 0)$ (`1` empty block) | $2,849 	imes 1 = 2,849$ | Same ingredients as $j = 0$ with $V_1 \leftrightarrow V_2$ (**Jan de Heer & Steve Muir**; trivial empty block) | `47-13-5.txt`: `af0df98e87b41ad88537bd7f6ba9e26b65b0a337aa4d28d554b46ad471807835`<br>`47-0-0.txt`: `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b` | Same as $j = 0$ |
| **Total** | | | **`125,236` blocks** | Zenodo LJCR v1.2 archive: https://zenodo.org/records/19735294 (`coverdata.json` `sha256: 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87`, `covers.json` `md5: bb59d977afd6724b32dcc187f68a229c`, fetched `2026-10-18T09:40:54Z`) | `built/94-13-5.txt`: `4ddf66cf9edf0cf96165e7514dbcd0cafb9c3dc67198326ea0586a63661ffcfb` (`4,706,688` B) | |

Run the self-contained builder `how-we-built-it/build.py` (which either parses `--covers-json /path/to/covers.json` from Zenodo `19735294` or extracts the ingredients directly from `object/design_94_13_5_part1.txt..part5.txt`, verifies all six ingredient `sha256`s above, and writes `built/94-13-5.txt` with `125,236` blocks and `sha256: 4ddf66cf9edf0cf96165e7514dbcd0cafb9c3dc67198326ea0586a63661ffcfb`):

```sh
python3 how-we-built-it/build.py
```

## 3. Run Pair-Merge Reduction (`125,236 -> 125,184` Blocks)

Run `merge` with all 7 required positional arguments (`v=94 k=13 t=5 in=built/94-13-5.txt out=design_94_13_5.txt time_sec=60 max_cand=200000`):

```sh
./merge 94 13 5 built/94-13-5.txt design_94_13_5.txt 60 200000
shasum -a 256 design_94_13_5.txt
```

Output:
```text
nb=125236 |U| histogram: 10:4 11:104 12:10074 13:115054
candidates=125236
merge in=125236 merges=52 out=125184 secs=15.2
e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908  design_94_13_5.txt
```

Specifically, `merge.c` merges `52` disjoint block pairs (`26` in the $j=1$ $(2,11)$ section and `26` in the $j=4$ $(11,2)$ section: `14` tail merges combining `{44,45}+B` and `{45,46}+B` into `{44,45,46}+B'` on 14 blocks $B \in C(47,11,4)$ whose uniquely-covered 4-subsets span $\le 10$ points, plus `12` merges combining `{2i,2i+1}+B_*` and `{2i+2,2i+3}+B_*` into `{2i,2i+1,2i+2,2i+3}+B_*'` on the block $B_* = (0,1,2,3,4,5,7,9,10,22,38) \in C(47,11,4)$ whose uniquely-covered 4-subsets span only the 9 points `{0,1,2,3,4,5,7,9,10}`).

## 4. Split into `< 1 MB` Parts for `object/`

```sh
split -l 25037 design_94_13_5.txt part_
mv part_aa object/design_94_13_5_part1.txt
mv part_ab object/design_94_13_5_part2.txt
mv part_ac object/design_94_13_5_part3.txt
mv part_ad object/design_94_13_5_part4.txt
mv part_ae object/design_94_13_5_part5.txt
```
