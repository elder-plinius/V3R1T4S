# Pre-Registration: Least Prime with Prescribed Quadratic Character (A000229 n=39..43)

- **Target ID**: `least-qnr-prescribed-quadratic-character-next-terms`
- **Registered Prior Record**:
  - `A000229` (`https://oeis.org/A000229/b000229.txt`, SHA-256 `cfeddbe49cafbc4f498bfbbd0a6e4afa0382ddbc8254c51a93cf8a7d4d90478b`) ends at `n = 38` (`a(38) = 70864718555231`, least QNR `p_38 = 163`).
  - `A002223` (`https://oeis.org/A002223/b002223.txt`, SHA-256 `2e6b7bdde46a35f33e84ed84e9e68b14b94628721c5450cd4d82df0db5650ba3`) gives `A002223(38) = 317398900373231` (`7 mod 8`, least QNR `167`) and `A002223(40) = A002223(41) = 501108392233679` (`7 mod 8`, least QNR `191`).
  - `A002224` (`https://oeis.org/A002224/b002224.txt`, SHA-256 `70fa340ea4ea5035017afad7742632f61ae03c75cafdcf7ab0e69f2b99579ce8`) gives `A002224(38) = A002224(39) = 112434732901969` (`1 mod 8`, least QNR `173`) and `A002224(40) = A002224(41) = 178936222537081` (`1 mod 8`, least QNR `181`).
- **Planned Attack & Independent Verification Protocol**:
  1. Exhaustively search `[1, 317398900373231]` via two independent CRT modulus splits (`M1 = 892,371,480` with 20 sieve primes and `M2 = 25,878,772,920` with 28 sieve primes) to reproduce `A000229(30..38)`, `A002223(30..38)`, and `A002224(30..41)` from 1 and certify `A000229(39) = 317398900373231` (unblocking `A000229(40) = 112434732901969`).
  2. Exhaustively search `[1, 1463971373078639]` for primes with the first 40 primes (`2..173`) as quadratic residues via two independent CRT modulus splits (`M2 = 25,878,772,920` with 30 sieve primes and `M3 = 802,241,960,520` with 29 sieve primes) to certify `A000229(41) = 1463971373078639` (unblocking `A000229(42) = 178936222537081` and `A000229(43) = 501108392233679`).
  3. Verify every prime via deterministic 64-bit Miller-Rabin primality testing, Euler criterion `p^((q-1)/2) mod q`, and Quadratic Reciprocity Legendre symbols.
