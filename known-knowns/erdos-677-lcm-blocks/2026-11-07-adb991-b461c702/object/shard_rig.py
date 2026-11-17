"""Run deep_rig.py (bytes unchanged) on one shard of the admissible ratios: the shard of index I out of S keeps the
ratios at positions j with j % S == I of deep_cf's admissible_r(k) list (its own deterministic order). The S shards
partition the list, so their TOTAL lines add up to deep_rig's unsharded result. Usage:
  SHARD=I/S QEXP=495 python3 -I shard_rig.py KMIN KMAX DIG ETA X0"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
I, S = map(int, os.environ["SHARD"].split("/"))
import deep_rig
_full = deep_rig.admissible_r
def shard(k):
    rs = list(_full(k))
    return [r for j, r in enumerate(rs) if j % S == I]
deep_rig.admissible_r = shard
print(f"SHARD {I}/{S}", flush=True)
deep_rig.main()
