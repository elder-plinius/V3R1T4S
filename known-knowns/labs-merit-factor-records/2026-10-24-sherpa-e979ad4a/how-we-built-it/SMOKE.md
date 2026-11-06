# Smoke run

`python test_kernels.py` (from `code/`; NVIDIA GPU), real output at package build time. It checks every move energy against brute force at 16 lengths and exact energy tracking over long runs:

```
L=5: dE checked for 6x3 moves
L=7: dE checked for 6x4 moves
L=9: dE checked for 6x5 moves
L=11: dE checked for 6x6 moves
L=13: dE checked for 6x7 moves
L=15: dE checked for 6x8 moves
L=17: dE checked for 6x9 moves
L=21: dE checked for 6x11 moves
L=23: dE checked for 6x12 moves
L=51: dE checked for 6x26 moves
L=53: dE checked for 6x27 moves
L=101: dE checked for 6x51 moves
L=103: dE checked for 6x52 moves
L=449: dE checked for 6x225 moves
L=451: dE checked for 6x226 moves
L=599: dE checked for 6x300 moves
L=101: 64 walkers x 10000 steps in 0.01s (53,828,121 steps/s); tracked energies exact; best E=706 F=7.2245
L=119: 64 walkers x 10000 steps in 0.01s (49,364,717 steps/s); tracked energies exact; best E=1011 F=7.0035
L=451: 64 walkers x 10000 steps in 0.05s (14,206,918 steps/s); tracked energies exact; best E=19385 F=5.2464
FAILURES: 0
```
