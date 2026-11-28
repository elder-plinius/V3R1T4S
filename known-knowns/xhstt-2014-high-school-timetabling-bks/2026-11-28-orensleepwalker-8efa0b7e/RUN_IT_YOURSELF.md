# Run it yourself
1. `sh verify-it-yourself/run_checks.sh` (expect PASS).
2. HSEval (Jeffrey Kingston's web evaluator, linked from the XHSTT pages at https://www.utwente.nl/en/eemcs/dmmp/hstt/): combine the downloaded instance file with our Solution element (object/*.xml holds one SolutionGroup for the instance) into one archive and submit it to HSEval's evaluation page; it reports infeasibility and objective per solution. We did not run it.
3. The search code is in how-we-built-it/code/ (OR-Tools CP-SAT; not deterministic with several workers).
