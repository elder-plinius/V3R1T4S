"""Download the third-party files listed in third_party_sources.json, check every sha256, stop on the first mismatch.

Python 3.8+, standard library only. Run from this folder:  python fetch_third_party.py
Files are written to baseline/wit/ and status_source/ (the places surgery_baseline.py, derivability.py and
lb_closure.py expect). One plain request per URL, no retries. Nothing here is needed by verify-it-yourself/.
Saurabh's three matrices are extracted from https://arxiv.org/html/2608.26603v1: the first three <pre> blocks that
contain only lines of 0 and 1, in page order, one text file each (rows joined by LF, final LF).
"""
import hashlib
import json
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "V3R1T4S-fetch (plain request, stdlib)"


def sha256(b):
    return hashlib.sha256(b).hexdigest()


class PreBlocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.cur = []
        self.blocks = []

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            self.depth += 1
            self.cur = []

    def handle_endtag(self, tag):
        if tag == "pre" and self.depth:
            self.depth -= 1
            self.blocks.append("".join(self.cur))

    def handle_data(self, data):
        if self.depth:
            self.cur.append(data)


def extract_matrices(html_text):
    """Return the first three 0/1 <pre> blocks of the page, each as the bytes of a matrix text file."""
    p = PreBlocks()
    p.feed(html_text)
    out = []
    for blk in p.blocks:
        lines = [l.strip() for l in blk.splitlines() if l.strip()]
        if lines and all(re.fullmatch(r"[01]+", l) for l in lines):
            out.append(("\n".join(lines) + "\n").encode("ascii"))
    return out[:3]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def put(rel, data, want):
    got = sha256(data)
    if got != want:
        sys.exit("STOP: sha256 mismatch for %s\n  expected %s\n  got      %s" % (rel, want, got))
    path = os.path.join(HERE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    print("ok   %s" % rel)


def main():
    files = json.load(open(os.path.join(HERE, "third_party_sources.json")))["files"]
    page = None
    sau_order = [f for f in files if f["url"].startswith("https://arxiv.org/html/")]
    for f in files:
        if f in sau_order:
            continue
        put(f["file"], get(f["url"]), f["sha256"])
    if sau_order:
        page = get(sau_order[0]["url"]).decode("utf-8", "replace")
        mats = extract_matrices(page)
        if len(mats) != len(sau_order):
            sys.exit("STOP: found %d matrices on the arXiv page, expected %d" % (len(mats), len(sau_order)))
        for f, data in zip(sau_order, mats):
            put(f["file"], data, f["sha256"])
    print("ALL THIRD-PARTY FILES OK")


if __name__ == "__main__":
    main()
