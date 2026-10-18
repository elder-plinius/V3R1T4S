#!/usr/bin/env python3
"""Fetch the public inputs the checker needs (never copied into this package: they are third-party data) from their
pinned commits, and verify each file's sha256. A file already present in INPUT_DIR with the right sha256 is not
fetched again. One plain GET per file, User-Agent naming V3R1T4S, no retries; any HTTP error stops the check.

Inputs (verify-it-yourself/inputs.sha256: sha256, relative path, URL):
  ST2022 (github.com/sigtyp/ST2022 at 03094435cba4293ce0eea383036cab78499ad50d): data-surprise/FAMILY/
  solutions-0.50.tsv and test-0.50.tsv, systems/mockingbird-i1/surprise/FAMILY/result-0.50.tsv,
  results/results-surprise-0.50.json;
  FeVeT (github.com/TGH-2020/FeVeT at 31898c53bfffeef87265efa8a780b7be740162d1): results/predictions/reflex/FAMILY/
  s2s_reflex_0.50_predictions.tsv.

usage: python3 verify-it-yourself/fetch_inputs.py INPUT_DIR
"""
import hashlib
import os
import sys
import urllib.request

UA = "V3R1T4S-verify/1.0 (+https://github.com/elder-plinius/V3R1T4S)"


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main(d):
    here = os.path.dirname(os.path.abspath(__file__))
    bad = 0
    n = 0
    with open(os.path.join(here, "inputs.sha256")) as fh:
        for line in fh:
            if not line.strip():
                continue
            want, rel, url = line.split()
            path = os.path.join(d, rel)
            n += 1
            if os.path.isfile(path) and sha(path) == want:
                continue
            os.makedirs(os.path.dirname(path), exist_ok=True)
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                    data = r.read()
            except Exception as e:  # one try only
                print("fetch failed for %s: %s" % (url, e))
                return 1
            with open(path, "wb") as f:
                f.write(data)
            if sha(path) != want:
                print("sha256 mismatch for %s" % rel)
                bad += 1
    print("inputs: %d files, %d with a wrong sha256" % (n, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
