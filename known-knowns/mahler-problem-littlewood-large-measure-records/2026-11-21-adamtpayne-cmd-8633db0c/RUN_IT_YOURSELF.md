# Run it yourself (from this folder, fresh shell)

## Check (standard library only)
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`.

## Second, independent certification (needs `pip install python-flint mpmath`)
```sh
python3 how-we-built-it/certify.py $(cat object/littlewood_d40.txt) 6.153645888590
```
Expected (see `how-we-built-it/certify_output_d40.txt`): an Arb ball [6.15435589127620035908539751099 +/- 1.3e-33], an mpmath 60-digit value agreeing to more than 20 digits, and `certified M - table > 1e-9: True`.

## Rebuild (stochastic search)
```sh
python3 how-we-built-it/search.py 40 120 280
```
This prints the best polynomials found in 120 s. The object came from this unseeded run (seed 280); another seed or machine may return a different, possibly better, polynomial.
