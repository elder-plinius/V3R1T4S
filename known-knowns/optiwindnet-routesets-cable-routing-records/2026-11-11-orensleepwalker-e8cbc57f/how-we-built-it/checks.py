"""Criterion checks for a route set graph G (optiwindnet conventions)."""
import math
import numpy as np
import shapely.geometry as sg
from optiwindnet.validating import validate_routeset

def euclid_length(G):
    VC = G.graph['VertexC']; fnT = G.graph.get('fnT')
    def xy(n):
        i = fnT[n] if fnT is not None else n
        return VC[i]
    return float(sum(math.dist(xy(u), xy(v)) for u, v in G.edges()))

def containment(G):
    VC = G.graph['VertexC']; fnT = G.graph.get('fnT'); bad = []
    border = G.graph.get('border'); obstacles = G.graph.get('obstacles', [])
    def xy(n):
        i = fnT[n] if fnT is not None else n
        return tuple(VC[i])
    bpoly = sg.Polygon(VC[border]) if border is not None and len(border) else None
    opolys = [sg.Polygon(VC[o]) for o in obstacles]
    for u, v in G.edges():
        seg = sg.LineString([xy(u), xy(v)])
        if bpoly is not None and not bpoly.covers(seg): bad.append(('outside_border', u, v))
        for k, op in enumerate(opolys):
            if seg.crosses(op) or op.contains(seg) or seg.within(op): bad.append(('in_obstacle', k, u, v))
    return bad

def full_check(G):
    v = validate_routeset(G)
    return {'violations': v[:10], 'containment': containment(G)[:10], 'length_euclid': euclid_length(G),
            'length_attr': float(sum(d['length'] for _, _, d in G.edges(data=True)))}
