"""Fetch Zeng's public certificate (Zenodo 10.5281/zenodo.20528351, file certificate.zip) and verify it by md5 and sha256.

usage: python fetch_inputs.py DEST_DIR   (standard library only; needs network the first time)
The 765 MB file is cached in V3R1T4S_CACHE (default: <system temp>/v3r1t4s_zeng_cache); a cached copy is used only after
both hashes match. Writes DEST_DIR/certificate.zip (a copy). The download can take a while on a slow connection.
"""
import hashlib, os, shutil, sys, tempfile, urllib.request
URL = "https://zenodo.org/records/20528351/files/certificate.zip?download=1"
MD5 = "73b400c8c3b30f74fa9d6e971a5ddc65"
SHA256 = "5b4e2300ab7666893a861b537c02581826774d43b9326808dd0ef0e509f9cc69"
SIZE = 765065866
def ok(path):
    if not os.path.isfile(path) or os.path.getsize(path) != SIZE:
        return False
    m, s = hashlib.md5(), hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            m.update(b); s.update(b)
    return m.hexdigest() == MD5 and s.hexdigest() == SHA256
dest = sys.argv[1]
cache = os.environ.get("V3R1T4S_CACHE") or os.path.join(tempfile.gettempdir(), "v3r1t4s_zeng_cache")
os.makedirs(cache, exist_ok=True)
cached = os.path.join(cache, "certificate.zip")
if ok(cached):
    print("using cached copy, md5 and sha256 verified")
else:
    print("downloading", URL)
    req = urllib.request.Request(URL, headers={"User-Agent": "V3R1T4S-verify-it-yourself"})
    tmp = cached + ".part"
    with urllib.request.urlopen(req, timeout=600) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f, 1 << 22)
    if not ok(tmp):
        os.remove(tmp)
        sys.exit("download hash mismatch")
    os.replace(tmp, cached)
    print("downloaded, md5 and sha256 verified")
os.makedirs(dest, exist_ok=True)
shutil.copyfile(cached, os.path.join(dest, "certificate.zip"))
