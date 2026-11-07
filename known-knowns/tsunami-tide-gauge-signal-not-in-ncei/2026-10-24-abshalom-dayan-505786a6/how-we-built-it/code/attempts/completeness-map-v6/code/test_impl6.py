"""Synthetic checks of the PREREG.v6 corrections: gap bridging <= 30 min only, stuck rule on raw samples."""
import sys, os
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', '..', '..', 'lib'))
import numpy as np, pandas as pd, det
idx = pd.date_range('2020-01-01', periods=600, freq='1min')
x = pd.Series(np.sin(np.arange(600) / 30.0), index=idx)
y = x.copy(); y.iloc[100:130] = np.nan; y.iloc[300:345] = np.nan      # a 30-min and a 45-min gap
for flag in (False, True):
    det.IMPL6 = flag
    f = det._fill(y, 30)
    print(f'IMPL6={flag}: 30-min gap filled {int(f.iloc[100:130].notna().sum())}/30, 45-min gap filled '
          f'{int(f.iloc[300:345].notna().sum())}/45')
det.IMPL6 = True
f = det._fill(y, 30)
lin = np.interp(np.arange(100, 130), [99, 130], [y.iloc[99], y.iloc[130]])
print('30-min gap linear:', bool(np.allclose(f.iloc[100:130].values, lin)))
# stuck: 1-min raw with a 40-min hole between two equal values -> gridded series has >= 60 identical minutes, raw has 21+1+21
t = pd.date_range('2020-01-02', periods=1500, freq='1min')
v = np.sin(np.arange(1500) / 50.0)
v[700:721] = 1.234; v[761:782] = 1.234
keep = np.r_[0:721, 761:1500]
rows = [dict(stime=str(t[k]), slevel=float(v[k]), sensor='rad') for k in keep]
o = pd.Timestamp('2020-01-03 02:00')
for flag in (False, True):
    det.IMPL6 = flag
    s, _ = det.series(rows, t[0], t[-1])
    s2 = s.copy(); s2.iloc[721:761] = 1.234          # what the old gridded path would see after filling the hole
    if flag:
        s2.attrs['raw'] = s.attrs['raw']
    print(f'IMPL6={flag}: stuck on a series whose gridded copy has a 82-min flat run ->', det.stuck(s2, o))
rows2 = [dict(stime=str(t[k]), slevel=float(1.0 if 600 <= k < 660 else v[k]), sensor='rad') for k in range(1500)]
det.IMPL6 = True
s, _ = det.series(rows2, t[0], t[-1])
print('IMPL6=True: 60 identical raw values -> stuck', det.stuck(s, o))
