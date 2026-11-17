"""Bank verification step: train with every test-glacier row deleted from the training input (by BREID and by RGIID)
and confirm the test predictions are bit-identical to the primary model's. Usage: deleted_test_rows.py CLAIM_CODE DATA"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, sys.argv[1])
import reimpl_p3 as R
wide = pd.read_csv(os.path.join(sys.argv[2], R.DATA['wide']))
test_rgi = sorted(wide.loc[wide['BREID'].isin(R.TEST_BREID), 'RGIID'].unique())
print('test RGIIDs', len(test_rgi), test_rgi)
rows, _ = R.build_records(wide)
te = rows[rows['BREID'].isin(R.TEST_BREID)].reset_index(drop=True)
tr = rows[~rows['BREID'].isin(R.TEST_BREID)].reset_index(drop=True)
wide_del = wide[~wide['BREID'].isin(R.TEST_BREID) & ~wide['RGIID'].isin(test_rgi)].reset_index(drop=True)
print('wide rows', len(wide), '-> after deleting test-glacier rows', len(wide_del),
      '| RGIIDs left that are test RGIIDs:', len(set(wide_del['RGIID']) & set(test_rgi)))
rows_del, _ = R.build_records(wide_del)
assert not rows_del['BREID'].isin(R.TEST_BREID).any()
p_full = R.predict(R.train(tr, 5, 0.05, 300, 0, 4, 'hist'), te)
p_del = R.predict(R.train(rows_del, 5, 0.05, 300, 0, 4, 'hist'), te)
print('train monthly rows: split', len(tr), '| deleted-input', len(rows_del))
print('test predictions bit-identical (split vs deleted-input training):', bool(np.array_equal(p_full, p_del)))
sc = R.score(R.aggregate(te['rid'].values, te['season'].values, te['balance'].values, p_del))
print('deleted-input model on test records:', R.fmt(sc))
