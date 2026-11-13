"""Compare the Steim2 reader's output with the PDS GeoCSV twin (sample values and times)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, sys.argv[3])
from mseed_steim2 import read_mseed
recs = read_mseed(sys.argv[1])
vals = np.concatenate([r['data'] for r in recs])
times = np.concatenate([r['start'] + np.round(np.arange(len(r['data'])) / r['rate'] * 1e9).astype(np.int64) for r in recs])
hdr = [l for l in open(sys.argv[2]) if l.startswith('#')]
print(''.join(hdr).strip())
df = pd.read_csv(sys.argv[2], comment='#', skipinitialspace=True)
cv = df['Sample'].to_numpy()
ct = pd.to_datetime(df['Time'].str.replace('Z', ''), format='ISO8601').to_numpy().astype('datetime64[ns]').astype(np.int64)
print('n mseed', len(vals), 'n csv', len(cv))
print('values identical:', bool(len(vals) == len(cv) and np.array_equal(vals, cv)))
dt = (times - ct) / 1e9
print('time diff (s): max abs', np.abs(dt).max(), 'mean', dt.mean())
gaps = [(recs[i + 1]['start'] - (recs[i]['start'] + len(recs[i]['data']) / recs[i]['rate'] * 1e9)) / 1e9 for i in range(len(recs) - 1)]
print('inter-record gap (s): min %.6f max %.6f' % (min(gaps), max(gaps)))
print('count of -1 samples:', int((vals == -1).sum()))
