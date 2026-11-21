# Run it yourself (from this folder, fresh shell)

## Check (standard library only)
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`.

## Second, independent certification (needs `pip install python-flint mpmath`)
```sh
python3 how-we-built-it/certify.py $(cat object/littlewood_d36.txt) 5.823385551581
```
Expected (see `how-we-built-it/certify_output_d36.txt`): an Arb ball [5.86686085131976269716667397204 +/- 1.31e-31], an mpmath 60-digit value agreeing to more than 20 digits, and `certified M - table > 1e-9: True`.

## Rebuild (stochastic search)
```sh
python3 how-we-built-it/search.py 36 120 252
```
This prints the best polynomials found in 120 s. The object came from this unseeded run (seed 252); another seed or machine may return a different, possibly better, polynomial.
