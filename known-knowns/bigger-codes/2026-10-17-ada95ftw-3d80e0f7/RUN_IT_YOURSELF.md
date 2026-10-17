# Run it yourself
From this folder, in a fresh shell (Python 3.8+, standard library only):
```sh
sha256sum -c SHA256SUMS
sh verify-it-yourself/run_checks.sh
```
Expected output: the self-test line, one `column x=...` line per Johnson distance, `certified: A(34,10,8) <= 114444/185 = ...`, `VERIFIED bound 618`, then `PASS`.
Then open https://aeb.win.tue.nl/codes/Andw.html, section "Bounds on A(n,10,w)" / "Values of A(n,10,8)", and read the cell A(34,10,8) (upper bound 637 on 2026-10-17) and the input cell A(26,10,7).
To rebuild the object: see how-we-built-it/README.md (needs numpy and scipy, pinned in how-we-built-it/requirements.txt).
