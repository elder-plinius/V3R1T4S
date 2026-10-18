#!/usr/bin/env python3
"""One public GET per source, preserving raw body, status, time and errors."""
import concurrent.futures
import datetime
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEST = Path(__file__).resolve().parent
DEFAULT = {
    'lille-2x5x5.html': 'https://fmm.univ-lille.fr/2x5x5.html',
    'fmm_sota.json': 'https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json',
    'perminov-tree.json': 'https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1',
    'reduced_known.json': 'https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json',
    'perminov-README.md': 'https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md',
    'perminov-CHANGELOG.md': 'https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md',
    'catalog-COVERAGE.md': 'https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md',
    'veritas-pulls-open.json': 'https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100',
}

def fetch(item):
    filename, url = item
    meta = {'url': url, 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'method': 'GET', 'requests_attempted': 1}
    path = DEST / filename
    assert not path.with_name(path.name+'.fetch.json').exists(), 'Refusing repeat GET: '+url
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Criterion-Audit/1.0'})
        with urllib.request.urlopen(req, timeout=45) as response:
            body = response.read()
            meta.update(http_status=response.status, final_url=response.url, headers=dict(response.headers))
    except urllib.error.HTTPError as e:
        body = e.read()
        meta.update(http_status=e.code, final_url=e.url, headers=dict(e.headers), error=str(e))
    except Exception as e:
        body = b''
        meta.update(http_status=None, error=repr(e))
    meta.update(finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
    path.write_bytes(body)
    path.with_name(path.name+'.fetch.json').write_text(json.dumps(meta, indent=2)+'\n')
    return {'file': filename, 'url': url, 'http_status': meta['http_status'], 'bytes':len(body), 'error':meta.get('error')}

sources = DEFAULT if len(sys.argv) == 1 else json.loads(Path(sys.argv[1]).read_text())
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for result in pool.map(fetch, sources.items()):
        print(json.dumps(result))
