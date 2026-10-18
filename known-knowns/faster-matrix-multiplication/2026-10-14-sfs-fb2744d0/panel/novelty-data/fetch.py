import concurrent.futures
import datetime
import hashlib
import json
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent

def fetch(item):
    name, url = item.split('=', 1)
    path = ROOT / name
    meta = {'url': url, 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'file': name}
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Codex-Independent-Matrix-Multiplication-Audit/1.0'})
        with urllib.request.urlopen(request, timeout=35) as response:
            data = response.read()
            meta.update(http_status=response.status, final_url=response.geturl(), headers=dict(response.headers.items()))
    except urllib.error.HTTPError as error:
        data = error.read()
        meta.update(http_status=error.code, final_url=error.geturl(), headers=dict(error.headers.items()), error=str(error))
    except Exception as error:
        data = b''
        meta.update(http_status=None, error=repr(error))
    meta.update(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
    path.write_bytes(data)
    path.with_name(path.name + '.fetch.json').write_text(json.dumps(meta, indent=2) + '\n')
    return {key: meta[key] for key in ('file', 'http_status', 'utc', 'sha256', 'bytes')} | ({'error': meta['error']} if 'error' in meta else {})

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for result in pool.map(fetch, sys.argv[1:]):
            print(json.dumps(result))
