# The Record We Beat

- **Target ID**: `least-qnr-prescribed-quadratic-character-next-terms`
- **Primary Status Sources Checked (UTC `2026-10-31T02:16:36Z`)**:
  - `https://oeis.org/A000229` — HTTP 200, `19906` bytes, SHA-256: `42d1576bff6905f7f1f27208f9ca2cecc4c4dd86427983ed98de1c50d5a39d07`
  - `https://oeis.org/A000229/b000229.txt` — HTTP 200, `453` bytes, SHA-256: `cfeddbe49cafbc4f498bfbbd0a6e4afa0382ddbc8254c51a93cf8a7d4d90478b`
  - `https://oeis.org/A002223/b002223.txt` — HTTP 200, `864` bytes, SHA-256: `2e6b7bdde46a35f33e84ed84e9e68b14b94628721c5450cd4d82df0db5650ba3`
  - `https://oeis.org/A002224/b002224.txt` — HTTP 200, `532` bytes, SHA-256: `70fa340ea4ea5035017afad7742632f61ae03c75cafdcf7ab0e69f2b99579ce8`
- **Prior Published Frontier**:
  - `A000229` and `b000229.txt` end at $n = 38$ (`a(38) = 70864718555231`, least QNR $163$, from Tomas Oliveira e Silva exhaustive verification to $10^{14}$).
- **New Exact Values Established**:
  - `A000229(39) = 317398900373231` (least prime with least QNR $p_{39} = 167$, certified minimal by exhaustive search of $q \equiv 1 \pmod 8$ and $q \equiv 7 \pmod 8$ from $1$ to $317,398,900,373,231$).
  - `A000229(40) = 112434732901969` (least prime with least QNR $p_{40} = 173$, unblocked once `A000229(39)` is settled).
  - `A000229(41) = 1463971373078639` (least prime with least QNR $p_{41} = 179$, certified minimal by two independent CRT modulus splits across $[1, 1463971373078639]$).
  - `A000229(42) = 178936222537081` (least prime with least QNR $p_{42} = 181$, unblocked once `A000229(41)` is settled).
  - `A000229(43) = 501108392233679` (least prime with least QNR $p_{43} = 191$, unblocked once `A000229(41..42)` are settled).
