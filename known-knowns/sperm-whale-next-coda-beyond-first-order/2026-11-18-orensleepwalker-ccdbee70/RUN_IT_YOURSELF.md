# Reproduce

Use a POSIX shell, curl, sha256sum, Python 3 and NumPy 2.5.4. Run `sh verify-it-yourself/run_checks.sh` from the package folder. Expect PASS.

The verifier needs only the pinned annotations at https://raw.githubusercontent.com/pratyushasharma/sw-combinatoriality/7228c8eed2cc27ddd23b74c51aeccec9d762389e/data/sperm-whale-dialogues.csv (SHA-256 1856c8bf915cc5ae6f928aaa2036cbbc6ad8840bb6e4f6a96aaeb96953215da2). It rebuilds N-gram probabilities using the author pipeline and checks frozen NPZ objects and control scores.

To rerun all controls, create a disposable working folder with code/, output/ and data/. Copy the three programs in how-we-built-it/code to code/ and download the pinned annotations to data/sperm-whale-dialogues.csv. Run `python3 code/controls.py dialogues payload` and `python3 code/controls.py dialogues first_order`. These are the two 400-seed runs. Use one numerical library thread on a shared machine.
