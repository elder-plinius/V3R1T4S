# Run it yourself
From this folder, in a fresh shell (Python 3.8+, standard library only):
```sh
sha256sum -c SHA256SUMS
sh verify-it-yourself/run_checks.sh
```
Expected output: the self-test line, one `column x=...` line per Johnson distance, `certified: A(33,10,7) <= 26928/185 = ...`, `VERIFIED bound 145`, then `PASS`.
Then open https://aeb.win.tue.nl/codes/Andw.html, section "Bounds on A(n,10,w)" / "Values of A(n,10,7)", and read the cell A(33,10,7) (upper bound 150 on 2026-10-17) and the input cell A(26,10,7).
To rebuild the object: see how-we-built-it/README.md (needs numpy and scipy, pinned in how-we-built-it/requirements.txt).
