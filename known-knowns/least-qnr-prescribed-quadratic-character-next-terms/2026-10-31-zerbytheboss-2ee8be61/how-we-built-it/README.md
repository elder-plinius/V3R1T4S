# How We Built It

- `PREREG.md`: Pre-registered target specification, baseline OEIS b-file hashes, and multi-modulus CRT sieve verification plan.
- `verify_qnr_sieve.c`: C99 bit-parallel Chinese Remainder Theorem (CRT) sieve implementing Stage 1 (`M1 = 892,371,480` and `M2 = 25,878,772,920` up to `317,398,900,373,231`) and Stage 2 (`M2 = 25,878,772,920` and `M3 = 802,241,960,520` up to `1,463,971,373,078,639`).
- `check_qnr.py`: Python verifier checking deterministic 64-bit Miller-Rabin primality, Euler criterion, Quadratic Reciprocity Legendre symbols, `b000229.txt` SHA-256 reproduction, and element-by-element C sieve output parity.
