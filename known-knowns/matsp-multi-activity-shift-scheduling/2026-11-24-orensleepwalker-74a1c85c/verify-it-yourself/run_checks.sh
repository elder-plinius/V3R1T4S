#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (POSIX shell, curl, sha256sum, Python 3 standard library)
set -u
failure() { printf '%s\n' FAIL; exit 1; }
sha256sum --check --quiet SHA256SUMS || failure
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
UA='V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)'
curl -fsSL --max-time 180 -A "$UA" -o "$tmp/instances1_225.zip" 'https://www.schedulingbenchmarks.org/matsp/data/instances1_225.zip' || failure
printf '%s  %s\n' '202ddbc48da844a404298f24edecc00f717c21e334e1dfe510e9b20d081cd556' "$tmp/instances1_225.zip" | sha256sum --check --quiet || failure
curl -fsSL --max-time 60 -A "$UA" -o "$tmp/example.xml" 'https://www.schedulingbenchmarks.org/matsp/data/8_7_20_2.Solution.889.xml' || failure
printf '%s  %s\n' 'ee1af323a538aa10af486ce87bb5d77d842fd01ebf3f571d85aae4222e31c27f' "$tmp/example.xml" | sha256sum --check --quiet || failure
python3 -I -c "import zipfile, sys; z = zipfile.ZipFile(sys.argv[1]); [open(sys.argv[2] + '/' + n.split('/')[-1], 'wb').write(z.read(n)) for n in z.namelist() if n.startswith('instances1_225/txt/') and n.endswith('.txt')]" "$tmp/instances1_225.zip" "$tmp" || failure
echo 'Example (site file, posted penalty 889; the evaluator must reproduce it):'
ex=$(PYTHONDONTWRITEBYTECODE=1 python3 -I verify-it-yourself/verify.py "$tmp/8_7_20_2.txt" "$tmp/example.xml" 890 | tail -2 | tr '\n' ' ')
echo "$ex"
case "$ex" in *"violations 0, penalty 889, record 890 PASS"*) ;; *) failure;; esac
bad=0; n=0
while read stem obj osha rec pen; do
  n=$((n+1))
  [ "$(sha256sum "$obj" | cut -d' ' -f1)" = "$osha" ] || { echo "$stem: sha256 mismatch"; bad=$((bad+1)); continue; }
  res=$(PYTHONDONTWRITEBYTECODE=1 python3 -I verify-it-yourself/verify.py "$tmp/$stem.txt" "$obj" "$rec" | tail -2 | tr '\n' ' ')
  echo "$stem: $res"
  case "$res" in *"violations 0, penalty $pen, record $rec PASS"*) ;; *) bad=$((bad+1));; esac
done < verify-it-yourself/expected.txt
echo "checked $n, failed $bad"
if [ "$bad" -eq 0 ] && [ "$n" -eq 123 ]; then printf '%s\n' PASS; else failure; fi
