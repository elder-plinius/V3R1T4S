# Receipts (real output, 2026-11-01 and 2026-11-07)

## sh verify-it-yourself/run_checks.sh
```
object hashes ok
N=3 m=12326115 accepted by three checkers; m+1, perturb and drop refused by all three
N=4 m=12621691 accepted by three checkers; m+1, perturb and drop refused by all three
N=5 m=12776965 accepted by three checkers; m+1, perturb and drop refused by all three
N=8 m=13020558 accepted by three checkers; m+1, perturb and drop refused by all three
Lemma 1 small cases hold
exact tests N=3 ok
exact tests N=4 ok
exact tests N=5 ok
PASS
```

## Full N = 17 check on the three certificate files
```
check_a17 17 16777216 13332272: ACCEPT claimed m=13332272, L=m/K=13332272/16777216=0.794665336609 (14.34 s, peak footprint 1,697,301,992 bytes; rerun with the shipped source after its argument checks were added)
  N=17 states=242084334 row_action_states=107272712 K=16777216 min_E=13332272 Vmin=10073540 Vmax=217519211
  m+1: exit=1 REJECT min_E 13332272 < claimed 13332273
  perturb: exit=1 REJECT min_E 13332271 < claimed 13332272
  drop: exit=1 REJECT closure row: b=37999 h=27126 a=0 next 91126 missing
check_d 17 16777216 13332272: ACCEPT m=13332272 K=16777216 (29.99 s)
  rowStates=107272712 shiftStates=134811622 minE=13332272 (attained by 3 states, first index 4751) failures: structure=0 C1=0 C2=0 C3=0
  m+1: exit=1 REJECT m=13332273 K=16777216
  perturb: exit=1 REJECT m=13332272 K=16777216 (mutated, perturb)
  drop: exit=1 REJECT m=13332272 K=16777216 (mutated, drop)
check_e 17 16777216 13332272: ACCEPT m=13332272 K=16777216 (9.41 s)
  statesWithE=242084334 minE=13332272 sumE=3227536924871139 violations C1=0 C2=0 C3=0
  m+1: exit=1 REJECT C1=0 C2=0 C3=3
  perturb: exit=1 REJECT (perturb detected) C1=0 C2=0 C3=1
  drop: exit=1 REJECT (drop detected) C1=0 C2=1 C3=0
```

## Simulated rate (numerical only, carries no weight in the bound)
```
N=17 T=200000000 reward=79467025 rows=102217951 2R/T=0.794670 rowfrac=0.51109
```

## Clean rebuild, after the panel (one machine; another machine may round floats differently)
```
46f3504cef37fc75999afac8688b0d643ab5cba34e2429bac938a833ea22cb93  c17.counts
b35375dd4799af6c4c78ad1fcbb4d69832a32116b1926974509c78a2e00c3d44  c17.states
6016451b188244d4654c35c32ff331085791178076a1bfcb7a6f499a372d8aeb  c17.V
identical c17.counts
identical c17.states
identical c17.V
prod4 peak footprint 2,537,474,160 bytes
```

## prod4 in non-lean mode at N = 16, final code, against the earlier N = 16 files
```
c3fdd79483fd7e1c97d361cb945aeedb5cd51253fc7e8daa857cdae6f5c535b0  c16.V
a081327e3f909d7679d60d8c679e15333e525aef5768479a372a8456d525db8a  c16.states
peak footprint 1,421,460,824 bytes
```

## Rebuild of 2026-11-07, same machine, commands of RUN_IT_YOURSELF.md, about 14 minutes

check_d and check_e were each written in a fresh context from object/PROOF.md and object/FORMAT.md.

```
M=14 rho in [0.3959816,0.3961249] gamma>=[0.7919632,0.7922498] t=38.4
POLISHED N=17 states=242084334 E_min=13332272 E_max=13332290 certified L=0.794665337 upper-ish=0.794666409 maxrss_MB=2536 t=729.4
46f3504cef37fc75999afac8688b0d643ab5cba34e2429bac938a833ea22cb93  c17.counts
b35375dd4799af6c4c78ad1fcbb4d69832a32116b1926974509c78a2e00c3d44  c17.states
6016451b188244d4654c35c32ff331085791178076a1bfcb7a6f499a372d8aeb  c17.V
check_a17: ACCEPT claimed m=13332272, L=m/K=13332272/16777216=0.794665336609
check_d: ACCEPT m=13332272 K=16777216
check_e: ACCEPT m=13332272 K=16777216
m+1, perturb and drop: refused by all three (exit 1)
```
