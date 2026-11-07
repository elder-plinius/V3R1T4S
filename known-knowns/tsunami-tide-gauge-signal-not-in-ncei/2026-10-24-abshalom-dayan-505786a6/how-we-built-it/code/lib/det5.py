"""PREREG.v5 runner: rules 1-2 (literal control days, every tied sensor scored on its own series). Detector functions
are det.py's, unchanged; the overlap rule (3) is applied by the caller through `overlap`."""
import numpy as np, pandas as pd
import det, tt


def _agg(per, nm):
    """Code-level result for origin nm from per-sensor results (rule 2)."""
    U = {k: v[nm] for k, v in per.items() if v[nm].get('usable')}
    if not U:
        return dict(usable=False)
    lo = min(U, key=lambda k: U[k]['r'])
    d = dict(usable=True, sensors=sorted(U), r=U[lo]['r'], arrival=U[lo]['arrival'],
             detects=all(x['detects'] for x in U.values()))
    if d['detects'] and all('ctrl_n' in x for x in U.values()):
        d['ctrl_n'] = min(x['ctrl_n'] for x in U.values())
        d['ctrl_max_r'] = max([x['ctrl_max_r'] for x in U.values() if x['ctrl_max_r'] is not None], default=None)
        r5 = any(x['ctrl_r5'] for x in U.values())
        d['passes'] = bool(all(x['ctrl_n'] >= 10 and not x['ctrl_r5'] for x in U.values()))
        d['undecided'] = bool(not d['passes'] and not r5 and any(x['ctrl_n'] < 10 for x in U.values()))
        d['ctrl_r5'] = r5
    return d


def run_source5(label, origin, lat, lon, fakes=(), overlap=None, maxkm=det.MAXKM):
    o = pd.Timestamp(origin)
    if o.tzinfo is not None:
        o = o.tz_convert(None)
    o = o.floor('s')
    st = det.stations().copy()
    st['km'] = tt.gc_km(lat, lon, st.lat.values, st.lon.values)
    st = st[st.km <= maxkm].sort_values('km')
    res = dict(label=label, origin=str(o), lat=lat, lon=lon, alt=int(tt.alt_at(lat, lon)), dmin=det.DMIN, c=det.C,
               fakes=list(fakes), rules='PREREG.v5', overlap=overlap or {})
    try:
        f = tt.FMM(lat, lon, radius_km=1700)
        res['src_snap_km'] = f.src_snap_km
    except RuntimeError as ex:
        res['error'] = f'tt: {ex}'; res['gauges'] = []; return res
    gs = []
    for _, g in st.iterrows():
        t, sd, h = f.eta(g.lat, g.lon, dmin=det.DMIN)
        if not np.isfinite(t):
            continue
        eta = t + det.C
        if det.ETA_LO <= eta <= det.ETA_HI:
            gs.append(dict(code=g.code, name=g['name'], country=g.country, lat=g.lat, lon=g.lon, km=round(float(g.km), 1),
                           eta=round(float(eta), 2), snap_km=round(sd, 2), snap_depth=h))
    site = det.sites_of(gs)
    for g in gs:
        g['site'] = site[g['code']]
    t0 = det.floor_h(o - pd.Timedelta(hours=31)); t1 = det.ceil_h(o + pd.Timedelta(hours=7))
    split = det.floor_h(o - pd.Timedelta(hours=25))
    T0 = det.floor_h(o - pd.Timedelta(days=8, hours=1)); T1 = det.ceil_h(o + pd.Timedelta(days=9))
    origins = [('real', o)] + [(f'fake{h}', o - pd.Timedelta(hours=h)) for h in fakes]
    for g in gs:
        rows = det.raw_window(g['code'], t0, t1, alt_split=split)
        sens = det.tied_sensors(rows)
        per = {}
        for sn in sens:
            s, info = det.series(rows, t0, t1, sensor=sn)
            if s is None:
                continue
            bp = det.highpass(s); bpc = det.highpass_causal(s)
            per[sn] = {nm: det.stat(s, bp, oo, g['eta'], bpc) for nm, oo in origins}
        g['tied'] = sens
        if not per:
            g['status'] = 'no usable tied sensor series'; continue
        need = [nm for nm, _ in origins if _agg(per, nm).get('detects')]
        if need:
            # stage-2 window per origin: the real origin's for all (as run), or relative to each fake origin (PREREG.v6)
            W2 = {nm: (det.floor_h(oo - pd.Timedelta(days=8, hours=1)), det.ceil_h(oo + pd.Timedelta(days=9)))
                  if det.IMPL6 and nm != 'real' else (T0, T1) for nm, oo in origins}
            rows2 = {}
            for nm in need:
                if W2[nm] not in rows2:
                    rows2[W2[nm]] = det.ioc_raw(g['code'], *W2[nm])
            for sn, v in per.items():
                if not any(v[nm].get('usable') for nm in need):
                    continue
                sw = {}
                for nm, oo in origins:
                    if nm not in need or not v[nm].get('usable'):
                        continue
                    if W2[nm] not in sw:
                        s2, _ = det.series(rows2[W2[nm]], *W2[nm], sensor=sn)
                        sw[W2[nm]] = (s2, det.highpass(s2) if s2 is not None else None,
                                      det.highpass_causal(s2) if s2 is not None else None)
                    s2, bp2, bpc2 = sw[W2[nm]]
                    ctrl = []
                    for k in det.CTRL:
                        if bp2 is None:
                            continue
                        c = det.stat(s2, bp2, oo + pd.Timedelta(days=k), g['eta'], bpc2)
                        if c['usable']:
                            ctrl.append(dict(day=k, r=c['r'], detects=c['detects']))
                    v[nm].update(ctrl_n=len(ctrl), ctrl_max_r=max([c['r'] for c in ctrl], default=None),
                                 ctrl_r5=any(c['r'] > 5 for c in ctrl), ctrl=ctrl)
        g['res_by_sensor'] = per
        g['res'] = {nm: _agg(per, nm) for nm, _ in origins}
    res['gauges'] = gs
    summ = {}
    for nm, _ in origins:
        us = {g['site'] for g in gs if g.get('res', {}).get(nm, {}).get('usable')}
        de = {g['site'] for g in gs if g.get('res', {}).get(nm, {}).get('detects')}
        pa = {g['site'] for g in gs if g.get('res', {}).get(nm, {}).get('passes')}
        und = {g['site'] for g in gs if g.get('res', {}).get(nm, {}).get('undecided')}
        if not gs:
            cls = 'NO_GAUGE'
        elif (overlap or {}).get(nm):
            cls = 'OVERLAP'
        elif not us:
            cls = 'NO_DATA'
        elif pa:
            cls = 'SIGNAL'
        elif und:
            cls = 'SIGNAL_UNDECIDED'
        else:
            cls = 'NO_SIGNAL'
        summ[nm] = dict(cls=cls, n_sites=len(set(site.values())), n_usable=len(us), n_detect=len(de), n_pass=len(pa))
    res['summary'] = summ
    return res
