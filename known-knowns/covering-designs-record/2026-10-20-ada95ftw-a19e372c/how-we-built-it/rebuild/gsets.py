#!/usr/bin/env python3
"""Groups and their transitive coset actions (G/H) of small degree. Reuses run 2026-10-19-1303 helpers."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mr, orbit_cover as oc

def all_groups():
    G = dict(mr.groups())                      # A5, S5, PSL27 (as in run 1303)
    G['PGL27'] = oc.group_gens(7, 'PGL')      # order 336 on 8 points
    G['PSL28'] = oc.group_gens(8, 'PSL')      # order 504 on 9 points (= PGL(2,8))
    G['PGaL28'] = oc.group_gens(8, 'PGaL')    # order 1512
    G['PSL211'] = oc.group_gens(11, 'PSL')    # order 660 on 12 points
    G['A6'] = [(1,2,3,4,0,5), (0,2,3,4,5,1)]  # (01234),(12345) generate A6
    return G

def actions(gname, gens, maxdeg, seed=1):
    E, cls = mr.subgroup_classes([tuple(g) for g in gens], seed)
    acts = []
    for H in cls:
        d = len(E)//len(H)
        if d <= maxdeg:
            acts.append((d, len(H), mr.coset_action([tuple(g) for g in gens], E, H)))
    return len(E), acts

if __name__ == '__main__':
    for n, g in all_groups().items():
        o, a = actions(n, g, 40)
        print(n, o, sorted((d, h) for d, h, _ in a))
