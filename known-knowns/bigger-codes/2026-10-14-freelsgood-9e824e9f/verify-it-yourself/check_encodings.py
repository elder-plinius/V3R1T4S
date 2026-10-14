from pathlib import Path
import hashlib
raw=Path('object/A27_6_10_13026.txt').read_bytes()
if hashlib.sha256(raw).hexdigest()!='9e824e9f8a92e74226231152fc8e8a972be5ba79549e2a10e512fe63a3934f49': raise SystemExit('FAIL: binary hash')
a=[int(x,2) for x in raw.splitlines()]
b=[int(x,16) for x in Path('object/a27.6.10.13026H').read_text().splitlines()]
if a!=b: raise SystemExit('FAIL: hex and binary differ')
print('ENCODINGS: PASS')
