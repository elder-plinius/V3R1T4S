# The certificate

N = 17, K = 2^24 = 16777216, m = 13332272, 242,084,334 canonical states. Three files, two far too large to ship here:

| file | bytes | sha256 |
|---|---|---|
| c17.counts | 262,144 | 46f3504cef37fc75999afac8688b0d643ab5cba34e2429bac938a833ea22cb93 |
| c17.states | 726,253,002 | b35375dd4799af6c4c78ad1fcbb4d69832a32116b1926974509c78a2e00c3d44 |
| c17.V | 968,337,336 | 6016451b188244d4654c35c32ff331085791178076a1bfcb7a6f499a372d8aeb |

object/FORMAT.md gives the format. object/PROOF.md section 5 states what must hold. c17.counts is held back with the other two because it is useless alone.

RUN_IT_YOURSELF.md rebuilds all three from how-we-built-it/. Float rounding on another machine may change the bytes; any files that pass the checkers at m give gamma_2 >= m/K, whatever produced them.

object/small/ holds certificates for N = 3, 4, 5, 8 in the same format, used by the quick check. object/small_old/ holds the same four in the older 4-byte state format that verify-it-yourself/exact_small.py and sim_check.py read.
