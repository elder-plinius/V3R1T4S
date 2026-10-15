"""Hash-bound public-input acquisition and two independent exact evaluations."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import urllib.request
from datetime import datetime, timezone

import portfolio_check
import literal_check

ROOT=Path(__file__).resolve().parents[1]
EXPECTED_OBJECT='7bf097a5c2987de75318a75948fbfcbc24dbe9a59323beccb374d2dddfc2bac9'


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()


def acquire(cache):
    sources=json.loads((ROOT/'verify-it-yourself/SOURCES.json').read_text())
    paths={}
    cache.mkdir(parents=True,exist_ok=True)
    for name,source in sources.items():
        target=cache/name
        if target.exists():
            assert target.stat().st_size==source['bytes'] and sha(target)==source['sha256'], 'cached input mismatch: '+name
            print(json.dumps({'input':name,'source':'verified public-data cache','sha256':source['sha256']}))
        else:
            request=urllib.request.Request(source['url'],headers={'User-Agent':'V3R1T4S exact portfolio verifier'})
            started=datetime.now(timezone.utc).isoformat()
            # One request only. Any access error, mismatch, or timeout fails.
            with urllib.request.urlopen(request,timeout=240) as response:
                assert response.status==200,'source HTTP status is not 200'
                with target.open('wb') as out:
                    count=0
                    while True:
                        b=response.read(1048576)
                        if not b:break
                        count+=len(b);assert count<=source['bytes'],'oversized input'
                        out.write(b)
            assert target.stat().st_size==source['bytes'] and sha(target)==source['sha256'],'downloaded input mismatch: '+name
            print(json.dumps({'input':name,'url':source['url'],'utc':started,'http_status':200,'sha256':source['sha256'],'bytes':source['bytes']}))
        paths[name]=target
    return paths


def verify(cache):
    started=time.monotonic();obj=ROOT/'object/portfolio.sol'
    assert sha(obj)==EXPECTED_OBJECT,'candidate file hash mismatch'
    data=acquire(cache);prices=data['stock_prices.txt.gz'];cov=data['covariance_matrices.txt.gz']
    a=portfolio_check.check(prices,cov,obj,'po_a400_t10_s00',100,'0.01')
    b=literal_check.run(prices,cov,obj)
    assert a['feasible'] and a['objective']==b['objective']==-1696664
    assert a['components']==b['components']
    assert a['objective'] < -1090282
    print(json.dumps({'object_sha256':EXPECTED_OBJECT,'objective':a['objective'],
                     'components':a['components'],'reference_budget':100,
                     'risk_weight':'0.01','independent_evaluators_agree':True,
                     'seconds':round(time.monotonic()-started,3)},sort_keys=True))


def main():
    cache=os.environ.get('V3R1T4S_QOBLIB_CACHE')
    if cache:verify(Path(cache))
    else:
        with tempfile.TemporaryDirectory(prefix='qoblib-public-') as folder:verify(Path(folder))
    print('PASS')


if __name__=='__main__':
    try:main()
    except Exception as error:
        print('FAIL:',str(error));sys.exit(1)
