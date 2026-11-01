"""Fetch the public inputs of Mishra's certificate at the PINNED commit of the author's repository and verify them by sha256.

usage: python fetch_inputs.py DEST      (standard library only; needs network)
Writes DEST/cert_B_08344.bin (gunzipped; sha256 pinned), DEST/certB_test.bin (the author's small valid control certificate).
Source: https://github.com/Ujjwal238/universal-cover-problem at commit da956b117a5f876fc3c530db3e00673e6cb18865 (raw file URLs).
No author code is downloaded or run.
"""
import gzip, hashlib, os, sys, urllib.request
C = "da956b117a5f876fc3c530db3e00673e6cb18865"
BASE = "https://raw.githubusercontent.com/Ujjwal238/universal-cover-problem/%s/certificates/" % C
GZ_SHA = "600e5690a010bcc0cb5303a3d740c5c9012ca354a832e648ff26152e8d1916fa"
BIN_SHA = "33973342ab754dd5261b682d657e0b46b55f3377173a9238a2fa3948fefdb91f"
CTL_SHA = "fe2dd30b6c96115f30409f276928b254b1d84b54d35f263505f3161410d3d455"
def get(rel):
    req = urllib.request.Request(BASE + rel, headers={"User-Agent": "V3R1T4S-verify-it-yourself"})
    return urllib.request.urlopen(req, timeout=600).read()
dest = sys.argv[1]
os.makedirs(dest, exist_ok=True)
gz = get("cert_B_08344.bin.gz")
if hashlib.sha256(gz).hexdigest() != GZ_SHA:
    sys.exit("sha256 mismatch for cert_B_08344.bin.gz")
raw = gzip.decompress(gz)
if hashlib.sha256(raw).hexdigest() != BIN_SHA:
    sys.exit("sha256 mismatch for cert_B_08344.bin (uncompressed)")
open(os.path.join(dest, "cert_B_08344.bin"), "wb").write(raw)
ctl = get("controls/certB_test.bin")
if hashlib.sha256(ctl).hexdigest() != CTL_SHA:
    sys.exit("sha256 mismatch for certB_test.bin")
open(os.path.join(dest, "certB_test.bin"), "wb").write(ctl)
print("fetched and verified cert_B_08344.bin (%d bytes) and certB_test.bin from commit %s" % (len(raw), C[:8]))
