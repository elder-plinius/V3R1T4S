"""Nest templates with a glitch screen (PREREG.v11): as tools/nesttemplates.py, but a member channel window whose
max|x|/rms exceeds SCREEN (8) is left out of that channel's stack.

Nest templates by iterative alignment and stacking (the algorithm of the frozen A1 dev builder, made generic).

build(ev, chans, band, L, ref_index) -> dict(tm (list per channel or None), chans, members, starts, onset_rel_s)
ev: DataFrame from evlib.load_nest_events. Alignment search +/- 240 s around the catalogued start, 4 iterations,
members D >= 0.3 (fallback: best 5), onset pick on the stack envelope (4 x median of the first 60 s of a window
starting 120 s earlier), windows shifted to start 30 s before the onset, final re-stack.
"""
import numpy as np
from apollo_lib import NS, norm_template
from evlib import DayCache, best_lag, event_block, FS


SCREEN = 8.0


def _clean(y):
    sd = y.std()
    return sd > 0 and np.abs(y - y.mean()).max() / sd <= SCREEN


def _unit(y):
    y = y - y.mean(); n = np.sqrt((y * y).sum()); return y / n if n > 0 else None


def build(ev, chans_all, band, L, ref, cache=None, acc=0.3, search_s=240, iters=4):
    cache = cache or DayCache(band)
    M = int(round(L * FS))

    def contributions(starts):
        con = {}
        for i, s in starts.items():
            blk = event_block(cache, chans_all, s, M)
            con[i] = [_unit(y) if (y is not None and v.mean() >= 0.95 and _clean(y)) else None for y, v in blk]
        return con

    def make_tm(con, include):
        tm = []
        for k in range(len(chans_all)):
            a = [con[i][k] for i in include if con[i][k] is not None]
            tm.append(norm_template(np.sum(a, axis=0)) if a else None)
        return tm

    def active(tm):
        return [c for c, t in zip(chans_all, tm) if t is not None], [t for t in tm if t is not None]

    blk = event_block(cache, chans_all, int(ev.loc[ref, 't_ns']), M)
    tm = [norm_template(y) if (y is not None and v.mean() > 0.95) else None for y, v in blk]
    if sum(t is not None for t in tm) < 2:
        return None
    found = {}
    members = []
    for it in range(iters):
        ch, tt = active(tm)
        if len(ch) < 2:
            return None
        found = {}
        for i, r in ev.iterrows():
            t = int(r['t_ns'])
            b = best_lag(cache, ch, tt, t - search_s * NS, t + search_s * NS)
            if b is not None:
                found[i] = (b[0], b[1])
        members = [i for i, (d, s) in found.items() if d >= acc]
        if len(members) < 3:
            members = sorted(found, key=lambda i: -found[i][0])[:5]
        con = contributions({i: found[i][1] for i in members})
        tm = make_tm(con, members)
    PRE = int(120 * FS); Ml = M + 2 * PRE
    E = np.zeros(Ml)
    for k in range(len(chans_all)):
        a = []
        for i in members:
            y, v = event_block(cache, [chans_all[k]], found[i][1] - 120 * NS, Ml)[0]
            if y is not None and v.mean() >= 0.95 and _clean(y):
                a.append(_unit(y))
        if a:
            st = np.mean(a, axis=0); E += st * st
    w5 = int(5 * FS); Es = np.convolve(E, np.ones(w5) / w5, mode='same')
    noise = np.median(Es[:int(60 * FS)])
    above = np.flatnonzero(Es[int(60 * FS):] > 4 * noise)
    onset_idx = int(60 * FS) + int(above[0]) if above.size else PRE + int(30 * FS)
    onset_rel_s = (onset_idx - PRE) / FS
    shift = int((onset_rel_s - 30.0) * NS)
    starts = {i: found[i][1] + shift for i in members}
    con = contributions(starts)
    tm = make_tm(con, members)
    return dict(tm=tm, chans=chans_all, members=members, starts=starts, onset_rel_s=onset_rel_s,
                member_D={i: found[i][0] for i in members})
