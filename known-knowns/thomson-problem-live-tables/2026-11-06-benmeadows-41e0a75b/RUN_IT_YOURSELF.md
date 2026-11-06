# Run it yourself

From this folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (about one second with numpy installed; the energy part needs only Python 3):

```
sha256 41e0a75b4b6d5bbb4a7c8f3d951ab712da44e958b69641eb2ac2c2da3967f979
points: 436  fewest significant digits in a coordinate: 30
E* = 90020.681268073011826514460478379715290371348019301
claimed E* = 90020.68126807301182651446  difference = 4.78379715290371348019301E-22
table minimum - E* = 0.034817546988173485539521620284709628651980699
float64 tangent gradient norm: 1.902e-12
tangent Hessian: 869 positive (need 869), 3 zero (rotations, expect 3), 0 negative; lowest [...]
PASS
```

Without numpy the gradient and Hessian lines are replaced by a note that those checks were skipped; the last line is
still PASS. The full mpmath certificate (Newton to gradient norm below 1e-20, and the polish of the posted table
files) is `how-we-built-it/src/certify.py`, which needs numpy, scipy and mpmath (`how-we-built-it/requirements.txt`):

```sh
python3 how-we-built-it/src/certify.py object/thomson-436.txt 90020.71608562 out e.436.txt deeter 436.xyz xyz
```

with `e.436.txt` from https://deetour.net/oppp/thomson/e.436.txt and `436.xyz` from
https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/xyz/436.xyz downloaded beside it. Its last lines on our run:
`ALL CHECKS PASS`, after about 3.5 minutes on one core.

To rebuild the object: `how-we-built-it/COMMANDS.md`.
