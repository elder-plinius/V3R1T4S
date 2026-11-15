# Run It Yourself

To verify the complex line packing directly from this package directory in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Object: object/5x49_v3r1t4s.txt
Dimension d=5, Lines n=49
Computed Coherence mu (40 digits): 0.5414603056425635743462895172126666579322
Leaderboard Record Coherence    : 0.54164128
Theoretical Lower Bound         : 0.50751922
Strict Lowering Margin          : 0.000180974357436425653710482787333342067819
VERIFIED: mu = 0.5414603056425635743462895172126666579322 strictly beats 0.54164128 by 0.000180974357436425653710482787333342067819 >= 1e-8
PASS
```

## How to Rebuild the Object
To rerun the active-set SQP equalizer that produced the object:
```sh
python3 how-we-built-it/sqp_equalizer.py
```
Note: `how-we-built-it/sqp_equalizer.py` reads `../../data/5x49_oai.txt` (`https://raw.githubusercontent.com/gnikylime/GameofSloanes/master/CurrentBestPackings/5x49_oai.txt`, SHA-256 `bb50766d16ea892dad8645f2993ca38edd04c2f2fe5af895b8909b2819ef8280`) and also processes rows `(6, 44)` (`../../data/6x44_oai.txt`, `https://raw.githubusercontent.com/gnikylime/GameofSloanes/master/CurrentBestPackings/6x44_oai.txt`, SHA-256 `51cb29423b8ae4cdcb6f2884702974e874eb29b30f1254a609f3cadc4d41de10`) and `(7, 29)` (`../../data/7x29_oai.txt`, `https://raw.githubusercontent.com/gnikylime/GameofSloanes/master/CurrentBestPackings/7x29_oai.txt`, SHA-256 `6b9163c2dc1a94ba2ae561aec135a730d7bf26d8ea575aa00a9319d9a1b24a7f`), writing polished outputs to `result/`.

Dependencies: Python 3.8+, numpy, scipy, mpmath.
