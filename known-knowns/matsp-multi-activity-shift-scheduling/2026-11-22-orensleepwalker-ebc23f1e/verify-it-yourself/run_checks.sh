#!/bin/sh
set -eu
failure() { printf '%s\n' FAIL; exit 1; }
sha256sum --check --quiet SHA256SUMS || failure
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
UA='V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)'
curl -fsSL --max-time 180 -A "$UA" -o "$tmp/instances1_225.zip" 'https://www.schedulingbenchmarks.org/matsp/data/instances1_225.zip' || failure
printf '%s  %s\n' '202ddbc48da844a404298f24edecc00f717c21e334e1dfe510e9b20d081cd556' "$tmp/instances1_225.zip" | sha256sum --check --quiet || failure
curl -fsSL --max-time 60 -A "$UA" -o "$tmp/example.xml" 'https://www.schedulingbenchmarks.org/matsp/data/8_7_20_2.Solution.889.xml' || failure
printf '%s  %s\n' 'ee1af323a538aa10af486ce87bb5d77d842fd01ebf3f571d85aae4222e31c27f' "$tmp/example.xml" | sha256sum --check --quiet || failure
python3 -I -c "import zipfile, sys; z = zipfile.ZipFile(sys.argv[1]); [open(sys.argv[2] + '/' + n.split('/')[-1], 'wb').write(z.read(n)) for n in ('instances1_225/txt/8_7_20_2.txt', 'instances1_225/txt/155_28_10_2.txt')]" "$tmp/instances1_225.zip" "$tmp" || failure
echo 'Example (site file, posted penalty 889; the evaluator must reproduce it):'
PYTHONDONTWRITEBYTECODE=1 python3 -I verify-it-yourself/verify.py "$tmp/8_7_20_2.txt" "$tmp/example.xml" 890 || failure
echo 'Claimed roster against the best known 24:'
PYTHONDONTWRITEBYTECODE=1 python3 -I verify-it-yourself/verify.py "$tmp/155_28_10_2.txt" object/155_28_10_2.Solution.0.xml 24 || failure
printf '%s\n' PASS
