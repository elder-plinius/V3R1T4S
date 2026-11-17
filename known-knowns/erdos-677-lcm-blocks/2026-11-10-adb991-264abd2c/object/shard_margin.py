"""Run rig_margin_exact.py (bytes unchanged) on one shard of the admissible ratios: the shard of index I out of S
keeps the ratios at positions j with j % S == I of deep_cf's admissible_r(k) list (its own deterministic order).
The S shards partition the list, so their pair counts add up to the unsharded run. Usage:
  SHARD=I/S python3 -I shard_margin.py KMIN KMAX X0 ... (the same arguments as rig_margin_exact.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
I, S = map(int, os.environ["SHARD"].split("/"))
import rig_margin_exact
_full = rig_margin_exact.admissible_r
def shard(k):
    rs = list(_full(k))
    return [r for j, r in enumerate(rs) if j % S == I]
rig_margin_exact.admissible_r = shard
print(f"SHARD {I}/{S}", flush=True)
rig_margin_exact.main()
