"""Onodera (Zenodo 8373651) SP event windows: list windows within +/- 5 min of, or containing, a time."""
import os, datetime as dt
import numpy as np
import pandas as pd

NS = 1_000_000_000
UNPARSED = []


def load(litdir):
    rows = []
    for s in (14, 15, 16):
        p = os.path.join(litdir, 'onodera_S%d_New_MQ_SP.csv' % s)
        if not os.path.isfile(p):
            continue
        for r in pd.read_csv(p, dtype=str).itertuples():
            try:
                a = dt.datetime.strptime(r.Start.strip(), "%d/%m/%Y %H:%M"); b = dt.datetime.strptime(r.End.strip(), "%d/%m/%Y %H:%M")
            except ValueError:
                UNPARSED.append((s, r.ID, r.Start, r.End)); continue
            ta = int((a - dt.datetime(1970, 1, 1)).total_seconds()) * NS; tb = int((b - dt.datetime(1970, 1, 1)).total_seconds()) * NS
            rows.append((ta, tb, 'onodera S%d id %s type %s' % (s, r.ID, r.Type)))
    return rows


def matches(rows, t):
    return [lab for a, b, lab in rows if abs(a - t) <= 300 * NS or a - 300 * NS <= t <= b + 300 * NS]
